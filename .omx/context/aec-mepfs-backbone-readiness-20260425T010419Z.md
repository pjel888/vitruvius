# AEC-MEPFS Backbone Readiness Context

## Task Statement

Create a consensus readiness plan for the AEC-MEPFS Backbone architecture shift.
The user wants this to precede implementation, include blast-radius analysis,
improve the existing plan packet, and explicitly use multiple agents/skills.

## Desired Outcome

- Planning-only readiness plan.
- Improved `AEC-MEPFS-Backbone` plan packet.
- Clear gates before any code, Neo4j cleanup, feature flag flip, or derived
  artifact reset.
- Blast-radius and cleanup strategy grounded in repository evidence.
- Consensus review from architecture and critique perspectives.

## Known Facts / Evidence

- `AEC-MEPFS-Backbone/` exists under `.ai/03_plans/`.
- The packet currently contains research, audit, architecture overhaul plan,
  cleanup/blast-radius plan, validation note, and README.
- Current KG runtime loads shared taxonomy/concepts through
  `TaxonomyLoader`, not a governed backbone.
- `003_Canonical-Knowledge-Layer/backbone/` is absent.
- Current feature flags include `k_taxonomy_v2: false` and
  `k_backbone_validation: false`.
- Current Neo4j/Explorer MVP is based on the enriched `001-Laws` graph and
  should remain a baseline until shadow parity exists.
- `.gitnexus/meta.json` exists but is stale versus current `HEAD`; impact
  analysis must be refreshed before implementation.
- `omx_code_intel` AST MCP transport was unavailable during the prior planning
  pass.

## Constraints

- Planning only. No runtime implementation.
- No database cleanup yet.
- No Neo4j reset.
- No feature-flag flips.
- No raw/canonical rebuild.
- Follow `AGENTS.md` execution loop and plan/readiness gates.
- Use consensus planning before execution.

## Unknowns / Open Questions

- Whether shadow graph should use a separate Neo4j database, separate labels, or
  a separate local instance.
- Whether history/people/works should be top-level domain, facet/entity layer, or
  both.
- Standards licensing policy for broad seed ingestion versus reference mapping.
- Exact readiness scorecard thresholds for authoring, data, API, Explorer, and
  database cleanup.

## Likely Codebase Touchpoints

- `scripts/vitruvius/kg/schemas.py`
- `scripts/vitruvius/kg/evidence_materializer.py`
- `scripts/vitruvius/kg/unified_snapshot_builder.py`
- `scripts/vitruvius/kg/neo4j_loader.py`
- `scripts/vitruvius/kg/quality_report.py`
- `scripts/vitruvius/kg/relationship_enricher.py`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/config_flags.py`
- `config/vitruvius.yaml`
- `api/index.ts`
- `explorer/src/types/index.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/App.tsx`
- `explorer/src/components/graph/VisNetworkHost.tsx`
