# Retrospective Scoring Rules

These rules define deterministic retrospective scoring. Classify the historical record first; inspect later prices only after all frozen fields are set.

See `event-model.md` for ACTION/OPINION and attribution rules.

## 1. Direction

Use:

- `BULLISH`: expects or leans toward rising prices; buy/add/hold-risk-on actions are normally bullish.
- `BEARISH`: expects or leans toward falling prices; sell/reduce/clear/avoid-risk actions are normally bearish.
- `NEUTRAL`: market-related but no recoverable directional lean.
- `UNSCORABLE`: no reliable testable market opinion/action can be established.

RAW includes every testable BULLISH/BEARISH record regardless of opinion confidence.

## 2. Event type

Freeze `event_type` before outcome lookup:

- `ACTION`: target's own explicit position/trade decision.
- `OPINION`: directional belief/forecast/recommendation without a position change.
- `UNKNOWN`: legacy or unresolved type.

Always report ACTION and OPINION statistics separately in addition to combined RAW.

## 3. Attribution

Freeze `attribution` before outcome lookup:

- `TARGET`
- `THIRD_PARTY`
- `UNCERTAIN`

Only `TARGET` records may be scored as the target's history. `THIRD_PARTY` and `UNCERTAIN` records must be excluded or marked `UNSCORABLE`.

## 4. Opinion confidence

Assign every directional record an `opinion_confidence` from 0 to 100 before checking outcomes. It measures how clearly the directional meaning is recoverable, not how likely it is to be correct.

| Confidence | Label | Typical evidence |
|---:|---|---|
| 90-100 | VERY_HIGH | explicit own buy/sell/full-position/clear-position action; unambiguous hard bullish/bearish call |
| 70-89 | HIGH | clear 看多/看空/继续涨/要跌 stance |
| 50-69 | MEDIUM | clear directional recommendation or preference such as 更看好/不看好/可以关注 |
| 30-49 | LOW | weak qualified direction such as 可能有机会/感觉要调整 |
| 10-29 | VERY_LOW | tentative directional hint with substantial ambiguity |
| 0-9 | TRACE | extremely weak but still recoverable directional trace |

Do not change confidence after checking later prices.

## 5. Confidence buckets

Calculate independent Contrarian Scores for:

- `90-100`
- `70-89`
- `50-69`
- `30-49`
- `10-29`
- `0-9`

A bucket with no scored calls returns `null`.

## 6. RAW score

No confidence filter:

`RAW Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

Also calculate the same formula separately for ACTION and OPINION.

## 7. Evaluation horizon

### ACTION default

If the action has no explicit horizon:

- exchange-traded asset: **next trading-session close**;
- 24/7 asset: approximately **24 hours** after the action timestamp.

Do not use the most dramatic intraday high/low. Optional 5-day diagnostics may be shown separately but cannot replace the primary score after outcomes are known.

### OPINION default

Use explicit horizon when present. Otherwise freeze using:

| Wording | Evaluation point |
|---|---:|
| intraday / today / 日内 / 今天 | next relevant market close |
| tomorrow / 明天 | next trading-day close |
| this week / next few days / short term / 这周 / 几天 / 短期 / 这波 | 5 trading days |
| no time wording | 5 trading days |
| this month / medium term / 本月 / 一个月 / 中期 | 20 trading days |
| quarter / long term / 季度 / 长期 | 60 trading days |

For continuously traded assets, map 1/5/20/60 trading days to elapsed 24-hour periods.

Never select/change horizon after seeing the outcome.

## 8. Price references

Record entry and evaluation timestamps, prices, and source.

For exchange-traded assets:

- during regular hours: first reliable tradable/reference price at or immediately after publication;
- outside regular hours: next regular-session open unless the post explicitly references another benchmark.

For 24/7 assets use the first reliable price at or immediately after publication.

## 9. Outcome

For ordinary directional records:

- BULLISH + later price up -> `ORIGINAL_CORRECT`
- BULLISH + later price down -> `CONTRARIAN_HIT`
- BEARISH + later price down -> `ORIGINAL_CORRECT`
- BEARISH + later price up -> `CONTRARIAN_HIT`
- immaterial/no reliable move -> `FLAT`
- insufficient/reliable price evidence unavailable -> `UNVERIFIABLE`

`FLAT` and `UNVERIFIABLE` do not enter score denominators.

## 10. Explicit targets and deadlines

Preserve precise target/deadline conditions before checking outcomes. Score against the stated condition. Never invent missing targets, deadlines, or invalidation levels.

## 11. Conditional statements

A conditional claim is scorable only if its trigger occurred and can be timestamped. If the trigger did not occur, exclude it.

## 12. Repeated thesis and double counting

Within a rolling 48-hour window, substantially identical asset + direction + thesis records count once unless the target materially changes direction, position/action, target, horizon, invalidation, or thesis.

When one post contains an ACTION plus wording that merely explains the same action, keep one ACTION record. Create a separate OPINION record only when the opinion is independently testable.

## 13. Multiple assets/claims

Split independently testable claims into separate records. If separation changes the meaning, score the relationship only when objectively testable; otherwise mark UNSCORABLE.

## 14. Edited/deleted/quoted posts

If historical wording or attribution cannot be established reliably, do not score it. A timestamped archive may be used when it clearly preserves wording and context.

Fan submissions, quoted stories, reposted opinions, or third-party trades are not target predictions unless the target explicitly adopts the same view as their own separate statement.

## 15. Required record

```json
{
  "published_at": "ISO-8601 timestamp",
  "source_url": "original public source",
  "platform": "platform name",
  "attribution": "TARGET",
  "event_type": "ACTION or OPINION",
  "action_type": "optional for ACTION",
  "asset": "instrument or market",
  "direction": "BULLISH or BEARISH",
  "opinion_confidence": 0,
  "horizon": "frozen horizon",
  "entry_timestamp": "ISO-8601 timestamp",
  "entry_price": 0,
  "evaluation_timestamp": "ISO-8601 timestamp",
  "evaluation_price": 0,
  "return_pct": 0,
  "price_source": "historical price source",
  "outcome": "ORIGINAL_CORRECT or CONTRARIAN_HIT"
}
```

Keep excluded records so the report can explain coverage and exclusion reasons.
