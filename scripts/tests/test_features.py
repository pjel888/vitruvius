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
}


def test_repo_config_contains_every_expected_flag() -> None:
    features = load_features(REPO_CONFIG)
    missing = EXPECTED_FLAGS - set(features.flags.keys())
    assert not missing, f"Missing flags in config/vitruvius.yaml: {sorted(missing)}"


def test_repo_config_every_flag_is_false() -> None:
    """The non-breaking contract (plan §1.3) requires every flag default to False.

    If this test fails, someone flipped a flag in config/vitruvius.yaml and
    must (a) revert the flip OR (b) update the plan's non-breaking contract
    and the backward-compat regression suite accordingly.
    """
    features = load_features(REPO_CONFIG)
    enabled = [name for name in EXPECTED_FLAGS if features.is_enabled(name)]
    assert not enabled, (
        f"These Stream A-K flags are enabled in config/vitruvius.yaml "
        f"and violate the non-breaking contract: {sorted(enabled)}"
    )
