---
task: aec-first-bounded-slice
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — AEC First Bounded Slice Pre-Implementation Candidate

## Verdict
- **Planning verdict:** GO
- **Implementation verdict:** NO-GO
- **Critic outcome:** APPROVE only as a blocked pre-implementation candidate, not as a sprint plan

## Audit findings

### A-001 — The artifact must stay pre-`AEC-T020`
The live gate-state JSON still says `ready_to_implement=false`, and `AEC-T020` depends on broader upstream closures. Any artifact that reads like an executable first sprint would overclaim repo readiness.

### A-002 — Boundary risk still comes first
A boundary-only package is too weak, but an ECS-first framing misorders the highest-risk seam. The candidate must keep the boundary lane first while still showing the downstream reference-world chain it will eventually prove.

### A-003 — Verifier scope must be demoted
Because vault truth law and AST admission remain unresolved upstream work, the verifier portion of the candidate can only pre-bind whitelist/refusal/schema design and future evidence lanes. It cannot behave like a finished implementation-ready verifier package.

### A-004 — Open upstream work must remain foregrounded
`AEC-T001`–`AEC-T011`, `AEC-T006`, `AEC-T013`, `AEC-T017`, `AEC-T018`, `AEC-T019`, and `G1`–`G8` are not background assumptions. They are still blocker truth and must remain explicit in the plan.

### A-005 — Graph/backend law must stay explicit
`AEC-T008` and `AEC-T010A` are easy to lose when the slice is framed around boundary/ECS/spatial/verifier flow. The plan must still call them out so graph-contract reuse and backend-duality law are not smuggled in by precedent.

## Audit conclusion
Approve the next artifact only if it is framed as a **blocked pre-implementation bounded-slice candidate** with:
- `implementation_blocked: true`
- `ready_to_implement: false`
- `not_a_sprint_plan: true`
- `cannot_close_tasks: [AEC-T020]`
- an explicit blocker list including `AEC-T006`, `AEC-T013`, `AEC-T017`, `AEC-T018`, `AEC-T019`, and `G1`–`G8`

## Final audit recommendation
The accepted candidate should define the likely first-slice spine, bind future evidence lanes, and stop there. It must not authorize implementation, close `AEC-T020`, or imply that the sprint template can already be executed.
