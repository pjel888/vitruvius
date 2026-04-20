---
title: AEC Engine LLM Tool Calling Implementation Plan
type: subsystem-plan
task: aec-engine-llm-tool-calling
phase: "05"
status: accepted
created: 2026-04-16
last_updated: 2026-04-16
planned_code_locations:
  - scripts/vitruvius/aec/tools/catalog.py
  - scripts/vitruvius/aec/tools/router.py
  - scripts/vitruvius/aec/tools/refusals.py
  - scripts/vitruvius/aec/tools/explainer.py
repo_grounding:
  - scripts/vitruvius/query/engine.py
  - scripts/vitruvius/query/graphrag_router.py
  - scripts/vitruvius/compound/adversarial.py
  - scripts/vitruvius/compound/dspy_compiler.py
  - scripts/vitruvius/wiki/llm_client.py
governing_inputs:
  - .ai/06_specs/AEC_ENGINE/01_COMPOUND_AI_OPERATING_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
---

# AEC Engine LLM Tool Calling Implementation Plan

## 0. Planning Status
- status: accepted
- execution role: downstream / not in first slice
- current use: authoritative subsystem plan paired with the accepted T019 foundation plan

## 1. Scope
Provide a bounded LLM-facing layer that:
- routes user intent into whitelisted AEC tool calls
- refuses unsupported requests explicitly
- explains existing verification or coordination artifacts

This layer is a router and explainer.
It is not an authority source.

## 2. Current Repo Anchors
- `query/engine.py` already returns structured evidence-citing query results
- `query/graphrag_router.py` already shows a bounded routing pattern
- `compound/adversarial.py` already shows deterministic multi-role orchestration
- `compound/dspy_compiler.py` already shows how the repo treats prompt tooling as a bounded, testable adapter rather than an open-ended agent

## 3. Planned Code Locations
- `scripts/vitruvius/aec/tools/catalog.py`
- `scripts/vitruvius/aec/tools/router.py`
- `scripts/vitruvius/aec/tools/refusals.py`
- `scripts/vitruvius/aec/tools/explainer.py`

## 4. V1 Tool Catalog
- `load_aec_snapshot`
- `translate_boundary_payload`
- `run_aec_verification`
- `get_coordination_issues`
- `get_pricing_summary`
- `get_optimization_frontier`
- `explain_aec_artifact`

No tool may silently perform multiple authority-changing actions.

## 5. Refusal Taxonomy
- unsupported discipline or rule family
- missing admitted snapshot or provenance
- request asks the LLM to decide compliance directly
- request asks for open-ended generation outside the verified loop
- request asks for unsupported import/export breadth
- request exceeds bounded candidate or artifact limits

## 6. Responsibilities
- tool catalog definition
- request classification
- refusal behavior
- explanation rendering from existing artifacts
- transcript-safe audit logging

## 7. Boundaries
- must not compute geometry
- must not price anything itself
- must not decide compliance
- must not create canonical truth
- must not persist hidden chain-of-thought

## 8. Inputs / Outputs

### Inputs
- structured user intent
- existing AEC subsystem artifacts
- tool catalog metadata

### Outputs
- tool-call envelope
- refusal artifact
- explanation payload

## 9. Data Contracts
- `tool_name`
- `tool_request_id`
- `tool_input_schema_version`
- `refusal_reason`
- `artifact_reference`
- `explanation_payload`

## 10. Dependencies
- AEC master plan
- query/structured-result patterns
- verification, coordination, pricing, and optimization plans

## 11. Ordered Implementation Steps
1. Freeze the tool catalog and request envelopes.
2. Implement a router that classifies into one tool or one refusal.
3. Reuse structured result idioms from `query/engine.py`.
4. Implement explanation rendering strictly from existing artifacts, not from fresh silent reasoning.
5. Add transcript/audit logging with bounded payload size.

## 12. Edge Cases
- ambiguous user intent spanning multiple tools
- request for unsupported design generation
- explanation request against a missing artifact
- tool-call fan-out that would hide multiple state changes

## 13. Risks
- LLM layer becomes a second orchestration plane
- explanations diverge from stored artifacts
- refusal behavior is under-specified and turns into guesswork
- chain-of-thought leakage becomes persistent state

## 14. Validation Plan

### Existing Tests To Reuse As Pattern
- `python -m pytest scripts/tests/test_query_engine.py`
- `python -m pytest scripts/tests/test_graphrag_router.py`
- `python -m pytest scripts/tests/test_query_result.py`

### New Tests Required
- `scripts/tests/test_aec_tools_catalog.py`
- `scripts/tests/test_aec_tools_router.py`
- `scripts/tests/test_aec_tools_refusals.py`
- `scripts/tests/test_aec_tools_explainer.py`

### Acceptance Gates
- every request resolves to exactly one tool or one refusal
- explanations quote only stored artifact facts
- no tool path bypasses verification or pricing authority boundaries

## 15. Performance Considerations
- keep prompts and transcripts bounded
- do not drag heavyweight AEC state into context when an artifact reference is enough
- prefer structured retrieval over raw file scans in tool implementations

## 16. Execution Checklist
- [ ] tool catalog frozen
- [ ] refusal taxonomy frozen
- [ ] explanation payload schema frozen
- [ ] transcript/audit logging bounded
- [ ] new `test_aec_tools_*` suite added

## 17. Stop Conditions
- tool routing starts making compliance decisions
- explanations are generated without artifact grounding
- chain-of-thought persistence is introduced
- requests fan out into hidden multi-action workflows
