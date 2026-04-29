# Validation Log — LEA/ALE Subject-Domain Knowledge Graph Enrichment

**Date:** 2026-04-29  
**Scope:** file-backed AEC-MEPFS backbone enrichment for Philippine Licensure Examination for Architects / Architects Licensure Examination / Board Licensure Examination for Architects (LEA/ALE/BLEA).  
**Primary artifacts:**
- `scripts/vitruvius/kg/lea_ale_semantic_enrichment.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- `006_System-Manifests/aec-mepfs-backbone/lea-ale-enrichment/20260429T091500Z/lea-ale-enrichment-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T092800Z/`

## Result Summary

- Enrichment report `20260429T091500Z`: `ok=true`.
- Output graph: 9,403 nodes and 10,979 governed relationships.
- New LEA/ALE/source nodes: 236.
- Improved existing nodes: 65.
- New governed relationships: 1,193.
- Cross-domain relationships: 799.
- Philippine law/code relationships: 572.
- Aliases added or preserved on new/improved nodes: 1,135.
- Source-rights registry: 79 rows total, 28 rows added in this slice.
- Shadow staging `20260429T092800Z`: `ok=true`; read-only consumer report `ok=true`.

The enrichment is organized by actual subject/domain structures, not only PRC exam-day areas: LEA/ALE meta, history/theory/Philippine architecture, design/site/urban planning, Philippine laws/codes/practice, fire/life safety, water/sanitation/public health, accessibility/universal design, materials/methods/specifications, structural concepts, utilities/environmental systems, interiors/human factors, sustainability/resilience, and contracts/construction administration.

## Raw Source Inventory and Rights Classification

Raw-source custody paths were inspected by filename/inventory only. No PDF/XLSX body text, tables, figures, diagrams, reviewer text, exam questions, or answer keys were copied into the graph.

| Raw custody path | Rights/source classification | Use in this slice |
|---|---|---|
| `001_Raw-Source-Layer/001-Laws/CHED/CHED CMO 61 Series 2017 - BS Architecture Curriculum Standards.pdf` | official public education/regulatory material | public metadata/source-family signal only |
| `001_Raw-Source-Layer/001-Laws/LGU/784708893-PALAUIG-ZAMBALES-CLUP.pdf` | public/local-government planning material candidate | inventory signal only; not ingested |
| `001_Raw-Source-Layer/001-Laws/PD-1096/PD 1096 RIRR 2004 - Revised IRR (Architecture Board).pdf` | official public metadata/IRR reference candidate | metadata/source-family signal only; no code clauses/tables |
| `001_Raw-Source-Layer/001-Laws/PRC/RES_Architecture and AR Interiors are Exclusive.pdf` | official PRC/public regulatory resolution candidate | inventory signal only; not ingested |
| `001_Raw-Source-Layer/001-Laws/RA-9266/RA-9266 IRR Architecture Act of 2004.pdf` | official public law/IRR reference candidate | metadata/source-family signal only; no protected payload |
| `001_Raw-Source-Layer/001-Laws/test/ALE - Building Laws Cross-Reference Table (Pedro Santos Jr).xlsx` | private/third-party exam-prep spreadsheet | metadata-only source-rights row; no spreadsheet payload |
| `001_Raw-Source-Layer/001-Laws/test/CHED CMO 61 Series 2017 - BS Architecture Curriculum Standards.pdf` | duplicate official public education/regulatory material | inventory signal only; not ingested |
| `001_Raw-Source-Layer/002-History/A History of Architecture on the Comparative Method, 5th ed. 1905 (Banister Fletcher).pdf` | likely public-domain historical book candidate, still source-reviewed | inventory signal only; not ingested |
| `001_Raw-Source-Layer/002-History/Chinese Architecture.pdf` | unknown/protected rights candidate | no ingest |
| `001_Raw-Source-Layer/002-History/Filipino Architecture.pdf` | unknown/protected rights candidate | no ingest |
| `001_Raw-Source-Layer/002-History/George Salvan Architectural Character and the History of Architecture.pdf` | private/copyrighted book/reviewer candidate | no ingest |
| `001_Raw-Source-Layer/002-History/Hindu Architecture.pdf` | unknown/protected rights candidate | no ingest |
| `001_Raw-Source-Layer/002-History/History of Architecture Sample Exam.pdf` | private exam-prep/sample exam candidate | no ingest |
| `001_Raw-Source-Layer/002-History/Modern Architectures in History (Brazil) - Richard J. Williams.pdf` | private/copyrighted book candidate | no ingest |
| `001_Raw-Source-Layer/002-History/Modern Architectures in History (USA) - Gwendolyn Wright.pdf` | private/copyrighted book candidate | no ingest |
| `001_Raw-Source-Layer/002-History/Theory of Architecture Reviewer.pdf` | private/third-party reviewer candidate | no ingest |
| `001_Raw-Source-Layer/002-History/Vitruvius - 10 Books of Architecture.pdf` | public-domain/classical reference candidate depending edition/translation | inventory signal only; not ingested |
| `001_Raw-Source-Layer/003-Theory/TOA 4 (Tropical Architecture).pdf` | unknown/protected handout/reviewer candidate | no ingest |
| `001_Raw-Source-Layer/003-Theory/TOA 5 (Masters of Architecture).pdf` | unknown/protected handout/reviewer candidate | no ingest |
| `001_Raw-Source-Layer/004-Technology/ALE BT REVIEWER.pdf` | private/third-party reviewer PDF | metadata-only source-rights row; no PDF payload |
| `001_Raw-Source-Layer/004-Technology/Building Technology June 2010 ALE.pdf` | private exam/reviewer PDF candidate | metadata-only source-rights row; no exam/reviewer payload |
| `001_Raw-Source-Layer/005-Utilities/Building Laws _ Utilities Mock Test with Key.pdf` | private mock-test/answer-key candidate | no ingest |

## Validation Commands and Results

```bash
RUN_ID=20260429T091500Z
PYTHONPATH=scripts python3 -m vitruvius.kg.lea_ale_semantic_enrichment \
  --report 006_System-Manifests/aec-mepfs-backbone/lea-ale-enrichment/20260429T091500Z/lea-ale-enrichment-report.json \
  --write
```

Result: `ok=true`; 236 nodes added, 65 nodes improved, 1,193 relationships added.

```bash
RUN_ID=20260429T092800Z
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging \
  --run-id "$RUN_ID" \
  --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --run-id "$RUN_ID"
```

Result: staging `ok=true`; consumer report `ok=true`; 9,403 nodes / 10,979 edges / 79 source-rights rows.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m py_compile \
  scripts/vitruvius/kg/lea_ale_semantic_enrichment.py \
  scripts/tests/test_kg_lea_ale_semantic_enrichment.py \
  scripts/tests/test_kg_backbone_contracts.py
```

Result: passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_lea_ale_semantic_enrichment.py
```

Result: 4 passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q \
  scripts/tests/test_kg_lea_ale_semantic_enrichment.py \
  scripts/tests/test_kg_backbone_contracts.py
```

Result: 52 passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q \
  scripts/tests/test_kg_lea_ale_semantic_enrichment.py \
  scripts/tests/test_kg_backbone_contracts.py \
  scripts/tests/test_kg_architecture_taxonomy_enrichment.py \
  scripts/tests/test_kg_broad_taxonomy_semantic_enrichment.py \
  scripts/tests/test_kg_cross_domain_overlay_enrichment.py \
  scripts/tests/test_kg_targeted_taxonomy_semantic_enrichment.py \
  scripts/tests/test_kg_backbone_shadow_staging.py \
  scripts/tests/test_kg_backbone_shadow_report_reader.py
```

Result: 96 passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg*.py
```

Result: 576 passed.

```bash
cd api && bun test v2Backbone.test.ts
```

Result: 69 passed / 0 failed.

```bash
python3 - <<'PY'
import json
from pathlib import Path
for path in [
    'scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json',
    '.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json',
    '006_System-Manifests/aec-mepfs-backbone/lea-ale-enrichment/20260429T091500Z/lea-ale-enrichment-report.json',
    '006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T092800Z/shadow-staging-report.json',
    '006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T092800Z/shadow-staging-consumer-report.json',
    '006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T092800Z/shadow-backbone-staging.json',
    '006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T092800Z/shadow-backbone-graph.json',
]:
    json.loads(Path(path).read_text())
    print(f'OK {path}')
PY
```

Result: all listed JSON files loaded successfully.

```bash
python3 - <<'PY'
import json
from pathlib import Path
fixture=Path('scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json')
data=json.loads(fixture.read_text())
records=data['records']; rels=data['relationships']
ids=[r['id'] for r in records]
paths=[r['path_code'] for r in records]
ids_set=set(ids); paths_set=set(paths)
missing=[]
for rel in rels:
    src = rel.get('source') or rel.get('source_id') or rel.get('from_id')
    tgt = rel.get('target') or rel.get('target_id') or rel.get('to_id')
    if src not in ids_set or tgt not in ids_set:
        missing.append(rel)
missing_parent_paths=[r['path_code'] for r in records if r.get('parent_path_code') and r['parent_path_code'] not in paths_set]
print('records', len(records), 'relationships', len(rels))
print('duplicate_ids', len(ids)-len(ids_set))
print('duplicate_paths', len(paths)-len(paths_set))
print('missing_edge_endpoints', len(missing))
print('missing_parent_paths', len(missing_parent_paths))
print('lea_nodes', sum(1 for r in records if str(r.get('generation_method','')).startswith('steward_governed_lea_ale')))
print('lea_rels', sum(1 for r in rels if str(r.get('generation_method','')).startswith('steward_governed_lea_ale')))
PY
```

Result: 9,403 records; 10,979 relationships; duplicate IDs 0; duplicate paths 0; missing edge endpoints 0; missing parent paths 0; LEA nodes 236; LEA relationships 1,193.

```bash
git diff --check
```

Result: passed.

```bash
npx --yes gitnexus@1.6.2-rc.10 status
```

Result: index up-to-date at current commit `742ac6c`.

## Kimi Review

Kimi advisory synthesis was used before implementation, and Kimi final read-only audit was run after validation. Final audit verdict: **PASS**.

Kimi final audit evidence:
- The enrichment uses real LEA/ALE subject-domain semantic kinds and categories rather than only exam-day buckets.
- New/improved nodes include source-family IDs, provenance notes, confidence, quality signals, and steward-admitted status.
- Raw-source uses are metadata-only and explicitly block protected payloads.
- `opencode.json` keeps the KG enrichment researcher route on `moonshot/kimi-k2.6`; report flags show `codex_spark_used_for_research_or_synthesis=false` and `kimi_used_for_advisory_synthesis=true`.
- No blockers were identified before final reporting.

## Safety Assertions

- No protected source payloads were ingested.
- No reviewer text, exam questions, answer keys, protected code clauses, protected tables, figures, or diagrams were copied.
- No raw-source PDF/XLSX body content was ingested.
- No Neo4j/live graph promotion, KG rebuild/reload/reset, or destructive graph operation was performed.
- No active Codex Spark enrichment routing was used; Kimi was used for advisory synthesis and final audit.
