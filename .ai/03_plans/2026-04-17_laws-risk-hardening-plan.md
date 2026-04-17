---
task: laws-risk-hardening
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Risk Hardening Plan

## Objective
Reduce or eliminate the highest-value remaining risks in the bounded laws tranche before broader widening.

## Work lanes
1. **PD-957 duplicate/raw-alias hardening**
   - clarify representative-vs-alias policy
   - improve reporting / guardrails / candidate selection if needed
2. **PD-1216 OCR quality hardening**
   - inspect OCR output quality
   - define acceptance or spot-review rules
3. **Graph richness hardening**
   - identify the smallest truthful admission slices that improve sparse relationship yield
4. **Widening gate hardening**
   - ensure docs/state keep bounded tranche success distinct from all-laws readiness

## Acceptance criteria
- duplicate/raw-alias risk is reduced or better bounded
- OCR quality confidence is improved or explicitly gated
- next graph-richness moves are concrete and bounded
- widening remains correctly gated
