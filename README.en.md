# Contrarian Signal — Agent Skill for Market Commentator Backtesting

An open Agent Skill for **retrospective market-opinion backtesting, contrarian-signal analysis, social-media investment research, and behavioral calibration of public market commentators**.

Contrarian Signal reviews public market commentary and disclosed actions over a historical window, separates ACTION from OPINION, freezes direction, opinion clarity, horizon, and style before looking at outcomes, and produces auditable historical contrarian-hit statistics using verified market data.

It is designed for questions such as: **“Was this finance creator historically a contrarian indicator?” “How accurate were this commentator's public market calls?” “Did their disclosed actions match their public opinions?”**

> Research support only. Not investment advice. No trade execution, order instructions, portfolio sizing, leverage recommendations, or future-return promises.

## Install

```bash
npx skills add GoodLoongStudio/contrarian-signal-skill
```

Or install directly from GitHub:

```bash
npx skills add https://github.com/GoodLoongStudio/contrarian-signal-skill
```

## Use cases

- historical **contrarian indicator** analysis for finance creators and market commentators;
- backtesting public investment opinions from **X / Twitter, Weibo, and other public social media**;
- separating disclosed trading ACTION from directional OPINION;
- measuring historical call accuracy across opinion-clarity buckets;
- behavioral-finance research on thesis, momentum, dip-buying, breakout chasing, and rapid reversals;
- attribution checks that prevent reposts, fan submissions, or quoted third-party views from being scored as the target's own call;
- auditable historical reports with evidence strength, sample strength, 95% Wilson intervals, and coverage limits.

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

The score describes historical samples only. Sample size, personal style, leverage, and reputation never silently rewrite the empirical score.

## Benchmark methodology cases

The first public methodology benchmarks include:

- Weibo: **峰哥亡命天涯** — used to test ACTION classification, rapid reversals, chase/clear-position behavior, attribution, and viral-example bias;
- X: **@aleabitoreddit (Serenity)** — used to test long-horizon THESIS versus short-horizon ACTION/TIMING separation.

Benchmarks validate the method. They are not personal character judgments and are not future trading signals.

## FAQ

### What is a Contrarian Score?

It is the historical share of scorable directional records that moved opposite to the commentator's frozen direction under a predefined observation window. It is a retrospective statistic, not a forecast probability.

### Can it backtest finance creators on X / Twitter or Weibo?

Yes, when the public evidence can be reliably attributed to the target and the timestamp, asset, direction, and observation horizon can be recovered. Records with insufficient evidence are excluded rather than forced into the score.

### Is this a trading-signal generator?

No. The Skill is for public-information research, historical backtesting, and behavioral calibration. It does not generate personalized trades, positions, leverage instructions, or return guarantees.

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

GitHub Actions runs unit tests, the repository validator, and the Agent Skill specification validator.

Current version: **0.5.0**

If this project is useful to your research, consider giving it a **GitHub Star ⭐** so more Agent Skill users can discover it.
