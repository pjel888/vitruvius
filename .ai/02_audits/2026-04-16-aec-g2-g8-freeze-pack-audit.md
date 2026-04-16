---
task: aec-g2-g8-freeze-pack
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — AEC G2-G8 Freeze Pack

## Verdict
- Planning verdict: GO
- Implementation verdict: NO-GO

## Audit conclusion
A single accepted freeze pack is sufficient to close `G2`-`G8` at the planning/spec layer **if and only if** it:
- names the AEC root and language ownership map explicitly
- freezes the replay-safe envelope fields
- freezes DTO/ID/version families
- freezes frame/unit/tolerance policy with explicit canonical internal units
- freezes candidate/canonical truth separation and backend-law boundaries
- freezes benchmark doctrine and parity requirements
- keeps `ready_to_implement=false`
- leaves `G1` / `AEC-T006` open until the working tree is clean

## Stop conditions
- any freeze remains implicit or split across conflicting docs
- TypeScript gains authority for policy/units/tolerances
- Rust gains authority for truth/routing/provenance
- the freeze pack is used to claim clean baseline or sprint readiness
