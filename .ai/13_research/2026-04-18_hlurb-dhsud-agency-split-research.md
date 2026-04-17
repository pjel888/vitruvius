---
task: hlurb-dhsud-agency-split-correction
created: 2026-04-18
status: complete
---

# Research — HLURB and DHSUD agency split correction

## Goal
Correct the current repo truth where HLURB and DHSUD were conflated in a combined raw folder even though they are distinct agencies.

## Official-source verification
- DHSUD official profile states DHSUD was created on **February 14, 2019** by **Republic Act No. 11201**.
- DHSUD official profile also states RA 11201 consolidated the functions of the former **HLURB** and **HUDCC** into DHSUD, except adjudication, which went to HSAC.
- DHSUD official guidebook page currently hosts both older HLURB materials and newer DHSUD publications.

## Local source evidence for the tranche-12 documents
The two currently staged guidance files inside the combined raw folder are explicitly DHSUD publications:
- `Open Space Development Guidelines.pdf`
  - title page says: `Department of Human Settlements and Urban Development`
  - copyright/publication year: `2025`
- `Resilient Urban Design and Development Guidelines.pdf`
  - title page says: `Department of Human Settlements and Urban Development`
  - copyright/publication year: `2025`

## Truthful fix
- preserve the raw storage folder `HLURB-DHSUD` as an archival/container reality
- represent the staged tranche-12 documents under logical agency identity `DHSUD`
- keep older HLURB materials in the combined folder explicit and excluded from the DHSUD-scoped tranche lane until a separate HLURB lane is opened
