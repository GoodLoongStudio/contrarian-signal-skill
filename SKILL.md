---
name: contrarian-signal-skill
description: Backtest a public person's market actions and opinions over the previous 365 days to measure how often the opposite side would have been correct. Use for 反指 / contrarian-indicator analysis, historical call accuracy, raw all-opinion scoring, confidence-band scoring, or separate ACTION versus OPINION inverse-hit rates. Collect public evidence, freeze attribution/event type/direction/confidence/horizon before outcome lookup, verify later market prices, deduplicate repeated theses, and return auditable 0-100 Contrarian Scores with sample strength and coverage limits.
license: MIT
compatibility: Requires access to public web/social content and historical market-price data. Python 3 is optional for deterministic score calculation.
metadata:
  author: GoodLoongStudio
  version: "0.3.0"
---

# Contrarian Signal Skill

Measure whether a public market commentator has historically functioned as a contrarian indicator.

## Core outputs

Always produce these separately:

1. **RAW Contrarian Score** — all scored directional records, no confidence threshold.
2. **ACTION Contrarian Score** — only the target's own explicit position/trade actions.
3. **OPINION Contrarian Score** — only directional forecasts/views/recommendations.
4. **Confidence-bucket scores** — 90-100, 70-89, 50-69, 30-49, 10-29, 0-9.
5. **Sample strength + 95% Wilson interval** for every score where calculable.

Formula:

`Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

Do not modify the numerical score because of sample size. Report sample strength separately.

## Critical concepts

### Event type

Freeze before checking outcomes:

- `ACTION`: target's own buy/add/hold/reduce/sell/clear/position decision.
- `OPINION`: directional market view without a position change.
- `UNKNOWN`: legacy/unresolved records only.

Read `references/event-model.md` when classifying event type.

### Attribution

Freeze before checking outcomes:

- `TARGET`
- `THIRD_PARTY`
- `UNCERTAIN`

Only `TARGET` records may enter target scores. Fan submissions, reposted opinions, quoted stories, and another person's trades are not the target's predictions.

### Opinion confidence

`opinion_confidence` is 0-100 and measures how clearly the directional meaning is recoverable from wording/action. It is **not** the probability that the call will be correct and is **not** statistical confidence.

Assign it before looking at subsequent prices.

## Default scope

Unless the user specifies otherwise:

- analyze the previous 365 days;
- use public content only;
- seek complete reachable coverage rather than viral examples;
- include every testable BULLISH/BEARISH record in RAW;
- preserve exclusions and coverage gaps;
- report ACTION and OPINION separately.

## Activation examples

Use for requests such as:

- "看看这个人是不是反指"
- "统计他过去一年的预测准确率"
- "算一下 @xxx 的反指指数"
- "90%-100% 置信度的反指是多少"
- "不设置信度，所有观点都统计"
- "把实际买卖动作和普通观点分开算"
- "Backtest this commentator's calls for the last year"

Do not activate for generic portfolio advice or generic sentiment analysis without a defined source/group to evaluate.

## Workflow

### 1. Resolve identity

Resolve exact target by profile URL, unique account ID/handle, or display name + platform. Never merge similar accounts.

### 2. Collect corpus

Collect market-related public content inside the window. Preserve at least:

- publication time
- source URL/stable ID
- platform
- faithful text/excerpt
- direct context needed for attribution

Aim for complete reachable coverage. If pagination, deleted posts, access restrictions, or indexing gaps prevent completeness, mark coverage `PARTIAL` and state the missing areas.

### 3. Attribution gate

Before market lookup, classify each candidate as `TARGET`, `THIRD_PARTY`, or `UNCERTAIN`.

Only TARGET can become a scored target record. Keep excluded third-party/uncertain items in the audit trail.

### 4. Classify event type

Before market lookup, classify each directional target record as ACTION, OPINION, or UNKNOWN using `references/event-model.md`.

Do not convert a fan submission into ACTION. Do not convert metaphorical trading language into ACTION.

### 5. Extract direction

Classify:

- `BULLISH`
- `BEARISH`
- `NEUTRAL`
- `UNSCORABLE`

RAW should retain weak-but-recoverable direction instead of requiring strong wording. Truly neutral/ambiguous content stays out of the score.

### 6. Assign opinion confidence

For every BULLISH/BEARISH target record assign `opinion_confidence` 0-100 using `references/scoring-rules.md`.

Freeze it before outcome lookup.

### 7. Deduplicate

Within 48 hours, substantially identical asset + direction + thesis records count once unless direction, action/position, target, horizon, invalidation, or independently testable thesis materially changes.

If ACTION wording and OPINION wording merely describe the same single decision, keep one ACTION record. Split only independently testable claims.

### 8. Freeze evaluation horizon

Freeze before inspecting later prices.

- ACTION with no explicit horizon: next trading-session close; 24h for 24/7 assets.
- OPINION: explicit horizon first; otherwise deterministic wording mapping; if no time wording, 5 trading days.

Never choose a dramatic intraday high/low or change horizon after seeing results.

### 9. Verify price outcome

Use reliable historical market data. Record:

- entry timestamp/price
- evaluation timestamp/price
- return_pct
- price source

### 10. Label outcome

Use:

- `ORIGINAL_CORRECT`
- `CONTRARIAN_HIT`
- `FLAT`
- `UNVERIFIABLE`
- `UNSCORABLE`

For normal directional records:

| Direction | Later price | Outcome |
|---|---|---|
| BULLISH | up | ORIGINAL_CORRECT |
| BULLISH | down | CONTRARIAN_HIT |
| BEARISH | down | ORIGINAL_CORRECT |
| BEARISH | up | CONTRARIAN_HIT |

Exclude FLAT/UNVERIFIABLE/UNSCORABLE from score denominators but report counts.

### 11. Calculate deterministically

Prefer:

`python3 scripts/calc_score.py calls.json --pretty`

The calculator returns:

- combined RAW
- ACTION / OPINION / UNKNOWN splits
- overall confidence buckets
- ACTION confidence buckets
- OPINION confidence buckets
- missing-field audit counts

### 12. Interpret conservatively

Sample strength:

- N < 5 -> INSUFFICIENT
- 5-9 -> VERY_LOW
- 10-19 -> LOW
- 20-49 -> MEDIUM
- 50+ -> HIGH

Do not call a person a reliable contrarian indicator from a tiny bucket even if its numerical score is high.

### 13. Report

Use `assets/report-template.md` and include:

- target + window + coverage
- candidate/excluded counts
- RAW / ACTION / OPINION scores
- confidence buckets
- sample strength + Wilson intervals
- chronological evidence table
- exclusions with reasons
- methodology and limitations

## Bias controls

Actively prevent:

- cherry-picking viral failures;
- double-counting repeated posts;
- counting third-party submissions as target calls;
- post-hoc event-type changes;
- post-hoc confidence changes;
- post-hoc horizon selection;
- using intraday extremes because they make the story funnier;
- treating a whole multi-claim post as one outcome when claims can be separated;
- reputation/popularity influencing classification.

## Failure modes

If corpus retrieval is incomplete, do not claim full-year completeness. Return `PARTIAL` coverage.

If attribution is uncertain, exclude the record from target scoring.

If reliable price data is unavailable, mark `UNVERIFIABLE`.

If direction or event identity cannot be recovered honestly, mark `UNSCORABLE`.

## Current-call mode

If the user asks what the target's latest call implies:

1. calculate historical scores first;
2. classify latest record as ACTION or OPINION;
3. freeze attribution, direction, confidence, and horizon;
4. reference the matching historical event-type/confidence bucket;
5. show the mechanically inverted direction only as a historical-statistics signal, never a guaranteed forecast.

## Supporting files

- Event/attribution model: `references/event-model.md`
- Scoring/confidence/horizon rules: `references/scoring-rules.md`
- Deterministic calculator: `scripts/calc_score.py`
- Report template: `assets/report-template.md`
