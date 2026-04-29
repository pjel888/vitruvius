# Architecture Scaffold Placeholder Audit

Date: 2026-04-29  
Scope: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`

## Finding

Before this pass, the Architecture branch had:

- `ARC` records: 478
- L2: 39
- L3: 146
- L4: 292
- Generic Architecture L4 scaffold labels: 292

Examples of the unacceptable pattern:

- `ARC.HIS.ANC.CON` — `Ancient And Classical Traditions Concepts`
- `ARC.PRC.LEG.CON` — `Legal Practice Framework Concepts`
- `ARC.WAC.PAO.RUL` — `Prehistoric And Ancient Origins Rule Context`

These labels were placeholders. They did not represent the detailed architecture topic tree the user expected.

## Required correction

Replace Architecture L4 placeholder anchors with real, rights-safe semantic nodes under every Architecture L3 parent. The final branch must prove:

- zero Architecture L4 labels ending in `Concepts`, `Concept Anchor`, or `Rule Context`;
- every Architecture L3 has multiple real L4 children;
- history/theory, professional practice, laws/codes, building technology, design process, heritage, accessibility, sustainability, materials, site, interiors, digital/BIM, and construction administration have real topic coverage;
- no protected source payload is admitted.
