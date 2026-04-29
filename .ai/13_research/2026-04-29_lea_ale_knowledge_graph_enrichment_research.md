---
task: lea-ale-knowledge-graph-enrichment
phase: 03
created: 2026-04-29
author: PLANNER
supersedes: null
status: DRAFT
---

# Research Pack — LEA/ALE Knowledge Graph Enrichment

## 01 — Discover
- Repo exploration found the source-of-truth graph fixture at `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Source-rights registry: `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`.
- Existing architecture enrichment: `scripts/vitruvius/kg/architecture_taxonomy_enrichment.py`.
- Relevant tests: `scripts/tests/test_kg_architecture_taxonomy_enrichment.py`, `scripts/tests/test_kg_backbone_contracts.py`, `api/v2Backbone.test.ts`.
- Raw-source filename signals found: `ALE BT REVIEWER.pdf`, `Building Technology June 2010 ALE.pdf`, `ALE - Building Laws Cross-Reference Table (Pedro Santos Jr).xlsx`.
- Existing local ALE anchors include `Philippines ALE Subject Families`, `Philippines ALE History Theory Practice Area`, `Philippines ALE Structures Materials Utilities Area`, and `Philippines ALE Design And Site Planning Area`.

## Initial safe source strategy
Use official/public metadata first: PRC/BLEA pages and resolutions/TOS where available; R.A. 9266 and IRR; P.D. 1096/NBCP and revised IRR; R.A. 9514/Fire Code; B.P. 344/accessibility; P.D. 1067/Water Code; P.D. 856/Sanitation Code; Local Government Code/zoning; DENR/EIS; DHSUD/HLURB CLUP/Zoning; NCCA/National Artists; protected technical codes only as metadata-only source families.

## Rights boundary
Raw PDFs are only topic-signal inputs after classification. Do not copy their bodies, tables, clauses, questions, answer keys, reviewer explanations, figures, or diagrams.

## Pending research actions
- Browse official/public sources for current metadata and URLs.
- Run a concise Kimi advisory pass for subject-domain/source-family review.
- Complete raw PDF inventory/source-rights classification.
