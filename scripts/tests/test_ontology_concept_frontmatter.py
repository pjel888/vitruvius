"""Stream M.2 — validate optional ifc_class / ifc_psets frontmatter on concepts."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from vitruvius.ontology.ifc_registry import load_ifc_mapping


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REAL_CONCEPTS_DIR = (
    REPO_ROOT / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
)
SPEC_PATH = REPO_ROOT / ".ai" / "06_specs" / "concept-schema.md"


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    body = text[3:end].strip()
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def test_spec_documents_optional_ifc_fields() -> None:
    text = SPEC_PATH.read_text(encoding="utf-8")
    assert "`ifc_class`" in text, "concept schema must document optional ifc_class field"
    assert "`ifc_psets`" in text, "concept schema must document optional ifc_psets field"


def test_concept_without_ifc_class_is_valid(tmp_path: Path) -> None:
    body = (
        "---\n"
        "id: concept-doors-and-exits\n"
        "title: Doors And Exits\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n"
        "---\n\n# Doors And Exits\n"
    )
    fm = _parse_frontmatter(body)
    assert fm.get("id") == "concept-doors-and-exits"
    assert fm.get("ifc_class") is None


def test_concept_with_valid_ifc_class_accepted(tmp_path: Path) -> None:
    mapping = load_ifc_mapping()
    body = (
        "---\n"
        "id: concept-doors-and-exits\n"
        "title: Doors And Exits\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "ifc_class: IfcDoor\n"
        "ifc_psets: [Pset_DoorCommon]\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n"
        "---\n"
    )
    fm = _parse_frontmatter(body)
    declared = fm.get("ifc_class")
    assert isinstance(declared, str)
    # Registry class for this concept should match the declared class.
    entry = mapping.get(fm.get("id"))
    assert entry is not None
    assert entry.ifc_class == declared


def test_concept_with_unknown_ifc_class_rejected_by_registry() -> None:
    mapping = load_ifc_mapping()
    body = (
        "---\n"
        "id: concept-doors-and-exits\n"
        "title: Doors And Exits\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "ifc_class: TotallyFakeClass\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n"
        "---\n"
    )
    fm = _parse_frontmatter(body)
    declared = fm.get("ifc_class")
    # A concept declaring a class NOT present in the registry-registered class
    # set is invalid at lint time.
    known_ifc_classes = {entry.ifc_class for entry in mapping.values()}
    assert declared not in known_ifc_classes


def test_real_concept_files_with_ifc_class_match_registry() -> None:
    if not REAL_CONCEPTS_DIR.exists():
        pytest.skip("concepts directory not present in this checkout")
    mapping = load_ifc_mapping()
    offenders: list[str] = []
    for path in sorted(REAL_CONCEPTS_DIR.glob("*.md")):
        fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
        if "ifc_class" not in fm:
            continue
        declared = fm.get("ifc_class")
        if not isinstance(declared, str) or not declared.startswith("Ifc"):
            offenders.append(f"{path.name}: invalid ifc_class value {declared!r}")
            continue
        concept_id = fm.get("id")
        if concept_id in mapping and mapping[concept_id].ifc_class != declared:
            offenders.append(
                f"{path.name}: declares {declared!r}, registry expects "
                f"{mapping[concept_id].ifc_class!r}"
            )
    assert offenders == [], "\n".join(offenders)
