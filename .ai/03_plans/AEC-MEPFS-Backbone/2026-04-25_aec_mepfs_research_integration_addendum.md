---
task: aec-mepfs-backbone
phase: research-integration
created: 2026-04-25
author: CODEX
status: approved-planning-integration
workflow: ralplan-consensus
context:
  - .omx/context/aec-mepfs-research-integration-20260425T080306Z.md
research:
  - ".ai/13_research/AECMEPFS++/deep-research-report.md"
  - ".ai/13_research/AECMEPFS++/deep-research-report (1).md"
  - ".ai/13_research/AECMEPFS++/deep-research-report 3.md"
related:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_overhaul_plan.md
---

# AECMEPFS++ Research Integration Addendum

## Purpose

This addendum records how the AECMEPFS++ research reports are integrated into
the AEC-MEPFS Backbone readiness packet.

The reports are planning evidence. They do not become canonical backbone
content, do not authorize implementation, and do not permit code, database,
feature-flag, graph rebuild, backup/restore, or cleanup work.

## Research Inputs Reviewed

- `deep-research-report.md` - production-ready master AEC taxonomy and
  Vitruvian Context resolver proposal.
- `deep-research-report (1).md` - expanded AECMEPFS++ candidate master tree.
- `deep-research-report 3.md` - implementation artifact checklist for
  governance, authoring, migration, resolver, standards/legal sources,
  operations, training, and risk.

## RALPLAN-DR Summary

### Principles

- Keep taxonomy first, graph second, document ingestion third.
- Treat external standards as mapped references, not internal identity.
- Treat the AECMEPFS++ tree as candidate authoring material until steward and
  source gates approve it.
- Specify deterministic resolver behavior before runtime implementation.
- Keep jurisdictional variation as overlays, not parallel taxonomies.

### Decision Drivers

- The existing readiness plan already blocks implementation until source rights,
  seed, shadow, parity, and verification gates close.
- The new reports add missing readiness concerns: governance pack, resolver pack,
  authoring controls, review queues, golden datasets, and Philippines overlay
  scope.
- The reports contain standard-version and source-status claims that must be
  verified against primary sources before admission.

### Viable Options

#### Option A - Evidence Overlay Into Readiness Packet

Integrate the reports as evidence, artifact targets, and stricter gates while
preserving the current readiness plan as the controlling artifact.

Pros:

- preserves the approved no-side-effects gate
- adds missing governance/resolver/QA deliverables
- avoids accidentally canonicalizing unverified research

Cons:

- adds more readiness work before implementation can start
- requires later source-verification and steward review

#### Option B - Replace The Current Backbone Plan With AECMEPFS++ Reports

Treat the reports as the new plan and rewrite around the expanded tree.

Pros:

- fastest way to adopt the new research language
- gives a more expansive taxonomy immediately

Cons:

- bypasses the approved readiness/control packet
- risks importing unverified source/version claims
- risks turning the candidate tree into canonical content without steward review

#### Option C - Archive The Reports As Reference Only

Leave current plans unchanged and keep the reports as background reading.

Pros:

- lowest change volume
- avoids scope expansion

Cons:

- misses clear readiness gaps around governance, resolver, QA, and PH overlays
- future agents may re-discover the same gaps

### Preferred Option

Option A. Integrate the reports as a planning evidence overlay and keep the
readiness packet in control.

## Accepted Integrations

- Add AECMEPFS++ reports to readiness-plan research inputs.
- Add local research-evidence summary and integration rule.
- Add source-verification gates for report claims.
- Add a first-slice decision requirement for the 18-domain proposal and larger
  AECMEPFS++ candidate tree.
- Add governance/editorial-control readiness gate.
- Add deterministic Vitruvian Context resolver readiness gate.
- Add taxonomy authoring, migration QA, review queue, and golden dataset gate.
- Add Philippines overlay pilot readiness gate.
- Add new artifact targets for R8-R11 and expanded R2/R3.
- Update the architecture plan with the 18-domain candidate backbone,
  orthogonal facets, resolver phase, no-LLM-hot-path rule, and PH overlay
  separation.

## Deferred Or Verification-Gated Claims

- Current standard versions and source status in the reports remain unverified
  until checked against official/primary sources.
- The expanded AECMEPFS++ tree is not a canonical import.
- The proposed delivery schedule is directional only and does not change the
  current no-side-effects readiness lane.
- Philippines source families are candidate pilot scope until source-rights and
  legal/provenance review pass.

## New Artifact Targets

- `.ai/03_plans/AEC-MEPFS-Backbone/standards-legal-source-pack.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/master-taxonomy-l1-l2-decision-record.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/governance-editorial-control-pack.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/vitruvian-context-resolver-pack.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/taxonomy-authoring-migration-qa-pack.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/philippines-overlay-pilot-pack.md`

## Acceptance

- Readiness plan still says `not ready`.
- No runtime implementation is authorized.
- AECMEPFS++ reports are referenced as planning inputs only.
- New gates and artifact targets are testable.
- Architect and critic consensus approve the integration.
