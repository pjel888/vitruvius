# Ralph Context Snapshot: AEC-MEPFS Shadow Autonomy

## Task Statement

Continue safe shadow-only/read-only AEC-MEPFS backbone work from the current
repo state. Select, implement, verify, document, commit, push, and continue
through bounded safe slices until no further repo-evidenced safe work remains.

## Desired Outcome

- Improve shadow-only AEC-MEPFS evidence, QA, preview, and parity surfaces.
- Keep every change file-backed, auditable, and opt-in.
- Commit and push each green slice with validation evidence.

## Known Facts / Evidence

- Current pushed baseline before this snapshot: `fef745aa`.
- Latest completed slice refreshed route inventory, boundary audit, benchmark,
  and evidence manifest from clean source.
- GitNexus CLI status reports the repository indexed at current commit
  `fef745a`.
- Team tmux runtime cannot launch from this session because `TMUX` is unset.
- Gemini CLI exists but has been failing with service-disabled 403 in prior
  slices.
- Kimi CLI exists and has been usable for advisory review.

## Constraints

- Do not promote to live graph.
- Do not write Neo4j.
- Do not rebuild or reset KG.
- Do not ingest protected content.
- Do not cut over feature flags.
- Do not mount `/v2/resolve` or `/v2/resolve/trace`.
- Do not make Explorer adopt the shadow graph as its default graph.

## Unknowns / Open Questions

- Whether Gemini access remains blocked in this shell.
- Whether GitNexus symbol lookup can disambiguate duplicated private helper
  names before extraction.
- Whether any remaining safe slice after repo-state helper extraction is worth
  doing before runtime design acceptance.

## Likely Touchpoints

- `scripts/vitruvius/kg/backbone_api_route_inventory.py`
- `scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`
- `scripts/vitruvius/kg/backbone_shadow_benchmark.py`
- `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`
- `scripts/tests/test_kg_backbone_*`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
