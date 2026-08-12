---
name: contrarian-signal-skill
description: Backtest a public person's market actions and opinions over the previous 365 days to measure how often the opposite side would have been correct, then condition interpretation on the person's recurring trading/research style. Use for 反指 / contrarian-indicator analysis, historical call accuracy, raw all-opinion scoring, confidence-band scoring, ACTION versus OPINION inverse-hit rates, style-conditioned scores, or style-adjusted inverse signals. Collect public evidence, freeze attribution/event type/direction/confidence/horizon/style tags before outcome lookup, verify later prices, deduplicate repeated theses, and return auditable empirical and style-adjusted results with sample strength and coverage limits.
license: MIT
compatibility: Requires access to public web/social content and historical market-price data. Python 3 is optional for deterministic score calculation.
metadata:
  author: GoodLoongStudio
  version: "0.4.0"
---

# Contrarian Signal Skill

Measure whether a public market commentator has historically functioned as a contrarian indicator without confusing poor timing, leverage, or personal trading style with bad directional research.

## Core outputs

Always keep these layers separate:

1. **RAW Contrarian Score** — all scored directional records, no confidence threshold.
2. **ACTION Contrarian Score** — only the target's own explicit position/trade actions.
3. **OPINION Contrarian Score** — only directional forecasts/views/recommendations.
4. **Confidence-bucket scores** — 90-100, 70-89, 50-69, 30-49, 10-29, 0-9.
5. **Style-conditioned scores** — historical inverse-hit rate for recurring styles such as THESIS, MOMENTUM, DIP_BUY, CATALYST, RAPID_REVERSAL, etc.
6. **Personal Style Profile** — primary archetype, secondary archetypes, risk amplifiers, and transferability components.
7. **Style-Adjusted Contrarian Score** — optional conservative generalization score; never replaces empirical scores.
8. **Sample strength + 95% Wilson interval** for empirical scores where calculable.

Empirical formula:

`Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

Do not modify the empirical score because of sample size or style. Report interpretation layers separately.

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

Only TARGET records may enter target scores. Fan submissions, reposted opinions, quoted stories, and another person's trades are not the target's predictions.

### Opinion confidence

`opinion_confidence` is 0-100 and measures how clearly the directional meaning is recoverable from wording/action. It is not the probability that the call will be correct and is not statistical confidence.

Assign it before looking at subsequent prices.

### Personal style

Personal style explains **which historical records are comparable to the current call**. It must never be used to manufacture a higher/lower empirical win rate.

Before outcome lookup, assign zero or more `style_tags` to each TARGET directional record using `references/style-model.md`.

Examples include:

- THESIS
- CATALYST
- MOMENTUM
- MEAN_REVERSION
- DIP_BUY
- BREAKOUT_CHASE
- VALUE
- MACRO
- NEWS_REACTION
- HIGH_CONVICTION
- LEVERAGED
- CONCENTRATED
- RAPID_REVERSAL
- LONG_HORIZON
- SHORT_HORIZON

## Default scope

Unless the user specifies otherwise:

- analyze the previous 365 days;
- use public content only;
- seek complete reachable coverage rather than viral examples;
- include every testable BULLISH/BEARISH record in RAW;
- preserve exclusions and coverage gaps;
- report ACTION and OPINION separately;
- build a style profile only when the corpus supports it.

## Activation examples

Use for requests such as:

- "看看这个人是不是反指"
- "统计他过去一年的预测准确率"
- "算一下 @xxx 的反指指数"
- "90%-100% 置信度的反指是多少"
- "不设置信度，所有观点都统计"
- "把实际买卖动作和普通观点分开算"
- "他的风格会不会影响反指判断"
- "这个人长期 thesis 很准但择时差，怎么评价"
- "Backtest this commentator's calls for the last year"

Do not activate for generic portfolio advice or generic sentiment analysis without a defined source/group to evaluate.

## Workflow

### 1. Resolve identity

Resolve exact target by profile URL, unique account ID/handle, or display name + platform. Never merge similar accounts.

### 2. Collect corpus

Collect market-related public content inside the window. Preserve at least publication time, source URL/stable ID, platform, faithful text/excerpt, and direct context needed for attribution.

Aim for complete reachable coverage. If pagination, deleted posts, access restrictions, or indexing gaps prevent completeness, mark coverage `PARTIAL` and state missing areas.

### 3. Attribution gate

Before market lookup, classify each candidate as TARGET, THIRD_PARTY, or UNCERTAIN.

Only TARGET can become a scored target record. Keep excluded third-party/uncertain items in the audit trail.

### 4. Classify event type

Before market lookup, classify each directional target record as ACTION, OPINION, or UNKNOWN using `references/event-model.md`.

Do not convert a fan submission into ACTION. Do not convert metaphorical trading language into ACTION.

### 5. Extract direction

Classify BULLISH, BEARISH, NEUTRAL, or UNSCORABLE.

RAW should retain weak-but-recoverable direction instead of requiring strong wording. Truly neutral/ambiguous content stays out of the score.

### 6. Assign opinion confidence

For every BULLISH/BEARISH target record assign `opinion_confidence` 0-100 using `references/scoring-rules.md` and freeze it before outcome lookup.

### 7. Assign style tags

Before looking at outcomes, tag the record using `references/style-model.md`.

Use evidence from wording, disclosed behavior, horizon, and context. Never add/remove a style tag because the trade later won or lost.

### 8. Deduplicate

Within 48 hours, substantially identical asset + direction + thesis records count once unless direction, action/position, target, horizon, invalidation, or independently testable thesis materially changes.

If ACTION wording and OPINION wording merely describe the same single decision, keep one ACTION record. Split only independently testable claims.

### 9. Freeze evaluation horizon

Freeze before inspecting later prices.

- ACTION with no explicit horizon: next trading-session close; 24h for 24/7 assets.
- OPINION: explicit horizon first; otherwise deterministic wording mapping; if no time wording, 5 trading days.
- Long-horizon THESIS records must use their stated/intended horizon when recoverable; do not downgrade them to next-day timing tests.

Never choose a dramatic intraday high/low or change horizon after seeing results.

### 10. Verify price outcome

Use reliable historical market data. Record entry timestamp/price, evaluation timestamp/price, return_pct, and price source.

### 11. Label outcome

Use ORIGINAL_CORRECT, CONTRARIAN_HIT, FLAT, UNVERIFIABLE, or UNSCORABLE.

For normal directional records:

| Direction | Later price | Outcome |
|---|---|---|
| BULLISH | up | ORIGINAL_CORRECT |
| BULLISH | down | CONTRARIAN_HIT |
| BEARISH | down | ORIGINAL_CORRECT |
| BEARISH | up | CONTRARIAN_HIT |

Exclude FLAT/UNVERIFIABLE/UNSCORABLE from score denominators but report counts.

### 12. Calculate empirical scores deterministically

Prefer:

`python3 scripts/calc_score.py calls.json --pretty`

The calculator returns combined RAW, ACTION/OPINION/UNKNOWN splits, overall confidence buckets, event-type confidence buckets, style-tag scores, and audit counts.

### 13. Build Personal Style Profile

After corpus classification, summarize the recurring behavioral pattern using `references/style-model.md`.

Report:

- primary archetype;
- optional secondary archetypes;
- dominant style tags;
- risk amplifiers;
- whether THESIS accuracy and TIMING accuracy diverge;
- style transferability components when evidence supports them.

Risk amplifiers such as leverage, concentration, high beta, or averaging down are explanatory only. They do not automatically increase Contrarian Score.

### 14. Calculate optional Style-Adjusted Score

Only when all five transferability components are supportable:

- horizon_consistency
- action_opinion_consistency
- regime_stability
- directional_persistence
- corpus_representativeness

The calculator derives their arithmetic mean as `style_transferability` and applies:

`Style-Adjusted Score = 50 + (Base Contrarian Score - 50) * style_transferability / 100`

This shrinks unstable or poorly transferable historical patterns toward neutral 50.

Never show the adjusted score without the empirical base score.

### 15. Current-call matching

When the user asks what a latest call implies, prefer the narrowest adequately sampled historical comparison in this order:

1. same event type + matching style tag(s) + matching confidence band;
2. same event type + matching style tag(s);
3. same event type + confidence band;
4. same event type;
5. RAW.

If the narrow bucket has insufficient data, fall back one level and say so.

### 16. Interpret conservatively

Sample strength:

- N < 5 -> INSUFFICIENT
- 5-9 -> VERY_LOW
- 10-19 -> LOW
- 20-49 -> MEDIUM
- 50+ -> HIGH

Do not call a person a reliable contrarian indicator from a tiny bucket even if its numerical score is high.

### 17. Report

Use `assets/report-template.md` and include target/window/coverage, candidate/excluded counts, RAW/ACTION/OPINION, confidence buckets, style profile, style-conditioned scores, optional style-adjusted score, evidence table, exclusions, methodology, and limitations.

## Bias controls

Actively prevent:

- cherry-picking viral failures;
- double-counting repeated posts;
- counting third-party submissions as target calls;
- post-hoc event-type changes;
- post-hoc confidence changes;
- post-hoc style-tag changes;
- post-hoc horizon selection;
- using intraday extremes because they make the story funnier;
- treating leverage/concentration as evidence of wrong direction;
- treating next-day losses as proof a long-horizon thesis was wrong;
- rescuing a bad short-term action by extending the horizon later;
- reputation/popularity influencing classification.

## Failure modes

If corpus retrieval is incomplete, do not claim full-year completeness. Return `PARTIAL` coverage.

If attribution is uncertain, exclude the record from target scoring.

If reliable price data is unavailable, mark UNVERIFIABLE.

If direction or event identity cannot be recovered honestly, mark UNSCORABLE.

If style-transferability components cannot be justified, omit Style-Adjusted Score rather than guessing.

## Supporting files

- Event/attribution model: `references/event-model.md`
- Scoring/confidence/horizon rules: `references/scoring-rules.md`
- Personal style model: `references/style-model.md`
- Deterministic calculator: `scripts/calc_score.py`
- Report template: `assets/report-template.md`
