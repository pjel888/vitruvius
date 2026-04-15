---
task: nested-agents-governance
phase: 04
created: 2026-04-15
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — Nested AGENTS Governance Needs

## Executive Judgment
The repository already has a root `AGENTS.md` and a small set of nested `AGENTS.md` files, but the hierarchy is incomplete and stale. The current nested coverage is too thin to protect several high-risk boundaries:
- governance memory under `.ai/`
- test behavior under `scripts/tests/`
- Rust compute zones under `scripts/vitruvius/engine_rs/` and `scripts/vitruvius/datalog_rs/`
- the TypeScript spatial sibling under `spatial-daemon/`
- truth-bearing canonical storage under `003_Canonical-Knowledge-Layer/`
- performance / graph artifact storage under `005_Operational-Intelligence-Layer/`

At the same time, creating `AGENTS.md` files for every subpackage under `scripts/vitruvius/` would be governance clutter and would drift quickly.

## 1. Current Root Governance Quality

### Strengths
- Root `AGENTS.md` is strict and explicit about authority order, stop conditions, and MCP-first exploration.
- The root contract already expects nested guidance in several top-level directories.
- The repo has mature governance collateral under `.ai/06_specs/` that nested files can point to instead of duplicating.

### Weaknesses
- Root `AGENTS.md` is stale on active-state file paths.
- Root `AGENTS.md` does not reflect today’s high-risk boundaries such as `.ai/`, `spatial-daemon/`, Rust crate roots, or canonical / operational-intelligence layers.
- The existing nested `AGENTS.md` files are generic and underpowered for a repo with Rust, TypeScript, Z3, RocksDB, GraphSAGE, and truth-promotion contracts.

## 2. Existing Nested Coverage

### Present
- `scripts/AGENTS.md`
- `scripts/vitruvius/AGENTS.md`
- `scripts/vitruvius/rules/AGENTS.md`
- `config/AGENTS.md`
- `docs/AGENTS.md`
- `006_System-Manifests/AGENTS.md`

### Assessment
- all six are justified in principle
- all six are too generic in current form
- none of them adequately describe local risk, forbidden ownership, or validation expectations for the current codebase

## 3. Repo Areas Lacking Local Operating Contracts
- `.ai/` — governance / state / plans / audits / specs all live here; no local contract currently
- `scripts/tests/` — tests are a first-class safety surface and differ from production code
- `scripts/vitruvius/engine_rs/` — Rust workspace with PyO3 + wasm32 boundary
- `scripts/vitruvius/datalog_rs/` — standalone Rust crate with Python bridge, separate from workspace
- `spatial-daemon/` — Node/TypeScript sibling with contract-writer role
- `003_Canonical-Knowledge-Layer/` — trusted canonical truth store
- `005_Operational-Intelligence-Layer/` — graph, embeddings, caches, snapshots; not source-of-truth law

## 4. Areas Where Local Contracts Would Be Redundant
- `001_Raw-Source-Layer/` — root law already enforces immutability clearly
- `002_Raw-Conversion-Layer/` — mostly generated intermediates; little stable human-owned architecture
- `004_Derived-Content-Layer/` — currently low architectural weight
- deep leaves under `scripts/vitruvius/` such as `graph/`, `review/`, `query/`, `parsers/`, `normalization/`
  - adding local files there would fragment guidance without enough stable distinction

## 5. Risk Categories By Directory

| Directory | Architecture | Truth | Performance | Rust | Cross-language | State drift | Audit Judgment |
|---|---|---:|---:|---:|---:|---:|---|
| `.ai/` | HIGH | MEDIUM | LOW | LOW | LOW | HIGH | Needs local AGENTS |
| `scripts/` | MEDIUM | LOW | LOW | LOW | LOW | MEDIUM | Existing AGENTS should be upgraded |
| `scripts/vitruvius/` | HIGH | HIGH | HIGH | MEDIUM | HIGH | MEDIUM | Existing AGENTS should be upgraded |
| `scripts/tests/` | MEDIUM | MEDIUM | MEDIUM | MEDIUM | MEDIUM | LOW | Needs local AGENTS |
| `scripts/vitruvius/rules/` | MEDIUM | HIGH | LOW | LOW | LOW | LOW | Existing AGENTS should be upgraded |
| `scripts/vitruvius/engine_rs/` | HIGH | LOW | HIGH | HIGH | HIGH | LOW | Needs local AGENTS |
| `scripts/vitruvius/datalog_rs/` | HIGH | MEDIUM | MEDIUM | HIGH | HIGH | LOW | Needs local AGENTS |
| `spatial-daemon/` | HIGH | LOW | MEDIUM | LOW | HIGH | LOW | Needs local AGENTS |
| `config/` | MEDIUM | MEDIUM | MEDIUM | LOW | LOW | MEDIUM | Existing AGENTS should be upgraded |
| `docs/` | LOW | MEDIUM | LOW | LOW | LOW | MEDIUM | Existing AGENTS should be upgraded |
| `003_Canonical-Knowledge-Layer/` | MEDIUM | HIGH | LOW | LOW | LOW | MEDIUM | Needs local AGENTS |
| `005_Operational-Intelligence-Layer/` | MEDIUM | MEDIUM | HIGH | LOW | LOW | MEDIUM | Needs local AGENTS |
| `006_System-Manifests/` | LOW | MEDIUM | LOW | LOW | LOW | MEDIUM | Existing AGENTS should be upgraded |

## 6. Proposed AGENTS Hierarchy

### Root
- `AGENTS.md`
  - remains controlling law
  - should be minimally reconciled where it currently points to stale state paths

### Justified Local Contracts
- `.ai/AGENTS.md`
- `scripts/AGENTS.md`
- `scripts/vitruvius/AGENTS.md`
- `scripts/tests/AGENTS.md`
- `scripts/vitruvius/rules/AGENTS.md`
- `scripts/vitruvius/engine_rs/AGENTS.md`
- `scripts/vitruvius/datalog_rs/AGENTS.md`
- `spatial-daemon/AGENTS.md`
- `config/AGENTS.md`
- `docs/AGENTS.md`
- `003_Canonical-Knowledge-Layer/AGENTS.md`
- `005_Operational-Intelligence-Layer/AGENTS.md`
- `006_System-Manifests/AGENTS.md`

## 7. Potential Contradictions or Stale Areas
- Root `AGENTS.md` uses stale state paths.
- `.ai/06_specs/GOVERNANCE/02_DOCUMENT_AUTHORITY_AND_UPDATE_POLICY.md` uses the same stale paths.
- `.ai/01_roadmap/current-phase.md` and `.ai/10_state/active_context.md` are stale relative to the actual git branch and newer roadmap state.
- Existing nested `AGENTS.md` files imply a much smaller repository footprint than the live codebase.

## 8. Audit Decision
Proceed with a bounded hierarchy:
- update root `AGENTS.md` minimally for truthfulness
- upgrade the six existing nested files
- create only the seven missing local contracts that correspond to real subsystem boundaries
- do not add `AGENTS.md` files below that level unless a future audit proves a persistent need
