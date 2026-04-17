# Laws Wave Reload Protocol

Use this when reopening the laws dataset expansion/remediation wave in a fresh session.

## 1. Read the compact state first
- `.ai/10_state/laws-wave-status.json`

This gives you the current counts, remaining uncovered folders, and the core artifact references.

## 2. Read the machine-readable ledgers
- `config/datasets/laws-completed-lanes.yaml`
- `config/datasets/laws-remaining-dispositions.yaml`
- `config/datasets/laws-source-provenance.yaml`
- `config/datasets/laws-manifest-index.yaml`

These answer, respectively:
- what was completed
- what remains and why it is deferred
- which important truth decisions were grounded by official/primary sources
- which concrete manifests define the completed lanes

## 3. Read the artifact index / completion roll-up
- `docs/LAWS_WAVE_ARTIFACT_INDEX.md`
- `.ai/05_logs/2026-04-18_laws-wave-completion-summary.md`

Use these for fast human orientation.

## 4. Read the current tracker surfaces
- `docs/LAWS_REMAINING_POOL_ROADMAP.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/10_state/active_context.md`

These should already agree with the machine-readable ledgers.

## 5. If the task is about a truth correction, read the specific validation log
Examples:
- HLURB/DHSUD correction:
  - `.ai/05_logs/2026-04-18_hlurb-dhsud-agency-split-validation.md`
- RA-9279 mismatch resolution:
  - `.ai/05_logs/2026-04-18_laws-ra-9279-remediation-validation.md`
- PRC lane:
  - `.ai/05_logs/2026-04-18_laws-tranche-prc-validation.md`

## 6. If reopening execution, apply this rule
Only reopen a lane when the source is stronger than the current explicit defer pool.

That means:
- enacted law
- final IRR / final regulatory issuance
- primary government resolution / board issuance
- or another source with equivalent authority

Do **not** reopen simply because something is text-readable.
Drafts, bills, empty folders, and user guides remain deferred unless their authority changes.

## 7. For law-related truth questions
Prefer official / primary sources.
At minimum, consider:
- Official agency sites
- Official Gazette
- Lawphil

If the question is materially about legal or agency identity, re-verify before changing repo truth.

## 8. End-state expectation
The current laws wave is in a saturated truth-complete state.
A future session should assume:
- no hidden executable tranche remains in the current residual pool
- any new work must come from:
  - a genuinely new authoritative source
  - a new truth correction
  - or a user-directed reopening of a deferred item with stronger evidence
