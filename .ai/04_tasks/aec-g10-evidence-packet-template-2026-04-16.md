---
task: aec-g10-evidence-packet-template
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC G10 Evidence Packet Template

## Purpose
This is the exact future evidence packet template to populate when attempting to close G10.

## 1. Baseline identity
- baseline branch:
- baseline worktree path:
- git commit SHA:
- `git status --short --branch` output:

## 2. Test-file presence proof
Record existence for all bounded-slice test files.
Minimum required fields:
- path
- exists: true/false
- checked_in_worktree:

## 3. Fixture-file presence proof
Record existence for all bounded first-slice fixture families.
Minimum required fields:
- fixture root
- expected files/families
- exists: true/false

## 4. Command-output proof
Record exact outputs for:
- boundary pytest group
- ECS pytest group
- spatial pytest group
- verification pytest group

Minimum required fields:
- command
- exit code
- pass/fail summary
- log or output path

## 5. Artifact-root inspection proof
Record inspection of:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/`
- `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`
- `006_System-Manifests/aec/promotions/first-slice/`
- bounded replay diagnostics under the same namespace

Minimum required fields:
- root path
- expected files present: true/false
- notes

## 6. Validation-log proof
- validation log path:
- validation log written: true/false
- out-of-scope drift observed: true/false
- template used: `.ai/05_logs/aec-first-slice-validation-template-2026-04-16.md`

## 7. Final G10 verdict
Choose one only:
- `G10 stays open`
- `G10 closes`

## Closure rule
`G10 closes` may be recorded only when every section above is complete and positive.

## Final rule
This template exists so the last blocker can be closed with auditable evidence instead of memory or chat summary.


## Companion machine-readable ledger
- `.ai/10_state/aec-first-slice-g10-evidence-ledger.template.json`
