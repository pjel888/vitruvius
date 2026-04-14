"""Stream M.1 — IFC concept registry loader."""
from __future__ import annotations

from pathlib import Path
from types import MappingProxyType

import pytest

from vitruvius.ontology.ifc_registry import (
    DEFAULT_IFC_MAPPING_PATH,
    IfcMapping,
    load_ifc_mapping,
    lookup_ifc_class,
)


def _write_yaml(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "ifc_mapping.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_load_happy_path(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-building-permit\n"
        "  ifc_class: IfcBuildingElementProxy\n"
        "  psets: [Pset_ElementCommon]\n"
        '  notes: "Permit is a process entity."\n',
    )
    mapping = load_ifc_mapping(path)
    assert "concept-building-permit" in mapping
    entry = mapping["concept-building-permit"]
    assert isinstance(entry, IfcMapping)
    assert entry.concept_id == "concept-building-permit"
    assert entry.ifc_class == "IfcBuildingElementProxy"
    assert entry.psets == ("Pset_ElementCommon",)
    assert entry.notes == "Permit is a process entity."


def test_load_entries_with_missing_fields_are_skipped(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-valid\n"
        "  ifc_class: IfcWall\n"
        "  psets: []\n"
        "  notes: valid\n"
        "- concept_id: concept-missing-class\n"
        "  psets: []\n"
        "  notes: no ifc_class\n"
        "- ifc_class: IfcDoor\n"
        "  psets: []\n"
        "  notes: no concept_id\n",
    )
    mapping = load_ifc_mapping(path)
    assert set(mapping.keys()) == {"concept-valid"}


def test_load_empty_registry(tmp_path: Path) -> None:
    path = _write_yaml(tmp_path, "[]\n")
    mapping = load_ifc_mapping(path)
    assert len(mapping) == 0


def test_lookup_ifc_class_hit(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-door\n"
        "  ifc_class: IfcDoor\n"
        "  psets: [Pset_DoorCommon]\n"
        "  notes: door mapping\n",
    )
    mapping = load_ifc_mapping(path)
    entry = lookup_ifc_class("concept-door", mapping=mapping)
    assert entry is not None
    assert entry.ifc_class == "IfcDoor"


def test_lookup_ifc_class_miss_returns_none(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-door\n"
        "  ifc_class: IfcDoor\n"
        "  psets: []\n"
        "  notes: door mapping\n",
    )
    mapping = load_ifc_mapping(path)
    assert lookup_ifc_class("concept-nonexistent", mapping=mapping) is None


def test_deterministic_ordering(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-zeta\n"
        "  ifc_class: IfcZone\n"
        "  psets: []\n"
        "  notes: zeta\n"
        "- concept_id: concept-alpha\n"
        "  ifc_class: IfcAlarmSystem\n"
        "  psets: []\n"
        "  notes: alpha\n"
        "- concept_id: concept-mu\n"
        "  ifc_class: IfcMember\n"
        "  psets: []\n"
        "  notes: mu\n",
    )
    mapping = load_ifc_mapping(path)
    assert list(mapping.keys()) == ["concept-alpha", "concept-mu", "concept-zeta"]


def test_ifc_mapping_is_frozen() -> None:
    entry = IfcMapping(
        concept_id="concept-door",
        ifc_class="IfcDoor",
        psets=("Pset_DoorCommon",),
        notes="n",
    )
    with pytest.raises(Exception):
        entry.ifc_class = "IfcWall"  # type: ignore[misc]


def test_duplicate_concept_id_raises(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-door\n"
        "  ifc_class: IfcDoor\n"
        "  psets: []\n"
        "  notes: first\n"
        "- concept_id: concept-door\n"
        "  ifc_class: IfcDoorLining\n"
        "  psets: []\n"
        "  notes: dupe\n",
    )
    with pytest.raises(ValueError, match="duplicate"):
        load_ifc_mapping(path)


def test_mapping_is_read_only(tmp_path: Path) -> None:
    path = _write_yaml(
        tmp_path,
        "- concept_id: concept-door\n"
        "  ifc_class: IfcDoor\n"
        "  psets: []\n"
        "  notes: n\n",
    )
    mapping = load_ifc_mapping(path)
    assert isinstance(mapping, MappingProxyType)
    with pytest.raises(TypeError):
        mapping["concept-new"] = IfcMapping(  # type: ignore[index]
            concept_id="concept-new",
            ifc_class="IfcWall",
            psets=(),
            notes="",
        )


def test_default_mapping_path_exists_and_loads() -> None:
    assert DEFAULT_IFC_MAPPING_PATH.exists()
    mapping = load_ifc_mapping()
    assert len(mapping) >= 5
    for entry in mapping.values():
        assert isinstance(entry, IfcMapping)
        assert entry.concept_id.startswith("concept-")
        assert entry.ifc_class.startswith("Ifc")
