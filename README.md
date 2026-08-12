# Contrarian Signal Skill

![Agent Skill CI](https://github.com/GoodLoongStudio/contrarian-signal-skill/actions/workflows/ci.yml/badge.svg)

A portable Agent Skill for retrospectively measuring whether a public market commentator has functioned as a contrarian indicator.

## v0.3 highlights

The score is no longer a single undifferentiated number. The skill now separates:

- **RAW** — every scored directional record, no confidence threshold;
- **ACTION** — the target's own actual buy/sell/hold/reduce/clear-position actions;
- **OPINION** — directional market views without a position change;
- **confidence buckets** — 90-100, 70-89, 50-69, 30-49, 10-29, 0-9;
- **attribution** — TARGET vs THIRD_PARTY vs UNCERTAIN.

This prevents fan submissions, reposts, ordinary opinions, and actual trades from being mixed into one misleading statistic.

## Core metric

```text
Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

Sample size never modifies the numerical score; sample strength and Wilson confidence intervals are reported separately.

## Default retrospective workflow

1. review reachable public market-related content from the previous 365 days;
2. resolve whether each record is the target's own statement/action;
3. classify `event_type` as ACTION / OPINION / UNKNOWN;
4. extract BULLISH / BEARISH / NEUTRAL / UNSCORABLE direction;
5. assign `opinion_confidence` before checking later prices;
6. freeze the evaluation horizon before outcome lookup;
7. deduplicate repeated theses/actions;
8. verify later market prices;
9. calculate RAW, ACTION, OPINION, and confidence-bucket scores;
10. report evidence, exclusions, sample strength, Wilson intervals, and coverage limitations.

## Horizon policy

To prevent hindsight selection:

- ACTION without an explicit horizon -> next trading-session close (24h for 24/7 markets);
- OPINION -> explicit horizon when present; otherwise deterministic wording mapping; default 5 trading days when no time wording exists;
- optional longer-horizon diagnostics may be shown separately, but cannot replace the frozen primary score after outcomes are known.

## Repository layout

```text
contrarian-signal-skill/
├── SKILL.md
├── README.md
├── scripts/
│   └── calc_score.py
├── references/
│   ├── event-model.md
│   └── scoring-rules.md
├── assets/
│   └── report-template.md
└── tests/
    └── test_calc_score.py
```

## Example requests

```text
看看这个人过去一年是不是反指。
```

```text
把他的实际买卖动作和普通观点分开算反指指数。
```

```text
把 90%-100%、70%-89% 等置信度分桶列出来，再给一个不限置信度 RAW 分数。
```

## Calculator input

```json
{
  "calls": [
    {
      "outcome": "CONTRARIAN_HIT",
      "event_type": "ACTION",
      "attribution": "TARGET",
      "opinion_confidence": 98
    },
    {
      "outcome": "ORIGINAL_CORRECT",
      "event_type": "OPINION",
      "attribution": "TARGET",
      "opinion_confidence": 75
    }
  ]
}
```

Run:

```bash
python3 scripts/calc_score.py calls.json --pretty
```

The JSON output contains:

- `raw`
- `by_event_type.ACTION`
- `by_event_type.OPINION`
- `by_event_type.UNKNOWN`
- `confidence_buckets`
- `confidence_buckets_by_event_type.ACTION`
- `confidence_buckets_by_event_type.OPINION`
- missing-field audit counts

## Data-integrity guards

- A scored record with `attribution=THIRD_PARTY` or `UNCERTAIN` is rejected by the calculator.
- Missing legacy `event_type` is retained as `UNKNOWN` rather than silently guessed.
- Repeated substantially identical calls are deduplicated.
- Event type, attribution, direction, confidence, and horizon must be frozen before outcome lookup.
- Viral/embarrassing examples must not be cherry-picked as a substitute for reachable corpus coverage.

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

CI also validates the Agent Skill and runs the calculator tests on pushes and pull requests.

## Version

Current Skill version: **0.3.0**
