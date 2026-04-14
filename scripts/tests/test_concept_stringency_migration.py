"""Stream W3.1 — migration: add stringency_vector to every concept file."""
from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONCEPTS_DIR = REPO_ROOT / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
ALLOWED = {"maximize", "minimize", "qualitative"}


def _iter_frontmatter():
    for path in sorted(CONCEPTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            yield path, None
            continue
        end = text.find("\n---", 3)
        if end == -1:
            yield path, None
            continue
        fm = yaml.safe_load(text[3:end].strip())
        yield path, fm if isinstance(fm, dict) else None


def test_every_concept_file_has_stringency_vector() -> None:
    missing = []
    for path, fm in _iter_frontmatter():
        if fm is None:
            continue
        if "stringency_vector" not in fm:
            missing.append(path.name)
    assert missing == [], (
        f"{len(missing)} concept files missing stringency_vector: {missing[:5]}..."
    )


def test_every_stringency_vector_is_valid() -> None:
    invalid = []
    for path, fm in _iter_frontmatter():
        if fm is None:
            continue
        value = fm.get("stringency_vector")
        if value not in ALLOWED:
            invalid.append((path.name, value))
    assert invalid == [], (
        f"{len(invalid)} concept files have invalid stringency_vector: {invalid[:5]}"
    )


def test_numeric_concepts_default_to_maximize() -> None:
    expected_maximize = {
        "setbacks",
        "exit-width",
        "fire-resistive-construction",
        "light-and-ventilation",
        "means-of-egress",
    }
    for path, fm in _iter_frontmatter():
        if fm is None:
            continue
        stem = path.stem
        if stem in expected_maximize:
            assert fm.get("stringency_vector") == "maximize", (
                f"{stem} expected stringency_vector: maximize, "
                f"got {fm.get('stringency_vector')}"
            )


def test_minimize_concepts() -> None:
    expected_minimize = {
        "lot-occupancy",
        "floor-area",
        "building-height",
    }
    for path, fm in _iter_frontmatter():
        if fm is None:
            continue
        stem = path.stem
        if stem in expected_minimize:
            assert fm.get("stringency_vector") == "minimize", (
                f"{stem} expected stringency_vector: minimize, "
                f"got {fm.get('stringency_vector')}"
            )
