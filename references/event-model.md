# Event Model: ACTION vs OPINION

Separate market actions from market opinions before checking outcomes.

## Event types

### ACTION

Use `ACTION` only when the target clearly states that they personally changed or maintained a market position.

Typical actions: `BUY`, `ADD`, `ENTER_LONG`, `HOLD`, `REDUCE`, `SELL`, `CLEAR`, `EXIT_LONG`.

Examples:
- "我全仓上车半导体了" -> ACTION / BULLISH
- "今天加仓小米" -> ACTION / BULLISH
- "一键清仓，不玩了" -> ACTION / BEARISH
- "继续持有，一股不卖" -> ACTION / BULLISH

Do not classify metaphorical trading language as ACTION.

### OPINION

Use `OPINION` for a directional belief, forecast, recommendation, preference, or thesis without a personal position change.

Examples:
- "我继续看好 AI" -> OPINION / BULLISH
- "科技炒作差不多到头了" -> OPINION / BEARISH
- "创新药可以关注" -> OPINION / usually BULLISH with lower confidence
- "感觉明天可能调整" -> OPINION / BEARISH

### UNKNOWN

Use `UNKNOWN` for legacy records or when event type cannot be recovered reliably. New analyses should minimize it.

## Attribution gate

Set `attribution` before outcome lookup:
- `TARGET`: clearly the target's own statement/action
- `THIRD_PARTY`: quoted submission, fan story, reposted claim, or another person's action
- `UNCERTAIN`: authorship cannot be established

Only `TARGET` records may enter target statistics. A fan submission posted on the target's timeline is not automatically the target's prediction.

## Default horizons

### ACTION

Without an explicit horizon, use the **next trading-session close** for exchange-traded assets. For 24/7 assets use approximately 24 hours after the action timestamp.

Optional 5-day diagnostics may be reported separately, but never replace the primary ACTION outcome after seeing the chart.

### OPINION

Use the author's explicit horizon when present. Otherwise use `scoring-rules.md`. If no time language is inferable, default to **5 trading days**.

## Multiple claims

One post may create multiple independent records when claims are independently testable.

Example: "科技差不多到头了，可以看看创新药" may become technology/BEARISH and innovative-drug sector/BULLISH.

If a post contains an ACTION plus a thesis, avoid double counting when the thesis merely restates the action.

## Required v0.3 fields

```json
{
  "published_at": "ISO-8601 timestamp",
  "source_url": "original public source",
  "platform": "weibo",
  "attribution": "TARGET",
  "event_type": "ACTION",
  "action_type": "BUY",
  "asset": "instrument / index / sector",
  "direction": "BULLISH",
  "opinion_confidence": 98,
  "horizon": "NEXT_SESSION_CLOSE",
  "entry_timestamp": "ISO-8601 timestamp",
  "entry_price": 0,
  "evaluation_timestamp": "ISO-8601 timestamp",
  "evaluation_price": 0,
  "return_pct": 0,
  "price_source": "historical price source",
  "outcome": "ORIGINAL_CORRECT"
}
```

For OPINION, omit `action_type`.
