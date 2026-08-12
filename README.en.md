# Contrarian Signal

An Agent Skill for **retrospective public-market opinion backtesting and behavioral calibration**.

It reviews a public account's market commentary and disclosed actions over a historical window, separates ACTION from OPINION, freezes direction/confidence/horizon/style before looking at outcomes, and produces auditable historical contrarian-hit statistics.

> Research support only. Not investment advice. No trade execution, order instructions, portfolio sizing, or future-return promises.

## v0.5 highlights

- separate RAW / ACTION / OPINION empirical scores;
- opinion-clarity buckets: 90-100, 70-89, 50-69, 30-49, 10-29, 0-9;
- style-conditioned backtests for THESIS, MOMENTUM, DIP_BUY, BREAKOUT_CHASE, RAPID_REVERSAL and more;
- optional Style-Adjusted Score for conservative transferability interpretation;
- attribution gate: TARGET / THIRD_PARTY / UNCERTAIN;
- evidence ladder: Strong / Medium / Weak / Needs checking;
- explicit investment-research and public-person evaluation boundaries;
- release-grade `evals/`, `agents/`, validator, SECURITY and CHANGELOG.

## Core metric

```text
Contrarian Score =
CONTRARIAN_HIT /
(CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

The score describes historical samples only. Sample size, personal style, leverage and reputation never silently rewrite the empirical score.

## Benchmark methodology cases

The first public methodology benchmarks include:

- Weibo: **峰哥亡命天涯** — used to test ACTION classification, rapid reversals, chase/clear-position behavior, attribution, and viral-example bias;
- X: **@aleabitoreddit (Serenity)** — used to test long-horizon THESIS versus short-horizon ACTION/TIMING separation.

Benchmarks validate the method. They are not personal character judgments and are not future trading signals.

## Repository layout

```text
contrarian-signal-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── README.en.md
├── SECURITY.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── report-template.md
├── evals/
│   └── test-cases.md
├── examples/
│   └── benchmark-safe-output.md
├── references/
│   ├── risk-and-compliance.md
│   ├── evidence-ladder.md
│   ├── research-sources.md
│   ├── public-person-evaluation.md
│   ├── event-model.md
│   ├── scoring-rules.md
│   └── style-model.md
├── scripts/
│   ├── calc_score.py
│   └── validate_skill.py
└── tests/
    └── test_calc_score.py
```

## Run the calculator

```bash
python3 scripts/calc_score.py calls.json --pretty
```

## Validate locally

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests -p 'test_*.py'
```

GitHub Actions runs unit tests, the repository validator and the official Agent Skill specification validator.

Current version: **0.5.0**
