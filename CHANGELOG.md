# Changelog

## 0.5.0 - 2026-08-12

### Added

- research/compliance boundary for investment-adjacent prompts;
- evidence ladder and public-source playbook;
- public-person evaluation guardrails;
- Agent interface metadata under `agents/openai.yaml`;
- evaluation test cases covering attribution, contrarian framing, real-person evaluation, partial coverage, and thesis-vs-timing separation;
- local release validator;
- security policy;
- bilingual repository documentation.

### Changed

- product positioning from a generic "reverse-trading signal" framing to **retrospective public-market opinion backtesting and behavioral calibration**;
- benchmark accounts are kept as methodology case studies rather than future trading signals;
- external-facing language now explicitly states: research support only, no trade execution, no guaranteed returns, no personalized order/position instructions.

### Preserved

- RAW / ACTION / OPINION empirical scoring;
- confidence buckets;
- style-conditioned scores;
- Style-Adjusted Score;
- Wilson intervals and sample-strength reporting;
- attribution gate, deterministic horizons, deduplication and anti-hindsight controls.

## 0.4.0

- Added personal style tags, archetypes, style transferability, style-conditioned scores, and Style-Adjusted Score.

## 0.3.0

- Split ACTION and OPINION scoring and added attribution controls and deterministic horizons.

## 0.2.0

- Added RAW scoring and confidence buckets.

## 0.1.0

- Initial Contrarian Signal scoring model.
