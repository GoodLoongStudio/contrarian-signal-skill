# Retrospective Scoring Rules

These rules define how to classify historical public market calls consistently.
The purpose is retrospective measurement, not generation of live trading advice.

## 1. Scorable direction

Every market-related statement should first be classified for direction, even when the wording is weak.

Use:

- `BULLISH`: expects or leans toward the referenced asset, index, sector, or market rising; includes buy/add/hold-risk-on actions when the directional meaning is clear.
- `BEARISH`: expects or leans toward it falling; includes sell/reduce/clear-position/avoid-risk actions when the directional meaning is clear.
- `NEUTRAL`: expresses a market opinion but no directional lean can be recovered.
- `UNSCORABLE`: no usable market opinion can be established.

The **RAW Contrarian Score** should include every testable BULLISH or BEARISH opinion regardless of how weak or strong the wording is. Do not require a confidence threshold for RAW.

Neutral or non-directional commentary cannot be scored against later price direction and therefore does not enter the RAW score denominator, but it should still be counted in corpus statistics when relevant.

## 2. Opinion confidence

Assign every BULLISH or BEARISH opinion an `opinion_confidence` from 0 to 100 **before checking the later market outcome**.

This value means: **how confidently the agent can recover a directional market opinion from the author's wording/action and direct context.**

It is not:

- the statistical confidence of the final sample;
- the author's probability estimate unless explicitly stated;
- a measure of whether the prediction eventually proved correct.

Use these bands:

| Opinion confidence | Label | Typical evidence |
|---:|---|---|
| 90-100 | VERY_HIGH | explicit buy/sell/clear/full-position action; "必涨/必跌"; explicit bullish/bearish call with clear asset and timing |
| 70-89 | HIGH | clear "看多/看空/继续涨/要跌" stance, but without a hard action or precise condition |
| 50-69 | MEDIUM | directional recommendation or clear lean such as "更看好/不看好/可以关注/风险较大" with identifiable asset |
| 30-49 | LOW | weak directional implication such as "可能有机会/感觉要调整" where direction is recoverable but qualified |
| 10-29 | VERY_LOW | very tentative directional hint; substantial ambiguity remains but bullish/bearish lean is still more likely than neutral |
| 0-9 | TRACE | extremely weak directional trace. Keep it for RAW analysis when a direction can still be assigned, but do not overstate it as a strong call |

Do not raise or lower `opinion_confidence` after observing the market outcome.

### 2.1 Confidence-bucket scores

Calculate a separate Contrarian Score for each band:

- `90-100`
- `70-89`
- `50-69`
- `30-49`
- `10-29`
- `0-9`

Each bucket score uses only scored calls in that confidence range:

`bucket_contrarian_score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

A bucket with no scored calls returns `null`, not zero.

### 2.2 RAW score

Also calculate one score with **no opinion-confidence filter**:

`RAW Contrarian Score = all CONTRARIAN_HIT / (all CONTRARIAN_HIT + all ORIGINAL_CORRECT) * 100`

The RAW score is the broadest measure and should include every testable directional opinion, including LOW, VERY_LOW, and TRACE opinions.

Always report both RAW and confidence-bucket scores when confidence data is available.

## 3. Evaluation horizon

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

## 4. Price references

Record both timestamps and source identifiers used for price verification.

For exchange-traded assets:

- during regular trading hours: use the first reliable tradable/reference price at or immediately after publication;
- outside regular trading hours: use the next regular-session open unless the post explicitly references another benchmark.

For continuously traded assets, use the first reliable price at or immediately after publication.

Use the price at the frozen evaluation point as the end price.

## 5. Outcome classification

For an ordinary directional call:

- BULLISH + later price higher => `ORIGINAL_CORRECT`
- BULLISH + later price lower => `CONTRARIAN_HIT`
- BEARISH + later price lower => `ORIGINAL_CORRECT`
- BEARISH + later price higher => `CONTRARIAN_HIT`
- no change within the precision of the source => `FLAT`
- insufficient or unreliable data => `UNVERIFIABLE`

`FLAT` and `UNVERIFIABLE` do not enter the score denominator.

## 6. Explicit targets and deadlines

If a historical post contains a precise, objectively testable target and deadline, preserve that claim before checking the later record and score against the explicit condition.

Do not invent targets, deadlines, invalidation levels, or success criteria.

## 7. Conditional statements

A conditional claim is only scorable if its stated trigger occurred and can be timestamped. If the trigger never occurred, exclude the claim rather than counting it as correct or incorrect.

## 8. Repeated thesis

Within a rolling 48-hour window, repeated posts expressing substantially the same asset, direction, and thesis count once.

A new call can be counted if the author materially changes the direction, target, horizon, position/action, or testable thesis.

## 9. Multiple assets

If one post contains separate, independently testable calls for multiple assets, split them into separate records.

If a multi-asset statement cannot be separated without changing its meaning, score the relationship itself only when that relationship is objectively testable; otherwise mark it `UNSCORABLE`.

## 10. Edited or deleted posts

If the historical wording cannot be established reliably, do not score it.

A timestamped archive may be used when it clearly preserves the relevant wording and publication context. Record the archive source.

## 11. Required per-call record

For every directional opinion preserve at least:

```json
{
  "published_at": "ISO-8601 timestamp",
  "source_url": "original public source",
  "platform": "platform name",
  "asset": "instrument or market",
  "direction": "BULLISH or BEARISH",
  "opinion_confidence": 0,
  "horizon": "frozen evaluation horizon",
  "entry_timestamp": "ISO-8601 timestamp",
  "entry_price": 0,
  "evaluation_timestamp": "ISO-8601 timestamp",
  "evaluation_price": 0,
  "price_source": "historical price source",
  "outcome": "ORIGINAL_CORRECT or CONTRARIAN_HIT"
}
```

Keep excluded records separately so the report can explain why they were not scored.
