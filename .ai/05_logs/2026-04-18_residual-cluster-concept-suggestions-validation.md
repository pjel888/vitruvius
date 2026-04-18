---
task: residual-cluster-concept-suggestions
created: 2026-04-18
status: complete
---

# Validation — residual cluster concept suggestions

## Goal
Add a deterministic operator surface that suggests missing concept scaffold candidates from refined source text so the residual orphan/partial laws can advance without fabricating stronger relationships.

## Implementation
- Added `scripts/vitruvius/concept_candidate_suggestions.py`
  - extracts definition-style candidate terms from refined markdown (`X means`, quoted terms, `defined as` clauses)
  - compares them to the shared concept inventory
  - reports matched existing concepts vs unmatched scaffold candidates
- Added CLI command:
  - `python3 scripts/pipeline_cli.py suggest-concept-candidates-from-refined --refined-markdown-path <path>`
- Added tests:
  - `scripts/tests/test_concept_candidate_suggestions.py`

## Verification
- `python3 -m pytest scripts/tests/test_concept_candidate_suggestions.py scripts/tests/test_concept_matching.py -q`
  - 7 passed

## Residual-cluster evidence
### ADR / RA-9285
Command:
- `python3 scripts/pipeline_cli.py suggest-concept-candidates-from-refined --refined-markdown-path '001-Laws/refined_markdown/RA-9285/RA_9285.md' --top-n 20`

Result highlights:
- `candidate_count = 25`
- examples:
  - `Alternative Dispute Resolution System`
  - `Arbitration`
  - `Mediator`
  - `Court-Annexed Mediation`
  - `Early Neutral Evaluation`

### RA-6969
Command:
- `python3 scripts/pipeline_cli.py suggest-concept-candidates-from-refined --refined-markdown-path '001-Laws/refined_markdown/RA-6969/RA 6969 Toxic Substances and Hazardouse Nuclear Wastes Control Act 1990.md' --top-n 20`

Result highlights:
- `candidate_count = 7`
- examples:
  - `Chemical substance`
  - `Chemical mixture`
  - `Importation`
  - `Manufacture`
  - `Unreasonable risk`
  - `Hazardous wastes`

### RA-1378 / Plumbing
Command:
- `python3 scripts/pipeline_cli.py suggest-concept-candidates-from-refined --refined-markdown-path '001-Laws/refined_markdown/RA-1378/MASTER PLUMBING LAW.md' --top-n 20`

Result highlights:
- `candidate_count = 0`
- indicates the current heuristic is useful for definition-heavy statutes, but not enough yet for sparse-title sources like the Plumbing Law.

## Outcome
The new operator surface gives the next safe automation step for the residual cluster: derive concept-scaffold candidates from explicit definition-style text before attempting any new relationship admission.
