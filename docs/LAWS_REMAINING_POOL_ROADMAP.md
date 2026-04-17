# Laws Remaining Pool Roadmap

## Current count
- total law folders: **47**
- covered through pilot/core bundle + completed lanes: **41**
- remaining uncovered folders: **6**

## Newly completed after the original roadmap draft
- `PRC` — professional-practice / PRBoA resolution lane now completed
- `RA-9279` — remediation lane now resolved truthfully as the Section 18 RA 7279 IRR source surface

## Historical completed lane sequence
### Previously completed tranche / lane families
- Environmental / implementation guidance
  - `DENR`
  - `DOE`
  - `DPWH`
- Architecture duplicate-remediation
  - `RA-9266`
- Fire-code overlap closure singleton
  - `PD-9514`
- Planning / settlements governance pack
  - `EO`
  - `DHSUD` (from the legacy combined `HLURB-DHSUD` raw folder)
- Local ordinance / zoning sharding lane
- `LGU`
  - completed shards:
    - San Mateo zoning ordinance + San Mateo/Rizal CLUP
    - Dagupan ordinance no. 2061-2016
    - Malolos city zoning ordinance
    - Meycauayan zoning ordinance
    - Davao city CLUP / zoning deck
    - Tarlac city zoning ordinance
    - Quezon City ordinance no. 2117 / QC-CBD zoning ordinance
    - Pasay City zoning ordinance of 2003
  - remaining blocker: the wider LGU lane still needs additional city/family shards beyond San Mateo
- Professional-practice / board-resolution lane
  - `PRC`
- Filename/folder mismatch remediation
  - `RA-9279`

## Remediation / defer lanes
### Remediation-first
- `RA-9266` — exact duplicate cluster inside folder (completed remediation lane)
- `RA-9279` — filename/folder mismatch (completed remediation lane)
- `LGU` — multi-city bundle with internal sharding and exact duplicate cleanup required before truthful tranche execution

### Draft / empty / weak-authority defer
- `RA-11361` — draft-only
- `RA-7920` — empty
- `HB-3391` — bill only
- `HB-5207` — bill only
- `SB-2982` — bill only
- `BERDE` — rating/user-guide surface rather than primary law

## Final disposition status
- `RA-11361` — defer: draft IRR for comments, not final authoritative issuance
- `RA-7920` — defer: empty folder
- `HB-3391` — defer: bill only
- `HB-5207` — defer: bill only
- `SB-2982` — defer: bill only
- `BERDE` — defer: user-guide / standards-support surface, not primary law or government regulation

## Machine-readable disposition artifact
- `config/datasets/laws-remaining-dispositions.yaml`

## Realistic remaining workload
- stronger normal executable tranches currently evident: **0**
- residual defer/final-disposition lanes: **6 uncovered folders**
- additional work would require:
  - new authoritative source material
  - a material change in source status/finality
  - or an explicit user-directed reopening of a deferred item

## Tracking rule
Track progress by **lane completed**, not just tranche number. Some future lanes are remediation-only and should not be counted as normal law tranches.
