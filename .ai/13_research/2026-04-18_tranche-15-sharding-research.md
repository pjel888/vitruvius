---
task: laws-tranche-15-sharding
created: 2026-04-18
status: complete
---

# Research — Tranche-15 LGU sharding

## Goal
Prepare the next truthful remaining-pool lane for the LGU folder without pretending the folder is a normal single-law tranche.

## Fresh evidence
- LGU raw file count: `56`
- exact duplicate clusters: `2`
  - `866816954-Calamba-Clup.pdf` / `866816954-Calamba-Clup (1).pdf`
  - `459742704-Zoning-Ordinance-2016-2025.pdf` / `459742704-Zoning-Ordinance-2016-2025 (1).pdf`
- sampled zoning/CLUP PDFs detect as:
  - `TEXT_PDF`
  - `OPENDATALOADER_DIRECT`

## Current interpretation
The LGU folder is a multi-city ordinance / CLUP bundle and must be internally sharded before a truthful tranche-15 manifest can exist.
