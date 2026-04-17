---
task: laws-tranche-post-readiness-review
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche Post-Readiness Review Audit

## Review question
What code-quality and operator-documentation risks should be preserved while the
next tranche slice is implemented?

## Findings

### 1) Command naming is already drifting

Current repo evidence is inconsistent:

- `scripts/pipeline_cli.py` registers `run-laws-all-dry-run`
- `scripts/tests/test_dataset_pipeline_cli.py` verifies `run-laws-all-dry-run`
- `scripts/vitruvius/cli_experience.py` still documents `run-all-laws-dry-run`
- `README.md` currently contains both names

**Risk:** tranche support could repeat the same mismatch across parser/help/docs,
which would make operator instructions untrustworthy.

**Recommendation:** choose one canonical tranche command id and keep parser,
help/experience text, tests, and README synchronized.

### 2) The existing manifest contract is the correct expansion boundary

`config/datasets/laws-core-bundle-m1.yaml` already shows the safest shape for
future tranche manifests:

- explicit raw anchors
- explicit canonical inputs
- explicit relationship inputs
- explicit `law_units`

**Risk:** a convenience shortcut that widens by directory sweep would bypass the
truth-preserving manifest boundary.

**Recommendation:** tranche-1 should be a sibling manifest, not a generic
all-laws toggle.

### 3) BP220-style shallow admission needs report-first language

The current graph contract is concept-centric. A law can therefore show rich
section/header structure while still having thin law-native concept admission.

**Risk:** if tranche guardrails describe structural richness as readiness, the
system could overstate graph depth.

**Recommendation:** automated output should explicitly distinguish:

- source inventory richness
- section/header richness
- admitted concept richness
- law-backed relationship richness

and should keep execute gated when those dimensions diverge materially.

## Bottom line

The safest review stance is:

1. preserve manifest-backed tranche boundaries
2. preserve Phase 11 gating
3. keep `m2-8gb-safe` as the low-spec planning baseline
4. normalize command naming before the tranche workflow is considered operator-ready
