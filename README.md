# Contrarian Signal Skill

![Agent Skill CI](https://github.com/GoodLoongStudio/contrarian-signal-skill/actions/workflows/ci.yml/badge.svg)

A portable Agent Skill for retrospectively measuring whether a public market commentator has functioned as a contrarian indicator.

## What it does

Given a specific public person/account, the skill:

1. reviews public market-related posts from the previous 365 days by default;
2. extracts only objectively testable bullish/bearish calls;
3. freezes the asset, direction, and evaluation horizon before checking later prices;
4. verifies the historical outcome with market-price data;
5. deduplicates repeated calls;
6. calculates the person's original directional accuracy and the opposite-side historical hit rate;
7. reports the result as a transparent `Contrarian Score` from 0 to 100 with sample size, confidence interval, evidence, exclusions, and coverage limitations.

The core metric is:

```text
Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

Example: if 32 historical calls are scorable and the opposite direction would have been correct on 24 of them, the Contrarian Score is `75.0`.

## Repository layout

```text
contrarian-signal-skill/
├── SKILL.md
├── README.md
├── scripts/
│   └── calc_score.py
├── references/
│   └── scoring-rules.md
└── assets/
    └── report-template.md
```

## Agent Skills compatibility

This repository follows the open Agent Skills directory format:

- `SKILL.md` contains discovery metadata and the main workflow.
- `references/` contains detailed rules loaded when needed.
- `scripts/` contains deterministic executable helpers.
- `assets/` contains reusable output templates.

The skill requires access to public web/social content and historical market-price data. The included calculator itself uses only the Python standard library.

## Example requests

```text
看看 @some-account 过去一年是不是反指。
```

```text
统计这个博主过去 365 天所有能验证的看多看空观点，给我 Contrarian Score 和证据表。
```

```text
Backtest this public commentator's directional calls over the last year and calculate the Contrarian Score.
```

## Deterministic calculator

The agent can save classified historical calls to JSON and run:

```bash
python3 scripts/calc_score.py calls.json --pretty
```

Minimal input:

```json
{
  "calls": [
    {"outcome": "CONTRARIAN_HIT"},
    {"outcome": "CONTRARIAN_HIT"},
    {"outcome": "ORIGINAL_CORRECT"},
    {"outcome": "FLAT"}
  ]
}
```

Example output:

```json
{
  "candidate_calls": 4,
  "scored_calls": 3,
  "counts": {
    "ORIGINAL_CORRECT": 1,
    "CONTRARIAN_HIT": 2,
    "FLAT": 1,
    "UNVERIFIABLE": 0,
    "UNSCORABLE": 0
  },
  "original_accuracy": 33.3,
  "contrarian_score": 66.7,
  "sample_strength": "INSUFFICIENT",
  "contrarian_score_wilson_95": [20.8, 93.9]
}
```

## Design principles

- **Auditable:** every scored call should be traceable to a public source and historical-price source.
- **No cherry-picking:** incomplete corpus coverage must be disclosed.
- **No hindsight leakage:** classification and horizon are frozen before later prices are checked.
- **No duplicate inflation:** repeated versions of the same thesis are deduplicated.
- **Score stays interpretable:** sample size affects reported evidence strength, not the 0-100 score itself.
- **Retrospective by default:** this project measures historical accuracy; it does not claim that historical inverse performance guarantees future outcomes.

## Version

Current Skill version: `0.1.0`
