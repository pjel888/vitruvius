from vitruvius.canonical_diff import should_overwrite


def test_draft_files_can_be_overwritten(tmp_path):
    p = tmp_path / "pd-1096.md"
    p.write_text(
        "---\nid: law-pd-1096\npage_type: source\ncanonical_status: draft\n---\n# X\n",
        encoding="utf-8",
    )
    decision = should_overwrite(p, new_body="newer content")
    assert decision.allowed
    assert decision.reason == "draft"


def test_enriched_files_are_protected(tmp_path):
    p = tmp_path / "pd-1096.md"
    p.write_text(
        "---\nid: law-pd-1096\npage_type: source\ncanonical_status: enriched\n---\n# X\n",
        encoding="utf-8",
    )
    decision = should_overwrite(p, new_body="newer content")
    assert not decision.allowed
    assert "enriched" in decision.reason


def test_nonexistent_files_can_be_written(tmp_path):
    p = tmp_path / "new.md"
    decision = should_overwrite(p, new_body="")
    assert decision.allowed
    assert decision.reason == "new_file"


def test_identical_content_is_noop(tmp_path):
    p = tmp_path / "pd-1096.md"
    content = (
        "---\nid: law-pd-1096\npage_type: source\ncanonical_status: draft\n---\n# X\n"
    )
    p.write_text(content, encoding="utf-8")
    decision = should_overwrite(p, new_body=content)
    assert not decision.allowed
    assert decision.reason == "unchanged"
