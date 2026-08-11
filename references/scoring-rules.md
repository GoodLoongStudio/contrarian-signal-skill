# Retrospective Scoring Rules

These rules define how to classify historical public market calls consistently.
The purpose is retrospective measurement, not generation of live trading advice.

## 1. Scorable direction

Only calls with a clearly identifiable direction enter the score:

- `BULLISH`: expects the referenced asset, index, sector, or market to rise.
- `BEARISH`: expects it to fall.

Everything else is `UNSCORABLE`.

## 2. Evaluation horizon

Use the author's explicit time horizon whenever available. If no explicit horizon exists, apply the mapping below before looking at later prices.

| Wording | Default evaluation point |
|---|---:|
| intraday / today / 日内 / 今天 | next relevant market close |
| tomorrow / 明天 | next trading-day close |
| this week / next few days / short term / 这周 / 几天 / 短期 / 这波 | 5 trading days |
| this month / medium term / 本月 / 一个月 / 中期 | 20 trading days |
| quarter / long term / 季度 / 长期 | 60 trading days |

For continuously traded assets, interpret 1, 5, 20, and 60 trading days as the corresponding number of elapsed 24-hour periods.

Never select or change the horizon after seeing the outcome.

## 3. Price references

Record both timestamps and source identifiers used for price verification.

For exchange-traded assets:

- during regular trading hours: use the first reliable tradable/reference price at or immediately after publication;
- outside regular trading hours: use the next regular-session open unless the post explicitly references another benchmark.

For continuously traded assets, use the first reliable price at or immediately after publication.

Use the price at the frozen evaluation point as the end price.

## 4. Outcome classification

For an ordinary directional call:

- BULLISH + later price higher => `ORIGINAL_CORRECT`
- BULLISH + later price lower => `CONTRARIAN_HIT`
- BEARISH + later price lower => `ORIGINAL_CORRECT`
- BEARISH + later price higher => `CONTRARIAN_HIT`
- no change within the precision of the source => `FLAT`
- insufficient or unreliable data => `UNVERIFIABLE`

`FLAT` and `UNVERIFIABLE` do not enter the score denominator.

## 5. Explicit targets and deadlines

If a historical post contains a precise, objectively testable target and deadline, preserve that claim before checking the later record and score against the explicit condition.

Do not invent targets, deadlines, invalidation levels, or success criteria.

## 6. Conditional statements

A conditional claim is only scorable if its stated trigger occurred and can be timestamped. If the trigger never occurred, exclude the claim rather than counting it as correct or incorrect.

## 7. Repeated thesis

Within a rolling 48-hour window, repeated posts expressing substantially the same asset, direction, and thesis count once.

A new call can be counted if the author materially changes the direction, target, horizon, or testable thesis.

## 8. Multiple assets

If one post contains separate, independently testable calls for multiple assets, split them into separate records.

If a multi-asset statement cannot be separated without changing its meaning, score the relationship itself only when that relationship is objectively testable; otherwise mark it `UNSCORABLE`.

## 9. Edited or deleted posts

If the historical wording cannot be established reliably, do not score it.

A timestamped archive may be used when it clearly preserves the relevant wording and publication context. Record the archive source.

## 10. Required per-call record

For every scored call, preserve at least:

```json
{
  "published_at": "ISO-8601 timestamp",
  "source_url": "original public source",
  "platform": "platform name",
  "asset": "instrument or market",
  "direction": "BULLISH or BEARISH",
  "horizon": "frozen evaluation horizon",
  "entry_timestamp": "ISO-8601 timestamp",
  "entry_price": 0,
  "evaluation_timestamp": "ISO-8601 timestamp",
  "evaluation_price": 0,
  "price_source": "historical price source",
  "outcome": "ORIGINAL_CORRECT or CONTRARIAN_HIT"
}
```

Keep any excluded records separately so the report can explain why they were not scored.
