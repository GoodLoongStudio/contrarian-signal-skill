# Contrarian Signal Report Template

# 反指指数 · Contrarian Signal — [Target]

> 本报告仅用于公开历史内容的研究与统计校准，不构成投资建议，也不代表未来表现。买卖决策由用户自行作出。

## Summary / 摘要

- **Target:** [name / handle]
- **Platform:** [platform]
- **Analysis window:** [start] → [end]
- **Corpus coverage:** [COMPLETE / PARTIAL + explanation]
- **Candidate market posts reviewed:** [count]
- **Directional TARGET records:** [count]
- **Excluded third-party/uncertain records:** [count]
- **Overall evidence quality:** [STRONG / MEDIUM / WEAK / MIXED]
- **Data quality status:** [PASS / PARTIAL / INSUFFICIENT]

## Core Scores / 核心历史分数

| Scope | Scored calls | Original accuracy | Historical Contrarian Score | Sample strength | 95% Wilson interval |
|---|---:|---:|---:|---|---|
| **RAW combined** | [N] | [x.x%] | **[x.x]** | [strength] | [low-high] |
| **ACTION** | [N] | [x.x%] | **[x.x]** | [strength] | [low-high] |
| **OPINION** | [N] | [x.x%] | **[x.x]** | [strength] | [low-high] |

Interpret ACTION and OPINION separately before drawing conclusions from RAW. These are retrospective statistics, not future trading probabilities.

## Confidence-bucket Scores / 观点明确度分桶

| Opinion confidence | Label | Scored calls | Original accuracy | Historical Contrarian Score | Sample strength |
|---:|---|---:|---:|---:|---|
| 90-100 | VERY_HIGH | [N] | [x.x%] | [x.x] | [strength] |
| 70-89 | HIGH | [N] | [x.x%] | [x.x] | [strength] |
| 50-69 | MEDIUM | [N] | [x.x%] | [x.x] | [strength] |
| 30-49 | LOW | [N] | [x.x%] | [x.x] | [strength] |
| 10-29 | VERY_LOW | [N] | [x.x%] | [x.x] | [strength] |
| 0-9 | TRACE | [N] | [x.x%] | [x.x] | [strength] |

When useful, repeat separately for ACTION and OPINION.

## Personal Style Profile / 个人风格画像

- **Primary archetype:** [THESIS_DRIVEN / CATALYST_TRADER / MOMENTUM_TRADER / MEAN_REVERSION_TRADER / MACRO_TRADER / VALUE_INVESTOR / HIGH_CONVICTION_CONCENTRATED / RAPID_REVERSAL_TRADER / MIXED]
- **Secondary archetypes:** [optional]
- **Dominant style tags:** [THESIS, DIP_BUY, CATALYST, ...]
- **Risk amplifiers:** [LEVERAGED / CONCENTRATED / HIGH_BETA / averaging down / etc.]
- **Thesis vs timing divergence:** [describe]

### Style transferability

| Component | Score | Evidence |
|---|---:|---|
| Horizon consistency | [0-100] | [brief evidence] |
| Action-opinion consistency | [0-100] | [brief evidence] |
| Regime stability | [0-100] | [brief evidence] |
| Directional persistence | [0-100] | [brief evidence] |
| Corpus representativeness | [0-100] | [brief evidence] |

- **Style transferability:** [x.x / 100 or null]

If any component is unsupported, return `null` and omit Style-Adjusted Score.

## Style-conditioned Scores / 风格条件化历史分数

| Style tag | Scored calls | Original accuracy | Historical Contrarian Score | Sample strength |
|---|---:|---:|---:|---|
| THESIS | [N] | [x.x%] | [x.x] | [strength] |
| CATALYST | [N] | [x.x%] | [x.x] | [strength] |
| DIP_BUY | [N] | [x.x%] | [x.x] | [strength] |
| BREAKOUT_CHASE | [N] | [x.x%] | [x.x] | [strength] |
| RAPID_REVERSAL | [N] | [x.x%] | [x.x] | [strength] |

Only show tags present in the corpus. Split by ACTION/OPINION when useful.

## Style-Adjusted Scores

| Scope | Empirical Score | Style transferability | Style-Adjusted Score |
|---|---:|---:|---:|
| RAW | [x.x] | [x.x] | [x.x] |
| ACTION | [x.x] | [x.x] | [x.x] |
| OPINION | [x.x] | [x.x] | [x.x] |

Style-adjusted values are conservative generalization metrics, not replacements for historical results.

## Interpretation / 解释

[Explain RAW, ACTION and OPINION. State where reverse outcomes are concentrated and where they are not. Distinguish thesis accuracy, timing accuracy, leverage/concentration risk and sample limitations. Use historical-statistics language rather than labeling the person.] 

Recommended phrasing:

> 在当前可验证样本和固定观察周期下，[scope/style] 的历史反向命中率为 [x.x%]，样本强度为 [strength]。该结果用于历史行为校准，不代表未来可以机械反向交易。

## Evidence / 证据

| # | Published | Source | Evidence | Attribution | Type | Asset | Frozen call | Confidence | Style tags | Horizon | Entry | Evaluation | Return | Outcome |
|---:|---|---|---|---|---|---|---|---:|---|---|---:|---:|---:|---|
| 1 | [time] | [source] | [Strong/Medium/Weak] | TARGET | ACTION | [asset] | [BULLISH/BEARISH] | [0-100] | [tags] | [horizon] | [price] | [price] | [x.x%] | [outcome] |

## Exclusions / 排除记录

| Source | Evidence | Attribution | Classification | Reason excluded |
|---|---|---|---|---|
| [source] | [level] | [THIRD_PARTY/UNCERTAIN/TARGET] | [NEUTRAL/UNSCORABLE/FLAT/UNVERIFIABLE/duplicate] | [reason] |

## Method / 方法

- RAW = all CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) × 100.
- ACTION and OPINION use the same formula on separate subsets.
- Only `attribution=TARGET` may enter target scores.
- ACTION without explicit horizon defaults to next trading-session close; 24h for 24/7 assets.
- OPINION uses explicit horizon, deterministic wording mapping, or 5 trading days when no time wording exists.
- Long-horizon THESIS uses its recoverable intended horizon.
- Confidence buckets: 90-100, 70-89, 50-69, 30-49, 10-29, 0-9.
- `opinion_confidence` measures directional clarity, not correctness probability.
- Style tags describe behavior and are frozen before outcome lookup.
- Style transferability = mean of horizon consistency, action-opinion consistency, regime stability, directional persistence and corpus representativeness.
- Style-Adjusted Score = 50 + (Empirical Score - 50) × style_transferability / 100.
- Leverage, concentration, options and high beta are risk amplifiers; they do not automatically change the empirical score.
- Repeated substantially identical calls inside 48 hours are deduplicated.
- Do not use post-hoc intraday extremes or change horizons after outcomes are known.
- Evidence should be graded using `references/evidence-ladder.md`.

## Limitations / 局限

- [coverage limitation]
- [deleted/inaccessible posts]
- [historical-price approximation]
- [attribution/classification ambiguity]
- [mapping of sector thesis to benchmark]
- [style-profile subjectivity]
- [market-regime dependence]
- [weak/secondary-source dependence]

## Research Boundary / 研究边界

This report is retrospective research and statistical calibration based on public information. It is not investment advice, does not provide order instructions, and does not predict future performance.

本报告基于公开信息做历史研究与统计校准，不构成投资建议，不提供下单指令，也不预测未来收益。
