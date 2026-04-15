"""Feature-flag loader — reads config/vitruvius.yaml → features: block.

Every Stream A-K module gates its behaviour on a feature flag. Flags live
under `features:` in config/vitruvius.yaml and default to False. The loader
fails safe: unknown flags, missing config, malformed YAML all return False.
The returned Features object is frozen to prevent accidental mutation.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from vitruvius.features import Features, load_features


def test_load_features_returns_all_defaults_false(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text("features: {}\n")
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is False
    assert features.is_enabled("h_causal_dag") is False


def test_load_features_reads_explicit_true(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text(
        textwrap.dedent(
            """
            features:
              a_merkle_hash: true
              b_shannon_classifier: false
            """
        ).lstrip()
    )
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is True
    assert features.is_enabled("b_shannon_classifier") is False


def test_unknown_flag_is_false_and_does_not_raise(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text("features: {}\n")
    features = load_features(cfg)
    assert features.is_enabled("nonexistent_flag") is False


def test_missing_config_file_is_safe(tmp_path: Path) -> None:
    cfg = tmp_path / "does_not_exist.yaml"
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is False


def test_malformed_yaml_is_safe(tmp_path: Path) -> None:
    cfg = tmp_path / "broken.yaml"
    cfg.write_text("features:\n  - not a dict")
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is False


def test_config_without_features_block_is_safe(tmp_path: Path) -> None:
    cfg = tmp_path / "no_features.yaml"
    cfg.write_text("project_name: Vitruvius\n")
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is False


def test_coerces_truthy_values(tmp_path: Path) -> None:
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text(
        textwrap.dedent(
            """
            features:
              a_merkle_hash: 1
              b_shannon_classifier: "true"
              c_tier_c_ocr_fix: "no"
            """
        ).lstrip()
    )
    features = load_features(cfg)
    assert features.is_enabled("a_merkle_hash") is True
    assert features.is_enabled("b_shannon_classifier") is True
    # "no" is a non-empty string → truthy under bool() coercion; this is
    # documented behaviour. Use real YAML booleans (true/false) for safety.


def test_direct_constructor_is_frozen() -> None:
    features = Features(flags={"a_merkle_hash": True})
    with pytest.raises(AttributeError):
        features.flags = {}  # type: ignore[misc]


def test_is_enabled_never_returns_non_bool() -> None:
    features = Features(flags={"a_merkle_hash": True, "x": "yes", "y": 0})
    for name in ["a_merkle_hash", "x", "y", "missing"]:
        result = features.is_enabled(name)
        assert isinstance(result, bool)


# ------- Integration: the real repo config ------- #

REPO_ROOT = Path(__file__).resolve().parents[2]
REPO_CONFIG = REPO_ROOT / "config" / "vitruvius.yaml"

# Authoritative flag list — keep in sync with plan §3.5.
EXPECTED_FLAGS = {
    "a_merkle_hash",
    "b_shannon_classifier", "b_table_graph", "b_parametric_ner",
    "c_tier_c_ocr_fix", "c_ast_chunking", "c_hybrid_chunking", "c_mahalanobis_outlier",
    "d_tfidf_concepts", "d_pmi_aliases", "d_fca_lattice", "d_contrastive_embedder",
    "e_spacy_svo", "e_crf_extractor", "e_kg_link_prediction",
    "f_naive_bayes_filter", "f_slm_swarm", "f_ontology_embedded_prompt",
    "f_conformal_prediction", "f_tension_point", "f_self_reflection",
    "f_ollama_speculative", "f_ollama_kv_cache", "f_choquet_aggregation",
    "g_bayesian_fusion", "g_stringency_matrix", "g_temporal_edges",
    "h_centrality", "h_spectral", "h_community", "h_mcmc", "h_tda",
    "h_wasserstein", "h_causal_dag", "h_tensor_factorisation",
    "i_ontology_nl_translator", "i_graphrag_routing", "i_mcmc_ranking",
    "i_hmm_observability",
    "j_active_learning", "j_expected_model_change",
    "k_rosetta_stone", "k_jurisdictional_overrides",
    "l_spatial_ingestion", "l_z3_constraint_solver",
    "m_ifc_ontology_mapping", "m_owl_turtle_export",
    "n_spatial_daemon_enabled",
    "o_watched_sources_registry", "o_mahalanobis_drift_detection",
    "o_duplicate_detector",
    # Stream Y — Per-Layer Embeddings & Agentic Reasoning (Sprint R)
    "y_contextual_priming", "y_domain_routing_moe", "y_thinking_mode_cot",
    "y_stateful_registry", "y_vision_ocr",
    # Sprint PHYS — Statistical Mechanics & Graph Physics (phase-16)
    "phys_pagerank", "phys_boltzmann_gate", "phys_motif_matcher",
    "phys_shannon_sampling", "phys_eigenvector_cascade",
    # Sprint HP — High-Performance Optimizations (phase-13)
    "hp_merkle_fs", "hp_event_sourced_graph", "hp_graphsage",
    "hp_wasm_kernels",
    # Sprint PQ-1 — Product Quantization for GraphSAGE embeddings
    "hp_graphsage_pq",
    # Sprint HP.3-R — RocksDB KV backend migration
    "hp_rocksdb_event_store", "hp_rocksdb_verdict_cache",
    # Sprint 1B-M1 — Phase 1B Modernization Tranche 1
    "p1b_docling_parser", "p1b_libreoffice_preprocessor",
    # Sprint 1B-M2 — Phase 1B Modernization Tranche 2 (scoped)
    "p1b_ocr_preprocessor", "p1b_process_pool_orchestration",
    # Sprint 1B-M3 — Phase 1B Modernization Tranche 3 (Rust PDF)
    "p1b_rust_pdf_parser",
    # Sprint GEOM — Geometric Constraint Engine (phase-15)
    "geom_csp_compiler", "geom_envelope_2d", "geom_envelope_3d",
    "geom_iou_audit", "geom_pareto_optimizer",
    # Sprint WIKI — Autonomous Knowledge Synthesis (phase-14)
    "wiki_docling_parser", "wiki_kuzu_store", "wiki_delta_tracking",
    "wiki_synthesis_loop", "wiki_ego_linter",
    # Sprint Z — Compound AI Evolution (phase-12)
    "z_dspy_compiler",
    "z_adversarial_swarm",
    "z_differential_dataflow",
    "z_neuro_symbolic",
    # Sprint GT — Geo-Topological Rust engine (phase-8b)
    "gt_engine_rs",
    # Sprint GT Stream GT.5 — Hardware Hardening (mmap + Bloom + MC dropout)
    "gt_hardware_hardening",
    # Sprint GT Stream GT.3 — Temporal Knowledge Graph (TemporalEdge +
    # versioned query + Parquet archiver)
    "gt_temporal_graph",
    # Sprint GT Stream GT.4 — Spatial GraphRAG bridge (octree proximity
    # jump + exponential distance decay + physically_adjacent_to edges)
    "gt_proximity_jump",
    "gt_spatial_edges",
    # Sprint RUST-MIG-1 — Python→Rust polyglot kernels (AD-036, AD-038).
    # Flag gates N4 Mahalanobis scoring kernel. N1 sliced Wasserstein
    # deferred per AD-038a (POT backend is already native). Both flags
    # flipped to true at AD-038 closure — S1+S2 under
    # rust_mig_spatial_kernels (both cleared the 2× gate at the kernel
    # level), N4 under rust_mig_stats_kernels (2.73× end-to-end).
    "rust_mig_spatial_kernels", "rust_mig_stats_kernels",
    # Sprint LSH-1 — MinHash LSH fuzzy near-duplicate layer on top of
    # the existing O(n log n) dict-grouped exact-endpoint dedup (see
    # AD-037 for the premise correction + language choice). Default
    # false per plan §1.3.
    "w_lsh_dedup",
    # Sprint CLEANUP-1 — 4-stream backlog cleanup (AD-043)
    "p1c_contract_validator", "p1c_slug_collision_policy", "p1c_table_isolation",
    "p3_density_extractor", "p3_bidirectional_refs",
    "p1b_page_isolation", "p1b_hallucination_trap",
    "p5e_llm_extraction",
}


def test_repo_config_contains_every_expected_flag() -> None:
    features = load_features(REPO_CONFIG)
    missing = EXPECTED_FLAGS - set(features.flags.keys())
    assert not missing, f"Missing flags in config/vitruvius.yaml: {sorted(missing)}"


def test_repo_config_every_flag_is_false() -> None:
    """The non-breaking contract (plan §1.3) requires every flag default to False,
    with AD-029 and AD-038 as documented exceptions.

    If this test fails (outside the AD-029 + AD-038 allowlists), someone
    flipped a flag in config/vitruvius.yaml and must (a) revert the flip
    OR (b) update the plan's non-breaking contract and the backward-compat
    regression suite accordingly, OR (c) add a new AD-### entry explaining
    the deliberate flip and extend this allowlist.

    AD-029 exceptions: hp_rocksdb_event_store + hp_rocksdb_verdict_cache were
    flipped to true on 2026-04-15 after the Sprint HP.3-R bench measured
    RocksDB at 18.7x (event store) and 24.3x (verdict cache) faster than
    SQLite at n=10000. See .ai/10_state/decisions.md AD-029.

    AD-038 exceptions: rust_mig_spatial_kernels + rust_mig_stats_kernels
    were flipped to true on 2026-04-15 after the Sprint RUST-MIG-1 Task 8
    bench cleared the ≥2× speedup gate on every shipped kernel (S1 200× raw,
    S2 12.18× raw / 2.84× end-to-end, N4 2.73× end-to-end). N1 sliced
    Wasserstein was deferred per AD-038a (POT backend already native).
    See .ai/10_state/decisions.md AD-038.
    """
    ad_029_exceptions = {"hp_rocksdb_event_store", "hp_rocksdb_verdict_cache"}
    ad_038_exceptions = {"rust_mig_spatial_kernels", "rust_mig_stats_kernels"}
    allowlist = ad_029_exceptions | ad_038_exceptions
    features = load_features(REPO_CONFIG)
    enabled = [
        name for name in EXPECTED_FLAGS
        if name not in allowlist and features.is_enabled(name)
    ]
    assert enabled == [], (
        f"flags enabled in config/vitruvius.yaml outside the AD-029+AD-038 allowlist: {enabled}. "
        "See .ai/09_archive/plans/statistical-architectural-upgrade-plan.md §1.3 and "
        ".ai/10_state/decisions.md AD-029 + AD-038."
    )


# ---------------------------------------------------------------------------
# Stream Y0.2 — per-layer embeddings feature flags
# ---------------------------------------------------------------------------
def test_y_flags_default_false() -> None:
    """Every Sprint R Y flag must default to False on a fresh load
    of the repo config, preserving the non-breaking contract."""
    features = load_features(REPO_CONFIG)
    assert features.is_enabled("y_contextual_priming") is False
    assert features.is_enabled("y_domain_routing_moe") is False
    assert features.is_enabled("y_thinking_mode_cot") is False
    assert features.is_enabled("y_stateful_registry") is False
    assert features.is_enabled("y_vision_ocr") is False


def test_y_flags_load_from_config(tmp_path: Path) -> None:
    """A YAML override flips a single Y flag but unspecified ones default
    to False."""
    cfg = tmp_path / "vitruvius.yaml"
    cfg.write_text(
        "features:\n"
        "  y_contextual_priming: true\n",
        encoding="utf-8",
    )
    features = load_features(cfg)
    assert features.is_enabled("y_contextual_priming") is True
    assert features.is_enabled("y_domain_routing_moe") is False


def test_hp_rocksdb_event_store_defaults_true() -> None:
    """Sprint HP.3-R AD-029 — the backend-switch flag defaults to true
    after the Task 8 bench measured RocksDB at 18.7x faster than SQLite
    (ratio 0.053 well inside the rocksdb_wins bucket of <= 0.5).

    The SQLite code path remains available by setting the flag to false
    in config/vitruvius.yaml. See .ai/10_state/decisions.md AD-029.
    """
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("hp_rocksdb_event_store") is True


def test_hp_rocksdb_verdict_cache_defaults_true() -> None:
    """Sprint HP.3-R AD-029 — the verdict-cache backend-switch flag
    defaults to true after the Task 8 bench measured RocksDB at 24.3x
    faster than SQLite (ratio 0.041 well inside the rocksdb_wins bucket).

    The SQLite code path remains available by setting the flag to false
    in config/vitruvius.yaml. See .ai/10_state/decisions.md AD-029.
    """
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("hp_rocksdb_verdict_cache") is True


def test_hp_graphsage_pq_defaults_false() -> None:
    """Sprint PQ-1 AD-041 — the PQ embedding compression deployment
    marker defaults to false. Bench at .ai/10_state/bench_pq_
    reconstruction_2026-04-15.json shows 32x compression with cosine
    delta 0.00017 (target <= 0.02), but the persistence layer that
    would consume the codes does not exist yet, so the flag stays
    false until that follow-up plan ships.
    """
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("hp_graphsage_pq") is False


def test_rust_mig_spatial_kernels_defaults_true() -> None:
    """Sprint RUST-MIG-1 AD-038 — the spatial kernels Rust fast-path
    flag defaults to true after the Task 8 bench cleared the ≥2× gate
    for both S1 build_spatial_adjacency_edges (200× raw kernel / 57%
    subprocess wall reduction at n=2000) and S2 weight_by_distance
    (12.18× raw kernel / 2.84× end-to-end at n=10000).

    The Python code path remains available by setting the flag to
    false in config/vitruvius.yaml. See .ai/10_state/decisions.md
    AD-038.
    """
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("rust_mig_spatial_kernels") is True


def test_rust_mig_stats_kernels_defaults_true() -> None:
    """Sprint RUST-MIG-1 AD-038 — the stats kernels Rust fast-path
    flag defaults to true after the Task 8 bench cleared the ≥2× gate
    for N4 mahalanobis_distance (2.73× end-to-end at n=1000 queries,
    64-dim). The original N1+N4 flag scope narrowed to N4-only after
    AD-038a deferred the N1 sliced Wasserstein port (POT backend is
    already native C++ LP).

    The Python code path remains available by setting the flag to
    false in config/vitruvius.yaml. See .ai/10_state/decisions.md
    AD-038 and AD-038a.
    """
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("rust_mig_stats_kernels") is True


def test_w_lsh_dedup_defaults_false() -> None:
    """Sprint LSH-1 AD-037 — the MinHash LSH fuzzy near-duplicate
    layer defaults to false. Per the plan §1.3 non-breaking contract
    the flag stays false until a full PD 1096 operator run confirms
    the fuzzy-match hit rate + zero-false-positive guard on live
    data. Test suite at scripts/tests/test_lsh_dedup.py locks in
    the byte-equivalence guarantee with the flag off and the fuzzy
    collapse behaviour with the flag on (via direct function
    invocation, bypassing config).

    See .ai/10_state/decisions.md AD-037 (premise correction) and
    AD-042 (sprint closure).
    """
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("w_lsh_dedup") is False


def test_p1b_docling_parser_defaults_false() -> None:
    """Sprint 1B-M1 — DoclingParser routing defaults false so the
    pre-tranche ingestion path is byte-identical until pipeline_cli.py
    integration lands in a follow-up."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_docling_parser") is False


def test_p1b_libreoffice_preprocessor_defaults_false() -> None:
    """Sprint 1B-M1 — LibreOfficePreprocessor routing defaults false."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_libreoffice_preprocessor") is False


def test_p1b_ocr_preprocessor_defaults_false() -> None:
    """Sprint 1B-M2 — OCRPreprocessor routing defaults false until
    pipeline_cli.py integration lands in a follow-up plan."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_ocr_preprocessor") is False


def test_p1b_process_pool_orchestration_defaults_false() -> None:
    """Sprint 1B-M2 — process_batch parallelism marker defaults false."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_process_pool_orchestration") is False


def test_p1b_rust_pdf_parser_defaults_false() -> None:
    """Sprint 1B-M3 AD-034 — RustPdfParser deployment-readiness marker
    defaults false until real-corpus validation through pipeline_cli.py
    integration confirms no regression vs docling. AD-033 bench +
    AD-034 quality spot check (similarity 0.9925) cleared the code,
    but live-pipeline validation on PD 1096 ingestion is still the
    gating condition for flipping to true."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_rust_pdf_parser") is False
