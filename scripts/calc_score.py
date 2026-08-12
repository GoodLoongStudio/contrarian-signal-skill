#!/usr/bin/env python3
"""Calculate retrospective Contrarian Scores from classified historical calls.

v0.3 adds event-type splits:
- combined RAW
- ACTION
- OPINION
- confidence buckets overall
- confidence buckets inside ACTION and OPINION

This script performs retrospective statistics only.
"""

from __future__ import annotations

import argparse
import json
import math
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
    original = sum(1 for c in calls if str(c.get("outcome", "")).upper() == "ORIGINAL_CORRECT")
    contrarian = sum(1 for c in calls if str(c.get("outcome", "")).upper() == "CONTRARIAN_HIT")
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


def normalize_and_validate(calls: list[dict[str, Any]]):
    normalized = []
    confidence_missing = 0
    event_type_missing = 0
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
        normalized.append(call)
    return normalized, confidence_missing, event_type_missing


def calculate(calls: list[dict[str, Any]]) -> dict[str, Any]:
    normalized, confidence_missing, event_type_missing = normalize_and_validate(calls)
    counts = {name: 0 for name in VALID_OUTCOMES}
    for call in normalized:
        counts[call["outcome"]] += 1

    action_calls = [c for c in normalized if c["event_type"] == "ACTION"]
    opinion_calls = [c for c in normalized if c["event_type"] == "OPINION"]
    unknown_calls = [c for c in normalized if c["event_type"] == "UNKNOWN"]

    return {
        "schema_version": "0.3.0",
        "candidate_calls": len(normalized),
        "counts": counts,
        "raw": score_subset(normalized),
        "by_event_type": {
            "ACTION": {"candidate_calls": len(action_calls), **score_subset(action_calls)},
            "OPINION": {"candidate_calls": len(opinion_calls), **score_subset(opinion_calls)},
            "UNKNOWN": {"candidate_calls": len(unknown_calls), **score_subset(unknown_calls)},
        },
        "confidence_buckets": bucket_results(normalized),
        "confidence_buckets_by_event_type": {
            "ACTION": bucket_results(action_calls),
            "OPINION": bucket_results(opinion_calls),
        },
        "confidence_missing_calls": confidence_missing,
        "event_type_missing_calls": event_type_missing,
    }


def load_calls(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    calls = data.get("calls") if isinstance(data, dict) else data
    if not isinstance(calls, list):
        raise ValueError("Input must be a JSON array or an object containing a `calls` array.")
    if not all(isinstance(item, dict) for item in calls):
        raise ValueError("Every item in `calls` must be a JSON object.")
    return calls


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate retrospective raw, event-type, and confidence-bucket Contrarian Scores.")
    parser.add_argument("input", type=Path, help="JSON file containing classified historical calls")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()
    try:
        result = calculate(load_calls(args.input))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
