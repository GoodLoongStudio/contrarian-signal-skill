#!/usr/bin/env python3
"""Calculate retrospective Contrarian Score from classified historical calls.

Input is a JSON array or an object with a `calls` array. Each call must contain
an `outcome` value. Recognized outcomes are ORIGINAL_CORRECT, CONTRARIAN_HIT,
FLAT, UNVERIFIABLE, and UNSCORABLE.

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


def calculate(calls: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {name: 0 for name in VALID}

    for index, call in enumerate(calls):
        outcome = str(call.get("outcome", "")).upper()
        if outcome not in VALID:
            raise ValueError(
                f"calls[{index}].outcome must be one of {sorted(VALID)}; received {outcome!r}"
            )
        counts[outcome] += 1

    original = counts["ORIGINAL_CORRECT"]
    contrarian = counts["CONTRARIAN_HIT"]
    scored = original + contrarian

    if scored == 0:
        original_accuracy = None
        contrarian_score = None
        interval = None
    else:
        original_accuracy = original / scored * 100
        contrarian_score = contrarian / scored * 100
        interval = wilson_interval(contrarian, scored)

    return {
        "candidate_calls": len(calls),
        "scored_calls": scored,
        "counts": counts,
        "original_accuracy": None if original_accuracy is None else round(original_accuracy, 1),
        "contrarian_score": None if contrarian_score is None else round(contrarian_score, 1),
        "sample_strength": sample_strength(scored),
        "contrarian_score_wilson_95": None
        if interval is None
        else [round(interval[0] * 100, 1), round(interval[1] * 100, 1)],
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
    parser = argparse.ArgumentParser(description="Calculate a retrospective Contrarian Score.")
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
