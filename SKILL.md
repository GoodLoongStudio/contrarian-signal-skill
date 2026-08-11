---
name: contrarian-signal-skill
description: Analyze a public person's market opinions and actions over the previous 365 days and measure how often taking the opposite side would have been correct. Use when a user asks whether a commentator, influencer, analyst, trader, blogger, or social-media account is a 反指 / contrarian indicator; asks for historical call accuracy; wants a raw all-opinion Contrarian Score; or wants separate inverse-hit rates by opinion-confidence band. Collect public posts, extract directional opinions, assign opinion confidence before checking outcomes, verify later market prices, and report transparent 0-100 scores with sample size and evidence.
license: MIT
compatibility: Requires access to public web/social content and historical market-price data. Python 3 is optional for deterministic score calculation.
metadata:
  author: GoodLoongStudio
  version: "0.2.0"
---

# Contrarian Signal Skill

Measure whether a public market commentator has historically functioned as a **contrarian indicator**.

This skill produces two complementary views:

1. **RAW Contrarian Score** — every testable directional opinion counts, with no opinion-confidence threshold.
2. **Confidence-bucket Contrarian Scores** — separate inverse hit rates for opinions with confidence 90-100, 70-89, 50-69, 30-49, 10-29, and 0-9.

The primary score formula is deliberately simple and auditable:

`Contrarian Score = contrarian_hits / scored_calls * 100`

A higher score means the opposite side of the person's historical directional opinions was correct more often.

Do not use reputation, popularity, follower count, tone, hindsight, or subjective dislike in the score.

## Critical distinction: two different kinds of confidence

Never mix these concepts:

### Opinion confidence

`opinion_confidence` is a 0-100 classification assigned to each historical statement **before checking the outcome**. It measures how clearly the wording/action expresses a directional market opinion.

Examples:

- explicit full-position buy / clear-position sell: typically 90-100;
- clear bullish/bearish statement: typically 70-89;
- directional recommendation or lean: typically 50-69;
- weak/qualified direction: typically 30-49;
- tentative hint: 10-29;
- trace directional implication: 0-9.

### Statistical sample strength

`sample_strength` describes how much scored historical evidence exists in a score calculation. It depends on sample size and is reported separately.

A statement can have `opinion_confidence=100` while the score built from only two such statements still has `sample_strength=INSUFFICIENT`.

## Default scope

Unless the user specifies otherwise:

- analyze the previous **365 days** from the current date;
- analyze all markets/assets for which the target expressed a recoverable directional opinion;
- use only public content;
- build RAW from every testable BULLISH/BEARISH opinion regardless of opinion confidence;
- additionally calculate confidence-bucket scores when confidence can be assigned;
- preserve corpus coverage limitations.

## Activation examples

Use this skill for requests such as:

- "看看这个人是不是反指"
- "统计他过去一年的预测准确率"
- "算一下 @xxx 的反指指数"
- "把他 90%-100% 置信度的观点单独算反指率"
- "不设置信度，把他说过的所有多空观点都算进去"
- "这个博主过去一年看多看空到底准不准"
- "Is this trader a contrarian indicator?"
- "Backtest this commentator's calls for the last year"

Do not activate for generic market prediction, portfolio advice, or sentiment analysis that is not centered on evaluating a specific public source or clearly defined group.

## Required result

Always return RAW results:

1. **RAW Original Accuracy** — how often the person's scored direction was correct across all testable opinions.
2. **RAW Contrarian Score** — how often the opposite direction was correct across all testable opinions.

When `opinion_confidence` is available, also return separate results for:

- 90-100 VERY_HIGH
- 70-89 HIGH
- 50-69 MEDIUM
- 30-49 LOW
- 10-29 VERY_LOW
- 0-9 TRACE

For binary scored calls inside any score calculation:

`Original Accuracy + Contrarian Score = 100%`

Keep statistical sample strength separate from all scores.

## Workflow

### 1. Resolve the target identity

Identify the exact public person/account before collecting posts.

Prefer, in order:

1. profile URL;
2. unique handle / account ID;
3. display name plus platform.

Do not merge multiple accounts with similar names.

### 2. Collect the analysis corpus

Collect public market-related content published inside the analysis window.

For each candidate item preserve:

- `published_at`
- `source_url` or stable source identifier
- `platform`
- `text` or a faithful short excerpt/paraphrase
- `asset`
- `candidate_direction`

Aim for complete coverage of the reachable period, not a hand-picked set of famous wins or losses.

If complete retrieval is impossible, explicitly report coverage limitations such as pagination limits, deleted posts, inaccessible historical pages, search-index gaps, or platform restrictions.

Never silently present a partial sample as the person's complete one-year history.

### 3. Extract every recoverable market opinion

Classify each market-related statement as one of:

- `BULLISH`
- `BEARISH`
- `NEUTRAL`
- `UNSCORABLE`

For RAW analysis, do **not** require strong wording. If a statement contains a weak but recoverable bullish or bearish lean, retain it and assign a low `opinion_confidence` instead of discarding it merely for being weak.

Examples that can enter RAW when direction is recoverable:

- buy / sell / add / reduce / clear position;
- "看多 / 看空";
- "更看好 / 不看好";
- "可能还有机会 / 感觉要调整";
- tentative directional language when one side is still more likely than neutral.

Mark `NEUTRAL` or `UNSCORABLE` for statements where no testable directional lean can honestly be recovered.

Never force truly neutral content into bullish or bearish solely to increase sample size.

### 4. Assign opinion confidence before outcome lookup

For every BULLISH/BEARISH record assign `opinion_confidence` from 0 to 100 using `references/scoring-rules.md`.

Freeze the value **before** inspecting later prices.

Do not use eventual correctness to modify confidence.

### 5. Deduplicate repeated calls

Do not let repeated posting artificially increase the sample.

Treat substantially identical calls on the same asset, same direction, and same thesis within 48 hours as one call unless the later post clearly changes at least one of:

- direction;
- position/action;
- target;
- horizon;
- invalidation condition;
- thesis in a way that creates a new independently testable claim.

Use the earliest qualifying timestamp for a duplicated thesis.

### 6. Freeze the prediction before checking the outcome

For every call, freeze:

- asset;
- direction;
- `opinion_confidence`;
- horizon;
- explicit target/invalidation if present;
- scoring rule.

Only after freezing those fields may you inspect subsequent price action.

This prevents hindsight leakage.

### 7. Verify with historical market data

Use a reliable historical price source appropriate for the asset.

Record:

- `entry_timestamp`
- `entry_price`
- `evaluation_timestamp`
- `evaluation_price`
- `return_pct`
- `price_source`

If the post occurs outside market hours, use the first tradable price after publication unless the claim explicitly refers to a known close/open.

For 24/7 assets, use the first reliable market price at or immediately after the post timestamp.

Follow the deterministic horizon and special-claim rules in `references/scoring-rules.md`.

### 8. Label each outcome

Each testable directional opinion must resolve to one of:

- `ORIGINAL_CORRECT`
- `CONTRARIAN_HIT`
- `FLAT`
- `UNVERIFIABLE`

For a normal directional call:

| Call | Later price | Outcome |
|---|---|---|
| BULLISH | up | ORIGINAL_CORRECT |
| BULLISH | down | CONTRARIAN_HIT |
| BEARISH | down | ORIGINAL_CORRECT |
| BEARISH | up | CONTRARIAN_HIT |

Exclude `FLAT` and `UNVERIFIABLE` from score denominators, but report their counts.

### 9. Calculate RAW score first

Let across **all** testable directional opinions, regardless of confidence:

- `C` = ORIGINAL_CORRECT count
- `R` = CONTRARIAN_HIT count
- `N = C + R`

Calculate:

- `RAW Original Accuracy = C / N * 100`
- `RAW Contrarian Score = R / N * 100`

RAW must not filter on `opinion_confidence`.

### 10. Calculate confidence-bucket scores

Repeat the same formula independently for these frozen opinion-confidence ranges:

- 90-100
- 70-89
- 50-69
- 30-49
- 10-29
- 0-9

Do not pool neighboring buckets after seeing outcomes.

If a bucket has no scored calls, return `null`, not 0.

If Python execution is available, prefer `scripts/calc_score.py` instead of doing arithmetic manually.

### 11. Assess evidence strength separately

For RAW and for every confidence bucket independently, report sample strength:

- `N < 5` → INSUFFICIENT
- `5-9` → VERY_LOW
- `10-19` → LOW
- `20-49` → MEDIUM
- `50+` → HIGH

When `N < 5`, show the numerical score if calculable but do not label the person a reliable contrarian indicator for that bucket.

When available, report the 95% Wilson confidence interval produced by `scripts/calc_score.py`.

### 12. Produce an auditable report

Use the structure in `assets/report-template.md`.

The report must include:

- target identity;
- analysis window;
- corpus coverage note;
- total candidate posts;
- directional opinions found;
- RAW Original Accuracy;
- RAW Contrarian Score;
- RAW sample strength;
- confidence-bucket scores and bucket sample sizes;
- evidence table with source references;
- exclusions;
- methodology note;
- limitations.

Sort evidence chronologically unless the user asks otherwise.

## Evidence rules

For every scored call, keep enough evidence for another person to reproduce the classification.

Prefer primary evidence:

- the person's original public post/page;
- first-party or established market-price data for the relevant instrument.

Do not score a call based only on another person's retelling when the original is available.

If a post has been deleted and only an unverifiable quote remains, exclude it or clearly mark it as unverifiable.

## Bias controls

The skill must actively avoid:

- cherry-picking only viral predictions;
- counting multiple reposts as multiple predictions;
- interpreting a post using information that became known later;
- changing the evaluation horizon after seeing the price path;
- changing opinion confidence after seeing correctness;
- treating weak language as high-confidence merely because it later looks impressive;
- rewarding or punishing a person because of identity, popularity, or reputation;
- converting correlation into claims of causation.

## Current-call mode

If the user also asks what the target's **latest** call implies:

1. calculate the historical RAW and confidence-bucket scores first;
2. identify the latest directional call;
3. freeze its `opinion_confidence`;
4. show its original direction;
5. show the mechanically inverted direction;
6. reference the historical bucket score that matches that confidence band;
7. label the inversion as a **historical-statistics signal**, not a guaranteed forecast.

Do not present the inverted call as certain investment advice.

## Failure modes

If the source corpus cannot be retrieved adequately:

- do not fabricate posts;
- do not infer a full-year score from a few search snippets;
- return a partial-analysis status;
- state exactly what data is missing;
- calculate scores only from clearly identified collected calls and label the coverage as partial.

If reliable historical price data is unavailable for a call, mark it `UNVERIFIABLE`.

## Supporting files

- Scoring, confidence, and horizon rules: `references/scoring-rules.md`
- Deterministic calculator: `scripts/calc_score.py`
- Report format: `assets/report-template.md`
