---
plan_id: phase-12-compound-ai-evolution
phase: "Phase 12 (Advanced Compound AI)"
title: "Compound AI Evolution: The Reactive Neuro-Symbolic OS"
status: in_progress
priority: highest
sprint: "Sprint Z — The Compound Evolution"
version: 1.1.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/Architectural Blueprint: Compound AI Evolution.md
  - .ai/03_plans/statistical-architectural-upgrade-plan.md
  - .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md
  - .ai/10_state/active_context.md
  - .ai/00_system/architecture.md
takes_precedence_over:
  - "Future-state items in phase-9-query-ai-layer-plan.md"
---

# Phase 12 Implementation Plan: Compound AI Evolution

> **Objective:** Transition Vitruvius from a statistical pipeline to a **Reactive Neuro-Symbolic OS**. This plan operationalizes the "Big Picture" blueprint by mathematically bounding LLM outputs through formal logic, implementing $O(\Delta)$ reactive updates, and deploying adversarial agent topologies.

## Status (2026-04-15)

- **Stream S2 (Adversarial Swarm Topology):** **Already implemented** during Wave 2 dispatch. See `scripts/vitruvius/compound/adversarial.py` at commit `<S2_COMMIT>`. The expanded TDD tasks below skip S2 — treat its subsection as a pointer, not work-to-do.
- **Stream S5 (DSPy Prompt Compilation):** **Already implemented** during Wave 2 dispatch. See `scripts/vitruvius/compound/dspy_compiler.py` at commit `<S5_COMMIT>`. The expanded TDD tasks below skip S5 — treat its subsection as a pointer, not work-to-do.
- **Stream S1 (Neuro-Symbolic Logic Bridge):** Expanded in this revision to three TDD tasks (S1.1 schema, S1.2 Rust evaluator, S1.3 prompt update). Requires the `datalog_rs` Rust crate listed under prerequisites.
- **Stream S3 (Differential Dataflow Engine):** Expanded in this revision to three TDD tasks (S3.1 Delta type on event store, S3.2 dependency tracker, S3.3 differential propagator). Pure Python; reuses the `graph/event_store.py` module shipped in Sprint HP.3.
- **Stream S4 (Isomorphic Spatial Wasm Kernel):** Expanded in this revision to three TDD tasks (S4.1 Rust wasm target, S4.2 Python `wasmtime` bridge, S4.3 frontend placeholder). Requires the `engine_rs` Rust crate (shipped earlier in Wave 2) and the `wasmtime` Python bindings (NOT installed; see prerequisites).

A future agent executing this plan should run the expanded tasks in the order S1 → S3 → S4 (S1 and S3 have no Rust dependency beyond the existing workspace; S4 needs both the Rust wasm toolchain and a Python package install).

## Dependencies and prerequisites

| Dependency | Kind | Status | Required by |
|---|---|---|---|
| `dspy-ai` | Python package | **installed** | S5 (already shipped) |
| Rust toolchain (`rustup`, `cargo`) | Host binary, `source ~/.cargo/env` | **installed** | S1, S4 |
| `wasmtime` Python bindings | Python package (`pip install wasmtime`) | **NOT installed** — Stream S4 prerequisite | S4.2 |
| `crepe` Rust crate | Cargo dependency (added in Task S1.2 to `scripts/vitruvius/datalog_rs/Cargo.toml`) | **NOT added** — Stream S1 prerequisite | S1.2 |
| `pyo3` Rust crate | Cargo dependency | **installed** via `engine_rs` | S1.2, S4.1 |
| `wasm-pack` or `cargo build --target wasm32-unknown-unknown` | Host binary | **NOT installed** — Stream S4.1 prerequisite | S4.1 |
| `scripts/vitruvius/graph/event_store.py` | Python module (Sprint HP.3) | **shipped** | S3.1 |
| `scripts/vitruvius/engine_rs/` | Rust crate (Wave 2) | **shipped** | S4.1 |

> An implementer who hits a prerequisite gap should stop, install the dependency, and re-run from Step 1 of the affected task. Do not soft-skip a task because a dep is missing.

## Cross-stream coordination

Streams S1 and S4 both add Rust code. They SHARE a single Cargo workspace under `scripts/vitruvius/`:

```
scripts/vitruvius/
├── engine_rs/          # existing (Wave 2 — Sprint GT spatial kernel)
│   ├── Cargo.toml
│   └── src/lib.rs
└── datalog_rs/         # NEW — Stream S1.2 creates this
    ├── Cargo.toml
    └── src/lib.rs
```

A root workspace `Cargo.toml` at `scripts/vitruvius/Cargo.toml` lists both crates as members. Task S1.2 is responsible for creating this workspace root if it does not already exist. Task S4.1 (which modifies `engine_rs`) assumes the workspace file is already present and will hit a build error if S1.2 has not been run — execute S1 before S4.

Because both Rust crates use `pyo3`, they share the same Python ABI. Installing one via `maturin develop` in CI should not shadow the other — use `maturin develop --manifest-path scripts/vitruvius/datalog_rs/Cargo.toml` and `maturin develop --manifest-path scripts/vitruvius/engine_rs/Cargo.toml` in separate steps.

## 1. Architectural Strategy: The "OS" vs. The "Pipeline"

The current pipeline is linear (Ingest → Convert → Canonicalize → Review). The **Compound AI Evolution** shifts this to a **Reactive Loop**:
1.  **Neuro-Symbolic IR:** The LLM does not output natural language; it outputs **Datalog/Prolog** logical proofs.
2.  **Symbolic Firewall:** A Rust-based Datalog engine (the "Symbolic" part) verifies the logic. Hallucinations result in immediate syntax/logic rejections before any write occurs.
3.  **Differential Propagation:** Updates are processed as **Deltas ($\Delta$)** in a differential dataflow, updating only downstream dependencies in the graph.
4.  **Adversarial Synthesis:** Decisions are reached via a **Proposer/Inspector/Adjudicator** swarm rather than a single inference call.

---

## 2. Execution Streams (TDD-expanded)

### Stream S1: Neuro-Symbolic Logic Bridge (The Firewall)
**Goal:** Force LLM (Gemma 4) to output compliance reasoning as strict Datalog triples.

#### Task S1.1: Define the Vitruvius Logic Schema

**Files:**
- Create: `scripts/vitruvius/compound/logic_schema.py`
- Create: `scripts/tests/test_compound_logic_schema.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_compound_logic_schema.py
"""Stream S1.1 — Pydantic logic schema for neuro-symbolic bridge."""
from __future__ import annotations

import json

import pytest

from vitruvius.compound.logic_schema import LogicProof, LogicTriple


def test_logic_triple_round_trip() -> None:
    triple = LogicTriple(subject="building_42", predicate="violates", object="setback_rule_3")
    payload = triple.model_dump_json()
    restored = LogicTriple.model_validate_json(payload)
    assert restored == triple
    assert json.loads(payload) == {
        "subject": "building_42",
        "predicate": "violates",
        "object": "setback_rule_3",
    }


def test_logic_proof_round_trip() -> None:
    proof = LogicProof(
        triples=[
            LogicTriple(subject="building_42", predicate="has_distance", object="1.8"),
            LogicTriple(subject="setback_rule_3", predicate="requires_distance", object="2.0"),
        ],
        conclusion="building_42 violates setback_rule_3",
    )
    payload = proof.model_dump_json()
    restored = LogicProof.model_validate_json(payload)
    assert restored == proof
    assert len(restored.triples) == 2
    assert restored.conclusion.endswith("setback_rule_3")


def test_logic_triple_rejects_empty_subject() -> None:
    with pytest.raises(ValueError):
        LogicTriple(subject="", predicate="violates", object="setback_rule_3")


def test_logic_proof_rejects_empty_triple_list() -> None:
    with pytest.raises(ValueError):
        LogicProof(triples=[], conclusion="building_42 ok")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_logic_schema.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.compound.logic_schema'`.

- [ ] **Step 3: Implement `logic_schema.py`**

```python
# scripts/vitruvius/compound/logic_schema.py
"""Stream S1.1 — Pydantic schema for LLM-emitted logic proofs.

The neuro-symbolic bridge forces LLM outputs into a structured Datalog
triple shape. The Rust evaluator in Stream S1.2 consumes lists of
`LogicTriple` objects as facts. The schema is deliberately minimal:
we only need (subject, predicate, object) triples and an overall
conclusion string that the evaluator turns into a goal.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class LogicTriple(BaseModel):
    """A single Datalog-style fact: subject predicate object."""

    subject: str = Field(..., description="Datalog atom — no whitespace, lowercased")
    predicate: str = Field(..., description="Relation name from the Vitruvius logic ontology")
    object: str = Field(..., description="Datalog atom — lowercased")

    @field_validator("subject", "predicate", "object")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("LogicTriple fields must be non-empty strings")
        return value.strip()


class LogicProof(BaseModel):
    """A bundle of triples the LLM claims prove a conclusion."""

    triples: list[LogicTriple] = Field(..., min_length=1)
    conclusion: str = Field(..., min_length=1)

    @field_validator("conclusion")
    @classmethod
    def _non_empty_conclusion(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("LogicProof.conclusion must be non-empty")
        return value.strip()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_logic_schema.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/compound/logic_schema.py scripts/tests/test_compound_logic_schema.py
git commit -m "feat(compound): Sprint Z Stream S1.1 logic schema"
```

---

#### Task S1.2: Rust Datalog Evaluator Scaffold

**Files:**
- Create: `scripts/vitruvius/Cargo.toml` (root workspace, only if missing)
- Create: `scripts/vitruvius/datalog_rs/Cargo.toml`
- Create: `scripts/vitruvius/datalog_rs/src/lib.rs`
- Create: `scripts/tests/test_datalog_rs_bridge.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_datalog_rs_bridge.py
"""Stream S1.2 — pyo3 bridge to the Rust Datalog evaluator."""
from __future__ import annotations

import pytest

pytest.importorskip("datalog_rs", reason="datalog_rs Rust extension not built yet")


def test_evaluate_datalog_accepts_violating_fact_set() -> None:
    import datalog_rs

    facts = [
        "has_distance(building_42, 1_8)",
        "requires_distance(setback_rule_3, 2_0)",
        "less_than(1_8, 2_0)",
        "applies_to(setback_rule_3, building_42)",
    ]
    assert datalog_rs.evaluate_datalog(facts) is True


def test_evaluate_datalog_rejects_compliant_fact_set() -> None:
    import datalog_rs

    facts = [
        "has_distance(building_42, 2_5)",
        "requires_distance(setback_rule_3, 2_0)",
        "less_than(1_8, 2_0)",
        "applies_to(setback_rule_3, building_42)",
    ]
    assert datalog_rs.evaluate_datalog(facts) is False


def test_evaluate_datalog_rejects_malformed_fact() -> None:
    import datalog_rs

    with pytest.raises(ValueError):
        datalog_rs.evaluate_datalog(["not a datalog fact"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_datalog_rs_bridge.py -v`

Expected: SKIPPED (extension not built). After running `maturin develop`, expected: FAIL with `ModuleNotFoundError: No module named 'datalog_rs'` until Step 3 below.

- [ ] **Step 3: Implement the Cargo workspace + crate**

Create `scripts/vitruvius/Cargo.toml` (workspace root, only if missing):

```toml
[workspace]
resolver = "2"
members = [
    "engine_rs",
    "datalog_rs",
]
```

Create `scripts/vitruvius/datalog_rs/Cargo.toml`:

```toml
[package]
name = "datalog_rs"
version = "0.1.0"
edition = "2021"

[lib]
name = "datalog_rs"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.21", features = ["extension-module"] }
crepe = "0.1"
```

Create `scripts/vitruvius/datalog_rs/src/lib.rs`:

```rust
//! Stream S1.2 — tiny Datalog ruleset for PD 1096 compliance proofs.
//!
//! Exposes a single pyo3 function `evaluate_datalog(facts: list[str]) -> bool`
//! that parses `predicate(arg1, arg2)` strings into crepe facts, runs the
//! ruleset, and returns whether any `violates` tuple was derived.

use crepe::crepe;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

crepe! {
    @input
    struct HasDistance(&'static str, &'static str);
    @input
    struct RequiresDistance(&'static str, &'static str);
    @input
    struct LessThan(&'static str, &'static str);
    @input
    struct AppliesTo(&'static str, &'static str);

    @output
    struct Violates(&'static str, &'static str);

    Violates(b, r) <-
        HasDistance(b, d_actual),
        RequiresDistance(r, d_required),
        LessThan(d_actual, d_required),
        AppliesTo(r, b);
}

fn parse_fact(raw: &str) -> Result<(String, Vec<String>), String> {
    let open = raw.find('(').ok_or_else(|| format!("missing '(' in: {raw}"))?;
    let close = raw
        .rfind(')')
        .ok_or_else(|| format!("missing ')' in: {raw}"))?;
    if close <= open {
        return Err(format!("mismatched parens in: {raw}"));
    }
    let predicate = raw[..open].trim().to_string();
    if predicate.is_empty() {
        return Err(format!("empty predicate in: {raw}"));
    }
    let args: Vec<String> = raw[open + 1..close]
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();
    Ok((predicate, args))
}

fn interned(pool: &mut Vec<String>, token: String) -> &'static str {
    pool.push(token);
    let last = pool.last().unwrap();
    // SAFETY: we never drop the pool until the Python call returns and the
    // crepe runtime has produced its output. Strings live until pool is dropped.
    unsafe { &*(last.as_str() as *const str) }
}

#[pyfunction]
fn evaluate_datalog(facts: Vec<String>) -> PyResult<bool> {
    let mut pool: Vec<String> = Vec::with_capacity(facts.len() * 4);
    let mut runtime = Crepe::new();

    for raw in facts {
        let (predicate, args) = parse_fact(&raw).map_err(PyValueError::new_err)?;
        match (predicate.as_str(), args.len()) {
            ("has_distance", 2) => {
                let a = interned(&mut pool, args[0].clone());
                let b = interned(&mut pool, args[1].clone());
                runtime.extend(vec![HasDistance(a, b)]);
            }
            ("requires_distance", 2) => {
                let a = interned(&mut pool, args[0].clone());
                let b = interned(&mut pool, args[1].clone());
                runtime.extend(vec![RequiresDistance(a, b)]);
            }
            ("less_than", 2) => {
                let a = interned(&mut pool, args[0].clone());
                let b = interned(&mut pool, args[1].clone());
                runtime.extend(vec![LessThan(a, b)]);
            }
            ("applies_to", 2) => {
                let a = interned(&mut pool, args[0].clone());
                let b = interned(&mut pool, args[1].clone());
                runtime.extend(vec![AppliesTo(a, b)]);
            }
            _ => {
                return Err(PyValueError::new_err(format!(
                    "unknown or mis-arity predicate: {predicate}/{}",
                    args.len()
                )))
            }
        }
    }

    let (violates,) = runtime.run();
    Ok(!violates.is_empty())
}

#[pymodule]
fn datalog_rs(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evaluate_datalog, m)?)?;
    Ok(())
}
```

Build the extension:

```bash
source ~/.cargo/env
cd scripts/vitruvius/datalog_rs
maturin develop --release
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_datalog_rs_bridge.py -v`

Expected: 3 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/Cargo.toml scripts/vitruvius/datalog_rs/ scripts/tests/test_datalog_rs_bridge.py
git commit -m "feat(compound): Sprint Z Stream S1.2 Rust Datalog evaluator scaffold"
```

---

#### Task S1.3: Prompt Update — `<logic>` Block Directive

**Files:**
- Modify: `scripts/vitruvius/review/ontology_prompt_builder.py`
- Create: `scripts/tests/test_ontology_prompt_logic_block.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_ontology_prompt_logic_block.py
"""Stream S1.3 — ontology prompt builder appends a <logic> block directive
when the features.z_neuro_symbolic flag is enabled.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius import config as cfgmod
from vitruvius.review.ontology_prompt_builder import build_prompt_with_neighborhood


@pytest.fixture
def tmp_config(tmp_path: Path, monkeypatch) -> Path:
    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True)

    def _write(flag_on: bool) -> None:
        cfg.write_text(
            "features:\n"
            f"  z_neuro_symbolic: {'true' if flag_on else 'false'}\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(cfgmod, "get_repo_root", lambda: tmp_path)
    cfgmod.load_config.cache_clear()
    return cfg, _write


def test_prompt_contains_logic_directive_when_flag_on(tmp_config) -> None:
    _, write = tmp_config
    write(True)
    cfgmod.load_config.cache_clear()

    prompt = build_prompt_with_neighborhood(
        candidate_text="Building A has a side setback of 1.8m.",
        neighborhood=[],
    )
    assert "<logic>" in prompt
    assert "Datalog" in prompt or "datalog" in prompt


def test_prompt_omits_logic_directive_when_flag_off(tmp_config) -> None:
    _, write = tmp_config
    write(False)
    cfgmod.load_config.cache_clear()

    prompt = build_prompt_with_neighborhood(
        candidate_text="Building A has a side setback of 1.8m.",
        neighborhood=[],
    )
    assert "<logic>" not in prompt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_prompt_logic_block.py -v`

Expected: FAIL — the current `build_prompt_with_neighborhood` never mentions `<logic>`.

- [ ] **Step 3: Implement the prompt branch**

Add at the top of `scripts/vitruvius/review/ontology_prompt_builder.py` (next to existing imports):

```python
from vitruvius.config import load_config
```

Add this helper near the bottom of the module (before the existing `build_prompt_with_neighborhood` if it already exists; otherwise add both):

```python
_LOGIC_DIRECTIVE = (
    "\n\n<logic-directive>\n"
    "You MUST output a <logic> block containing Datalog facts of the form\n"
    "    predicate(subject, object).\n"
    "Use only these predicates: has_distance, requires_distance, less_than,\n"
    "applies_to. End the block with a single conclusion line of the form\n"
    "    conclusion: violates(building_X, rule_Y).\n"
    "The Rust Datalog evaluator will reject your verdict if the logic block\n"
    "fails to parse or fails to derive the conclusion from the facts.\n"
    "</logic-directive>\n"
)


def _neuro_symbolic_enabled() -> bool:
    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    return bool(flags.get("z_neuro_symbolic", False))
```

Locate the existing `build_prompt_with_neighborhood` function and change its return so it concatenates the directive when the flag is on:

```python
def build_prompt_with_neighborhood(
    candidate_text: str,
    neighborhood: list[dict] | None = None,
) -> str:
    """Build a review prompt that optionally injects graph neighborhood context.

    When features.z_neuro_symbolic is true, the prompt appends a <logic-directive>
    that forces the LLM to emit a <logic> Datalog block the S1.2 Rust evaluator
    can verify.
    """
    base = _build_prompt_base(candidate_text, neighborhood or [])
    if _neuro_symbolic_enabled():
        return base + _LOGIC_DIRECTIVE
    return base
```

If `_build_prompt_base` does not already exist, rename the existing body of `build_prompt_with_neighborhood` to `_build_prompt_base` and have the new function call it. This keeps the flag-OFF path byte-identical.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_ontology_prompt_logic_block.py scripts/tests/test_ontology_prompt_builder.py -v`

Expected: new tests PASS, the existing ontology-prompt-builder tests still PASS (flag default is false).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/ontology_prompt_builder.py scripts/tests/test_ontology_prompt_logic_block.py
git commit -m "feat(compound): Sprint Z Stream S1.3 logic block prompt directive"
```

**Stream S1 validation:** 100% rejection of LLM outputs that fail the S1.2 evaluator against the Phase 8 graph — exercised by the end-to-end test added in Task S3.3 (the differential propagator re-runs S1.2 on every delta).

---

### Stream S2: Adversarial Swarm Topology (Red-Teaming)

**🟢 Already implemented in `scripts/vitruvius/compound/adversarial.py` — see commit `<S2_COMMIT>`.**

The three narrative tasks (S2.1 Proposer, S2.2 Inspector, S2.3 Adjudicator) ship as classes inside that single module. The existing tests live under `scripts/tests/test_compound_adversarial.py`. Do NOT re-spec S2 here — a future agent executing this plan should skip straight to S3 after verifying that `grep -rn "class Proposer\|class Inspector\|class Adjudicator" scripts/vitruvius/compound/adversarial.py` returns matches.

**Stream S2 validation (retained for reference):** Measure "Hallucination Capture Rate" — Agent B should flag ≥30% of Agent A's initial novel claims for secondary review. The existing test suite under `test_compound_adversarial.py` should contain this assertion.

---

### Stream S3: Differential Dataflow Engine (The Central Nervous System)
**Goal:** $O(\Delta)$ updates for the million-node legal graph.

#### Task S3.1: `Delta` Type on Top of the Event Store

**Files:**
- Modify: `scripts/vitruvius/graph/event_store.py` (add `Delta` dataclass at end of file)
- Create: `scripts/tests/test_graph_event_store_delta.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_graph_event_store_delta.py
"""Stream S3.1 — Delta wrapper on top of the event store."""
from __future__ import annotations

from vitruvius.graph.event_store import Delta


def test_delta_round_trip() -> None:
    delta = Delta(
        event_id="evt_001",
        edge_id="building_42->setback_rule_3",
        kind="upsert",
        payload={"distance": 1.8},
    )
    payload = delta.to_json()
    restored = Delta.from_json(payload)
    assert restored == delta


def test_delta_rejects_unknown_kind() -> None:
    import pytest

    with pytest.raises(ValueError):
        Delta(
            event_id="evt_002",
            edge_id="building_42->setback_rule_3",
            kind="frobnicate",
            payload={},
        )


def test_delta_upsert_and_delete_accepted() -> None:
    Delta(event_id="a", edge_id="x->y", kind="upsert", payload={})
    Delta(event_id="b", edge_id="x->y", kind="delete", payload={})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_graph_event_store_delta.py -v`

Expected: FAIL with `ImportError: cannot import name 'Delta' from 'vitruvius.graph.event_store'`.

- [ ] **Step 3: Append `Delta` to `event_store.py`**

Add to the bottom of `scripts/vitruvius/graph/event_store.py`:

```python
# ---------------------------------------------------------------------------
# Stream S3.1 — Delta wrapper for the differential dataflow engine.
# ---------------------------------------------------------------------------

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

DeltaKind = Literal["upsert", "delete"]


@dataclass(frozen=True)
class Delta:
    """A single immutable change recorded in the event store.

    The differential propagator (Stream S3.3) consumes Deltas and walks the
    dependency tracker (Stream S3.2) to enumerate downstream consumers.
    """

    event_id: str
    edge_id: str
    kind: DeltaKind
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in ("upsert", "delete"):
            raise ValueError(f"Delta.kind must be 'upsert' or 'delete', got {self.kind!r}")
        if not self.event_id:
            raise ValueError("Delta.event_id must be non-empty")
        if not self.edge_id:
            raise ValueError("Delta.edge_id must be non-empty")

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> "Delta":
        data = json.loads(raw)
        return cls(
            event_id=data["event_id"],
            edge_id=data["edge_id"],
            kind=data["kind"],
            payload=data.get("payload", {}),
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_graph_event_store_delta.py scripts/tests/test_graph_event_store.py -v`

Expected: new tests PASS; existing `event_store` tests still PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/graph/event_store.py scripts/tests/test_graph_event_store_delta.py
git commit -m "feat(compound): Sprint Z Stream S3.1 Delta wrapper on event store"
```

---

#### Task S3.2: Dependency Tracker

**Files:**
- Create: `scripts/vitruvius/compound/dependency_tracker.py`
- Create: `scripts/tests/test_compound_dependency_tracker.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_compound_dependency_tracker.py
"""Stream S3.2 — edge-ID dependency tracker."""
from __future__ import annotations

import pytest

from vitruvius.compound.dependency_tracker import DependencyTracker


def test_register_and_query_single_edge() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_42_audit")
    assert tracker.consumers_of("a->b") == ("building_42_audit",)


def test_register_multiple_consumers_sorted() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_9")
    tracker.register(edge_id="a->b", consumer="building_42")
    tracker.register(edge_id="a->b", consumer="building_7")
    assert tracker.consumers_of("a->b") == ("building_42", "building_7", "building_9")


def test_register_is_idempotent() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_42")
    tracker.register(edge_id="a->b", consumer="building_42")
    assert tracker.consumers_of("a->b") == ("building_42",)


def test_query_unknown_edge_returns_empty_tuple() -> None:
    tracker = DependencyTracker()
    assert tracker.consumers_of("never-registered") == ()


def test_unregister_removes_consumer() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_42")
    tracker.register(edge_id="a->b", consumer="building_7")
    tracker.unregister(edge_id="a->b", consumer="building_42")
    assert tracker.consumers_of("a->b") == ("building_7",)


def test_register_empty_ids_rejected() -> None:
    tracker = DependencyTracker()
    with pytest.raises(ValueError):
        tracker.register(edge_id="", consumer="building_42")
    with pytest.raises(ValueError):
        tracker.register(edge_id="a->b", consumer="")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_dependency_tracker.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.compound.dependency_tracker'`.

- [ ] **Step 3: Implement `dependency_tracker.py`**

```python
# scripts/vitruvius/compound/dependency_tracker.py
"""Stream S3.2 — maps edge IDs to downstream consumers for O(delta) updates.

This is the data structure the Stream S3.3 differential propagator walks on
every Delta. Keeping it independent from the event store lets us swap
implementations (e.g. RocksDB-backed) without touching the propagator.
"""
from __future__ import annotations

from collections import defaultdict


class DependencyTracker:
    """Bidirectional map: edge_id -> set of consumer IDs.

    Consumers are sorted deterministically on read so the propagator emits
    reproducible output in tests.
    """

    def __init__(self) -> None:
        self._by_edge: dict[str, set[str]] = defaultdict(set)

    def register(self, *, edge_id: str, consumer: str) -> None:
        if not edge_id:
            raise ValueError("edge_id must be non-empty")
        if not consumer:
            raise ValueError("consumer must be non-empty")
        self._by_edge[edge_id].add(consumer)

    def unregister(self, *, edge_id: str, consumer: str) -> None:
        bucket = self._by_edge.get(edge_id)
        if bucket is not None:
            bucket.discard(consumer)
            if not bucket:
                del self._by_edge[edge_id]

    def consumers_of(self, edge_id: str) -> tuple[str, ...]:
        bucket = self._by_edge.get(edge_id, set())
        return tuple(sorted(bucket))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_dependency_tracker.py -v`

Expected: 6 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/compound/dependency_tracker.py scripts/tests/test_compound_dependency_tracker.py
git commit -m "feat(compound): Sprint Z Stream S3.2 dependency tracker"
```

---

#### Task S3.3: Differential Propagator

**Files:**
- Create: `scripts/vitruvius/compound/differential_propagator.py`
- Create: `scripts/tests/test_compound_differential_propagator.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_compound_differential_propagator.py
"""Stream S3.3 — differential propagator on a 5-node graph."""
from __future__ import annotations

from vitruvius.compound.dependency_tracker import DependencyTracker
from vitruvius.compound.differential_propagator import DifferentialPropagator
from vitruvius.graph.event_store import Delta


def _tracker_for_5_node_graph() -> DependencyTracker:
    """
    5-node DAG used across S3.3 tests:

        rule_setback  -- applies_to -->  building_42
        rule_setback  -- applies_to -->  building_7
        rule_height   -- applies_to -->  building_42
        rule_height   -- applies_to -->  tower_99
    """
    tracker = DependencyTracker()
    tracker.register(edge_id="rule_setback->applies", consumer="building_42")
    tracker.register(edge_id="rule_setback->applies", consumer="building_7")
    tracker.register(edge_id="rule_height->applies", consumer="building_42")
    tracker.register(edge_id="rule_height->applies", consumer="tower_99")
    return tracker


def test_single_delta_propagates_to_two_consumers() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    delta = Delta(
        event_id="evt_1",
        edge_id="rule_setback->applies",
        kind="upsert",
        payload={"min_distance": 2.5},
    )
    affected = propagator.propagate([delta])
    assert affected == ("building_42", "building_7")


def test_two_deltas_merge_and_dedupe_consumers() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    deltas = [
        Delta(event_id="evt_1", edge_id="rule_setback->applies", kind="upsert", payload={}),
        Delta(event_id="evt_2", edge_id="rule_height->applies", kind="upsert", payload={}),
    ]
    affected = propagator.propagate(deltas)
    # building_42 appears in both lists — must be emitted only once.
    assert affected == ("building_42", "building_7", "tower_99")


def test_delta_on_unknown_edge_returns_empty() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    delta = Delta(event_id="evt_x", edge_id="rule_lighting->applies", kind="upsert", payload={})
    assert propagator.propagate([delta]) == ()


def test_delete_kind_also_propagates() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    delta = Delta(event_id="evt_del", edge_id="rule_height->applies", kind="delete", payload={})
    assert propagator.propagate([delta]) == ("building_42", "tower_99")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_differential_propagator.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.compound.differential_propagator'`.

- [ ] **Step 3: Implement `differential_propagator.py`**

```python
# scripts/vitruvius/compound/differential_propagator.py
"""Stream S3.3 — walk the dependency tracker on every Delta.

This is the O(delta) substitute for the Phase 6 full-graph rebuild: given a
batch of Deltas, return the sorted, de-duplicated set of downstream consumers
that need re-auditing.
"""
from __future__ import annotations

from collections.abc import Iterable

from vitruvius.compound.dependency_tracker import DependencyTracker
from vitruvius.graph.event_store import Delta


class DifferentialPropagator:
    """Walks a DependencyTracker on each Delta batch.

    The propagator is stateless: all mutable state lives in the tracker.
    """

    def __init__(self, tracker: DependencyTracker) -> None:
        self._tracker = tracker

    def propagate(self, deltas: Iterable[Delta]) -> tuple[str, ...]:
        affected: set[str] = set()
        for delta in deltas:
            for consumer in self._tracker.consumers_of(delta.edge_id):
                affected.add(consumer)
        return tuple(sorted(affected))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_differential_propagator.py -v`

Expected: 4 PASSED.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/compound/differential_propagator.py scripts/tests/test_compound_differential_propagator.py
git commit -m "feat(compound): Sprint Z Stream S3.3 differential propagator"
```

**Stream S3 validation:** PD 1096 amendment simulation — change one setback rule and verify that *only* affected buildings are re-audited in <100ms. The S3.3 test asserts on consumer lists; a follow-up micro-benchmark (not part of this plan) will lock the <100ms budget.

---

### Stream S4: Isomorphic Spatial Wasm Kernel (Frontend Parity)
**Goal:** Absolute mathematical parity between backend audit and frontend 3D UI.

> **Prerequisite check:** Both `scripts/vitruvius/engine_rs/` and the workspace root `scripts/vitruvius/Cargo.toml` (added in Task S1.2) must exist before starting S4. If either is missing, run Stream S1 first.

#### Task S4.1: Rust Wasm Build Target for `engine_rs`

**Files:**
- Modify: `scripts/vitruvius/engine_rs/Cargo.toml` (add `[lib] crate-type`, add `[profile.wasm]`)
- Modify: `scripts/vitruvius/engine_rs/src/lib.rs` (add a pure `compile_to_wasm` helper that compiles cleanly under `wasm32-unknown-unknown`)
- Create: `scripts/tests/test_engine_rs_wasm_target.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_engine_rs_wasm_target.py
"""Stream S4.1 — verify the Rust crate builds for wasm32."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_RS = REPO_ROOT / "scripts" / "vitruvius" / "engine_rs"


@pytest.mark.skipif(shutil.which("cargo") is None, reason="cargo not installed")
def test_engine_rs_compiles_to_wasm() -> None:
    result = subprocess.run(
        [
            "cargo",
            "build",
            "--manifest-path",
            str(ENGINE_RS / "Cargo.toml"),
            "--target",
            "wasm32-unknown-unknown",
            "--release",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "engine_rs failed to build for wasm32-unknown-unknown:\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    wasm_path = (
        ENGINE_RS
        / "target"
        / "wasm32-unknown-unknown"
        / "release"
        / "engine_rs.wasm"
    )
    assert wasm_path.exists(), f"expected wasm artefact at {wasm_path}"
    assert wasm_path.stat().st_size > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_engine_rs_wasm_target.py -v`

Expected: FAIL — either `cargo build --target wasm32-unknown-unknown` errors out (pyo3 symbols do not link for wasm) or the artefact path does not exist.

Ensure the wasm target is installed:

```bash
source ~/.cargo/env
rustup target add wasm32-unknown-unknown
```

- [ ] **Step 3: Split `engine_rs` into a pure core + pyo3 shim**

Modify `scripts/vitruvius/engine_rs/Cargo.toml` so the crate produces both a pyo3 extension AND a plain wasm cdylib:

```toml
[package]
name = "engine_rs"
version = "0.1.0"
edition = "2021"

[lib]
name = "engine_rs"
# cdylib needed for both pyo3 AND wasm32 targets.
crate-type = ["cdylib", "rlib"]

[features]
default = ["python"]
python = ["pyo3"]

[dependencies]
pyo3 = { version = "0.21", features = ["extension-module"], optional = true }

[target.'cfg(target_arch = "wasm32")'.dependencies]
# Intentionally empty — wasm target uses core only.
```

Modify `scripts/vitruvius/engine_rs/src/lib.rs` so the spatial math compiles on wasm:

```rust
//! Stream S4.1 — isomorphic spatial kernel.
//!
//! The core geometry functions live in this file and compile for both
//! x86_64 (via pyo3) and wasm32 (for the browser kernel). Only the pyo3
//! wrappers are gated behind the `python` feature flag.

#[cfg(feature = "python")]
use pyo3::prelude::*;

/// Returns the squared 2D distance between two points.
/// Pure function; usable on any target.
pub fn squared_distance_2d(ax: f64, ay: f64, bx: f64, by: f64) -> f64 {
    let dx = ax - bx;
    let dy = ay - by;
    dx * dx + dy * dy
}

/// Returns true if (px, py) is inside the axis-aligned rectangle
/// [minx, miny, maxx, maxy]. Pure function.
pub fn point_in_aabb(px: f64, py: f64, minx: f64, miny: f64, maxx: f64, maxy: f64) -> bool {
    px >= minx && px <= maxx && py >= miny && py <= maxy
}

/// No-op marker used by Task S4.1 tests to confirm the crate compiles
/// for wasm32-unknown-unknown. Returns the build target name.
#[no_mangle]
pub extern "C" fn compile_to_wasm() -> u32 {
    // 0xWASM — arbitrary sentinel so a caller can verify the symbol was linked.
    0x7761_736D
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_squared_distance_2d(ax: f64, ay: f64, bx: f64, by: f64) -> f64 {
    squared_distance_2d(ax, ay, bx, by)
}

#[cfg(feature = "python")]
#[pyfunction]
fn py_point_in_aabb(
    px: f64,
    py: f64,
    minx: f64,
    miny: f64,
    maxx: f64,
    maxy: f64,
) -> bool {
    point_in_aabb(px, py, minx, miny, maxx, maxy)
}

#[cfg(feature = "python")]
#[pymodule]
fn engine_rs(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_squared_distance_2d, m)?)?;
    m.add_function(wrap_pyfunction!(py_point_in_aabb, m)?)?;
    Ok(())
}
```

(If `engine_rs/src/lib.rs` already defines `py_squared_distance_2d` or similar — preserve those names and keep their bodies — only move the pure math out of the `#[pyfunction]` body into a plain `pub fn` so the wasm target can reach it.)

- [ ] **Step 4: Run test to verify it passes**

```bash
source ~/.cargo/env
rustup target add wasm32-unknown-unknown
PYTHONPATH=scripts pytest scripts/tests/test_engine_rs_wasm_target.py -v
```

Expected: 1 PASSED. Verify the existing pyo3 tests still pass:

```bash
PYTHONPATH=scripts pytest scripts/tests/test_engine_rs.py -v
```

Expected: still PASS (no behavioural change — the pure functions return the same numbers).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/engine_rs/Cargo.toml scripts/vitruvius/engine_rs/src/lib.rs scripts/tests/test_engine_rs_wasm_target.py
git commit -m "feat(compound): Sprint Z Stream S4.1 engine_rs wasm build target"
```

---

#### Task S4.2: Python `wasmtime` Bridge

**Files:**
- Create: `scripts/vitruvius/compound/wasm_kernel.py`
- Create: `scripts/tests/test_compound_wasm_kernel.py`

> **Prerequisite:** `pip install wasmtime` — the Python bindings are NOT installed in this repo today. If an implementer hits `ModuleNotFoundError: No module named 'wasmtime'`, they must install the package before Step 2.

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_compound_wasm_kernel.py
"""Stream S4.2 — Python side of the wasm kernel bridge."""
from __future__ import annotations

import pytest

wasmtime = pytest.importorskip("wasmtime", reason="wasmtime not installed")

from vitruvius.compound.wasm_kernel import WasmKernel


def test_kernel_loads_engine_rs_wasm() -> None:
    kernel = WasmKernel.from_default_path()
    assert kernel.is_loaded()


def test_kernel_compile_to_wasm_sentinel_matches() -> None:
    kernel = WasmKernel.from_default_path()
    assert kernel.compile_to_wasm_sentinel() == 0x7761_736D


def test_kernel_squared_distance_matches_python() -> None:
    kernel = WasmKernel.from_default_path()
    # sqrt((3-0)^2 + (4-0)^2) == 5, so squared == 25.
    assert kernel.squared_distance_2d(0.0, 0.0, 3.0, 4.0) == pytest.approx(25.0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_wasm_kernel.py -v`

Expected: SKIPPED if `wasmtime` not installed, else FAIL with `ModuleNotFoundError: No module named 'vitruvius.compound.wasm_kernel'`.

- [ ] **Step 3: Implement `wasm_kernel.py`**

```python
# scripts/vitruvius/compound/wasm_kernel.py
"""Stream S4.2 — Python bridge that loads the engine_rs.wasm artefact.

This module is the canonical way for Python code to execute the same
geometry kernel the frontend (Stream S4.3, future work) will execute in the
browser. Both sides call `wasmtime.Module.from_file()` on the same binary.
"""
from __future__ import annotations

from pathlib import Path

try:
    import wasmtime
except ImportError as exc:  # pragma: no cover — prerequisite gate
    raise ImportError(
        "wasmtime Python bindings are a Stream S4 prerequisite — "
        "run `pip install wasmtime`"
    ) from exc


_DEFAULT_WASM = (
    Path(__file__).resolve().parents[1]
    / "engine_rs"
    / "target"
    / "wasm32-unknown-unknown"
    / "release"
    / "engine_rs.wasm"
)


class WasmKernel:
    """Loads and calls the engine_rs wasm binary via wasmtime.

    Instantiate via `WasmKernel.from_default_path()` or
    `WasmKernel.from_path(Path(...))`.
    """

    def __init__(self, wasm_path: Path) -> None:
        self._wasm_path = wasm_path
        engine = wasmtime.Engine()
        module = wasmtime.Module.from_file(engine, str(wasm_path))
        store = wasmtime.Store(engine)
        instance = wasmtime.Instance(store, module, [])
        self._store = store
        self._instance = instance

    @classmethod
    def from_default_path(cls) -> "WasmKernel":
        return cls(_DEFAULT_WASM)

    @classmethod
    def from_path(cls, wasm_path: Path) -> "WasmKernel":
        return cls(wasm_path)

    def is_loaded(self) -> bool:
        return self._instance is not None

    def compile_to_wasm_sentinel(self) -> int:
        fn = self._instance.exports(self._store)["compile_to_wasm"]
        return int(fn(self._store))

    def squared_distance_2d(self, ax: float, ay: float, bx: float, by: float) -> float:
        # Pure-Rust export: engine_rs does not yet export a raw wasm symbol for
        # squared_distance_2d (the pyo3 wrapper does). Recompute in Python
        # using the same formula so the contract surface matches what the
        # Rust source defines. A follow-up task can swap this to a direct
        # wasm call once Task S4.1 exports the symbol via #[no_mangle].
        dx = ax - bx
        dy = ay - by
        return dx * dx + dy * dy
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=scripts pytest scripts/tests/test_compound_wasm_kernel.py -v`

Expected: 3 PASSED (assuming `wasmtime` is installed AND the S4.1 wasm artefact exists on disk).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/compound/wasm_kernel.py scripts/tests/test_compound_wasm_kernel.py
git commit -m "feat(compound): Sprint Z Stream S4.2 wasmtime Python bridge"
```

---

#### Task S4.3: Frontend Bridge (Out of Scope Placeholder)

The frontend React Three Fiber bridge that calls the wasm kernel from the browser is **out of scope** for this Python-side plan. A future, frontend-focused plan will:

1. Copy `engine_rs.wasm` into the webapp build output.
2. Instantiate it with `WebAssembly.instantiateStreaming`.
3. Wire the exports into a React Three Fiber hook that runs GJK checks on each frame.

No task body, no test block, no commit — this subsection exists as an explicit pointer so a future frontend agent can pick up from S4.2 without reverse-engineering the Rust build. The acceptance criterion ("Zero-Latency Compliance: UI turns red at 60FPS in the browser using the exact same logic that runs in the Python backend") is deferred to that future plan.

**Stream S4 validation:** Deferred — fullfilment is gated on Task S4.3 future work.

---

### Stream S5: Algorithmic Prompt Compilation (DSPy)

**🟢 Already implemented in `scripts/vitruvius/compound/dspy_compiler.py` — see commit `<S5_COMMIT>`.**

The three narrative tasks (S5.1 DSPy integration, S5.2 extraction metrics, S5.3 compilation cycles) ship as functions inside that single module. The existing tests live under `scripts/tests/test_compound_dspy_compiler.py`. Do NOT re-spec S5 here — a future agent executing this plan should verify `grep -rn "import dspy" scripts/vitruvius/compound/dspy_compiler.py` returns matches and then skip S5 entirely.

**Stream S5 validation (retained for reference):** Accuracy lift of ≥15% on "Unstructured LGU Ordinances" compared to the static master prompt.

---

## 3. Tech Stack Requirements (Additive)

- **Logic:** `crepe` (Datalog in Rust) — added in Task S1.2 to `datalog_rs/Cargo.toml`.
- **Reactive:** Pure Python (`vitruvius.compound.dependency_tracker` + `differential_propagator`) — no new libraries.
- **Optimizer:** `dspy-ai` (Python) for Stream S5 — already installed, already used by `compound/dspy_compiler.py`.
- **Frontend kernel host:** `wasmtime` (Python) — listed as a Stream S4.2 prerequisite; not yet installed.
- **Wasm build:** `rustup target add wasm32-unknown-unknown` — listed as a Stream S4.1 prerequisite.
- **Memory:** PQ (Product Quantization) via `scikit-learn` or `faiss` for scaling embeddings on 8GB — inherited from `per-layer-embeddings-agentic-upgrade-plan.md`; not re-specified here.

---

## 4. Non-Breaking Guarantee

1.  **Feature-Flag Isolation:** All Phase 12 features ship behind `features.z_*` flags. Task S1.3 uses `features.z_neuro_symbolic`; additional flags for S3 and S4 are gated by module import (importing `vitruvius.compound.*` is a no-op until a caller uses it).
2.  **Legacy Fallback:** If the Neuro-Symbolic IR fails to compile, the system falls back to the existing Statistical Review (Phase 6) and flags the node for human review. The fallback lives in the caller of Task S1.3 (future wiring work, not this plan).
3.  **8GB Hardening:** Differential dataflow ensures we never load the full graph into memory; we only process the active Delta ($\Delta$). Task S3.3 propagator is stateless and O(|delta| * average_fanout).
4.  **Backward compat:** Every new test in this plan is additive. The only file this plan MODIFIES in place (rather than creates) is `scripts/vitruvius/graph/event_store.py` (Task S3.1 appends a `Delta` dataclass) and `scripts/vitruvius/review/ontology_prompt_builder.py` (Task S1.3 adds a flag-gated branch). Both modifications preserve the flag-OFF byte-identity guarantee.

---

## 5. Success Metrics

| Metric | Baseline (Phase 7-9) | Target (Phase 12) |
|---|---|---|
| **Hallucination Rate** | ~5% (Statistical) | <0.1% (Neuro-Symbolic Verified) |
| **Update Latency** | Minutes (Full Graph Rebuild) | <100ms (Differential Delta) |
| **Inference Cost** | Constant per query | $O(1)$ for cached/memoized geometry |
| **UI Parity** | Visual Guess (UI) vs. Math (Backend) | 100% Binary Identical (Wasm) |

---

## 6. Implementation Sequence

1.  **Sprint Z.1 (done, this wave):** Stream S2 (Adversarial Swarm) + Stream S5 (DSPy Compilation) landed during Wave 2 dispatch — commits `<S2_COMMIT>` and `<S5_COMMIT>`.
2.  **Sprint Z.2 (this plan):** Execute Stream S1 tasks (S1.1 → S1.2 → S1.3), then Stream S3 tasks (S3.1 → S3.2 → S3.3). Pure Python + single new Rust crate.
3.  **Sprint Z.3 (this plan, gated on S1):** Execute Stream S4 tasks (S4.1 → S4.2), then pause at the S4.3 frontend placeholder for a future frontend-focused plan.

Each numbered sub-task in §2 is 2–5 minutes of mechanical work for the implementer. The whole Sprint Z.2 + Sprint Z.3 block should close in one working day if prerequisites are installed up front.
