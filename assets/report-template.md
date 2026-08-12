# Contrarian Signal Report Template

# Contrarian Signal — [Target]

## Summary

- **Target:** [name / handle]
- **Platform:** [platform]
- **Analysis window:** [start] → [end]
- **Corpus coverage:** [COMPLETE / PARTIAL + explanation]
- **Candidate market posts reviewed:** [count]
- **Directional target records:** [count]
- **Excluded third-party/uncertain records:** [count]

## Core Scores

| Scope | Scored calls | Original accuracy | Contrarian Score | Sample strength | 95% Wilson interval |
|---|---:|---:|---:|---|---|
| **RAW combined** | [N] | [x.x%] | **[x.x]** | [strength] | [low-high] |
| **ACTION** | [N] | [x.x%] | **[x.x]** | [strength] | [low-high] |
| **OPINION** | [N] | [x.x%] | **[x.x]** | [strength] | [low-high] |

Interpret ACTION and OPINION separately before drawing conclusions from combined RAW.

## Confidence-bucket Contrarian Scores

| Opinion confidence | Label | Scored calls | Original accuracy | Contrarian Score | Sample strength |
|---:|---|---:|---:|---:|---|
| 90-100 | VERY_HIGH | [N] | [x.x%] | [x.x] | [strength] |
| 70-89 | HIGH | [N] | [x.x%] | [x.x] | [strength] |
| 50-69 | MEDIUM | [N] | [x.x%] | [x.x] | [strength] |
| 30-49 | LOW | [N] | [x.x%] | [x.x] | [strength] |
| 10-29 | VERY_LOW | [N] | [x.x%] | [x.x] | [strength] |
| 0-9 | TRACE | [N] | [x.x%] | [x.x] | [strength] |

When useful, repeat this table separately for ACTION and OPINION.

## Personal Style Profile

- **Primary archetype:** [THESIS_DRIVEN / CATALYST_TRADER / MOMENTUM_TRADER / MEAN_REVERSION_TRADER / MACRO_TRADER / VALUE_INVESTOR / HIGH_CONVICTION_CONCENTRATED / RAPID_REVERSAL_TRADER / MIXED]
- **Secondary archetypes:** [optional]
- **Dominant style tags:** [THESIS, DIP_BUY, CATALYST, ...]
- **Risk amplifiers:** [LEVERAGED / CONCENTRATED / HIGH_BETA / averaging down / etc.]
- **Thesis vs timing divergence:** [describe whether long-horizon research and short-horizon execution differ]

### Style transferability

| Component | Score | Evidence |
|---|---:|---|
| Horizon consistency | [0-100] | [brief evidence] |
| Action-opinion consistency | [0-100] | [brief evidence] |
| Regime stability | [0-100] | [brief evidence] |
| Directional persistence | [0-100] | [brief evidence] |
| Corpus representativeness | [0-100] | [brief evidence] |

- **Style transferability:** [x.x / 100 or null]

If any component is unsupported, set transferability to `null` and omit the Style-Adjusted Score.

## Style-conditioned Contrarian Scores

| Style tag | Scored calls | Original accuracy | Contrarian Score | Sample strength |
|---|---:|---:|---:|---|
| THESIS | [N] | [x.x%] | [x.x] | [strength] |
| CATALYST | [N] | [x.x%] | [x.x] | [strength] |
| DIP_BUY | [N] | [x.x%] | [x.x] | [strength] |
| BREAKOUT_CHASE | [N] | [x.x%] | [x.x] | [strength] |
| RAPID_REVERSAL | [N] | [x.x%] | [x.x] | [strength] |

Only show tags actually present in the corpus. When useful, split the same tag by ACTION vs OPINION.

## Style-Adjusted Scores

| Scope | Empirical Contrarian Score | Style transferability | Style-Adjusted Score |
|---|---:|---:|---:|
| RAW | [x.x] | [x.x] | [x.x] |
| ACTION | [x.x] | [x.x] | [x.x] |
| OPINION | [x.x] | [x.x] | [x.x] |

Style-adjusted values are conservative generalization metrics, not replacements for empirical history.

## Interpretation

[Explain RAW, then ACTION, then OPINION. Then explain whether apparent contrarian behavior is concentrated in specific styles such as BREAKOUT_CHASE or RAPID_REVERSAL, while other styles such as THESIS may remain accurate. Explicitly distinguish thesis accuracy, timing accuracy, and risk amplification.]

## Evidence

| # | Published | Source | Attribution | Type | Asset | Frozen call | Confidence | Style tags | Horizon | Entry | Evaluation | Return | Outcome |
|---:|---|---|---|---|---|---|---:|---|---|---:|---:|---:|---|
| 1 | [time] | [source] | TARGET | ACTION | [asset] | [BULLISH/BEARISH] | [0-100] | [tags] | [horizon] | [price] | [price] | [x.x%] | [outcome] |

## Exclusions

| Source | Attribution | Classification | Reason excluded |
|---|---|---|---|
| [source] | [THIRD_PARTY/UNCERTAIN/TARGET] | [NEUTRAL/UNSCORABLE/FLAT/UNVERIFIABLE/duplicate] | [reason] |

## Method

- RAW Contrarian Score = all CONTRARIAN_HIT / (all CONTRARIAN_HIT + all ORIGINAL_CORRECT) × 100.
- ACTION and OPINION use the same formula on separate subsets.
- Only `attribution=TARGET` may enter target scores.
- ACTION without explicit horizon defaults to next trading-session close (24h for 24/7 assets).
- OPINION uses explicit horizon, deterministic wording mapping, or 5 trading days if no time wording exists.
- Confidence buckets: 90-100, 70-89, 50-69, 30-49, 10-29, 0-9.
- `opinion_confidence` measures directional clarity, not correctness probability.
- Style tags are frozen before outcome lookup and describe behavior, not success/failure.
- Style-tag scores use the same empirical Contrarian Score formula on matching historical calls.
- Style transferability = mean of horizon consistency, action-opinion consistency, regime stability, directional persistence, and corpus representativeness.
- Style-Adjusted Score = 50 + (Empirical Contrarian Score - 50) × style_transferability / 100.
- Leverage, concentration, options, high beta, and averaging down are risk amplifiers; they do not automatically change the empirical Contrarian Score.
- Attribution, event type, direction, confidence, style tags, and horizon are frozen before checking outcomes.
- Repeated substantially identical calls inside 48 hours are deduplicated.
- Do not use post-hoc intraday extremes to decide correctness.
- Statistical sample strength is separate and never changes the numerical empirical Contrarian Score.

## Limitations

- [coverage limitation]
- [deleted/inaccessible posts]
- [historical-price approximation]
- [attribution/classification ambiguity]
- [mapping of sector thesis to benchmark, if applicable]
- [style-profile subjectivity and supporting evidence]
- [market-regime dependence]

## Data quality status

[PASS / PARTIAL / INSUFFICIENT]
