# Contrarian Signal Report Template

# Contrarian Signal — [Target]

## Summary

- **Target:** [name / handle]
- **Platform:** [platform]
- **Analysis window:** [start] → [end]
- **Corpus coverage:** [complete / partial + explanation]
- **Candidate market posts reviewed:** [count]
- **Directional opinions found:** [count]
- **Scored directional calls:** [N]
- **RAW Original Accuracy:** [x.x%]
- **RAW Contrarian Score:** [x.x / 100]
- **RAW Sample strength:** [INSUFFICIENT / VERY_LOW / LOW / MEDIUM / HIGH]
- **RAW 95% Wilson interval:** [lower%–upper%] or [not available]

## Confidence-bucket Contrarian Scores

| Opinion confidence | Label | Scored calls | Original accuracy | Contrarian Score | Sample strength |
|---:|---|---:|---:|---:|---|
| 90-100 | VERY_HIGH | [N] | [x.x%] | [x.x] | [strength] |
| 70-89 | HIGH | [N] | [x.x%] | [x.x] | [strength] |
| 50-69 | MEDIUM | [N] | [x.x%] | [x.x] | [strength] |
| 30-49 | LOW | [N] | [x.x%] | [x.x] | [strength] |
| 10-29 | VERY_LOW | [N] | [x.x%] | [x.x] | [strength] |
| 0-9 | TRACE | [N] | [x.x%] | [x.x] | [strength] |

## Interpretation

[Explain the RAW score first, then describe whether stronger/more explicit opinions behave differently from weaker opinions. Keep this retrospective. Do not turn the statistic into a guaranteed future forecast.]

## Evidence

| # | Published | Source | Asset | Frozen call | Opinion confidence | Horizon | Entry | Evaluation | Return | Outcome |
|---:|---|---|---|---|---:|---|---:|---:|---:|---|
| 1 | [time] | [source] | [asset] | [BULLISH/BEARISH] | [0-100] | [horizon] | [price] | [price] | [x.x%] | [outcome] |

## Exclusions

| Source | Classification | Reason excluded from score |
|---|---|---|
| [source] | [NEUTRAL / UNSCORABLE / FLAT / UNVERIFIABLE / duplicate] | [reason] |

## Method

- RAW Contrarian Score = all CONTRARIAN_HIT / (all CONTRARIAN_HIT + all ORIGINAL_CORRECT) × 100.
- RAW has **no opinion-confidence threshold**. Every testable BULLISH/BEARISH opinion enters when an outcome can be verified.
- Confidence buckets are 90-100, 70-89, 50-69, 30-49, 10-29, and 0-9.
- `opinion_confidence` measures how clearly a directional opinion can be recovered from the historical wording/action, not whether the call eventually proved correct.
- Opinion confidence is frozen before checking later prices.
- Prediction fields and horizon are frozen before later market prices are inspected.
- Repeated substantially identical calls inside 48 hours are deduplicated.
- Statistical sample strength is reported separately and does not modify any 0-100 Contrarian Score.

## Limitations

- [coverage limitation]
- [deleted/inaccessible posts]
- [historical-price approximation]
- [classification ambiguity, if any]

## Data quality status

[PASS / PARTIAL / INSUFFICIENT]
