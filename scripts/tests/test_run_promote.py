import json
from pathlib import Path

from vitruvius.promotion import run_promote_inner


def _seed_canonical_tree(root: Path) -> None:
    """Create a minimal canonical tree with one source and two concepts."""
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    (shared / "sources").mkdir(parents=True)
    (shared / "concepts").mkdir(parents=True)
    (shared / "relationships").mkdir(parents=True)

    (shared / "sources" / "pd-1096.md").write_text(
        "---\nid: law-pd-1096\ntitle: PD 1096\npage_type: source\n"
        "trust_level: primary\ncanonical_status: draft\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    for slug in ("occupancy-classification", "fire-resistive-construction"):
        (shared / "concepts" / f"{slug}.md").write_text(
            f"---\nid: concept-{slug}\ntitle: {slug}\npage_type: concept\n"
            "canonical_status: draft\n"
            "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
            encoding="utf-8",
        )


def _seed_high_conf_file(root: Path) -> None:
    runs = root / "006_System-Manifests" / "runs"
    runs.mkdir(parents=True)
    payload = {
        "generated_at": "20260414T030000Z",
        "source_report_generated_at": "20260414T025500Z",
        "source_model": "gemma4:31b",
        "source": "pd-1096",
        "threshold": 0.90,
        "count": 1,
        "candidates": [
            {
                "candidate": {
                    "from": "law-pd-1096",
                    "type": "governs",
                    "to": "concept-fire-resistive-construction",
                    "occurrences": 1,
                    "sections": ["sec-701"],
                    "examples": ["Every building shall be classified..."],
                },
                "review": {
                    "decision": "keep",
                    "confidence": 0.92,
                    "reason": "clear governs",
                    "suggested_type": None,
                },
            }
        ],
    }
    (runs / "latest_relationship_review_high_confidence.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_dry_run_does_not_write_files(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    result = run_promote_inner(repo_root=tmp_path, execute=False, rollback_batch_id=None)

    assert result["would_create"] == 1
    assert result["would_merge"] == 0
    rels_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    assert not any(p.name.startswith("rel-") for p in rels_dir.iterdir())


def test_execute_writes_file_and_audit(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    result = run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)

    assert result["created"] == 1
    assert result["merged"] == 0
    rels_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    created = [p for p in rels_dir.iterdir() if p.name.startswith("rel-")]
    assert len(created) == 1
    audit_log = tmp_path / "006_System-Manifests" / "runs" / "latest_promotion_audit.log"
    assert audit_log.exists()
    assert "created" in audit_log.read_text(encoding="utf-8")


def test_idempotent_execute(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)
    second = run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)

    # Second run must skip (identical evidence fingerprint), not merge or create.
    assert second["created"] == 0
    assert second["merged"] == 0
    assert second["skipped"] == 1


def test_idempotent_file_bytes_unchanged(tmp_path):
    _seed_canonical_tree(tmp_path)
    _seed_high_conf_file(tmp_path)

    run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)
    rels_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    first_bytes = {p.name: p.read_bytes() for p in rels_dir.iterdir() if p.name.startswith("rel-")}

    run_promote_inner(repo_root=tmp_path, execute=True, rollback_batch_id=None)
    second_bytes = {p.name: p.read_bytes() for p in rels_dir.iterdir() if p.name.startswith("rel-")}

    assert first_bytes == second_bytes
