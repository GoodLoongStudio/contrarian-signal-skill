# Personal Style Model

Personal style must refine interpretation without rewriting historical facts.

The skill therefore keeps three layers separate:

1. empirical Contrarian Scores from observed outcomes;
2. style-conditioned scores from historically similar calls;
3. a conservative Style-Adjusted Score used only to estimate how transferable the historical pattern is.

## 1. Style tags

Assign zero or more tags to each TARGET call before outcome lookup. Recommended tags:

- `THESIS`: multi-week/month structural or supply-chain thesis;
- `CATALYST`: earnings, contract, policy, filing, launch, approval, inclusion, or other dated catalyst;
- `MOMENTUM`: follows strength/continuation;
- `MEAN_REVERSION`: expects reversal after an extreme move;
- `DIP_BUY`: explicit buy/add after a decline;
- `BREAKOUT_CHASE`: entry after a breakout/large move;
- `VALUE`: valuation-normalization thesis;
- `MACRO`: direction primarily driven by rates/liquidity/geopolitics/macro;
- `NEWS_REACTION`: short-horizon reaction to new information;
- `HIGH_CONVICTION`: unusually strong language or unusually large disclosed position;
- `LEVERAGED`: leverage/options materially amplify exposure;
- `CONCENTRATED`: a small number of names dominate disclosed exposure;
- `RAPID_REVERSAL`: direction reverses within a short period;
- `LONG_HORIZON`: intended holding/evaluation horizon is 20+ trading days;
- `SHORT_HORIZON`: intended holding/evaluation horizon is <=5 trading days.

Tags describe behavior, not correctness. Never assign a tag because the trade later won or lost.

## 2. Primary archetype

After reviewing the corpus, summarize the person with one primary archetype and optional secondary archetypes. Examples:

- `THESIS_DRIVEN`
- `CATALYST_TRADER`
- `MOMENTUM_TRADER`
- `MEAN_REVERSION_TRADER`
- `MACRO_TRADER`
- `VALUE_INVESTOR`
- `HIGH_CONVICTION_CONCENTRATED`
- `RAPID_REVERSAL_TRADER`
- `MIXED`

Archetypes are explanatory labels only. They never directly add or subtract points.

## 3. Style-conditioned scores

For each style tag with scored calls, calculate the same empirical formula:

`Style-tag Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

Examples:

- `THESIS` may have a low contrarian score while `BREAKOUT_CHASE` is high;
- `ACTION + RAPID_REVERSAL` may be strongly contrarian while `OPINION + LONG_HORIZON` is not.

When evaluating a new/current call, prefer historical calls with matching event type and style tags before falling back to broader ACTION/OPINION or RAW scores.

## 4. Style transferability

Historical inverse behavior should not be assumed to generalize equally for every person. Build a `style_transferability` score only when the corpus supports all five components below.

Score each component 0-100 before using the final result:

- `horizon_consistency`: the person uses reasonably stable holding/forecast horizons;
- `action_opinion_consistency`: actions usually agree with stated views rather than contradicting them;
- `regime_stability`: the historical pattern is not confined to one narrow market regime;
- `directional_persistence`: the person does not constantly flip direction without a new thesis/catalyst;
- `corpus_representativeness`: the collected sample is broad enough to represent the person's normal behavior rather than viral highlights.

`style_transferability = arithmetic mean of the five components`

If any component cannot be supported, do not invent it. Return `style_transferability = null` and omit the Style-Adjusted Score.

## 5. Style-Adjusted Contrarian Score

This is a secondary interpretation metric, not a replacement for empirical scores.

Use shrinkage toward neutral 50:

`Style-Adjusted Score = 50 + (Base Contrarian Score - 50) * style_transferability / 100`

Examples:

- empirical score 80, transferability 100 => adjusted 80;
- empirical score 80, transferability 50 => adjusted 65;
- empirical score 20, transferability 50 => adjusted 35;
- transferability 0 => adjusted 50.

This prevents unstable personal style, sparse corpus, frequent reversals, or regime dependence from producing overconfident future inverse signals.

Always display the empirical base score next to the adjusted score.

## 6. Risk amplifiers are not contrarian evidence

Track these separately when visible:

- leverage;
- options exposure;
- concentration;
- high-beta/micro-cap bias;
- averaging down;
- frequent position resizing.

They can explain drawdowns and timing sensitivity but must not automatically increase Contrarian Score. A person can have strong thesis accuracy and still suffer large losses from leverage or poor sizing.

## 7. Timing versus thesis

For thesis-driven people, distinguish:

- `THESIS_ACCURACY`: was the directional/structural thesis right over its intended horizon?
- `TIMING_ACCURACY`: was the entry/action right over the short evaluation horizon?

Do not call a long-horizon thesis a contrarian failure merely because the next day was negative. Conversely, do not rescue a short-term action by extending the horizon after seeing a later recovery.

## 8. Required style profile

When enough data exists, report:

```json
{
  "primary_archetype": "THESIS_DRIVEN",
  "secondary_archetypes": ["CATALYST_TRADER", "HIGH_CONVICTION_CONCENTRATED"],
  "style_transferability_components": {
    "horizon_consistency": 85,
    "action_opinion_consistency": 75,
    "regime_stability": 65,
    "directional_persistence": 90,
    "corpus_representativeness": 80
  },
  "risk_amplifiers": ["LEVERAGED", "CONCENTRATED", "HIGH_BETA"]
}
```

The calculator may derive `style_transferability` and adjusted scores from these components, but the agent must justify the component values in the report.