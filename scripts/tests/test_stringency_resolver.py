"""Stringency matrix resolver — most-stringent-law-wins under three vectors."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from vitruvius.promotion.stringency_resolver import (
    DEFAULT_STRINGENCY_VECTOR,
    CandidateEdge,
    MigrationReport,
    StringencyVerdict,
    migrate_concept_frontmatter,
    resolve_stringency,
)


def _edge(eid, value, jur="national"):
    return CandidateEdge(
        edge_id=eid,
        from_entity="concept-setback",
        predicate="limits",
        to_entity="concept-r1-zone",
        numeric_value=value,
        jurisdiction=jur,
    )


def test_maximize_picks_higher_value() -> None:
    a = _edge("edge-a", 2.0, "national")
    b = _edge("edge-b", 3.0, "lgu-qc")
    verdict = resolve_stringency(a, b, stringency_vector="maximize")
    assert verdict.winner_edge_id == "edge-b"
    assert verdict.loser_edge_id == "edge-a"
    assert verdict.unresolved is False


def test_minimize_picks_lower_value() -> None:
    a = _edge("edge-a", 60.0)
    b = _edge("edge-b", 50.0)
    verdict = resolve_stringency(a, b, stringency_vector="minimize")
    assert verdict.winner_edge_id == "edge-b"
    assert verdict.loser_edge_id == "edge-a"


def test_tie_declares_first_edge_winner_deterministically() -> None:
    a = _edge("edge-a", 2.0)
    b = _edge("edge-b", 2.0)
    v1 = resolve_stringency(a, b, stringency_vector="maximize")
    v2 = resolve_stringency(a, b, stringency_vector="maximize")
    assert v1.winner_edge_id == v2.winner_edge_id
    assert v1.winner_edge_id == "edge-a"


def test_tie_under_minimize_also_first_wins() -> None:
    a = _edge("edge-a", 5.0)
    b = _edge("edge-b", 5.0)
    verdict = resolve_stringency(a, b, stringency_vector="minimize")
    assert verdict.winner_edge_id == "edge-a"
    assert verdict.loser_edge_id == "edge-b"


def test_qualitative_returns_unresolved() -> None:
    a = _edge("edge-a", None)
    b = _edge("edge-b", None)
    verdict = resolve_stringency(a, b, stringency_vector="qualitative")
    assert verdict.unresolved is True
    assert verdict.winner_edge_id is None
    assert verdict.loser_edge_id is None


def test_qualitative_ignores_numeric_values_present() -> None:
    a = _edge("edge-a", 2.0)
    b = _edge("edge-b", 3.0)
    verdict = resolve_stringency(a, b, stringency_vector="qualitative")
    assert verdict.unresolved is True
    assert verdict.winner_edge_id is None


def test_numeric_vector_with_missing_value_raises() -> None:
    a = _edge("edge-a", None)
    b = _edge("edge-b", 3.0)
    with pytest.raises(ValueError):
        resolve_stringency(a, b, stringency_vector="maximize")


def test_numeric_vector_with_both_missing_raises_naming_edges() -> None:
    a = _edge("edge-a", None)
    b = _edge("edge-b", None)
    with pytest.raises(ValueError) as exc_info:
        resolve_stringency(a, b, stringency_vector="minimize")
    msg = str(exc_info.value)
    assert "edge-a" in msg or "edge-b" in msg


def test_unknown_stringency_vector_raises() -> None:
    a = _edge("edge-a", 1.0)
    b = _edge("edge-b", 2.0)
    with pytest.raises(ValueError):
        resolve_stringency(a, b, stringency_vector="bogus")  # type: ignore[arg-type]


def test_migration_dry_run_does_not_write(tmp_path: Path) -> None:
    concepts = tmp_path / "concepts"
    concepts.mkdir()
    before = textwrap.dedent("""\
        ---
        id: concept-setback
        title: Setback
        page_type: concept
        ---

        # Setback

        A setback is...
    """)
    target = concepts / "setback.md"
    target.write_text(before)
    report = migrate_concept_frontmatter(concepts, dry_run=True)
    # File content unchanged
    assert target.read_text() == before
    # But the report counts it
    assert report.files_updated == 1
    assert report.dry_run is True


def test_migration_execute_writes_default_vector(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    target = concepts / "x.md"
    target.write_text(textwrap.dedent("""\
        ---
        id: concept-x
        title: X
        ---

        Body.
    """))
    report = migrate_concept_frontmatter(concepts, dry_run=False)
    text = target.read_text()
    assert "stringency_vector: qualitative" in text
    assert report.files_updated == 1
    assert report.dry_run is False


def test_migration_preserves_existing_stringency_vector(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    target = concepts / "setback.md"
    target.write_text(textwrap.dedent("""\
        ---
        id: concept-setback
        title: Setback
        stringency_vector: maximize
        ---

        Body.
    """))
    report = migrate_concept_frontmatter(concepts, dry_run=False)
    text = target.read_text()
    # NOT overwritten to "qualitative"
    assert "stringency_vector: maximize" in text
    assert "stringency_vector: qualitative" not in text
    assert report.files_updated == 0
    assert report.files_skipped == 1


def test_migration_skips_files_without_frontmatter(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    target = concepts / "no_fm.md"
    target.write_text("# Just a heading, no frontmatter.\n")
    report = migrate_concept_frontmatter(concepts, dry_run=False)
    assert report.files_updated == 0
    assert report.files_skipped == 1
    # File unchanged
    assert "no frontmatter" in target.read_text()


def test_migration_processes_multiple_files(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    for i in range(5):
        (concepts / f"c{i}.md").write_text(textwrap.dedent(f"""\
            ---
            id: concept-{i}
            title: Concept {i}
            ---

            Body {i}.
        """))
    report = migrate_concept_frontmatter(concepts, dry_run=False)
    assert report.total_files == 5
    assert report.files_updated == 5
    # Every file now has the default vector
    for i in range(5):
        assert "stringency_vector: qualitative" in (concepts / f"c{i}.md").read_text()


def test_migration_report_is_frozen_and_sorted(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    for name in ["z.md", "a.md", "m.md"]:
        (concepts / name).write_text(textwrap.dedent("""\
            ---
            id: x
            title: x
            ---
        """))
    report = migrate_concept_frontmatter(concepts, dry_run=False)
    assert isinstance(report, MigrationReport)
    # updated_paths sorted alphabetically
    assert list(report.updated_paths) == sorted(report.updated_paths)
    # Frozen
    with pytest.raises(AttributeError):
        report.files_updated = 0  # type: ignore[misc]


def test_migration_preserves_body_content(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    target = concepts / "x.md"
    body = "# Heading\n\nParagraph one.\n\nParagraph two.\n"
    target.write_text(textwrap.dedent("""\
        ---
        id: concept-x
        title: X
        ---

        """) + body)
    migrate_concept_frontmatter(concepts, dry_run=False)
    after = target.read_text()
    assert "# Heading" in after
    assert "Paragraph one." in after
    assert "Paragraph two." in after


def test_migration_dry_run_updated_paths_match_execute(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    (concepts / "a.md").write_text(textwrap.dedent("""\
        ---
        id: a
        ---
    """))
    (concepts / "b.md").write_text(textwrap.dedent("""\
        ---
        id: b
        stringency_vector: minimize
        ---
    """))
    dry = migrate_concept_frontmatter(concepts, dry_run=True)
    assert dry.files_updated == 1
    assert dry.files_skipped == 1
    assert dry.total_files == 2
    # Dry run did not mutate
    assert "stringency_vector" not in (concepts / "a.md").read_text()


def test_verdict_reason_is_human_readable() -> None:
    a = _edge("edge-a", 2.0)
    b = _edge("edge-b", 3.0)
    verdict = resolve_stringency(a, b, stringency_vector="maximize")
    # Reason should mention both edges, the vector, and the winner
    assert "maximize" in verdict.reason
    assert "edge-a" in verdict.reason
    assert "edge-b" in verdict.reason


def test_qualitative_reason_explains_unresolved() -> None:
    a = _edge("edge-a", None)
    b = _edge("edge-b", None)
    verdict = resolve_stringency(a, b, stringency_vector="qualitative")
    assert "qualitative" in verdict.reason.lower() or "unresolved" in verdict.reason.lower()


def test_default_vector_is_qualitative() -> None:
    assert DEFAULT_STRINGENCY_VECTOR == "qualitative"


def test_candidate_edge_is_frozen() -> None:
    edge = _edge("edge-a", 1.0)
    with pytest.raises(AttributeError):
        edge.numeric_value = 999.0  # type: ignore[misc]


def test_verdict_is_frozen() -> None:
    a = _edge("edge-a", 2.0)
    b = _edge("edge-b", 3.0)
    verdict = resolve_stringency(a, b, stringency_vector="maximize")
    with pytest.raises(AttributeError):
        verdict.unresolved = True  # type: ignore[misc]
