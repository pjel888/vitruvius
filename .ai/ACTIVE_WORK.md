# Active Work

**Updated:** 2026-04-26
**Scope:** only active and incomplete work belongs here

## NOW

### 1. AEC-MEPFS Backbone shadow readiness slices
- **Status:** file-backed shadow staging, read-only consumer/reporting, first additive `/v2` shadow read route, opt-in Explorer preview, bounded taxonomy preview route, first admitted `BackboneNode` L1/L2 fixture slice, first sibling shadow graph/parity slice, parity-runner hardening, placement/authoring QA runner, and read-only placement QA `/v2` route implemented; not live-runtime-authorized for primary graph cutover or Explorer adoption
- **Why it matters:** the planned architecture shift should start from an authored AEC-MEPFS Backbone, not another document-derived graph pass.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/eighth-readiness-runtime-priming-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/first-shadow-only-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/second-shadow-readonly-consumer-reporting-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/third-shadow-v2-backbone-route-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/fourth-shadow-explorer-preview-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/fifth-shadow-taxonomy-preview-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/sixth-shadow-backbone-node-fixture-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/seventh-shadow-graph-parity-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/eighth-shadow-parity-runner-hardening-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/ninth-shadow-placement-qa-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/tenth-shadow-placement-qa-v2-route-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/first-slice-backbone-model-spec.md`, `/.ai/14_human_inbox/ANSWER_HERE.md`, `/.ai/05_logs/2026-04-25_aec_bb_s8_runtime_priming_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_v2_backbone_route_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_backbone_node_fixture_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_parity_runner_hardening_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_v2_route_validation.md`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/shadow-staging-report.json`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/shadow-staging-consumer-report.json`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/shadow-backbone-graph.json`, `/006_System-Manifests/aec-mepfs-backbone/parity/20260426T024015Z/api-explorer-parity-report.json`, `/006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`
- **Next concrete action:** choose the next bounded shadow slice from fresh impact review, with priority on an opt-in Explorer placement QA preview section or additional file-backed report-reader hardening before any runtime cutover.
- **Dependency / blocker:** Protected content ingest, live graph mutation, Explorer cutover, feature-flag default-on behavior, and primary runtime promotion remain blocked.

### 2. Verification refresh for unverified claims
- **Status:** planned
- **Why it matters:** some success claims are log-backed but not freshly rerun.
- **Evidence:** `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`, `/.ai/IMPLEMENTATION_MATRIX.md`
- **Next concrete action:** rerun targeted verification before making fresh “green” claims after future implementation changes.
- **Dependency / blocker:** none; triggered by future code changes.

## NEXT

### 3. Skills / agents consolidation
- **Status:** planned
- **Why it matters:** duplicated skill and agent layers create ambiguity about what is active.
- **Evidence:** `/.ai/11_skills/`, `/.ai/skills/`, `/.ai/12_agents/`
- **Next concrete action:** choose one canonical skill layer and demote imported/unrelated packs to archive/reference.
- **Dependency / blocker:** not blocking the core operating surface.

### 4. Historical transcript demotion
- **Status:** planned
- **Why it matters:** transcripts are useful history but not active planning state.
- **Evidence:** `/.ai/chatGPT-Conversations/`
- **Next concrete action:** move or formally demote transcript material into archive/reference navigation.
- **Dependency / blocker:** reference impact should be mapped before moving files.
