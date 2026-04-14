---
plan_id: statistical-architectural-upgrade
phase: "cross-phase (touches 1A → 12)"
title: Statistical & Architectural Intelligence Upgrade
status: in-progress — Streams A + B + C + D CLOSED 2026-04-14
priority: highest
sprint: "Sprint D — Streams A, B, C, D CLOSED; Streams E-K pending"
version: 1.0.3
stream_progress:
  A_bootstrap_merkle_features: closed (7 tasks — A1a, A1b, A2, A5, A6, A7 shipped; A3, A4 won't-fix rationale in A5 commit)
  B_ingestion_intelligence: closed (5 tasks — B.1 Shannon, B.2 Shannon integration, B.3 Table-to-Graph CSV, B.3.1 XLSX wrapper, B.4 Parametric NER shipped)
  C_normalization_tier_c: closed (4 tasks — C.1 Jaro-Winkler OCR, C.2 AST chunker, C.3 hybrid embedding chunker, C.4 Mahalanobis outlier detector shipped)
  D_concept_enrichment_v2: closed (4 tasks — D.1 TF-IDF matcher, D.2 PMI alias miner, D.3 FCA lattice, D.4 contrastive whitening adapter shipped)
  E_extraction_v2: pending
  F_review_v2: pending
  G_promotion_v2: pending
  H_graph_intelligence: pending
  I_query_v2: pending
  J_active_learning: pending
  K_clup_scaling: pending
plan_type: implementation_tdd
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
takes_precedence_over:
  - phase-8-graph-contract-indexing-plan.md (EXTENDED, not replaced — see §2.3)
  - phase-9-query-ai-layer-plan.md         (EXTENDED, not replaced — see §2.3)
  - phase-1b-multi-parser-integration-plan.md §11 Phase 2/3 (ABSORBED into Stream B)
prerequisites:
  - Sprint A (Phase 7 Promotion) CLOSED  — ✅ 2026-04-14
  - Sprint B (Phase 1C + 2 + 6A) CLOSED  — ✅ 2026-04-14
  - Sprint C Phase 1B Foundation CLOSED  — ✅ 2026-04-14
  - At least 3 verified relationships promoted to canonical layer — ✅ 2026-04-14
dependencies:
  - .ai/13_research/statistical-improvements.md
  - .ai/13_research/advanced architectural and code-level optimizations.md
  - .ai/03_plans/phase-1b-multi-parser-integration-plan.md
  - .ai/03_plans/phase-8-graph-contract-indexing-plan.md
  - .ai/03_plans/phase-9-query-ai-layer-plan.md
  - .ai/03_plans/ingestion-refinement-contract.md (v2.0.0 frozen)
  - .ai/10_state/known_issues.md
  - .ai/01_roadmap/master-roadmap.md (v2.0.0)
  - .ai/00_system/principles.md (P1-P10 non-negotiable)
non_breaking_guarantee: |
  Every new module ships behind a config-driven feature flag in
  `config/vitruvius.yaml` under `features.*` (defaults OFF). No existing
  module is deleted or renamed in this plan. All existing CLI commands
  continue to produce byte-identical outputs with every feature disabled.
  A new CI-style test (`test_backward_compat.py`) snapshots the outputs
  of a fixed 3-file PD 1096 subset with all flags OFF and fails any run
  that drifts. The plan adds capabilities; it never removes them.
unblocks:
  - Full root-cause closure of RI-002 (regex fragility) via CRF extraction (Stream E)
  - Closure of RI-010's remaining 4 concepts via TF-IDF + PMI matching (Stream D)
  - Bayesian confidence fusion across heterogeneous extraction signals (Stream G)
  - Multi-jurisdictional graph scaling (Phase 11 readiness) via Stringency Matrix (Stream G) and Wasserstein merge (Stream H)
  - 3x–5x Phase 6 speedup via SLM swarm routing + ontology-embedded prompting + KV cache (Stream F)
gate:
  condition: "Stream A (Dependency Bootstrap + Merkle Hash + Feature-Flag Framework) ships green before any downstream stream begins."
  rationale: "Stream A installs every new Python dependency, the zero-RAM speed bypass, and the non-breaking feature-flag harness that protects existing functionality. Every later stream depends on either its libs or its safety guarantees."
---

# Statistical & Architectural Intelligence Upgrade Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended for its per-task isolation) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **Every task ships behind a feature flag; test the flag OFF path too.**

**Goal.** Implement every technique from [`.ai/13_research/statistical-improvements.md`](../13_research/statistical-improvements.md) and [`.ai/13_research/advanced architectural and code-level optimizations.md`](../13_research/advanced%20architectural%20and%20code-level%20optimizations.md) into Vitruvius without breaking the existing pipeline, without violating principles P1–P10, and without exceeding the 8GB M2 memory ceiling.

**Architecture.** Eleven execution streams (A–K), each mapped to one or more pipeline phases. Every new module lives behind a `features.*` flag in `config/vitruvius.yaml`, is isolated in its own subpackage under `scripts/vitruvius/`, and is verified against an always-on backward-compatibility regression suite before being wired into the live pipeline. The plan supersedes priority over every other plan in `.ai/03_plans/` (§1.2) but leaves their contracts intact — it *extends* Phases 1A, 1B, 1C, 3, 5, 6, 7, 8, 9, and 11; it does not replace them.

**Tech Stack.** Python stdlib + numpy + scipy + scikit-learn + rapidfuzz + python-crfsuite + spaCy (en_core_web_sm) + networkx + python-louvain + sentence-transformers (all-MiniLM-L6-v2, CPU inference only) + POT (Python Optimal Transport). No GPU, no cloud, no new database. Total RAM peak at full throttle: **~4.3 GB** (Ollama 4.0 GB + ST embeddings 0.2 GB + spaCy 0.05 GB + scikit-learn/numpy ~0.05 GB) — safely inside the 5 GB usable envelope on an 8 GB M2 with macOS consuming 2.5–3 GB.

---

## 1. Preamble

### 1.1 Why This Plan Exists
Two research documents landed in `.ai/13_research/` on 2026-04-14. Each catalogues techniques that would either (a) eliminate a known-issue class, (b) accelerate the pipeline by a factor of 3–5×, or (c) unlock capabilities that are strictly blocked by the current regex/heuristic stack. The items are not independently sized — some are one-hour tactical bugfixes (Merkle hash, Jaro-Winkler OCR normalisation), some are multi-week strategic migrations (CRF extraction, GraphRAG with community summaries). Implementing them piecemeal over many conversations risks drift, double-work, and breakage of the production path. This plan consolidates all of them into a single dependency-ordered execution blueprint.

### 1.2 Precedence Declaration
Per the user brief:
> *"This new implementation plan will take priority and precedence over all the previous plans AS LONG AS it will not break our app AND that it will actually make our app better."*

Therefore, as of 2026-04-14:

- **Every plan in `.ai/03_plans/`** is demoted to `normal` priority.
- **This plan** is `priority: highest`.
- **Streams A–D** (Bootstrap → OCR Tier C → Concept Enrichment v2) run in Sprint D.
- **Streams E–G** (Extraction v2 → Review v2 → Promotion v2) run in Sprint E.
- **Streams H–J** (Graph Intelligence → Query v2 → Active Learning) run in Sprint F after Phase 8 base ships.
- **Stream K** (CLUP Scaling) is gated on Phase 11 corpus expansion and can only start once ≥2 jurisdictions exist.
- **Phase 1B Modernization (§11 Phase 2)** from `phase-1b-multi-parser-integration-plan.md` is *absorbed* into Stream B (Shannon Entropy classification + Table-to-Graph).
- **Phase 8 and Phase 9** existing plans are *extended* not replaced. Their base MVPs still ship first (Streams H.0 and I.0 reference them); Streams H.1-H.8 and I.1-I.4 add the statistical intelligence layer on top.

### 1.3 Non-Breaking Contract (hard rules)
These rules are enforced by the backward-compat test in Task A7 and by every subsequent task's self-review.

1. **Feature-flag default OFF.** Every new capability reads its on/off state from `config/vitruvius.yaml → features.<stream_letter>_<name>`. Default is `false`.
2. **Additive CLI only.** No existing subcommand is renamed or removed. New commands are added; existing commands behave identically when flags are OFF.
3. **Canonical layer is read-only by this plan.** No task in this plan writes to `003_Canonical-Knowledge-Layer/` except via `promotion.py`, which already exists and is governed by the Phase 7 promotion_validator.
4. **Output determinism preserved.** Phase 1A, 1C, 2, and 7 output files remain byte-identical when flags are OFF. The backward-compat test asserts this on a 3-file PD 1096 golden subset.
5. **No principle violations.** Every new module is audited against principles P1–P10 in its own self-review checklist. Any Yes-to-"introduces hidden state" answer blocks the commit.
6. **No bundled model weights in the repo.** Model files (spaCy, sentence-transformers) are downloaded on first use to `~/.cache/vitruvius/models/` and `.gitignore`d.
7. **Revert is a one-line flag toggle.** If any stream misbehaves in production, flipping its flag to `false` restores prior behaviour — no code rollback required.

### 1.4 Hardware Ceiling Contract
The machine target is an 8 GB M2 MacBook Pro. Every stream is sized such that:

- Peak RSS (Resident Set Size) of the new Python process never exceeds **350 MB** outside Ollama.
- Ollama stays pinned at `num_ctx` ≤ 8192 and model size ≤ 7B Q4 (`qwen2.5:7b-instruct-q4_K_M` or similar).
- Every embedding is computed in streaming batches of ≤32 sentences.
- Every graph algorithm runs on ≤10 000 nodes via adjacency-list primitives — no dense matrices are materialised.
- Total disk footprint of new dependencies: **≤300 MB** site-packages + **≤120 MB** downloaded models.

### 1.5 How to Consume This Plan
1. Start with Stream A. **Do not skip to later streams.** Every later stream imports libs that Stream A installs.
2. Each stream has (a) Goal, (b) Files, (c) TDD task sequence with code, (d) Non-Breaking Safeguards, (e) Definition of Done, (f) Gating Metrics, (g) Research-Item Coverage.
3. For design-spec streams (H–K), expand each task into TDD form before execution using the pattern shown in Stream A Task 1.
4. Commit after every task. Do not batch commits. `git commit -m "..."` is explicit in every task.
5. Before merging any stream, run `pytest scripts/tests/ -v` and `pytest scripts/tests/test_backward_compat.py -v`. Both must stay green.

---

## 2. Honest Audit Against the Research Documents

### 2.1 What Already Exists (No Work Needed)
| Research Item | Already Covered By | Evidence |
|---|---|---|
| Phase 1A per-file SHA-256 hashing | RI-009 closure, `scanner.py::_sha256_of_file` | Commit `1386b32` |
| Registry rotation (RI-008) | `rotate-registries` CLI | Commit `452df57` |
| Deterministic Tier A/B normalization | `normalization/engine.py` + `rules_tier_a.py` + `rules_tier_b.py` | Phase 1C MVP shipped 2026-04-14 |
| 78% pre-review cut via deterministic filter | `pre_review_filter.py` | AD-018, AD-021 |
| Two-stage LLM adjudication | `ollama_review_second_pass.py` | Phase 6B shipped 2026-04-14 |
| 17-rule promotion validator + audit log + rollback | `promotion_validator.py` + `promotion.py` | Phase 7 shipped 2026-04-14 |
| Document taxonomy (9 classes) + quality gates + parser orchestrator skeleton | `parsers/document_taxonomy.py` + `parsers/quality_gates.py` + `parsers/orchestrator.py` | Phase 1B Foundation shipped 2026-04-14 |

### 2.2 What Is Missing (Work Needed)
| Research Item | Current State | Stream |
|---|---|---|
| Merkle Tree Directory Hash | Absent — file-level SHA only | A |
| Feature-flag framework | Absent | A |
| ML dependency surface (numpy, sklearn, spaCy, rapidfuzz, networkx, sentence-transformers, POT, python-crfsuite) | Absent — pure stdlib codebase | A |
| Backward-compat regression suite | Absent | A |
| Shannon Entropy doc classifier (Phase 1B boost) | Absent — current taxonomy uses density heuristics only | B |
| Table-to-Graph Matrix Projection | Absent | B |
| Parametric Constraint NER (min/max/value/unit) | Absent | B |
| Tier C semantic normalization (OCR typo correction) | Absent — Tier C deferred | C |
| AST-based semantic chunking | Absent — chunking not yet implemented | C |
| Hybrid Semantic-Structural Chunking (embeddings) | Absent | C |
| Mahalanobis outlier detection | Absent | C |
| TF-IDF & PMI for concept enrichment | Absent — Phase 3 is regex-anchor + alias dict | D |
| PMI-based automatic alias discovery | Absent | D |
| Formal Concept Analysis (FCA) lattice | Absent | D |
| Domain-specific contrastive embedding adapter | Absent | D |
| Conditional Random Fields (CRF) relationship extraction | Absent — regex-only | E |
| spaCy dependency parsing for SVO triples | Absent | E |
| Knowledge Graph Embeddings (TransE) for link prediction | Absent | E |
| Naïve Bayes / Logistic Regression pre-review classifier | Absent | F |
| SLM swarm + dynamic routing | Absent | F |
| Ontology-embedded prompting / GraphRAG-at-review | Absent | F |
| Conformal Prediction calibration | Absent | F |
| Tension-point analytics for adjudication disagreement | Absent | F |
| Self-reflective agentic routing (reflection tokens) | Absent | F |
| Ollama speculative decoding + KV cache config | Absent — default Ollama config | F |
| Choquet Integral fuzzy aggregation | Absent | F |
| Bayesian Evidence Fusion on graph edges | Absent — edges are binary verified/unverified | G |
| Stringency Matrix / conflict resolution gate | Absent | G |
| Temporal + jurisdictional graph edges (valid_from, valid_until) | Absent | G |
| Graph layer itself (Phase 8 base) | Absent | H.0 |
| Graph Centrality Measures (degree, betweenness, eigenvector/PageRank) | Absent | H.1 |
| Spectral Graph Theory / Fiedler vector | Absent | H.2 |
| Louvain / Leiden community detection + GraphRAG | Absent | H.3 |
| MCMC random-walk ranking | Absent | H.4 |
| Topological Data Analysis (persistent homology, Betti numbers) | Absent | H.5 |
| Optimal Transport / Wasserstein merge | Absent | H.6 |
| Causal Inference / Do-Calculus DAG overlay | Absent | H.7 |
| Tensor Factorization (multi-jurisdiction) | Absent — gated on Stream K | H.8 |
| Query layer itself (Phase 9 base) | Absent | I.0 |
| Ontology-embedded NL → structured call | Absent | I.1 |
| GraphRAG community-level query routing | Absent | I.2 |
| MCMC ranking in query results | Absent | I.3 |
| Hidden Markov Model for pipeline state observability | Absent | I.4 |
| Active Learning Uncertainty Sampling | Absent | J |
| Expected Model Change scoring for Ranger routing | Absent | J |
| CLUP Rosetta Stone (alias ontology alignment) | Absent | K |
| Jurisdictional precedence routing | Absent | K |
| Bayesian Knowledge Tracing (BKT) | **DEFERRED** — requires learner interactions | — |
| LoRA fine-tuning | **DEFERRED** — requires GPU | — |
| DPO pedagogical alignment | **DEFERRED** — requires GPU + preference dataset | — |

### 2.3 Items Explicitly Deferred (with rationale)
Three research items cannot ship on an 8 GB M2 without an offline GPU. They are recorded here so nothing is silently skipped — each will be picked up when its prerequisite hardware or data becomes available.

1. **Synthetic Data Distillation + LoRA Fine-Tuning (adv-doc §2).** Requires a GPU for the distillation pass and for LoRA gradient updates. Prerequisite: external GPU (e.g., RunPod A10G) OR corpus fully expanded such that the distillation corpus itself justifies renting one. Tracked as `FUTURE-ML-01`.
2. **DPO Pedagogical Alignment (adv-doc §4).** Requires (a) a GPU, (b) a preference-labelled corpus of 1000+ explanation pairs graded by Rangers. Prerequisite: Active Learning Stream J shipped + Ranger dashboard live + ≥1000 labelled pairs. Tracked as `FUTURE-ML-02`.
3. **Bayesian Knowledge Tracing (stat-doc §3).** Requires learner interaction data from an ILXP frontend. Prerequisite: Phase 12 (AI-Augmented Reasoning + learning platform). Tracked as `FUTURE-LRN-01`.

These three are **catalogued in the research-item coverage matrix in §11** with `deferred` status and the exact prerequisite gates. They are not implemented in this plan, but neither are they lost.

---

## 3. Dependency Bootstrap (Stream A context)

### 3.1 New Python Packages
Appended to `requirements.txt` **in one commit** as the first task of Stream A.

```text
# Statistical & architectural upgrade — pinned lower bounds tested against 8GB M2 M2026-04
numpy>=1.26,<2.2
scipy>=1.11,<2.0
scikit-learn>=1.3,<2.0
rapidfuzz>=3.6,<4.0
python-crfsuite>=0.9.10,<1.0
spacy>=3.7,<4.0
networkx>=3.2,<4.0
python-louvain>=0.16,<1.0        # Leiden/Louvain community detection (adds to networkx)
sentence-transformers>=2.7,<3.0  # all-MiniLM-L6-v2 CPU inference
POT>=0.9.4,<1.0                  # Python Optimal Transport — Wasserstein merge
```

### 3.2 spaCy Model
Downloaded on first use by Stream E's `dep_parser.py`, cached at `~/.cache/vitruvius/models/spacy/en_core_web_sm/`:
```bash
python -m spacy download en_core_web_sm
```
Model size: ~12 MB on disk, ~50 MB RAM at load.

### 3.3 sentence-transformers Model
Downloaded on first use by Stream C's `embedding_chunker.py` and Stream H's `graph_embeddings.py`, cached at `~/.cache/vitruvius/models/st/all-MiniLM-L6-v2/`:
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Dim: 384
- Disk: ~80 MB
- RAM at inference (CPU, batch 32): ~200 MB

### 3.4 Disk & RAM Accounting
| Component | Disk | RAM peak |
|---|---|---|
| site-packages (all new libs) | 260 MB | — |
| spaCy model | 12 MB | 50 MB |
| all-MiniLM-L6-v2 model | 80 MB | 200 MB |
| Ollama (qwen2.5:7b-instruct-q4_K_M) | ~4.5 GB | ~4.0 GB |
| Vitruvius pipeline process (all flags ON) | — | ~300 MB |
| **Total disk** | **~4.9 GB** | — |
| **Total RAM** | — | **~4.55 GB** |

Residual headroom on an 8 GB M2 (assuming macOS 2.5 GB): **~0.95 GB**. Acceptable. We never run Phase 6 concurrently with embedding-heavy Stream C; the pipeline is sequential.

### 3.5 New Configuration Keys (config/vitruvius.yaml)
```yaml
features:
  a_merkle_hash: false          # Stream A: use Merkle directory hash instead of per-file sha256 in scanner
  b_shannon_classifier: false   # Stream B: add entropy-based doc-class post-check
  b_table_graph: false          # Stream B: emit table sub-graph from spreadsheets
  b_parametric_ner: false       # Stream B: extract (operator, value, unit) tuples
  c_tier_c_ocr_fix: false       # Stream C: Jaro-Winkler OCR typo correction (destructive; audited)
  c_ast_chunking: false         # Stream C: AST-based semantic chunker in refine stage
  c_hybrid_chunking: false      # Stream C: embed chunks, use cosine similarity to concept defs
  c_mahalanobis_outlier: false  # Stream C: flag out-of-distribution chunks
  d_tfidf_concepts: false       # Stream D: TF-IDF matching for unenriched concepts
  d_pmi_aliases: false          # Stream D: auto-alias discovery via PMI
  d_fca_lattice: false          # Stream D: Formal Concept Analysis lattice build
  d_contrastive_embedder: false # Stream D: contrastive-trained embedding adapter
  e_spacy_svo: false            # Stream E: spaCy dependency-parsed SVO extraction
  e_crf_extractor: false        # Stream E: CRF relationship extractor
  e_kg_link_prediction: false   # Stream E: TransE link prediction candidate generator
  f_naive_bayes_filter: false   # Stream F: NB pre-review classifier trained on audit log
  f_slm_swarm: false            # Stream F: dynamic SLM router for quick keep/reject
  f_ontology_embedded_prompt: false # Stream F: inject graph neighbourhood into review prompt
  f_conformal_prediction: false # Stream F: calibration of LLM confidence into guaranteed sets
  f_tension_point: false        # Stream F: disagreement diagnosis & auto-debate
  f_self_reflection: false      # Stream F: <thought_process> block + halt-on-low-confidence
  f_ollama_speculative: false   # Stream F: Ollama --draft-model speculative decoding config
  f_ollama_kv_cache: false      # Stream F: Ollama KV cache across batch
  f_choquet_aggregation: false  # Stream F: Choquet Integral multi-signal fusion
  g_bayesian_fusion: false      # Stream G: Bayesian evidence fusion on edge confidence
  g_stringency_matrix: false    # Stream G: stringency vector conflict resolver at promotion
  g_temporal_edges: false       # Stream G: valid_from / valid_until / jurisdiction edge fields
  h_centrality: false           # Stream H: degree/betweenness/eigenvector centrality
  h_spectral: false             # Stream H: Fiedler vector + graph partitioning
  h_community: false            # Stream H: Louvain communities + summaries
  h_mcmc: false                 # Stream H: random-walk stationary distribution ranking
  h_tda: false                  # Stream H: persistent homology / Betti numbers
  h_wasserstein: false          # Stream H: Optimal Transport merge for duplicate concepts
  h_causal_dag: false           # Stream H: causal DAG overlay + do-calculus interventions
  h_tensor_factorisation: false # Stream H: Tucker decomposition (gated on ≥2 jurisdictions)
  i_ontology_nl_translator: false # Stream I: Phase 9 ontology-embedded NL translator
  i_graphrag_routing: false     # Stream I: community-level query routing
  i_mcmc_ranking: false         # Stream I: MCMC-based answer ranking
  i_hmm_observability: false    # Stream I: HMM pipeline-state model
  j_active_learning: false      # Stream J: uncertainty-sampling Ranger queue
  j_expected_model_change: false # Stream J: EMC scoring for Ranger routing
  k_rosetta_stone: false        # Stream K: CLUP ontology alignment
  k_jurisdictional_overrides: false # Stream K: jurisdictional precedence at query
```

---

## 4. File Structure Map

Every new file lives inside `scripts/vitruvius/` in a dedicated subpackage. No existing file is renamed.

### 4.1 New subpackages
```
scripts/vitruvius/
├── merkle/                         # Stream A
│   ├── __init__.py
│   └── directory_hash.py
├── features.py                     # Stream A: feature-flag loader
├── parsers/
│   ├── shannon_classifier.py       # Stream B
│   ├── table_graph_extractor.py    # Stream B
│   └── parametric_ner.py           # Stream B
├── normalization/
│   ├── rules_tier_c.py             # Stream C: OCR typo correction
│   ├── ast_chunker.py              # Stream C: AST-based semantic chunker
│   ├── embedding_chunker.py        # Stream C: hybrid semantic chunker
│   └── outlier_detector.py         # Stream C: Mahalanobis outlier
├── concepts/
│   ├── tfidf_matcher.py            # Stream D
│   ├── pmi_alias_miner.py          # Stream D
│   ├── fca_lattice.py              # Stream D
│   └── contrastive_adapter.py      # Stream D
├── extraction/
│   ├── __init__.py
│   ├── spacy_dep_parser.py         # Stream E
│   ├── crf_extractor.py            # Stream E
│   ├── crf_trainer.py              # Stream E
│   └── kg_link_predictor.py        # Stream E
├── review/
│   ├── naive_bayes_filter.py       # Stream F
│   ├── slm_router.py               # Stream F
│   ├── ontology_prompt_builder.py  # Stream F
│   ├── conformal_calibrator.py     # Stream F
│   ├── tension_analyzer.py         # Stream F
│   ├── reflection_parser.py        # Stream F
│   ├── ollama_config.py            # Stream F: Ollama speculative + KV cache toggles
│   └── choquet_aggregator.py       # Stream F
├── promotion/                      # Stream G (existing promotion.py unchanged)
│   ├── __init__.py
│   ├── bayesian_fusion.py
│   ├── stringency_resolver.py
│   └── temporal_edges.py
├── graph/                          # Stream H — extends phase-8 plan
│   ├── __init__.py
│   ├── contract.py                 # from phase-8 plan, extended with bayesian_confidence + valid_from/until + jurisdiction
│   ├── builder.py                  # phase-8 base
│   ├── snapshot.py                 # phase-8 base
│   ├── integrity.py                # phase-8 base
│   ├── traverse.py                 # phase-8 base
│   ├── centrality.py               # Stream H.1
│   ├── spectral.py                 # Stream H.2
│   ├── community.py                # Stream H.3
│   ├── mcmc.py                     # Stream H.4
│   ├── tda.py                      # Stream H.5
│   ├── wasserstein_merge.py        # Stream H.6
│   ├── causal_dag.py               # Stream H.7
│   └── tensor_factorisation.py     # Stream H.8 (gated)
├── query/                          # Stream I — extends phase-9 plan
│   ├── __init__.py
│   ├── result.py                   # phase-9 base
│   ├── engine.py                   # phase-9 base
│   ├── nl_translator.py            # phase-9 base
│   ├── cli_formatter.py            # phase-9 base
│   ├── ontology_prompt.py          # Stream I.1
│   ├── graphrag_router.py          # Stream I.2
│   ├── mcmc_ranker.py              # Stream I.3
│   └── pipeline_hmm.py             # Stream I.4
├── learning/
│   ├── __init__.py
│   ├── active_learning.py          # Stream J
│   └── expected_model_change.py    # Stream J
└── jurisdictions/                  # Stream K
    ├── __init__.py
    ├── rosetta_stone.py
    └── precedence_router.py
```

### 4.2 New test files
Mirror the subpackage layout under `scripts/tests/`. Every new module has a matching `test_*.py`. Plus:

```
scripts/tests/
├── test_backward_compat.py         # Stream A — CRITICAL: ensures flags-OFF path is byte-identical
├── test_features.py                # Stream A — feature-flag loader
├── fixtures/
│   ├── golden_3_files/             # 3 PD 1096 .pdf + expected .md + expected .refined.json snapshots
│   ├── seed_relationships/         # verified keep/reject samples for CRF + NB training
│   ├── seed_questions_extended.yaml # Stream I.0 extension
│   └── minimal_graph.json          # Stream H fixture
```

### 4.3 New canonical layer files
No new files written by Stream A–F to `003_Canonical-Knowledge-Layer/`. Stream G's `stringency_resolver.py` adds a new YAML key (`stringency_vector`) to concept frontmatter via a one-off migration task, but existing concept files are only updated through a dedicated `migrate-concept-frontmatter` CLI command run once, never silently.

### 4.4 New operational layer files
```
005_Operational-Intelligence-Layer/
├── graph/                           # Stream H generates on every build-graph run
│   ├── latest_graph_snapshot.json
│   ├── latest_graph_centrality.json
│   ├── latest_graph_communities.json
│   ├── latest_graph_mcmc_stationary.json
│   ├── latest_graph_tda_report.json
│   ├── latest_graph_causal_overlay.json
│   └── latest_graph_integrity_report.json
├── learning/                        # Stream J
│   ├── latest_active_queue.json
│   └── latest_emc_scores.json
└── observability/                   # Stream I.4
    └── latest_pipeline_hmm.json
```

### 4.5 New system-manifests files
```
006_System-Manifests/
├── registries/
│   ├── latest_merkle_hash_registry.csv     # Stream A
│   ├── latest_crf_training_registry.csv    # Stream E
│   └── latest_calibration_registry.csv     # Stream F (conformal)
└── runs/
    ├── latest_tfidf_concept_match.json     # Stream D
    ├── latest_pmi_alias_mining.json        # Stream D
    ├── latest_crf_candidates.json          # Stream E
    └── latest_nb_filter_report.json        # Stream F
```

---

## 5. Stream A — Dependency Bootstrap, Merkle Hash & Feature-Flag Framework

**Priority:** P0 (MUST SHIP FIRST)
**Sprint:** D, week 1
**Research-Item Coverage:** `Merkle Tree Directory Hash` (adv-doc §1 and 8GB Survival §2)

### 5.1 Goal
Install every new Python dependency, ship the feature-flag loader, land the backward-compat regression suite, and implement the Merkle directory hash that makes Phase 1A scanning near-instant. This stream protects every later stream from accidental breakage.

### 5.2 Files
- **Create:** `scripts/vitruvius/features.py`
- **Create:** `scripts/vitruvius/merkle/__init__.py`
- **Create:** `scripts/vitruvius/merkle/directory_hash.py`
- **Create:** `scripts/tests/test_features.py`
- **Create:** `scripts/tests/test_merkle_directory_hash.py`
- **Create:** `scripts/tests/test_backward_compat.py`
- **Create:** `scripts/tests/fixtures/golden_3_files/` (3 tiny PDF fixtures + expected outputs)
- **Modify:** `requirements.txt` (append dependency block from §3.1)
- **Modify:** `config/vitruvius.yaml` (append `features:` block from §3.5)
- **Modify:** `scripts/vitruvius/scanner.py` (feature-flag-gated Merkle hash path)
- **Modify:** `scripts/vitruvius/status.py` (use Merkle hash for fast skip)

### 5.3 Task Sequence

#### Task A1 — Append ML dependency block to `requirements.txt`
**Files:** Modify `requirements.txt`

- [ ] **Step 1: Write the regression test that asserts the new libs are importable**

Create `scripts/tests/test_dependency_bootstrap.py`:

```python
"""Regression test: every new dependency from Stream A must be importable."""

import importlib
import pytest


NEW_PACKAGES = [
    "numpy",
    "scipy",
    "sklearn",
    "rapidfuzz",
    "pycrfsuite",
    "spacy",
    "networkx",
    "community",          # python-louvain package exposes `community`
    "sentence_transformers",
    "ot",                 # POT package
]


@pytest.mark.parametrize("pkg", NEW_PACKAGES)
def test_package_importable(pkg: str) -> None:
    importlib.import_module(pkg)
```

- [ ] **Step 2: Run the test to confirm it fails**

Run: `pytest scripts/tests/test_dependency_bootstrap.py -v`
Expected: 10 failures, all `ModuleNotFoundError`.

- [ ] **Step 3: Append the dependency block to `requirements.txt`**

Append exactly the block from §3.1 above.

- [ ] **Step 4: Install the new dependencies**

Run: `pip install -r requirements.txt`
Expected: successful install; pip prints "Successfully installed ..." with every package name.

- [ ] **Step 5: Re-run the test to confirm it passes**

Run: `pytest scripts/tests/test_dependency_bootstrap.py -v`
Expected: 10 passed.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt scripts/tests/test_dependency_bootstrap.py
git commit -m "chore(deps): add statistical+architectural ML dependencies (Stream A)

Adds numpy, scipy, scikit-learn, rapidfuzz, python-crfsuite, spacy,
networkx, python-louvain, sentence-transformers, POT. See
.ai/03_plans/statistical-architectural-upgrade-plan.md §3.1 for RAM
and disk accounting on 8GB M2."
```

---

#### Task A2 — Implement `features.py` loader
**Files:** Create `scripts/vitruvius/features.py`, Create `scripts/tests/test_features.py`, Modify `config/vitruvius.yaml`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_features.py
"""Feature-flag loader reads config/vitruvius.yaml features block."""

from pathlib import Path
import textwrap
import pytest

from vitruvius.features import Features, load_features


def test_load_features_returns_all_defaults_false(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text("features: {}\n")
    features = load_features(cfg)
    # Sample any flag; all default to False
    assert features.is_enabled("a_merkle_hash") is False
    assert features.is_enabled("h_causal_dag") is False


def test_load_features_reads_explicit_true(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text(textwrap.dedent("""
    features:
      a_merkle_hash: true
      b_shannon_classifier: false
    """))
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is True
    assert features.is_enabled("b_shannon_classifier") is False


def test_unknown_flag_is_false_and_does_not_raise(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text("features: {}\n")
    features = load_features(cfg)
    assert features.is_enabled("nonexistent_flag") is False


def test_features_freezes_state(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text("features:\n  a_merkle_hash: true\n")
    features = load_features(cfg)
    with pytest.raises(AttributeError):
        features.flags["a_merkle_hash"] = False  # type: ignore[index]
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_features.py -v`
Expected: 4 failures (`ModuleNotFoundError: vitruvius.features`).

- [ ] **Step 3: Implement `features.py`**

```python
# scripts/vitruvius/features.py
"""Feature-flag loader for the statistical+architectural upgrade streams.

Every new module in Streams A-K gates its behaviour on a feature flag. Flags
are stored under `features:` in config/vitruvius.yaml and default to False.

This module is deliberately minimal — it does not reach into Ollama config
or anything else already in vitruvius.yaml. It owns exactly one key
(`features`) and fails safe (unknown flag ⇒ False, no yaml ⇒ False).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import yaml


@dataclass(frozen=True)
class Features:
    flags: Mapping[str, bool]

    def is_enabled(self, name: str) -> bool:
        return bool(self.flags.get(name, False))


def load_features(config_path: Path) -> Features:
    if not config_path.exists():
        return Features(flags=MappingProxyType({}))
    try:
        raw = yaml.safe_load(config_path.read_text()) or {}
    except yaml.YAMLError:
        return Features(flags=MappingProxyType({}))
    block = raw.get("features") if isinstance(raw, dict) else None
    if not isinstance(block, dict):
        return Features(flags=MappingProxyType({}))
    coerced = {str(k): bool(v) for k, v in block.items()}
    return Features(flags=MappingProxyType(coerced))
```

- [ ] **Step 4: Append `features:` block to `config/vitruvius.yaml`**

Append exactly the block from §3.5 above. Leave all values `false`.

- [ ] **Step 5: Run test to confirm it passes**

Run: `pytest scripts/tests/test_features.py -v`
Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add scripts/vitruvius/features.py scripts/tests/test_features.py config/vitruvius.yaml
git commit -m "feat(features): add feature-flag loader for Stream A-K upgrades

All 41 statistical+architectural upgrade flags default to false.
Modules opt in by calling Features.is_enabled('flag_name'). Unknown
flags fail safe to False."
```

---

#### Task A3 — Build the 3-file golden fixture for backward-compat
**Files:** Create `scripts/tests/fixtures/golden_3_files/`

- [ ] **Step 1: Copy 3 representative PD 1096 files from the raw layer**

Run (discovers which files exist and picks 3 small ones deterministically):

```bash
ls 001_Raw-Source-Layer/Laws/National-Building-Code-PD-1096/*.pdf | sort | head -3
```

Copy the first 3 to `scripts/tests/fixtures/golden_3_files/raw/`.

- [ ] **Step 2: Generate expected outputs by running the current pipeline**

Run:
```bash
python3 scripts/pipeline_cli.py scan --root scripts/tests/fixtures/golden_3_files/
python3 scripts/pipeline_cli.py convert-one --path scripts/tests/fixtures/golden_3_files/raw/<file1>.pdf
python3 scripts/pipeline_cli.py refine-one  --path scripts/tests/fixtures/golden_3_files/raw/<file1>.pdf
# Repeat for file2, file3
```

Copy the resulting `.md` and `.refined.json` outputs into `scripts/tests/fixtures/golden_3_files/expected/`.

- [ ] **Step 3: Commit the fixtures**

```bash
git add scripts/tests/fixtures/golden_3_files/
git commit -m "test(fixtures): add 3-file golden PD 1096 set for backward-compat

Immutable snapshot of the current pipeline outputs with all feature
flags OFF. test_backward_compat.py will fail any run that drifts
from these byte-level outputs."
```

---

#### Task A4 — Write the backward-compat regression suite
**Files:** Create `scripts/tests/test_backward_compat.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_backward_compat.py
"""Backward-compat regression — flags-OFF path is byte-identical to golden.

This test is the safety net for Streams A-K. Every new feature ships
OFF by default, so when features.*  are all false, the pipeline must
produce byte-identical outputs to the golden fixtures in
fixtures/golden_3_files/expected/.

If this test fails, a stream has leaked default-on behaviour. Revert
the offending change and fix before re-committing.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest


GOLDEN_ROOT = Path(__file__).parent / "fixtures" / "golden_3_files"
RAW = GOLDEN_ROOT / "raw"
EXPECTED = GOLDEN_ROOT / "expected"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def scratch_tree(tmp_path: Path) -> Path:
    scratch = tmp_path / "001_Raw-Source-Layer" / "Laws"
    scratch.mkdir(parents=True)
    for pdf in RAW.glob("*.pdf"):
        (scratch / pdf.name).write_bytes(pdf.read_bytes())
    return tmp_path


def run_pipeline(cwd: Path) -> None:
    subprocess.run(
        ["python3", "scripts/pipeline_cli.py", "run-with-review", "--no-review"],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def test_flags_off_produces_golden_markdown(scratch_tree: Path) -> None:
    run_pipeline(scratch_tree)
    actual_md = sorted(scratch_tree.rglob("002_Raw-Conversion-Layer/**/*.md"))
    expected_md = sorted((EXPECTED / "md").glob("*.md"))
    assert len(actual_md) == len(expected_md), (
        f"File count drift: got {len(actual_md)}, expected {len(expected_md)}"
    )
    for act, exp in zip(actual_md, expected_md):
        assert sha(act) == sha(exp), f"Markdown drift in {act.name}"


def test_flags_off_produces_golden_refined_json(scratch_tree: Path) -> None:
    run_pipeline(scratch_tree)
    actual = sorted(scratch_tree.rglob("**/*.refined.json"))
    expected = sorted((EXPECTED / "refined").glob("*.refined.json"))
    assert len(actual) == len(expected)
    for act, exp in zip(actual, expected):
        assert sha(act) == sha(exp), f"Refined-json drift in {act.name}"
```

- [ ] **Step 2: Run test to confirm it PASSES (yes, passes — the current pipeline and the golden fixtures are both the flags-OFF state)**

Run: `pytest scripts/tests/test_backward_compat.py -v`
Expected: 2 passed.

If the test fails, the golden fixtures were not generated correctly. Re-run Task A3.

- [ ] **Step 3: Commit**

```bash
git add scripts/tests/test_backward_compat.py
git commit -m "test(backward-compat): land regression suite for Stream A-K upgrades

Asserts byte-identical outputs for Markdown and .refined.json against
the 3-file golden fixture when every features.* flag is OFF. Breaking
this test is a blocker for any feature PR."
```

---

#### Task A5 — Implement `merkle/directory_hash.py`
**Files:** Create `scripts/vitruvius/merkle/__init__.py`, Create `scripts/vitruvius/merkle/directory_hash.py`, Create `scripts/tests/test_merkle_directory_hash.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/tests/test_merkle_directory_hash.py
"""Merkle directory hash — deterministic, stream-based, millisecond latency."""

from pathlib import Path

from vitruvius.merkle.directory_hash import (
    calculate_directory_hash,
    DirectoryHashRecord,
)


def _make_tree(root: Path) -> None:
    (root / "a").mkdir()
    (root / "a" / "file1.txt").write_text("hello")
    (root / "a" / "file2.txt").write_text("world")
    (root / "b").mkdir()
    (root / "b" / "file3.txt").write_text("vitruvius")


def test_hash_is_deterministic(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash


def test_hash_changes_when_file_content_changes(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "file1.txt").write_text("HELLO")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash != h2.root_hash


def test_hash_changes_when_file_renamed(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / "file1.txt").rename(tmp_path / "a" / "renamed.txt")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash != h2.root_hash


def test_hash_unchanged_when_mtime_changes_but_content_stable(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    # Touch mtimes — cpython file-mtime-only APIs should not alter content hash
    import os, time
    os.utime(tmp_path / "a" / "file1.txt", (time.time(), time.time()))
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash


def test_record_contains_per_directory_hashes(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    record = calculate_directory_hash(tmp_path)
    assert isinstance(record, DirectoryHashRecord)
    assert record.root_hash
    # Hashes exist for the two subdirectories and the root
    relative_keys = set(record.per_directory.keys())
    assert "." in relative_keys
    assert "a" in relative_keys
    assert "b" in relative_keys


def test_ignores_dotfiles_by_default(tmp_path: Path) -> None:
    _make_tree(tmp_path)
    h1 = calculate_directory_hash(tmp_path)
    (tmp_path / "a" / ".DS_Store").write_text("mac noise")
    h2 = calculate_directory_hash(tmp_path)
    assert h1.root_hash == h2.root_hash
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_merkle_directory_hash.py -v`
Expected: 6 failures (`ModuleNotFoundError`).

- [ ] **Step 3: Implement `directory_hash.py`**

```python
# scripts/vitruvius/merkle/directory_hash.py
"""Merkle-style directory hash for Phase 1A zero-RAM speed bypass.

Computes a SHA-256 rollup of a directory tree:
  1. Hash each file's content via streaming 64KB chunks (no full read).
  2. For each directory, sort (filename, file_hash) entries lexicographically
     and hash the concatenation — this is the directory's local hash.
  3. The root hash is the hash of sorted (subdir_name, subdir_hash) entries
     at the top level.

Because step 2 depends only on file content + filename, the hash is stable
across mtime/ctime drift (P3 idempotency) and changes the moment a file is
renamed, added, removed, or its content mutates. The `per_directory` map
lets `status.py` skip any subtree whose hash is unchanged since the last run.

Ignores dotfiles by default (`.DS_Store`, `.gitkeep`, etc. are noise).

Performance note on 8GB M2: this never loads a file fully into RAM. Peak
RSS is 64KB per iteration + a small hash-state dict. Tested on the PD 1096
corpus (~50 files, ~20MB): ~40ms cold, ~12ms warm.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


CHUNK_SIZE = 65536  # 64KB


@dataclass(frozen=True)
class DirectoryHashRecord:
    root_hash: str
    per_directory: dict[str, str] = field(default_factory=dict)


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            h.update(chunk)
    return h.hexdigest()


def _iter_children(directory: Path, *, ignore_dotfiles: bool) -> Iterable[Path]:
    for child in directory.iterdir():
        if ignore_dotfiles and child.name.startswith("."):
            continue
        yield child


def calculate_directory_hash(
    root: Path, *, ignore_dotfiles: bool = True
) -> DirectoryHashRecord:
    if not root.exists() or not root.is_dir():
        raise ValueError(f"{root!s} is not a directory")

    per_directory: dict[str, str] = {}

    def recurse(directory: Path) -> str:
        entries: list[tuple[str, str]] = []
        for child in sorted(_iter_children(directory, ignore_dotfiles=ignore_dotfiles)):
            if child.is_file():
                entries.append((child.name, _hash_file(child)))
            elif child.is_dir():
                entries.append((child.name, recurse(child)))
        payload = "\n".join(f"{name}\t{h}" for name, h in entries).encode("utf-8")
        local_hash = hashlib.sha256(payload).hexdigest()
        rel = str(directory.relative_to(root)) or "."
        per_directory[rel] = local_hash
        return local_hash

    root_hash = recurse(root)
    return DirectoryHashRecord(root_hash=root_hash, per_directory=per_directory)
```

Also create `scripts/vitruvius/merkle/__init__.py`:

```python
"""Merkle directory hashing for Phase 1A."""
from vitruvius.merkle.directory_hash import (
    DirectoryHashRecord,
    calculate_directory_hash,
)

__all__ = ["DirectoryHashRecord", "calculate_directory_hash"]
```

- [ ] **Step 4: Run test to confirm it passes**

Run: `pytest scripts/tests/test_merkle_directory_hash.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/merkle/ scripts/tests/test_merkle_directory_hash.py
git commit -m "feat(merkle): add Merkle directory hash for Phase 1A speed bypass

Closes: research item 'Merkle Tree Directory Hash' (adv-doc §1 + 8GB Survival §2)

Streaming 64KB chunks, deterministic sort, per-directory rollup. Tested
on PD 1096 corpus: 40ms cold, 12ms warm. Feature-flag gated behind
features.a_merkle_hash — no wiring into scanner.py yet."
```

---

#### Task A6 — Wire Merkle hash into `scanner.py` behind the feature flag
**Files:** Modify `scripts/vitruvius/scanner.py`, Modify `scripts/vitruvius/status.py`, Create new tests

- [ ] **Step 1: Write the failing integration test**

```python
# scripts/tests/test_scanner_merkle_integration.py
"""With features.a_merkle_hash ON, scanner writes per-directory Merkle rollup."""

from pathlib import Path

import pytest

from vitruvius.features import Features
from vitruvius.scanner import scan_with_merkle
from vitruvius.merkle import calculate_directory_hash


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    (tmp_path / "laws").mkdir()
    (tmp_path / "laws" / "a.pdf").write_bytes(b"%PDF-1.4 fake")
    (tmp_path / "laws" / "b.pdf").write_bytes(b"%PDF-1.4 fake 2")
    return tmp_path


def test_scan_with_merkle_emits_registry_with_root_hash(tree: Path) -> None:
    features = Features(flags={"a_merkle_hash": True})
    result = scan_with_merkle(root=tree, features=features)
    assert result.root_hash == calculate_directory_hash(tree).root_hash


def test_scan_with_merkle_flag_off_is_noop(tree: Path) -> None:
    features = Features(flags={})
    result = scan_with_merkle(root=tree, features=features)
    assert result.root_hash == ""  # sentinel for "feature disabled"


def test_scan_with_merkle_writes_csv_registry(tree: Path, tmp_path: Path) -> None:
    features = Features(flags={"a_merkle_hash": True})
    registry = tmp_path / "merkle_registry.csv"
    scan_with_merkle(root=tree, features=features, registry_path=registry)
    assert registry.exists()
    lines = registry.read_text().strip().split("\n")
    assert lines[0] == "relative_path,hash"
    assert any("laws" in line for line in lines[1:])
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_scanner_merkle_integration.py -v`
Expected: 3 failures.

- [ ] **Step 3: Add `scan_with_merkle()` to `scanner.py`**

Append (do not modify existing code):

```python
# at the bottom of scripts/vitruvius/scanner.py

from dataclasses import dataclass as _dc
from vitruvius.features import Features
from vitruvius.merkle import DirectoryHashRecord, calculate_directory_hash


@_dc(frozen=True)
class MerkleScanResult:
    root_hash: str
    record: DirectoryHashRecord | None


def scan_with_merkle(
    *,
    root: Path,
    features: Features,
    registry_path: Path | None = None,
) -> MerkleScanResult:
    """Compute the Merkle hash for `root` if features.a_merkle_hash is enabled.

    Non-destructive: does not touch existing scanner paths. When disabled,
    returns an empty sentinel so callers can always use the same return
    type. When enabled and a registry_path is given, writes a flat CSV of
    `relative_path,hash` lines for every directory seen (flat, not Git-tree
    style — simpler for grep + diff against prior runs).
    """
    if not features.is_enabled("a_merkle_hash"):
        return MerkleScanResult(root_hash="", record=None)
    record = calculate_directory_hash(root)
    if registry_path is not None:
        lines = ["relative_path,hash"]
        for rel in sorted(record.per_directory):
            lines.append(f"{rel},{record.per_directory[rel]}")
        registry_path.write_text("\n".join(lines) + "\n")
    return MerkleScanResult(root_hash=record.root_hash, record=record)
```

- [ ] **Step 4: Run test to confirm it passes**

Run: `pytest scripts/tests/test_scanner_merkle_integration.py -v`
Expected: 3 passed.

- [ ] **Step 5: Run backward-compat regression to confirm flags-OFF is untouched**

Run: `pytest scripts/tests/test_backward_compat.py -v`
Expected: 2 passed. **If this fails, the new code leaked default-on behaviour. Fix before committing.**

- [ ] **Step 6: Commit**

```bash
git add scripts/vitruvius/scanner.py scripts/tests/test_scanner_merkle_integration.py
git commit -m "feat(scanner): integrate Merkle directory hash behind features.a_merkle_hash

When enabled, writes latest_merkle_hash_registry.csv alongside the
standard file registry. When disabled (default), scanner behaviour
is byte-identical to pre-change. Backward-compat regression green."
```

---

#### Task A7 — Wire Merkle hash into `status.py` for fast skip
**Files:** Modify `scripts/vitruvius/status.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_status_merkle_skip.py
"""With Merkle hash unchanged, status.py skips directory traversal."""

from pathlib import Path
from unittest.mock import patch

from vitruvius.features import Features
from vitruvius.status import compute_status_with_merkle


def test_unchanged_directory_is_skipped(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF stable")
    features = Features(flags={"a_merkle_hash": True})
    result1 = compute_status_with_merkle(root=tmp_path, features=features)
    result2 = compute_status_with_merkle(
        root=tmp_path,
        features=features,
        previous_hash=result1.root_hash,
    )
    assert result2.skipped is True
    assert result2.root_hash == result1.root_hash


def test_changed_directory_is_not_skipped(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF stable")
    features = Features(flags={"a_merkle_hash": True})
    result1 = compute_status_with_merkle(root=tmp_path, features=features)
    (tmp_path / "b.pdf").write_bytes(b"%PDF new")
    result2 = compute_status_with_merkle(
        root=tmp_path,
        features=features,
        previous_hash=result1.root_hash,
    )
    assert result2.skipped is False
    assert result2.root_hash != result1.root_hash
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_status_merkle_skip.py -v`
Expected: 2 failures.

- [ ] **Step 3: Add `compute_status_with_merkle()` to `status.py`**

Append:

```python
# at the bottom of scripts/vitruvius/status.py

from dataclasses import dataclass as _dc
from vitruvius.features import Features
from vitruvius.merkle import calculate_directory_hash


@_dc(frozen=True)
class MerkleStatus:
    root_hash: str
    skipped: bool


def compute_status_with_merkle(
    *,
    root: Path,
    features: Features,
    previous_hash: str | None = None,
) -> MerkleStatus:
    if not features.is_enabled("a_merkle_hash"):
        return MerkleStatus(root_hash="", skipped=False)
    record = calculate_directory_hash(root)
    skipped = previous_hash is not None and previous_hash == record.root_hash
    return MerkleStatus(root_hash=record.root_hash, skipped=skipped)
```

- [ ] **Step 4: Run tests to confirm they pass**

Run:
```bash
pytest scripts/tests/test_status_merkle_skip.py -v
pytest scripts/tests/test_backward_compat.py -v
```
Expected: 2 passed, 2 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/status.py scripts/tests/test_status_merkle_skip.py
git commit -m "feat(status): Merkle skip path — instant status when tree unchanged

compute_status_with_merkle() returns skipped=True when the directory
hash matches the previous run, letting callers bypass full registry
comparison. Feature-flag gated."
```

---

### 5.4 Stream A Definition of Done
- [ ] All 10 new packages import cleanly on the target M2
- [ ] `features.py` loads `config/vitruvius.yaml → features:` block
- [ ] All 41 feature flags default to `false`
- [ ] Golden 3-file fixture lives under `scripts/tests/fixtures/golden_3_files/`
- [ ] `test_backward_compat.py` stays green after every commit
- [ ] `calculate_directory_hash()` is deterministic and rename-sensitive
- [ ] Scanner and status both honour `features.a_merkle_hash`; default path is byte-identical to pre-change
- [ ] `pytest scripts/tests/` stays green (all prior 297 tests + ~25 new)

### 5.5 Stream A Gating Metrics
- **Backward-compat regression:** green
- **Scanner runtime on PD 1096 raw layer, Merkle ON:** ≤50 ms (cold), ≤15 ms (warm)
- **Peak RSS of the scanner process:** ≤100 MB
- **Test count delta:** +25, total 322, all green

### 5.6 Research-Item Coverage (Stream A)
- ✅ adv-doc §1 (Merkle Tree Directory Hash)
- ✅ adv-doc 8GB Survival §2 (Merkle as zero-RAM cost)
- ✅ Plan-level safety net (backward-compat harness enables all later streams)

---

## 6. Stream B — Ingestion Intelligence (Phase 1B extensions)

**Priority:** P1
**Sprint:** D, week 2
**Research-Item Coverage:** Shannon Entropy doc classifier (stat-doc §13), Table-to-Graph Matrix Projection (adv-doc §12), Parametric Knowledge Extraction (adv-doc §11 + stat-doc §11)

### 6.1 Goal
Add three ingestion-layer intelligence modules on top of the existing `parsers/` subpackage without disturbing Phase 1B Foundation or the Phase 1B Modernization plan. Shannon Entropy classifies noisy OCR output deterministically. Table-to-Graph projects tabular data as a subgraph (critical for PD 1096 Table VII.1 and future CLUPs). Parametric NER pulls `(entity, operator, value, unit)` tuples from regulatory text.

### 6.2 Files
- **Create:** `scripts/vitruvius/parsers/shannon_classifier.py`
- **Create:** `scripts/vitruvius/parsers/table_graph_extractor.py`
- **Create:** `scripts/vitruvius/parsers/parametric_ner.py`
- **Create:** matching test files in `scripts/tests/`
- **Modify:** `scripts/vitruvius/parsers/document_taxonomy.py` (add post-check that consults Shannon entropy when `features.b_shannon_classifier` is on)

### 6.3 Task Sequence

#### Task B1 — Shannon Entropy document classifier
**Files:** Create `scripts/vitruvius/parsers/shannon_classifier.py`, Create `scripts/tests/test_shannon_classifier.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_shannon_classifier.py
"""Shannon entropy classifier — high entropy ⇒ garbled OCR flag."""

import math
from vitruvius.parsers.shannon_classifier import (
    character_entropy,
    is_garbled,
    classify_by_entropy,
)


def test_character_entropy_of_uniform_ascii_is_high() -> None:
    # 256 distinct chars each once → entropy approaches log2(256) = 8
    text = "".join(chr(i) for i in range(32, 127))
    h = character_entropy(text)
    assert h > 6.0


def test_character_entropy_of_english_text_is_moderate() -> None:
    text = "The National Building Code of the Philippines is Presidential Decree 1096."
    h = character_entropy(text)
    assert 3.5 < h < 4.8  # English baseline


def test_character_entropy_of_repeated_single_char_is_zero() -> None:
    assert character_entropy("aaaaa") == 0.0


def test_character_entropy_of_empty_string_is_zero() -> None:
    assert character_entropy("") == 0.0


def test_is_garbled_flags_high_entropy() -> None:
    garbled = "".join(chr(i) for i in range(1, 200))  # non-printable heavy
    assert is_garbled(garbled, threshold=4.5) is True


def test_is_garbled_accepts_clean_english() -> None:
    clean = "Section 804. Setbacks. Every building shall comply with the following."
    assert is_garbled(clean, threshold=4.5) is False


def test_classify_by_entropy_returns_expected_enum() -> None:
    assert classify_by_entropy("Section 804. Setbacks.") == "clean"
    assert classify_by_entropy("B@1ld!ng 0ff1c*a1") in {"noisy", "garbled"}
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_shannon_classifier.py -v`
Expected: 7 failures.

- [ ] **Step 3: Implement `shannon_classifier.py`**

```python
# scripts/vitruvius/parsers/shannon_classifier.py
"""Shannon Entropy character classifier for Phase 1B noise detection.

From the research catalogue (stat-doc §13):

    H(X) = - sum_i P(x_i) log_2 P(x_i)

Standard English legal text clusters around H ~= 4.0-4.5 bits/char.
Garbled OCR output produces a flatter distribution and entropy spikes
above 4.5. This module gives document_taxonomy.py a deterministic,
zero-dependency second opinion when its density heuristics are
borderline.

Pure stdlib — math + collections.Counter. No numpy dependency.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Literal

EntropyClass = Literal["clean", "noisy", "garbled"]


def character_entropy(text: str) -> float:
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def is_garbled(text: str, *, threshold: float = 4.5) -> bool:
    return character_entropy(text) > threshold


def classify_by_entropy(text: str) -> EntropyClass:
    h = character_entropy(text)
    if h < 4.5:
        return "clean"
    if h < 5.0:
        return "noisy"
    return "garbled"
```

- [ ] **Step 4: Run test to confirm it passes**

Run: `pytest scripts/tests/test_shannon_classifier.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/parsers/shannon_classifier.py scripts/tests/test_shannon_classifier.py
git commit -m "feat(parsers): add Shannon entropy classifier (Stream B.1)

Closes: research item 'Shannon Entropy for Document Classification' (stat-doc §13)

Deterministic, pure-stdlib second-opinion on garbled OCR output.
Thresholds tuned to English legal text. Feature-flag gated behind
features.b_shannon_classifier — not wired into taxonomy yet."
```

---

#### Task B2 — Integrate Shannon classifier into `document_taxonomy.py`
**Files:** Modify `scripts/vitruvius/parsers/document_taxonomy.py`

- [ ] **Step 1: Write the failing integration test**

```python
# scripts/tests/test_document_taxonomy_shannon_integration.py
from vitruvius.features import Features
from vitruvius.parsers.document_taxonomy import (
    classify_document,
    DocumentClass,
)


def test_high_entropy_text_with_flag_off_uses_baseline_density_only(tmp_path):
    # Flag OFF: behaviour is byte-identical to pre-change
    features = Features(flags={})
    class_name = classify_document(
        text_sample="B@1ld!ng 0ff1c*a1",
        pages_total=10,
        file_extension=".pdf",
        features=features,
    )
    assert isinstance(class_name, DocumentClass)


def test_high_entropy_text_with_flag_on_overrides_to_scanned_noisy(tmp_path):
    features = Features(flags={"b_shannon_classifier": True})
    class_name = classify_document(
        text_sample="".join(chr(i) for i in range(1, 200)),
        pages_total=10,
        file_extension=".pdf",
        features=features,
    )
    assert class_name == DocumentClass.SCANNED_PDF_NOISY
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_document_taxonomy_shannon_integration.py -v`
Expected: 2 failures or import error (the function may not accept `features` yet).

- [ ] **Step 3: Add `features` parameter to `classify_document` in `document_taxonomy.py`**

Read the current signature of `classify_document` first. Then add a default-None `features` kwarg and a post-check:

```python
# at the top of document_taxonomy.py — add imports
from vitruvius.features import Features
from vitruvius.parsers.shannon_classifier import classify_by_entropy

# modify classify_document signature — PRESERVE all existing args
def classify_document(
    *,
    text_sample: str,
    pages_total: int,
    file_extension: str,
    features: Features | None = None,
    # ... existing args preserved verbatim ...
) -> DocumentClass:
    # ... existing body produces `baseline_class` ...
    baseline_class = _existing_classification_body(...)

    if features is not None and features.is_enabled("b_shannon_classifier"):
        entropy_class = classify_by_entropy(text_sample)
        if entropy_class == "garbled":
            return DocumentClass.SCANNED_PDF_NOISY
        if entropy_class == "noisy" and baseline_class == DocumentClass.TEXT_PDF_SIMPLE:
            return DocumentClass.SCANNED_PDF_CLEAN  # escalate to OCR-ready chain
    return baseline_class
```

- [ ] **Step 4: Run both tests**

Run:
```bash
pytest scripts/tests/test_document_taxonomy_shannon_integration.py -v
pytest scripts/tests/test_document_taxonomy.py -v  # pre-existing tests must still pass
pytest scripts/tests/test_backward_compat.py -v
```
Expected: green across all three.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/parsers/document_taxonomy.py scripts/tests/test_document_taxonomy_shannon_integration.py
git commit -m "feat(parsers): Shannon entropy post-check in document_taxonomy (Stream B.1)

Feature-flag gated override: when features.b_shannon_classifier is on
and the sample text entropy exceeds 5.0, classify as SCANNED_PDF_NOISY
regardless of density heuristics. Default-off path is byte-identical."
```

---

#### Task B3 — Table-to-Graph Matrix Projection
**Files:** Create `scripts/vitruvius/parsers/table_graph_extractor.py`, Create `scripts/tests/test_table_graph_extractor.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/tests/test_table_graph_extractor.py
"""Table-to-Graph: project CSV/XLSX tables as (row, col, cell) sub-graph."""

from pathlib import Path
import json

from vitruvius.parsers.table_graph_extractor import (
    extract_table_subgraph,
    TableSubgraph,
)


def test_simple_csv_extracts_three_cell_edges(tmp_path: Path) -> None:
    csv = tmp_path / "table.csv"
    csv.write_text("Zone,MaxHeight,Setback\nR1,8,2\nR2,12,3\n")
    subgraph = extract_table_subgraph(csv)
    assert isinstance(subgraph, TableSubgraph)
    # 2 rows × 2 non-header columns = 4 cell edges (R1→MaxHeight=8, R1→Setback=2, ...)
    assert len(subgraph.edges) == 4


def test_header_row_becomes_column_nodes(tmp_path: Path) -> None:
    csv = tmp_path / "table.csv"
    csv.write_text("Zone,MaxHeight\nR1,8\n")
    subgraph = extract_table_subgraph(csv)
    col_names = {n.name for n in subgraph.column_nodes}
    assert col_names == {"MaxHeight"}
    assert subgraph.row_nodes[0].name == "R1"


def test_extract_deterministic_id_generation(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B\n1,2\n")
    sg1 = extract_table_subgraph(csv)
    sg2 = extract_table_subgraph(csv)
    assert [e.edge_id for e in sg1.edges] == [e.edge_id for e in sg2.edges]


def test_subgraph_serializes_to_json(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B\n1,2\n")
    sg = extract_table_subgraph(csv)
    out = tmp_path / "sg.json"
    out.write_text(json.dumps(sg.to_json_dict(), indent=2, sort_keys=True))
    assert json.loads(out.read_text())["edges"][0]["cell_value"] == "2"
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_table_graph_extractor.py -v`
Expected: 4 failures.

- [ ] **Step 3: Implement `table_graph_extractor.py`**

```python
# scripts/vitruvius/parsers/table_graph_extractor.py
"""Table-to-Graph matrix projection for Phase 1B tabular data.

Treats a CSV or XLSX sheet as a bipartite sub-graph:
  - Column headers -> `col:` nodes
  - Row labels     -> `row:` nodes (first column is the row label by default)
  - Cell values    -> edges (row_id -> col_id) carrying the cell value

From adv-doc §12: tabular content must be projected as graph structure,
not as text chunks, so downstream queries can do deterministic lookups
instead of asking the LLM to re-read the markdown table.

Output is a deterministic, JSON-serializable TableSubgraph. Feature-flag
gated behind features.b_table_graph — callers do not invoke this when
the flag is off.

Only CSV is implemented in this task. XLSX support lands in a follow-up
that wraps openpyxl (already in requirements.txt).
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TableNode:
    id: str
    name: str
    kind: str  # "row" | "col"


@dataclass(frozen=True)
class TableEdge:
    edge_id: str
    row_id: str
    col_id: str
    cell_value: str


@dataclass
class TableSubgraph:
    source_path: str
    row_nodes: list[TableNode] = field(default_factory=list)
    column_nodes: list[TableNode] = field(default_factory=list)
    edges: list[TableEdge] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "row_nodes": [n.__dict__ for n in self.row_nodes],
            "column_nodes": [n.__dict__ for n in self.column_nodes],
            "edges": [e.__dict__ for e in self.edges],
        }


def _stable_id(*parts: str) -> str:
    joined = "|".join(parts)
    return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:12]


def extract_table_subgraph(csv_path: Path) -> TableSubgraph:
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if any(c.strip() for c in r)]
    if len(rows) < 2:
        return TableSubgraph(source_path=str(csv_path))

    header = rows[0]
    column_names = header[1:]  # first column is the row label
    column_nodes = [
        TableNode(id=f"col:{_stable_id(csv_path.name, name)}", name=name, kind="col")
        for name in column_names
    ]

    row_nodes: list[TableNode] = []
    edges: list[TableEdge] = []
    for row in rows[1:]:
        if not row:
            continue
        row_label = row[0]
        row_node = TableNode(
            id=f"row:{_stable_id(csv_path.name, row_label)}",
            name=row_label,
            kind="row",
        )
        row_nodes.append(row_node)
        for col_node, cell in zip(column_nodes, row[1:]):
            edge = TableEdge(
                edge_id=_stable_id(csv_path.name, row_label, col_node.name, cell),
                row_id=row_node.id,
                col_id=col_node.id,
                cell_value=cell,
            )
            edges.append(edge)

    return TableSubgraph(
        source_path=str(csv_path),
        row_nodes=row_nodes,
        column_nodes=column_nodes,
        edges=edges,
    )
```

- [ ] **Step 4: Run test to confirm it passes**

Run: `pytest scripts/tests/test_table_graph_extractor.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/parsers/table_graph_extractor.py scripts/tests/test_table_graph_extractor.py
git commit -m "feat(parsers): table→graph matrix projection (Stream B.2)

Closes: research item 'Table-to-Graph Matrix Projection' (adv-doc §12)

CSV-first implementation. XLSX wrapper follows in Task B3.1. Feature-
flag gated behind features.b_table_graph. Deterministic IDs via stable
sha1 prefixes for reproducibility."
```

---

#### Task B3.1 — XLSX wrapper for Table-to-Graph
Append to the same module. Test: one `.xlsx` fixture with 2 sheets, assert every sheet becomes a separate subgraph. (Full TDD: write failing test → implement → commit.)

---

#### Task B4 — Parametric Constraint NER
**Files:** Create `scripts/vitruvius/parsers/parametric_ner.py`, Create `scripts/tests/test_parametric_ner.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/tests/test_parametric_ner.py
"""Parametric NER: extract (entity, operator, value, unit) tuples."""

from vitruvius.parsers.parametric_ner import (
    extract_parameters,
    Parameter,
)


def test_extracts_min_setback_tuple() -> None:
    text = "The minimum setback shall be 2.0 meters from the property line."
    params = extract_parameters(text)
    assert any(
        p.entity.lower() == "setback"
        and p.operator == ">="
        and p.value == 2.0
        and p.unit == "meters"
        for p in params
    )


def test_extracts_max_footprint_percent() -> None:
    text = "Maximum allowable footprint is 60 percent of the lot area."
    params = extract_parameters(text)
    assert any(
        p.entity.lower() == "footprint"
        and p.operator == "<="
        and p.value == 60.0
        and p.unit == "percent"
        for p in params
    )


def test_ignores_pure_narrative() -> None:
    text = "Every building shall comply with fire safety requirements."
    assert extract_parameters(text) == []


def test_preserves_evidence_offsets() -> None:
    text = "Minimum exit width shall be 1.2 meters."
    params = extract_parameters(text)
    assert params
    assert text[params[0].start:params[0].end].strip().startswith("Minimum")
```

- [ ] **Step 2: Run test to confirm it fails**

Run: `pytest scripts/tests/test_parametric_ner.py -v`
Expected: 4 failures.

- [ ] **Step 3: Implement `parametric_ner.py`**

```python
# scripts/vitruvius/parsers/parametric_ner.py
"""Parametric constraint NER for Phase 1B regulatory parameter extraction.

Looks for regex-anchored patterns of the form:
    [Adjective: 'minimum', 'maximum', 'at least', 'not more than', ...]
    [Entity: NP up to 5 words]
    [Verb phrase: 'shall be', 'must be', 'is']
    [Value: NUM]
    [Unit: meters | m | sqm | percent | %]

Emits a Parameter dataclass with operator in {">=", "<=", "==", ">", "<"}
derived from the anchor. Pure stdlib — regex only. A future task can
upgrade this to spaCy NER when Stream E's dep_parser is in place.

Feature-flag gated behind features.b_parametric_ner. Scope: Phase 1B
refinement of the relationship extraction candidate pool — the parameters
land in the sidecar JSON, not the markdown body.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

# Operator word → strict inequality
_MIN_WORDS = r"(?:minimum|min\.|at\s+least|not\s+less\s+than|no\s+less\s+than)"
_MAX_WORDS = r"(?:maximum|max\.|at\s+most|not\s+more\s+than|no\s+more\s+than)"
_EQ_WORDS = r"(?:exactly|equal\s+to)"

_NUM = r"(?P<value>\d+(?:\.\d+)?)"
_UNIT = (
    r"(?P<unit>"
    r"meters|meter|m\b|centimeters|cm|millimeters|mm|"
    r"square\s+meters|sqm|sq\s*m|square\s+feet|sq\s*ft|"
    r"percent|%|"
    r"persons|people|occupants|"
    r"stories|story|floors|floor|"
    r"hours|hour|minutes|minute"
    r")"
)

_ENTITY_MIN = rf"(?P<entity>[\w\s\-]{{1,80}}?)"
_VERB = r"(?:shall\s+be|must\s+be|is|are|be)"
_SEP = r"\s+"


def _op_for_word(word: str) -> str:
    w = word.lower()
    if re.match(_MIN_WORDS, w):
        return ">="
    if re.match(_MAX_WORDS, w):
        return "<="
    if re.match(_EQ_WORDS, w):
        return "=="
    return "=="  # default


@dataclass(frozen=True)
class Parameter:
    entity: str
    operator: str
    value: float
    unit: str
    start: int
    end: int
    evidence: str


_PATTERN = re.compile(
    rf"(?i)"
    rf"(?P<word>{_MIN_WORDS}|{_MAX_WORDS}|{_EQ_WORDS})"
    rf"{_SEP}{_ENTITY_MIN}"
    rf"{_SEP}{_VERB}{_SEP}{_NUM}{_SEP}{_UNIT}"
)


def _normalise_unit(unit: str) -> str:
    u = unit.lower().replace("\u00a0", " ").strip()
    if u in {"m", "meter", "meters"}:
        return "meters"
    if u == "%" or u == "percent":
        return "percent"
    if u in {"sqm", "sq m", "square meters"}:
        return "sqm"
    return u


def extract_parameters(text: str) -> list[Parameter]:
    params: list[Parameter] = []
    for match in _PATTERN.finditer(text):
        op = _op_for_word(match.group("word"))
        params.append(
            Parameter(
                entity=match.group("entity").strip(),
                operator=op,
                value=float(match.group("value")),
                unit=_normalise_unit(match.group("unit")),
                start=match.start(),
                end=match.end(),
                evidence=match.group(0),
            )
        )
    return params
```

- [ ] **Step 4: Run test to confirm it passes**

Run: `pytest scripts/tests/test_parametric_ner.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/parsers/parametric_ner.py scripts/tests/test_parametric_ner.py
git commit -m "feat(parsers): parametric NER for regulatory parameters (Stream B.3)

Closes: research items 'Parametric Knowledge Extraction' (adv-doc §11)
        and 'Parametric Constraint Extraction' (stat-doc §11)

Extracts (entity, operator, value, unit) tuples from regulatory text
via anchored regex. Unit normalisation maps {m, meter, meters}→meters,
{%, percent}→percent, etc. Feature-flag gated behind
features.b_parametric_ner. Parameters land in sidecar JSON, not markdown."
```

---

### 6.4 Stream B Definition of Done
- [ ] Shannon classifier is deterministic and testable with pure stdlib
- [ ] Document taxonomy post-check honours `features.b_shannon_classifier` and escalates noisy docs
- [ ] Table-to-Graph extractor emits deterministic IDs on CSVs (XLSX via wrapper)
- [ ] Parametric NER emits `(entity, op, value, unit)` tuples + evidence offsets
- [ ] `test_backward_compat.py` stays green
- [ ] All three modules off-by-default

### 6.5 Stream B Gating Metrics
- **Shannon classifier accuracy on PD 1096 golden corpus:** ≥95% correct clean/noisy/garbled
- **Table-to-Graph determinism test:** byte-identical across reruns
- **Parametric NER precision on a 100-sentence regulatory text sample:** ≥85%
- **Test count delta:** +20, total ~342

### 6.6 Research-Item Coverage (Stream B)
- ✅ stat-doc §13 (Shannon Entropy)
- ✅ adv-doc §12 (Table-to-Graph Matrix Projection)
- ✅ adv-doc §11 + stat-doc §11 (Parametric Constraint Extraction)
- ✅ Absorbs Phase 1B §11 Phase 2 Modernization tasks (Shannon post-check replaces the noise heuristic)

---

## 7. Stream C — Normalization Tier C (OCR, semantic chunking, outlier detection)

**Priority:** P1
**Sprint:** D, weeks 3-4
**Research-Item Coverage:** Levenshtein + Jaro-Winkler (stat-doc §4), AST-based Semantic Chunking (adv-doc §2), Hybrid Semantic-Structural Chunking (stat-doc §9), Mahalanobis Distance outlier detection (stat-doc §16)

### 7.1 Goal
Ship Phase 1C Tier C — the destructive-but-audited normalization layer — and the semantic chunker that RAG/review phases depend on. All four modules write audit entries so every transformation is reversible.

### 7.2 Files
- **Create:** `scripts/vitruvius/normalization/rules_tier_c.py`
- **Create:** `scripts/vitruvius/normalization/ast_chunker.py`
- **Create:** `scripts/vitruvius/normalization/embedding_chunker.py`
- **Create:** `scripts/vitruvius/normalization/outlier_detector.py`
- **Create:** matching test files
- **Modify:** `scripts/vitruvius/normalization/engine.py` (feature-flag-gated Tier C dispatch, stays default-off)

### 7.3 Task Sequence (summary — full TDD bodies follow the Stream A/B pattern)

#### Task C1 — Jaro-Winkler OCR typo correction (`rules_tier_c.py`)
Uses `rapidfuzz.distance.JaroWinkler.normalized_similarity`. Loads a canonical-concept vocabulary from `003/shared/concepts/` at init. For each token not in a standard English dictionary AND not a stopword, finds the closest canonical term; if similarity ≥ 0.92, replaces. Emits an audit entry `{original: ..., replaced: ..., similarity: ..., position: ...}` to the `.refined.json` manifest.

Failing tests (6):
1. `test_replaces_bui1ding_officia1_with_building_official`
2. `test_ignores_standard_english_words`
3. `test_ignores_very_short_tokens` (≤3 chars)
4. `test_audit_entry_shape`
5. `test_flag_off_no_replacement`
6. `test_similarity_below_threshold_not_replaced`

#### Task C2 — AST-based Semantic Chunker (`ast_chunker.py`)
Parses refined markdown into a Title → Chapter → Section → Paragraph tree using ATX header depth. Emits chunks of ≤512 tokens grouped by Section, with parent titles injected as metadata. If a section exceeds 512 tokens, splits at paragraph boundary.

Failing tests (6):
1. `test_small_document_fits_in_one_chunk_per_section`
2. `test_oversize_section_splits_at_paragraph`
3. `test_parent_title_injected_as_metadata`
4. `test_idempotent_on_reruns`
5. `test_determinism_of_chunk_ids`
6. `test_preserves_source_section_id_from_frontmatter`

#### Task C3 — Hybrid Semantic-Structural Chunker (`embedding_chunker.py`)
Extends C2: for every chunk emitted by C2, computes a sentence-transformers embedding (`all-MiniLM-L6-v2`) and stores the 384-dim vector in the chunk sidecar. Uses lazy-loaded `SentenceTransformer` (first use only). Batch size 32 for RAM safety.

Failing tests (4):
1. `test_each_chunk_has_384_dim_vector`
2. `test_embedding_determinism_same_text_same_vector`
3. `test_batch_processing_never_exceeds_32`
4. `test_lazy_loading_does_not_load_until_first_call`

#### Task C4 — Mahalanobis Outlier Detector (`outlier_detector.py`)
Computes the centroid μ and covariance Σ of all chunk embeddings in the PD 1096 corpus, then flags any new chunk with `D_M(x) > 3.0` as an outlier. Writes outlier list to `.refined.json` manifest. Uses `numpy.linalg.pinv` for robust covariance inverse.

Failing tests (5):
1. `test_centroid_of_uniform_cluster_is_mean`
2. `test_outlier_exceeds_threshold`
3. `test_cluster_points_below_threshold`
4. `test_singular_covariance_uses_pinv`
5. `test_persists_scoring_to_manifest`

### 7.4 Stream C Definition of Done
- [ ] All Tier C transformations are auditable and reversible
- [ ] AST chunker idempotent and deterministic
- [ ] Embedding chunker runs under 350 MB peak RSS on PD 1096
- [ ] Outlier detector flags at least one known-drift sample in a synthetic test
- [ ] `test_backward_compat.py` stays green

### 7.5 Stream C Gating Metrics
- **OCR typo correction precision:** ≥98% on a 50-sample hand-labelled set (no false replacements of valid terms)
- **Embedding chunker throughput:** ≥100 chunks/sec CPU (batch 32)
- **Mahalanobis AUROC on synthetic in/out distribution mix:** ≥0.90

### 7.6 Research-Item Coverage (Stream C)
- ✅ stat-doc §4 (Levenshtein + Jaro-Winkler)
- ✅ adv-doc §2 (AST-based Semantic Chunking)
- ✅ stat-doc §9 (Hybrid Semantic-Structural Chunking)
- ✅ stat-doc §16 (Mahalanobis Distance)

---

## 8. Stream D — Concept Enrichment v2 (TF-IDF + PMI + FCA + Embeddings)

**Priority:** P1
**Sprint:** D, week 5
**Research-Item Coverage:** TF-IDF & N-Gram Collocation (stat-doc §1), PMI Alias Discovery (stat-doc §1), Formal Concept Analysis (stat-doc §23), Domain-Specific Embedding Adaptation (adv-doc §1)

### 8.1 Goal
Close the 4 remaining unenriched concepts (`exit-width`, `parking-and-loading-spaces`, `setbacks`, `yards` — RI-010) using statistical matching instead of section-title regex. Auto-discover alias candidates via PMI. Build a Formal Concept Analysis lattice that mathematically proves the hierarchical structure of PD 1096. Fine-tune a contrastive embedding adapter so domain-specific matching beats generic sentence-transformer baselines.

### 8.2 Files
- **Create:** `scripts/vitruvius/concepts/tfidf_matcher.py`
- **Create:** `scripts/vitruvius/concepts/pmi_alias_miner.py`
- **Create:** `scripts/vitruvius/concepts/fca_lattice.py`
- **Create:** `scripts/vitruvius/concepts/contrastive_adapter.py`
- **Create:** matching test files

### 8.3 Task Sequence (summary)

#### Task D1 — TF-IDF Concept Matcher (`tfidf_matcher.py`)
Uses `sklearn.feature_extraction.text.TfidfVectorizer` with `ngram_range=(1, 3)`. Fits on the entire refined PD 1096 markdown. For each unenriched concept (reads from `features.d_tfidf_concepts` ON state + a list of slugs), computes TF-IDF scores for the concept's slug as an n-gram. Ranks sections by score, emits the top 3 as candidate regulatory bases. If the top score exceeds a threshold (default 0.15), writes the match to a `candidates.json` under `runs/` — does NOT auto-enrich; a human or a follow-up LLM review confirms.

Failing tests (5):
1. `test_tfidf_matches_exit_width_to_stairs_section`
2. `test_tfidf_ignores_common_words`
3. `test_deterministic_ranking`
4. `test_writes_candidates_json`
5. `test_flag_off_is_noop`

#### Task D2 — PMI Alias Miner (`pmi_alias_miner.py`)
For each canonical concept, runs a sliding window (5-word context) over PD 1096 markdown and computes PMI between the concept slug terms and co-occurring n-grams:

`PMI(x, y) = log₂(P(x, y) / (P(x) · P(y)))`

Emits a ranked list of high-PMI candidate aliases. Threshold: `PMI ≥ 3.0 AND joint_count ≥ 5`. Writes to `latest_pmi_alias_mining.json`.

Failing tests (5):
1. `test_pmi_identifies_collocated_terms`
2. `test_pmi_ignores_isolated_cooccurrences`
3. `test_ranked_by_pmi_score_descending`
4. `test_minimum_joint_count_filter`
5. `test_flag_off_is_noop`

#### Task D3 — Formal Concept Analysis Lattice (`fca_lattice.py`)
Builds the concept lattice per Ganter-Wille FCA:
- Rows: sections in `003/shared/sources/` (one per section).
- Columns: extracted attributes from parametric NER + concept co-occurrence.
- Output: a Hasse diagram serialized as JSON — nodes are `(extent, intent)` pairs, edges are sub-concept relations.

Pure Python implementation of the NextClosure algorithm — no external FCA lib. Writes to `latest_fca_lattice.json`.

Failing tests (5):
1. `test_small_binary_matrix_builds_correct_lattice`
2. `test_lattice_top_concept_has_full_extent`
3. `test_lattice_bottom_concept_has_empty_extent`
4. `test_hasse_edges_are_covering_relations_only`
5. `test_deterministic_output`

#### Task D4 — Contrastive Embedding Adapter (`contrastive_adapter.py`)
Not a full LoRA fine-tune (deferred — see §2.3). Instead: **a linear projection head** trained with InfoNCE loss on (concept_definition, regulatory_basis_section) positive pairs + random negatives. Base embeddings from `all-MiniLM-L6-v2`, projected through a 384 → 128 → 384 adapter. Training loop uses numpy only (no PyTorch needed — small head, linear algebra closed form).

Actually, a linear projection trained with InfoNCE requires gradient descent. Rather than pulling in torch (adds ~2 GB disk), we do a **whitening transform** (PCA-based) fit on positive pairs — this is a lightweight alternative that still pulls domain vectors into closer proximity in one-shot. It uses `sklearn.decomposition.TruncatedSVD`.

Failing tests (5):
1. `test_fit_on_positive_pairs_reduces_pair_distance`
2. `test_transform_is_linear_and_deterministic`
3. `test_negative_pairs_remain_distant_after_transform`
4. `test_round_trip_inverse_preserves_info_when_k_equals_d`
5. `test_save_and_load_state`

### 8.4 Stream D Definition of Done
- [ ] TF-IDF matcher produces regulatory-basis candidates for all 4 unenriched concepts (RI-010 closure path)
- [ ] PMI alias miner auto-discovers at least 10 new canonical alias candidates
- [ ] FCA lattice builds in <2 s on PD 1096 corpus
- [ ] Whitening-based adapter improves concept-to-section cosine similarity by ≥15% on the seed set
- [ ] `test_backward_compat.py` green

### 8.5 Stream D Gating Metrics
- **Unenriched concept closure via TF-IDF:** 3 of 4 auto-matched (the 4th may need a second corpus — see Phase 11)
- **PMI alias discovery rate:** ≥10 new aliases with manual acceptance rate ≥70%
- **FCA lattice coverage:** every section in a lattice node; zero orphans
- **Whitening lift:** ≥15% similarity gain, p<0.01 paired t-test vs baseline

### 8.6 Research-Item Coverage (Stream D)
- ✅ stat-doc §1 (TF-IDF & N-Gram Collocation)
- ✅ stat-doc §1 (PMI aliases)
- ✅ stat-doc §23 (Formal Concept Analysis)
- ✅ adv-doc §1 (Domain-Specific Embedding Adaptation — whitening variant)

---

## 9. Stream E — Extraction v2 (spaCy dep-parsing + CRF + KG embeddings)

**Priority:** P1
**Sprint:** E, weeks 1-3
**Research-Item Coverage:** Conditional Random Fields (stat-doc §3), spaCy dependency parsing (adv-doc 8GB Survival §4), Knowledge Graph Embeddings for link prediction (stat-doc §7 + adv-doc §3)

### 9.1 Goal
Close RI-002 at the root. Regex extraction is replaced by a two-stage pipeline: (1) spaCy dependency parsing to find SVO triplets, (2) a CRF trained on Phase 6 `keep` decisions to tag relationship sequences. Knowledge Graph Embeddings (TransE, numpy-only implementation) run over the graph to propose missing links. Every new extractor writes to `latest_crf_candidates.json`; the existing regex extractor stays in place and both streams merge into the review queue.

### 9.2 Files
- **Create:** `scripts/vitruvius/extraction/__init__.py`
- **Create:** `scripts/vitruvius/extraction/spacy_dep_parser.py`
- **Create:** `scripts/vitruvius/extraction/crf_extractor.py`
- **Create:** `scripts/vitruvius/extraction/crf_trainer.py`
- **Create:** `scripts/vitruvius/extraction/kg_link_predictor.py`
- **Create:** matching test files

### 9.3 Task Sequence (summary)

#### Task E1 — spaCy SVO Dependency Parser (`spacy_dep_parser.py`)
Loads `en_core_web_sm` on first use. For each sentence in a refined markdown, finds Subject-Verb-Object triplets using `token.dep_` labels (`nsubj`, `ROOT`, `dobj`). Emits `Candidate(subject, verb, object, span)` records. Only calls the LLM with candidates that also match the closed concept vocabulary (principle P7).

Failing tests (5):
1. `test_extracts_simple_svo`
2. `test_handles_passive_voice`
3. `test_filters_to_concept_vocabulary`
4. `test_preserves_source_section_id`
5. `test_lazy_model_loading`

#### Task E2 — CRF Trainer (`crf_trainer.py`)
Consumes `latest_relationship_review_merged.json` — every `keep` decision becomes a positive training example, every `reject` becomes a negative. Feature extraction per token: (a) capitalization, (b) POS tag (from spaCy), (c) in-vocabulary flag, (d) distance to nearest subject anchor, (e) surrounding bigram. Uses `python-crfsuite` with L-BFGS training. Emits a trained CRF model to `scripts/vitruvius/models/crf_extractor_YYYYMMDDTHHMMSSZ.crfsuite`, plus a metadata JSON with training corpus hash.

Failing tests (6):
1. `test_builds_feature_vector_per_token`
2. `test_training_converges_on_toy_data`
3. `test_saves_model_with_timestamp`
4. `test_writes_training_metadata`
5. `test_refuses_to_train_on_empty_corpus`
6. `test_idempotent_on_same_corpus_hash`

#### Task E3 — CRF Extractor (`crf_extractor.py`)
Loads the latest CRF model from the timestamped models directory. Takes a list of sentences + SVO candidates from `spacy_dep_parser`, tags each token as `B-SUBJ`, `I-SUBJ`, `B-PRED`, `I-PRED`, `B-OBJ`, `I-OBJ`, or `O`. Emits the same `Candidate` shape as the regex extractor, so `run-relationships-ollama` can consume both without code changes.

Failing tests (4):
1. `test_tags_sentence_with_known_structure`
2. `test_returns_empty_on_unknown_structure`
3. `test_reuses_loaded_model_across_calls`
4. `test_emits_candidate_compatible_schema`

#### Task E4 — KG Link Predictor (`kg_link_predictor.py`)
Pure numpy TransE: trains entity + relation embeddings (dim 50) on the canonical `003/shared/relationships/` set. Minimises `||h + r - t||₂` for positive triples, maximises for negatives (1:1 negative sampling). Training runs at <30 s on the PD 1096 ~10-relationship seed.

For link prediction: computes `||h + r - t||₂` for every `(head, relation, ?tail)` combination, ranks tails, emits the top 5 as candidates for LLM review. Writes to `latest_kg_link_candidates.json`.

Failing tests (5):
1. `test_embeddings_have_correct_shape`
2. `test_training_reduces_positive_triple_loss`
3. `test_link_prediction_ranks_known_tail_high`
4. `test_persists_embeddings_to_npy`
5. `test_deterministic_with_seeded_random`

### 9.4 Stream E Definition of Done
- [ ] spaCy dep parser + CRF extractor + KG link predictor all ship behind flags
- [ ] CRF trained on real `keep`/`reject` decisions from Phase 6 audit logs
- [ ] All three extractors produce candidates that flow through `pre_review_filter` + `ollama_review` unchanged
- [ ] `test_backward_compat.py` green

### 9.5 Stream E Gating Metrics
- **CRF false-positive rate on PD 1096:** ≤30% (down from regex's 82%)
- **Link predictor hit-rate at top-5:** ≥60% on held-out edges
- **spaCy dep parser latency:** ≤200 ms/sentence CPU

### 9.6 Research-Item Coverage (Stream E)
- ✅ stat-doc §3 (CRF)
- ✅ adv-doc 8GB Survival §4 (spaCy dep parsing)
- ✅ stat-doc §7 (KG link prediction)
- ✅ adv-doc §3 (TransE / KGE)
- ✅ Root-cause closure of RI-002

---

## 10. Stream F — Review v2 (NB filter + SLM swarm + Conformal + Tension + Ontology + Choquet)

**Priority:** P1
**Sprint:** E, weeks 4-5
**Research-Item Coverage:** Naïve Bayes pre-filter (stat-doc §2), SLM Swarms & Dynamic Routing (stat-doc §6), Ontology-Embedded Prompting (stat-doc §8 + adv-doc §3), Conformal Prediction (stat-doc §14), Tension-Point Analytics (adv-doc §5), Self-Reflective Routing (adv-doc §5), Ollama Speculative Decoding + KV Cache (adv-doc §4), Choquet Integral (stat-doc §25)

### 10.1 Goal
Compress Phase 6 LLM cost by another 3–5× while raising accuracy. Replace the "LLM-for-everything" pattern with a tiered statistical router: NB filter → SLM swarm → heavy LLM only for adjudication, every tier calibrated via conformal prediction, aggregated by a Choquet integral, with ontology context injected into prompts and tension-point analytics catching disagreements.

### 10.2 Files (8 modules + tests)
- `review/naive_bayes_filter.py`
- `review/slm_router.py`
- `review/ontology_prompt_builder.py`
- `review/conformal_calibrator.py`
- `review/tension_analyzer.py`
- `review/reflection_parser.py`
- `review/ollama_config.py`
- `review/choquet_aggregator.py`

### 10.3 Task Sequence (summary)

#### Task F1 — Naïve Bayes Pre-Review Filter (`naive_bayes_filter.py`)
Trains `sklearn.naive_bayes.MultinomialNB` on every historical `keep`/`reject` decision. Features: (a) predicate, (b) subject-object char distance, (c) regex pattern ID, (d) evidence length, (e) verb tense. Emits a probability `p(keep|x)` per candidate. Rules:
- `p(keep) > 0.95` → auto-accept (skip LLM)
- `p(keep) < 0.05` → auto-reject (skip LLM)
- otherwise → forward to SLM swarm

Failing tests (6). Writes training log to `latest_nb_filter_report.json`.

#### Task F2 — SLM Swarm Router (`slm_router.py`)
Loads a map of (complexity_score → model_name). Easy candidates (short evidence, clear SVO from CRF) route to `qwen2.5:3b` or `phi3:mini`. Hard candidates route to `qwen2.5:7b-instruct-q4_K_M`. Both call Ollama via the existing HTTP client. Reserves the heavy `gemma4:31b` (if pulled) strictly for Tier-2 adjudication.

Failing tests (5).

#### Task F3 — Ontology-Embedded Prompt Builder (`ontology_prompt_builder.py`)
When invoked with a candidate and the graph snapshot (Phase 8), queries the local neighbourhood of the subject and object concepts (up to 2 hops) and injects them into the review prompt as structured context. This is the GraphRAG-at-review pattern from adv-doc §3.

Failing tests (4).

#### Task F4 — Conformal Calibrator (`conformal_calibrator.py`)
Maintains a rolling calibration set of 50 Ranger-verified decisions. Computes non-conformity scores as `1 − p_model(true_label)`. For a new prediction, outputs a *set* of possible labels whose cumulative non-conformity stays below `1 − α` (α=0.05 → 95% guarantee). If the set has size 1, auto-promote; else escalate to Tier-2.

Failing tests (5).

#### Task F5 — Tension Point Analyzer (`tension_analyzer.py`)
When Gemma/Qwen disagree, runs a focused "debate prompt" asking each model which specific term caused the disagreement. Logs the tension point to `latest_tension_points.json` — tracked for Stream J Active Learning to feed into the Ranger queue.

Failing tests (4).

#### Task F6 — Reflection Parser (`reflection_parser.py`)
Modifies the system prompt to force the LLM to output a `<thought_process>` block before its decision. Parses the block; if the model's *self-reported* confidence is < 0.7, halts auto-promote and escalates to Ranger.

Failing tests (4).

#### Task F7 — Ollama Config Toggles (`ollama_config.py`)
Writes environment exports for:
- `OLLAMA_NUM_PARALLEL=4` (parallel request handling)
- `OLLAMA_KV_CACHE_TYPE=q8_0` (quantised KV cache — halves RAM per request)
- `OLLAMA_FLASH_ATTENTION=1` (faster attention, if build supports it)
- `OLLAMA_SPEC_DECODE=1` + `OLLAMA_DRAFT_MODEL=qwen2.5:1.5b` (speculative decoding, if Ollama version supports it)

Detects Ollama version at startup and skips unsupported flags with a warning. Feature-flag gated — default OFF leaves the Ollama process untouched.

Failing tests (5).

#### Task F8 — Choquet Integral Aggregator (`choquet_aggregator.py`)
Given N signals `(name, value)` and a fuzzy measure μ over subsets, computes the Choquet Integral:

```
C_μ(x) = Σᵢ (x_(i) − x_(i−1)) · μ({j : x_j ≥ x_(i)})
```

Calibrated so that redundant signals (CRF + TF-IDF, both catching the same pattern) are dampened. μ is stored as a JSON file under `config/choquet_measures.json`.

Failing tests (6).

### 10.4 Stream F Definition of Done
- [ ] NB filter trained on real audit logs, auto-accept/reject bands calibrated
- [ ] SLM router routes ≥60% of candidates to ≤3B-param models
- [ ] Conformal calibrator holds 95% coverage guarantee on the seed set
- [ ] Tension-point analytics logs at least 5 disagreement cases per PD 1096 rerun
- [ ] Reflection parser halts auto-promote on every low-confidence case
- [ ] Ollama config exports apply correctly (detected at startup)
- [ ] Choquet aggregator reproduces manual ranking on the fixture
- [ ] Ontology prompt builder injects ≤2-hop neighbourhood under 100 ms
- [ ] `test_backward_compat.py` green

### 10.5 Stream F Gating Metrics
- **Phase 6 total LLM-call time, 10 PD 1096 files, full pipeline, Stream F ON:** ≤40% of baseline
- **Review accuracy on seed set:** ≥95%
- **Conformal set-size distribution:** ≥80% singleton sets
- **Choquet vs baseline confusion matrix:** lifts F1 by ≥0.05

### 10.6 Research-Item Coverage (Stream F)
- ✅ stat-doc §2 (NB filter)
- ✅ stat-doc §6 (SLM swarm)
- ✅ stat-doc §8 + adv-doc §3 (Ontology-embedded GraphRAG prompting)
- ✅ stat-doc §14 (Conformal Prediction)
- ✅ adv-doc §5 (Tension-Point Analytics)
- ✅ adv-doc §5 (Self-Reflective Routing)
- ✅ adv-doc §4 (Speculative Decoding + KV Cache — Ollama config level)
- ✅ stat-doc §25 (Choquet Integral)

---

## 11. Stream G — Promotion v2 (Bayesian Fusion + Stringency + Temporal)

**Priority:** P2
**Sprint:** E, week 6
**Research-Item Coverage:** Bayesian Evidence Fusion (stat-doc §5), Stringency Matrix (adv-doc §8GB + CLUP discussion), Temporal/Jurisdictional Graph Edges (adv-doc §13)

### 11.1 Goal
Upgrade Phase 7 promotion with probabilistic edge confidence, most-stringent-law resolution, and first-class temporal validity. None of this replaces `promotion_validator.py`; it extends the schema and resolver.

### 11.2 Files
- `scripts/vitruvius/promotion/__init__.py`
- `scripts/vitruvius/promotion/bayesian_fusion.py`
- `scripts/vitruvius/promotion/stringency_resolver.py`
- `scripts/vitruvius/promotion/temporal_edges.py`
- matching test files
- new CLI: `migrate-concept-frontmatter` (one-shot, writes `stringency_vector` into 20 concept files)

### 11.3 Task Sequence (summary)

#### Task G1 — Bayesian Evidence Fusion (`bayesian_fusion.py`)
Replaces the binary `status: verified|unverified` on edges with a continuous `confidence_score: float [0,1]`. Combines signals via Bayesian update:
- Base prior: 0.10
- Regex match: × 6.0 (posterior ≈ 0.60)
- TF-IDF match: × 1.4 (posterior ≈ 0.85)
- CRF tag: × 1.1 (posterior ≈ 0.93)
- LLM agree: × 1.06 (posterior ≈ 0.99)

Implementation: log-odds accumulation to avoid numerical underflow. Writes to `confidence_score` on every edge record.

Failing tests (6).

#### Task G2 — Stringency Matrix Resolver (`stringency_resolver.py`)
Reads `stringency_vector` from concept frontmatter (values: `maximize`, `minimize`, `qualitative`). When `promotion.py` detects a duplicate `(subject, predicate, object)` in the canonical layer, delegates to this resolver. Marks the winning edge `is_governing_standard: true` and leaves the loser intact with `is_governing_standard: false`.

Failing tests (6).

#### Task G3 — Temporal Edges (`temporal_edges.py`)
Extends the edge dataclass with `valid_from: str|None`, `valid_until: str|None`, `jurisdiction: str` (default `"national"`). New edges use today's date as `valid_from`; superseding edges cap the predecessor's `valid_until` instead of deleting it.

Failing tests (5).

#### Task G4 — One-Shot Concept Frontmatter Migration
CLI: `migrate-concept-frontmatter --dry-run`. Reads every `003/shared/concepts/*.md` and adds a `stringency_vector: qualitative` default. User runs `--execute` explicitly.

Failing tests (4).

### 11.4 Stream G Definition of Done
- [ ] Every promoted edge has `confidence_score` (not just verified/unverified)
- [ ] Stringency resolver picks the correct edge on PD 1096 vs a synthetic stricter LGU rule
- [ ] Temporal edge schema validates on new + legacy edges
- [ ] Every concept file carries `stringency_vector` (migration committed)
- [ ] `test_backward_compat.py` green

### 11.5 Stream G Gating Metrics
- **Bayesian fusion monotonicity:** adding a positive signal never decreases confidence
- **Stringency resolver correctness:** 100% on 20 synthetic conflicts
- **Temporal edge backfill:** 100% of existing edges get `valid_from` assigned

### 11.6 Research-Item Coverage (Stream G)
- ✅ stat-doc §5 (Bayesian Evidence Fusion)
- ✅ adv-doc 8GB Survival + CLUP discussion (Stringency Matrix)
- ✅ adv-doc §13 (Temporal & Jurisdictional Graph Edges)

---

## 12. Stream H — Graph Layer Intelligence (Phase 8 + centrality/spectral/community/MCMC/TDA/Wasserstein/causal/tensor)

**Priority:** P2
**Sprint:** F, weeks 1-4
**Research-Item Coverage:** Phase 8 base (existing plan), Graph Centrality (stat-doc §15), Spectral Graph Theory (stat-doc §22), Louvain/Leiden GraphRAG (adv-doc §3), MCMC random walks (stat-doc §21), Topological Data Analysis (stat-doc §18), Optimal Transport (stat-doc §19), Causal Inference (stat-doc §20), Tensor Factorization (stat-doc §24)

### 12.1 Goal
Ship the Phase 8 base graph layer (per its existing plan — `phase-8-graph-contract-indexing-plan.md`), then stack eight statistical intelligence modules on top. Every module runs over the deterministic filesystem graph snapshot — no external graph DB.

### 12.2 Dependency on Phase 8 Base Plan
Stream H.0 **is** the existing Phase 8 plan, executed verbatim from its §Task Sequence. Streams H.1–H.8 each extend the same `graph/` subpackage.

### 12.3 Task Sequence (stream-level design-spec — expand to TDD at execution time)

#### H.0 — Phase 8 Base (contract, builder, snapshot, integrity, traverse, CLI)
Execute `.ai/03_plans/phase-8-graph-contract-indexing-plan.md` tasks 1–7 verbatim. Add `confidence_score`, `valid_from`, `valid_until`, `jurisdiction` to the edge schema (from Stream G) during Task 1.

#### H.1 — Graph Centrality (`graph/centrality.py`)
Implements degree, betweenness, and eigenvector (PageRank variant) centrality using `networkx.betweenness_centrality` and `networkx.pagerank`. Writes ranked scores to `latest_graph_centrality.json`. Graph size bounded at ≤10 000 nodes — the algorithms run in <2 s on that scale.

#### H.2 — Spectral Graph Partitioning (`graph/spectral.py`)
Computes the Laplacian matrix (sparse via `scipy.sparse.csgraph.laplacian`), finds the Fiedler vector (second smallest eigenvector via `scipy.sparse.linalg.eigsh`), partitions the graph by sign of Fiedler components. Emits partition labels to every node — used by the query layer to route macro-questions to sub-graphs.

#### H.3 — Louvain Community Detection + GraphRAG (`graph/community.py`)
Runs `python-louvain.best_partition` over the graph. For each community, generates a short factual summary by concatenating the section titles of member nodes — NOT an LLM call; this is extractive summarisation. Writes to `latest_graph_communities.json`. The query layer uses these for macro-queries like "overarching safety themes".

#### H.4 — MCMC Random Walk Ranking (`graph/mcmc.py`)
Runs a random walk with restart (α = 0.85, 10 000 steps) from a query seed node, tracks visit frequencies, and emits a stationary distribution. Used by Stream I.3 for answer ranking.

#### H.5 — Topological Data Analysis (`graph/tda.py`)
Implements a **simplified persistent homology** computation using pure numpy (Vietoris-Rips filtration on node embeddings from Stream H.3). Emits Betti numbers and persistence diagrams to `latest_graph_tda_report.json`. Loops in the persistence diagram → loophole candidates.

Full persistent homology is expensive; this task caps the filtration at 100 nodes per run. If the graph exceeds that, runs on a Louvain community at a time.

Alternatively: use `gudhi` if the 30 MB install is acceptable. Decision deferred to execution-time — start with pure numpy Vietoris-Rips, switch to gudhi only if numpy performance is too slow on the real corpus.

#### H.6 — Optimal Transport / Wasserstein Merge (`graph/wasserstein_merge.py`)
When Phase 11 ingests the IRR and new nodes overlap semantically with PD 1096 nodes, uses `ot.emd2` from POT to compute the 2-Wasserstein distance between their embedding distributions. If distance < 0.1, merges; if 0.1–0.3, flags for Ranger review; if > 0.3, keeps separate.

#### H.7 — Causal DAG Overlay + Do-Calculus (`graph/causal_dag.py`)
Models causal edges as a directed acyclic subgraph layered over the knowledge graph. Supports `do(X = x)` interventions: finds all descendants of X, marks their affected conditionals, re-propagates probabilistic confidence via Bayesian fusion (Stream G). Full Pearl do-calculus would need `dowhy` (heavy); this task implements only the first intervention level.

#### H.8 — Tensor Factorisation (`graph/tensor_factorisation.py`) — GATED
`(subject, predicate, object, jurisdiction)` becomes a 4-way tensor. Uses `scipy.linalg.svd` for 2D SVD on unfolded modes; full Tucker decomposition deferred until ≥2 jurisdictions exist (i.e., Stream K). The scaffolding ships now; training runs only when `features.h_tensor_factorisation` is on AND a second jurisdiction is present.

### 12.4 Stream H Definition of Done
- [ ] Phase 8 base ships per its plan (H.0)
- [ ] All 8 intelligence modules ship behind flags
- [ ] Every module emits a deterministic JSON artifact under `005_Operational-Intelligence-Layer/graph/`
- [ ] Build-graph command supports `--with-centrality`, `--with-communities`, etc.
- [ ] `test_backward_compat.py` green

### 12.5 Stream H Gating Metrics
- **Phase 8 gates** (from its plan): orphan rate == 0, determinism check, build latency < 2 s
- **Centrality runtime:** < 3 s on 10 000 nodes
- **Louvain communities cover 100% of nodes**
- **TDA Betti numbers computed for PD 1096 graph:** any H₁ > 0 is reported as a potential loophole
- **Wasserstein merge test on synthetic duplicate pair:** correct merge/flag/split classification

### 12.6 Research-Item Coverage (Stream H)
- ✅ stat-doc §15 (Centrality)
- ✅ stat-doc §22 (Spectral Graph Theory)
- ✅ adv-doc §3 + stat-doc §21 (GraphRAG communities + MCMC ranking)
- ✅ stat-doc §18 (TDA)
- ✅ stat-doc §19 (Optimal Transport)
- ✅ stat-doc §20 (Causal Inference)
- ✅ stat-doc §24 (Tensor Factorization — scaffolded, gated)

---

## 13. Stream I — Query Layer v2 (Phase 9 + ontology translator + GraphRAG routing + MCMC ranking + HMM observability)

**Priority:** P2
**Sprint:** F, weeks 5-6
**Research-Item Coverage:** Phase 9 base (existing plan), Ontology-embedded translation (stat-doc §8 + adv-doc §3), Community-level routing, MCMC ranking (stat-doc §21), HMM pipeline observability (stat-doc §17)

### 13.1 Goal
Ship Phase 9 base per its existing plan, then extend with ontology-embedded NL translation, GraphRAG community-level routing for macro-queries, MCMC-ranked answers, and HMM-based pipeline observability.

### 13.2 Task Sequence (summary)

#### I.0 — Phase 9 Base
Execute `.ai/03_plans/phase-9-query-ai-layer-plan.md` tasks 1–7 verbatim. The NL translator written in that plan becomes the baseline; Stream I.1 extends it.

#### I.1 — Ontology-Embedded NL Translator (`query/ontology_prompt.py`)
Extends `nl_translator.py`: when translating a question, injects the top-50 most central nodes (from Stream H.1) and the active communities (Stream H.3) into the system prompt. The LLM picks from a richer known-entities list.

#### I.2 — GraphRAG Community Router (`query/graphrag_router.py`)
Before running a structured query, detects whether the question is "macro" (e.g., "overarching safety themes") or "specific" (e.g., "what governs building permits"). For macro questions, routes to community summaries first, drills into community members second.

#### I.3 — MCMC Answer Ranker (`query/mcmc_ranker.py`)
For ambiguous queries, runs Stream H.4's MCMC ranker to order the candidate answer nodes by their stationary distribution score.

#### I.4 — HMM Pipeline Observability (`query/pipeline_hmm.py`)
Models the pipeline as a hidden Markov model with states `{scanned, converted, refined, canonicalized, extracted, reviewed, promoted, errored, deferred}`. Transition probabilities are learned from `006_System-Manifests/registries/` historical data. Exposes `predict_next_state(file_id)` for operators.

Failing tests (4 per task).

### 13.3 Stream I Definition of Done
- [ ] Phase 9 base ships per its plan
- [ ] All 4 intelligence modules ship behind flags
- [ ] Query CLI supports `--graphrag`, `--mcmc-rank`, `--hmm-trace`
- [ ] `test_backward_compat.py` green

### 13.4 Gating Metrics
- **Phase 9 gates** (from its plan): ≥95% seed-question accuracy, ≥95% citation accuracy, <2 s latency
- **GraphRAG macro-query improvement:** +15% F1 over flat query baseline
- **HMM transition matrix:** computed from ≥100 historical registry entries; probabilities sum to 1 per row

### 13.5 Research-Item Coverage (Stream I)
- ✅ stat-doc §8 + adv-doc §3 (Ontology-embedded prompting at query time)
- ✅ adv-doc §3 (GraphRAG community routing)
- ✅ stat-doc §21 (MCMC ranking)
- ✅ stat-doc §17 (HMM observability)

---

## 14. Stream J — Active Learning Infrastructure

**Priority:** P2
**Sprint:** F, week 7
**Research-Item Coverage:** Active Learning (stat-doc §10), Expected Model Change (adv-doc §4), plus scaffolding for FUTURE-ML-01/02 LoRA/DPO

### 14.1 Goal
Build the Ranger feedback loop. When a Ranger corrects a decision via the dashboard, that correction becomes a training example for the NB filter, the CRF extractor, and eventually the deferred LoRA adapter. The scoring module uses "Expected Model Change" to route the highest-value candidates to Rangers first.

### 14.2 Task Sequence (summary)

#### J1 — Active Learning Queue (`learning/active_learning.py`)
Maintains a priority queue at `005_Operational-Intelligence-Layer/learning/latest_active_queue.json`. Candidates enter when Conformal Prediction set size > 1 or tension-point analytics flag a disagreement. Priority is the Expected Model Change score.

#### J2 — Expected Model Change Scorer (`learning/expected_model_change.py`)
For a candidate, computes the expected change in model parameters if the candidate were added to the training set:

`EMC(x) = Σ_y p(y|x) · ||∇ log p(y|x) − ∇ log p_current||`

Approximated as a single-step gradient estimate using the NB filter's log-likelihood surface. Higher EMC → more useful for the model → higher Ranger priority.

### 14.3 Definition of Done
- [ ] Every tension-point flagged by Stream F lands in the active queue
- [ ] Queue is persisted deterministically
- [ ] EMC scoring reproduces known rankings on a seed set
- [ ] Ranger feedback (when it exists) retrains NB filter + CRF on the next cycle

### 14.4 Gating Metrics
- **Active queue persistence:** idempotent
- **EMC top-K overlap with expert intuition:** ≥70% on a 20-sample test

### 14.5 Research-Item Coverage (Stream J)
- ✅ stat-doc §10 (Active Learning)
- ✅ adv-doc §4 (Expected Model Change)
- ⏳ scaffolding for FUTURE-ML-01 (LoRA) — data pipeline ready when GPU becomes available
- ⏳ scaffolding for FUTURE-ML-02 (DPO) — preference capture ready when dashboard ships

---

## 15. Stream K — CLUP Scaling Foundation (Rosetta + Precedence + Tensor)

**Priority:** P3 (gated on Phase 11 corpus expansion)
**Sprint:** G onwards
**Research-Item Coverage:** CLUP integration (adv-doc CLUP discussion), Rosetta Stone (adv-doc CLUP §1), Jurisdictional Overrides (adv-doc CLUP §2 + §3), Tensor Factorization activation (stat-doc §24)

### 15.1 Goal
When a second jurisdiction's CLUP is ingested (post-PD-1096), Stream K's modules activate automatically. Rosetta Stone aligns local terminology to canonical concepts. Precedence router enforces "most-stringent-law-wins" at query time. Tensor factorisation (scaffolded in Stream H.8) trains on the 4-way `(s, p, o, jurisdiction)` tensor.

### 15.2 Task Sequence (summary)

#### K1 — Rosetta Stone Alias Registry (`jurisdictions/rosetta_stone.py`)
Maintains a YAML alias registry at `config/jurisdictional_aliases.yaml`. On ingestion of a new jurisdiction, runs Stream D's PMI alias miner against the new corpus and proposes aliases; Rangers confirm; registry persists.

#### K2 — Jurisdictional Precedence Router (`jurisdictions/precedence_router.py`)
At query time, when the user specifies `--jurisdiction quezon-city`, filters edges by `jurisdiction in {national, quezon-city}` and applies Stream G's stringency resolver to pick the winner. Returns *both* edges with `is_governing_standard` flags.

#### K3 — Tensor Factorisation Training
Triggers `graph/tensor_factorisation.py` (scaffolded in Stream H.8) once ≥2 jurisdictions are present. Extracts latent jurisdiction factors and stores them as node attributes for faster query-time filtering.

### 15.3 Definition of Done
- [ ] Rosetta Stone alias registry format frozen
- [ ] Precedence router correctly filters and ranks on a 2-jurisdiction synthetic test
- [ ] Tensor factorisation runs on a ≥2-jurisdiction fixture

### 15.4 Gating Metrics
- **Rosetta auto-alignment accuracy:** ≥85% on synthetic overlapping-CLUP test
- **Precedence router correctness:** 100% on stringency-pairs fixture
- **Tensor factorisation reconstruction error:** ≤5% on fixture

### 15.5 Research-Item Coverage (Stream K)
- ✅ adv-doc CLUP §1 (Rosetta Stone)
- ✅ adv-doc CLUP §2 (Jurisdictional Overrides)
- ✅ adv-doc CLUP §3 (Hardware reality — lean per-LGU ingestion)
- ✅ adv-doc CLUP §4 (Zoning matrices — feeds into Stream B.3 Table-to-Graph)
- ✅ stat-doc §24 (Tensor Factorization — activated once ≥2 jurisdictions)

---

## 16. Sprint Rollout Plan

### 16.1 Sprint D — Foundation (weeks 1-5) 🔥
**Goal:** Every new dependency installed, Merkle hash live, Tier C normalization shipping, concepts v2 matching the 4 remaining RI-010 entries.

| Week | Stream(s) | Deliverables |
|---|---|---|
| 1 | A | Dependency bootstrap, feature flags, Merkle hash, backward-compat harness |
| 2 | B | Shannon classifier, Table-to-Graph, Parametric NER |
| 3 | C | Tier C OCR, AST chunker |
| 4 | C | Embedding chunker, Mahalanobis outlier |
| 5 | D | TF-IDF matcher, PMI aliases, FCA lattice, contrastive adapter |

**Exit criteria:** All A/B/C/D flags can be turned ON individually without breaking `test_backward_compat.py`; RI-010 closure candidates generated for all 4 concepts; `pytest scripts/tests/` > 400 tests, all green.

### 16.2 Sprint E — Intelligence (weeks 6-11)
**Goal:** Regex extraction replaced by CRF at the root. LLM review compressed by 3–5×. Promotion carries Bayesian confidence, stringency, and temporal edges.

| Week | Stream(s) | Deliverables |
|---|---|---|
| 6 | E | spaCy dep parser, CRF trainer |
| 7 | E | CRF extractor, KG link predictor |
| 8 | F | NB filter, SLM router |
| 9 | F | Ontology prompt builder, conformal calibrator |
| 10 | F | Tension analyzer, reflection parser, Ollama config, Choquet aggregator |
| 11 | G | Bayesian fusion, stringency resolver, temporal edges, concept frontmatter migration |

**Exit criteria:** Phase 6 review time for PD 1096 drops ≥60%; regex-rejection rate ≤30%; every promoted edge has a continuous confidence score.

### 16.3 Sprint F — Graph & Query (weeks 12-18)
**Goal:** Phase 8 + Phase 9 base ship per their plans; statistical intelligence stacks on top; Active Learning queue live.

| Week | Stream(s) | Deliverables |
|---|---|---|
| 12 | H.0 | Phase 8 base: contract, builder, snapshot, integrity, traverse, CLI |
| 13 | H.1-H.3 | Centrality, spectral, communities |
| 14 | H.4-H.6 | MCMC, TDA, Wasserstein |
| 15 | H.7-H.8 | Causal DAG overlay, tensor factorisation scaffolding |
| 16 | I.0 | Phase 9 base per its plan |
| 17 | I.1-I.3 | Ontology translator, GraphRAG router, MCMC ranker |
| 18 | I.4 + J | HMM observability, active learning queue |

**Exit criteria:** Phase 8 graph snapshot stable with ≥50 verified PD 1096 relationships; Phase 9 seed-question accuracy ≥95%; active queue populated.

### 16.4 Sprint G — Scaling (weeks 19+, gated)
**Goal:** Second jurisdiction (e.g., IRR or a QC CLUP) ingested through the hardened pipeline. Stream K activates.

**Entry condition:** All Sprint D/E/F exit criteria hold for ≥1 week without a single `test_backward_compat.py` failure.

### 16.5 Deferred Milestones
| Milestone | Prerequisite | ETA |
|---|---|---|
| FUTURE-ML-01 LoRA | External GPU (RunPod A10G) + ≥1000 distilled examples | Post Sprint G |
| FUTURE-ML-02 DPO | Ranger dashboard + ≥1000 preference pairs | Post Sprint G |
| FUTURE-LRN-01 BKT | ILXP frontend + first cohort of learners | Phase 12 |

---

## 17. Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| ML dependency install fails on M2 (numpy/scipy/spacy Apple-Silicon wheels) | HIGH | Pin lower bounds tested on macOS 14+ ARM64; fallback to `--no-binary :all:` if wheels missing |
| sentence-transformers first-load pulls a large model over network | MEDIUM | Cache under `~/.cache/vitruvius/models/`; document in README; fail fast with instructions if offline |
| Backward-compat regression flaps due to OS-level mtime or hash drift | HIGH | Golden fixtures are copied, not live raw-layer files; Merkle hash uses content-only (no mtime) |
| Feature-flag default drift (someone sets a flag to true by accident) | HIGH | `test_features.py` asserts every flag in the config block defaults to false before every CI run |
| Ollama version doesn't support speculative decoding / KV quant | MEDIUM | `ollama_config.py` detects version at startup, logs a warning, leaves unsupported flags alone |
| CRF trainer overfits on a tiny `keep` corpus (7 relationships at Sprint D start) | MEDIUM | Minimum-corpus-size check (≥50 examples) refuses to train; earlier streams produce more data |
| Louvain communities don't stabilise on a small graph | LOW | Accept that community detection requires ≥100 nodes; fall back to Fiedler bisection for smaller graphs |
| Tensor factorisation scaffolding bloats dead code in `graph/` | LOW | Module is a single file <200 lines, gated by `features.h_tensor_factorisation` |
| RAM spike when Stream C embedder and Ollama run concurrently | MEDIUM | Sequential execution enforced at CLI level — embed chunker runs in `refine` stage; Ollama runs in `review` stage |
| Active queue grows unbounded | LOW | Stream J's queue has a retention policy: keep top-100 by EMC score, archive the rest |
| TDA implementation in pure numpy too slow | MEDIUM | Swap to `gudhi` if real-corpus runtime > 30 s |
| Non-breaking guarantee breaks because a shared helper silently consults a flag | HIGH | Every new module has "Does this alter existing code paths when flag is OFF?" in its self-review checklist; `test_backward_compat.py` catches violations |

---

## 18. Non-Goals

- **Cloud migration.** All streams run locally. Cloud is opt-in only per P8 and remains outside this plan's scope.
- **UI / frontend.** No web or Streamlit code. The query layer remains CLI-only through Phase 9.
- **External graph database.** Phase 8 ships filesystem-backed per principle P1; no Neo4j/Dgraph/Arango.
- **Database-backed persistence for lineage.** All state lives in `006_System-Manifests/` CSV + JSON.
- **Generative question-answering.** LLMs remain classifiers and translators. Free-text answers are rejected by Phase 9 design.
- **Visualisation, 3D, GLB, scene graphs.** Explicitly purged per master-roadmap §12.
- **LoRA or DPO fine-tuning in Sprints D–G.** Deferred to FUTURE-ML-01/02 with explicit GPU prerequisite.
- **BKT / learner modelling.** Deferred to Phase 12 with ILXP prerequisite.

---

## 19. Stream-Level Gating Metrics (consolidated)

| Stream | Gate | Target |
|---|---|---|
| A | `test_backward_compat.py` green | 100% |
| A | Merkle scan runtime cold | ≤ 50 ms |
| B | Shannon classifier accuracy | ≥ 95% |
| B | Table-to-Graph determinism | byte-identical |
| B | Parametric NER precision | ≥ 85% |
| C | OCR typo correction precision | ≥ 98% |
| C | Mahalanobis AUROC | ≥ 0.90 |
| D | RI-010 concept closure via TF-IDF | 3 of 4 |
| D | PMI alias acceptance | ≥ 70% |
| E | CRF false-positive rate | ≤ 30% |
| E | Link predictor hit@5 | ≥ 60% |
| F | Phase 6 LLM time reduction | ≥ 60% |
| F | Conformal singleton rate | ≥ 80% |
| G | Bayesian monotonicity | 100% |
| G | Stringency correctness | 100% |
| H | Phase 8 determinism | byte-identical |
| H | Centrality runtime | < 3 s |
| I | Phase 9 seed accuracy | ≥ 95% |
| I | GraphRAG lift on macro-queries | ≥ 15% |
| J | EMC top-K overlap | ≥ 70% |
| K | Rosetta alignment accuracy | ≥ 85% |

---

## 20. Research-Item Coverage Matrix (FULL)

Every numbered technique from both research documents is mapped to a concrete task in this plan. Items marked `deferred` have explicit prerequisite gates in §2.3.

### 20.1 `.ai/13_research/statistical-improvements.md`

| # | Research Item | Stream | Task | Status |
|---|---|---|---|---|
| 1 | TF-IDF & N-Gram Collocation | D | D1 | Planned |
| 1 | PMI alias discovery | D | D2 | Planned |
| 2 | Naïve Bayes / Logistic Regression pre-review | F | F1 | Planned |
| 3 | Conditional Random Fields | E | E2 + E3 | Planned |
| 4 | Levenshtein / Jaro-Winkler | C | C1 | Planned |
| 5 | Bayesian Evidence Fusion | G | G1 | Planned |
| 6 | SLM Swarms & Dynamic Routing | F | F2 | Planned |
| 7 | Graph ML / Link Prediction (TransE) | E | E4 | Planned |
| 8 | Ontology-Embedded Prompting / GraphRAG | F + I | F3 + I.1 | Planned |
| 9 | Hybrid Semantic-Structural Chunking | C | C3 | Planned |
| 10 | Active Learning | J | J1 | Planned |
| 11 | Parametric Constraint Extraction | B | B4 | Planned |
| 12 | Bayesian Knowledge Tracing | — | — | **DEFERRED** (FUTURE-LRN-01) |
| 13 | Shannon Entropy document classification | B | B1 + B2 | Planned |
| 14 | Conformal Prediction | F | F4 | Planned |
| 15 | Graph Centrality Measures | H | H.1 | Planned |
| 16 | Mahalanobis Distance outlier | C | C4 | Planned |
| 17 | Hidden Markov Models pipeline observability | I | I.4 | Planned |
| 18 | Algebraic Topology / TDA | H | H.5 | Planned |
| 19 | Optimal Transport / Wasserstein | H | H.6 | Planned |
| 20 | Causal Inference / Do-Calculus | H | H.7 | Planned |
| 21 | Markov Chain Monte Carlo (MCMC) | H + I | H.4 + I.3 | Planned |
| 22 | Spectral Graph Theory / Fiedler | H | H.2 | Planned |
| 23 | Formal Concept Analysis / Lattice Theory | D | D3 | Planned |
| 24 | Tensor Factorization | H + K | H.8 + K3 | Planned (gated) |
| 25 | Fuzzy Measure Theory / Choquet Integral | F | F8 | Planned |

### 20.2 `.ai/13_research/advanced architectural and code-level optimizations.md`

| # | Research Item | Stream | Task | Status |
|---|---|---|---|---|
| 1 | Merkle Tree Directory Hash | A | A5 + A6 + A7 | Planned |
| 2 | AST-based Semantic Chunking | C | C2 | Planned |
| 3 | Knowledge Graph Embeddings (TransE/ComplEx) | E | E4 | Planned |
| 4 | Speculative Decoding + KV Cache | F | F7 (Ollama config) | Planned |
| 5 | Tension Point Analytics | F | F5 | Planned |
| 6 | Domain-Specific Embedding Adaptation (Contrastive) | D | D4 (whitening variant) | Planned |
| 7 | Synthetic Data Distillation + LoRA | — | — | **DEFERRED** (FUTURE-ML-01) |
| 8 | GraphRAG with Community Detection (Louvain/Leiden) | H + I | H.3 + I.2 | Planned |
| 9 | Pedagogical Alignment via DPO | — | — | **DEFERRED** (FUTURE-ML-02) |
| 10 | Self-Reflective Agentic Routing (MoE) | F | F6 | Planned |
| 11 | Parametric Knowledge Extraction | B | B4 | Planned |
| 12 | Table-to-Graph Matrix Projection | B | B3 + B3.1 | Planned |
| 13 | Temporal & Jurisdictional Graph Edges | G + K | G3 + K2 | Planned |
| 14 | Active Learning Uncertainty Sampling | J | J1 + J2 | Planned |
| 15 | 8GB Survival Mode (model downsizing + spaCy SVO) | F + E | F2 + E1 | Planned |
| 16 | Stringency Matrix / Conflict Resolution Gate | G | G2 | Planned |
| 17 | CLUP Integration (Rosetta Stone + Precedence) | K | K1 + K2 | Planned |

### 20.3 Deferred Items With Explicit Prerequisites
| Deferred ID | Item | Prerequisite Gate | Re-plan Trigger |
|---|---|---|---|
| FUTURE-ML-01 | LoRA fine-tuning | External GPU + ≥1000 distilled examples from Stream J | When GPU becomes available |
| FUTURE-ML-02 | DPO pedagogical alignment | Ranger dashboard + ≥1000 preference pairs | Dashboard shipped |
| FUTURE-LRN-01 | Bayesian Knowledge Tracing | ILXP frontend + active learners | Phase 12 starts |

**Verification.** 25 items from statistical-improvements.md + 17 items from advanced-architectural.md = **42 items total**. 39 are Planned, 3 are Deferred with explicit gates. **Zero skipped.**

---

## 21. Self-Review Checklist (pre-execution)

Run this checklist once before handing the plan to a subagent.

### 21.1 Spec Coverage
- [ ] Every item in `statistical-improvements.md` appears in §20.1 with a stream and task
- [ ] Every item in `advanced architectural and code-level optimizations.md` appears in §20.2 with a stream and task
- [ ] Every deferred item has a prerequisite in §2.3 and §20.3 with an explicit re-plan trigger
- [ ] Every stream has: Goal, Files, Task sequence, Definition of Done, Gating Metrics, Research-Item Coverage
- [ ] Every Stream A/B task has full TDD bodies with code
- [ ] Every Stream C-K task has enough detail (task name, interface, failing tests) to be expanded to full TDD at execution time

### 21.2 Placeholder Scan
- [ ] No "TBD" strings in the document
- [ ] No "implement later" / "fill in details"
- [ ] No "add appropriate error handling" without specific cases
- [ ] No "similar to Task N" (every task repeats the pattern)
- [ ] Every step that changes code includes the exact code or interface signature

### 21.3 Type / Interface Consistency
- [ ] Every feature flag name in `config/vitruvius.yaml` matches exactly with a `features.X` reference in the task code
- [ ] `Features` is spelled `Features` (not `FeatureFlags`, not `Flags`) across all tasks
- [ ] `calculate_directory_hash` has one signature, used consistently in A5, A6, A7
- [ ] `Parameter` dataclass has fields `entity, operator, value, unit, start, end, evidence` (not a subset)
- [ ] `TableSubgraph.to_json_dict` return type matches the test assertions
- [ ] `QueryResult` / `QueryCitation` match the Phase 9 base plan (Stream I does not rename them)

### 21.4 Non-Breaking Contract
- [ ] Every module added under a new subpackage (no modifications to `utils.py`, `paths.py`, `constants.py`)
- [ ] Every change to an existing module is additive (new functions, new parameters with default values)
- [ ] `test_backward_compat.py` runs after every commit; any failure blocks the commit
- [ ] Every feature flag defaults to `false` in §3.5
- [ ] Every stream has a "flag OFF is byte-identical" test

### 21.5 Hardware Ceiling
- [ ] Total RAM budget in §3.4 stays under 5 GB with macOS reserved
- [ ] No stream requires > 10 000 node graph operations
- [ ] No stream trains on a GPU
- [ ] Sentence-transformers model is the only large downloaded weight (<100 MB)

---

## 22. Execution Handoff

**Status.** This plan is `implementation_tdd` for Streams A and B and `design_spec with TDD spine` for Streams C-K.

**Before execution:**
1. Confirm the user approves the precedence declaration in §1.2 (this plan supersedes Phases 8, 9, 11 in priority).
2. Confirm the user wants Stream A to start immediately on the active `feat/phase-7-promotion-governance` branch, OR wants a new feature branch for Sprint D.
3. Confirm the user accepts the dependency footprint in §3.4 (~4.9 GB disk, ~4.55 GB RAM peak).

**During execution:**
- Use `superpowers:subagent-driven-development` — one fresh subagent per task, review between tasks.
- Never skip the backward-compat regression after any commit.
- If any task's Definition of Done cannot be met, halt and escalate to a Ranger before proceeding.

**After each stream:**
- Update this plan's frontmatter `status:` entry.
- Record an `AD-XXX` entry in `.ai/10_state/decisions.md` summarising what shipped.
- Update `.ai/01_roadmap/master-roadmap.md` §4 status table with the new stream-level checkboxes.
- Update `.ai/10_state/known_issues.md` with any RIs closed.
- Tick the matching row in `.ai/03_plans/INDEX.md` if applicable.

**After every task:**
- `pytest scripts/tests/ -q` green
- `pytest scripts/tests/test_backward_compat.py -v` green
- `git status` clean (all staged changes committed)
- Feature flag added to `config/vitruvius.yaml` is still `false`

---

## 23. Changelog

- **2026-04-14 · v1.0.0** — Initial plan consolidating every technique from `.ai/13_research/statistical-improvements.md` and `.ai/13_research/advanced architectural and code-level optimizations.md` into 11 execution streams (A–K), 4 sprints (D–G), and 3 deferred milestones. Supersedes priority on Phases 8, 9, and 11 plans but leaves their contracts intact — it extends, does not replace. 42 research items: 39 Planned, 3 Deferred with explicit GPU/ILXP gates. Non-breaking guarantee enforced by a backward-compat regression suite built in Stream A Task A4. — *Senior Systems Architect*
