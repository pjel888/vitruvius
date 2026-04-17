---
task: laws-risk-hardening
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Risk Hardening Research

## Question
What are the highest-value remaining risks after the bounded tranche source-to-graph execute succeeded?

## Fresh evidence
- bounded tranche execute succeeded for:
  - `PD-957`
  - `PD-1216`
  - `PD-1185`
- current live execute evidence includes:
  - `generated_relationship_count = 2`
  - `duplicate_law_folders = [PD-957]`
  - `shallow_representation_count = 0`
- `PD-957` still contains exact duplicate raw variants with conflicting filename semantics.
- `PD-1216` OCR-prepared successfully, but the OCR probe and produced markdown still show stamp/signature/front-matter noise.

## Highest-value risks
1. duplicate/raw-alias ambiguity around `PD-957`
2. OCR-quality confidence for `PD-1216`
3. modest relationship richness / thin graph growth
4. accidental widening from bounded tranche success into generic all-laws assumptions

## Best next move
A bounded risk-hardening pass should address those lanes in parallel before broader widening.
