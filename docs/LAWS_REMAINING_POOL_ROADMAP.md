# Laws Remaining Pool Roadmap

## Current count
- total law folders: **47**
- covered through pilot/core bundle + tranches 1–14: **38**
- remaining uncovered folders: **9**

## Proposed future tranche sequence
### Tranche 9 — Environmental / implementation guidance
- `DENR`
- `DOE`
- `DPWH`

### Tranche 10 — Architecture duplicate-remediation lane
- `RA-9266`
- optional bounded supporting context later from `PRC`

### Tranche 11 — Fire-code overlap closure singleton
- `PD-9514`

### Tranche 12 — Planning / settlements governance pack
- `EO`
- `HLURB-DHSUD`

### Tranche 15 — Local ordinance / zoning sharding lane
- `LGU`
  - completed shards:
    - San Mateo zoning ordinance + San Mateo/Rizal CLUP
    - Dagupan ordinance no. 2061-2016
    - Malolos city zoning ordinance
    - Meycauayan zoning ordinance
  - remaining blocker: the wider LGU lane still needs additional city/family shards beyond San Mateo

## Remediation / defer lanes
### Remediation-first
- `RA-9266` — exact duplicate cluster inside folder
- `RA-9279` — filename/folder mismatch
- `LGU` — multi-city bundle with internal sharding and exact duplicate cleanup required before truthful tranche execution

### Draft / empty / weak-authority defer
- `RA-11361` — draft-only
- `RA-7920` — empty
- `HB-3391` — bill only
- `HB-5207` — bill only
- `SB-2982` — bill only
- `BERDE` — rating/user-guide surface rather than primary law

## Realistic remaining workload
- normal future tranches likely needed: **4–6**
- remediation/defer lanes likely needed: **3–5**
- realistic remaining total work units: **7–9**

## Tracking rule
Track progress by **lane completed**, not just tranche number. Some future lanes are remediation-only and should not be counted as normal law tranches.
