"""Sprint CLEANUP-1 Stream C1.2 — slug collision resolver test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.collision_resolver import (
    SlugAliasRegistry,
    resolve_canonical_id,
)


def test_no_collision_returns_original(tmp_path: Path) -> None:
    registry_file = tmp_path / "registry.yaml"
    registry_file.write_text("collisions: {}\n")
    registry = SlugAliasRegistry.load(registry_file)

    resolved = resolve_canonical_id(
        prefix="law",
        slug="pd1096",
        source_path="001_Raw-Source-Layer/001-Laws/PD-1096.pdf",
        existing_ids=set(),
        registry=registry,
    )
    assert resolved == "law-pd1096"
    assert registry.get("001_Raw-Source-Layer/001-Laws/PD-1096.pdf") is None


def test_first_collision_appends_short_hash(tmp_path: Path) -> None:
    registry_file = tmp_path / "registry.yaml"
    registry_file.write_text("collisions: {}\n")
    registry = SlugAliasRegistry.load(registry_file)

    # The first source path already owns "law-pd1096".
    existing = {"law-pd1096"}
    resolved = resolve_canonical_id(
        prefix="law",
        slug="pd1096",
        source_path="001_Raw-Source-Layer/001-Laws/alt-PD-1096.pdf",
        existing_ids=existing,
        registry=registry,
    )
    # Collision → append short hash (first 6 chars of md5 of source_path)
    assert resolved.startswith("law-pd1096-")
    assert len(resolved) == len("law-pd1096-") + 6
    # Registry recorded the mapping
    assert registry.get("001_Raw-Source-Layer/001-Laws/alt-PD-1096.pdf") == resolved


def test_persistent_collision_returns_previously_assigned_id(tmp_path: Path) -> None:
    """Re-resolving the same source_path returns the same disambiguated id
    (idempotency — Principle P3 + P6)."""
    registry_file = tmp_path / "registry.yaml"
    registry_file.write_text(
        'collisions:\n'
        '  "001_Raw-Source-Layer/001-Laws/alt-PD-1096.pdf": "law-pd1096-a1b2c3"\n'
    )
    registry = SlugAliasRegistry.load(registry_file)

    resolved = resolve_canonical_id(
        prefix="law",
        slug="pd1096",
        source_path="001_Raw-Source-Layer/001-Laws/alt-PD-1096.pdf",
        existing_ids={"law-pd1096"},
        registry=registry,
    )
    assert resolved == "law-pd1096-a1b2c3"
