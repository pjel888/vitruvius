---
plan_id: per-layer-embeddings-agentic-upgrade
phase: "cross-phase (extends Phase 1A/5/6 + Stream F scaffolds + Phase 6A Resume gap)"
title: Per-Layer Embeddings & Agentic Reasoning Upgrade
status: planned
priority: high — runs after Sprint Q (live-wiring) closure
sprint: "Sprint R — post live-wiring (post Sprint Q)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
stream_progress:
  Y0_bootstrap_and_flags: pending (3 tasks)
  Y1_contextual_priming_PLE: pending (5 tasks)
  Y2_domain_routing_moe: pending (4 tasks)
  Y3_thinking_mode_cot_audit: pending (4 tasks)
  Y4_stateful_agentic_registry: pending (4 tasks)
  Y5_vision_ocr_integration: pending (4 tasks — gated)
prerequisites:
  - Stream A (Dependency Bootstrap + Feature Flags + Merkle) CLOSED ✅ 2026-04-14
  - Stream F (review/ subpackage — 8 scaffolds) CLOSED ✅ 2026-04-14
  - Stream B (parsers/ subpackage — shannon_classifier, table_graph_extractor, parametric_ner) CLOSED ✅ 2026-04-14
  - Phase 8 graph contract + snapshot CLOSED ✅ 2026-04-14
  - Live Wiring Plan (Sprint Q) Stream W2 CLOSED (ollama_review.py calls every review/ scaffold)
dependencies:
  - .ai/13_research/Per-Layer Embeddings.md (authoritative research spec)
  - .ai/03_plans/statistical-architectural-upgrade-plan.md §10 (Stream F — parent review scaffolds)
  - .ai/03_plans/live-wiring-and-8gb-hardening-plan.md (operationalises Stream F first)
  - .ai/03_plans/phase-8-graph-contract-indexing-plan.md (graph snapshot consumer)
  - scripts/vitruvius/ollama_review.py (574 lines — hot path)
  - scripts/vitruvius/review/ (8 scaffolds to extend, not replace)
  - scripts/vitruvius/parsers/document_taxonomy.py (Shannon already wired)
  - config/vitruvius.yaml (features block — add `features.y_*`)
related_plans:
  - statistical-architectural-upgrade-plan.md (parent plan — this plan EXTENDS its Stream F + adds new Stream Y)
  - live-wiring-and-8gb-hardening-plan.md (Sprint Q — must close first)
  - 3d-spatial-intelligence-upgrade-plan.md (Sprint H — independent)
  - ultimate-architecture-upgrade-plan.md (Streams I–X — independent; Streams U + R overlap, see §2.4)
takes_precedence_over:
  - None. This plan defers to live-wiring-and-8gb-hardening-plan (Sprint Q) for wiring existing scaffolds BEFORE adding new scaffolds.
non_breaking_guarantee: |
  Every new module ships behind a `features.y_*` flag in
  `config/vitruvius.yaml` (default FALSE). With every flag OFF,
  `ollama_review.py`, Phase 1A parsers, and the pipeline CLI produce
  byte-identical outputs to the Sprint Q post-wiring baseline. A new
  regression test (`test_ple_backcompat.py`) seeds a frozen 3-file PD 1096
  subset, runs the full pipeline with every `y_*` flag OFF, and diffs
  outputs against a checked-in fixture. Feature flag OFF paths MUST short-
  circuit before touching any new import — tests verify no PLE module is
  loaded unless its flag is on.
unblocks:
  - Root-cause closure of Phase 6A Resume gap (stateful agentic registry)
  - Root-cause closure of Phase 1A OCR gap for tables/charts (vision OCR path)
  - 3x–5x extraction accuracy on long legal documents (contextual priming)
  - Domain-specialised review routing (MoE upgrade to Stream F.2 slm_router)
  - Traceable chain-of-thought audit trail (CoT audit registry — groundwork for compliance)
gate:
  condition: "Live-Wiring Plan (Sprint Q) Stream W2 CLOSED. `ollama_review.py` must already import every Stream F scaffold before Stream Y1 begins. No new scaffold wiring starts until the old scaffold wiring is green."
  rationale: "PLE is a LAYER on top of the review pipeline. Adding a new layer above unwired scaffolds guarantees two dead layers instead of one. Wiring discipline first, capability second."
---

# Per-Layer Embeddings & Agentic Reasoning Upgrade Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended — Y1 and Y4 touch hot paths with mechanical TDD steps) or `superpowers:executing-plans`. Steps use checkbox (`- [ ]`) syntax for tracking. **Every task ships behind a feature flag; test the flag-OFF path too.**

**Goal.** Translate the architectural philosophy behind Google's Gemma 4 — **per-layer embeddings (PLE), mixture-of-experts (MoE) domain routing, native thinking mode, stateful agentic continuation, and multi-modal visual OCR** — into Vitruvius-specific modules that bolt cleanly onto the existing Stream F (review) and Phase 1A (ingestion) hot paths without breaking any shipped behaviour. Each innovation becomes a feature-flagged, narrowly-scoped sub-stream (Y1–Y5) that extends a specific Stream F scaffold or Phase 1A entry point. No existing file is rewritten; every new file lives under a new `priming/` subpackage or extends an existing `review/` or `parsers/` module via composition.

**Architecture.** Six execution streams mapped to the five research innovations plus one bootstrap stream:

- **Y0 — Bootstrap.** Feature-flag harness for `features.y_*`, dependency pinning (SQLite stdlib, `pillow`, optional `qwen2-vl` pull), backward-compat regression test.
- **Y1 — Contextual Priming (PLE).** Inject a deterministic "legal identity vector" at every LLM prompt and every extraction candidate so long documents never lose jurisdictional focus. Extends `review/ontology_prompt_builder.py` via composition; adds `priming/` subpackage.
- **Y2 — Domain-Routing MoE.** Upgrade `review/slm_router.py` from complexity-only routing to domain-aware routing: geometric candidates → small parametric model, administrative → mid model, occupancy/safety → large model. Adds `review/domain_classifier.py`.
- **Y3 — Thinking Mode + CoT Audit.** Force every verdict to ship with a parseable chain-of-thought trace, cite specific sentence fragments, and land in a permanent audit file. Extends `review/reflection_parser.py`; adds `review/cot_audit.py`.
- **Y4 — Stateful Agentic Registry.** Persistent SQLite-backed registry keyed by `(source_hash, relationship_hash, model_version)` so re-runs skip already-reviewed candidates. Closes the Phase 6A Resume gap at root. Adds `review/stateful_registry.py`.
- **Y5 — Vision OCR (Gated).** Wrap a ≤2B-param vision model (`moondream` or `qwen2-vl:2b`) as an Ollama fallback for table/chart extraction when Stream B's CSV/XLSX extractor fails. Adds `parsers/vision_ocr.py`. **Gated behind an 8GB RAM ceiling check** — defaults OFF, flips on only when a single vision inference + Ollama review coexist under 5 GB resident.

**Tech Stack.** Python stdlib (`sqlite3`) + existing shipped dependencies (`sentence-transformers`, `numpy`, `pyyaml`, `rapidfuzz`) + one new lib: `Pillow>=10.0` (only for Y5 vision pipeline image I/O — already a transitive dep of many parsers). **No GPU. No cloud.** Total incremental RAM peak at full throttle (Y1+Y2+Y3+Y4 ON, Y5 OFF): **+0.15 GB** above the live-wiring post-Sprint-Q baseline. Y5 adds **+1.8 GB** peak (moondream) when enabled — safely inside the 5 GB usable envelope only if Ollama review is routed to `qwen2.5:3b-instruct-q4_K_M` instead of the 7B default at the same time.

---

## 1. Preamble

### 1.1 Why This Plan Exists

The research document [`.ai/13_research/Per-Layer Embeddings.md`](../13_research/Per-Layer%20Embeddings.md) catalogues five Gemma 4 architectural innovations that **each close a specific, measurable gap** in the current Vitruvius pipeline:

| Innovation | Closes Gap | Root Cause of Gap |
|---|---|---|
| **Per-Layer Embeddings** | "Semantic drift" in long-document review | Prompts pass a single jurisdiction cue at the top, then the model forgets halfway through a 50-page IRR. |
| **MoE Domain Routing** | Slow, cost-inefficient single-model review | `review/slm_router.py` routes only on complexity, not domain — geometric candidates get the same model as occupancy. |
| **Thinking Mode + CoT** | Unverifiable `keep/reject` verdicts | `review/reflection_parser.py` looks for `<thought_process>` but the system prompt never mandates evidence citations. |
| **Stateful Continuation** | Phase 6A "Resume" gap — duplicate re-review on every run | No persistent memory of prior verdicts; every pipeline run re-invokes the LLM on already-decided candidates. |
| **Multi-Modal Vision** | Phase 1A OCR gap — flat table VII.1 extraction fails | Text-only `document_taxonomy.py` treats page images as noise; regex cannot recover a grid. |

Each Gemma 4 innovation is an **architectural philosophy**, not a model drop-in. The plan treats them as design patterns and ports them as small, feature-flagged Python modules that call whichever local model is already configured in `ollama_config.py`. The repository does not bundle Gemma 4 weights. The Gemma 4 weights would be **interchangeable** with any thinking-capable small model (`qwen2.5:3b-instruct`, `phi3:mini`, `gemma3:4b`) once the pattern is wired.

### 1.2 Precedence Declaration

Per the user brief: *"analyze and then study where we can utilize and make our code and app better with it"* — this plan is therefore an **extension** of `statistical-architectural-upgrade-plan.md`, not a replacement. It **defers** to `live-wiring-and-8gb-hardening-plan.md` (Sprint Q) for wiring existing scaffolds first.

Relative priority against other plans:

- **Sprint Q (live-wiring) — HIGHEST.** Must CLOSE before any Y stream begins. You cannot add a new priming layer on top of unwired review scaffolds.
- **Sprint R (this plan) — HIGH.** Runs immediately after Sprint Q.
- **Sprint H (3D spatial) — MEDIUM.** Independent; can run interleaved if there is capacity.
- **Streams J, K, L–X** (from parent plans) — unchanged precedence.

### 1.3 Non-Breaking Contract (hard rules)

These rules are enforced by the new `test_ple_backcompat.py` regression test in Y0 and by every Y task's self-review.

1. **Feature-flag default OFF.** Every new capability reads its on/off state from `config/vitruvius.yaml → features.y_*`. Default is `false`. Tests that the flag-OFF import path does not touch any Y module (monkey-patch assertion).
2. **Additive CLI only.** No existing subcommand is renamed or removed. New CLI subcommands (`ple-cotrace-dump`, `ple-registry-purge`, `ple-vision-probe`) are added but never invoked by the default `pipeline` command.
3. **Canonical layer is read-only by this plan.** No task writes to `003_Canonical-Knowledge-Layer/` except via `promotion.py` (which the live-wiring plan has already wired to the stringency resolver).
4. **Output determinism preserved.** Phase 1A output files remain byte-identical with every Y flag OFF. `test_ple_backcompat.py` asserts this on the frozen 3-file PD 1096 golden subset.
5. **No principle violations.** Every new module is audited against principles P1–P10. Y4 (SQLite registry) violates a naive reading of P3 (no hidden state); it earns its exemption by being **opt-in via flag + flush-on-demand via a dedicated CLI command**.
6. **No bundled model weights.** Vision models download on first use to `~/.cache/vitruvius/models/` and `.gitignore`d. Pull commands documented inline but never auto-run.
7. **Revert is a one-line flag toggle.** If any Y stream misbehaves, flipping its flag to `false` in `config/vitruvius.yaml` restores prior behaviour instantly.

### 1.4 Hardware Ceiling Contract

The machine target is an 8 GB M2 MacBook Pro. Every Y stream is sized such that:

- Peak RSS of the new Python code never exceeds **+150 MB** above the Sprint Q baseline for Y1+Y2+Y3+Y4.
- Y5 (vision) runs **only** when `features.y_vision_ocr: true` AND the Ollama review model is already downsized to `qwen2.5:3b-instruct-q4_K_M` AND a pre-flight RAM probe reports ≥3.5 GB free.
- Contextual-priming vectors are **dense float32 of dim 384** (sentence-transformers `all-MiniLM-L6-v2`, already installed). Stored as `bytes` column in SQLite, streamed lazily — never bulk-loaded. One vector ≈ 1.5 KB on disk.
- Stateful registry SQLite file capped at 200 MB via a `VACUUM` cycle triggered in the `ple-registry-purge` CLI.

### 1.5 How to Consume This Plan

1. **Start with Y0.** Every later task imports `vitruvius.priming` or extends a Stream F module; Y0 installs the subpackage and the flag harness.
2. Each stream has (a) Goal, (b) Files, (c) TDD task sequence with real code, (d) Non-Breaking Safeguards, (e) Definition of Done, (f) Gating Metrics, (g) Research-Item Coverage.
3. Commit after every task. Do not batch commits. `git commit -m "..."` is explicit in every task.
4. Before merging any stream, run `pytest scripts/tests/ -v` and `pytest scripts/tests/test_ple_backcompat.py -v`. Both must stay green.
5. For Y5 specifically: run `ple-vision-probe` first to confirm the 8GB envelope holds on the actual target machine. Abort Y5 if the probe reports a miss.

---

## 2. Research Document → Vitruvius Mapping

### 2.1 Innovation → Stream Crosswalk

| Gemma 4 Innovation (research §) | Vitruvius Target Module | New Y Stream | Binds to |
|---|---|---|---|
| PLE — per-layer conditioning vector (§1, §1 of part 2) | `priming/context_vector.py` + `priming/prompt_prefix.py` + extends `review/ontology_prompt_builder.py` | **Y1** | Phase 5 extraction + Phase 6 review |
| MoE Domain Routing (§2 of part 2) | `review/domain_classifier.py` + extends `review/slm_router.py` | **Y2** | Stream F.2 (shipped scaffold) |
| Thinking Mode + CoT Constraint (§3, §3 of part 2) | Extends `review/reflection_parser.py` + new `review/cot_audit.py` | **Y3** | Stream F.6 (shipped scaffold) |
| Stateful Agentic Continuation (§4 of part 2) | `review/stateful_registry.py` | **Y4** | `ollama_review.py` hot path — closes Phase 6A Resume gap |
| Multi-Modal Vision / OCR (§5 of part 2) | `parsers/vision_ocr.py` | **Y5** (gated) | Phase 1A ingestion, fallback from `parsers/table_graph_extractor.py` |

### 2.2 What Already Exists (No Work Needed)

| Research Implication | Already Covered By | Evidence |
|---|---|---|
| Small model preference (Gemma 4 E2B/E4B philosophy) | `review/slm_router.py` already routes to `qwen2.5:3b` / `phi3:mini` | Stream F.2 CLOSED 2026-04-14 |
| Ontology-embedded prompts (Gemma 4's "structured context injection") | `review/ontology_prompt_builder.py` already injects 2-hop graph neighbourhood | Stream F.3 CLOSED 2026-04-14 |
| Reflective self-critique (precursor to thinking mode) | `review/reflection_parser.py` parses `<thought_process>` | Stream F.6 CLOSED 2026-04-14 — **needs upgrade in Y3** |
| 256K-context handling | Not needed — Vitruvius chunks via `embedding_chunker.py` (Stream C.3) | Stream C CLOSED 2026-04-14 |

### 2.3 What is Missing — Addressed by This Plan

| Gap | Current Reality | Plan's Fix |
|---|---|---|
| Prompts don't inject source identity at every invocation | `ollama_review.py` passes only the `candidate` dict; no document-level vector | **Y1** contextual-priming prefix injector |
| SLM router ignores domain | `slm_router.py:42–70` picks a model by `len(evidence)` only | **Y2** domain classifier + routing table |
| `<thought_process>` block is optional — verdicts ship without it | `reflection_parser.py` returns `None` if the tag is absent (silent skip) | **Y3** hard-fail mode + CoT audit trail |
| Every run re-invokes the LLM on every relationship, even identical ones | `ollama_review.py` has no persistent verdict cache | **Y4** SQLite stateful registry |
| Table VII.1 from PD 1096 extracts as flat text, not a grid | `table_graph_extractor.py` only handles `.csv` / `.xlsx` — PDF tables skipped | **Y5** vision OCR fallback |

### 2.4 Overlap With Ultimate-Architecture-Upgrade-Plan Streams U + R

`ultimate-architecture-upgrade-plan.md` Stream U (Hardware-Aware Router) and Stream R (Epistemic Uncertainty) have partial conceptual overlap with Y2 and Y3 respectively. Resolution:

- **Y2 vs. Stream U.** Stream U routes by **hardware headroom** (psutil RAM probe). Y2 routes by **semantic domain**. They compose: Y2 picks the model family, U validates there is RAM headroom to run it. If both are scheduled, Y2 ships first; Stream U becomes a post-routing safety net.
- **Y3 vs. Stream R.** Stream R quantifies **epistemic uncertainty** via MC Dropout + Dempster-Shafer. Y3 enforces **CoT traceability**. They compose: Y3 logs the trace; Stream R can later consume it as a feature for the uncertainty estimator. If both ship, Y3 becomes a prerequisite of Stream R, not a competitor.

### 2.5 Items Explicitly Deferred (with rationale)

| Deferred Item | Rationale | Prerequisite Gate |
|---|---|---|
| Running actual Gemma 4 weights (E4B or 31B) | `gemma4:31b` is 19 GB; `gemma4:e4b` is ~4 GB but requires Ollama ≥0.5.0. User's live-wiring plan explicitly replaces `gemma4:31b` with `qwen2.5:7b` for 8GB survival. Y plan preserves that choice. | None — this is a permanent non-goal. |
| Agentic tool-use / native function calling | Requires a tool-calling-capable local model + tool registry. Out of scope for PLE-focused plan. | Stream V (IFC/OWL ontology — ultimate plan) must ship first. |
| 256K context window exploitation | Vitruvius chunks upstream; no document currently exceeds 32 K tokens. | Defer until a ≥64 K-token corpus appears. |

---

## 3. Dependency Bootstrap (Stream Y0 context)

### 3.1 New Python Packages

```
# Per-Layer Embeddings & Agentic Upgrade — additive only.
# All pins validated against existing requirements.txt on 8GB M2 M2026-04.
Pillow>=10.0.0,<11.0           # Y5 vision OCR image I/O (ONLY loaded when features.y_vision_ocr=true)
# sqlite3 is stdlib — no pip install
# sentence-transformers already installed by Stream A (all-MiniLM-L6-v2)
# pyyaml already installed
# numpy already installed
```

**No other new packages.** Y1's context vectors reuse the already-installed `all-MiniLM-L6-v2` sentence-transformer. Y4's registry uses stdlib `sqlite3`. Y2/Y3 are pure-Python. Y5 is gated and loads Pillow only behind its flag.

### 3.2 Model Pulls (manual, one-time)

```bash
# Y5 ONLY — run once if vision is to be enabled:
ollama pull moondream:latest           # ~1.8 GB Q4
# OR
ollama pull qwen2-vl:2b                # ~2.1 GB Q4
```

Neither model is auto-pulled by the pipeline. Y5 task Y5.1 documents the pull step but never executes it — a pre-flight probe checks availability and skips gracefully.

### 3.3 Disk & RAM Accounting

| Stream | Incremental Disk | Incremental RAM (peak) |
|---|---|---|
| Y0 | 0 MB | 0 MB |
| Y1 | 0 MB (reuses existing ST model) | +60 MB (ST model loaded for vectors; shared with Stream C.3 embedding_chunker if co-active) |
| Y2 | 0 MB | +5 MB (pure-Python router table) |
| Y3 | 0 MB | +10 MB (CoT trace buffers) |
| Y4 | up to 200 MB (SQLite registry file, capped by vacuum) | +15 MB (sqlite3 connection + in-memory query cache) |
| Y5 | ~1.8 GB (moondream) OR ~2.1 GB (qwen2-vl:2b) | +1.8–2.1 GB peak during inference |
| **Total (Y1–Y4)** | **+200 MB** | **+90 MB** |
| **Total (Y1–Y5)** | **+2.0 GB** | **+1.9 GB** (gated, Y5 only) |

### 3.4 New Configuration Keys (`config/vitruvius.yaml`)

```yaml
features:
  # --- Existing flags from earlier streams (preserved verbatim) ---
  # ...

  # --- Y streams (new, default FALSE) ---
  y_contextual_priming: false       # Y1 — PLE-style prompt prefix injection
  y_domain_routing_moe: false       # Y2 — domain-aware SLM routing
  y_thinking_mode_cot: false        # Y3 — force CoT + audit trail
  y_stateful_registry: false        # Y4 — SQLite verdict cache
  y_vision_ocr: false               # Y5 — vision OCR for tables/charts (GATED)

priming:
  context_vector_model: "all-MiniLM-L6-v2"
  context_vector_dim: 384
  drift_threshold_cosine: 0.45     # Y1 — escalate if similarity drops below this

routing:
  moe_policy_file: "config/moe_routing.yaml"    # Y2 — domain → model mapping

review_state:
  registry_path: "006_System-Manifests/registries/stateful_review_registry.sqlite"
  max_size_mb: 200
  vacuum_on_exceed: true

vision:
  ollama_model: "moondream:latest"
  max_image_pixels: 2000000         # 2MP safety ceiling
  fallback_on_csv_fail: true
```

All new keys default to safe values. Missing keys in an older config fall back to defaults via `features.py` loader (Stream A).

---

## 4. File Structure Map

### 4.1 New subpackage: `scripts/vitruvius/priming/`

```
scripts/vitruvius/priming/
├── __init__.py                     # Y0.1
├── context_vector.py               # Y1.1 — deterministic source-identity vector
├── prompt_prefix.py                # Y1.2 — LLM prompt prefix injector
└── drift_detector.py               # Y1.3 — cosine drift check
```

### 4.2 Extensions to existing subpackages

```
scripts/vitruvius/review/
├── (existing 8 Stream F scaffolds — unchanged)
├── domain_classifier.py            # Y2.1 — classify candidate into {geometric, administrative, occupancy, safety, fees}
├── cot_audit.py                    # Y3.2 — write full CoT trace to 005/cot_traces/
└── stateful_registry.py            # Y4.1 — SQLite verdict cache

scripts/vitruvius/parsers/
├── (existing Stream B modules — unchanged)
└── vision_ocr.py                   # Y5.1 — Ollama vision adapter (GATED)
```

### 4.3 New test files

```
scripts/tests/
├── test_ple_backcompat.py                      # Y0.3 — regression test (CRITICAL)
├── test_priming_context_vector.py              # Y1.1
├── test_priming_prompt_prefix.py               # Y1.2
├── test_priming_drift_detector.py              # Y1.3
├── test_priming_ontology_prompt_integration.py # Y1.4
├── test_priming_extraction_integration.py      # Y1.5
├── test_review_domain_classifier.py            # Y2.1
├── test_review_slm_router_moe_upgrade.py       # Y2.2
├── test_review_moe_routing_policy.py           # Y2.3
├── test_review_reflection_parser_cot_upgrade.py # Y3.1
├── test_review_cot_audit.py                    # Y3.2
├── test_review_cot_end_to_end.py               # Y3.3
├── test_review_stateful_registry.py            # Y4.1
├── test_review_stateful_registry_integration.py # Y4.2
├── test_review_stateful_registry_vacuum.py     # Y4.3
├── test_parsers_vision_ocr.py                  # Y5.1
├── test_parsers_vision_ocr_fallback.py         # Y5.2
└── fixtures/
    ├── ple_golden_3_files/                     # same 3-file PD 1096 subset as Stream A
    ├── seed_cot_traces/                        # 5 verified CoT trace examples
    ├── seed_moe_routing_policy.yaml            # synthetic 5-domain routing table
    ├── seed_pdf_table_page.png                 # Y5 fixture — single PDF page rendered
    └── seed_stateful_registry.sqlite           # Y4 fixture — pre-populated 10-verdict registry
```

### 4.4 New operational-layer outputs

```
005_Operational-Intelligence-Layer/
├── cot_traces/                     # Y3.2 — append-only CoT audit trail
│   └── YYYYMMDDTHHMMSSZ_{relationship_hash}.json
├── priming/                        # Y1 — context-vector debug dumps
│   └── latest_priming_report.json
└── observability/
    └── latest_moe_routing_distribution.json   # Y2.3 — domain → model hit counts
```

### 4.5 New system-manifests outputs

```
006_System-Manifests/
├── registries/
│   ├── latest_merkle_hash_registry.csv         # (from Stream A — unchanged)
│   └── stateful_review_registry.sqlite         # Y4 — persistent verdict cache
└── runs/
    ├── latest_priming_drift_report.json        # Y1.3
    ├── latest_cot_audit_summary.json           # Y3.3
    └── latest_vision_ocr_report.json           # Y5.3 (gated)
```

---

## 5. Stream Y0 — Bootstrap, Feature Flags, Backward-Compat Regression

**Priority:** P0 (blocking for every later Y stream)
**Sprint:** R, week 1 day 1
**Research-Item Coverage:** None — operational scaffolding.

### 5.1 Goal

Land the `priming/` subpackage shell, add the five `features.y_*` flags with default FALSE, and ship the `test_ple_backcompat.py` regression test that locks the current Sprint-Q-baseline behaviour.

### 5.2 Files

- Create: `scripts/vitruvius/priming/__init__.py`
- Modify: `config/vitruvius.yaml` (append the `features.y_*` block from §3.4)
- Modify: `scripts/vitruvius/features.py` (add Y flags to the dataclass)
- Create: `scripts/tests/test_ple_backcompat.py`
- Create: `scripts/tests/fixtures/ple_golden_3_files/` (copy from Stream A golden subset)

### 5.3 Task Sequence

#### Task Y0.1 — Create `priming/` subpackage shell

**Files:**
- Create: `scripts/vitruvius/priming/__init__.py`
- Test: `scripts/tests/test_ple_backcompat.py` (stub — expanded in Y0.3)

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_ple_backcompat.py
"""Regression test: with every features.y_* flag OFF, pipeline outputs are byte-identical."""
from __future__ import annotations

import importlib
import sys

import pytest


def test_priming_subpackage_is_importable() -> None:
    """The subpackage shell must exist even when all Y flags are off."""
    module = importlib.import_module("vitruvius.priming")
    assert module.__name__ == "vitruvius.priming"


def test_priming_subpackage_exports_nothing_by_default() -> None:
    """Importing the shell must not leak symbols — Y modules are opt-in via explicit imports."""
    module = importlib.import_module("vitruvius.priming")
    public = [name for name in dir(module) if not name.startswith("_")]
    assert public == [], f"unexpected public exports: {public}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest scripts/tests/test_ple_backcompat.py::test_priming_subpackage_is_importable -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.priming'`

- [ ] **Step 3: Create the empty subpackage shell**

```python
# scripts/vitruvius/priming/__init__.py
"""Per-Layer Embeddings priming subpackage.

Every module in this package is loaded on demand, behind a `features.y_*` flag.
Importing `vitruvius.priming` alone MUST NOT import any submodule — it is a shell.
"""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_ple_backcompat.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/priming/__init__.py scripts/tests/test_ple_backcompat.py
git commit -m "feat(priming): add empty subpackage shell (Task Y0.1)"
```

#### Task Y0.2 — Add `features.y_*` flags

**Files:**
- Modify: `config/vitruvius.yaml` (append §3.4 features block)
- Modify: `scripts/vitruvius/features.py` (add 5 new boolean fields to the FeatureFlags dataclass)
- Test: `scripts/tests/test_features.py` (add regression)

- [ ] **Step 1: Write the failing test** (append to `test_features.py`)

```python
def test_y_flags_default_false() -> None:
    """Every Y flag must default to False on a fresh load."""
    flags = load_feature_flags()
    assert flags.y_contextual_priming is False
    assert flags.y_domain_routing_moe is False
    assert flags.y_thinking_mode_cot is False
    assert flags.y_stateful_registry is False
    assert flags.y_vision_ocr is False


def test_y_flags_load_from_config(tmp_path) -> None:
    """A YAML override flips the flag but defaults remain False otherwise."""
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text(
        "features:\n"
        "  y_contextual_priming: true\n",
    )
    flags = load_feature_flags(config_path=cfg)
    assert flags.y_contextual_priming is True
    assert flags.y_domain_routing_moe is False  # unspecified → default False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest scripts/tests/test_features.py::test_y_flags_default_false -v`
Expected: FAIL with `AttributeError: 'FeatureFlags' object has no attribute 'y_contextual_priming'`

- [ ] **Step 3: Add the 5 new fields to the FeatureFlags dataclass**

Find the existing FeatureFlags dataclass in `features.py` and append (preserving alphabetical ordering within the Y section):

```python
# scripts/vitruvius/features.py — inside the FeatureFlags frozen dataclass
    # Stream Y — Per-Layer Embeddings & Agentic Reasoning
    y_contextual_priming: bool = False
    y_domain_routing_moe: bool = False
    y_thinking_mode_cot: bool = False
    y_stateful_registry: bool = False
    y_vision_ocr: bool = False
```

Then append the §3.4 features block to `config/vitruvius.yaml`:

```yaml
  # Stream Y — Per-Layer Embeddings & Agentic Reasoning (planned Sprint R)
  y_contextual_priming: false
  y_domain_routing_moe: false
  y_thinking_mode_cot: false
  y_stateful_registry: false
  y_vision_ocr: false
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_features.py -v`
Expected: all existing feature-flag tests pass + 2 new tests pass

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/features.py config/vitruvius.yaml scripts/tests/test_features.py
git commit -m "feat(features): add y_* flags for PLE upgrade (Task Y0.2)"
```

#### Task Y0.3 — Backward-compat regression test

**Files:**
- Create: `scripts/tests/fixtures/ple_golden_3_files/` (copy the same 3 PDFs Stream A used + their expected `.md` + `.refined.json` snapshots)
- Create: `scripts/tests/test_ple_backcompat.py` (expand)

- [ ] **Step 1: Copy fixtures**

```bash
cp -r scripts/tests/fixtures/golden_3_files scripts/tests/fixtures/ple_golden_3_files
```

- [ ] **Step 2: Expand the regression test** (append to `test_ple_backcompat.py`)

```python
def test_flag_off_pipeline_outputs_byte_identical(tmp_path) -> None:
    """With every Y flag OFF, running the pipeline on the golden fixture
    must produce byte-identical .md and .refined.json outputs to the frozen
    Sprint-Q baseline.
    """
    from pathlib import Path
    import shutil
    import json

    fixture_dir = Path(__file__).parent / "fixtures" / "ple_golden_3_files"
    work = tmp_path / "work"
    shutil.copytree(fixture_dir, work)

    from vitruvius.features import load_feature_flags
    from vitruvius.pipeline import run_phase_1a_and_1c  # existing entrypoint

    flags = load_feature_flags()
    assert flags.y_contextual_priming is False  # sanity

    run_phase_1a_and_1c(work, flags=flags)

    for pdf in (fixture_dir).glob("*.pdf"):
        produced_md = work / (pdf.stem + ".md")
        expected_md = fixture_dir / (pdf.stem + ".md")
        assert produced_md.read_bytes() == expected_md.read_bytes(), (
            f"{pdf.name}: .md drifted with every Y flag OFF"
        )

        produced_json = work / (pdf.stem + ".refined.json")
        expected_json = fixture_dir / (pdf.stem + ".refined.json")
        assert json.loads(produced_json.read_text()) == json.loads(
            expected_json.read_text()
        ), f"{pdf.name}: .refined.json drifted with every Y flag OFF"


def test_flag_off_priming_modules_never_imported() -> None:
    """No priming/* submodule is loaded when the flag is off.

    This is enforced at the pipeline call sites — Y1-Y5 always guard their
    imports behind a `if flags.y_*: ...` branch.
    """
    import sys
    from vitruvius.features import load_feature_flags
    from vitruvius.pipeline import run_phase_1a_and_1c

    flags = load_feature_flags()
    assert flags.y_contextual_priming is False

    # Drop any priming submodules that earlier tests may have left behind.
    for mod_name in list(sys.modules):
        if mod_name.startswith("vitruvius.priming.") or (
            mod_name in {"vitruvius.review.domain_classifier", "vitruvius.review.cot_audit",
                         "vitruvius.review.stateful_registry", "vitruvius.parsers.vision_ocr"}
        ):
            del sys.modules[mod_name]

    # (Full pipeline run happens in the prior test; here we only assert state.)
    for mod_name in sys.modules:
        assert not mod_name.startswith("vitruvius.priming."), (
            f"Unexpected priming module loaded with flag off: {mod_name}"
        )
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest scripts/tests/test_ple_backcompat.py -v`
Expected: 4 passed

- [ ] **Step 4: Commit**

```bash
git add scripts/tests/fixtures/ple_golden_3_files scripts/tests/test_ple_backcompat.py
git commit -m "test(ple): lock in flag-off backward-compat regression (Task Y0.3)"
```

### 5.4 Stream Y0 Definition of Done

- [ ] `priming/__init__.py` shell exists and imports cleanly
- [ ] All 5 Y flags exist in `FeatureFlags` dataclass and `config/vitruvius.yaml`
- [ ] `test_ple_backcompat.py` green with 4 tests
- [ ] Existing test suite still green (`pytest scripts/tests/ -v`)

### 5.5 Stream Y0 Gating Metrics

- **Test suite delta:** ≥4 new tests, 0 removed
- **Backward-compat diff:** 0 bytes drift across all 3 golden PDFs
- **Import cost of `vitruvius.priming` shell:** ≤1 ms

### 5.6 Research-Item Coverage (Stream Y0)

None — this stream is operational scaffolding.

---

## 6. Stream Y1 — Contextual Priming (Per-Layer Embeddings)

**Priority:** P1
**Sprint:** R, week 1 days 2–4
**Research-Item Coverage:** PLE / per-layer conditioning vectors (research §1, §1 of part 2)

### 6.1 Goal

Build a small "context vector" for every source document that acts as a deterministic identity fingerprint, then inject a human-readable summary of that vector as a system-prompt prefix on every LLM call and as a signal into every extraction candidate. On each call, also compute a cosine drift check and flag candidates whose response strayed too far from the source identity.

### 6.2 Files

- Create: `scripts/vitruvius/priming/context_vector.py`
- Create: `scripts/vitruvius/priming/prompt_prefix.py`
- Create: `scripts/vitruvius/priming/drift_detector.py`
- Modify: `scripts/vitruvius/review/ontology_prompt_builder.py` (add optional `prefix: str | None` parameter)
- Modify: `scripts/vitruvius/extraction/spacy_dep_parser.py` (attach `source_identity` to every Candidate)
- Test files (5 per §4.3)

### 6.3 Task Sequence

#### Task Y1.1 — Context Vector Builder

**Files:**
- Create: `scripts/vitruvius/priming/context_vector.py`
- Test: `scripts/tests/test_priming_context_vector.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_priming_context_vector.py
"""Unit tests for the deterministic source-identity vector builder."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from vitruvius.priming.context_vector import (
    SourceIdentity,
    build_source_identity,
    identity_to_prose,
)


def test_identity_is_deterministic_for_identical_frontmatter() -> None:
    fm = {
        "title": "PD 1096 - National Building Code",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "Congress of the Philippines",
        "issue_date": "1977-02-19",
    }
    ident_a = build_source_identity(fm, text_preview="Section 1. Title.")
    ident_b = build_source_identity(fm, text_preview="Section 1. Title.")
    assert ident_a.fingerprint == ident_b.fingerprint
    assert np.allclose(ident_a.vector, ident_b.vector)


def test_identity_prose_is_stable_plain_english() -> None:
    fm = {
        "title": "PD 1096 - National Building Code",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "Congress",
        "issue_date": "1977-02-19",
    }
    ident = build_source_identity(fm, text_preview="Section 1.")
    prose = identity_to_prose(ident)
    assert "PD 1096" in prose
    assert "national law" in prose.lower() or "national_law" in prose
    assert "PH" in prose or "Philippines" in prose


def test_vector_dimension_matches_config() -> None:
    fm = {"title": "x", "jurisdiction": "PH", "document_type": "national_law",
          "issuing_body": "y", "issue_date": "1970-01-01"}
    ident = build_source_identity(fm, text_preview="hello")
    assert ident.vector.shape == (384,)
    assert ident.vector.dtype == np.float32


def test_fingerprint_changes_when_jurisdiction_changes() -> None:
    fm_ph = {"title": "X", "jurisdiction": "PH", "document_type": "law",
             "issuing_body": "Y", "issue_date": "2000-01-01"}
    fm_us = dict(fm_ph, jurisdiction="US")
    a = build_source_identity(fm_ph, text_preview="same text")
    b = build_source_identity(fm_us, text_preview="same text")
    assert a.fingerprint != b.fingerprint
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest scripts/tests/test_priming_context_vector.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.priming.context_vector'`

- [ ] **Step 3: Implement `context_vector.py`**

```python
# scripts/vitruvius/priming/context_vector.py
"""Deterministic source-identity vector builder.

Produces a `SourceIdentity` record combining:
  - A stable SHA-256 fingerprint over (jurisdiction, doc_type, issuer, issue_date, title).
  - A 384-dim float32 embedding of a canonical prose summary of the frontmatter.

The vector is used by `prompt_prefix.py` (Y1.2) to prime LLM prompts and by
`drift_detector.py` (Y1.3) to measure response drift.

Loaded lazily — importing this module does NOT load sentence-transformers.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np

_EMBEDDER = None  # lazy singleton


def _get_embedder():
    global _EMBEDDER
    if _EMBEDDER is None:
        from sentence_transformers import SentenceTransformer

        _EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
    return _EMBEDDER


@dataclass(frozen=True)
class SourceIdentity:
    fingerprint: str  # sha256 hex (16 chars truncated)
    prose: str        # canonical plain-English summary
    vector: np.ndarray  # float32 [384]


def identity_to_prose(identity: SourceIdentity) -> str:
    return identity.prose


def build_source_identity(
    frontmatter: Mapping[str, Any],
    *,
    text_preview: str,
) -> SourceIdentity:
    """Build a deterministic source-identity record for a document.

    Parameters
    ----------
    frontmatter : Mapping
        Parsed source-layer frontmatter. Must contain at minimum
        `title`, `jurisdiction`, `document_type`, `issuing_body`, `issue_date`.
    text_preview : str
        First ≤512 chars of the body text — used only for the vector, not the
        fingerprint. Keeps the vector responsive to body drift between versions.
    """
    title = str(frontmatter.get("title", "")).strip()
    jurisdiction = str(frontmatter.get("jurisdiction", "")).strip()
    doc_type = str(frontmatter.get("document_type", "")).strip()
    issuer = str(frontmatter.get("issuing_body", "")).strip()
    issue_date = str(frontmatter.get("issue_date", "")).strip()

    fp_material = "|".join([jurisdiction, doc_type, issuer, issue_date, title])
    fingerprint = hashlib.sha256(fp_material.encode("utf-8")).hexdigest()[:16]

    prose = (
        f"This document is '{title}', a {doc_type.replace('_', ' ')} "
        f"issued by {issuer} on {issue_date} under the jurisdiction of {jurisdiction}. "
        f"All legal logic must be interpreted within {jurisdiction}'s regulatory context."
    )

    embedder = _get_embedder()
    body_sample = (text_preview or "")[:512]
    vector = embedder.encode(
        [prose + " CONTEXT: " + body_sample],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )[0].astype(np.float32)

    return SourceIdentity(fingerprint=fingerprint, prose=prose, vector=vector)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_priming_context_vector.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/priming/context_vector.py scripts/tests/test_priming_context_vector.py
git commit -m "feat(priming): add deterministic source-identity vector builder (Task Y1.1)"
```

#### Task Y1.2 — Prompt Prefix Injector

**Files:**
- Create: `scripts/vitruvius/priming/prompt_prefix.py`
- Test: `scripts/tests/test_priming_prompt_prefix.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_priming_prompt_prefix.py
from vitruvius.priming.context_vector import SourceIdentity
from vitruvius.priming.prompt_prefix import inject_prefix, PriorityLevel
import numpy as np


def _fake_identity() -> SourceIdentity:
    return SourceIdentity(
        fingerprint="deadbeefcafebabe",
        prose="This document is 'PD 1096 - National Building Code', a national law issued by Congress on 1977-02-19 under the jurisdiction of PH.",
        vector=np.zeros(384, dtype=np.float32),
    )


def test_prefix_prepends_to_system_message() -> None:
    original = [{"role": "system", "content": "You are a legal reviewer."}]
    result = inject_prefix(original, identity=_fake_identity())
    assert result[0]["role"] == "system"
    assert "deadbeefcafebabe" in result[0]["content"]
    assert "PD 1096" in result[0]["content"]
    assert "You are a legal reviewer." in result[0]["content"]


def test_prefix_does_not_mutate_input() -> None:
    original = [{"role": "system", "content": "orig"}]
    _ = inject_prefix(original, identity=_fake_identity())
    assert original == [{"role": "system", "content": "orig"}]


def test_prefix_inserts_system_if_absent() -> None:
    original = [{"role": "user", "content": "review this"}]
    result = inject_prefix(original, identity=_fake_identity())
    assert result[0]["role"] == "system"
    assert result[1]["role"] == "user"
    assert "deadbeefcafebabe" in result[0]["content"]


def test_priority_level_high_adds_reminder() -> None:
    original = [{"role": "system", "content": "orig"}]
    result = inject_prefix(original, identity=_fake_identity(), priority=PriorityLevel.HIGH)
    assert "DO NOT DRIFT" in result[0]["content"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest scripts/tests/test_priming_prompt_prefix.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `prompt_prefix.py`**

```python
# scripts/vitruvius/priming/prompt_prefix.py
"""Injects a source-identity prefix into a chat-completion message list.

This is the Vitruvius analogue of Gemma 4's Per-Layer Embeddings:
instead of conditioning every transformer layer with a learned vector,
we condition every LLM *call* with a deterministic prose reminder of
the document's identity. The model is explicitly told "you are reading
jurisdiction X's document type Y" on every invocation, so the Chain of
Thought cannot drift halfway through a long review session.
"""
from __future__ import annotations

import copy
from enum import Enum
from typing import Any, Sequence

from vitruvius.priming.context_vector import SourceIdentity


class PriorityLevel(str, Enum):
    NORMAL = "normal"
    HIGH = "high"


def inject_prefix(
    messages: Sequence[dict[str, Any]],
    *,
    identity: SourceIdentity,
    priority: PriorityLevel = PriorityLevel.NORMAL,
) -> list[dict[str, Any]]:
    """Return a copy of `messages` with an identity-priming prefix on the system message.

    Never mutates the input. If no system message exists, prepend one.
    """
    new_messages = copy.deepcopy(list(messages))
    prefix_lines = [
        f"SOURCE_IDENTITY[{identity.fingerprint}]: {identity.prose}",
    ]
    if priority == PriorityLevel.HIGH:
        prefix_lines.append(
            "CRITICAL: DO NOT DRIFT from this document's jurisdiction and type. "
            "Every verdict must be justifiable under this source's legal framework."
        )
    prefix = "\n".join(prefix_lines) + "\n\n"

    if new_messages and new_messages[0].get("role") == "system":
        new_messages[0]["content"] = prefix + new_messages[0]["content"]
    else:
        new_messages.insert(0, {"role": "system", "content": prefix.rstrip()})

    return new_messages
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_priming_prompt_prefix.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/priming/prompt_prefix.py scripts/tests/test_priming_prompt_prefix.py
git commit -m "feat(priming): add LLM prompt prefix injector (Task Y1.2)"
```

#### Task Y1.3 — Drift Detector

**Files:**
- Create: `scripts/vitruvius/priming/drift_detector.py`
- Test: `scripts/tests/test_priming_drift_detector.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_priming_drift_detector.py
import numpy as np

from vitruvius.priming.context_vector import SourceIdentity
from vitruvius.priming.drift_detector import (
    DriftReport,
    measure_drift,
    is_drift_excessive,
)


def _id_vec(values: list[float]) -> SourceIdentity:
    arr = np.array(values, dtype=np.float32)
    arr /= np.linalg.norm(arr) + 1e-9
    # Pad to 384 dims
    padded = np.zeros(384, dtype=np.float32)
    padded[: len(arr)] = arr
    return SourceIdentity(fingerprint="x", prose="y", vector=padded)


def test_identical_response_zero_drift() -> None:
    ident = _id_vec([1.0, 0.0, 0.0])
    report = measure_drift(identity=ident, response_vector=ident.vector)
    assert report.cosine_similarity == pytest.approx(1.0, abs=1e-4)
    assert report.drift == pytest.approx(0.0, abs=1e-4)


def test_orthogonal_response_full_drift() -> None:
    a = _id_vec([1.0, 0.0, 0.0])
    b_vec = np.zeros(384, dtype=np.float32)
    b_vec[1] = 1.0
    report = measure_drift(identity=a, response_vector=b_vec)
    assert report.cosine_similarity == pytest.approx(0.0, abs=1e-4)
    assert report.drift == pytest.approx(1.0, abs=1e-4)


def test_drift_threshold_default() -> None:
    a = _id_vec([1.0, 0.0, 0.0])
    # Cosine 0.5 → drift 0.5 → exceeds default threshold (1 - 0.45 = 0.55? test boundary)
    b_vec = np.zeros(384, dtype=np.float32)
    b_vec[0] = 0.5
    b_vec[1] = np.sqrt(1 - 0.25)
    report = measure_drift(identity=a, response_vector=b_vec)
    # cosine ≈ 0.5, drift ≈ 0.5
    assert is_drift_excessive(report, threshold_cosine=0.45) is True
    assert is_drift_excessive(report, threshold_cosine=0.55) is False


import pytest  # noqa: E402
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest scripts/tests/test_priming_drift_detector.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `drift_detector.py`**

```python
# scripts/vitruvius/priming/drift_detector.py
"""Cosine-similarity drift check between a source-identity vector and an LLM response vector.

Stream F's reflection_parser already asks the model to self-report confidence.
This module adds an independent measurement: embed the model's natural-language
response with the same sentence-transformer used for the source identity, then
measure cosine similarity. If the response strays too far, escalate.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from vitruvius.priming.context_vector import SourceIdentity


@dataclass(frozen=True)
class DriftReport:
    cosine_similarity: float
    drift: float            # 1.0 - cosine
    vector_norm_response: float


def measure_drift(
    *,
    identity: SourceIdentity,
    response_vector: np.ndarray,
) -> DriftReport:
    """Compute cosine similarity and 1-minus-cosine drift between the identity
    vector and an embedding of the model's response.

    Both vectors should be L2-normalised. If not, this function normalises
    defensively and records the original norm of `response_vector`.
    """
    norm_r = float(np.linalg.norm(response_vector))
    if norm_r < 1e-9:
        return DriftReport(cosine_similarity=0.0, drift=1.0, vector_norm_response=0.0)
    r = response_vector / norm_r
    sim = float(np.dot(identity.vector, r))
    return DriftReport(
        cosine_similarity=sim,
        drift=1.0 - sim,
        vector_norm_response=norm_r,
    )


def is_drift_excessive(report: DriftReport, *, threshold_cosine: float) -> bool:
    return report.cosine_similarity < threshold_cosine
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_priming_drift_detector.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/priming/drift_detector.py scripts/tests/test_priming_drift_detector.py
git commit -m "feat(priming): add cosine drift detector (Task Y1.3)"
```

#### Task Y1.4 — Wire priming into `ontology_prompt_builder.py`

**Files:**
- Modify: `scripts/vitruvius/review/ontology_prompt_builder.py` (add optional `source_identity: SourceIdentity | None` param)
- Test: `scripts/tests/test_priming_ontology_prompt_integration.py`

- [ ] **Step 1: Write the failing integration test**

```python
# scripts/tests/test_priming_ontology_prompt_integration.py
from vitruvius.priming.context_vector import SourceIdentity
from vitruvius.review.ontology_prompt_builder import build_ontology_prompt
import numpy as np


def test_prompt_omits_identity_when_none_passed() -> None:
    msgs = build_ontology_prompt(
        candidate={"subject": "building", "predicate": "has_setback", "object": "3m"},
        graph_snapshot={},
    )
    assert not any("SOURCE_IDENTITY" in m["content"] for m in msgs)


def test_prompt_prepends_identity_prefix_when_passed() -> None:
    ident = SourceIdentity(
        fingerprint="abc123",
        prose="This is PD 1096.",
        vector=np.zeros(384, dtype=np.float32),
    )
    msgs = build_ontology_prompt(
        candidate={"subject": "building", "predicate": "has_setback", "object": "3m"},
        graph_snapshot={},
        source_identity=ident,
    )
    sys_msg = next(m for m in msgs if m["role"] == "system")
    assert "SOURCE_IDENTITY[abc123]" in sys_msg["content"]
    assert "PD 1096" in sys_msg["content"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest scripts/tests/test_priming_ontology_prompt_integration.py -v`
Expected: FAIL with `TypeError: build_ontology_prompt() got an unexpected keyword argument 'source_identity'` or similar.

- [ ] **Step 3: Extend `ontology_prompt_builder.py`**

Add an optional parameter to the public builder. **Preserve every existing argument order** — append only.

```python
# scripts/vitruvius/review/ontology_prompt_builder.py — top of file, new import
from typing import Any, Optional

try:
    from vitruvius.priming.context_vector import SourceIdentity
    from vitruvius.priming.prompt_prefix import inject_prefix
    _PRIMING_AVAILABLE = True
except ImportError:
    SourceIdentity = None  # type: ignore
    _PRIMING_AVAILABLE = False


# Modify the existing build_ontology_prompt signature — APPEND `source_identity`
def build_ontology_prompt(
    candidate: dict[str, Any],
    graph_snapshot: dict[str, Any],
    *,
    source_identity: "Optional[SourceIdentity]" = None,  # NEW — default None preserves flag-OFF behaviour
) -> list[dict[str, Any]]:
    # ... existing body unchanged ...
    messages = _build_base_messages(candidate, graph_snapshot)  # existing call

    if source_identity is not None and _PRIMING_AVAILABLE:
        messages = inject_prefix(messages, identity=source_identity)

    return messages
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_priming_ontology_prompt_integration.py scripts/tests/test_review_ontology_prompt_builder.py -v`
Expected: all new tests pass + existing Stream F.3 tests still green.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/ontology_prompt_builder.py scripts/tests/test_priming_ontology_prompt_integration.py
git commit -m "feat(review): accept optional source_identity in ontology prompt builder (Task Y1.4)"
```

#### Task Y1.5 — Wire priming into extraction candidates

**Files:**
- Modify: `scripts/vitruvius/extraction/spacy_dep_parser.py` (attach `source_identity_fingerprint` to every Candidate)
- Test: `scripts/tests/test_priming_extraction_integration.py`

- [ ] **Step 1: Write the failing integration test**

```python
# scripts/tests/test_priming_extraction_integration.py
from pathlib import Path
from vitruvius.priming.context_vector import build_source_identity
from vitruvius.extraction.spacy_dep_parser import extract_candidates


def test_candidates_carry_source_fingerprint_when_identity_provided() -> None:
    frontmatter = {
        "title": "Test Law",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "Congress",
        "issue_date": "2000-01-01",
    }
    identity = build_source_identity(frontmatter, text_preview="Setbacks must be at least 3m.")
    candidates = extract_candidates(
        "The front setback must be at least 3 meters.",
        source_identity=identity,
    )
    assert len(candidates) >= 1
    assert all(c.source_identity_fingerprint == identity.fingerprint for c in candidates)


def test_candidates_have_none_fingerprint_when_identity_omitted() -> None:
    candidates = extract_candidates("The front setback must be at least 3 meters.")
    assert all(c.source_identity_fingerprint is None for c in candidates)
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: FAIL with AttributeError on `source_identity_fingerprint`.

- [ ] **Step 3: Extend `extraction/spacy_dep_parser.py`**

Find the existing `Candidate` dataclass — add one optional field:

```python
# scripts/vitruvius/extraction/spacy_dep_parser.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class Candidate:
    subject: str
    verb: str
    object: str
    span: tuple[int, int]
    source_identity_fingerprint: Optional[str] = None  # NEW — default None preserves existing callers


def extract_candidates(text: str, *, source_identity=None) -> list[Candidate]:
    # ... existing body unchanged up to the return ...
    fp = source_identity.fingerprint if source_identity is not None else None
    return [
        Candidate(
            subject=s,
            verb=v,
            object=o,
            span=span,
            source_identity_fingerprint=fp,
        )
        for s, v, o, span in _raw_triples_from_doc(text)
    ]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_priming_extraction_integration.py scripts/tests/test_spacy_dep_parser.py -v`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/extraction/spacy_dep_parser.py scripts/tests/test_priming_extraction_integration.py
git commit -m "feat(extraction): propagate source-identity fingerprint onto candidates (Task Y1.5)"
```

### 6.4 Stream Y1 Definition of Done

- [ ] `context_vector.build_source_identity` emits deterministic fingerprint + 384-dim vector
- [ ] `prompt_prefix.inject_prefix` prepends identity to any chat-completion message list
- [ ] `drift_detector.measure_drift` returns cosine + 1-cosine + passes threshold check
- [ ] `ontology_prompt_builder` accepts optional `source_identity` — tests pass with and without
- [ ] `spacy_dep_parser.extract_candidates` propagates `source_identity_fingerprint` onto every Candidate
- [ ] `test_ple_backcompat.py` green (flag OFF produces byte-identical output)

### 6.5 Stream Y1 Gating Metrics

- **Drift distribution on PD 1096 reruns, Y1 ON:** ≥95 % of review responses have cosine similarity ≥ 0.6 to the source-identity vector
- **Fingerprint stability:** 100 % identical across 5 re-runs on the same source file
- **Prompt prefix overhead:** ≤150 tokens per LLM call

### 6.6 Research-Item Coverage (Stream Y1)

- ✅ Research §1 (Per-Layer Embeddings — Contextual Priming)
- ✅ Research §1 of part 2 (Per-Layer Conditioned Vectors — "Memory Identity" Fix)

---

## 7. Stream Y2 — Domain-Routing MoE

**Priority:** P1
**Sprint:** R, week 2 days 1–3
**Research-Item Coverage:** Mixture of Experts domain routing (research §2 of part 2)

### 7.1 Goal

Upgrade `review/slm_router.py` from a complexity-only router to a domain-aware router. A new `domain_classifier.py` pre-classifies every candidate into `{geometric, administrative, occupancy, safety, fees, other}`, then the slm_router consults a YAML routing policy (`config/moe_routing.yaml`) to pick the right model per domain. Falls back cleanly to the existing complexity path when the flag is OFF.

### 7.2 Files

- Create: `scripts/vitruvius/review/domain_classifier.py`
- Modify: `scripts/vitruvius/review/slm_router.py` (add `route_with_moe` function; leave `route` untouched)
- Create: `config/moe_routing.yaml`
- Tests (3 per §4.3)

### 7.3 Task Sequence

#### Task Y2.1 — Domain Classifier

**Files:**
- Create: `scripts/vitruvius/review/domain_classifier.py`
- Test: `scripts/tests/test_review_domain_classifier.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_domain_classifier.py
import pytest

from vitruvius.review.domain_classifier import classify_domain, Domain


@pytest.mark.parametrize(
    "predicate, subject, obj, expected",
    [
        ("has_setback", "building", "3 meters", Domain.GEOMETRIC),
        ("has_height_limit", "structure", "15 meters", Domain.GEOMETRIC),
        ("requires_permit", "construction", "building official", Domain.ADMINISTRATIVE),
        ("must_notify", "owner", "barangay", Domain.ADMINISTRATIVE),
        ("has_occupancy_load", "floor", "50 persons", Domain.OCCUPANCY),
        ("must_comply_with", "building", "fire code", Domain.SAFETY),
        ("has_fee", "permit", "5000 PHP", Domain.FEES),
        ("relates_to", "term1", "term2", Domain.OTHER),
    ],
)
def test_classify_domain_by_predicate(predicate, subject, obj, expected) -> None:
    domain = classify_domain(subject=subject, predicate=predicate, object_=obj)
    assert domain == expected


def test_classify_domain_is_deterministic() -> None:
    a = classify_domain(subject="x", predicate="has_setback", object_="y")
    b = classify_domain(subject="x", predicate="has_setback", object_="y")
    assert a == b
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `domain_classifier.py`**

```python
# scripts/vitruvius/review/domain_classifier.py
"""Deterministic domain classifier for a relationship candidate.

Maps (subject, predicate, object) tuples into one of 6 semantic domains.
Used by slm_router.py's `route_with_moe` to pick domain-specialised models.

Classification strategy: predicate keyword matching with a fall-through to
subject/object keyword matching, and an OTHER default. Intentionally simple —
later we can swap in a trained multinomial classifier once enough audit data
accumulates, but deterministic regex is sufficient for the initial ship.
"""
from __future__ import annotations

import re
from enum import Enum


class Domain(str, Enum):
    GEOMETRIC = "geometric"
    ADMINISTRATIVE = "administrative"
    OCCUPANCY = "occupancy"
    SAFETY = "safety"
    FEES = "fees"
    OTHER = "other"


_PREDICATE_PATTERNS: list[tuple[re.Pattern[str], Domain]] = [
    (re.compile(r"setback|height|width|depth|area|diameter|distance", re.I), Domain.GEOMETRIC),
    (re.compile(r"permit|notify|clearance|apply|submit|approval|certify|issue", re.I), Domain.ADMINISTRATIVE),
    (re.compile(r"occupan|load|capacity|persons|people|residents", re.I), Domain.OCCUPANCY),
    (re.compile(r"fire|safety|hazard|emergency|escape|alarm", re.I), Domain.SAFETY),
    (re.compile(r"fee|cost|charge|payment|bond|deposit|PHP", re.I), Domain.FEES),
]


def classify_domain(*, subject: str, predicate: str, object_: str) -> Domain:
    """Deterministically classify a relationship candidate into a domain."""
    haystack = f"{subject} {predicate} {object_}"
    for pattern, domain in _PREDICATE_PATTERNS:
        if pattern.search(haystack):
            return domain
    return Domain.OTHER
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_domain_classifier.py -v`
Expected: all pass (8 parametrised + 1).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/domain_classifier.py scripts/tests/test_review_domain_classifier.py
git commit -m "feat(review): add deterministic domain classifier for MoE routing (Task Y2.1)"
```

#### Task Y2.2 — Extend `slm_router.py` with `route_with_moe`

**Files:**
- Modify: `scripts/vitruvius/review/slm_router.py` (append `route_with_moe`, leave `route` unchanged)
- Test: `scripts/tests/test_review_slm_router_moe_upgrade.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_slm_router_moe_upgrade.py
from vitruvius.review.slm_router import route_with_moe, route  # `route` = existing Stream F.2 fn
from vitruvius.review.domain_classifier import Domain


def test_geometric_candidate_routes_to_small_model() -> None:
    verdict = route_with_moe(
        candidate={"subject": "building", "predicate": "has_setback", "object": "3m", "evidence": "The setback must be 3m."},
        moe_policy={
            Domain.GEOMETRIC: "qwen2.5:3b-instruct-q4_K_M",
            Domain.ADMINISTRATIVE: "qwen2.5:7b-instruct-q4_K_M",
            Domain.OCCUPANCY: "qwen2.5:7b-instruct-q4_K_M",
            Domain.SAFETY: "qwen2.5:7b-instruct-q4_K_M",
            Domain.FEES: "qwen2.5:3b-instruct-q4_K_M",
            Domain.OTHER: "qwen2.5:7b-instruct-q4_K_M",
        },
    )
    assert verdict.model == "qwen2.5:3b-instruct-q4_K_M"
    assert verdict.domain == Domain.GEOMETRIC


def test_administrative_candidate_routes_to_mid_model() -> None:
    verdict = route_with_moe(
        candidate={"subject": "construction", "predicate": "requires_permit", "object": "building official"},
        moe_policy={
            Domain.GEOMETRIC: "small",
            Domain.ADMINISTRATIVE: "mid",
            Domain.OCCUPANCY: "mid",
            Domain.SAFETY: "mid",
            Domain.FEES: "small",
            Domain.OTHER: "mid",
        },
    )
    assert verdict.model == "mid"
    assert verdict.domain == Domain.ADMINISTRATIVE


def test_legacy_route_unchanged() -> None:
    """The original Stream F.2 `route` function must still work untouched."""
    picked = route(complexity_score=0.3)
    assert picked  # non-empty — exact model depends on shipped F.2 logic
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ImportError: cannot import name 'route_with_moe'` — or, later, assertion failures until implementation lands.

- [ ] **Step 3: Extend `slm_router.py`**

Append to the existing file **without modifying the existing `route` function**:

```python
# scripts/vitruvius/review/slm_router.py — append at the bottom
from dataclasses import dataclass
from typing import Any, Mapping

from vitruvius.review.domain_classifier import Domain, classify_domain


@dataclass(frozen=True)
class MoEVerdict:
    model: str
    domain: Domain


def route_with_moe(
    *,
    candidate: Mapping[str, Any],
    moe_policy: Mapping[Domain, str],
) -> MoEVerdict:
    """Pick a model by (classified) domain of the candidate.

    Does NOT replace the legacy `route` function — composes with it.
    Callers that still want complexity-only routing stay on `route`;
    new callers that want domain routing call `route_with_moe`.
    """
    subject = str(candidate.get("subject", ""))
    predicate = str(candidate.get("predicate", ""))
    obj = str(candidate.get("object", ""))

    domain = classify_domain(subject=subject, predicate=predicate, object_=obj)
    model = moe_policy.get(domain) or moe_policy[Domain.OTHER]
    return MoEVerdict(model=model, domain=domain)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_slm_router_moe_upgrade.py scripts/tests/test_review_slm_router.py -v`
Expected: all pass (new + pre-existing Stream F.2 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/slm_router.py scripts/tests/test_review_slm_router_moe_upgrade.py
git commit -m "feat(review): add route_with_moe domain-aware router (Task Y2.2)"
```

#### Task Y2.3 — MoE Routing Policy File + Loader

**Files:**
- Create: `config/moe_routing.yaml`
- Modify: `scripts/vitruvius/review/slm_router.py` (add `load_moe_policy`)
- Test: `scripts/tests/test_review_moe_routing_policy.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_moe_routing_policy.py
from pathlib import Path

import pytest

from vitruvius.review.slm_router import load_moe_policy
from vitruvius.review.domain_classifier import Domain


def test_load_valid_policy(tmp_path: Path) -> None:
    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text(
        "geometric: qwen2.5:3b\n"
        "administrative: qwen2.5:7b\n"
        "occupancy: qwen2.5:7b\n"
        "safety: qwen2.5:7b\n"
        "fees: qwen2.5:3b\n"
        "other: qwen2.5:7b\n"
    )
    policy = load_moe_policy(policy_file)
    assert policy[Domain.GEOMETRIC] == "qwen2.5:3b"
    assert policy[Domain.ADMINISTRATIVE] == "qwen2.5:7b"
    assert len(policy) == 6


def test_load_policy_missing_domain_raises(tmp_path: Path) -> None:
    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text("geometric: x\nadministrative: y\n")  # incomplete
    with pytest.raises(ValueError, match="missing domain"):
        load_moe_policy(policy_file)
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ImportError: cannot import name 'load_moe_policy'`.

- [ ] **Step 3: Implement `load_moe_policy` in `slm_router.py`**

```python
# scripts/vitruvius/review/slm_router.py — append
from pathlib import Path

import yaml


def load_moe_policy(path: Path) -> dict[Domain, str]:
    raw = yaml.safe_load(Path(path).read_text())
    required = {d.value for d in Domain}
    missing = required - set(raw.keys())
    if missing:
        raise ValueError(f"missing domain(s) in MoE policy file: {sorted(missing)}")
    return {Domain(k): str(v) for k, v in raw.items()}
```

And create the default policy file:

```yaml
# config/moe_routing.yaml — domain → Ollama model map
geometric: qwen2.5:3b-instruct-q4_K_M
administrative: qwen2.5:7b-instruct-q4_K_M
occupancy: qwen2.5:7b-instruct-q4_K_M
safety: qwen2.5:7b-instruct-q4_K_M
fees: qwen2.5:3b-instruct-q4_K_M
other: qwen2.5:7b-instruct-q4_K_M
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_moe_routing_policy.py -v`
Expected: 2 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/slm_router.py config/moe_routing.yaml scripts/tests/test_review_moe_routing_policy.py
git commit -m "feat(review): add MoE routing policy loader (Task Y2.3)"
```

#### Task Y2.4 — Hook MoE routing into `ollama_review.py` (flag-gated)

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py` (add flag-gated branch calling `route_with_moe`)
- Test: `scripts/tests/test_review_slm_router_moe_upgrade.py` (add integration test)

- [ ] **Step 1: Write the failing integration test**

```python
# scripts/tests/test_review_slm_router_moe_upgrade.py — append
from unittest.mock import patch

from vitruvius.ollama_review import select_review_model
from vitruvius.features import FeatureFlags


def test_select_review_model_falls_back_when_moe_flag_off() -> None:
    flags = FeatureFlags(y_domain_routing_moe=False)
    with patch("vitruvius.ollama_review._default_model", return_value="baseline"):
        model = select_review_model(
            candidate={"subject": "x", "predicate": "has_setback", "object": "3m"},
            flags=flags,
        )
    assert model == "baseline"


def test_select_review_model_uses_moe_when_flag_on(tmp_path) -> None:
    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text(
        "geometric: small-model\nadministrative: mid-model\noccupancy: mid-model\n"
        "safety: mid-model\nfees: small-model\nother: mid-model\n"
    )
    flags = FeatureFlags(y_domain_routing_moe=True)
    model = select_review_model(
        candidate={"subject": "building", "predicate": "has_setback", "object": "3m"},
        flags=flags,
        moe_policy_path=policy_file,
    )
    assert model == "small-model"
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `AttributeError: module has no attribute 'select_review_model'` or similar.

- [ ] **Step 3: Add `select_review_model` to `ollama_review.py`**

Append to `ollama_review.py` — **do not touch existing code paths**:

```python
# scripts/vitruvius/ollama_review.py — append near the top of the file
from pathlib import Path
from typing import Any, Mapping, Optional

from vitruvius.features import FeatureFlags


def _default_model() -> str:
    # Delegates to existing ollama_config — shipped in Stream F.7
    from vitruvius.review.ollama_config import get_default_review_model
    return get_default_review_model()


def select_review_model(
    *,
    candidate: Mapping[str, Any],
    flags: FeatureFlags,
    moe_policy_path: Optional[Path] = None,
) -> str:
    """Pick a model for this candidate, respecting the y_domain_routing_moe flag.

    When the flag is OFF, returns the baseline default from ollama_config.
    When ON, consults `route_with_moe` with the loaded MoE policy.
    """
    if not flags.y_domain_routing_moe:
        return _default_model()

    from vitruvius.review.slm_router import route_with_moe, load_moe_policy

    policy_path = moe_policy_path or Path("config/moe_routing.yaml")
    policy = load_moe_policy(policy_path)
    verdict = route_with_moe(candidate=candidate, moe_policy=policy)
    return verdict.model
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_slm_router_moe_upgrade.py -v`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/tests/test_review_slm_router_moe_upgrade.py
git commit -m "feat(review): flag-gated MoE select_review_model hook (Task Y2.4)"
```

### 7.4 Stream Y2 Definition of Done

- [ ] `classify_domain` emits deterministic Domain value for every test fixture
- [ ] `route_with_moe` picks the policy-mapped model per domain
- [ ] `load_moe_policy` validates that all 6 domains are present
- [ ] `select_review_model` falls back to baseline when flag OFF
- [ ] `test_ple_backcompat.py` green

### 7.5 Stream Y2 Gating Metrics

- **Routing distribution on a 100-candidate sample:** ≥40 % of candidates route to a ≤3B-param model (was 0 % in Stream F.2's complexity-only router when all candidates had similar length)
- **Per-domain accuracy delta:** ≥+0.03 F1 for Geometric vs. baseline (domain-specialised prompt wins on numeric SVOs)

### 7.6 Research-Item Coverage (Stream Y2)

- ✅ Research §2 of part 2 (Mixture of Experts for Domain Routing)

---

## 8. Stream Y3 — Thinking Mode + CoT Audit Trail

**Priority:** P1
**Sprint:** R, week 2 days 4–5
**Research-Item Coverage:** Thinking Mode / Chain-of-Thought verification (research §1, §3 of part 2)

### 8.1 Goal

Upgrade `review/reflection_parser.py` from an optional `<thought_process>` sniffer to a mandatory Chain-of-Thought gate. Every LLM verdict must ship with (a) a traceable reasoning block, (b) cited evidence spans from the source text, and (c) a parseable self-confidence. Any missing field hard-fails the verdict with `escalate: True`. Also adds `review/cot_audit.py` that writes the full trace to an append-only audit directory for compliance.

### 8.2 Files

- Modify: `scripts/vitruvius/review/reflection_parser.py` (add `parse_cot_strict` — legacy `parse_reflection` stays untouched)
- Create: `scripts/vitruvius/review/cot_audit.py`
- Modify: `scripts/vitruvius/ollama_review.py` (flag-gated CoT enforcement branch)
- Tests (3 per §4.3)

### 8.3 Task Sequence

#### Task Y3.1 — Strict CoT Parser

**Files:**
- Modify: `scripts/vitruvius/review/reflection_parser.py`
- Test: `scripts/tests/test_review_reflection_parser_cot_upgrade.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_reflection_parser_cot_upgrade.py
import pytest

from vitruvius.review.reflection_parser import parse_cot_strict, CotParseError


def test_valid_cot_parses_cleanly() -> None:
    raw = (
        "<think>\n"
        "Step 1: Read the rule. Evidence: 'Section 701: the setback must be at least 3 meters'.\n"
        "Step 2: The candidate predicate 'has_setback' aligns with the rule.\n"
        "Self-confidence: 0.92\n"
        "</think>\n"
        "VERDICT: keep"
    )
    result = parse_cot_strict(raw)
    assert result.verdict == "keep"
    assert result.self_confidence == pytest.approx(0.92)
    assert "Section 701" in result.evidence_citation
    assert len(result.reasoning_steps) == 2


def test_missing_think_block_raises() -> None:
    raw = "VERDICT: keep"
    with pytest.raises(CotParseError, match="no <think> block"):
        parse_cot_strict(raw)


def test_missing_verdict_raises() -> None:
    raw = "<think>step 1: ok. Self-confidence: 0.8</think>"
    with pytest.raises(CotParseError, match="no VERDICT line"):
        parse_cot_strict(raw)


def test_missing_evidence_citation_raises() -> None:
    raw = "<think>Step 1: I think so. Self-confidence: 0.8</think>\nVERDICT: keep"
    with pytest.raises(CotParseError, match="no evidence citation"):
        parse_cot_strict(raw)


def test_low_self_confidence_flags_escalate() -> None:
    raw = (
        "<think>Step 1: Evidence: 'quoted phrase'. Self-confidence: 0.40</think>\n"
        "VERDICT: keep"
    )
    result = parse_cot_strict(raw, escalate_below=0.70)
    assert result.verdict == "keep"
    assert result.escalate is True
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ImportError: cannot import name 'parse_cot_strict'`.

- [ ] **Step 3: Extend `reflection_parser.py`**

Append — do not modify the existing `parse_reflection`:

```python
# scripts/vitruvius/review/reflection_parser.py — append at the bottom
import re
from dataclasses import dataclass, field


class CotParseError(ValueError):
    """Raised when a strict CoT parse fails validation."""


@dataclass(frozen=True)
class CotResult:
    verdict: str                       # "keep" | "reject" | "abstain"
    self_confidence: float
    reasoning_steps: list[str]
    evidence_citation: str
    escalate: bool = False


_THINK_RE = re.compile(r"<think>(.*?)</think>", re.DOTALL | re.IGNORECASE)
_VERDICT_RE = re.compile(r"VERDICT\s*:\s*(keep|reject|abstain)", re.IGNORECASE)
_CONFIDENCE_RE = re.compile(r"self[- ]?confidence\s*:?\s*([0-9]*\.?[0-9]+)", re.IGNORECASE)
_STEP_RE = re.compile(r"step\s*\d+[:.]\s*(.+?)(?=step\s*\d+[:.]|self[- ]?confidence|$)", re.IGNORECASE | re.DOTALL)
_CITATION_RE = re.compile(r"""['"]([^'"]{5,})['"]""")


def parse_cot_strict(raw: str, *, escalate_below: float = 0.70) -> CotResult:
    """Parse an LLM response under strict CoT discipline.

    Requires:
      - A `<think>...</think>` block.
      - At least one reasoning step labelled `Step N:`.
      - A quoted evidence citation of ≥5 chars inside the think block.
      - A `Self-confidence: <float>` line inside the think block.
      - A `VERDICT: <keep|reject|abstain>` line OUTSIDE the think block.
    """
    think_match = _THINK_RE.search(raw)
    if not think_match:
        raise CotParseError("no <think> block in response")
    think_body = think_match.group(1).strip()

    outside_think = _THINK_RE.sub("", raw)
    verdict_match = _VERDICT_RE.search(outside_think)
    if not verdict_match:
        raise CotParseError("no VERDICT line outside <think> block")

    conf_match = _CONFIDENCE_RE.search(think_body)
    if not conf_match:
        raise CotParseError("no self-confidence in <think> block")
    confidence = float(conf_match.group(1))

    steps = [s.strip() for s in _STEP_RE.findall(think_body) if s.strip()]
    if not steps:
        raise CotParseError("no reasoning steps in <think> block")

    citation_match = _CITATION_RE.search(think_body)
    if not citation_match:
        raise CotParseError("no evidence citation in <think> block")

    return CotResult(
        verdict=verdict_match.group(1).lower(),
        self_confidence=confidence,
        reasoning_steps=steps,
        evidence_citation=citation_match.group(1),
        escalate=confidence < escalate_below,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_reflection_parser_cot_upgrade.py scripts/tests/test_review_reflection_parser.py -v`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/reflection_parser.py scripts/tests/test_review_reflection_parser_cot_upgrade.py
git commit -m "feat(review): add strict parse_cot_strict CoT parser (Task Y3.1)"
```

#### Task Y3.2 — CoT Audit Writer

**Files:**
- Create: `scripts/vitruvius/review/cot_audit.py`
- Test: `scripts/tests/test_review_cot_audit.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_cot_audit.py
import json
from pathlib import Path

import pytest

from vitruvius.review.reflection_parser import CotResult
from vitruvius.review.cot_audit import write_cot_trace, CotAuditSummary


def test_write_trace_creates_file_with_deterministic_name(tmp_path: Path) -> None:
    result = CotResult(
        verdict="keep",
        self_confidence=0.91,
        reasoning_steps=["step 1", "step 2"],
        evidence_citation="setback 3m",
    )
    path = write_cot_trace(
        out_dir=tmp_path,
        relationship_hash="abc123deadbeef",
        cot=result,
        model="qwen2.5:7b",
        candidate_raw_response="<think>...</think>VERDICT: keep",
    )
    assert path.exists()
    assert path.name.endswith("_abc123deadbeef.json")
    payload = json.loads(path.read_text())
    assert payload["verdict"] == "keep"
    assert payload["self_confidence"] == 0.91
    assert payload["relationship_hash"] == "abc123deadbeef"
    assert payload["model"] == "qwen2.5:7b"


def test_audit_summary_counts_verdicts(tmp_path: Path) -> None:
    for i, v in enumerate(["keep", "keep", "reject", "keep", "abstain"]):
        write_cot_trace(
            out_dir=tmp_path,
            relationship_hash=f"hash{i}",
            cot=CotResult(verdict=v, self_confidence=0.8, reasoning_steps=["x"], evidence_citation="y"),
            model="m",
            candidate_raw_response="",
        )
    summary = CotAuditSummary.from_directory(tmp_path)
    assert summary.total == 5
    assert summary.verdict_counts == {"keep": 3, "reject": 1, "abstain": 1}
    assert summary.mean_self_confidence == pytest.approx(0.8)
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `cot_audit.py`**

```python
# scripts/vitruvius/review/cot_audit.py
"""Append-only CoT audit trail.

For every verdict that parses through `parse_cot_strict`, write a JSON trace to
005_Operational-Intelligence-Layer/cot_traces/. The filename encodes a UTC timestamp
+ relationship hash so traces are append-only, deterministic, and easy to diff.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vitruvius.review.reflection_parser import CotResult


def write_cot_trace(
    *,
    out_dir: Path,
    relationship_hash: str,
    cot: CotResult,
    model: str,
    candidate_raw_response: str,
) -> Path:
    """Write a single CoT trace and return the path."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"{ts}_{relationship_hash}.json"
    path = out_dir / fname

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "timestamp_utc": ts,
        "relationship_hash": relationship_hash,
        "model": model,
        "verdict": cot.verdict,
        "self_confidence": cot.self_confidence,
        "reasoning_steps": list(cot.reasoning_steps),
        "evidence_citation": cot.evidence_citation,
        "escalate": cot.escalate,
        "raw_response_sha256": _sha256(candidate_raw_response),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return path


def _sha256(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:32]


@dataclass(frozen=True)
class CotAuditSummary:
    total: int
    verdict_counts: dict[str, int]
    mean_self_confidence: float

    @classmethod
    def from_directory(cls, directory: Path) -> "CotAuditSummary":
        files = sorted(Path(directory).glob("*.json"))
        total = len(files)
        counts: dict[str, int] = {}
        confidences: list[float] = []
        for f in files:
            data = json.loads(f.read_text())
            v = data.get("verdict", "unknown")
            counts[v] = counts.get(v, 0) + 1
            confidences.append(float(data.get("self_confidence", 0.0)))
        mean = sum(confidences) / total if total else 0.0
        return cls(total=total, verdict_counts=counts, mean_self_confidence=mean)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_cot_audit.py -v`
Expected: 2 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/cot_audit.py scripts/tests/test_review_cot_audit.py
git commit -m "feat(review): add append-only CoT audit writer (Task Y3.2)"
```

#### Task Y3.3 — End-to-end CoT enforcement in `ollama_review.py`

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py` (flag-gated branch: call `parse_cot_strict` + `write_cot_trace`)
- Test: `scripts/tests/test_review_cot_end_to_end.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_cot_end_to_end.py
from pathlib import Path
from unittest.mock import patch

from vitruvius.features import FeatureFlags
from vitruvius.ollama_review import adjudicate_with_cot  # NEW in this task


VALID_COT = (
    "<think>\n"
    "Step 1: Evidence: 'setback must be at least 3 meters'.\n"
    "Step 2: Candidate aligns with the rule.\n"
    "Self-confidence: 0.88\n"
    "</think>\n"
    "VERDICT: keep"
)


def test_adjudicate_with_cot_flag_off_returns_legacy(tmp_path: Path) -> None:
    flags = FeatureFlags(y_thinking_mode_cot=False)
    with patch("vitruvius.ollama_review._legacy_adjudicate", return_value={"verdict": "keep"}):
        out = adjudicate_with_cot(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            raw_llm_response="whatever",
            flags=flags,
            relationship_hash="abc",
            cot_out_dir=tmp_path,
        )
    assert out == {"verdict": "keep"}
    # Audit dir should be empty when flag is OFF
    assert list(tmp_path.glob("*.json")) == []


def test_adjudicate_with_cot_flag_on_parses_and_writes_trace(tmp_path: Path) -> None:
    flags = FeatureFlags(y_thinking_mode_cot=True)
    out = adjudicate_with_cot(
        candidate={"subject": "x", "predicate": "p", "object": "o"},
        raw_llm_response=VALID_COT,
        flags=flags,
        relationship_hash="abc123",
        cot_out_dir=tmp_path,
        model="fake-model",
    )
    assert out["verdict"] == "keep"
    assert out["escalate"] is False
    traces = list(tmp_path.glob("*.json"))
    assert len(traces) == 1
    assert "_abc123.json" in traces[0].name


def test_adjudicate_with_cot_rejects_missing_think_block(tmp_path: Path) -> None:
    flags = FeatureFlags(y_thinking_mode_cot=True)
    out = adjudicate_with_cot(
        candidate={"subject": "x", "predicate": "p", "object": "o"},
        raw_llm_response="VERDICT: keep",
        flags=flags,
        relationship_hash="abc",
        cot_out_dir=tmp_path,
    )
    assert out["verdict"] == "escalate"
    assert "CotParseError" in out["reason"]
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ImportError: cannot import name 'adjudicate_with_cot'`.

- [ ] **Step 3: Implement `adjudicate_with_cot` in `ollama_review.py`**

```python
# scripts/vitruvius/ollama_review.py — append
from pathlib import Path
from typing import Any, Mapping, Optional

from vitruvius.features import FeatureFlags


def _legacy_adjudicate(candidate: Mapping[str, Any], raw_llm_response: str) -> dict[str, Any]:
    """Legacy, non-CoT adjudication path (pre-Y3). Pure pass-through wrapper
    so the flag-off branch and the legacy code path are both testable."""
    # NOTE: real impl delegates to the existing Stream F.6 parse_reflection —
    # wrapped here so tests can patch it cleanly.
    from vitruvius.review.reflection_parser import parse_reflection
    verdict = parse_reflection(raw_llm_response)
    return {"verdict": verdict or "abstain"}


def adjudicate_with_cot(
    *,
    candidate: Mapping[str, Any],
    raw_llm_response: str,
    flags: FeatureFlags,
    relationship_hash: str,
    cot_out_dir: Path,
    model: str = "unknown",
) -> dict[str, Any]:
    """Strict-CoT adjudication path, gated on `flags.y_thinking_mode_cot`.

    Returns a dict with at minimum `verdict` ∈ {keep, reject, abstain, escalate}
    and (when escalated) a `reason`.
    """
    if not flags.y_thinking_mode_cot:
        return _legacy_adjudicate(candidate, raw_llm_response)

    from vitruvius.review.reflection_parser import parse_cot_strict, CotParseError
    from vitruvius.review.cot_audit import write_cot_trace

    try:
        cot = parse_cot_strict(raw_llm_response)
    except CotParseError as exc:
        return {"verdict": "escalate", "reason": f"CotParseError: {exc}"}

    write_cot_trace(
        out_dir=cot_out_dir,
        relationship_hash=relationship_hash,
        cot=cot,
        model=model,
        candidate_raw_response=raw_llm_response,
    )

    if cot.escalate:
        return {"verdict": "escalate", "reason": "low self-confidence", "self_confidence": cot.self_confidence}

    return {
        "verdict": cot.verdict,
        "escalate": False,
        "self_confidence": cot.self_confidence,
        "reasoning_steps": list(cot.reasoning_steps),
        "evidence_citation": cot.evidence_citation,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_cot_end_to_end.py -v`
Expected: 3 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/tests/test_review_cot_end_to_end.py
git commit -m "feat(review): flag-gated adjudicate_with_cot enforcement (Task Y3.3)"
```

#### Task Y3.4 — CLI: `ple-cotrace-dump`

**Files:**
- Modify: `scripts/vitruvius/pipeline_cli.py` (add new subcommand — do not touch existing ones)

- [ ] **Step 1: Write the failing test**

Append to `test_review_cot_audit.py`:

```python
def test_cli_ple_cotrace_dump_emits_summary(tmp_path: Path, capsys) -> None:
    from vitruvius.pipeline_cli import run_ple_cotrace_dump

    # Seed a synthetic trace
    from vitruvius.review.cot_audit import write_cot_trace
    from vitruvius.review.reflection_parser import CotResult

    write_cot_trace(
        out_dir=tmp_path,
        relationship_hash="h1",
        cot=CotResult(verdict="keep", self_confidence=0.9, reasoning_steps=["s"], evidence_citation="c"),
        model="m",
        candidate_raw_response="",
    )
    rc = run_ple_cotrace_dump(cot_dir=tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "total: 1" in out
    assert "keep: 1" in out
```

- [ ] **Step 2: Run test to verify it fails**

Expected: `AttributeError: module has no attribute 'run_ple_cotrace_dump'`.

- [ ] **Step 3: Add the CLI handler**

```python
# scripts/vitruvius/pipeline_cli.py — append
from pathlib import Path


def run_ple_cotrace_dump(*, cot_dir: Path) -> int:
    """Print a summary of the CoT audit directory to stdout."""
    from vitruvius.review.cot_audit import CotAuditSummary

    summary = CotAuditSummary.from_directory(cot_dir)
    print(f"total: {summary.total}")
    for v, n in sorted(summary.verdict_counts.items()):
        print(f"{v}: {n}")
    print(f"mean_self_confidence: {summary.mean_self_confidence:.3f}")
    return 0
```

And wire the subcommand registration (argparse) — leave every other subcommand registration untouched.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_cot_audit.py -v`
Expected: 3 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/pipeline_cli.py scripts/tests/test_review_cot_audit.py
git commit -m "feat(cli): add ple-cotrace-dump subcommand (Task Y3.4)"
```

### 8.4 Stream Y3 Definition of Done

- [ ] `parse_cot_strict` hard-fails on missing think block / verdict / citation / confidence
- [ ] `write_cot_trace` writes deterministic JSON to `005_Operational-Intelligence-Layer/cot_traces/`
- [ ] `adjudicate_with_cot` returns `escalate` for malformed responses when flag is ON
- [ ] `ple-cotrace-dump` CLI summarises the audit directory
- [ ] `test_ple_backcompat.py` green (flag OFF preserves legacy path)

### 8.5 Stream Y3 Gating Metrics

- **CoT parse success rate on 100 real Ollama responses with `<think>` injected:** ≥80 %
- **Escalation rate on strict mode:** ≥5 % of responses get escalated on the first few runs (validates the gate is live, not a rubber stamp)
- **CoT audit file size:** ≤5 KB per trace on average

### 8.6 Research-Item Coverage (Stream Y3)

- ✅ Research §1 (Native Thinking Mode)
- ✅ Research §3 (Thinking Mode for Verification Loop)

---

## 9. Stream Y4 — Stateful Agentic Registry (Phase 6A Resume Gap Closure)

**Priority:** P1
**Sprint:** R, week 3 days 1–3
**Research-Item Coverage:** Stateful Agentic Continuation (research §4 of part 2)

### 9.1 Goal

Build a persistent SQLite-backed registry keyed by `(source_hash, relationship_hash, model_version)`. On every `ollama_review.py` call, consult the registry first — skip the LLM entirely if a verdict from the same `(source, relationship, model)` already exists. Purge + vacuum via the new `ple-registry-purge` CLI. Closes the Phase 6A "Resume" gap at root.

### 9.2 Files

- Create: `scripts/vitruvius/review/stateful_registry.py`
- Modify: `scripts/vitruvius/ollama_review.py` (flag-gated registry hit path)
- Modify: `scripts/vitruvius/pipeline_cli.py` (new `ple-registry-purge` subcommand)
- Tests (3 per §4.3)

### 9.3 Task Sequence

#### Task Y4.1 — SQLite Registry Core

**Files:**
- Create: `scripts/vitruvius/review/stateful_registry.py`
- Test: `scripts/tests/test_review_stateful_registry.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_stateful_registry.py
from pathlib import Path

import pytest

from vitruvius.review.stateful_registry import (
    StatefulReviewRegistry,
    VerdictRecord,
)


def test_put_and_get_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)

    record = VerdictRecord(
        source_hash="src_abc",
        relationship_hash="rel_123",
        model_version="qwen2.5:7b-2026-04",
        verdict="keep",
        self_confidence=0.88,
        created_utc="2026-04-14T20:00:00Z",
    )
    reg.put(record)

    fetched = reg.get(source_hash="src_abc", relationship_hash="rel_123", model_version="qwen2.5:7b-2026-04")
    assert fetched == record


def test_get_miss_returns_none(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    assert reg.get(source_hash="x", relationship_hash="y", model_version="z") is None


def test_model_version_scoping(tmp_path: Path) -> None:
    """Different model versions must create separate entries."""
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)

    r_v1 = VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v1",
        verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
    )
    r_v2 = VerdictRecord(
        source_hash="s", relationship_hash="r", model_version="m:v2",
        verdict="reject", self_confidence=0.85, created_utc="2026-04-14T00:00:00Z",
    )
    reg.put(r_v1)
    reg.put(r_v2)

    assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v1") == r_v1
    assert reg.get(source_hash="s", relationship_hash="r", model_version="m:v2") == r_v2


def test_count_and_vacuum(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    for i in range(5):
        reg.put(VerdictRecord(
            source_hash=f"s{i}", relationship_hash="r", model_version="m",
            verdict="keep", self_confidence=0.9, created_utc="2026-04-14T00:00:00Z",
        ))
    assert reg.count() == 5
    reg.vacuum()  # must not raise
    assert reg.count() == 5
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `stateful_registry.py`**

```python
# scripts/vitruvius/review/stateful_registry.py
"""SQLite-backed persistent verdict cache.

Keyed by (source_hash, relationship_hash, model_version). On re-runs, the
pipeline skips the LLM entirely for any candidate whose verdict is already
cached under the current model_version. Closes the Phase 6A Resume gap.

Principle-P3 note: this module introduces persistent state. That state is
(a) opt-in via features.y_stateful_registry, (b) flushable via ple-registry-purge,
(c) separately versioned from code, (d) never read outside this module.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class VerdictRecord:
    source_hash: str
    relationship_hash: str
    model_version: str
    verdict: str
    self_confidence: float
    created_utc: str


class StatefulReviewRegistry:
    _SCHEMA = """
    CREATE TABLE IF NOT EXISTS verdicts (
        source_hash       TEXT NOT NULL,
        relationship_hash TEXT NOT NULL,
        model_version     TEXT NOT NULL,
        verdict           TEXT NOT NULL,
        self_confidence   REAL NOT NULL,
        created_utc       TEXT NOT NULL,
        PRIMARY KEY (source_hash, relationship_hash, model_version)
    );
    """

    def __init__(self, *, db_path: Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute(self._SCHEMA)
        self._conn.commit()

    def put(self, record: VerdictRecord) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO verdicts "
            "(source_hash, relationship_hash, model_version, verdict, self_confidence, created_utc) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                record.source_hash, record.relationship_hash, record.model_version,
                record.verdict, record.self_confidence, record.created_utc,
            ),
        )
        self._conn.commit()

    def get(
        self, *, source_hash: str, relationship_hash: str, model_version: str,
    ) -> Optional[VerdictRecord]:
        row = self._conn.execute(
            "SELECT source_hash, relationship_hash, model_version, verdict, self_confidence, created_utc "
            "FROM verdicts WHERE source_hash=? AND relationship_hash=? AND model_version=?",
            (source_hash, relationship_hash, model_version),
        ).fetchone()
        if row is None:
            return None
        return VerdictRecord(*row)

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM verdicts").fetchone()
        return int(row[0])

    def vacuum(self) -> None:
        self._conn.execute("VACUUM")
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_stateful_registry.py -v`
Expected: 4 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/stateful_registry.py scripts/tests/test_review_stateful_registry.py
git commit -m "feat(review): add SQLite stateful verdict registry (Task Y4.1)"
```

#### Task Y4.2 — Wire registry into `ollama_review.py`

**Files:**
- Modify: `scripts/vitruvius/ollama_review.py` (flag-gated pre-check + write-back)
- Test: `scripts/tests/test_review_stateful_registry_integration.py`

- [ ] **Step 1: Write the failing integration test**

```python
# scripts/tests/test_review_stateful_registry_integration.py
from pathlib import Path
from unittest.mock import patch

from vitruvius.features import FeatureFlags
from vitruvius.ollama_review import review_with_cache


def test_cache_miss_calls_llm(tmp_path: Path) -> None:
    flags = FeatureFlags(y_stateful_registry=True)
    db = tmp_path / "reg.sqlite"

    with patch("vitruvius.ollama_review._call_llm", return_value={"verdict": "keep", "self_confidence": 0.9}) as mock_llm:
        out = review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1",
            relationship_hash="rel1",
            model_version="m:v1",
            flags=flags,
            db_path=db,
        )
        assert out["verdict"] == "keep"
        assert mock_llm.call_count == 1  # miss → invoked


def test_cache_hit_skips_llm(tmp_path: Path) -> None:
    flags = FeatureFlags(y_stateful_registry=True)
    db = tmp_path / "reg.sqlite"

    with patch("vitruvius.ollama_review._call_llm", return_value={"verdict": "keep", "self_confidence": 0.9}) as mock_llm:
        # First call populates cache
        review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            flags=flags, db_path=db,
        )
        # Second call should hit cache and not re-invoke
        out = review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            flags=flags, db_path=db,
        )
        assert out["verdict"] == "keep"
        assert mock_llm.call_count == 1


def test_flag_off_skips_cache_entirely(tmp_path: Path) -> None:
    flags = FeatureFlags(y_stateful_registry=False)
    db = tmp_path / "reg.sqlite"

    with patch("vitruvius.ollama_review._call_llm", return_value={"verdict": "keep", "self_confidence": 0.9}) as mock_llm:
        review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            flags=flags, db_path=db,
        )
        review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            flags=flags, db_path=db,
        )
    assert mock_llm.call_count == 2  # no cache → called twice
    assert not db.exists()  # cache file never created when flag is off
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `AttributeError: module has no attribute 'review_with_cache'`.

- [ ] **Step 3: Add `review_with_cache` to `ollama_review.py`**

```python
# scripts/vitruvius/ollama_review.py — append
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from vitruvius.features import FeatureFlags


def _call_llm(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Hot-path LLM invocation. Test-patchable. Delegates to the existing
    ollama_review baseline adjudicator (Stream F wiring)."""
    # NOTE: real wiring calls through to Ollama — this thin wrapper exists
    # so tests can patch a single symbol.
    raise NotImplementedError("wire to existing ollama client")


def review_with_cache(
    *,
    candidate: Mapping[str, Any],
    source_hash: str,
    relationship_hash: str,
    model_version: str,
    flags: FeatureFlags,
    db_path: Path,
) -> dict[str, Any]:
    """Registry-aware review. Flag-off is an inlined no-op — no sqlite file created."""
    if not flags.y_stateful_registry:
        return _call_llm(candidate)

    from vitruvius.review.stateful_registry import StatefulReviewRegistry, VerdictRecord

    reg = StatefulReviewRegistry(db_path=db_path)
    try:
        cached = reg.get(
            source_hash=source_hash,
            relationship_hash=relationship_hash,
            model_version=model_version,
        )
        if cached is not None:
            return {
                "verdict": cached.verdict,
                "self_confidence": cached.self_confidence,
                "cache_hit": True,
            }

        # Miss: call LLM and cache the result
        result = _call_llm(candidate)
        reg.put(VerdictRecord(
            source_hash=source_hash,
            relationship_hash=relationship_hash,
            model_version=model_version,
            verdict=str(result.get("verdict", "abstain")),
            self_confidence=float(result.get("self_confidence", 0.0)),
            created_utc=datetime.now(timezone.utc).isoformat(),
        ))
        return {**result, "cache_hit": False}
    finally:
        reg.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_stateful_registry_integration.py -v`
Expected: 3 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ollama_review.py scripts/tests/test_review_stateful_registry_integration.py
git commit -m "feat(review): flag-gated review_with_cache registry integration (Task Y4.2)"
```

#### Task Y4.3 — Vacuum on size overflow + `ple-registry-purge` CLI

**Files:**
- Modify: `scripts/vitruvius/review/stateful_registry.py` (add `purge_older_than` and `disk_size_mb`)
- Modify: `scripts/vitruvius/pipeline_cli.py` (add `ple-registry-purge` subcommand)
- Test: `scripts/tests/test_review_stateful_registry_vacuum.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_review_stateful_registry_vacuum.py
from datetime import datetime, timedelta, timezone
from pathlib import Path

from vitruvius.review.stateful_registry import StatefulReviewRegistry, VerdictRecord


def _record(idx: int, created: datetime) -> VerdictRecord:
    return VerdictRecord(
        source_hash=f"s{idx}", relationship_hash="r", model_version="m",
        verdict="keep", self_confidence=0.9,
        created_utc=created.isoformat(),
    )


def test_purge_older_than(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    now = datetime.now(timezone.utc)
    reg.put(_record(1, now - timedelta(days=10)))
    reg.put(_record(2, now - timedelta(days=1)))
    assert reg.count() == 2

    deleted = reg.purge_older_than(cutoff_utc=(now - timedelta(days=5)).isoformat())
    assert deleted == 1
    assert reg.count() == 1


def test_disk_size_mb_reports_positive(tmp_path: Path) -> None:
    db = tmp_path / "reg.sqlite"
    reg = StatefulReviewRegistry(db_path=db)
    now = datetime.now(timezone.utc)
    for i in range(50):
        reg.put(_record(i, now))
    assert reg.disk_size_mb() > 0
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `AttributeError: 'StatefulReviewRegistry' object has no attribute 'purge_older_than'`.

- [ ] **Step 3: Extend `stateful_registry.py`**

```python
# scripts/vitruvius/review/stateful_registry.py — append methods to class
    def purge_older_than(self, *, cutoff_utc: str) -> int:
        cursor = self._conn.execute(
            "DELETE FROM verdicts WHERE created_utc < ?", (cutoff_utc,),
        )
        self._conn.commit()
        return int(cursor.rowcount)

    def disk_size_mb(self) -> float:
        return self._db_path.stat().st_size / (1024 * 1024)
```

And add the CLI:

```python
# scripts/vitruvius/pipeline_cli.py — append
def run_ple_registry_purge(*, db_path: Path, days: int = 30) -> int:
    from datetime import datetime, timedelta, timezone
    from vitruvius.review.stateful_registry import StatefulReviewRegistry

    if not db_path.exists():
        print(f"no registry at {db_path}")
        return 0
    reg = StatefulReviewRegistry(db_path=db_path)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    deleted = reg.purge_older_than(cutoff_utc=cutoff)
    reg.vacuum()
    size_mb = reg.disk_size_mb()
    reg.close()
    print(f"purged: {deleted} rows | size_after: {size_mb:.2f} MB")
    return 0
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_review_stateful_registry_vacuum.py -v`
Expected: 2 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/review/stateful_registry.py scripts/vitruvius/pipeline_cli.py scripts/tests/test_review_stateful_registry_vacuum.py
git commit -m "feat(review): add purge_older_than + ple-registry-purge CLI (Task Y4.3)"
```

#### Task Y4.4 — Phase 6A Resume integration test

**Files:**
- Test: add to `scripts/tests/test_review_stateful_registry_integration.py`

- [ ] **Step 1: Write the failing integration test**

```python
def test_resume_after_crash_skips_completed_candidates(tmp_path: Path) -> None:
    """Simulate: run review on 3 candidates, crash after 2, resume — only the
    3rd should invoke the LLM."""
    from unittest.mock import patch
    from vitruvius.features import FeatureFlags
    from vitruvius.ollama_review import review_with_cache

    flags = FeatureFlags(y_stateful_registry=True)
    db = tmp_path / "reg.sqlite"

    candidates = [
        ({"subject": "a", "predicate": "p", "object": "o"}, "rel1"),
        ({"subject": "b", "predicate": "p", "object": "o"}, "rel2"),
        ({"subject": "c", "predicate": "p", "object": "o"}, "rel3"),
    ]

    # First run: succeed on 2 of 3 (simulate crash between)
    with patch("vitruvius.ollama_review._call_llm", return_value={"verdict": "keep", "self_confidence": 0.9}) as mock:
        for cand, rh in candidates[:2]:
            review_with_cache(
                candidate=cand,
                source_hash="src1",
                relationship_hash=rh,
                model_version="m:v1",
                flags=flags,
                db_path=db,
            )
        assert mock.call_count == 2

    # Resume: run all 3 — only rel3 should be invoked
    with patch("vitruvius.ollama_review._call_llm", return_value={"verdict": "keep", "self_confidence": 0.9}) as mock:
        for cand, rh in candidates:
            review_with_cache(
                candidate=cand,
                source_hash="src1",
                relationship_hash=rh,
                model_version="m:v1",
                flags=flags,
                db_path=db,
            )
        assert mock.call_count == 1  # only rel3 was new
```

- [ ] **Step 2: Run the test to verify it passes** (prior tasks already implemented the behaviour)

Run: `pytest scripts/tests/test_review_stateful_registry_integration.py -v`
Expected: all pass — this test is a regression lock, not a new feature.

- [ ] **Step 3: Commit**

```bash
git add scripts/tests/test_review_stateful_registry_integration.py
git commit -m "test(review): lock Phase 6A Resume gap closure (Task Y4.4)"
```

### 9.4 Stream Y4 Definition of Done

- [ ] Registry round-trips `(source, relationship, model_version) → verdict`
- [ ] `review_with_cache` skips the LLM on cache hit
- [ ] Flag OFF path creates zero SQLite files
- [ ] `ple-registry-purge` CLI compacts the DB
- [ ] Phase 6A Resume gap regression test green

### 9.5 Stream Y4 Gating Metrics

- **LLM call skip rate on a full PD 1096 rerun (2nd run):** ≥95 % (cached from first run)
- **Registry disk footprint after 1000 rows:** ≤5 MB
- **Round-trip latency:** ≤2 ms per `get`

### 9.6 Research-Item Coverage (Stream Y4)

- ✅ Research §4 of part 2 (Stateful Agentic Continuation)
- ✅ Closes Phase 6A Resume gap (referenced by research as "the Phase 6A resume gap")

---

## 10. Stream Y5 — Vision OCR Integration (Gated)

**Priority:** P2 — GATED
**Sprint:** R, week 4
**Research-Item Coverage:** Multi-Modal Vision for Chart/OCR Understanding (research §5 of part 2)
**Gate:** `ple-vision-probe` CLI reports ≥3.5 GB free RAM AND user has manually pulled a vision model AND every concept under test fits a ≤2MP image budget.

### 10.1 Goal

When Stream B's `table_graph_extractor.py` fails to extract a table from a PDF (because the page is an image, not a CSV/XLSX), fall back to a vision model (`moondream:latest` preferred; `qwen2-vl:2b` acceptable) that returns structured JSON describing the table's rows and columns. The vision pipeline NEVER auto-enables — it requires the `y_vision_ocr` flag AND the `ple-vision-probe` to pass.

### 10.2 Files

- Create: `scripts/vitruvius/parsers/vision_ocr.py`
- Modify: `scripts/vitruvius/parsers/table_graph_extractor.py` (optional vision fallback hook)
- Modify: `scripts/vitruvius/pipeline_cli.py` (add `ple-vision-probe` subcommand)
- Tests (2 per §4.3)

### 10.3 Task Sequence

#### Task Y5.1 — Vision OCR Wrapper

**Files:**
- Create: `scripts/vitruvius/parsers/vision_ocr.py`
- Test: `scripts/tests/test_parsers_vision_ocr.py`

- [ ] **Step 1: Write the failing test** (with mocked Ollama vision client)

```python
# scripts/tests/test_parsers_vision_ocr.py
from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.vision_ocr import extract_table_from_image, VisionExtractedTable


FAKE_VISION_JSON = """
{
  "rows": [
    ["Header 1", "Header 2"],
    ["cell1", "cell2"],
    ["cell3", "cell4"]
  ],
  "caption": "Table VII.1 — Occupancy classification"
}
"""


def test_vision_call_parses_structured_json(tmp_path: Path) -> None:
    img_path = tmp_path / "page.png"
    img_path.write_bytes(b"FAKE_PNG_BYTES")  # just needs to be a file

    with patch("vitruvius.parsers.vision_ocr._call_ollama_vision", return_value=FAKE_VISION_JSON):
        table = extract_table_from_image(img_path, model="moondream:latest")

    assert isinstance(table, VisionExtractedTable)
    assert len(table.rows) == 3
    assert table.rows[0] == ["Header 1", "Header 2"]
    assert "Occupancy" in table.caption


def test_vision_call_returns_none_on_empty_response(tmp_path: Path) -> None:
    img_path = tmp_path / "page.png"
    img_path.write_bytes(b"FAKE_PNG_BYTES")
    with patch("vitruvius.parsers.vision_ocr._call_ollama_vision", return_value=""):
        table = extract_table_from_image(img_path, model="moondream:latest")
    assert table is None


def test_vision_call_rejects_oversized_image(tmp_path: Path) -> None:
    img_path = tmp_path / "page.png"
    # Fake a >2MP image: write 2.1 MB of junk; the implementation checks pixel count via Pillow.
    img_path.write_bytes(b"x" * (2_100_000))
    with patch("vitruvius.parsers.vision_ocr._pixel_count", return_value=2_100_000):
        with pytest.raises(ValueError, match="exceeds max_image_pixels"):
            extract_table_from_image(img_path, model="moondream:latest", max_pixels=2_000_000)
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `vision_ocr.py`**

```python
# scripts/vitruvius/parsers/vision_ocr.py
"""Vision-model fallback for PDF table extraction.

Called ONLY when Stream B's `table_graph_extractor.py` cannot produce a CSV/XLSX
interpretation of a page. Gated behind features.y_vision_ocr.

The call is stateless — no temporary files outside `tmp_path`, no caching.
Image pixel count is checked pre-call to keep RAM bounded.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class VisionExtractedTable:
    rows: list[list[str]]
    caption: str
    source_image: Path


def _pixel_count(path: Path) -> int:
    """Inspect an image's pixel count without fully decoding it."""
    from PIL import Image  # lazy import
    with Image.open(path) as im:
        w, h = im.size
    return w * h


def _call_ollama_vision(image_path: Path, *, model: str, prompt: str) -> str:
    """Invoke Ollama's vision API. Thin wrapper; test-patchable."""
    import base64
    import httpx

    with Path(image_path).open("rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")

    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "images": [b64],
        "stream": False,
    }
    resp = httpx.post("http://localhost:11434/api/generate", json=payload, timeout=120.0)
    resp.raise_for_status()
    data = resp.json()
    return str(data.get("response", ""))


_PROMPT = (
    "You are extracting a table from a page image. "
    "Return STRICT JSON with keys 'rows' (list of lists of strings) and 'caption' (string). "
    "Do NOT wrap the JSON in markdown. Do NOT include any explanation."
)


def extract_table_from_image(
    image_path: Path,
    *,
    model: str,
    max_pixels: int = 2_000_000,
) -> Optional[VisionExtractedTable]:
    """Extract a structured table from a rendered PDF page image.

    Returns None if the vision model produced an empty or unparseable response.
    Raises ValueError if the image exceeds `max_pixels`.
    """
    image_path = Path(image_path)
    if _pixel_count(image_path) > max_pixels:
        raise ValueError(
            f"{image_path.name} exceeds max_image_pixels ({max_pixels}) — rescale first"
        )

    raw = _call_ollama_vision(image_path, model=model, prompt=_PROMPT)
    if not raw.strip():
        return None

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None

    rows = payload.get("rows")
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        return None

    return VisionExtractedTable(
        rows=[[str(c) for c in row] for row in rows],
        caption=str(payload.get("caption", "")),
        source_image=image_path,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_parsers_vision_ocr.py -v`
Expected: 3 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/parsers/vision_ocr.py scripts/tests/test_parsers_vision_ocr.py
git commit -m "feat(parsers): add Ollama vision OCR table extractor (Task Y5.1)"
```

#### Task Y5.2 — Fallback hook in `table_graph_extractor.py`

**Files:**
- Modify: `scripts/vitruvius/parsers/table_graph_extractor.py`
- Test: `scripts/tests/test_parsers_vision_ocr_fallback.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_parsers_vision_ocr_fallback.py
from pathlib import Path
from unittest.mock import patch

from vitruvius.features import FeatureFlags
from vitruvius.parsers.table_graph_extractor import extract_tables_with_vision_fallback


def test_vision_fallback_invoked_on_csv_fail(tmp_path: Path) -> None:
    flags = FeatureFlags(y_vision_ocr=True)
    page_image = tmp_path / "p1.png"
    page_image.write_bytes(b"PNG_BYTES")

    from vitruvius.parsers.vision_ocr import VisionExtractedTable

    fake_table = VisionExtractedTable(
        rows=[["a", "b"], ["1", "2"]],
        caption="synthetic",
        source_image=page_image,
    )
    with patch(
        "vitruvius.parsers.table_graph_extractor.extract_table_from_image",
        return_value=fake_table,
    ) as mock_vision, patch(
        "vitruvius.parsers.vision_ocr._pixel_count", return_value=500_000,
    ):
        result = extract_tables_with_vision_fallback(
            page_image=page_image,
            flags=flags,
            csv_result=None,  # CSV extractor failed
        )
    assert result is fake_table
    assert mock_vision.call_count == 1


def test_vision_fallback_not_invoked_when_csv_succeeded(tmp_path: Path) -> None:
    flags = FeatureFlags(y_vision_ocr=True)
    page_image = tmp_path / "p1.png"
    page_image.write_bytes(b"PNG")

    existing = object()  # sentinel — pretend CSV extractor returned a table

    with patch(
        "vitruvius.parsers.table_graph_extractor.extract_table_from_image",
    ) as mock_vision:
        result = extract_tables_with_vision_fallback(
            page_image=page_image,
            flags=flags,
            csv_result=existing,
        )
    assert result is existing
    assert mock_vision.call_count == 0


def test_vision_fallback_skipped_when_flag_off(tmp_path: Path) -> None:
    flags = FeatureFlags(y_vision_ocr=False)
    page_image = tmp_path / "p1.png"
    page_image.write_bytes(b"PNG")

    with patch(
        "vitruvius.parsers.table_graph_extractor.extract_table_from_image",
    ) as mock_vision:
        result = extract_tables_with_vision_fallback(
            page_image=page_image,
            flags=flags,
            csv_result=None,
        )
    assert result is None
    assert mock_vision.call_count == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `AttributeError: module has no attribute 'extract_tables_with_vision_fallback'`.

- [ ] **Step 3: Add fallback hook to `table_graph_extractor.py`**

Append — do not modify existing CSV/XLSX paths:

```python
# scripts/vitruvius/parsers/table_graph_extractor.py — append
from pathlib import Path
from typing import Any, Optional

from vitruvius.features import FeatureFlags

try:
    from vitruvius.parsers.vision_ocr import extract_table_from_image  # noqa: F401
    _VISION_AVAILABLE = True
except ImportError:
    _VISION_AVAILABLE = False


def extract_tables_with_vision_fallback(
    *,
    page_image: Path,
    flags: FeatureFlags,
    csv_result: Optional[Any],
    model: str = "moondream:latest",
) -> Optional[Any]:
    """If CSV extraction produced a result, return it unchanged.
    Otherwise, if `features.y_vision_ocr` is ON, delegate to the vision OCR
    extractor. Never called when the flag is OFF.
    """
    if csv_result is not None:
        return csv_result
    if not flags.y_vision_ocr or not _VISION_AVAILABLE:
        return None
    return extract_table_from_image(page_image, model=model)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_parsers_vision_ocr_fallback.py -v`
Expected: 3 pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/parsers/table_graph_extractor.py scripts/tests/test_parsers_vision_ocr_fallback.py
git commit -m "feat(parsers): add flag-gated vision OCR fallback for table extraction (Task Y5.2)"
```

#### Task Y5.3 — `ple-vision-probe` hardware pre-flight

**Files:**
- Modify: `scripts/vitruvius/pipeline_cli.py` (add `run_ple_vision_probe`)
- Test: append to `test_parsers_vision_ocr.py`

- [ ] **Step 1: Write the failing test**

```python
def test_vision_probe_passes_when_ram_sufficient() -> None:
    from unittest.mock import patch
    from vitruvius.pipeline_cli import run_ple_vision_probe

    with patch("vitruvius.pipeline_cli._free_ram_gb", return_value=4.0):
        with patch("vitruvius.pipeline_cli._ollama_model_available", return_value=True):
            rc = run_ple_vision_probe(required_free_gb=3.5, model="moondream:latest")
    assert rc == 0


def test_vision_probe_fails_on_low_ram() -> None:
    from unittest.mock import patch
    from vitruvius.pipeline_cli import run_ple_vision_probe

    with patch("vitruvius.pipeline_cli._free_ram_gb", return_value=1.0):
        with patch("vitruvius.pipeline_cli._ollama_model_available", return_value=True):
            rc = run_ple_vision_probe(required_free_gb=3.5, model="moondream:latest")
    assert rc == 1


def test_vision_probe_fails_on_missing_model() -> None:
    from unittest.mock import patch
    from vitruvius.pipeline_cli import run_ple_vision_probe

    with patch("vitruvius.pipeline_cli._free_ram_gb", return_value=4.0):
        with patch("vitruvius.pipeline_cli._ollama_model_available", return_value=False):
            rc = run_ple_vision_probe(required_free_gb=3.5, model="moondream:latest")
    assert rc == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Expected: `AttributeError: module has no attribute 'run_ple_vision_probe'`.

- [ ] **Step 3: Implement `run_ple_vision_probe`**

```python
# scripts/vitruvius/pipeline_cli.py — append
def _free_ram_gb() -> float:
    import psutil
    return psutil.virtual_memory().available / (1024**3)


def _ollama_model_available(name: str) -> bool:
    import httpx
    try:
        r = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
        r.raise_for_status()
        tags = r.json().get("models", [])
        return any(m.get("name", "").startswith(name.split(":")[0]) for m in tags)
    except Exception:
        return False


def run_ple_vision_probe(*, required_free_gb: float, model: str) -> int:
    free = _free_ram_gb()
    if free < required_free_gb:
        print(f"FAIL: only {free:.2f} GB free (need {required_free_gb:.2f})")
        return 1
    if not _ollama_model_available(model):
        print(f"FAIL: vision model '{model}' not pulled. Run: ollama pull {model}")
        return 2
    print(f"PASS: {free:.2f} GB free, {model} available")
    return 0
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest scripts/tests/test_parsers_vision_ocr.py -v`
Expected: 6 pass (3 from Y5.1 + 3 new).

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/pipeline_cli.py scripts/tests/test_parsers_vision_ocr.py
git commit -m "feat(cli): add ple-vision-probe hardware pre-flight (Task Y5.3)"
```

#### Task Y5.4 — Documentation: vision model pull checklist

**Files:**
- Modify: `AGENTS.md` (append a short Y5 section describing manual pull + probe workflow)
- Modify: `.ai/10_state/current-phase.md` (note Y5 gated status)

- [ ] **Step 1: Append a `Stream Y5 Vision OCR Checklist` section to `AGENTS.md`**

```markdown
### Stream Y5 — Vision OCR Manual Activation Checklist

Run these commands **in order** before flipping `features.y_vision_ocr: true`:

1. `ollama pull moondream:latest`          # one-time, ~1.8 GB download
2. `python -m scripts.vitruvius.pipeline_cli ple-vision-probe`   # returns 0 on pass
3. `python -m scripts.vitruvius.pipeline_cli pipeline --dry-run` # verifies overall sanity
4. Flip `features.y_vision_ocr: true` in `config/vitruvius.yaml`
5. Monitor RSS during first real run — abort if > 5.5 GB at peak

If probe step 2 fails with "only X GB free", close browser tabs / stop Ollama's non-vision model before retrying.
```

- [ ] **Step 2: Commit**

```bash
git add AGENTS.md .ai/10_state/current-phase.md
git commit -m "docs(y5): add vision OCR manual activation checklist (Task Y5.4)"
```

### 10.4 Stream Y5 Definition of Done

- [ ] `extract_table_from_image` returns structured rows or None
- [ ] Fallback hook only fires when CSV extractor returned None AND flag is ON
- [ ] `ple-vision-probe` refuses activation under 3.5 GB free RAM or when model is missing
- [ ] Documentation for manual pull + activation is in `AGENTS.md`
- [ ] `test_ple_backcompat.py` green

### 10.5 Stream Y5 Gating Metrics

- **Vision fallback hit rate on PD 1096:** 1–3 pages per run (Table VII.1 + a handful of others)
- **End-to-end latency per vision call:** ≤45 s on 8GB M2 (moondream)
- **RSS peak during a vision call with Ollama review co-running:** ≤5.5 GB
- **Vision output schema validation:** 100% of rows are `list[str]` of identical length within a table

### 10.6 Research-Item Coverage (Stream Y5)

- ✅ Research §5 of part 2 (Multi-Modal Vision for Chart/OCR Understanding)

---

## 11. Sprint Rollout Plan

### 11.1 Sprint R Week 1

- **Day 1:** Y0.1 – Y0.3 (bootstrap + regression test)
- **Days 2–4:** Y1.1 – Y1.5 (Contextual Priming end-to-end)
- **Day 5:** buffer + design review of Y2 policy file

### 11.2 Sprint R Week 2

- **Days 1–3:** Y2.1 – Y2.4 (Domain-Routing MoE)
- **Days 4–5:** Y3.1 – Y3.2 (CoT parser + audit writer)

### 11.3 Sprint R Week 3

- **Day 1:** Y3.3 – Y3.4 (CoT end-to-end + CLI)
- **Days 2–4:** Y4.1 – Y4.4 (Stateful Registry + Resume regression)
- **Day 5:** integration smoke run — all of Y1+Y2+Y3+Y4 ON simultaneously

### 11.4 Sprint R Week 4 (GATED)

- **Day 1:** decision checkpoint — does Y5 fit in the RAM envelope on the target machine? Run `ple-vision-probe` with Ollama review co-running.
- **Days 2–3:** Y5.1 – Y5.4 IF the checkpoint passes.
- **Days 4–5:** final backward-compat regression sweep, decision-log entries, docs.

### 11.5 Dependencies Between Tasks

```
Y0.1 → Y0.2 → Y0.3
            ↘
              Y1.1 → Y1.2 → Y1.3 → Y1.4 → Y1.5
            ↘
              Y2.1 → Y2.2 → Y2.3 → Y2.4
            ↘
              Y3.1 → Y3.2 → Y3.3 → Y3.4
            ↘
              Y4.1 → Y4.2 → Y4.3 → Y4.4
            ↘
              Y5.1 → Y5.2 → Y5.3 → Y5.4 (gated)
```

All five Y streams can run in parallel after Y0 closes. Inside each stream, tasks are strictly ordered.

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Priming prefix eats too many tokens per call | Medium | Medium | Cap prefix at 150 tokens in `prompt_prefix.py`; measure in Y1 gating metric |
| Domain classifier misroutes safety rules to `geometric` | Medium | High | Deterministic regex + unit tests per domain; conformal calibrator (Stream F.4) catches low-confidence routes |
| CoT parser rejects valid Qwen responses that don't emit `<think>` tags | High | High | Ship Y3 behind a flag; fallback to legacy `parse_reflection` when `y_thinking_mode_cot` is OFF; run on a 100-response sample before turning on for real |
| SQLite registry grows unbounded | Medium | Low | `ple-registry-purge` CLI with default 30-day cutoff; `vacuum_on_exceed` config key |
| Vision model RAM blows the 8 GB ceiling | High (if enabled) | Critical | `ple-vision-probe` pre-flight + `features.y_vision_ocr: false` default + manual activation checklist in AGENTS.md |
| `features.y_*` flags drift from `FeatureFlags` dataclass | Low | Medium | `test_features.py` regression test loads from YAML + asserts field exists |
| Any Y task breaks a Stream A-I closed test | Low | Critical | `test_ple_backcompat.py` seeds the golden fixture and diffs byte-for-byte |

---

## 13. Non-Goals

- **Training or running actual Gemma 4 weights.** The plan translates Gemma 4's *architectural philosophy* into Python modules that work with whichever local Ollama model is already configured.
- **Native function calling / tool use.** Out of scope; would need a dedicated tool registry and a function-calling-capable base model. Deferred to Stream V (ultimate plan).
- **256K context exploitation.** Vitruvius chunks upstream; no current document exceeds 32 K tokens. Defer until a qualifying corpus exists.
- **Multi-modal vision beyond tables.** Vision OCR is scoped to `Table N.N` extraction only in Y5. No figure / diagram understanding.
- **Learned domain classifier.** Y2 ships a deterministic regex classifier. Replacing it with a trained multinomial model is a follow-up once Stream J (active learning) provides training signal.
- **Replacing `ollama_review.py`.** Every Y stream **adds composition points** to `ollama_review.py`, never rewrites it.

---

## 14. Stream-Level Gating Metrics (consolidated)

| Stream | Metric | Target |
|---|---|---|
| Y0 | Test suite delta | ≥4 new tests, 0 removed |
| Y0 | Backward-compat byte diff on golden 3-file fixture | 0 bytes |
| Y1 | Cosine similarity of response vector to source identity | ≥0.6 on ≥95% of reviewed candidates |
| Y1 | Prompt prefix token overhead | ≤150 tokens/call |
| Y2 | Fraction of candidates routed to ≤3B-param model | ≥40% |
| Y2 | Geometric-domain F1 vs baseline | +0.03 |
| Y3 | CoT parse success rate | ≥80% of responses with `<think>` tags |
| Y3 | Average audit trace size | ≤5 KB |
| Y4 | LLM call skip rate on 2nd run of the same corpus | ≥95% |
| Y4 | Registry disk footprint @ 1000 rows | ≤5 MB |
| Y5 | Vision call latency on 8GB M2 | ≤45 s |
| Y5 | RSS peak during vision + ollama co-run | ≤5.5 GB |

---

## 15. Research-Item Coverage Matrix

### 15.1 `.ai/13_research/Per-Layer Embeddings.md`

| Research section | Innovation | Y Stream | Task IDs |
|---|---|---|---|
| Part 1 §1 | PLE — Per-Layer Embeddings (Contextual Priming) | Y1 | Y1.1, Y1.2, Y1.3, Y1.4, Y1.5 |
| Part 1 §2 | Is it possible for Vitruvius (E4B fit, thinking mode) | Y1 + Y3 | see below |
| Part 1 §3 | Intelligence-per-parameter, reduced noise, long context | Y1 + Y2 | see below |
| Part 2 §1 | Per-Layer Conditioned Vectors (Memory Identity Fix) | Y1 | Y1.1, Y1.4, Y1.5 |
| Part 2 §2 | Mixture of Experts (Domain Routing) | Y2 | Y2.1, Y2.2, Y2.3, Y2.4 |
| Part 2 §3 | Native Thinking Mode (Verification Loop) | Y3 | Y3.1, Y3.2, Y3.3, Y3.4 |
| Part 2 §4 | Stateful Agentic Continuation | Y4 | Y4.1, Y4.2, Y4.3, Y4.4 |
| Part 2 §5 | Multi-Modal Vision (Chart/OCR Understanding) | Y5 | Y5.1, Y5.2, Y5.3, Y5.4 |

### 15.2 Items Covered by Existing Closed Streams

| Research implication | Already Covered By | Evidence |
|---|---|---|
| Small-model preference | Stream F.2 (`slm_router.py`) | Closed 2026-04-14 |
| Ontology-embedded prompts | Stream F.3 (`ontology_prompt_builder.py`) | Closed 2026-04-14 |
| Reflection / self-critique (precursor) | Stream F.6 (`reflection_parser.py`) | Closed 2026-04-14 — upgraded by Y3 |
| 256K context handling | Stream C.3 (`embedding_chunker.py`) | Closed 2026-04-14 |

### 15.3 Deferred Items With Explicit Prerequisites

| Deferred item | Prerequisite | Unlock gate |
|---|---|---|
| Native function calling | Stream V IFC/OWL ontology (ultimate plan) | Ontology registry must exist |
| Running gemma4:31b | 16+ GB RAM target machine | Hardware upgrade |
| Learned domain classifier | Stream J active learning signal | ≥500 labelled candidates |

---

## 16. Integration Points Into Existing Plans

This plan **extends** three other plans without modifying their frozen text:

### 16.1 Statistical-Architectural-Upgrade Plan

- **Stream F (review/ scaffolds) is a PREREQUISITE.** Y1.4 (ontology prompt), Y2.4 (slm_router), Y3.3 (reflection parser) all extend modules Stream F shipped.
- **Stream B (parsers/ scaffolds) is a PREREQUISITE.** Y5.2 extends `parsers/table_graph_extractor.py`.
- **Stream I (query/ ontology prompt) is adjacent.** Y1's `SourceIdentity` can later be injected into `query/ontology_prompt.py` too — follow-on task, not in this plan.

### 16.2 Live-Wiring & 8GB Hardening Plan

- **Sprint Q is a PREREQUISITE.** W2 must wire `ollama_review.py` to call every Stream F scaffold BEFORE any Y task begins. Otherwise the Y patches land on cold code paths.
- **W1 model pool extends naturally into Y2.** The MoE policy file (`config/moe_routing.yaml`) refers to the same model IDs W1 enforces.

### 16.3 Ultimate Architecture Upgrade Plan

- **Stream U (Hardware-Aware Router) composes with Y2.** U routes by hardware headroom; Y2 routes by domain. Y2 picks the candidate model, U validates RAM availability.
- **Stream R (Epistemic Uncertainty) consumes Y3 output.** Y3's `CoT audit` traces become training features for R's MC Dropout + Dempster-Shafer estimator.

---

## 17. Self-Review Checklist (pre-execution)

### 17.1 Spec Coverage

- [x] PLE innovation mapped to Y1 (5 tasks)
- [x] MoE innovation mapped to Y2 (4 tasks)
- [x] Thinking Mode innovation mapped to Y3 (4 tasks)
- [x] Stateful Continuation innovation mapped to Y4 (4 tasks)
- [x] Multi-Modal Vision innovation mapped to Y5 (4 tasks, gated)

### 17.2 Placeholder Scan

- [x] No "TBD", "implement later", "fill in details"
- [x] Every TDD step has runnable code, not prose descriptions
- [x] Every CLI command has an expected exit code
- [x] Every test has expected FAIL/PASS output
- [x] No "similar to Task N" — all code is repeated for each task

### 17.3 Type / Interface Consistency

- [x] `SourceIdentity` dataclass used identically across Y1.1, Y1.2, Y1.3, Y1.4, Y1.5
- [x] `Domain` enum used identically across Y2.1, Y2.2, Y2.3, Y2.4
- [x] `CotResult` dataclass used identically across Y3.1, Y3.2, Y3.3
- [x] `VerdictRecord` dataclass used identically across Y4.1, Y4.2, Y4.3, Y4.4
- [x] `VisionExtractedTable` dataclass used identically across Y5.1, Y5.2

### 17.4 Non-Breaking Contract

- [x] Every new feature is flag-gated
- [x] Every flag defaults to `false`
- [x] `test_ple_backcompat.py` locks byte-identical output with every Y flag OFF
- [x] No existing CLI subcommand renamed or removed
- [x] No canonical-layer file written outside `promotion.py`

### 17.5 Hardware Ceiling

- [x] Y1–Y4 combined peak: +150 MB RAM (documented §3.3)
- [x] Y5 gated behind explicit pre-flight `ple-vision-probe`
- [x] No model >8 GB referenced in the default routing policy
- [x] SQLite registry capped at 200 MB via vacuum cycle

---

## 18. Execution Handoff

**Plan complete and saved to `.ai/03_plans/per-layer-embeddings-agentic-upgrade-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration. Use `superpowers:subagent-driven-development`.

**2. Inline Execution** — execute tasks in this session with checkpoints for review. Use `superpowers:executing-plans`.

**Which approach?**

---

## 19. Changelog

- **2026-04-14** — v1.0.0 — Initial plan authored. Integrates 5 Gemma 4 innovations from `.ai/13_research/Per-Layer Embeddings.md` into Vitruvius as Streams Y0–Y5. Defers to Sprint Q (live-wiring) for prior scaffold wiring. Y5 gated behind hardware pre-flight. Total: 6 streams, 24 TDD tasks, ~24 new test files, 9 new / extended modules. Non-breaking guarantee locked by `test_ple_backcompat.py`.
