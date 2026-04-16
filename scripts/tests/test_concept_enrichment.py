"""Tests for the concept enrichment orchestrator (Phase 3C Task 3).

Loads a placeholder concept file, runs definition + alias extraction,
renders an enriched frontmatter + body, and writes it back under
diff-before-write protection.
"""

import textwrap
from pathlib import Path
from unittest.mock import patch

from vitruvius.concept_enrichment import enrich_concept_inner, enrich_concepts_inner
from vitruvius.concept_enrichment import _collect_source_texts


def _seed_repo(tmp_path: Path, concept_slug: str, source_text: str) -> None:
    """Create a minimal repo tree with one concept placeholder + one source."""
    shared = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    concepts = shared / "concepts"
    sources = shared / "sources"
    concepts.mkdir(parents=True)
    sources.mkdir(parents=True)

    (concepts / f"{concept_slug}.md").write_text(
        textwrap.dedent(f"""\
            ---
            id: concept-{concept_slug}
            title: {concept_slug.replace('-', ' ').title()}
            page_type: concept
            canonical_status: placeholder
            concept_status: placeholder
            last_canonicalized_utc: 2026-04-14T00:00:00Z
            ---

            # {concept_slug.replace('-', ' ').title()}

            ## Definition

            {concept_slug.replace('-', ' ').title()} is a defined concept within the Vitruvius system.
            """),
        encoding="utf-8",
    )

    (sources / "pd-1096.md").write_text(
        textwrap.dedent("""\
            ---
            id: law-pd-1096
            title: PD 1096
            page_type: source
            trust_level: primary
            canonical_status: draft
            last_canonicalized_utc: 2026-04-14T00:00:00Z
            ---

            # PD 1096

            """) + source_text,
        encoding="utf-8",
    )

    # Refined source text has to exist in the refined layer too (enrichment
    # scans both canonical sources and refined markdown).
    refined = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown"
    refined.mkdir(parents=True)
    (refined / "pd-1096.md").write_text(source_text, encoding="utf-8")


def test_enriches_concept_with_section_title_match(tmp_path):
    source_text = textwrap.dedent("""\
        ### SECTION 701. Occupancy Classification

        Every building shall be classified in accordance with its use or occupancy.
        The National Building Code (NBC) specifies the classifications.
        """)
    _seed_repo(tmp_path, "occupancy-classification", source_text)

    result = enrich_concept_inner(
        concept_slug="occupancy-classification",
        repo_root=tmp_path,
        force=False,
    )

    assert result["enriched"] is True, f"expected enriched, got {result}"

    concept_file = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "occupancy-classification.md"
    content = concept_file.read_text(encoding="utf-8")

    # Frontmatter updates
    assert "canonical_status: enriched" in content
    assert "concept_status: enriched" in content
    assert "regulatory_basis:" in content
    assert "sec-701" in content

    # Body sections
    assert "## Definition" in content
    assert "## Regulatory Basis" in content


def test_skips_already_enriched_concept_unless_forced(tmp_path):
    source_text = "### SECTION 701. Occupancy Classification\n\nBody here."
    _seed_repo(tmp_path, "occupancy-classification", source_text)

    concept_file = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "occupancy-classification.md"
    concept_file.write_text(
        textwrap.dedent("""\
            ---
            id: concept-occupancy-classification
            title: Occupancy Classification
            page_type: concept
            canonical_status: enriched
            concept_status: enriched
            last_canonicalized_utc: 2026-04-14T00:00:00Z
            ---

            # Occupancy Classification

            ## Definition

            Hand-curated content.
            """),
        encoding="utf-8",
    )

    result = enrich_concept_inner(
        concept_slug="occupancy-classification",
        repo_root=tmp_path,
        force=False,
    )
    assert result["enriched"] is False
    assert "already_enriched" in result.get("reason", "")

    # Content preserved
    content = concept_file.read_text(encoding="utf-8")
    assert "Hand-curated content" in content


def test_missing_concept_returns_error(tmp_path):
    _seed_repo(tmp_path, "existing-concept", "some text")
    result = enrich_concept_inner(
        concept_slug="nonexistent-concept",
        repo_root=tmp_path,
        force=False,
    )
    assert result["enriched"] is False
    assert "not_found" in result.get("reason", "")


def test_concept_without_definition_stays_placeholder(tmp_path):
    source_text = "Generic source text with no mention of the concept or any definition anchors."
    _seed_repo(tmp_path, "obscure-concept", source_text)

    result = enrich_concept_inner(
        concept_slug="obscure-concept",
        repo_root=tmp_path,
        force=False,
    )
    assert result["enriched"] is False
    assert "no_definition_found" in result.get("reason", "")


def test_batch_enriches_multiple_concepts(tmp_path):
    source_text = textwrap.dedent("""\
        ### SECTION 701. Occupancy Classification

        Every building shall be classified by its occupancy.

        ### SECTION 301. Building Permit

        No person shall build without a permit.
        """)
    _seed_repo(tmp_path, "occupancy-classification", source_text)

    # Add a second concept to the same tree
    concepts_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    (concepts_dir / "building-permit.md").write_text(
        textwrap.dedent("""\
            ---
            id: concept-building-permit
            title: Building Permit
            page_type: concept
            canonical_status: placeholder
            concept_status: placeholder
            last_canonicalized_utc: 2026-04-14T00:00:00Z
            ---

            # Building Permit

            ## Definition

            Building Permit is a defined concept within the Vitruvius system.
            """),
        encoding="utf-8",
    )

    summary = enrich_concepts_inner(repo_root=tmp_path, force=False)

    assert summary["total"] == 2
    assert summary["enriched"] == 2
    assert summary["skipped"] == 0


def test_collect_source_texts_preserves_non_pd_source_ids(tmp_path):
    shared = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    shared.mkdir(parents=True)
    (shared / "bp344.md").write_text(
        textwrap.dedent("""\
            ---
            id: irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344
            title: BP 344
            page_type: source
            trust_level: primary
            canonical_status: draft
            last_canonicalized_utc: 2026-04-14T00:00:00Z
            ---

            body
            """),
        encoding="utf-8",
    )
    refined = (
        tmp_path
        / "002_Raw-Conversion-Layer"
        / "001-Laws"
        / "refined_markdown"
        / "BP-344"
    )
    refined.mkdir(parents=True)
    (refined / "2024 Revised Implementing Rules and Regulations Batas Pambansa Blg. 344 _ National Council on Disability Affairs.md").write_text(
        "Accessible ramps text",
        encoding="utf-8",
    )

    pairs = _collect_source_texts(tmp_path)
    source_ids = [source_id for source_id, _text in pairs]
    assert "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344" in source_ids
