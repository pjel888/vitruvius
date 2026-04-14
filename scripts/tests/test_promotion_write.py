from vitruvius.promotion import write_relationship_file


def test_write_creates_valid_markdown_with_frontmatter(tmp_path):
    record = {
        "id": "rel-x-governs-y",
        "title": "X Governs Y",
        "page_type": "relationship",
        "relationship_type": "governs",
        "from_entity": "law-x",
        "to_entity": "concept-y",
        "trust_level": "primary",
        "canonical_status": "promoted",
        "confidence_score": 0.95,
        "promotion_batch_id": "B",
        "promotion_audit_log_ref": "p.log",
        "last_promoted_utc": "2026-04-14T00:00:00Z",
        "evidence": [{
            "source_id": "law-x",
            "source_section_id": "sec-1",
            "evidence_snippet": "snip",
            "reviewer_model": "gemma4:31b",
            "reviewer_confidence": 0.95,
            "review_decision": "keep",
            "reviewer_reason": "ok",
            "reviewed_at_utc": "2026-04-13T00:00:00Z",
        }],
    }
    output = tmp_path / "rel-x-governs-y.md"
    write_relationship_file(output, record)
    text = output.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "id: rel-x-governs-y" in text
    assert "# X Governs Y" in text
    assert "## Relationship Summary" in text
    assert "## Evidence" in text
    assert "sec-1" in text
