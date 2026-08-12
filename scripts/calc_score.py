#!/usr/bin/env python3
"""Calculate retrospective Contrarian Scores from classified historical calls.

v0.4 outputs:
- combined RAW
- ACTION / OPINION / UNKNOWN
- confidence buckets
- style-tag conditioned scores
- optional Style-Adjusted Scores using conservative shrinkage toward 50

This script performs retrospective statistics only.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

VALID_OUTCOMES = {
    "ORIGINAL_CORRECT",
    "CONTRARIAN_HIT",
    "FLAT",
    "UNVERIFIABLE",
    "UNSCORABLE",
}
VALID_EVENT_TYPES = {"ACTION", "OPINION", "UNKNOWN"}
VALID_ATTRIBUTION = {"TARGET", "THIRD_PARTY", "UNCERTAIN"}
TRANSFERABILITY_COMPONENTS = (
    "horizon_consistency",
    "action_opinion_consistency",
    "regime_stability",
    "directional_persistence",
    "corpus_representativeness",
)
BUCKETS = [
    (90, 100, "90-100", "VERY_HIGH"),
    (70, 89, "70-89", "HIGH"),
    (50, 69, "50-69", "MEDIUM"),
    (30, 49, "30-49", "LOW"),
    (10, 29, "10-29", "VERY_LOW"),
    (0, 9, "0-9", "TRACE"),
]


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054):
    if total <= 0:
        return None
    p = successes / total
    z2 = z * z
    denom = 1 + z2 / total
    center = (p + z2 / (2 * total)) / denom
    margin = (z / denom) * math.sqrt((p * (1 - p) / total) + (z2 / (4 * total * total)))
    return max(0.0, center - margin), min(1.0, center + margin)


def sample_strength(n: int) -> str:
    if n < 5:
        return "INSUFFICIENT"
    if n < 10:
        return "VERY_LOW"
    if n < 20:
        return "LOW"
    if n < 50:
        return "MEDIUM"
    return "HIGH"


def score_subset(calls: list[dict[str, Any]]) -> dict[str, Any]:
    original = sum(1 for c in calls if c.get("outcome") == "ORIGINAL_CORRECT")
    contrarian = sum(1 for c in calls if c.get("outcome") == "CONTRARIAN_HIT")
    scored = original + contrarian
    if scored == 0:
        return {
            "scored_calls": 0,
            "original_correct": 0,
            "contrarian_hits": 0,
            "original_accuracy": None,
            "contrarian_score": None,
            "sample_strength": "INSUFFICIENT",
            "contrarian_score_wilson_95": None,
        }
    original_accuracy = original / scored * 100
    contrarian_score = contrarian / scored * 100
    interval = wilson_interval(contrarian, scored)
    return {
        "scored_calls": scored,
        "original_correct": original,
        "contrarian_hits": contrarian,
        "original_accuracy": round(original_accuracy, 1),
        "contrarian_score": round(contrarian_score, 1),
        "sample_strength": sample_strength(scored),
        "contrarian_score_wilson_95": [round(interval[0] * 100, 1), round(interval[1] * 100, 1)] if interval else None,
    }


def confidence_bucket(value: float):
    if value < 0 or value > 100:
        raise ValueError(f"opinion_confidence must be between 0 and 100; received {value}")
    for low, high, key, label in BUCKETS:
        if low <= value <= high:
            return low, high, key, label
    raise AssertionError("Unreachable confidence bucket")


def bucket_results(calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = {key: [] for _, _, key, _ in BUCKETS}
    for call in calls:
        value = call.get("opinion_confidence")
        if value is None:
            continue
        _, _, key, _ = confidence_bucket(float(value))
        grouped[key].append(call)
    return [
        {"range": key, "label": label, "candidate_calls": len(grouped[key]), **score_subset(grouped[key])}
        for _, _, key, label in BUCKETS
    ]


def normalize_style_tag(value: str) -> str:
    tag = value.strip().upper().replace("-", "_").replace(" ", "_")
    if not tag or not re.fullmatch(r"[A-Z0-9_]+", tag):
        raise ValueError(f"style tag must be a non-empty alphanumeric/underscore label; received {value!r}")
    return tag


def style_tag_results(calls: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for call in calls:
        for tag in call.get("style_tags", []):
            grouped.setdefault(tag, []).append(call)
    return {
        tag: {"candidate_calls": len(grouped[tag]), **score_subset(grouped[tag])}
        for tag in sorted(grouped)
    }


def normalize_and_validate(calls: list[dict[str, Any]]):
    normalized = []
    confidence_missing = 0
    event_type_missing = 0
    style_tags_missing = 0

    for index, original_call in enumerate(calls):
        call = dict(original_call)

        outcome = str(call.get("outcome", "")).upper()
        if outcome not in VALID_OUTCOMES:
            raise ValueError(f"calls[{index}].outcome must be one of {sorted(VALID_OUTCOMES)}; received {outcome!r}")
        call["outcome"] = outcome

        raw_event_type = call.get("event_type")
        if raw_event_type is None:
            event_type_missing += 1
            event_type = "UNKNOWN"
        else:
            event_type = str(raw_event_type).upper()
            if event_type not in VALID_EVENT_TYPES:
                raise ValueError(f"calls[{index}].event_type must be one of {sorted(VALID_EVENT_TYPES)}; received {event_type!r}")
        call["event_type"] = event_type

        raw_attribution = call.get("attribution")
        if raw_attribution is not None:
            attribution = str(raw_attribution).upper()
            if attribution not in VALID_ATTRIBUTION:
                raise ValueError(f"calls[{index}].attribution must be one of {sorted(VALID_ATTRIBUTION)}; received {attribution!r}")
            call["attribution"] = attribution
            if outcome in {"ORIGINAL_CORRECT", "CONTRARIAN_HIT"} and attribution != "TARGET":
                raise ValueError(
                    f"calls[{index}] is scored but attribution={attribution}; only TARGET records may enter target scores"
                )

        if call.get("opinion_confidence") is None:
            confidence_missing += 1
        else:
            value = call.get("opinion_confidence")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"calls[{index}].opinion_confidence must be a number from 0 to 100")
            confidence_bucket(float(value))

        raw_tags = call.get("style_tags")
        if raw_tags is None:
            style_tags_missing += 1
            call["style_tags"] = []
        else:
            if not isinstance(raw_tags, list) or not all(isinstance(x, str) for x in raw_tags):
                raise ValueError(f"calls[{index}].style_tags must be an array of strings")
            call["style_tags"] = sorted({normalize_style_tag(x) for x in raw_tags})

        normalized.append(call)

    return normalized, confidence_missing, event_type_missing, style_tags_missing


def validate_style_profile(style_profile: dict[str, Any] | None) -> dict[str, Any] | None:
    if style_profile is None:
        return None
    if not isinstance(style_profile, dict):
        raise ValueError("style_profile must be a JSON object")

    profile = dict(style_profile)
    components = profile.get("style_transferability_components")
    if components is None:
        profile["style_transferability"] = None
        return profile
    if not isinstance(components, dict):
        raise ValueError("style_transferability_components must be a JSON object")

    missing = [name for name in TRANSFERABILITY_COMPONENTS if name not in components]
    if missing:
        profile["style_transferability"] = None
        profile["style_transferability_missing_components"] = missing
        return profile

    values = []
    normalized_components = {}
    for name in TRANSFERABILITY_COMPONENTS:
        value = components[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 100:
            raise ValueError(f"style_transferability_components.{name} must be a number from 0 to 100")
        normalized_components[name] = round(float(value), 1)
        values.append(float(value))

    profile["style_transferability_components"] = normalized_components
    profile["style_transferability"] = round(sum(values) / len(values), 1)
    return profile


def style_adjusted(base: dict[str, Any], transferability: float | None) -> dict[str, Any] | None:
    if transferability is None or base.get("contrarian_score") is None:
        return None
    empirical = float(base["contrarian_score"])
    adjusted = 50 + (empirical - 50) * transferability / 100
    return {
        "empirical_contrarian_score": round(empirical, 1),
        "style_transferability": round(transferability, 1),
        "style_adjusted_contrarian_score": round(adjusted, 1),
        "scored_calls": base.get("scored_calls", 0),
        "sample_strength": base.get("sample_strength"),
    }


def calculate(calls: list[dict[str, Any]], style_profile: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized, confidence_missing, event_type_missing, style_tags_missing = normalize_and_validate(calls)
    profile = validate_style_profile(style_profile)

    counts = {name: 0 for name in VALID_OUTCOMES}
    for call in normalized:
        counts[call["outcome"]] += 1

    action_calls = [c for c in normalized if c["event_type"] == "ACTION"]
    opinion_calls = [c for c in normalized if c["event_type"] == "OPINION"]
    unknown_calls = [c for c in normalized if c["event_type"] == "UNKNOWN"]

    raw = score_subset(normalized)
    action_score = score_subset(action_calls)
    opinion_score = score_subset(opinion_calls)
    unknown_score = score_subset(unknown_calls)

    transferability = profile.get("style_transferability") if profile else None

    return {
        "schema_version": "0.4.0",
        "candidate_calls": len(normalized),
        "counts": counts,
        "raw": raw,
        "by_event_type": {
            "ACTION": {"candidate_calls": len(action_calls), **action_score},
            "OPINION": {"candidate_calls": len(opinion_calls), **opinion_score},
            "UNKNOWN": {"candidate_calls": len(unknown_calls), **unknown_score},
        },
        "confidence_buckets": bucket_results(normalized),
        "confidence_buckets_by_event_type": {
            "ACTION": bucket_results(action_calls),
            "OPINION": bucket_results(opinion_calls),
        },
        "by_style_tag": style_tag_results(normalized),
        "by_style_tag_and_event_type": {
            "ACTION": style_tag_results(action_calls),
            "OPINION": style_tag_results(opinion_calls),
        },
        "style_profile": profile,
        "style_adjusted": {
            "RAW": style_adjusted(raw, transferability),
            "ACTION": style_adjusted(action_score, transferability),
            "OPINION": style_adjusted(opinion_score, transferability),
        },
        "confidence_missing_calls": confidence_missing,
        "event_type_missing_calls": event_type_missing,
        "style_tags_missing_calls": style_tags_missing,
    }


def load_payload(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        calls = data.get("calls")
        style_profile = data.get("style_profile")
    else:
        calls = data
        style_profile = None
    if not isinstance(calls, list):
        raise ValueError("Input must be a JSON array or an object containing a `calls` array.")
    if not all(isinstance(item, dict) for item in calls):
        raise ValueError("Every item in `calls` must be a JSON object.")
    return calls, style_profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate retrospective empirical and style-conditioned Contrarian Scores.")
    parser.add_argument("input", type=Path, help="JSON file containing classified historical calls")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()
    try:
        calls, style_profile = load_payload(args.input)
        result = calculate(calls, style_profile)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
