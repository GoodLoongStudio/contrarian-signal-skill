#!/usr/bin/env python3
"""Calculate retrospective Contrarian Scores from classified historical calls.

Input is a JSON array or an object with a `calls` array. Each call must contain
an `outcome` value. Directional calls may also contain `opinion_confidence`
from 0 to 100.

The script always calculates a RAW Contrarian Score from all scored calls,
regardless of opinion confidence. When confidence is present, it also reports
separate scores for fixed confidence buckets.

This script performs retrospective statistics only. It does not generate a
current trading recommendation.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

VALID = {
    "ORIGINAL_CORRECT",
    "CONTRARIAN_HIT",
    "FLAT",
    "UNVERIFIABLE",
    "UNSCORABLE",
}

BUCKETS = [
    (90, 100, "90-100", "VERY_HIGH"),
    (70, 89, "70-89", "HIGH"),
    (50, 69, "50-69", "MEDIUM"),
    (30, 49, "30-49", "LOW"),
    (10, 29, "10-29", "VERY_LOW"),
    (0, 9, "0-9", "TRACE"),
]


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float] | None:
    """Return a two-sided 95% Wilson interval for a binomial proportion."""
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
    original = sum(1 for call in calls if str(call.get("outcome", "")).upper() == "ORIGINAL_CORRECT")
    contrarian = sum(1 for call in calls if str(call.get("outcome", "")).upper() == "CONTRARIAN_HIT")
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


def confidence_bucket(value: float) -> tuple[int, int, str, str]:
    if value < 0 or value > 100:
        raise ValueError(f"opinion_confidence must be between 0 and 100; received {value}")
    for low, high, key, label in BUCKETS:
        if low <= value <= high:
            return low, high, key, label
    raise AssertionError("Unreachable confidence bucket")


def calculate(calls: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {name: 0 for name in VALID}
    bucket_calls: dict[str, list[dict[str, Any]]] = {key: [] for _, _, key, _ in BUCKETS}
    confidence_missing = 0

    for index, call in enumerate(calls):
        outcome = str(call.get("outcome", "")).upper()
        if outcome not in VALID:
            raise ValueError(
                f"calls[{index}].outcome must be one of {sorted(VALID)}; received {outcome!r}"
            )
        counts[outcome] += 1

        if "opinion_confidence" not in call or call.get("opinion_confidence") is None:
            confidence_missing += 1
            continue

        value = call.get("opinion_confidence")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"calls[{index}].opinion_confidence must be a number from 0 to 100")
        _, _, key, _ = confidence_bucket(float(value))
        bucket_calls[key].append(call)

    raw = score_subset(calls)

    buckets: list[dict[str, Any]] = []
    for low, high, key, label in BUCKETS:
        subset = bucket_calls[key]
        bucket_result = score_subset(subset)
        buckets.append(
            {
                "range": key,
                "label": label,
                "candidate_calls": len(subset),
                **bucket_result,
            }
        )

    return {
        "candidate_calls": len(calls),
        "counts": counts,
        "raw": raw,
        "confidence_buckets": buckets,
        "confidence_missing_calls": confidence_missing,
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
    parser = argparse.ArgumentParser(description="Calculate retrospective raw and confidence-bucket Contrarian Scores.")
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
