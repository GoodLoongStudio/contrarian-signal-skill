# Contrarian Signal Skill

![Agent Skill CI](https://github.com/GoodLoongStudio/contrarian-signal-skill/actions/workflows/ci.yml/badge.svg)

A portable Agent Skill for retrospectively measuring whether a public market commentator has functioned as a contrarian indicator — while separating bad direction from bad timing, leverage, concentration, and personal trading style.

## v0.4 highlights

The skill now has three analysis layers:

- **Empirical scores:** RAW, ACTION, OPINION, and confidence buckets;
- **Style-conditioned scores:** historical inverse-hit rates for recurring behaviors such as THESIS, CATALYST, DIP_BUY, BREAKOUT_CHASE, MOMENTUM, RAPID_REVERSAL, etc.;
- **Style-Adjusted Score:** optional conservative generalization score that shrinks unstable historical patterns toward neutral 50.

This matters because a person can have accurate long-horizon research but poor short-horizon entries, or vice versa.

## Core empirical metric

```text
Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

Sample size and personal style never rewrite this empirical number.

## Style-adjusted metric

When a sufficiently broad corpus supports all five style-transferability dimensions:

```text
style_transferability = mean(
  horizon_consistency,
  action_opinion_consistency,
  regime_stability,
  directional_persistence,
  corpus_representativeness
)

Style-Adjusted Score =
  50 + (Empirical Contrarian Score - 50) * style_transferability / 100
```

Example: empirical Contrarian Score `80`, style transferability `50` -> Style-Adjusted Score `65`.

The adjustment never replaces the historical `80`; it communicates that the pattern is only moderately transferable.

## Personal style model

Calls can contain zero or more `style_tags`, assigned before checking outcomes. Recommended tags include:

- `THESIS`
- `CATALYST`
- `MOMENTUM`
- `MEAN_REVERSION`
- `DIP_BUY`
- `BREAKOUT_CHASE`
- `VALUE`
- `MACRO`
- `NEWS_REACTION`
- `HIGH_CONVICTION`
- `LEVERAGED`
- `CONCENTRATED`
- `RAPID_REVERSAL`
- `LONG_HORIZON`
- `SHORT_HORIZON`

The report also summarizes a primary archetype such as `THESIS_DRIVEN`, `CATALYST_TRADER`, `MOMENTUM_TRADER`, `VALUE_INVESTOR`, `HIGH_CONVICTION_CONCENTRATED`, `RAPID_REVERSAL_TRADER`, or `MIXED`.

Risk amplifiers such as leverage and concentration are reported separately. They can explain drawdowns but do not automatically imply contrarian behavior.

## Default retrospective workflow

1. review reachable public market-related content from the previous 365 days;
2. resolve attribution: TARGET / THIRD_PARTY / UNCERTAIN;
3. classify `event_type`: ACTION / OPINION / UNKNOWN;
4. extract BULLISH / BEARISH / NEUTRAL / UNSCORABLE direction;
5. assign `opinion_confidence` before checking prices;
6. assign style tags before checking prices;
7. freeze the evaluation horizon;
8. deduplicate repeated theses/actions;
9. verify later market prices;
10. calculate RAW, ACTION, OPINION, confidence-bucket, and style-conditioned scores;
11. build the Personal Style Profile;
12. optionally calculate Style-Adjusted Scores when all transferability dimensions are justified.

## Horizon policy

To prevent hindsight selection:

- ACTION without explicit horizon -> next trading-session close (24h for 24/7 markets);
- OPINION -> explicit horizon when present; otherwise deterministic wording mapping; default 5 trading days when no time wording exists;
- long-horizon THESIS records use their recoverable intended horizon, not an arbitrary next-day test;
- a bad short-term action cannot be rescued by extending the horizon after the result is known.

## Repository layout

```text
contrarian-signal-skill/
├── SKILL.md
├── README.md
├── scripts/
│   └── calc_score.py
├── references/
│   ├── event-model.md
│   ├── scoring-rules.md
│   └── style-model.md
├── assets/
│   └── report-template.md
└── tests/
    └── test_calc_score.py
```

## Example calculator input

```json
{
  "style_profile": {
    "primary_archetype": "THESIS_DRIVEN",
    "style_transferability_components": {
      "horizon_consistency": 85,
      "action_opinion_consistency": 75,
      "regime_stability": 65,
      "directional_persistence": 90,
      "corpus_representativeness": 80
    },
    "risk_amplifiers": ["LEVERAGED", "CONCENTRATED"]
  },
  "calls": [
    {
      "outcome": "ORIGINAL_CORRECT",
      "event_type": "OPINION",
      "attribution": "TARGET",
      "opinion_confidence": 92,
      "style_tags": ["THESIS", "LONG_HORIZON", "HIGH_CONVICTION"]
    },
    {
      "outcome": "CONTRARIAN_HIT",
      "event_type": "ACTION",
      "attribution": "TARGET",
      "opinion_confidence": 98,
      "style_tags": ["BREAKOUT_CHASE", "LEVERAGED"]
    }
  ]
}
```

Run:

```bash
python3 scripts/calc_score.py calls.json --pretty
```

Output includes:

- `raw`
- `by_event_type`
- `confidence_buckets`
- `confidence_buckets_by_event_type`
- `by_style_tag`
- `by_style_tag_and_event_type`
- `style_profile`
- `style_adjusted`
- missing-field audit counts

## Data-integrity guards

- Scored THIRD_PARTY or UNCERTAIN records are rejected.
- Missing legacy event type stays `UNKNOWN` instead of being guessed.
- Style tags must be assigned before outcome lookup.
- Incomplete style-transferability evidence produces `null`, not a guessed adjusted score.
- Leverage/concentration do not alter empirical accuracy.
- Viral failures cannot substitute for broad corpus coverage.
- Long-horizon thesis accuracy and short-horizon timing accuracy are explicitly separable.

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

CI also validates the Agent Skill specification.

## Version

Current Skill version: **0.4.0**
