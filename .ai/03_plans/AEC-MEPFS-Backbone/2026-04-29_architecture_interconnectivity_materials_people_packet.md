# 2026-04-29 Architecture Interconnectivity Materials People Packet

## Research Pack
- Team read-only audit confirmed the pre-phase file-backed backbone baseline at 9502 nodes, 11617 relationships, 95 source-rights rows, 52 resolver cases, and no duplicate IDs/path codes, missing edge endpoints, or missing parent paths.
- Kimi advisory ran through `kimi-for-coding/k2p6` after the configured Moonshot Kimi credential path was unavailable; the advisory approved the dry enrichment and confirmed metadata-only public source families were safe for the intended use.
- Official/public metadata source families used: official Pritzker laureates page, Wikidata CC0 identifier metadata, Getty vocabularies metadata, VIAF authority metadata, and Library of Congress linked-data authority metadata.
- Local raw-source custody was inspected by filename only: 350 files total, 142 architecture/material/history/technology/utility topic-signal filenames; no payload text was opened or ingested.

## Audit Document
Interconnectivity gaps before this phase:
- Materials taxonomy existed but lacked a dedicated cross-cutting material-performance and assembly facet with enough links to structural systems, envelopes, finishes, moisture, acoustics, fire, sustainability, tropical design, and specifications.
- Pritzker laureate/person/work/material paths were absent or too sparse for resolver questions about people, works, materials, and systems.
- Engineer/architect-engineer nodes were underconnected to bridge, shell, tensile, long-span, and structural-expression concepts.
- Prior source-reference label cleanup remained valid: learner-facing labels no longer exposed raw-source filename metadata, and direct selected-neighborhood highlighting is UI-side direct-edge based.

## Implementation Plan
1. Add a governed architecture interconnectivity enrichment generator for materials, people, works, source-rights rows, and resolver cases.
2. Add file-backed graph nodes and governed relationships only through existing predicates: `broader_than`, `has_facet`, `requires`, and `constrains`.
3. Add metadata-only public source-rights rows for Pritzker and authority-file source families.
4. Add resolver/API golden cases proving person-work-material, architect-engineer, material-performance, and Philippine vernacular material paths.
5. Preserve learner-facing label cleanup by asserting no source/process-heavy labels appear in concept graph output.
6. Refresh shadow staging, resolver QA, contract counts, API expectations, and validation evidence.

## Plan Critique
- Avoided direct person-to-material edges because they can imply unsupported signature-material claims; paths are mediated through works, roles, systems, or movements.
- Avoided new predicates; relationship semantics are mapped to existing governed predicates.
- Kept source references metadata-only and did not ingest biographies, essays, monograph text, raw PDFs, protected code, reviewer material, exam questions, tables, clauses, figures, or diagrams.
- Excluded interconnectivity material L3 nodes from the broad taxonomy auto-population pass to prevent generic broad-batch child nodes from diluting curated material taxonomy quality.

## Execution Checklist
- [x] Add graph enrichment generator.
- [x] Add source-rights metadata rows.
- [x] Add resolver golden cases.
- [x] Regenerate file-backed graph fixture, resolver fixture, source registry, shadow staging, and resolver QA reports.
- [x] Add Python KG tests and API resolver assertions.
- [x] Run graph integrity, label-quality, source-rights, API, UI-highlight, JSON, and safety validation.
- [x] Run Kimi advisory; final Kimi audit logged separately.

## Validation Report Link
- `.ai/05_logs/2026-04-29_architecture_interconnectivity_enrichment_validation.md`
