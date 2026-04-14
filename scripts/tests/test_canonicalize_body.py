from pathlib import Path

from vitruvius.canonicalize import (
    extract_section_headers,
    extract_key_points,
    build_overview_paragraph,
)


FIXTURE = Path(__file__).parent / "fixtures" / "refined_pd_1096_sample.md"


def test_extract_section_headers_returns_coverage_items():
    text = FIXTURE.read_text(encoding="utf-8")
    headers = extract_section_headers(text)
    assert len(headers) == 4
    assert headers[0]["level"] == 2
    assert "Title" in headers[0]["title"]


def test_extract_key_points_returns_top_n_sentences():
    text = FIXTURE.read_text(encoding="utf-8")
    key_points = extract_key_points(text, limit=3)
    assert 1 <= len(key_points) <= 3
    assert all(len(kp) < 300 for kp in key_points)


def test_build_overview_paragraph_returns_first_non_header_para():
    text = FIXTURE.read_text(encoding="utf-8")
    overview = build_overview_paragraph(text)
    assert "National Building Code" in overview or "Decree" in overview
    assert not overview.startswith("#")


def test_resolve_referenced_concepts_from_text(tmp_path):
    from vitruvius.canonicalize import resolve_referenced_concepts

    concepts_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    concepts_dir.mkdir(parents=True)
    for slug in ("occupancy-classification", "fire-resistive-construction", "building-permit"):
        (concepts_dir / f"{slug}.md").write_text(
            f"---\nid: concept-{slug}\ntitle: {slug}\npage_type: concept\n"
            "canonical_status: placeholder\n"
            "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
            encoding="utf-8",
        )

    body = (
        "Every building shall be classified by occupancy classification. "
        "Fire-resistive construction is determined by occupancy. "
        "A building permit must be obtained before construction."
    )
    resolved = resolve_referenced_concepts(body, repo_root=tmp_path)
    assert "concept-occupancy-classification" in resolved
    assert "concept-fire-resistive-construction" in resolved
    assert "concept-building-permit" in resolved
