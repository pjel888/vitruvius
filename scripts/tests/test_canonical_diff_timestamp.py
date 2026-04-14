from vitruvius.canonical_diff import should_overwrite


def test_files_differing_only_by_timestamp_are_unchanged(tmp_path):
    p = tmp_path / "pd-1096.md"
    existing = (
        "---\n"
        "id: law-pd-1096\n"
        "title: PD 1096\n"
        "page_type: source\n"
        "canonical_status: draft\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n"
        "---\n"
        "# PD 1096\n\nBody\n"
    )
    p.write_text(existing, encoding="utf-8")

    new_body = existing.replace(
        "2026-04-14T00:00:00Z",
        "2026-05-01T12:34:56Z",
    )

    decision = should_overwrite(p, new_body)
    assert not decision.allowed
    assert decision.reason == "unchanged"


def test_files_differing_in_body_still_trigger_overwrite(tmp_path):
    p = tmp_path / "pd-1096.md"
    existing = (
        "---\n"
        "id: law-pd-1096\n"
        "page_type: source\n"
        "canonical_status: draft\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n"
        "---\n"
        "# PD 1096\n\nOld body\n"
    )
    p.write_text(existing, encoding="utf-8")

    new_body = existing.replace("Old body", "New body")
    decision = should_overwrite(p, new_body)
    assert decision.allowed
    assert decision.reason == "draft"


def test_files_differing_in_enriched_timestamp_are_unchanged(tmp_path):
    p = tmp_path / "concept.md"
    existing = (
        "---\n"
        "id: concept-foo\n"
        "page_type: concept\n"
        "canonical_status: enriched\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n"
        "enriched_at_utc: 2026-04-14T00:00:00Z\n"
        "---\n"
        "# Foo\n"
    )
    p.write_text(existing, encoding="utf-8")
    new_body = existing.replace("2026-04-14", "2026-05-01")
    decision = should_overwrite(p, new_body)
    assert not decision.allowed
    assert decision.reason == "unchanged"
