# Contrarian Signal Report Template

# Contrarian Signal — [Target]

## Summary

- **Target:** [name / handle]
- **Platform:** [platform]
- **Analysis window:** [start] → [end]
- **Corpus coverage:** [complete / partial + explanation]
- **Candidate market posts reviewed:** [count]
- **Scored directional calls:** [N]
- **Original Accuracy:** [x.x%]
- **Contrarian Score:** [x.x / 100]
- **Sample strength:** [INSUFFICIENT / VERY_LOW / LOW / MEDIUM / HIGH]
- **95% Wilson interval:** [lower%–upper%] or [not available]

## Interpretation

[One short paragraph explaining what the historical score means. Keep this retrospective. Do not turn the statistic into a guaranteed future forecast.]

## Evidence

| # | Published | Source | Asset | Frozen call | Horizon | Entry | Evaluation | Return | Outcome |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 1 | [time] | [source] | [asset] | [BULLISH/BEARISH] | [horizon] | [price] | [price] | [x.x%] | [outcome] |

## Exclusions

| Source | Reason excluded |
|---|---|
| [source] | [UNSCORABLE / FLAT / UNVERIFIABLE / duplicate / trigger not reached] |

## Method

- Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) × 100.
- Only testable directional historical calls enter the denominator.
- Prediction fields are frozen before later market prices are inspected.
- Repeated substantially identical calls inside 48 hours are deduplicated.
- Sample strength is reported separately and does not modify the score.

## Limitations

- [coverage limitation]
- [deleted/inaccessible posts]
- [historical-price approximation]
- [classification ambiguity, if any]

## Data quality status

[PASS / PARTIAL / INSUFFICIENT]
