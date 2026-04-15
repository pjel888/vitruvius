# Rust Code Review Checklist

## Purpose
This checklist is used by Codex during self-review and by human reviewers during acceptance review.

## How to Use
Do not review by vibe.
Review by checklist.

---

## Section A — Intent and Scope
- Is the purpose of the change explicit?
- Is the Rust location justified?
- Is the change narrow enough?
- Is the task aligned with current phase and roadmap?

## Section B — Architecture
- Does the change keep Rust as compute, not orchestration?
- Does it preserve Python as orchestration?
- Does it preserve external rule authority?
- Does it avoid leaking internal structures across boundaries?
- Does it preserve deterministic design intent?

## Section C — Data Contract
- Are units explicit?
- Is coordinate frame explicit?
- Are numeric types justified?
- Are invalid states defined?
- Is threshold behavior explicit?
- Is tolerance policy documented?

## Section D — Correctness
- Are canonical tests present?
- Are edge cases tested?
- Are degenerate cases handled?
- Are threshold comparisons intentional?
- Is there any silent fallback behavior?
- Are panics avoided in normal operation?

## Section E — Numerical Risk
- Could catastrophic cancellation occur?
- Could precision degrade at large coordinates?
- Could near-threshold cases flip unexpectedly?
- Are `f32` uses justified?
- Is local-frame conversion needed?

## Section F — Performance
- Is this in a hot path?
- Are unnecessary allocations avoided?
- Are large clones avoided?
- Are structs or components minimal?
- Is cache-friendly data layout preserved?
- Is benchmark evidence provided when required?

## Section G — ECS Discipline
- Did this introduce a god component?
- Are unrelated fields bundled together?
- Is metadata kept out of hot loops?
- Are queries loading only what they need?
- Does the system operate over the right component granularity?

## Section H — Cross-Language Boundary
- Is PyO3 interface narrow?
- Is ownership clear?
- Is serialization minimized?
- Are Wasm implications considered?
- Are host-language assumptions documented?

## Section I — Dependency and Maintenance
- Did this add a new crate?
- Is the dependency justified?
- Is the API understandable by future engineers?
- Are docs and comments sufficient?
- Is migration or rollback hard?

## Section J — Validation
- Did fmt, clippy, and tests pass?
- Were property tests run where needed?
- Were benchmarks run where needed?
- Was a validation report written?
- Were state docs updated?

---

## Review Verdict Categories
- Approve
- Approve with minor follow-up
- Needs revision
- Reject pending redesign

## Final Rule
If a reviewer cannot explain why the code is correct, the code is not ready.
