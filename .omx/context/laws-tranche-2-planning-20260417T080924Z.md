# Laws tranche-2 and broader tranche planning context

## Task statement
Select and implement the next tranche manifests after the current bounded tranche, then execute them with the same bounded workflow only when the readiness evidence supports it.

## Desired outcome
1. identify the safest/highest-value tranche-2 candidate laws
2. define tranche-2 / broader tranche manifest strategy
3. execute the same bounded workflow for tranche-2 once it is truly ready

## Known facts
- Current bounded tranche execute now succeeds for PD-957, PD-1216, and PD-1185.
- Fresh all-laws readiness (20260417T080744Z):
  - discovered_law_folder_count = 47
  - raw_pdf_count = 183
  - inventory_only_law_count = 43
  - duplicate_cluster_count = 9
- Current tranche still has explicit risks:
  - PD-957 duplicate/raw-alias complexity
  - PD-1216 OCR spot-review path
- Generic all-laws execution remains gated.

## Constraints
- preserve bounded-slice discipline
- no generic all-laws execute
- prefer tranche candidates justified by readiness, adjacency, and risk
- no raw mutation

## Unknowns
- which next law families are the best tranche-2 candidates
- whether tranche-2 should prioritize adjacency, readiness, or graph-richness
- whether a broader tranche manifest family beyond tranche-2 should be defined now or only after tranche-2 evidence

## Likely touchpoints
- config/datasets/
- scripts/vitruvius/laws_readiness.py
- .ai roadmap / planning / validation docs
- 006_System-Manifests/runs/datasets/laws-all-readiness/
