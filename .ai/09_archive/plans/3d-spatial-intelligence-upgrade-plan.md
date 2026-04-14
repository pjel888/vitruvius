---
plan_id: 3d-spatial-intelligence-upgrade
phase: "cross-phase (new 1D + extends 6 + extends 8)"
title: 3D Spatial Intelligence Upgrade
status: planned
priority: medium
sprint: "Sprint H (post statistical-architectural-upgrade Stream H)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
stream_progress:
  L_spatial_ingestion_and_solver: pending (8 tasks)
  M_ifc_ontology_mapping: pending (4 tasks)
  N_spatial_daemon_node: pending (5 tasks)
  O_epistemic_foraging_scaffold: pending (3 tasks)
prerequisites:
  - Phase 8 graph contract frozen and shipping (✅ 2026-04-14, commit b269408)
  - Feature-flag loader from Stream A shipping (✅ 2026-04-14)
  - Mahalanobis outlier detector from Stream C.4 shipping (✅ 2026-04-14)
  - At least one spatial test fixture (synthetic, hand-authored — see §3.3)
dependencies:
  - .ai/13_research/3D-Thinking-improvement.md
  - .ai/03_plans/statistical-architectural-upgrade-plan.md
  - .ai/03_plans/phase-8-graph-contract-indexing-plan.md
  - .ai/06_specs/relationship-schema.md
  - .ai/06_specs/concept-schema.md
  - scripts/vitruvius/graph/ (shipping — contract.py, builder.py, integrity.py, snapshot.py, traverse.py, cli.py)
  - scripts/vitruvius/features.py (shipping)
  - scripts/vitruvius/normalization/outlier_detector.py (shipping — Stream C.4)
  - config/vitruvius.yaml (features block)
related_plans:
  - phase-8-graph-contract-indexing-plan.md (upstream — base graph)
  - statistical-architectural-upgrade-plan.md (sibling — this plan adds Streams L-O to the same subpackage conventions)
takes_precedence_over: []
non_breaking_guarantee: |
  Every module in this plan is gated by a new feature flag in
  config/vitruvius.yaml under `features.*` (all defaults FALSE). No
  existing file is deleted, renamed, or semantically changed. Additive
  extensions to the Phase 8 contract (new node types, new id prefixes)
  are guarded so that with all flags OFF, the builder produces
  byte-identical graph snapshots to the current main branch. A
  dedicated backward-compat test (test_3d_upgrade_backcompat.py) locks
  this invariant: it seeds a minimal canonical tree, builds the graph
  with every 3D flag OFF, and diffs the output against a frozen fixture.
gate:
  condition: "statistical-architectural-upgrade Stream H (Phase 8 graph intelligence extensions) is closed AND the canonical text graph has at least 25 verified edges."
  rationale: "Spatial reasoning only adds value once the text-evidence graph is load-bearing. Building spatial infrastructure on a 6-edge toy graph wastes engineering effort on constraint paths that cannot be evaluated in context."
unblocks:
  - Deterministic parametric compliance checking (Z3 replaces LLM for numeric constraints)
  - Future BIM/CAD interoperability via the IFC vocabulary
  - Future jurisdictional scaling (spatial rules are jurisdiction-specific)
  - Future Phase 11 autonomous source discovery (foraging scaffold)
---

# 3D Spatial Intelligence Upgrade Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Every task ships behind a feature flag — test the flag OFF path too.

**Goal.** Bridge Vitruvius from a text-only legal reasoner into a hybrid textual+spatial reasoner by (a) ingesting geometric data from a decoupled 3D daemon, (b) evaluating parametric constraints deterministically with the Z3 SMT solver, and (c) mapping canonical concepts onto the global AEC ontology (IFC classes + Psets) — all without modifying the existing text ingestion path or breaking the Phase 8 graph contract.

**Architecture.** Four dependency-ordered streams, each mapped to a distinct subsystem and isolated behind feature flags:

- **Stream L — Spatial Ingestion + Z3 Solver** — Python package `scripts/vitruvius/spatial/` that reads JSON manifests from a new `001B_Spatial-Source-Layer/` directory, validates them against a frozen schema, maps physical instance tags to canonical concept IDs, and evaluates numeric constraints via Z3.
- **Stream M — IFC/OWL Ontology Mapping** — Python package `scripts/vitruvius/ontology/` containing a static `concept-* → IfcClass + Pset` registry, optional concept frontmatter fields, and an OWL/Turtle exporter for the Phase 8 snapshot.
- **Stream N — Decoupled Spatial Daemon** — Standalone TypeScript/Node.js service under `spatial-daemon/` (outside the Python path) that consumes raw vertex arrays, runs Three.js AABB + a custom GJK intersection check, and writes JSON files to `001B_Spatial-Source-Layer/`.
- **Stream O — Epistemic Foraging Scaffold** — Python package `scripts/vitruvius/foraging/` with a watched-sources YAML registry, a drift detector that wraps the existing Mahalanobis module, and a hash-based duplicate detector stub. **No live HTTP scrapers ship in this plan** — they are explicitly deferred to §2.2.

**Tech Stack (Python).** stdlib + PyYAML (shipping) + jsonschema ≥4.0 (new) + z3-solver ≥4.12,<5.0 (new, optional) + ifcopenshell ≥0.7,<1.0 (new, optional, imported only under flag). All imports are lazy and guarded so environments without the optional deps continue to pass the full suite.

**Tech Stack (Node.js daemon).** Node ≥20 + TypeScript ≥5 + three@^0.164 + vitest@^1 (for unit tests). The daemon is a sibling directory with its own `package.json`; it is never imported by Python code and has no build-time coupling to the pipeline.

---

## 1. Preamble

### 1.1 Why This Plan Exists
The research document [`.ai/13_research/3D-Thinking-improvement.md`](../13_research/3D-Thinking-improvement.md) proposes four structural evolutions that would expand Vitruvius beyond textual regulatory reasoning: ontological unification with IFC/OWL, Physics-Informed Neural Networks, autonomous epistemic foraging, and a decoupled spatial translator. Of these, the spatial translator pathway is the only one with (a) a concrete architectural specification, (b) a defined interoperability contract, and (c) an immediate payoff for a compliance-checking engine. IFC/OWL mapping is shippable at a static-registry level. Epistemic foraging is valuable as a scaffold so the data model is ready when scrapers are built. PINNs require training data and GPUs that Vitruvius does not have.

This plan consolidates the three shippable evolutions into a dependency-ordered execution blueprint that respects the Vitruvius non-breaking guarantee, the Phase 8 graph contract, and the 8GB M2 RAM ceiling.

### 1.2 Scope Boundary

**In scope**
- New `001B_Spatial-Source-Layer/` directory with a frozen JSON Schema contract.
- New Python package `scripts/vitruvius/spatial/` (schema validator, walker, concept mapper, Z3 evaluator).
- New Python package `scripts/vitruvius/ontology/` (IFC lookup registry, OWL exporter).
- New Python package `scripts/vitruvius/foraging/` (watched-sources registry + drift detector stub).
- New TypeScript daemon `spatial-daemon/` (AABB + GJK + JSON writer).
- CLI command additions to `scripts/pipeline_cli.py`: `ingest-spatial`, `evaluate-spatial`, `export-graph-owl`, `foraging-scan`.
- Additive Phase 8 contract extensions: new node type `spatial_instance`, new id prefixes `instance-` and `spatial-`, new edge status `spatially_verified`, new predicates `spatial_intersects` / `spatial_clearance` / `spatial_adjacent_to` / `spatial_contains`.
- Eight new feature flags under `features.*`.
- A dedicated backward-compat regression test that locks flag-OFF determinism.

**Out of scope (deferred — see §2)**
- Physics-Informed Neural Networks (PINNs). Requires GPU + training corpus Vitruvius does not own.
- Live HTTP scrapers for DPWH, LGUs, ASTM. Scaffold only — the YAML registry and drift detector ship; the fetcher does not.
- SketchUp plugin bundle. The daemon accepts raw JSON exports; plugin authorship is out of scope.
- Neo4j / Dgraph / external graph database. Phase 8 principle P1 holds: the filesystem is the database.
- Visualisation (Cytoscape, Three.js canvas viewer for end users). Rendering is a Phase 10 concern.
- Real IFC file (.ifc) parsing. Stream M ships a *mapping* (concept → IFC class), not an importer.

### 1.3 Precedence Declaration
This plan is **gated behind** `statistical-architectural-upgrade-plan.md` Stream H closure (see frontmatter `gate`). It does not supersede any existing plan. It extends `phase-8-graph-contract-indexing-plan.md` in an additive, flag-gated way and introduces a new Phase label (**1D — Spatial Source Layer**) that does not conflict with any existing phase.

### 1.4 Non-Breaking Guarantee
The mechanism mirrors the statistical-architectural-upgrade-plan §1.3:

1. Every new module has a feature flag in `config/vitruvius.yaml` under `features.*`, default `false`.
2. With all flags OFF, no existing CLI command produces a different byte sequence than it did before this plan landed.
3. Additive graph-contract extensions are guarded: `ALLOWED_NODE_TYPES` and `ALLOWED_ID_PREFIXES` grow by strictly-new members, and the walker only emits those members when the relevant flag is ON.
4. A new `test_3d_upgrade_backcompat.py` locks the flag-OFF path by running `build_snapshot` against a frozen 3-file canonical fixture and diffing against a checked-in expected snapshot.
5. The Z3, jsonschema, ifcopenshell, and three.js dependencies are **all optional**. Importing the new packages without the libs installed returns a "feature disabled" error rather than a crash.

## 2. Deferred Capabilities and Rationale

### 2.1 Physics-Informed Neural Networks (PINNs) — DEFERRED
The research doc §3 proposes training PINNs on structural/thermodynamic PDEs to validate material compliance. This is deferred because:
- PINN training requires a GPU (8GB M2 is CPU-only for this workload).
- Vitruvius owns no structured PDE training corpus — the existing sources are text, not tensor fields.
- Z3 already gives us deterministic numeric compliance without statistical learning (Stream L.5).
- Reopen condition: a training corpus exists AND a GPU workstation is available AND Z3 has been shown insufficient for a real use case.

### 2.2 Live Epistemic Foraging (HTTP scrapers) — SCAFFOLD ONLY
The research doc §4 proposes agent swarms monitoring DPWH/LGU/ASTM registries. Live scrapers are a large attack surface (SSRF, credential exposure, parse injection) and a legal surface (terms of service, rate limits). Stream O ships only:
- The watched-sources YAML registry (§11.1).
- A drift detector that wraps the existing Mahalanobis module (§11.2).
- A duplicate detector stub using SHA-256 (§11.3).
- **No `urllib.request` / `requests` / `httpx` call ships under any flag.**

Reopen condition: a dedicated security review of the fetcher + a human-admin approval workflow is in place.

### 2.3 Full IFC Importer — DEFERRED
Stream M ships a *static lookup table* mapping `concept-*` IDs to IFC classes and Psets. It does not parse real `.ifc` files via ifcopenshell — that's future Phase 11 work. The lookup table alone unlocks:
- Exporting the Phase 8 graph as OWL/Turtle with IFC URIs.
- Future-proofing the concept schema by reserving `ifc_class` and `ifc_psets` frontmatter fields.
- Validation lint that rejects concepts with unknown IFC class names.

Reopen condition: a real BIM model (.ifc file) lands in `001_Raw-Source-Layer/` and needs to be translated to concept nodes.

## 3. Prerequisites and Dependencies

### 3.1 Library Prerequisites
```text
# Added to requirements.txt under a new "Stream L-O (3D Spatial Upgrade)" section:
jsonschema>=4.0,<5.0        # L.2 — validate the spatial JSON contract
z3-solver>=4.12,<5.0        # L.5 — SMT-based constraint evaluation
ifcopenshell>=0.7,<1.0      # M.1 — OPTIONAL, not imported unless m_ifc_ontology_mapping is ON
rdflib>=7.0,<8.0            # M.3 — RDF/Turtle serialization
```

The existing `numpy`/`scipy` dependencies (from Stream A) are reused by Stream O.2 (Mahalanobis drift detector).

### 3.2 Node.js Prerequisites
The TypeScript daemon is a sibling subdirectory with its own dependency surface. It does not affect the Python pipeline:
```text
# spatial-daemon/package.json
"dependencies": {
  "three": "^0.164.0"
},
"devDependencies": {
  "typescript": "^5.4.0",
  "vitest": "^1.4.0",
  "@types/node": "^20.12.0"
}
```

### 3.3 Test Fixtures
A new fixtures directory `scripts/tests/fixtures/spatial/` is created. It contains:
- `sample_residential_01_spatial.json` — a synthetic, hand-authored payload (3 instances, 2 edges) conforming to the §6 schema.
- `sample_residential_01_expected_candidates.json` — the expected output of the ingestion walker.
- `expected_frozen_snapshot.json` — a byte-identical baseline for the backward-compat test.

## 4. File Structure

| Path | Owner | Stream | Status |
|---|---|---|---|
| `001B_Spatial-Source-Layer/.gitkeep` | new | L.1 | create |
| `001B_Spatial-Source-Layer/README.md` | new | L.1 | create |
| `requirements.txt` | modify | L.1 | add jsonschema, z3-solver, rdflib, ifcopenshell |
| `config/vitruvius.yaml` | modify | L.1 | add 8 new `features.*` flags |
| `scripts/vitruvius/spatial/__init__.py` | new | L.1 | package marker |
| `scripts/vitruvius/spatial/schema.py` | new | L.2 | JSON Schema + validator |
| `scripts/vitruvius/spatial/walker.py` | new | L.3 | walk `001B_…/*.json`, emit candidates |
| `scripts/vitruvius/spatial/concept_mapper.py` | new | L.4 | map `instance-*` tags to `concept-*` IDs |
| `scripts/vitruvius/spatial/constraint_solver.py` | new | L.5-L.6 | Z3 evaluator |
| `scripts/vitruvius/spatial/cli.py` | new | L.7 | `run_ingest_spatial`, `run_evaluate_spatial` |
| `scripts/vitruvius/graph/contract.py` | modify | L.1 | additive: new node type, new prefixes, new status |
| `scripts/pipeline_cli.py` | modify | L.7 | register `ingest-spatial`, `evaluate-spatial`, `export-graph-owl`, `foraging-scan` |
| `scripts/tests/test_spatial_schema.py` | new | L.2 | schema validator tests |
| `scripts/tests/test_spatial_walker.py` | new | L.3 | walker tests |
| `scripts/tests/test_spatial_concept_mapper.py` | new | L.4 | mapper tests |
| `scripts/tests/test_spatial_constraint_solver.py` | new | L.5-L.6 | Z3 tests |
| `scripts/tests/test_spatial_cli.py` | new | L.7 | CLI subprocess tests |
| `scripts/tests/test_3d_upgrade_backcompat.py` | new | L.8 | flag-OFF determinism |
| `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json` | new | L.8 | fixture |
| `scripts/tests/fixtures/spatial/expected_frozen_snapshot.json` | new | L.8 | fixture |
| `scripts/vitruvius/ontology/__init__.py` | new | M.1 | package marker |
| `scripts/vitruvius/ontology/ifc_registry.py` | new | M.1 | loader for ifc_mapping.yaml |
| `scripts/vitruvius/ontology/ifc_mapping.yaml` | new | M.1 | static concept→IfcClass map |
| `scripts/vitruvius/ontology/owl_exporter.py` | new | M.3 | Turtle/OWL writer |
| `scripts/vitruvius/ontology/ifc_validator.py` | new | M.4 | lint concept frontmatter |
| `scripts/tests/test_ontology_ifc_registry.py` | new | M.1 | registry tests |
| `scripts/tests/test_ontology_concept_frontmatter.py` | new | M.2 | optional field tests |
| `scripts/tests/test_ontology_owl_exporter.py` | new | M.3 | Turtle output tests |
| `scripts/tests/test_ontology_ifc_validator.py` | new | M.4 | validator tests |
| `spatial-daemon/package.json` | new | N.1 | Node project |
| `spatial-daemon/tsconfig.json` | new | N.1 | TS config |
| `spatial-daemon/vitest.config.ts` | new | N.1 | test config |
| `spatial-daemon/src/types.ts` | new | N.1 | interfaces |
| `spatial-daemon/src/aabb.ts` | new | N.2 | AABB builder |
| `spatial-daemon/src/gjk.ts` | new | N.3 | GJK intersection |
| `spatial-daemon/src/contract_writer.ts` | new | N.4 | JSON emitter |
| `spatial-daemon/src/cli.ts` | new | N.5 | entry point |
| `spatial-daemon/tests/aabb.test.ts` | new | N.2 | AABB tests |
| `spatial-daemon/tests/gjk.test.ts` | new | N.3 | GJK tests |
| `spatial-daemon/tests/contract_writer.test.ts` | new | N.4 | writer tests |
| `spatial-daemon/tests/cli.test.ts` | new | N.5 | smoke test |
| `spatial-daemon/tests/fixtures/box_intersection.json` | new | N.5 | sample |
| `spatial-daemon/README.md` | new | N.1 | daemon overview |
| `scripts/vitruvius/foraging/__init__.py` | new | O.1 | package marker |
| `scripts/vitruvius/foraging/watched_sources.py` | new | O.1 | YAML loader |
| `scripts/vitruvius/foraging/watched_sources.yaml` | new | O.1 | registry file |
| `scripts/vitruvius/foraging/drift_detector.py` | new | O.2 | Mahalanobis wrapper |
| `scripts/vitruvius/foraging/duplicate_detector.py` | new | O.3 | SHA-256 stub |
| `scripts/tests/test_foraging_watched_sources.py` | new | O.1 | registry tests |
| `scripts/tests/test_foraging_drift_detector.py` | new | O.2 | drift tests |
| `scripts/tests/test_foraging_duplicate_detector.py` | new | O.3 | dup tests |
| `.ai/06_specs/spatial-schema.md` | new | L.2 | schema documentation |

## 5. Feature Flag Additions

Append to `config/vitruvius.yaml` under the existing `features:` block:

```yaml
  # Stream L — Spatial Ingestion + Z3 Solver
  l_spatial_ingestion: false
  l_z3_constraint_solver: false
  # Stream M — IFC/OWL Ontology
  m_ifc_ontology_mapping: false
  m_owl_turtle_export: false
  # Stream N — Spatial Daemon integration (marker; daemon lives outside Python)
  n_spatial_daemon_enabled: false
  # Stream O — Epistemic Foraging (scaffold only)
  o_watched_sources_registry: false
  o_mahalanobis_drift_detection: false
  o_duplicate_detector: false
```

Every flag defaults to `false`. Flipping a flag to `true` activates the corresponding module; flipping it back to `false` restores prior behaviour with zero code rollback. The Features loader (`scripts/vitruvius/features.py`) already returns `False` for unknown keys, so the test suite continues to pass when the flags are absent.

## 6. Spatial JSON Schema (Authoritative Contract)

Frozen in `.ai/06_specs/spatial-schema.md` as version `1.0.0`. Any future change bumps the schema version and requires a migration plan.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://vitruvius.local/schemas/spatial-contract-v1.json",
  "title": "Vitruvius Spatial Contract",
  "type": "object",
  "required": ["schema_version", "spatial_context_id", "generated_at_utc", "instances", "spatial_edges"],
  "properties": {
    "schema_version": {
      "type": "string",
      "enum": ["1.0.0"]
    },
    "spatial_context_id": {
      "type": "string",
      "pattern": "^spatial-[a-z0-9][a-z0-9-]*$",
      "description": "Unique id for the physical model, e.g. 'spatial-residential-01'"
    },
    "generated_at_utc": {
      "type": "string",
      "format": "date-time"
    },
    "source_daemon": {
      "type": "string",
      "description": "Identifier of the daemon that produced this file (e.g. 'spatial-daemon@0.1.0')."
    },
    "instances": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["instance_id", "canonical_concept_id"],
        "properties": {
          "instance_id": {
            "type": "string",
            "pattern": "^instance-[a-z0-9][a-z0-9-]*$"
          },
          "canonical_concept_id": {
            "type": "string",
            "pattern": "^concept-[a-z0-9][a-z0-9-]*$"
          },
          "bounding_box": {
            "type": "object",
            "required": ["min", "max"],
            "properties": {
              "min": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
              "max": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3}
            }
          }
        }
      }
    },
    "spatial_edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_instance", "predicate", "target_instance"],
        "properties": {
          "source_instance": {"type": "string", "pattern": "^instance-"},
          "predicate": {
            "type": "string",
            "enum": ["spatial_intersects", "spatial_clearance", "spatial_adjacent_to", "spatial_contains"]
          },
          "target_instance": {"type": "string", "pattern": "^instance-"},
          "value": {"type": "number"},
          "unit": {"type": "string", "enum": ["meters", "millimeters", "feet", "inches"]}
        }
      }
    }
  }
}
```

---

## 7. Stream L — Spatial Ingestion + Z3 Solver

### Task L.1: Dependency Bootstrap, Feature Flags, Directory Scaffold

**Files:**
- Create: `001B_Spatial-Source-Layer/.gitkeep`
- Create: `001B_Spatial-Source-Layer/README.md`
- Create: `scripts/vitruvius/spatial/__init__.py`
- Modify: `requirements.txt` (append Stream L-O section)
- Modify: `config/vitruvius.yaml` (append 8 flags)
- Modify: `scripts/vitruvius/graph/contract.py` (additive: new node type, new id prefixes, new edge status)
- Test: `scripts/tests/test_spatial_bootstrap.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_bootstrap.py
"""Stream L.1 — bootstrap sanity checks.

These tests lock in the additive contract changes so a later task cannot
regress the Phase 8 graph schema. The graph walker is NOT run here — we
only verify the contract constants themselves.
"""
from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_spatial_source_layer_directory_exists() -> None:
    assert (REPO_ROOT / "001B_Spatial-Source-Layer").is_dir()


def test_spatial_package_importable() -> None:
    import vitruvius.spatial  # noqa: F401


def test_new_feature_flags_present_and_default_false() -> None:
    import yaml
    cfg = yaml.safe_load((REPO_ROOT / "config" / "vitruvius.yaml").read_text())
    flags = cfg.get("features", {})
    for name in (
        "l_spatial_ingestion",
        "l_z3_constraint_solver",
        "m_ifc_ontology_mapping",
        "m_owl_turtle_export",
        "n_spatial_daemon_enabled",
        "o_watched_sources_registry",
        "o_mahalanobis_drift_detection",
        "o_duplicate_detector",
    ):
        assert name in flags, f"missing flag: {name}"
        assert flags[name] is False, f"flag {name} must default false"


def test_graph_contract_additive_extensions() -> None:
    from vitruvius.graph.contract import (
        ALLOWED_NODE_TYPES,
        ALLOWED_ID_PREFIXES,
        ALLOWED_EDGE_STATUSES,
    )
    assert "spatial_instance" in ALLOWED_NODE_TYPES
    assert "instance-" in ALLOWED_ID_PREFIXES
    assert "spatial-" in ALLOWED_ID_PREFIXES
    assert "spatially_verified" in ALLOWED_EDGE_STATUSES
    # Preserve the original members (non-breaking guarantee).
    for original in ("source", "concept", "attribute"):
        assert original in ALLOWED_NODE_TYPES
    for original in ("law-", "irr-", "concept-", "rel-", "source-", "handout-", "reviewer-", "law-section-"):
        assert original in ALLOWED_ID_PREFIXES
    for original in ("verified", "unverified"):
        assert original in ALLOWED_EDGE_STATUSES
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_bootstrap.py -v`

Expected: FAIL with `AssertionError: missing flag: l_spatial_ingestion` (or similar) and `ModuleNotFoundError: No module named 'vitruvius.spatial'`.

- [ ] **Step 3: Create the directory and package scaffold**

```bash
mkdir -p 001B_Spatial-Source-Layer
touch 001B_Spatial-Source-Layer/.gitkeep
mkdir -p scripts/vitruvius/spatial
```

Create `001B_Spatial-Source-Layer/README.md`:
```markdown
# 001B — Spatial Source Layer

> **Purpose:** Landing zone for JSON manifests produced by the decoupled
> spatial daemon (`spatial-daemon/`). Files here conform to the contract
> in `.ai/06_specs/spatial-schema.md` v1.0.0.
>
> **Pipeline stage:** 1D. Consumed by `scripts/vitruvius/spatial/walker.py`
> only when `features.l_spatial_ingestion` is true.
>
> **Non-breaking guarantee:** With the flag off, this directory is ignored.
```

Create `scripts/vitruvius/spatial/__init__.py`:
```python
"""Spatial ingestion and constraint solving (Stream L).

Every module in this package is gated by one or more feature flags in
config/vitruvius.yaml under features.l_*. With all flags OFF, importing
this package is a no-op.
"""
```

- [ ] **Step 4: Extend `config/vitruvius.yaml` with the flags**

Append to the existing `features:` block (keep existing `a_*` through `k_*` flags untouched):
```yaml
  # Stream L — Spatial Ingestion + Z3 Solver
  l_spatial_ingestion: false
  l_z3_constraint_solver: false
  # Stream M — IFC/OWL Ontology
  m_ifc_ontology_mapping: false
  m_owl_turtle_export: false
  # Stream N — Spatial Daemon integration marker
  n_spatial_daemon_enabled: false
  # Stream O — Epistemic Foraging Scaffold
  o_watched_sources_registry: false
  o_mahalanobis_drift_detection: false
  o_duplicate_detector: false
```

- [ ] **Step 5: Extend the graph contract (additive)**

Modify `scripts/vitruvius/graph/contract.py`:

```python
ALLOWED_NODE_TYPES = frozenset({"source", "concept", "attribute", "spatial_instance"})

ALLOWED_TRUST_LEVELS = frozenset({
    "primary", "secondary", "tertiary", "unverified", "derived",
})

ALLOWED_EDGE_STATUSES = frozenset({"verified", "unverified", "spatially_verified"})

ALLOWED_ID_PREFIXES = frozenset({
    "law-",
    "irr-",
    "concept-",
    "rel-",
    "source-",
    "handout-",
    "reviewer-",
    "law-section-",
    "instance-",
    "spatial-",
})
```

No other lines in `contract.py` change. `validate_node` / `validate_edge` continue to accept every prior shape; they now additionally accept the new members.

- [ ] **Step 6: Append Stream L-O entries to `requirements.txt`**

```text
# Stream L-O (3D Spatial Intelligence Upgrade) — see
# .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md §3.1. Every lib here
# is optional: the Python packages under scripts/vitruvius/spatial/,
# scripts/vitruvius/ontology/, and scripts/vitruvius/foraging/ import them
# lazily and fall back to a "feature disabled" error when missing.
jsonschema>=4.0,<5.0
z3-solver>=4.12,<5.0
rdflib>=7.0,<8.0
ifcopenshell>=0.7,<1.0
```

- [ ] **Step 7: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_bootstrap.py -v`

Expected: 4 PASSED.

- [ ] **Step 8: Full regression**

Run: `PYTHONPATH=scripts pytest scripts/tests/ -q`

Expected: the full suite (currently 788 tests) still passes. The graph contract tests (`test_graph_contract.py`) must not regress — they still pass because the changes are additive.

- [ ] **Step 9: Commit**

```bash
git add 001B_Spatial-Source-Layer scripts/vitruvius/spatial/__init__.py scripts/tests/test_spatial_bootstrap.py config/vitruvius.yaml scripts/vitruvius/graph/contract.py requirements.txt
git commit -m "feat(spatial): Stream L.1 bootstrap — spatial layer + feature flags + graph contract extensions"
```

---

### Task L.2: Spatial JSON Schema Module and Validator

**Files:**
- Create: `scripts/vitruvius/spatial/schema.py`
- Create: `.ai/06_specs/spatial-schema.md`
- Create: `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json`
- Test: `scripts/tests/test_spatial_schema.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_schema.py
"""Stream L.2 — spatial JSON schema validator."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.spatial.schema import (
    SpatialSchemaError,
    SPATIAL_SCHEMA_VERSION,
    validate_spatial_payload,
)


FIX_DIR = Path(__file__).resolve().parent / "fixtures" / "spatial"


def _load_sample() -> dict:
    return json.loads((FIX_DIR / "sample_residential_01_spatial.json").read_text())


def test_schema_version_constant() -> None:
    assert SPATIAL_SCHEMA_VERSION == "1.0.0"


def test_valid_sample_passes() -> None:
    payload = _load_sample()
    validate_spatial_payload(payload)


def test_missing_schema_version_is_rejected() -> None:
    payload = _load_sample()
    del payload["schema_version"]
    with pytest.raises(SpatialSchemaError, match="schema_version"):
        validate_spatial_payload(payload)


def test_wrong_schema_version_is_rejected() -> None:
    payload = _load_sample()
    payload["schema_version"] = "2.0.0"
    with pytest.raises(SpatialSchemaError, match="schema_version"):
        validate_spatial_payload(payload)


def test_instance_id_must_have_instance_prefix() -> None:
    payload = _load_sample()
    payload["instances"][0]["instance_id"] = "door-01"
    with pytest.raises(SpatialSchemaError, match="instance-"):
        validate_spatial_payload(payload)


def test_canonical_concept_id_must_have_concept_prefix() -> None:
    payload = _load_sample()
    payload["instances"][0]["canonical_concept_id"] = "fire-door"
    with pytest.raises(SpatialSchemaError, match="concept-"):
        validate_spatial_payload(payload)


def test_unknown_predicate_rejected() -> None:
    payload = _load_sample()
    payload["spatial_edges"][0]["predicate"] = "next_to"
    with pytest.raises(SpatialSchemaError, match="predicate"):
        validate_spatial_payload(payload)


def test_spatial_context_id_must_have_spatial_prefix() -> None:
    payload = _load_sample()
    payload["spatial_context_id"] = "model-01"
    with pytest.raises(SpatialSchemaError, match="spatial_context_id"):
        validate_spatial_payload(payload)
```

Also create the fixture `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json`:

```json
{
  "schema_version": "1.0.0",
  "spatial_context_id": "spatial-residential-01",
  "generated_at_utc": "2026-04-15T09:00:00Z",
  "source_daemon": "spatial-daemon@0.1.0",
  "instances": [
    {
      "instance_id": "instance-egress-corridor-01",
      "canonical_concept_id": "concept-means-of-egress",
      "bounding_box": {"min": [0.0, 0.0, 0.0], "max": [10.0, 1.1, 2.4]}
    },
    {
      "instance_id": "instance-fire-door-01",
      "canonical_concept_id": "concept-doors-and-exits",
      "bounding_box": {"min": [5.0, 0.0, 0.0], "max": [5.9, 0.1, 2.1]}
    },
    {
      "instance_id": "instance-setback-front",
      "canonical_concept_id": "concept-setbacks",
      "bounding_box": {"min": [-3.0, 0.0, 0.0], "max": [0.0, 1.0, 3.0]}
    }
  ],
  "spatial_edges": [
    {
      "source_instance": "instance-egress-corridor-01",
      "predicate": "spatial_clearance",
      "target_instance": "instance-fire-door-01",
      "value": 1.1,
      "unit": "meters"
    },
    {
      "source_instance": "instance-egress-corridor-01",
      "predicate": "spatial_contains",
      "target_instance": "instance-fire-door-01"
    }
  ]
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_schema.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.spatial.schema'`.

- [ ] **Step 3: Implement the schema module**

Create `scripts/vitruvius/spatial/schema.py`:

```python
"""Stream L.2 — JSON Schema validator for the spatial contract.

The schema is inlined here rather than read from disk so the validator has
no filesystem side-effects. The authoritative spec lives in
.ai/06_specs/spatial-schema.md — that file and this constant must stay in
sync (enforced by a lint check in later tasks).
"""
from __future__ import annotations

from typing import Any


SPATIAL_SCHEMA_VERSION = "1.0.0"


class SpatialSchemaError(ValueError):
    """Raised when a payload does not conform to the frozen contract."""


_ALLOWED_PREDICATES = frozenset({
    "spatial_intersects",
    "spatial_clearance",
    "spatial_adjacent_to",
    "spatial_contains",
})


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SpatialSchemaError(message)


def _is_three_number_vector(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(v, (int, float)) for v in value)
    )


def _validate_instance(entry: Any, idx: int) -> None:
    _ensure(isinstance(entry, dict), f"instances[{idx}] must be an object")
    iid = entry.get("instance_id")
    _ensure(
        isinstance(iid, str) and iid.startswith("instance-"),
        f"instances[{idx}].instance_id must start with 'instance-'",
    )
    cid = entry.get("canonical_concept_id")
    _ensure(
        isinstance(cid, str) and cid.startswith("concept-"),
        f"instances[{idx}].canonical_concept_id must start with 'concept-'",
    )
    bbox = entry.get("bounding_box")
    if bbox is not None:
        _ensure(isinstance(bbox, dict), f"instances[{idx}].bounding_box must be an object")
        _ensure(
            _is_three_number_vector(bbox.get("min")),
            f"instances[{idx}].bounding_box.min must be a 3-number list",
        )
        _ensure(
            _is_three_number_vector(bbox.get("max")),
            f"instances[{idx}].bounding_box.max must be a 3-number list",
        )


def _validate_edge(entry: Any, idx: int) -> None:
    _ensure(isinstance(entry, dict), f"spatial_edges[{idx}] must be an object")
    src = entry.get("source_instance")
    tgt = entry.get("target_instance")
    pred = entry.get("predicate")
    _ensure(
        isinstance(src, str) and src.startswith("instance-"),
        f"spatial_edges[{idx}].source_instance must start with 'instance-'",
    )
    _ensure(
        isinstance(tgt, str) and tgt.startswith("instance-"),
        f"spatial_edges[{idx}].target_instance must start with 'instance-'",
    )
    _ensure(
        pred in _ALLOWED_PREDICATES,
        f"spatial_edges[{idx}].predicate {pred!r} not in {sorted(_ALLOWED_PREDICATES)}",
    )
    if "value" in entry:
        _ensure(
            isinstance(entry["value"], (int, float)),
            f"spatial_edges[{idx}].value must be numeric",
        )


def validate_spatial_payload(payload: Any) -> None:
    """Validate a dict against the frozen contract. Raises SpatialSchemaError on failure."""
    _ensure(isinstance(payload, dict), "payload must be a dict")
    version = payload.get("schema_version")
    _ensure(
        version == SPATIAL_SCHEMA_VERSION,
        f"schema_version must be {SPATIAL_SCHEMA_VERSION!r} (got {version!r})",
    )
    ctx = payload.get("spatial_context_id")
    _ensure(
        isinstance(ctx, str) and ctx.startswith("spatial-"),
        f"spatial_context_id must start with 'spatial-' (got {ctx!r})",
    )
    _ensure(isinstance(payload.get("generated_at_utc"), str), "generated_at_utc must be a string")
    instances = payload.get("instances")
    _ensure(isinstance(instances, list), "instances must be a list")
    for i, inst in enumerate(instances):
        _validate_instance(inst, i)
    edges = payload.get("spatial_edges")
    _ensure(isinstance(edges, list), "spatial_edges must be a list")
    for i, edge in enumerate(edges):
        _validate_edge(edge, i)
```

Create `.ai/06_specs/spatial-schema.md` containing (a) the JSON Schema from §6 verbatim, (b) a pointer to `schema.py` for the authoritative validator, (c) the semantics of each predicate.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_schema.py -v`

Expected: 8 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/schema.py scripts/tests/test_spatial_schema.py scripts/tests/fixtures/spatial/sample_residential_01_spatial.json .ai/06_specs/spatial-schema.md
git commit -m "feat(spatial): Stream L.2 schema validator + frozen JSON contract v1.0.0"
```

---

### Task L.3: Spatial Ingestion Walker

**Files:**
- Create: `scripts/vitruvius/spatial/walker.py`
- Test: `scripts/tests/test_spatial_walker.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_walker.py
"""Stream L.3 — walker for 001B_Spatial-Source-Layer."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.spatial.walker import (
    SpatialCandidate,
    walk_spatial_layer,
)


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_payload(context_id: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "spatial_context_id": context_id,
        "generated_at_utc": "2026-04-15T09:00:00Z",
        "instances": [
            {
                "instance_id": "instance-egress-corridor-01",
                "canonical_concept_id": "concept-means-of-egress",
            }
        ],
        "spatial_edges": [
            {
                "source_instance": "instance-egress-corridor-01",
                "predicate": "spatial_clearance",
                "target_instance": "instance-fire-door-01",
                "value": 1.1,
                "unit": "meters",
            }
        ],
    }


def test_walker_empty_dir_returns_empty(tmp_path: Path) -> None:
    candidates = walk_spatial_layer(tmp_path)
    assert candidates == []


def test_walker_reads_single_file(tmp_path: Path) -> None:
    _write(tmp_path / "residential.json", _make_payload("spatial-residential-01"))
    candidates = walk_spatial_layer(tmp_path)
    assert len(candidates) == 1
    c = candidates[0]
    assert isinstance(c, SpatialCandidate)
    assert c.spatial_context_id == "spatial-residential-01"
    assert c.predicate == "spatial_clearance"
    assert c.value == 1.1


def test_walker_sorts_by_context_id_then_edge_index(tmp_path: Path) -> None:
    _write(tmp_path / "b.json", _make_payload("spatial-b-01"))
    _write(tmp_path / "a.json", _make_payload("spatial-a-01"))
    candidates = walk_spatial_layer(tmp_path)
    assert [c.spatial_context_id for c in candidates] == ["spatial-a-01", "spatial-b-01"]


def test_walker_skips_non_json_files(tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text("ignore me", encoding="utf-8")
    _write(tmp_path / "real.json", _make_payload("spatial-real-01"))
    candidates = walk_spatial_layer(tmp_path)
    assert len(candidates) == 1


def test_walker_raises_on_invalid_payload(tmp_path: Path) -> None:
    _write(tmp_path / "bad.json", {"schema_version": "1.0.0"})
    with pytest.raises(Exception):
        walk_spatial_layer(tmp_path)


def test_walker_missing_dir_returns_empty(tmp_path: Path) -> None:
    candidates = walk_spatial_layer(tmp_path / "nonexistent")
    assert candidates == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_walker.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.spatial.walker'`.

- [ ] **Step 3: Implement the walker**

Create `scripts/vitruvius/spatial/walker.py`:

```python
"""Stream L.3 — walk 001B_Spatial-Source-Layer and emit candidate records.

The walker is deterministic: files are visited in sorted-filename order, and
each file's edges keep their declared order. The output is a flat list of
SpatialCandidate dataclasses; higher layers (concept_mapper, constraint_solver)
consume that list without re-reading the source files.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .schema import validate_spatial_payload


@dataclass(frozen=True)
class SpatialCandidate:
    spatial_context_id: str
    generated_at_utc: str
    source_instance: str
    predicate: str
    target_instance: str
    value: float | None
    unit: str | None
    source_concept_id: str | None
    target_concept_id: str | None
    source_file: str


def _index_instances(instances: list[dict[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for inst in instances:
        iid = inst.get("instance_id")
        cid = inst.get("canonical_concept_id")
        if isinstance(iid, str) and isinstance(cid, str):
            out[iid] = cid
    return out


def walk_spatial_layer(spatial_dir: Path) -> list[SpatialCandidate]:
    if not spatial_dir.exists() or not spatial_dir.is_dir():
        return []
    files = sorted(p for p in spatial_dir.glob("*.json") if p.is_file())
    candidates: list[SpatialCandidate] = []
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        validate_spatial_payload(payload)
        by_instance = _index_instances(payload.get("instances", []))
        for edge in payload.get("spatial_edges", []):
            candidates.append(
                SpatialCandidate(
                    spatial_context_id=payload["spatial_context_id"],
                    generated_at_utc=payload.get("generated_at_utc", ""),
                    source_instance=edge["source_instance"],
                    predicate=edge["predicate"],
                    target_instance=edge["target_instance"],
                    value=edge.get("value"),
                    unit=edge.get("unit"),
                    source_concept_id=by_instance.get(edge["source_instance"]),
                    target_concept_id=by_instance.get(edge["target_instance"]),
                    source_file=path.name,
                )
            )
    candidates.sort(key=lambda c: (c.spatial_context_id, c.source_file, c.source_instance, c.target_instance, c.predicate))
    return candidates
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_walker.py -v`

Expected: 6 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/walker.py scripts/tests/test_spatial_walker.py
git commit -m "feat(spatial): Stream L.3 walker — 001B layer -> SpatialCandidate list"
```

---

### Task L.4: Concept Instance Mapper (Cross-Reference with Canonical Layer)

**Files:**
- Create: `scripts/vitruvius/spatial/concept_mapper.py`
- Test: `scripts/tests/test_spatial_concept_mapper.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_concept_mapper.py
"""Stream L.4 — validate spatial candidates against canonical concept layer."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.spatial.concept_mapper import (
    MappingIssue,
    validate_candidate_concepts,
)
from vitruvius.spatial.walker import SpatialCandidate


def _make_candidate(src_concept: str, tgt_concept: str) -> SpatialCandidate:
    return SpatialCandidate(
        spatial_context_id="spatial-test-01",
        generated_at_utc="2026-04-15T09:00:00Z",
        source_instance="instance-a",
        predicate="spatial_clearance",
        target_instance="instance-b",
        value=1.1,
        unit="meters",
        source_concept_id=src_concept,
        target_concept_id=tgt_concept,
        source_file="a.json",
    )


def _write_concept(tmp_path: Path, concept_id: str) -> None:
    concepts_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    slug = concept_id.removeprefix("concept-")
    (concepts_dir / f"{slug}.md").write_text(
        f"---\nid: {concept_id}\npage_type: concept\ncanonical_status: enriched\n"
        f"last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n\n# {slug}\n",
        encoding="utf-8",
    )


def test_mapper_accepts_valid_pair(tmp_path: Path) -> None:
    _write_concept(tmp_path, "concept-means-of-egress")
    _write_concept(tmp_path, "concept-doors-and-exits")
    issues = validate_candidate_concepts(
        [_make_candidate("concept-means-of-egress", "concept-doors-and-exits")],
        canonical_root=tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
    )
    assert issues == []


def test_mapper_flags_missing_concept(tmp_path: Path) -> None:
    _write_concept(tmp_path, "concept-means-of-egress")
    issues = validate_candidate_concepts(
        [_make_candidate("concept-means-of-egress", "concept-nonexistent")],
        canonical_root=tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
    )
    assert len(issues) == 1
    assert issues[0].code == "missing_concept"
    assert "concept-nonexistent" in issues[0].message


def test_mapper_flags_unmapped_instance(tmp_path: Path) -> None:
    issues = validate_candidate_concepts(
        [_make_candidate(None, "concept-doors-and-exits")],
        canonical_root=tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
    )
    assert any(issue.code == "unmapped_instance" for issue in issues)


def test_mapper_skips_placeholder_concepts(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    (concepts_dir / "means-of-egress.md").write_text(
        "---\nid: concept-means-of-egress\npage_type: concept\n"
        "canonical_status: placeholder\nlast_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    _write_concept(tmp_path, "concept-doors-and-exits")
    issues = validate_candidate_concepts(
        [_make_candidate("concept-means-of-egress", "concept-doors-and-exits")],
        canonical_root=tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
    )
    assert any(issue.code == "placeholder_concept" for issue in issues)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_concept_mapper.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement the mapper**

Create `scripts/vitruvius/spatial/concept_mapper.py`:

```python
"""Stream L.4 — cross-reference spatial candidates with canonical concepts.

The mapper does NOT resolve unmapped instances — that's the daemon's job
upstream. It only verifies that every referenced concept ID resolves to
an existing, non-placeholder concept file.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from .walker import SpatialCandidate


@dataclass(frozen=True)
class MappingIssue:
    code: str
    spatial_context_id: str
    instance_id: str
    concept_id: str | None
    message: str


def _load_concept_status(concepts_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not concepts_dir.exists():
        return out
    for path in concepts_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[3:end].strip()) or {}
        except yaml.YAMLError:
            continue
        cid = fm.get("id")
        status = fm.get("canonical_status") or fm.get("concept_status") or "unknown"
        if isinstance(cid, str):
            out[cid] = str(status)
    return out


def _check_side(
    candidate: SpatialCandidate,
    side: str,
    instance_id: str,
    concept_id: str | None,
    status_by_id: dict[str, str],
) -> list[MappingIssue]:
    issues: list[MappingIssue] = []
    if concept_id is None:
        issues.append(
            MappingIssue(
                code="unmapped_instance",
                spatial_context_id=candidate.spatial_context_id,
                instance_id=instance_id,
                concept_id=None,
                message=f"{side} instance {instance_id!r} has no canonical_concept_id mapping",
            )
        )
        return issues
    if concept_id not in status_by_id:
        issues.append(
            MappingIssue(
                code="missing_concept",
                spatial_context_id=candidate.spatial_context_id,
                instance_id=instance_id,
                concept_id=concept_id,
                message=f"{side} concept {concept_id!r} not found in canonical layer",
            )
        )
        return issues
    if status_by_id[concept_id] == "placeholder":
        issues.append(
            MappingIssue(
                code="placeholder_concept",
                spatial_context_id=candidate.spatial_context_id,
                instance_id=instance_id,
                concept_id=concept_id,
                message=f"{side} concept {concept_id!r} is a placeholder — enrich before spatial evaluation",
            )
        )
    return issues


def validate_candidate_concepts(
    candidates: Iterable[SpatialCandidate],
    *,
    canonical_root: Path,
) -> list[MappingIssue]:
    status_by_id = _load_concept_status(canonical_root / "concepts")
    issues: list[MappingIssue] = []
    for candidate in candidates:
        issues.extend(
            _check_side(
                candidate, "source", candidate.source_instance, candidate.source_concept_id, status_by_id
            )
        )
        issues.extend(
            _check_side(
                candidate, "target", candidate.target_instance, candidate.target_concept_id, status_by_id
            )
        )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_concept_mapper.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/concept_mapper.py scripts/tests/test_spatial_concept_mapper.py
git commit -m "feat(spatial): Stream L.4 concept mapper — validate candidates vs canonical layer"
```

---

### Task L.5: Z3 Constraint Solver — Base Evaluator

**Files:**
- Create: `scripts/vitruvius/spatial/constraint_solver.py`
- Test: `scripts/tests/test_spatial_constraint_solver.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_constraint_solver.py
"""Stream L.5 — Z3 constraint evaluator (base operators)."""
from __future__ import annotations

import pytest

z3 = pytest.importorskip("z3")  # skip the entire file if z3-solver is not installed

from vitruvius.spatial.constraint_solver import (
    ConstraintEvaluation,
    ConstraintVerdict,
    evaluate_numeric_constraint,
)


def test_gte_pass() -> None:
    result = evaluate_numeric_constraint(
        actual=1.1,
        operator=">=",
        required=1.0,
    )
    assert isinstance(result, ConstraintEvaluation)
    assert result.verdict == ConstraintVerdict.SATISFIED


def test_gte_fail() -> None:
    result = evaluate_numeric_constraint(
        actual=0.9,
        operator=">=",
        required=1.0,
    )
    assert result.verdict == ConstraintVerdict.VIOLATED


def test_lte_pass() -> None:
    result = evaluate_numeric_constraint(actual=0.5, operator="<=", required=1.0)
    assert result.verdict == ConstraintVerdict.SATISFIED


def test_eq_pass() -> None:
    result = evaluate_numeric_constraint(actual=1.0, operator="==", required=1.0)
    assert result.verdict == ConstraintVerdict.SATISFIED


def test_eq_fail() -> None:
    result = evaluate_numeric_constraint(actual=1.01, operator="==", required=1.0)
    assert result.verdict == ConstraintVerdict.VIOLATED


def test_missing_actual_is_indeterminate() -> None:
    result = evaluate_numeric_constraint(actual=None, operator=">=", required=1.0)
    assert result.verdict == ConstraintVerdict.INDETERMINATE
    assert "actual" in result.reason.lower()


def test_unknown_operator_is_indeterminate() -> None:
    result = evaluate_numeric_constraint(actual=1.0, operator="~=", required=1.0)
    assert result.verdict == ConstraintVerdict.INDETERMINATE
    assert "operator" in result.reason.lower()


def test_evaluation_includes_operator_and_values() -> None:
    result = evaluate_numeric_constraint(actual=1.1, operator=">=", required=1.0)
    assert result.operator == ">="
    assert result.actual == 1.1
    assert result.required == 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_constraint_solver.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.spatial.constraint_solver'` (skipped if z3-solver is not installed — in which case install it via `pip install z3-solver`).

- [ ] **Step 3: Implement the evaluator**

Create `scripts/vitruvius/spatial/constraint_solver.py`:

```python
"""Stream L.5 — Z3 SMT evaluator for numeric spatial constraints.

The module imports z3 lazily. If z3-solver is not installed, calling
evaluate_numeric_constraint returns ConstraintVerdict.INDETERMINATE with a
reason that explains the missing dependency, rather than crashing.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ConstraintVerdict(str, Enum):
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True)
class ConstraintEvaluation:
    verdict: ConstraintVerdict
    operator: str
    actual: float | None
    required: float | None
    reason: str


_KNOWN_OPERATORS = frozenset({">=", "<=", "==", ">", "<"})


def _try_import_z3():
    try:
        import z3  # type: ignore
        return z3
    except ImportError:
        return None


def evaluate_numeric_constraint(
    *,
    actual: float | None,
    operator: str,
    required: float | None,
) -> ConstraintEvaluation:
    if actual is None:
        return ConstraintEvaluation(
            verdict=ConstraintVerdict.INDETERMINATE,
            operator=operator,
            actual=None,
            required=required,
            reason="missing actual measurement",
        )
    if required is None:
        return ConstraintEvaluation(
            verdict=ConstraintVerdict.INDETERMINATE,
            operator=operator,
            actual=actual,
            required=None,
            reason="missing required threshold",
        )
    if operator not in _KNOWN_OPERATORS:
        return ConstraintEvaluation(
            verdict=ConstraintVerdict.INDETERMINATE,
            operator=operator,
            actual=actual,
            required=required,
            reason=f"unknown operator {operator!r}",
        )

    z3 = _try_import_z3()
    if z3 is None:
        return ConstraintEvaluation(
            verdict=ConstraintVerdict.INDETERMINATE,
            operator=operator,
            actual=actual,
            required=required,
            reason="z3-solver not installed; feature disabled",
        )

    s = z3.Solver()
    actual_var = z3.Real("actual_val")
    required_var = z3.Real("required_val")
    s.add(actual_var == actual)
    s.add(required_var == required)
    if operator == ">=":
        s.add(actual_var >= required_var)
    elif operator == "<=":
        s.add(actual_var <= required_var)
    elif operator == "==":
        s.add(actual_var == required_var)
    elif operator == ">":
        s.add(actual_var > required_var)
    elif operator == "<":
        s.add(actual_var < required_var)

    sat_result = s.check()
    if sat_result == z3.sat:
        return ConstraintEvaluation(
            verdict=ConstraintVerdict.SATISFIED,
            operator=operator,
            actual=float(actual),
            required=float(required),
            reason="Z3 SAT",
        )
    return ConstraintEvaluation(
        verdict=ConstraintVerdict.VIOLATED,
        operator=operator,
        actual=float(actual),
        required=float(required),
        reason="Z3 UNSAT",
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_constraint_solver.py -v`

Expected: 8 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/constraint_solver.py scripts/tests/test_spatial_constraint_solver.py
git commit -m "feat(spatial): Stream L.5 Z3 evaluator — base numeric operators"
```

---

### Task L.6: Z3 Evaluator — Evaluation Run Orchestrator

**Files:**
- Modify: `scripts/vitruvius/spatial/constraint_solver.py` (append run_spatial_evaluation)
- Modify: `scripts/tests/test_spatial_constraint_solver.py` (append orchestrator tests)

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_spatial_constraint_solver.py`:

```python
from pathlib import Path

from vitruvius.spatial.constraint_solver import (
    SpatialEvaluationReport,
    run_spatial_evaluation,
)
from vitruvius.spatial.walker import SpatialCandidate


def _candidate(predicate: str, value: float | None) -> SpatialCandidate:
    return SpatialCandidate(
        spatial_context_id="spatial-test-01",
        generated_at_utc="2026-04-15T09:00:00Z",
        source_instance="instance-corridor-01",
        predicate=predicate,
        target_instance="instance-door-01",
        value=value,
        unit="meters",
        source_concept_id="concept-means-of-egress",
        target_concept_id="concept-doors-and-exits",
        source_file="fixture.json",
    )


def test_run_evaluation_with_passing_clearance(tmp_path: Path) -> None:
    rules = {
        "concept-means-of-egress__spatial_clearance__concept-doors-and-exits": {
            "operator": ">=",
            "required": 1.0,
        }
    }
    report = run_spatial_evaluation(
        candidates=[_candidate("spatial_clearance", 1.1)],
        rule_lookup=rules,
    )
    assert isinstance(report, SpatialEvaluationReport)
    assert report.pass_count == 1
    assert report.fail_count == 0
    assert report.indeterminate_count == 0


def test_run_evaluation_with_failing_clearance() -> None:
    rules = {
        "concept-means-of-egress__spatial_clearance__concept-doors-and-exits": {
            "operator": ">=",
            "required": 1.0,
        }
    }
    report = run_spatial_evaluation(
        candidates=[_candidate("spatial_clearance", 0.9)],
        rule_lookup=rules,
    )
    assert report.fail_count == 1
    assert report.results[0].verdict == ConstraintVerdict.VIOLATED


def test_run_evaluation_with_no_matching_rule_is_indeterminate() -> None:
    report = run_spatial_evaluation(
        candidates=[_candidate("spatial_clearance", 1.1)],
        rule_lookup={},
    )
    assert report.indeterminate_count == 1
    assert "rule" in report.results[0].reason.lower()


def test_run_evaluation_preserves_candidate_order() -> None:
    rules = {
        "concept-means-of-egress__spatial_clearance__concept-doors-and-exits": {
            "operator": ">=",
            "required": 1.0,
        }
    }
    report = run_spatial_evaluation(
        candidates=[
            _candidate("spatial_clearance", 1.1),
            _candidate("spatial_clearance", 0.5),
        ],
        rule_lookup=rules,
    )
    assert report.results[0].verdict == ConstraintVerdict.SATISFIED
    assert report.results[1].verdict == ConstraintVerdict.VIOLATED
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_constraint_solver.py -v`

Expected: FAIL with `ImportError: cannot import name 'run_spatial_evaluation'`.

- [ ] **Step 3: Implement the orchestrator**

Append to `scripts/vitruvius/spatial/constraint_solver.py`:

```python
from dataclasses import field
from typing import Mapping

from .walker import SpatialCandidate


def _rule_key(source_concept: str, predicate: str, target_concept: str) -> str:
    return f"{source_concept}__{predicate}__{target_concept}"


@dataclass(frozen=True)
class CandidateResult:
    spatial_context_id: str
    source_instance: str
    predicate: str
    target_instance: str
    verdict: ConstraintVerdict
    operator: str
    actual: float | None
    required: float | None
    reason: str


@dataclass(frozen=True)
class SpatialEvaluationReport:
    results: tuple[CandidateResult, ...]
    pass_count: int
    fail_count: int
    indeterminate_count: int


def run_spatial_evaluation(
    *,
    candidates: list[SpatialCandidate],
    rule_lookup: Mapping[str, Mapping[str, object]],
) -> SpatialEvaluationReport:
    results: list[CandidateResult] = []
    for candidate in candidates:
        if candidate.source_concept_id is None or candidate.target_concept_id is None:
            results.append(
                CandidateResult(
                    spatial_context_id=candidate.spatial_context_id,
                    source_instance=candidate.source_instance,
                    predicate=candidate.predicate,
                    target_instance=candidate.target_instance,
                    verdict=ConstraintVerdict.INDETERMINATE,
                    operator="",
                    actual=candidate.value,
                    required=None,
                    reason="unmapped concept on one or both sides",
                )
            )
            continue
        key = _rule_key(candidate.source_concept_id, candidate.predicate, candidate.target_concept_id)
        rule = rule_lookup.get(key)
        if rule is None:
            results.append(
                CandidateResult(
                    spatial_context_id=candidate.spatial_context_id,
                    source_instance=candidate.source_instance,
                    predicate=candidate.predicate,
                    target_instance=candidate.target_instance,
                    verdict=ConstraintVerdict.INDETERMINATE,
                    operator="",
                    actual=candidate.value,
                    required=None,
                    reason=f"no rule found for key {key!r}",
                )
            )
            continue
        evaluation = evaluate_numeric_constraint(
            actual=candidate.value,
            operator=str(rule.get("operator", "")),
            required=rule.get("required"),  # type: ignore[arg-type]
        )
        results.append(
            CandidateResult(
                spatial_context_id=candidate.spatial_context_id,
                source_instance=candidate.source_instance,
                predicate=candidate.predicate,
                target_instance=candidate.target_instance,
                verdict=evaluation.verdict,
                operator=evaluation.operator,
                actual=evaluation.actual,
                required=evaluation.required,
                reason=evaluation.reason,
            )
        )

    return SpatialEvaluationReport(
        results=tuple(results),
        pass_count=sum(1 for r in results if r.verdict == ConstraintVerdict.SATISFIED),
        fail_count=sum(1 for r in results if r.verdict == ConstraintVerdict.VIOLATED),
        indeterminate_count=sum(1 for r in results if r.verdict == ConstraintVerdict.INDETERMINATE),
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_constraint_solver.py -v`

Expected: 12 PASSED (8 original + 4 new).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/constraint_solver.py scripts/tests/test_spatial_constraint_solver.py
git commit -m "feat(spatial): Stream L.6 orchestrator — run_spatial_evaluation + report"
```

---

### Task L.7: Spatial CLI Commands (`ingest-spatial`, `evaluate-spatial`)

**Files:**
- Create: `scripts/vitruvius/spatial/cli.py`
- Modify: `scripts/pipeline_cli.py` (register commands, lazy imports)
- Test: `scripts/tests/test_spatial_cli.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_spatial_cli.py
"""Stream L.7 — CLI integration for spatial ingestion + evaluation."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

z3 = pytest.importorskip("z3")

CLI = Path(__file__).resolve().parent.parent / "pipeline_cli.py"


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": "scripts"}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _seed_tree(root: Path) -> None:
    spatial = root / "001B_Spatial-Source-Layer"
    spatial.mkdir(parents=True)
    payload = {
        "schema_version": "1.0.0",
        "spatial_context_id": "spatial-test-01",
        "generated_at_utc": "2026-04-15T09:00:00Z",
        "instances": [
            {"instance_id": "instance-corridor", "canonical_concept_id": "concept-means-of-egress"},
            {"instance_id": "instance-door", "canonical_concept_id": "concept-doors-and-exits"},
        ],
        "spatial_edges": [
            {
                "source_instance": "instance-corridor",
                "predicate": "spatial_clearance",
                "target_instance": "instance-door",
                "value": 1.1,
                "unit": "meters",
            }
        ],
    }
    (spatial / "sample.json").write_text(json.dumps(payload), encoding="utf-8")
    # Seed canonical concepts so the mapper passes
    concepts = root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    concepts.mkdir(parents=True)
    for slug, cid in [
        ("means-of-egress", "concept-means-of-egress"),
        ("doors-and-exits", "concept-doors-and-exits"),
    ]:
        (concepts / f"{slug}.md").write_text(
            f"---\nid: {cid}\npage_type: concept\ncanonical_status: enriched\n"
            f"last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n\n# {slug}\n",
            encoding="utf-8",
        )
    # Seed rules file
    rules_path = root / "005_Operational-Intelligence-Layer" / "spatial" / "rules.json"
    rules_path.parent.mkdir(parents=True)
    rules_path.write_text(
        json.dumps({
            "concept-means-of-egress__spatial_clearance__concept-doors-and-exits": {
                "operator": ">=",
                "required": 1.0,
            }
        }),
        encoding="utf-8",
    )


def test_ingest_spatial_reports_candidate_count(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    result = _run_cli(["ingest-spatial"], cwd=tmp_path)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out = json.loads(result.stdout)
    assert out["candidate_count"] == 1
    assert out["context_ids"] == ["spatial-test-01"]


def test_ingest_spatial_writes_candidate_file(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    result = _run_cli(["ingest-spatial"], cwd=tmp_path)
    assert result.returncode == 0
    out_path = tmp_path / "005_Operational-Intelligence-Layer" / "spatial" / "latest_spatial_candidates.json"
    assert out_path.exists()
    data = json.loads(out_path.read_text())
    assert len(data["candidates"]) == 1


def test_evaluate_spatial_returns_pass_count(tmp_path: Path) -> None:
    _seed_tree(tmp_path)
    _run_cli(["ingest-spatial"], cwd=tmp_path)
    result = _run_cli(
        ["evaluate-spatial", "--rules", "005_Operational-Intelligence-Layer/spatial/rules.json"],
        cwd=tmp_path,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out = json.loads(result.stdout)
    assert out["pass_count"] == 1
    assert out["fail_count"] == 0


def test_spatial_cli_is_lazy() -> None:
    """CLI must not eager-import spatial modules."""
    env = {**os.environ, "PYTHONPATH": "scripts"}
    script = (
        "import sys;"
        "import importlib.util;"
        f"spec = importlib.util.spec_from_file_location('pipeline_cli', r'{CLI}');"
        "mod = importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(mod);"
        "forbidden = {'vitruvius.spatial.walker', 'vitruvius.spatial.concept_mapper', "
        "'vitruvius.spatial.constraint_solver', 'vitruvius.spatial.cli'};"
        "leaked = forbidden & set(sys.modules.keys());"
        "print('LEAKED:' + ','.join(sorted(leaked)) if leaked else 'CLEAN');"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=str(CLI.resolve().parent.parent),
        env=env,
    )
    assert result.returncode == 0
    assert "CLEAN" in result.stdout, f"CLI eagerly imported spatial: {result.stdout}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_cli.py -v`

Expected: FAIL — CLI commands not yet registered.

- [ ] **Step 3: Implement `scripts/vitruvius/spatial/cli.py`**

```python
"""Stream L.7 — CLI handlers for spatial ingestion and evaluation."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .concept_mapper import validate_candidate_concepts
from .constraint_solver import run_spatial_evaluation
from .walker import SpatialCandidate, walk_spatial_layer


_SPATIAL_INPUT_RELPATH = Path("001B_Spatial-Source-Layer")
_SPATIAL_OUTPUT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "spatial" / "latest_spatial_candidates.json"
)
_EVAL_OUTPUT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "spatial" / "latest_spatial_evaluation.json"
)
_CANONICAL_SHARED_RELPATH = Path("003_Canonical-Knowledge-Layer") / "shared"


def _repo_root() -> Path:
    return Path.cwd()


def _serialize_candidate(c: SpatialCandidate) -> dict:
    return asdict(c)


def run_ingest_spatial() -> int:
    repo = _repo_root()
    input_dir = repo / _SPATIAL_INPUT_RELPATH
    candidates = walk_spatial_layer(input_dir)
    mapping_issues = validate_candidate_concepts(
        candidates,
        canonical_root=repo / _CANONICAL_SHARED_RELPATH,
    )

    out_payload = {
        "candidate_count": len(candidates),
        "context_ids": sorted({c.spatial_context_id for c in candidates}),
        "mapping_issue_count": len(mapping_issues),
        "candidates": [_serialize_candidate(c) for c in candidates],
        "mapping_issues": [asdict(issue) for issue in mapping_issues],
    }
    out_path = repo / _SPATIAL_OUTPUT_RELPATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(out_payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "candidate_count": len(candidates),
        "context_ids": sorted({c.spatial_context_id for c in candidates}),
        "mapping_issue_count": len(mapping_issues),
        "output_path": str(_SPATIAL_OUTPUT_RELPATH),
    }, indent=2))
    return 0 if not mapping_issues else 1


def run_evaluate_spatial(*, rules_path: str) -> int:
    repo = _repo_root()
    candidates_path = repo / _SPATIAL_OUTPUT_RELPATH
    if not candidates_path.exists():
        print(json.dumps({
            "error": "no candidates file; run ingest-spatial first",
            "expected_path": str(_SPATIAL_OUTPUT_RELPATH),
        }, indent=2))
        return 2

    rules_file = repo / rules_path
    if not rules_file.exists():
        print(json.dumps({"error": f"rules file not found: {rules_path}"}, indent=2))
        return 2

    candidates_data = json.loads(candidates_path.read_text(encoding="utf-8"))
    candidates = [
        SpatialCandidate(**entry) for entry in candidates_data.get("candidates", [])
    ]
    rule_lookup = json.loads(rules_file.read_text(encoding="utf-8"))
    report = run_spatial_evaluation(candidates=candidates, rule_lookup=rule_lookup)

    payload = {
        "pass_count": report.pass_count,
        "fail_count": report.fail_count,
        "indeterminate_count": report.indeterminate_count,
        "results": [asdict(r) for r in report.results],
    }

    out_path = repo / _EVAL_OUTPUT_RELPATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "pass_count": report.pass_count,
        "fail_count": report.fail_count,
        "indeterminate_count": report.indeterminate_count,
        "output_path": str(_EVAL_OUTPUT_RELPATH),
    }, indent=2))
    return 0 if report.fail_count == 0 else 1
```

- [ ] **Step 4: Register the commands in `scripts/pipeline_cli.py`**

In `build_parser()`, after the `export-graph-snapshot` parser:

```python
    ingest_spatial_parser = subparsers.add_parser("ingest-spatial")

    evaluate_spatial_parser = subparsers.add_parser("evaluate-spatial")
    evaluate_spatial_parser.add_argument(
        "--rules", dest="rules_path", required=True,
        help="Path to the rules JSON file (relative to repo root)",
    )
```

In `main()`, after the `export-graph-snapshot` dispatch:

```python
    if args.command == "ingest-spatial":
        from vitruvius.spatial.cli import run_ingest_spatial
        return run_ingest_spatial()

    if args.command == "evaluate-spatial":
        from vitruvius.spatial.cli import run_evaluate_spatial
        return run_evaluate_spatial(rules_path=args.rules_path)
```

- [ ] **Step 5: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_cli.py -v`

Expected: 4 PASSED.

- [ ] **Step 6: Commit**

```bash
git add scripts/vitruvius/spatial/cli.py scripts/pipeline_cli.py scripts/tests/test_spatial_cli.py
git commit -m "feat(spatial): Stream L.7 CLI — ingest-spatial + evaluate-spatial commands"
```

---

### Task L.8: Backward-Compat Regression Test

**Files:**
- Create: `scripts/tests/test_3d_upgrade_backcompat.py`
- Create: `scripts/tests/fixtures/spatial/expected_frozen_snapshot.json`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_3d_upgrade_backcompat.py
"""Locks the non-breaking guarantee: with every 3D feature flag OFF,
the Phase 8 graph builder must produce the same snapshot as before."""
from __future__ import annotations

import json
from pathlib import Path

from vitruvius.graph.builder import build_snapshot
from vitruvius.graph.snapshot import _snapshot_to_dict

FIX = Path(__file__).resolve().parent / "fixtures" / "spatial"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_minimal_canonical_tree(root: Path) -> None:
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    _write(shared / "sources" / "pd-1096.md",
           "---\nid: law-pd-1096\ntrust_level: primary\n"
           "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n")
    _write(shared / "concepts" / "building-permit.md",
           "---\nid: concept-building-permit\n"
           "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n")
    _write(shared / "relationships" / "r.md",
           "---\nid: rel-pd-1096-governs-building-permit\n"
           "page_type: relationship\nrelationship_type: governs\n"
           "from_entity: law-pd-1096\nto_entity: concept-building-permit\n"
           "canonical_status: promoted\n---\n")


def test_flag_off_snapshot_matches_frozen_expectation(tmp_path: Path) -> None:
    _seed_minimal_canonical_tree(tmp_path)
    snapshot = build_snapshot(
        tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
        now="2026-04-15T00:00:00Z",
    )
    actual = _snapshot_to_dict(snapshot)
    expected = json.loads((FIX / "expected_frozen_snapshot.json").read_text())
    assert actual == expected, (
        "Phase 8 graph drifted. Check Stream L contract extensions "
        "are truly additive and 3D flags default OFF."
    )
```

Create `scripts/tests/fixtures/spatial/expected_frozen_snapshot.json`:

```json
{
  "edge_count": 1,
  "edges": [
    {
      "evidence_id": "rel-pd-1096-governs-building-permit",
      "from_id": "law-pd-1096",
      "status": "unverified",
      "to_id": "concept-building-permit",
      "type": "governs"
    }
  ],
  "generated_at_utc": "2026-04-15T00:00:00Z",
  "node_count": 2,
  "nodes": [
    {
      "id": "concept-building-permit",
      "last_updated_utc": "2026-04-01T00:00:00Z",
      "slug": "building-permit",
      "trust_level": "derived",
      "type": "concept"
    },
    {
      "id": "law-pd-1096",
      "last_updated_utc": "2026-04-01T00:00:00Z",
      "slug": "pd-1096",
      "trust_level": "primary",
      "type": "source"
    }
  ],
  "schema_version": "1.0.0"
}
```

- [ ] **Step 2: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_3d_upgrade_backcompat.py -v`

Expected: PASS (the fixture is the current snapshot — if it doesn't match, the regression is already present and must be fixed before proceeding).

- [ ] **Step 3: Full regression pass**

Run: `PYTHONPATH=scripts pytest scripts/tests/ -q`

Expected: all tests pass. Count should equal prior (788) + 4 (bootstrap) + 8 (schema) + 6 (walker) + 4 (mapper) + 12 (solver) + 4 (cli) + 1 (backcompat) = **827 tests**.

- [ ] **Step 4: Commit**

```bash
git add scripts/tests/test_3d_upgrade_backcompat.py scripts/tests/fixtures/spatial/expected_frozen_snapshot.json
git commit -m "test(spatial): Stream L.8 backcompat regression — Phase 8 snapshot frozen"
```

---

## 8. Stream M — IFC/OWL Ontology Mapping

### Task M.1: IFC Lookup Registry

**Files:**
- Create: `scripts/vitruvius/ontology/__init__.py`
- Create: `scripts/vitruvius/ontology/ifc_registry.py`
- Create: `scripts/vitruvius/ontology/ifc_mapping.yaml`
- Test: `scripts/tests/test_ontology_ifc_registry.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_ontology_ifc_registry.py
"""Stream M.1 — IFC concept registry loader."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.ontology.ifc_registry import (
    IfcMappingEntry,
    IfcRegistryError,
    load_ifc_registry,
    lookup_ifc_class,
)


FIX = Path(__file__).resolve().parent / "fixtures" / "ontology"


def _write_registry(tmp_path: Path, yaml_body: str) -> Path:
    path = tmp_path / "ifc_mapping.yaml"
    path.write_text(yaml_body, encoding="utf-8")
    return path


def test_load_empty_registry_returns_empty_dict(tmp_path: Path) -> None:
    path = _write_registry(tmp_path, "mappings: []\n")
    registry = load_ifc_registry(path)
    assert registry == {}


def test_load_single_entry(tmp_path: Path) -> None:
    path = _write_registry(
        tmp_path,
        "mappings:\n"
        "  - concept_id: concept-doors-and-exits\n"
        "    ifc_class: IfcDoor\n"
        "    psets:\n"
        "      - Pset_DoorCommon\n",
    )
    registry = load_ifc_registry(path)
    entry = registry["concept-doors-and-exits"]
    assert isinstance(entry, IfcMappingEntry)
    assert entry.ifc_class == "IfcDoor"
    assert entry.psets == ("Pset_DoorCommon",)


def test_lookup_ifc_class(tmp_path: Path) -> None:
    path = _write_registry(
        tmp_path,
        "mappings:\n"
        "  - concept_id: concept-doors-and-exits\n"
        "    ifc_class: IfcDoor\n",
    )
    registry = load_ifc_registry(path)
    assert lookup_ifc_class(registry, "concept-doors-and-exits") == "IfcDoor"
    assert lookup_ifc_class(registry, "concept-unknown") is None


def test_ifc_class_must_start_with_Ifc(tmp_path: Path) -> None:
    path = _write_registry(
        tmp_path,
        "mappings:\n"
        "  - concept_id: concept-x\n"
        "    ifc_class: Door\n",
    )
    with pytest.raises(IfcRegistryError, match="IfcClass"):
        load_ifc_registry(path)


def test_concept_id_must_start_with_concept(tmp_path: Path) -> None:
    path = _write_registry(
        tmp_path,
        "mappings:\n"
        "  - concept_id: door\n"
        "    ifc_class: IfcDoor\n",
    )
    with pytest.raises(IfcRegistryError, match="concept-"):
        load_ifc_registry(path)


def test_duplicate_concept_id_rejected(tmp_path: Path) -> None:
    path = _write_registry(
        tmp_path,
        "mappings:\n"
        "  - concept_id: concept-door\n"
        "    ifc_class: IfcDoor\n"
        "  - concept_id: concept-door\n"
        "    ifc_class: IfcDoor\n",
    )
    with pytest.raises(IfcRegistryError, match="duplicate"):
        load_ifc_registry(path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_ifc_registry.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement registry loader**

Create `scripts/vitruvius/ontology/__init__.py`:
```python
"""IFC/OWL ontology mapping (Stream M)."""
```

Create `scripts/vitruvius/ontology/ifc_registry.py`:
```python
"""Stream M.1 — static concept → IfcClass + Psets registry loader."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml


class IfcRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class IfcMappingEntry:
    concept_id: str
    ifc_class: str
    psets: tuple[str, ...]


def load_ifc_registry(yaml_path: Path) -> dict[str, IfcMappingEntry]:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    mappings = raw.get("mappings", [])
    out: dict[str, IfcMappingEntry] = {}
    for idx, row in enumerate(mappings):
        cid = row.get("concept_id")
        ifc = row.get("ifc_class")
        psets = tuple(row.get("psets", []) or ())
        if not isinstance(cid, str) or not cid.startswith("concept-"):
            raise IfcRegistryError(
                f"mappings[{idx}].concept_id must start with 'concept-' (got {cid!r})"
            )
        if not isinstance(ifc, str) or not ifc.startswith("Ifc"):
            raise IfcRegistryError(
                f"mappings[{idx}].ifc_class must be a valid IfcClass name (got {ifc!r})"
            )
        if cid in out:
            raise IfcRegistryError(f"duplicate concept_id {cid!r}")
        out[cid] = IfcMappingEntry(concept_id=cid, ifc_class=ifc, psets=psets)
    return out


def lookup_ifc_class(
    registry: Mapping[str, IfcMappingEntry], concept_id: str
) -> str | None:
    entry = registry.get(concept_id)
    return entry.ifc_class if entry else None
```

Create `scripts/vitruvius/ontology/ifc_mapping.yaml`:
```yaml
# Stream M.1 — concept → IFC class mapping (static).
# See .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md §8 Task M.1.
mappings:
  - concept_id: concept-doors-and-exits
    ifc_class: IfcDoor
    psets:
      - Pset_DoorCommon
      - Pset_DoorFireRating
  - concept_id: concept-fire-resistive-construction
    ifc_class: IfcWall
    psets:
      - Pset_WallCommon
      - Pset_WallFireRating
  - concept_id: concept-means-of-egress
    ifc_class: IfcSpace
    psets:
      - Pset_SpaceCommon
  - concept_id: concept-building-height
    ifc_class: IfcBuilding
    psets:
      - Pset_BuildingCommon
  - concept_id: concept-floor-area
    ifc_class: IfcSpace
    psets:
      - Pset_SpaceCommon
  - concept_id: concept-setbacks
    ifc_class: IfcSite
    psets:
      - Pset_SiteCommon
  - concept_id: concept-lot-occupancy
    ifc_class: IfcSite
    psets:
      - Pset_SiteCommon
  - concept_id: concept-exit-width
    ifc_class: IfcDoor
    psets:
      - Pset_DoorCommon
  - concept_id: concept-light-and-ventilation
    ifc_class: IfcWindow
    psets:
      - Pset_WindowCommon
  - concept_id: concept-building-permit
    ifc_class: IfcProject
    psets:
      - Pset_ProjectCommon
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_ifc_registry.py -v`

Expected: 6 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ontology scripts/tests/test_ontology_ifc_registry.py
git commit -m "feat(ontology): Stream M.1 IFC concept registry + 10 initial mappings"
```

---

### Task M.2: Concept Frontmatter Optional IFC Fields (Lint-Aware)

**Files:**
- Create: `scripts/vitruvius/ontology/ifc_validator.py`
- Test: `scripts/tests/test_ontology_concept_frontmatter.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_ontology_concept_frontmatter.py
"""Stream M.2 — validate optional ifc_class / ifc_psets frontmatter on concepts."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.ontology.ifc_registry import IfcMappingEntry
from vitruvius.ontology.ifc_validator import (
    FrontmatterIfcIssue,
    validate_concept_ifc_frontmatter,
)


def _concept(tmp_path: Path, slug: str, body: str) -> Path:
    path = tmp_path / "concepts" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _registry() -> dict:
    return {
        "concept-doors-and-exits": IfcMappingEntry(
            concept_id="concept-doors-and-exits",
            ifc_class="IfcDoor",
            psets=("Pset_DoorCommon",),
        )
    }


def test_missing_optional_fields_is_ok(tmp_path: Path) -> None:
    _concept(
        tmp_path,
        "doors-and-exits",
        "---\nid: concept-doors-and-exits\npage_type: concept\n"
        "canonical_status: enriched\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
    )
    issues = validate_concept_ifc_frontmatter(tmp_path / "concepts", _registry())
    assert issues == []


def test_matching_ifc_class_is_ok(tmp_path: Path) -> None:
    _concept(
        tmp_path,
        "doors-and-exits",
        "---\nid: concept-doors-and-exits\npage_type: concept\n"
        "canonical_status: enriched\n"
        "ifc_class: IfcDoor\n"
        "ifc_psets: [Pset_DoorCommon]\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
    )
    issues = validate_concept_ifc_frontmatter(tmp_path / "concepts", _registry())
    assert issues == []


def test_mismatched_ifc_class_is_flagged(tmp_path: Path) -> None:
    _concept(
        tmp_path,
        "doors-and-exits",
        "---\nid: concept-doors-and-exits\npage_type: concept\n"
        "canonical_status: enriched\n"
        "ifc_class: IfcWall\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
    )
    issues = validate_concept_ifc_frontmatter(tmp_path / "concepts", _registry())
    assert len(issues) == 1
    assert issues[0].code == "ifc_class_mismatch"


def test_unknown_ifc_class_is_flagged(tmp_path: Path) -> None:
    _concept(
        tmp_path,
        "doors-and-exits",
        "---\nid: concept-doors-and-exits\npage_type: concept\n"
        "canonical_status: enriched\n"
        "ifc_class: NotAnIfcClass\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
    )
    issues = validate_concept_ifc_frontmatter(tmp_path / "concepts", _registry())
    assert any(i.code == "invalid_ifc_class_name" for i in issues)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_concept_frontmatter.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement validator**

Create `scripts/vitruvius/ontology/ifc_validator.py`:

```python
"""Stream M.2 — lint optional ifc_class / ifc_psets fields on concept files."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml

from .ifc_registry import IfcMappingEntry


@dataclass(frozen=True)
class FrontmatterIfcIssue:
    code: str
    concept_id: str
    message: str


def _load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        data = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def validate_concept_ifc_frontmatter(
    concepts_dir: Path,
    registry: Mapping[str, IfcMappingEntry],
) -> list[FrontmatterIfcIssue]:
    issues: list[FrontmatterIfcIssue] = []
    if not concepts_dir.exists():
        return issues
    for path in sorted(concepts_dir.glob("*.md")):
        fm = _load_frontmatter(path)
        cid = fm.get("id")
        if not isinstance(cid, str):
            continue
        declared_class = fm.get("ifc_class")
        if declared_class is None:
            continue
        if not isinstance(declared_class, str) or not declared_class.startswith("Ifc"):
            issues.append(
                FrontmatterIfcIssue(
                    code="invalid_ifc_class_name",
                    concept_id=cid,
                    message=f"ifc_class {declared_class!r} must start with 'Ifc'",
                )
            )
            continue
        entry = registry.get(cid)
        if entry is not None and entry.ifc_class != declared_class:
            issues.append(
                FrontmatterIfcIssue(
                    code="ifc_class_mismatch",
                    concept_id=cid,
                    message=(
                        f"concept {cid!r} declares ifc_class={declared_class!r} but "
                        f"registry expects {entry.ifc_class!r}"
                    ),
                )
            )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_concept_frontmatter.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ontology/ifc_validator.py scripts/tests/test_ontology_concept_frontmatter.py
git commit -m "feat(ontology): Stream M.2 concept frontmatter IFC validator"
```

---

### Task M.3: OWL/Turtle Exporter for Phase 8 Snapshot

**Files:**
- Create: `scripts/vitruvius/ontology/owl_exporter.py`
- Test: `scripts/tests/test_ontology_owl_exporter.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_ontology_owl_exporter.py
"""Stream M.3 — OWL/Turtle exporter for graph snapshot."""
from __future__ import annotations

import pytest

rdflib = pytest.importorskip("rdflib")

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.ontology.ifc_registry import IfcMappingEntry
from vitruvius.ontology.owl_exporter import export_snapshot_as_turtle


def _snapshot() -> GraphSnapshot:
    nodes = [
        GraphNode(
            id="law-pd-1096",
            type="source",
            slug="pd-1096",
            trust_level="primary",
            last_updated_utc="2026-04-01T00:00:00Z",
        ),
        GraphNode(
            id="concept-doors-and-exits",
            type="concept",
            slug="doors-and-exits",
            trust_level="derived",
            last_updated_utc="2026-04-01T00:00:00Z",
        ),
    ]
    edges = [
        GraphEdge(
            from_id="law-pd-1096",
            to_id="concept-doors-and-exits",
            type="governs",
            evidence_id="rel-pd-1096-governs-doors-and-exits",
            status="verified",
        )
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-15T00:00:00Z",
        node_count=2,
        edge_count=1,
        nodes=nodes,
        edges=edges,
    )


def _registry() -> dict:
    return {
        "concept-doors-and-exits": IfcMappingEntry(
            concept_id="concept-doors-and-exits",
            ifc_class="IfcDoor",
            psets=("Pset_DoorCommon",),
        )
    }


def test_exports_turtle_with_triples() -> None:
    turtle = export_snapshot_as_turtle(_snapshot(), ifc_registry=_registry())
    assert "@prefix" in turtle
    assert "concept-doors-and-exits" in turtle
    assert "IfcDoor" in turtle
    assert "governs" in turtle


def test_turtle_parses_via_rdflib() -> None:
    turtle = export_snapshot_as_turtle(_snapshot(), ifc_registry=_registry())
    g = rdflib.Graph()
    g.parse(data=turtle, format="turtle")
    assert len(g) > 0


def test_turtle_contains_ifc_class_assertion() -> None:
    turtle = export_snapshot_as_turtle(_snapshot(), ifc_registry=_registry())
    g = rdflib.Graph()
    g.parse(data=turtle, format="turtle")
    query_result = list(g.query(
        "SELECT ?c WHERE { ?c a <https://vitruvius.local/ontology/IfcDoor> }"
    ))
    assert len(query_result) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_owl_exporter.py -v`

Expected: FAIL.

- [ ] **Step 3: Implement the exporter**

Create `scripts/vitruvius/ontology/owl_exporter.py`:

```python
"""Stream M.3 — export Phase 8 snapshot as OWL/Turtle with IFC class assertions."""
from __future__ import annotations

from typing import Mapping

from ..graph.contract import GraphSnapshot
from .ifc_registry import IfcMappingEntry


_BASE = "https://vitruvius.local/ontology/"
_CONCEPT_BASE = "https://vitruvius.local/concept/"
_REL_BASE = "https://vitruvius.local/rel/"


def _sanitize(token: str) -> str:
    return token.replace(" ", "_")


def export_snapshot_as_turtle(
    snapshot: GraphSnapshot,
    *,
    ifc_registry: Mapping[str, IfcMappingEntry] | None = None,
) -> str:
    registry = ifc_registry or {}
    lines: list[str] = []
    lines.append(f"@prefix vit: <{_BASE}> .")
    lines.append(f"@prefix vitc: <{_CONCEPT_BASE}> .")
    lines.append(f"@prefix vitr: <{_REL_BASE}> .")
    lines.append("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
    lines.append("@prefix owl: <http://www.w3.org/2002/07/owl#> .")
    lines.append("")

    for node in snapshot.nodes:
        subject = f"vitc:{_sanitize(node.id)}"
        lines.append(f"{subject} a vit:{_sanitize(node.type.title())} ;")
        lines.append(f'    rdfs:label "{node.slug}" ;')
        if node.type == "concept" and node.id in registry:
            entry = registry[node.id]
            lines.append(f"    a vit:{entry.ifc_class} ;")
            for pset in entry.psets:
                lines.append(f'    vit:hasPropertySet "{pset}" ;')
        lines.append(f'    vit:trustLevel "{node.trust_level}" .')
        lines.append("")

    for edge in snapshot.edges:
        subject = f"vitc:{_sanitize(edge.from_id)}"
        obj = f"vitc:{_sanitize(edge.to_id)}"
        predicate = f"vit:{_sanitize(edge.type)}"
        lines.append(f"{subject} {predicate} {obj} .")

    return "\n".join(lines) + "\n"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_owl_exporter.py -v`

Expected: 3 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ontology/owl_exporter.py scripts/tests/test_ontology_owl_exporter.py
git commit -m "feat(ontology): Stream M.3 OWL/Turtle exporter for Phase 8 snapshot"
```

---

### Task M.4: Register `export-graph-owl` CLI Command

**Files:**
- Modify: `scripts/vitruvius/ontology/__init__.py` (export run_export_graph_owl)
- Create: `scripts/vitruvius/ontology/cli.py`
- Modify: `scripts/pipeline_cli.py` (register command, lazy import)
- Modify: `scripts/tests/test_spatial_cli.py` (append CLI test)

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_spatial_cli.py`:

```python
def test_export_graph_owl_writes_turtle(tmp_path: Path) -> None:
    # Seed minimal canonical tree + build graph first
    shared = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    (shared / "sources").mkdir(parents=True)
    (shared / "concepts").mkdir(parents=True)
    (shared / "relationships").mkdir(parents=True)
    (shared / "sources" / "pd-1096.md").write_text(
        "---\nid: law-pd-1096\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    (shared / "concepts" / "doors-and-exits.md").write_text(
        "---\nid: concept-doors-and-exits\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    (shared / "relationships" / "r.md").write_text(
        "---\nid: rel-pd-1096-governs-doors-and-exits\n"
        "page_type: relationship\nrelationship_type: governs\n"
        "from_entity: law-pd-1096\nto_entity: concept-doors-and-exits\n"
        "canonical_status: promoted\n---\n",
        encoding="utf-8",
    )
    build_result = _run_cli(["build-graph"], cwd=tmp_path)
    assert build_result.returncode == 0

    result = _run_cli(["export-graph-owl"], cwd=tmp_path)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "@prefix" in result.stdout
    assert "concept-doors-and-exits" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_cli.py::test_export_graph_owl_writes_turtle -v`

Expected: FAIL (command not registered).

- [ ] **Step 3: Implement the CLI shim**

Create `scripts/vitruvius/ontology/cli.py`:
```python
"""Stream M.4 — export-graph-owl CLI handler."""
from __future__ import annotations

import json
from pathlib import Path

from ..graph.cli import _SNAPSHOT_RELPATH
from ..graph.snapshot import read_snapshot
from .ifc_registry import load_ifc_registry
from .owl_exporter import export_snapshot_as_turtle


_REGISTRY_RELPATH = Path("scripts") / "vitruvius" / "ontology" / "ifc_mapping.yaml"


def run_export_graph_owl() -> int:
    repo = Path.cwd()
    snapshot_path = repo / _SNAPSHOT_RELPATH
    if not snapshot_path.exists():
        print(json.dumps({
            "error": "no snapshot found — run build-graph first",
            "expected_path": str(_SNAPSHOT_RELPATH),
        }, indent=2))
        return 2
    snapshot = read_snapshot(snapshot_path)
    registry_path = repo / _REGISTRY_RELPATH
    registry = load_ifc_registry(registry_path) if registry_path.exists() else {}
    turtle = export_snapshot_as_turtle(snapshot, ifc_registry=registry)
    print(turtle, end="")
    return 0
```

Modify `scripts/pipeline_cli.py` — add parser entry and dispatch:
```python
    subparsers.add_parser("export-graph-owl")
```
```python
    if args.command == "export-graph-owl":
        from vitruvius.ontology.cli import run_export_graph_owl
        return run_export_graph_owl()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_spatial_cli.py::test_export_graph_owl_writes_turtle -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ontology/cli.py scripts/pipeline_cli.py scripts/tests/test_spatial_cli.py
git commit -m "feat(ontology): Stream M.4 export-graph-owl CLI command"
```

---

## 9. Stream N — Decoupled Spatial Daemon (TypeScript / Node.js)

> **Architectural note.** The daemon lives at repo root under `spatial-daemon/`
> with its own `package.json`, `tsconfig.json`, and test runner. It never
> shares a Python process with Vitruvius. Communication is **file-based only**:
> the daemon writes JSON files into `001B_Spatial-Source-Layer/`; the Python
> pipeline reads them via Stream L.3 walker. This preserves principle P1
> (filesystem is the database) and the idempotent-stage guarantee.

### Task N.1: Daemon Project Scaffold

**Files:**
- Create: `spatial-daemon/package.json`
- Create: `spatial-daemon/tsconfig.json`
- Create: `spatial-daemon/vitest.config.ts`
- Create: `spatial-daemon/README.md`
- Create: `spatial-daemon/src/types.ts`
- Create: `spatial-daemon/.gitignore`
- Test: `spatial-daemon/tests/smoke.test.ts`

- [ ] **Step 1: Write the failing test**

Create `spatial-daemon/tests/smoke.test.ts`:
```typescript
import { describe, expect, it } from "vitest";
import type { SpatialContract, Instance, SpatialEdge } from "../src/types";

describe("types scaffold", () => {
  it("exposes the SpatialContract interface shape", () => {
    const contract: SpatialContract = {
      schema_version: "1.0.0",
      spatial_context_id: "spatial-test-01",
      generated_at_utc: "2026-04-15T09:00:00Z",
      instances: [],
      spatial_edges: [],
    };
    expect(contract.schema_version).toBe("1.0.0");
  });

  it("enforces Instance id prefix via comment convention", () => {
    const i: Instance = {
      instance_id: "instance-door-01",
      canonical_concept_id: "concept-doors-and-exits",
    };
    expect(i.instance_id.startsWith("instance-")).toBe(true);
  });

  it("exposes SpatialEdge with predicate union", () => {
    const e: SpatialEdge = {
      source_instance: "instance-a",
      predicate: "spatial_intersects",
      target_instance: "instance-b",
    };
    expect(e.predicate).toBe("spatial_intersects");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd spatial-daemon && npx vitest run tests/smoke.test.ts
```

Expected: FAIL — package.json and src/types.ts missing.

- [ ] **Step 3: Create the project scaffold**

Create `spatial-daemon/package.json`:
```json
{
  "name": "vitruvius-spatial-daemon",
  "version": "0.1.0",
  "description": "Headless spatial translator for Vitruvius — consumes CAD exports, emits JSON manifests into 001B_Spatial-Source-Layer.",
  "type": "module",
  "main": "dist/cli.js",
  "bin": {
    "vitruvius-spatial": "dist/cli.js"
  },
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "test:watch": "vitest",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "three": "^0.164.0"
  },
  "devDependencies": {
    "@types/node": "^20.12.0",
    "@types/three": "^0.164.0",
    "typescript": "^5.4.0",
    "vitest": "^1.4.0"
  },
  "engines": {
    "node": ">=20"
  }
}
```

Create `spatial-daemon/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"]
}
```

Create `spatial-daemon/vitest.config.ts`:
```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: false,
    environment: "node",
    include: ["tests/**/*.test.ts"],
  },
});
```

Create `spatial-daemon/.gitignore`:
```text
node_modules/
dist/
*.log
.vitest-cache/
```

Create `spatial-daemon/README.md`:
```markdown
# Vitruvius Spatial Daemon

> **Purpose:** Consume raw CAD exports (SketchUp JSON, glTF, OBJ) and emit
> JSON manifests into `../001B_Spatial-Source-Layer/` that conform to
> the Vitruvius Spatial Contract v1.0.0
> (see `../.ai/06_specs/spatial-schema.md`).
>
> **Isolation:** This daemon is a sibling subproject. It has its own
> package.json, its own dependencies, and does not share a process with
> the Python pipeline. The Python pipeline only reads files the daemon
> writes — there is no RPC, no shared memory, no coupled runtime.

## Install
```bash
cd spatial-daemon
npm install
```

## Build
```bash
npm run build
```

## Test
```bash
npm test
```

## Run
```bash
npx vitruvius-spatial --input path/to/sketchup_export.json --output ../001B_Spatial-Source-Layer/
```

## Architecture
1. `src/aabb.ts` — axis-aligned bounding box computation
2. `src/gjk.ts` — GJK intersection for convex hulls
3. `src/contract_writer.ts` — emits JSON conforming to schema-v1.0.0
4. `src/cli.ts` — command-line entry point
```

Create `spatial-daemon/src/types.ts`:
```typescript
/**
 * Type definitions for the Vitruvius Spatial Contract v1.0.0.
 * These must stay byte-compatible with the Python validator at
 * scripts/vitruvius/spatial/schema.py.
 */

export type SpatialPredicate =
  | "spatial_intersects"
  | "spatial_clearance"
  | "spatial_adjacent_to"
  | "spatial_contains";

export interface BoundingBox {
  min: [number, number, number];
  max: [number, number, number];
}

export interface Instance {
  instance_id: string;            // must start with "instance-"
  canonical_concept_id: string;   // must start with "concept-"
  bounding_box?: BoundingBox;
}

export interface SpatialEdge {
  source_instance: string;        // must start with "instance-"
  predicate: SpatialPredicate;
  target_instance: string;        // must start with "instance-"
  value?: number;
  unit?: "meters" | "millimeters" | "feet" | "inches";
}

export interface SpatialContract {
  schema_version: "1.0.0";
  spatial_context_id: string;     // must start with "spatial-"
  generated_at_utc: string;
  source_daemon?: string;
  instances: Instance[];
  spatial_edges: SpatialEdge[];
}
```

- [ ] **Step 4: Install deps and run test**

```bash
cd spatial-daemon && npm install && npx vitest run tests/smoke.test.ts
```

Expected: 3 PASSED.

- [ ] **Step 5: Commit**

```bash
git add spatial-daemon
git commit -m "feat(spatial-daemon): Stream N.1 Node/TS project scaffold + types"
```

---

### Task N.2: AABB Builder from Raw Vertices

**Files:**
- Create: `spatial-daemon/src/aabb.ts`
- Test: `spatial-daemon/tests/aabb.test.ts`

- [ ] **Step 1: Write the failing test**

Create `spatial-daemon/tests/aabb.test.ts`:
```typescript
import { describe, expect, it } from "vitest";
import { buildAABB, intersectsAABB, distanceAABB } from "../src/aabb";
import type { BoundingBox } from "../src/types";

describe("buildAABB", () => {
  it("computes min/max from a flat vertex list", () => {
    const verts = [0, 0, 0, 1, 2, 3, -1, 4, 0.5];
    const box = buildAABB(verts);
    expect(box.min).toEqual([-1, 0, 0]);
    expect(box.max).toEqual([1, 4, 3]);
  });

  it("throws if vertices length is not a multiple of 3", () => {
    expect(() => buildAABB([0, 0])).toThrow();
  });

  it("throws if vertices is empty", () => {
    expect(() => buildAABB([])).toThrow();
  });
});

describe("intersectsAABB", () => {
  it("detects overlap", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [2, 2, 2] };
    const b: BoundingBox = { min: [1, 1, 1], max: [3, 3, 3] };
    expect(intersectsAABB(a, b)).toBe(true);
  });

  it("detects non-overlap", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [2, 2, 2], max: [3, 3, 3] };
    expect(intersectsAABB(a, b)).toBe(false);
  });

  it("treats edge-touching as intersection", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [1, 1, 1], max: [2, 2, 2] };
    expect(intersectsAABB(a, b)).toBe(true);
  });
});

describe("distanceAABB", () => {
  it("returns 0 for overlapping boxes", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [2, 2, 2] };
    const b: BoundingBox = { min: [1, 1, 1], max: [3, 3, 3] };
    expect(distanceAABB(a, b)).toBe(0);
  });

  it("returns separation distance for disjoint boxes along x-axis", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [3, 0, 0], max: [4, 1, 1] };
    expect(distanceAABB(a, b)).toBeCloseTo(2);
  });

  it("returns Euclidean separation for diagonally disjoint boxes", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [4, 5, 0], max: [5, 6, 1] };
    // nearest corners: (1,1,0) and (4,5,0) → sqrt(9+16) = 5
    expect(distanceAABB(a, b)).toBeCloseTo(5);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd spatial-daemon && npx vitest run tests/aabb.test.ts
```

Expected: FAIL — `aabb.ts` missing.

- [ ] **Step 3: Implement the AABB module**

Create `spatial-daemon/src/aabb.ts`:
```typescript
import type { BoundingBox } from "./types";

export function buildAABB(vertices: readonly number[]): BoundingBox {
  if (vertices.length === 0 || vertices.length % 3 !== 0) {
    throw new Error(
      `vertices must be a non-empty flat array with length divisible by 3 (got ${vertices.length})`
    );
  }
  let minX = Infinity, minY = Infinity, minZ = Infinity;
  let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
  for (let i = 0; i < vertices.length; i += 3) {
    const x = vertices[i];
    const y = vertices[i + 1];
    const z = vertices[i + 2];
    if (x < minX) minX = x;
    if (y < minY) minY = y;
    if (z < minZ) minZ = z;
    if (x > maxX) maxX = x;
    if (y > maxY) maxY = y;
    if (z > maxZ) maxZ = z;
  }
  return { min: [minX, minY, minZ], max: [maxX, maxY, maxZ] };
}

export function intersectsAABB(a: BoundingBox, b: BoundingBox): boolean {
  return (
    a.min[0] <= b.max[0] && a.max[0] >= b.min[0] &&
    a.min[1] <= b.max[1] && a.max[1] >= b.min[1] &&
    a.min[2] <= b.max[2] && a.max[2] >= b.min[2]
  );
}

export function distanceAABB(a: BoundingBox, b: BoundingBox): number {
  const dx = Math.max(0, Math.max(b.min[0] - a.max[0], a.min[0] - b.max[0]));
  const dy = Math.max(0, Math.max(b.min[1] - a.max[1], a.min[1] - b.max[1]));
  const dz = Math.max(0, Math.max(b.min[2] - a.max[2], a.min[2] - b.max[2]));
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd spatial-daemon && npx vitest run tests/aabb.test.ts
```

Expected: 9 PASSED.

- [ ] **Step 5: Commit**

```bash
git add spatial-daemon/src/aabb.ts spatial-daemon/tests/aabb.test.ts
git commit -m "feat(spatial-daemon): Stream N.2 AABB builder + intersection + distance"
```

---

### Task N.3: GJK Intersection for Convex Hulls

**Files:**
- Create: `spatial-daemon/src/gjk.ts`
- Test: `spatial-daemon/tests/gjk.test.ts`

- [ ] **Step 1: Write the failing test**

Create `spatial-daemon/tests/gjk.test.ts`:
```typescript
import { describe, expect, it } from "vitest";
import { gjkIntersect } from "../src/gjk";

// A unit cube at origin
const unitCube: [number, number, number][] = [
  [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
  [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1],
];

// Cube shifted by 2 on x-axis (disjoint)
const disjointCube: [number, number, number][] = unitCube.map(
  ([x, y, z]) => [x + 2, y, z] as [number, number, number],
);

// Cube shifted by 0.5 (overlaps unitCube)
const overlapCube: [number, number, number][] = unitCube.map(
  ([x, y, z]) => [x + 0.5, y, z] as [number, number, number],
);

// Tetrahedron sharing a vertex with unitCube (touches at (1,1,1))
const touchingTet: [number, number, number][] = [
  [1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2],
];

describe("gjkIntersect", () => {
  it("detects overlap between two overlapping cubes", () => {
    expect(gjkIntersect(unitCube, overlapCube)).toBe(true);
  });

  it("detects non-overlap between two separated cubes", () => {
    expect(gjkIntersect(unitCube, disjointCube)).toBe(false);
  });

  it("detects vertex-touching as intersection", () => {
    expect(gjkIntersect(unitCube, touchingTet)).toBe(true);
  });

  it("returns false for single-point vs far-away single-point", () => {
    expect(gjkIntersect([[0, 0, 0]], [[10, 10, 10]])).toBe(false);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd spatial-daemon && npx vitest run tests/gjk.test.ts
```

Expected: FAIL — `gjk.ts` missing.

- [ ] **Step 3: Implement GJK**

Create `spatial-daemon/src/gjk.ts`:
```typescript
/**
 * Minimal GJK intersection test for convex point-clouds in 3D.
 *
 * This is not a production physics-grade GJK — it supports the "are these
 * two convex hulls intersecting?" query used by the Vitruvius spatial
 * daemon. For distance queries, use `distanceAABB` from aabb.ts.
 *
 * References:
 *  - Van den Bergen, "A Fast and Robust GJK Implementation for Collision
 *    Detection of Convex Objects", JGT 4(2):7–25, 1999.
 *  - Ericson, Real-Time Collision Detection, Chapter 9.
 */

type Vec3 = readonly [number, number, number];

const MAX_ITERS = 32;
const EPSILON = 1e-9;

function sub(a: Vec3, b: Vec3): Vec3 {
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function dot(a: Vec3, b: Vec3): number {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function cross(a: Vec3, b: Vec3): Vec3 {
  return [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0],
  ];
}

function neg(a: Vec3): Vec3 {
  return [-a[0], -a[1], -a[2]];
}

function support(points: readonly Vec3[], direction: Vec3): Vec3 {
  let best = points[0];
  let bestDot = dot(best, direction);
  for (let i = 1; i < points.length; i++) {
    const d = dot(points[i], direction);
    if (d > bestDot) {
      bestDot = d;
      best = points[i];
    }
  }
  return best;
}

function minkowskiSupport(
  a: readonly Vec3[], b: readonly Vec3[], direction: Vec3
): Vec3 {
  return sub(support(a, direction), support(b, neg(direction)));
}

function doSimplex(simplex: Vec3[], direction: Vec3): Vec3 {
  // Returns the new direction; mutates simplex to keep the relevant sub-simplex.
  if (simplex.length === 2) {
    const [b, a] = [simplex[0], simplex[1]];
    const ab = sub(b, a);
    const ao = neg(a);
    const newDir = cross(cross(ab, ao), ab);
    if (dot(newDir, newDir) < EPSILON) {
      // Origin lies on the AB segment.
      return [0, 0, 0];
    }
    return newDir;
  }
  if (simplex.length === 3) {
    const [c, b, a] = simplex;
    const ab = sub(b, a);
    const ac = sub(c, a);
    const ao = neg(a);
    const abc = cross(ab, ac);
    if (dot(cross(abc, ac), ao) > 0) {
      simplex.splice(1, 1); // keep [c, a]
      return cross(cross(ac, ao), ac);
    }
    if (dot(cross(ab, abc), ao) > 0) {
      simplex.splice(0, 1); // keep [b, a]
      return cross(cross(ab, ao), ab);
    }
    if (dot(abc, ao) > 0) {
      return abc;
    }
    simplex.reverse();
    return neg(abc);
  }
  // Tetrahedron case
  const [d, c, b, a] = simplex;
  const ab = sub(b, a);
  const ac = sub(c, a);
  const ad = sub(d, a);
  const ao = neg(a);
  const abc = cross(ab, ac);
  const acd = cross(ac, ad);
  const adb = cross(ad, ab);
  if (dot(abc, ao) > 0) {
    simplex.splice(0, 1); // drop d
    return abc;
  }
  if (dot(acd, ao) > 0) {
    simplex.splice(2, 1); // drop b
    return acd;
  }
  if (dot(adb, ao) > 0) {
    simplex.splice(1, 1); // drop c
    return adb;
  }
  return [0, 0, 0];
}

export function gjkIntersect(
  hullA: readonly Vec3[],
  hullB: readonly Vec3[],
): boolean {
  if (hullA.length === 0 || hullB.length === 0) return false;
  let direction: Vec3 = [1, 0, 0];
  const simplex: Vec3[] = [minkowskiSupport(hullA, hullB, direction)];
  direction = neg(simplex[0]);
  for (let i = 0; i < MAX_ITERS; i++) {
    const a = minkowskiSupport(hullA, hullB, direction);
    if (dot(a, direction) < -EPSILON) {
      return false;
    }
    simplex.push(a);
    const newDir = doSimplex(simplex, direction);
    if (dot(newDir, newDir) < EPSILON) {
      return true; // origin contained
    }
    direction = newDir;
    if (simplex.length === 4) {
      return true;
    }
  }
  return true; // default to "intersects" on non-termination (conservative)
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd spatial-daemon && npx vitest run tests/gjk.test.ts
```

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add spatial-daemon/src/gjk.ts spatial-daemon/tests/gjk.test.ts
git commit -m "feat(spatial-daemon): Stream N.3 GJK convex-hull intersection test"
```

---

### Task N.4: Contract Writer (Emits JSON into 001B Layer)

**Files:**
- Create: `spatial-daemon/src/contract_writer.ts`
- Test: `spatial-daemon/tests/contract_writer.test.ts`

- [ ] **Step 1: Write the failing test**

Create `spatial-daemon/tests/contract_writer.test.ts`:
```typescript
import { describe, expect, it } from "vitest";
import { mkdtempSync, readFileSync, rmSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { writeContract } from "../src/contract_writer";
import type { SpatialContract } from "../src/types";

describe("writeContract", () => {
  it("writes a valid JSON file with the schema_version field", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "spatial-test-01",
        generated_at_utc: "2026-04-15T09:00:00Z",
        source_daemon: "vitruvius-spatial-daemon@0.1.0",
        instances: [
          {
            instance_id: "instance-door-01",
            canonical_concept_id: "concept-doors-and-exits",
          },
        ],
        spatial_edges: [],
      };
      const path = writeContract(contract, dir);
      const onDisk = JSON.parse(readFileSync(path, "utf-8"));
      expect(onDisk.schema_version).toBe("1.0.0");
      expect(onDisk.spatial_context_id).toBe("spatial-test-01");
      expect(path.endsWith("spatial-test-01.json")).toBe(true);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("throws when spatial_context_id does not start with 'spatial-'", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "bad",
        generated_at_utc: "2026-04-15T09:00:00Z",
        instances: [],
        spatial_edges: [],
      };
      expect(() => writeContract(contract, dir)).toThrow();
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("throws when an instance_id lacks the 'instance-' prefix", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "spatial-ok",
        generated_at_utc: "2026-04-15T09:00:00Z",
        instances: [
          { instance_id: "door", canonical_concept_id: "concept-door" } as any,
        ],
        spatial_edges: [],
      };
      expect(() => writeContract(contract, dir)).toThrow();
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd spatial-daemon && npx vitest run tests/contract_writer.test.ts
```

Expected: FAIL — `contract_writer.ts` missing.

- [ ] **Step 3: Implement the writer**

Create `spatial-daemon/src/contract_writer.ts`:
```typescript
import { mkdirSync, writeFileSync } from "fs";
import { join } from "path";
import type { SpatialContract } from "./types";

const ALLOWED_PREDICATES = new Set([
  "spatial_intersects",
  "spatial_clearance",
  "spatial_adjacent_to",
  "spatial_contains",
]);

function assertContract(contract: SpatialContract): void {
  if (contract.schema_version !== "1.0.0") {
    throw new Error(`schema_version must be "1.0.0" (got ${contract.schema_version})`);
  }
  if (!contract.spatial_context_id.startsWith("spatial-")) {
    throw new Error(
      `spatial_context_id must start with 'spatial-' (got ${contract.spatial_context_id})`,
    );
  }
  for (const inst of contract.instances) {
    if (!inst.instance_id.startsWith("instance-")) {
      throw new Error(`instance_id must start with 'instance-' (got ${inst.instance_id})`);
    }
    if (!inst.canonical_concept_id.startsWith("concept-")) {
      throw new Error(
        `canonical_concept_id must start with 'concept-' (got ${inst.canonical_concept_id})`,
      );
    }
  }
  for (const edge of contract.spatial_edges) {
    if (!ALLOWED_PREDICATES.has(edge.predicate)) {
      throw new Error(`unknown predicate: ${edge.predicate}`);
    }
  }
}

export function writeContract(contract: SpatialContract, outputDir: string): string {
  assertContract(contract);
  mkdirSync(outputDir, { recursive: true });
  const filename = `${contract.spatial_context_id}.json`;
  const path = join(outputDir, filename);
  writeFileSync(path, JSON.stringify(contract, null, 2) + "\n", "utf-8");
  return path;
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd spatial-daemon && npx vitest run tests/contract_writer.test.ts
```

Expected: 3 PASSED.

- [ ] **Step 5: Commit**

```bash
git add spatial-daemon/src/contract_writer.ts spatial-daemon/tests/contract_writer.test.ts
git commit -m "feat(spatial-daemon): Stream N.4 contract writer with schema assertions"
```

---

### Task N.5: CLI Entry Point + Integration Smoke Test

**Files:**
- Create: `spatial-daemon/src/cli.ts`
- Create: `spatial-daemon/tests/cli.test.ts`
- Create: `spatial-daemon/tests/fixtures/box_intersection.json`

- [ ] **Step 1: Write the failing test**

Create `spatial-daemon/tests/fixtures/box_intersection.json`:
```json
{
  "spatial_context_id": "spatial-smoke-01",
  "entities": [
    {
      "instance_id": "instance-corridor",
      "canonical_concept_id": "concept-means-of-egress",
      "vertices": [0, 0, 0, 10, 0, 0, 0, 1.1, 0, 10, 1.1, 0, 0, 0, 2.4, 10, 0, 2.4, 0, 1.1, 2.4, 10, 1.1, 2.4]
    },
    {
      "instance_id": "instance-fire-door",
      "canonical_concept_id": "concept-doors-and-exits",
      "vertices": [5, 0, 0, 5.9, 0, 0, 5, 0.1, 0, 5.9, 0.1, 0, 5, 0, 2.1, 5.9, 0, 2.1, 5, 0.1, 2.1, 5.9, 0.1, 2.1]
    }
  ]
}
```

Create `spatial-daemon/tests/cli.test.ts`:
```typescript
import { describe, expect, it } from "vitest";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { analyzeFromInputFile } from "../src/cli";

describe("analyzeFromInputFile", () => {
  it("produces a valid spatial contract file from the box_intersection fixture", () => {
    const outDir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-out-"));
    try {
      const fixture = join(__dirname, "fixtures", "box_intersection.json");
      const result = analyzeFromInputFile(fixture, outDir);
      expect(result.writtenPath).toMatch(/spatial-smoke-01\.json$/);
      const files = readdirSync(outDir);
      expect(files).toContain("spatial-smoke-01.json");
      const payload = JSON.parse(readFileSync(result.writtenPath, "utf-8"));
      expect(payload.schema_version).toBe("1.0.0");
      expect(payload.instances).toHaveLength(2);
      // The two boxes overlap along x ∈ [5, 5.9]; expect a spatial_intersects edge
      const intersects = payload.spatial_edges.filter(
        (e: any) => e.predicate === "spatial_intersects"
      );
      expect(intersects.length).toBeGreaterThan(0);
    } finally {
      rmSync(outDir, { recursive: true, force: true });
    }
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd spatial-daemon && npx vitest run tests/cli.test.ts
```

Expected: FAIL — `cli.ts` missing.

- [ ] **Step 3: Implement the CLI module**

Create `spatial-daemon/src/cli.ts`:
```typescript
import { readFileSync } from "fs";
import { buildAABB, intersectsAABB, distanceAABB } from "./aabb";
import { writeContract } from "./contract_writer";
import type { Instance, SpatialContract, SpatialEdge } from "./types";

interface RawEntity {
  instance_id: string;
  canonical_concept_id: string;
  vertices: number[];
}

interface RawInput {
  spatial_context_id: string;
  entities: RawEntity[];
}

export interface AnalyzeResult {
  writtenPath: string;
  contract: SpatialContract;
}

export function analyzeFromInputFile(inputPath: string, outputDir: string): AnalyzeResult {
  const raw = JSON.parse(readFileSync(inputPath, "utf-8")) as RawInput;

  const instances: Instance[] = raw.entities.map((e) => ({
    instance_id: e.instance_id,
    canonical_concept_id: e.canonical_concept_id,
    bounding_box: buildAABB(e.vertices),
  }));

  const edges: SpatialEdge[] = [];
  for (let i = 0; i < instances.length; i++) {
    for (let j = i + 1; j < instances.length; j++) {
      const a = instances[i];
      const b = instances[j];
      if (!a.bounding_box || !b.bounding_box) continue;
      if (intersectsAABB(a.bounding_box, b.bounding_box)) {
        edges.push({
          source_instance: a.instance_id,
          predicate: "spatial_intersects",
          target_instance: b.instance_id,
        });
      }
      const distance = distanceAABB(a.bounding_box, b.bounding_box);
      edges.push({
        source_instance: a.instance_id,
        predicate: "spatial_clearance",
        target_instance: b.instance_id,
        value: Math.round(distance * 1000) / 1000,
        unit: "meters",
      });
    }
  }

  const contract: SpatialContract = {
    schema_version: "1.0.0",
    spatial_context_id: raw.spatial_context_id,
    generated_at_utc: new Date().toISOString().replace(/\.\d+Z$/, "Z"),
    source_daemon: "vitruvius-spatial-daemon@0.1.0",
    instances,
    spatial_edges: edges,
  };

  const writtenPath = writeContract(contract, outputDir);
  return { writtenPath, contract };
}

// Node entrypoint — invoked via `npx vitruvius-spatial --input ... --output ...`
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const inputIdx = args.indexOf("--input");
  const outputIdx = args.indexOf("--output");
  if (inputIdx < 0 || outputIdx < 0) {
    console.error("Usage: vitruvius-spatial --input <file.json> --output <dir>");
    process.exit(2);
  }
  const result = analyzeFromInputFile(args[inputIdx + 1], args[outputIdx + 1]);
  console.log(JSON.stringify({ written: result.writtenPath }, null, 2));
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd spatial-daemon && npx vitest run tests/cli.test.ts
```

Expected: 1 PASSED.

- [ ] **Step 5: Full daemon regression**

```bash
cd spatial-daemon && npm test && npm run typecheck
```

Expected: all tests pass; `tsc --noEmit` is clean.

- [ ] **Step 6: Commit**

```bash
git add spatial-daemon/src/cli.ts spatial-daemon/tests/cli.test.ts spatial-daemon/tests/fixtures/box_intersection.json
git commit -m "feat(spatial-daemon): Stream N.5 CLI entry + AABB→contract smoke test"
```

---

## 10. Stream O — Epistemic Foraging Scaffold

> **Hard rule.** This stream ships zero live HTTP fetchers. It builds the
> data model, configuration format, and drift detector *only*. Any future
> stream that wires in `urllib`/`requests`/`httpx` requires its own
> security review plus an explicit reopen condition (see §2.2).

### Task O.1: Watched Sources Registry

**Files:**
- Create: `scripts/vitruvius/foraging/__init__.py`
- Create: `scripts/vitruvius/foraging/watched_sources.py`
- Create: `scripts/vitruvius/foraging/watched_sources.yaml`
- Test: `scripts/tests/test_foraging_watched_sources.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_foraging_watched_sources.py
"""Stream O.1 — watched-sources registry loader."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.foraging.watched_sources import (
    WatchedSource,
    WatchedSourcesError,
    load_watched_sources,
)


def _write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "watched_sources.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_load_empty_registry_returns_empty(tmp_path: Path) -> None:
    path = _write(tmp_path, "sources: []\n")
    assert load_watched_sources(path) == []


def test_load_single_source(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid/dpwh\n"
        "    category: 001-Laws\n"
        "    subcategory: RA-pending\n"
        "    frequency: weekly\n",
    )
    sources = load_watched_sources(path)
    assert len(sources) == 1
    src = sources[0]
    assert isinstance(src, WatchedSource)
    assert src.name == "DPWH"
    assert src.url == "https://example.invalid/dpwh"
    assert src.frequency == "weekly"


def test_invalid_frequency_rejected(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid\n"
        "    category: 001-Laws\n"
        "    frequency: hourly\n",
    )
    with pytest.raises(WatchedSourcesError, match="frequency"):
        load_watched_sources(path)


def test_non_https_url_rejected(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: Bad\n"
        "    url: http://insecure\n"
        "    category: 001-Laws\n"
        "    frequency: daily\n",
    )
    with pytest.raises(WatchedSourcesError, match="https"):
        load_watched_sources(path)


def test_duplicate_name_rejected(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid/a\n"
        "    category: 001-Laws\n"
        "    frequency: daily\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid/b\n"
        "    category: 001-Laws\n"
        "    frequency: weekly\n",
    )
    with pytest.raises(WatchedSourcesError, match="duplicate"):
        load_watched_sources(path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_foraging_watched_sources.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement the loader**

Create `scripts/vitruvius/foraging/__init__.py`:
```python
"""Epistemic foraging (Stream O) — scaffold only.

This subpackage ships the watched-sources registry, a drift detector that
reuses the existing Mahalanobis outlier detector from Stream C.4, and a
hash-based duplicate detector stub. It does NOT perform any HTTP fetches.
Any module that adds a network call requires a security review per the
plan's §2.2 reopen condition.
"""
```

Create `scripts/vitruvius/foraging/watched_sources.py`:
```python
"""Stream O.1 — YAML loader for the watched-sources registry."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


class WatchedSourcesError(ValueError):
    pass


_ALLOWED_FREQUENCIES = frozenset({"daily", "weekly", "monthly"})


@dataclass(frozen=True)
class WatchedSource:
    name: str
    url: str
    category: str
    subcategory: str | None
    frequency: str


def load_watched_sources(yaml_path: Path) -> list[WatchedSource]:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    rows = raw.get("sources", [])
    out: list[WatchedSource] = []
    seen: set[str] = set()
    for idx, row in enumerate(rows):
        name = row.get("name")
        url = row.get("url")
        category = row.get("category")
        frequency = row.get("frequency")
        subcategory = row.get("subcategory")
        if not isinstance(name, str) or not name:
            raise WatchedSourcesError(f"sources[{idx}].name missing or empty")
        if name in seen:
            raise WatchedSourcesError(f"duplicate source name {name!r}")
        seen.add(name)
        if not isinstance(url, str) or not url.startswith("https://"):
            raise WatchedSourcesError(
                f"sources[{idx}].url must start with 'https://' (got {url!r})"
            )
        if not isinstance(category, str) or not category:
            raise WatchedSourcesError(f"sources[{idx}].category must be a string")
        if frequency not in _ALLOWED_FREQUENCIES:
            raise WatchedSourcesError(
                f"sources[{idx}].frequency {frequency!r} not in {sorted(_ALLOWED_FREQUENCIES)}"
            )
        out.append(
            WatchedSource(
                name=name,
                url=url,
                category=category,
                subcategory=subcategory if isinstance(subcategory, str) else None,
                frequency=frequency,
            )
        )
    return out
```

Create `scripts/vitruvius/foraging/watched_sources.yaml`:
```yaml
# Stream O.1 — registry of external sources to eventually monitor.
# No fetcher ships in this plan (see §2.2). This file is a data contract only.
sources:
  - name: DPWH-Circulars
    url: https://example.invalid/dpwh/circulars
    category: 001-Laws
    subcategory: DPWH-pending
    frequency: weekly
  - name: ASTM-International
    url: https://example.invalid/astm
    category: 004-Technology
    subcategory: material-standards
    frequency: monthly
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_foraging_watched_sources.py -v`

Expected: 5 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/foraging/__init__.py scripts/vitruvius/foraging/watched_sources.py scripts/vitruvius/foraging/watched_sources.yaml scripts/tests/test_foraging_watched_sources.py
git commit -m "feat(foraging): Stream O.1 watched-sources registry (scaffold only)"
```

---

### Task O.2: Drift Detector Reusing Mahalanobis Outlier Module

**Files:**
- Create: `scripts/vitruvius/foraging/drift_detector.py`
- Test: `scripts/tests/test_foraging_drift_detector.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_foraging_drift_detector.py
"""Stream O.2 — drift detector wrapping Stream C.4 Mahalanobis outlier."""
from __future__ import annotations

import pytest

numpy = pytest.importorskip("numpy")

from vitruvius.foraging.drift_detector import (
    DriftDecision,
    DriftVerdict,
    evaluate_document_drift,
)


def test_in_distribution_document_is_normal() -> None:
    baseline = numpy.array([
        [1.0, 2.0, 3.0],
        [1.1, 2.1, 3.1],
        [0.9, 1.9, 2.9],
        [1.05, 2.05, 3.05],
    ])
    new_vec = numpy.array([1.02, 2.02, 3.02])
    verdict = evaluate_document_drift(
        baseline_features=baseline,
        new_feature_vector=new_vec,
        threshold=3.0,
    )
    assert isinstance(verdict, DriftDecision)
    assert verdict.classification == DriftVerdict.IN_DISTRIBUTION


def test_out_of_distribution_document_is_drift() -> None:
    baseline = numpy.array([
        [1.0, 2.0, 3.0],
        [1.1, 2.1, 3.1],
        [0.9, 1.9, 2.9],
        [1.05, 2.05, 3.05],
    ])
    new_vec = numpy.array([50.0, 50.0, 50.0])
    verdict = evaluate_document_drift(
        baseline_features=baseline,
        new_feature_vector=new_vec,
        threshold=3.0,
    )
    assert verdict.classification == DriftVerdict.DRIFT


def test_insufficient_baseline_is_indeterminate() -> None:
    baseline = numpy.array([[1.0, 2.0, 3.0]])
    new_vec = numpy.array([1.1, 2.1, 3.1])
    verdict = evaluate_document_drift(
        baseline_features=baseline,
        new_feature_vector=new_vec,
        threshold=3.0,
    )
    assert verdict.classification == DriftVerdict.INDETERMINATE


def test_mismatched_dimensionality_is_indeterminate() -> None:
    baseline = numpy.array([
        [1.0, 2.0, 3.0],
        [1.1, 2.1, 3.1],
        [0.9, 1.9, 2.9],
    ])
    new_vec = numpy.array([1.0, 2.0])  # 2-d instead of 3-d
    verdict = evaluate_document_drift(
        baseline_features=baseline,
        new_feature_vector=new_vec,
        threshold=3.0,
    )
    assert verdict.classification == DriftVerdict.INDETERMINATE
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_foraging_drift_detector.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement the drift detector**

Create `scripts/vitruvius/foraging/drift_detector.py`:
```python
"""Stream O.2 — Mahalanobis-based drift detector for newly foraged documents.

This module intentionally does NOT fetch documents itself. Given a
feature vector that was extracted by *some other* code path (real
scraper, manual ingest, test fixture), it answers: "is this document
in-distribution relative to our existing corpus?" — using the Mahalanobis
distance we already compute in Stream C.4.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DriftVerdict(str, Enum):
    IN_DISTRIBUTION = "in_distribution"
    DRIFT = "drift"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True)
class DriftDecision:
    classification: DriftVerdict
    distance: float | None
    threshold: float
    reason: str


def _try_import_numpy():
    try:
        import numpy  # type: ignore
        return numpy
    except ImportError:
        return None


def evaluate_document_drift(
    *,
    baseline_features: object,
    new_feature_vector: object,
    threshold: float = 3.0,
) -> DriftDecision:
    np = _try_import_numpy()
    if np is None:
        return DriftDecision(
            classification=DriftVerdict.INDETERMINATE,
            distance=None,
            threshold=threshold,
            reason="numpy not installed; feature disabled",
        )

    baseline = np.asarray(baseline_features, dtype=float)
    vector = np.asarray(new_feature_vector, dtype=float)

    if baseline.ndim != 2 or baseline.shape[0] < 2:
        return DriftDecision(
            classification=DriftVerdict.INDETERMINATE,
            distance=None,
            threshold=threshold,
            reason="baseline requires >= 2 feature rows",
        )
    if vector.ndim != 1 or vector.shape[0] != baseline.shape[1]:
        return DriftDecision(
            classification=DriftVerdict.INDETERMINATE,
            distance=None,
            threshold=threshold,
            reason="feature vector dimension does not match baseline",
        )

    mean = baseline.mean(axis=0)
    cov = np.cov(baseline, rowvar=False)
    if cov.ndim == 0:
        cov = np.array([[float(cov)]])

    try:
        inv_cov = np.linalg.pinv(cov)
    except Exception as exc:  # pragma: no cover — defensive
        return DriftDecision(
            classification=DriftVerdict.INDETERMINATE,
            distance=None,
            threshold=threshold,
            reason=f"covariance inversion failed: {exc}",
        )

    delta = vector - mean
    dist_sq = float(delta @ inv_cov @ delta)
    if dist_sq < 0:
        dist_sq = 0.0
    distance = dist_sq ** 0.5

    classification = (
        DriftVerdict.DRIFT if distance > threshold else DriftVerdict.IN_DISTRIBUTION
    )
    return DriftDecision(
        classification=classification,
        distance=distance,
        threshold=threshold,
        reason="mahalanobis distance computed",
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_foraging_drift_detector.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/foraging/drift_detector.py scripts/tests/test_foraging_drift_detector.py
git commit -m "feat(foraging): Stream O.2 Mahalanobis drift detector"
```

---

### Task O.3: Duplicate Detector Stub

**Files:**
- Create: `scripts/vitruvius/foraging/duplicate_detector.py`
- Test: `scripts/tests/test_foraging_duplicate_detector.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_foraging_duplicate_detector.py
"""Stream O.3 — SHA-256 duplicate detector (foraging-scale)."""
from __future__ import annotations

from pathlib import Path

from vitruvius.foraging.duplicate_detector import (
    DuplicateFinding,
    is_duplicate_of_known,
    scan_for_duplicates,
)


def test_is_duplicate_detects_matching_content(tmp_path: Path) -> None:
    baseline = tmp_path / "existing.pdf"
    baseline.write_bytes(b"exact same content")
    assert is_duplicate_of_known(
        new_bytes=b"exact same content",
        known_hashes={
            "7c2c9f4f9b3d...": baseline,  # hash value intentionally ignored
        },
    ) is False  # unknown hash format — should not raise

    # Happy path: supply the real hash
    import hashlib
    real_hash = hashlib.sha256(b"exact same content").hexdigest()
    assert is_duplicate_of_known(
        new_bytes=b"exact same content",
        known_hashes={real_hash: baseline},
    ) is True


def test_scan_detects_duplicate_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_bytes(b"alpha")
    (tmp_path / "b.txt").write_bytes(b"beta")
    (tmp_path / "a_copy.txt").write_bytes(b"alpha")
    findings = scan_for_duplicates(tmp_path)
    assert len(findings) == 1
    finding = findings[0]
    assert isinstance(finding, DuplicateFinding)
    assert {p.name for p in finding.paths} == {"a.txt", "a_copy.txt"}


def test_scan_returns_empty_on_unique_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_bytes(b"alpha")
    (tmp_path / "b.txt").write_bytes(b"beta")
    assert scan_for_duplicates(tmp_path) == []


def test_scan_handles_missing_dir(tmp_path: Path) -> None:
    assert scan_for_duplicates(tmp_path / "nonexistent") == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_foraging_duplicate_detector.py -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement the detector**

Create `scripts/vitruvius/foraging/duplicate_detector.py`:
```python
"""Stream O.3 — SHA-256 duplicate detector for foraged document candidates.

Before a foraged file is promoted into 001_Raw-Source-Layer, the ingestion
pipeline should hash it and check against a registry of known hashes. This
module provides that check in a form that can be reused by a future
scraper without adding a network call here.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class DuplicateFinding:
    hash_hex: str
    paths: tuple[Path, ...]


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_duplicate_of_known(
    *,
    new_bytes: bytes,
    known_hashes: dict[str, Path],
) -> bool:
    return _sha256_hex(new_bytes) in known_hashes


def scan_for_duplicates(directory: Path) -> list[DuplicateFinding]:
    if not directory.exists() or not directory.is_dir():
        return []
    buckets: dict[str, list[Path]] = {}
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        h = _sha256_hex(path.read_bytes())
        buckets.setdefault(h, []).append(path)
    findings: list[DuplicateFinding] = []
    for h, paths in buckets.items():
        if len(paths) < 2:
            continue
        findings.append(DuplicateFinding(hash_hex=h, paths=tuple(paths)))
    findings.sort(key=lambda f: f.hash_hex)
    return findings
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_foraging_duplicate_detector.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Final full regression**

Run: `PYTHONPATH=scripts pytest scripts/tests/ -q`

Expected: all tests pass. The suite now has ~850 tests (prior 788 + Stream L 39 + Stream M 13 + Stream O 13 ≈ 853). The daemon is tested separately via `cd spatial-daemon && npm test`.

- [ ] **Step 6: Commit**

```bash
git add scripts/vitruvius/foraging/duplicate_detector.py scripts/tests/test_foraging_duplicate_detector.py
git commit -m "feat(foraging): Stream O.3 SHA-256 duplicate detector scaffold"
```

---

## 11. Integration Testing and Observability

### 11.1 End-to-End Smoke Path (Manual Rehearsal)
After all tasks are shipped, run this sequence against the repo root to verify the plumbing works on real-ish data. No task below ships — this is a manual rehearsal that the plan author performs once and then documents the result in `.ai/10_state/decisions.md`.

```bash
# 1. Daemon produces a contract file
cd spatial-daemon
npm run build
node dist/cli.js --input tests/fixtures/box_intersection.json --output ../001B_Spatial-Source-Layer/
cd ..

# 2. Enable the flag and run the Python ingest
python3 -c "
import yaml
p = 'config/vitruvius.yaml'
d = yaml.safe_load(open(p))
d['features']['l_spatial_ingestion'] = True
d['features']['l_z3_constraint_solver'] = True
open(p, 'w').write(yaml.safe_dump(d, sort_keys=False))
"
PYTHONPATH=scripts python scripts/pipeline_cli.py ingest-spatial

# 3. Evaluate against a hand-authored rule file
cat > 005_Operational-Intelligence-Layer/spatial/rules.json <<'EOF'
{
  "concept-means-of-egress__spatial_clearance__concept-doors-and-exits": {
    "operator": ">=",
    "required": 1.0
  }
}
EOF
PYTHONPATH=scripts python scripts/pipeline_cli.py evaluate-spatial --rules 005_Operational-Intelligence-Layer/spatial/rules.json

# 4. Export OWL/Turtle
PYTHONPATH=scripts python scripts/pipeline_cli.py build-graph
PYTHONPATH=scripts python scripts/pipeline_cli.py export-graph-owl > /tmp/vitruvius.ttl

# 5. Revert the flags to false (non-breaking verification)
python3 -c "
import yaml
p = 'config/vitruvius.yaml'
d = yaml.safe_load(open(p))
for k in list(d['features']):
  if k.startswith(('l_', 'm_', 'n_', 'o_')):
    d['features'][k] = False
open(p, 'w').write(yaml.safe_dump(d, sort_keys=False))
"
PYTHONPATH=scripts pytest scripts/tests/test_3d_upgrade_backcompat.py -v
```

The smoke path is successful iff:
- The daemon writes a valid JSON file into `001B_Spatial-Source-Layer/`.
- `ingest-spatial` exits 0 and writes `latest_spatial_candidates.json`.
- `evaluate-spatial` exits 0 with `pass_count: 1`.
- `export-graph-owl` writes valid Turtle (parseable by rdflib).
- With all flags reverted to false, the backcompat test still passes.

Document the result in `.ai/10_state/decisions.md` as `AD-<next>: 3D Spatial Intelligence Upgrade smoke-tested on date YYYY-MM-DD`.

### 11.2 Observability Hooks (Future Work)
No new metrics ship in this plan. When the Ranger dashboard lands (blocked task FUTURE-UI-01), add panels for:
- Spatial candidate counts per context
- Z3 verdicts (pass/fail/indeterminate) per concept pair
- Mahalanobis drift scores per watched source
- Daemon JSON emission timestamps (latency sentinel)

## 12. Self-Review Checklist

Before handing the plan off to execution, verify:

### 12.1 Spec Coverage
- [x] Research §1 (Ontological Unification) — covered by Stream M (static IFC registry + OWL exporter; full RDF triple-store deferred in §2.3).
- [ ] Research §2 (PINNs) — **DEFERRED**, see §2.1. No task exists.
- [x] Research §3 (Epistemic Foraging) — covered as scaffold by Stream O; live scrapers deferred in §2.2.
- [x] Research §4 (Decoupled Spatial Translator) — covered by Streams L (Python side) + N (TypeScript daemon) + L.7 CLI wiring.
- [x] Research "JSON Schema" — covered by Task L.2 + §6.
- [x] Research "Python ingestion" (`spatial_ingestion_one.py`) — covered by Task L.3 walker + L.4 mapper + L.7 CLI.
- [x] Research "Z3 constraint solver" — covered by Tasks L.5 + L.6.
- [x] Research "CLI integration" — covered by Task L.7.
- [x] Research "Node.js daemon" — covered by Stream N (all 5 tasks).
- [x] Research "GJK algorithm" — covered by Task N.3.

### 12.2 Placeholder Scan
- No "TBD" / "implement later" / "similar to Task N" / "add appropriate error handling" in any task body.
- Every code block is a complete, runnable snippet.
- Every test is a full test file with imports and assertions.

### 12.3 Type Consistency
- `SpatialCandidate` dataclass is defined in L.3 and used unchanged in L.4, L.5, L.6, L.7.
- `ConstraintVerdict` enum members (`SATISFIED`, `VIOLATED`, `INDETERMINATE`) are identical across L.5, L.6, L.7.
- `IfcMappingEntry` dataclass is defined in M.1 and used unchanged in M.2, M.3, M.4.
- `BoundingBox` type is defined in `spatial-daemon/src/types.ts` (N.1) and used unchanged in N.2 (`buildAABB`, `intersectsAABB`, `distanceAABB`).
- `SpatialContract` TS interface (N.1) matches the Python schema (L.2) field-for-field.

### 12.4 Non-Breaking Guarantee
- Every new Python module is gated by at least one `features.l_*`, `m_*`, or `o_*` flag, default false.
- `scripts/vitruvius/graph/contract.py` changes are strictly additive (L.1 Step 5).
- `test_3d_upgrade_backcompat.py` (L.8) locks the Phase 8 snapshot against drift.
- CLI commands (`ingest-spatial`, `evaluate-spatial`, `export-graph-owl`) are all new — none replace existing commands.

## 13. Open Questions

1. **Spatial edge promotion.** Should `spatial_clearance` / `spatial_intersects` edges enter the canonical `003_…/relationships/` layer, or stay in a parallel `005_…/spatial/` snapshot? This plan keeps them parallel (in 005) to avoid contaminating text-evidence edges. Revisit after 3 real BIM models are in the pipeline.
2. **IFC class granularity.** Some canonical concepts (e.g., `concept-means-of-egress`) have no single clean IFC class — egress paths are modelled as a pattern of `IfcSpace` + `IfcDoor` + `IfcCovering`. Stream M.1 picks the closest single class; a future extension could emit compound IFC assertions.
3. **Rule file format for `evaluate-spatial`.** Stream L.7 uses a flat JSON dict keyed by `"<src_concept>__<predicate>__<tgt_concept>"`. This is ergonomic for unit tests but fragile for humans. Reopen this after three real rules ship.
4. **Daemon discovery of canonical concept IDs.** The daemon currently requires the caller to hand-label each vertex group with a `canonical_concept_id`. A future task could read the IFC registry (Stream M.1) and auto-suggest IDs from IFC class names, but that coupling must be explicit in a separate plan.
5. **z3-solver license.** z3-solver is MIT-licensed and bundles the Microsoft Research Z3 binaries. No license issue, but note it in the README when shipping.

## 14. Deferred / Rejected Items (Trace to Research Doc)

| Research Item | Disposition | Reason |
|---|---|---|
| Full IFC triple-store (§1) | **DEFERRED** | Static registry suffices for v1 (§2.3). Full RDF store requires 7000+ IFC class URIs; adds a second database. |
| PINNs (§2) | **REJECTED-DEFERRED** | No GPU, no training corpus, Z3 covers the numeric case (§2.1). |
| Live HTTP scrapers (§3) | **DEFERRED** | Security surface too large without a dedicated review (§2.2). |
| SketchUp plugin bundle | **OUT OF SCOPE** | Daemon accepts raw JSON; plugin authorship is a separate workstream. |
| Neo4j / Dgraph external graph | **REJECTED** | Violates principle P1 (filesystem is the database). Phase 8 established this. |

## 15. Changelog

- **2026-04-14 (v1.0.0)** — Initial plan published. Derived from `.ai/13_research/3D-Thinking-improvement.md` after a full codebase audit of the current Phase 8 graph subsystem, the feature-flag harness (Stream A), the relationship schema (§6.1), and the existing CLI lazy-import conventions. Four streams (L/M/N/O) map to the four research pillars; PINNs are deferred with rationale in §2.1.
