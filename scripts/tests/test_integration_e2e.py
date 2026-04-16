"""End-to-end integration tests.

These tests exercise multi-module flows that unit tests cannot catch.
Zero LLM calls — the tests never touch Ollama.
"""

import json
import textwrap
from pathlib import Path

import pytest


@pytest.fixture
def seeded_repo(tmp_path: Path) -> Path:
    """Build a minimal repo tree with one source, two concepts, and a refined
    markdown file that contains text the extractor + enricher can bite on.
    """
    refined = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "TEST"
    refined.mkdir(parents=True)
    # Note: split_sections in relationships_sections.py uses re.match which
    # anchors at line start — so the line must literally begin with SECTION.
    # The section-title extractor in concept_definitions.py is more permissive
    # and accepts "### SECTION" prefix. We want both to match, so use a plain
    # "SECTION X." line (no Markdown header prefix).
    (refined / "test-law.md").write_text(
        textwrap.dedent("""\
            Test Law

            SECTION 101. Building Permit

            No person, firm, or corporation shall erect any building or
            structure without first obtaining a building permit issued
            under this Code. The building permit shall be applied for in
            accordance with the requirements of Section 102.

            SECTION 102. Occupancy Classification

            Every building shall be classified in accordance with its use
            or occupancy. Occupancy classification determines the
            applicable fire-resistive requirements for the structure.
            """),
        encoding="utf-8",
    )

    shared = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    (shared / "sources").mkdir(parents=True)
    (shared / "concepts").mkdir(parents=True)
    (shared / "relationships").mkdir(parents=True)

    (shared / "sources" / "test-law.md").write_text(
        textwrap.dedent("""\
            ---
            id: law-test-law
            title: Test Law
            page_type: source
            trust_level: primary
            canonical_status: draft
            last_canonicalized_utc: 2026-04-14T00:00:00Z
            ---

            # Test Law
            """),
        encoding="utf-8",
    )

    for slug, title in [
        ("building-permit", "Building Permit"),
        ("occupancy-classification", "Occupancy Classification"),
    ]:
        (shared / "concepts" / f"{slug}.md").write_text(
            textwrap.dedent(f"""\
                ---
                id: concept-{slug}
                title: {title}
                page_type: concept
                canonical_status: draft
                concept_status: draft
                last_canonicalized_utc: 2026-04-14T00:00:00Z
                ---

                # {title}

                ## Definition

                {title} is a defined concept within the Vitruvius system.
                """),
            encoding="utf-8",
        )

    (tmp_path / "006_System-Manifests" / "runs").mkdir(parents=True)
    return tmp_path


def test_extract_dedup_prefilter_promote_enrich_end_to_end(seeded_repo, monkeypatch):
    """Full deterministic pipeline from refined markdown through enrichment."""
    import vitruvius.canonicalize as canonicalize_mod
    import vitruvius.concept_enrichment as ce_mod
    import vitruvius.pre_review_filter as prf_mod

    for mod in (canonicalize_mod, ce_mod):
        monkeypatch.setattr(mod, "get_repo_root", lambda: seeded_repo, raising=False)

    # Stage 1+2: extract + aggregate + dedup
    from vitruvius.relationships_sections import (
        aggregate_relationships,
        dedupe_by_endpoints,
        extract_section_relationships,
        split_sections,
    )

    text = (seeded_repo / "002_Raw-Conversion-Layer" / "001-Laws" /
            "refined_markdown" / "TEST" / "test-law.md").read_text(encoding="utf-8")

    concept_map = {
        "building permit": "concept-building-permit",
        "occupancy classification": "concept-occupancy-classification",
    }

    sections = split_sections(text)
    assert len(sections) >= 1

    raw_rels = []
    for section in sections:
        rels = extract_section_relationships(
            section, concept_map, source_id="law-test-law",
        )
        raw_rels.extend(rels)

    aggregated = aggregate_relationships(raw_rels)
    deduped = dedupe_by_endpoints(aggregated)

    assert len(deduped) > 0
    assert len(deduped) <= len(aggregated)

    # Stage 3: pre-review triage
    buckets = prf_mod.triage_candidates(deduped)
    total = sum(len(v) for v in buckets.values())
    assert total == len(deduped)
    assert "auto_accept" in buckets
    assert "auto_reject" in buckets
    assert "needs_review" in buckets

    # Stage 4: synthesize a high-confidence payload
    high_conf_items = []
    for cand in buckets["auto_accept"]:
        cand_clean = {k: v for k, v in cand.items() if k != "triage"}
        high_conf_items.append({
            "candidate": cand_clean,
            "review": {
                "decision": "keep",
                "confidence": 0.95,
                "reason": "pre_review_filter",
                "suggested_type": None,
                "source": "pre_review_filter",
            },
        })

    high_conf_payload = {
        "generated_at": "20260414T000000Z",
        "source_model": "deterministic",
        "source": "law-test-law",
        "threshold": 0.90,
        "count": len(high_conf_items),
        "candidates": high_conf_items,
    }

    runs = seeded_repo / "006_System-Manifests" / "runs"
    (runs / "latest_relationship_review_high_confidence.json").write_text(
        json.dumps(high_conf_payload), encoding="utf-8"
    )

    # Stage 5: promotion
    from vitruvius.promotion import run_promote_inner
    promote_result = run_promote_inner(
        repo_root=seeded_repo, execute=True, rollback_batch_id=None,
    )
    assert promote_result["rejected"] == 0, f"errors: {promote_result.get('errors')}"

    # Stage 6: concept enrichment
    from vitruvius.concept_enrichment import enrich_concepts_inner
    enrich_result = enrich_concepts_inner(repo_root=seeded_repo, force=False)

    assert enrich_result["total"] == 2
    assert enrich_result["enriched"] == 2, f"enrich result: {enrich_result}"

    concepts_dir = seeded_repo / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    for slug in ("building-permit", "occupancy-classification"):
        content = (concepts_dir / f"{slug}.md").read_text(encoding="utf-8")
        assert "canonical_status: enriched" in content
        assert "## Regulatory Basis" in content


def test_pipeline_is_deterministic_on_rerun(seeded_repo, monkeypatch):
    """Running enrichment twice on identical input produces byte-identical
    artifacts (modulo explicit timestamp fields).
    """
    import vitruvius.concept_enrichment as ce_mod
    monkeypatch.setattr(ce_mod, "get_repo_root", lambda: seeded_repo, raising=False)

    from vitruvius.concept_enrichment import enrich_concepts_inner

    enrich_concepts_inner(repo_root=seeded_repo, force=True)
    concepts_dir = seeded_repo / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"

    def _content_without_timestamps(path: Path) -> str:
        lines = path.read_text(encoding="utf-8").splitlines()
        return "\n".join(
            l for l in lines
            if not l.startswith("last_canonicalized_utc")
            and not l.startswith("enriched_at_utc")
        )

    first = {p.name: _content_without_timestamps(p) for p in concepts_dir.glob("*.md")}
    enrich_concepts_inner(repo_root=seeded_repo, force=True)
    second = {p.name: _content_without_timestamps(p) for p in concepts_dir.glob("*.md")}

    assert first == second, "enrichment must be deterministic modulo timestamps"


def test_dedup_is_closed_under_composition():
    """dedupe_by_endpoints(dedupe_by_endpoints(x)) == dedupe_by_endpoints(x)."""
    from vitruvius.relationships_sections import dedupe_by_endpoints

    candidates = [
        {"from": "concept-a", "type": "requires", "to": "concept-b",
         "occurrences": 1, "sections": [], "examples": []},
        {"from": "concept-a", "type": "affects", "to": "concept-b",
         "occurrences": 1, "sections": [], "examples": []},
        {"from": "concept-a", "type": "depends_on", "to": "concept-b",
         "occurrences": 2, "sections": [], "examples": []},
    ]

    once = dedupe_by_endpoints(candidates)
    twice = dedupe_by_endpoints(once)
    assert len(once) == len(twice)
    assert once[0]["type"] == twice[0]["type"]


def test_pre_review_filter_is_closed_under_composition():
    """Triaging the auto_accept bucket again yields the same bucket."""
    from vitruvius.pre_review_filter import triage_candidates

    candidates = [
        {
            "from": "law-test",
            "type": "governs",
            "to": "concept-building-permit",
            "occurrences": 3,
            "sections": ["sec-101"],
            "examples": ["No person shall erect a building without a building permit issued under this Code."],
        },
        {
            "from": "concept-a",
            "type": "requires",
            "to": "concept-b",
            "occurrences": 1,
            "sections": ["sec-1"],
            "examples": ["Concept a shall comply with the requirements of concept b in all respects of construction."],
        },
    ]

    first = triage_candidates(candidates)
    second = triage_candidates([
        {k: v for k, v in c.items() if k != "triage"}
        for c in first["auto_accept"]
    ])
    assert len(second["auto_accept"]) == len(first["auto_accept"])
