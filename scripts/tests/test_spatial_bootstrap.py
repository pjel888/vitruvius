"""Stream L.1 — bootstrap sanity checks.

These tests lock in the additive contract changes so a later task cannot
regress the Phase 8 graph schema. The graph walker is NOT run here — we
only verify the contract constants themselves.
"""
from __future__ import annotations

from pathlib import Path


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
        ALLOWED_EDGE_STATUSES,
        ALLOWED_ID_PREFIXES,
        ALLOWED_NODE_TYPES,
    )
    assert "spatial_instance" in ALLOWED_NODE_TYPES
    assert "instance-" in ALLOWED_ID_PREFIXES
    assert "spatial-" in ALLOWED_ID_PREFIXES
    assert "spatially_verified" in ALLOWED_EDGE_STATUSES
    for original in ("source", "concept", "attribute"):
        assert original in ALLOWED_NODE_TYPES
    for original in (
        "law-",
        "irr-",
        "concept-",
        "rel-",
        "source-",
        "handout-",
        "reviewer-",
        "law-section-",
    ):
        assert original in ALLOWED_ID_PREFIXES
    for original in ("verified", "unverified"):
        assert original in ALLOWED_EDGE_STATUSES
