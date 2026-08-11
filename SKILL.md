---
name: contrarian-signal-skill
description: Analyze a public person's market calls over the previous 365 days and measure how often taking the opposite side would have been correct. Use when a user asks whether a commentator, influencer, analyst, trader, blogger, or social-media account is a 反指 / contrarian indicator; asks for their historical call accuracy; or wants an evidence-backed Contrarian Score. Collect public posts, extract only testable bullish/bearish calls, verify each against later market prices, and report a transparent 0-100 score with sample size and evidence.
license: MIT
compatibility: Requires access to public web/social content and historical market-price data. Python 3 is optional for deterministic score calculation.
metadata:
  author: GoodLoongStudio
  version: "0.1.0"
---

# Contrarian Signal Skill

Measure whether a public market commentator has historically been useful as a **contrarian indicator**.

The primary metric is deliberately simple and auditable:

`Contrarian Score = contrarian_hits / scored_calls * 100`

A higher score means the opposite side of the person's testable historical calls was correct more often.

Do not use reputation, popularity, follower count, tone, hindsight, or subjective dislike in the score.

## Default scope

Unless the user specifies otherwise:

- analyze the previous **365 days** from the current date;
- analyze all markets/assets for which the target made testable directional calls;
- use only public content;
- include only calls that can be scored without inventing missing meaning.

## Activation examples

Use this skill for requests such as:

- "看看这个人是不是反指"
- "统计他过去一年的预测准确率"
- "算一下 @xxx 的反指指数"
- "这个博主过去一年看多看空到底准不准"
- "Is this trader a contrarian indicator?"
- "Backtest this commentator's calls for the last year"

Do not activate for generic market prediction, portfolio advice, or sentiment analysis that is not centered on evaluating a specific public source or clearly defined group.

## Required result

Return both:

1. **Original Accuracy** — how often the person's own scored direction was correct.
2. **Contrarian Score** — how often the opposite direction was correct.

For binary scored calls:

`Original Accuracy + Contrarian Score = 100%`

Keep sample confidence separate from the score.

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

### 3. Extract only testable calls

Classify each candidate as one of:

- `BULLISH`
- `BEARISH`
- `UNSCORABLE`

A call is scorable only when all of these are recoverable from the post itself or its direct context:

- identifiable asset / index / market;
- directional view;
- publication time;
- evaluation horizon, either explicit or deterministically inferred by the rules in `references/scoring-rules.md`.

Mark `UNSCORABLE` for:

- neutral commentary;
- pure news sharing;
- ambiguous jokes/sarcasm;
- statements made after the price move already occurred;
- vague claims such as "值得关注" without direction;
- claims whose asset cannot be identified;
- claims that require inventing a target or condition.

Never force an ambiguous post into bullish or bearish to increase sample size.

### 4. Deduplicate repeated calls

Do not let repeated posting artificially increase the sample.

Treat substantially identical calls on the same asset, same direction, and same thesis within 48 hours as one call unless the later post clearly changes at least one of:

- direction;
- target;
- horizon;
- invalidation condition;
- thesis in a way that creates a new independently testable claim.

Use the earliest qualifying timestamp for a duplicated thesis.

### 5. Freeze the prediction before checking the outcome

For every call, first freeze:

- asset;
- direction;
- horizon;
- explicit target/invalidation if present;
- scoring rule.

Only after freezing those fields may you inspect subsequent price action.

This prevents hindsight leakage.

### 6. Verify with historical market data

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

### 7. Label each outcome

Each scorable call must resolve to one of:

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

Exclude `FLAT` and `UNVERIFIABLE` from the score denominator, but report their counts.

### 8. Calculate deterministically

Let:

- `C` = ORIGINAL_CORRECT count
- `R` = CONTRARIAN_HIT count
- `N = C + R`

Calculate:

- `Original Accuracy = C / N * 100`
- `Contrarian Score = R / N * 100`

If Python execution is available, prefer `scripts/calc_score.py` instead of doing arithmetic manually.

Do not modify Contrarian Score based on sample size.

### 9. Assess evidence strength

Report sample strength separately:

- `N < 5` → INSUFFICIENT
- `5-9` → VERY_LOW
- `10-19` → LOW
- `20-49` → MEDIUM
- `50+` → HIGH

When `N < 5`, show the numerical score if calculable but do not label the person a reliable contrarian indicator.

When available, report the 95% Wilson confidence interval produced by `scripts/calc_score.py`.

### 10. Produce an auditable report

Use the structure in `assets/report-template.md`.

The report must include:

- target identity;
- analysis window;
- corpus coverage note;
- total candidate posts;
- scorable calls;
- excluded/flat/unverifiable counts;
- Original Accuracy;
- Contrarian Score;
- sample strength;
- evidence table with source references;
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
- treating vague confidence language as a precise prediction;
- rewarding or punishing a person because of identity, popularity, or reputation;
- converting correlation into claims of causation.

## Current-call mode

If the user also asks what the target's **latest** call implies:

1. calculate the historical Contrarian Score first;
2. identify the latest scorable call;
3. show its original direction;
4. show the mechanically inverted direction;
5. label that inversion as a **historical-statistics signal**, not a guaranteed forecast.

Do not present the inverted call as certain investment advice.

## Failure modes

If the source corpus cannot be retrieved adequately:

- do not fabricate posts;
- do not infer a full-year score from a few search snippets;
- return a partial-analysis status;
- state exactly what data is missing;
- calculate a score only from clearly identified collected calls and label the coverage as partial.

If reliable historical price data is unavailable for a call, mark it `UNVERIFIABLE`.

## Supporting files

- Scoring and horizon rules: `references/scoring-rules.md`
- Deterministic calculator: `scripts/calc_score.py`
- Report format: `assets/report-template.md`
