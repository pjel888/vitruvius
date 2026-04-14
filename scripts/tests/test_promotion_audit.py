from vitruvius.promotion import append_audit_entry, AuditEntry


def test_append_creates_file_if_missing(tmp_path):
    log = tmp_path / "latest_promotion_audit.log"
    entry = AuditEntry(
        batch_id="20260414T030000Z_a1b2c3d4",
        record_id="rel-a-governs-b",
        action="created",
        path="003/shared/relationships/rel-a-governs-b.md",
        detail="first promotion",
    )
    append_audit_entry(log, entry)
    assert log.exists()
    text = log.read_text(encoding="utf-8")
    assert "rel-a-governs-b" in text
    assert "created" in text


def test_append_is_append_only(tmp_path):
    log = tmp_path / "latest_promotion_audit.log"
    for i in range(3):
        append_audit_entry(log, AuditEntry(
            batch_id="B", record_id=f"rel-{i}", action="created",
            path=f"p-{i}.md", detail=""
        ))
    assert log.read_text(encoding="utf-8").count("\n") >= 3
