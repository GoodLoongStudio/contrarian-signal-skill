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

When useful, repeat this table separately for ACTION and OPINION using `confidence_buckets_by_event_type`.

## Interpretation

[Explain RAW, then ACTION, then OPINION. State whether apparent contrarian behavior is concentrated in actual trading actions, strong opinions, weak opinions, or nowhere consistently. Keep the result retrospective.]

## Evidence

| # | Published | Source | Attribution | Type | Asset | Frozen call | Confidence | Horizon | Entry | Evaluation | Return | Outcome |
|---:|---|---|---|---|---|---|---:|---|---:|---:|---:|---|
| 1 | [time] | [source] | TARGET | ACTION | [asset] | [BULLISH/BEARISH] | [0-100] | [horizon] | [price] | [price] | [x.x%] | [outcome] |

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
- Attribution, event type, direction, confidence, and horizon are frozen before checking outcomes.
- Repeated substantially identical calls inside 48 hours are deduplicated.
- Do not use post-hoc intraday extremes to decide correctness.
- Statistical sample strength is separate and never changes the numerical Contrarian Score.

## Limitations

- [coverage limitation]
- [deleted/inaccessible posts]
- [historical-price approximation]
- [attribution/classification ambiguity]
- [mapping of sector thesis to benchmark, if applicable]

## Data quality status

[PASS / PARTIAL / INSUFFICIENT]
