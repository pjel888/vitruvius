from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from vitruvius.ollama_review import run_review_relationships_ollama
from vitruvius.ollama_review_second_pass import run_second_pass_inner
from vitruvius.promotion import run_promote_inner
from vitruvius.relationships_sections import run_extract_relationships_sections_one_inner


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_extract_sections_inner_supports_explicit_outputs_and_source_id(tmp_path, monkeypatch) -> None:
    import vitruvius.relationships_sections as rs

    _write(
        tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "RA-9514" / "fire.md",
        "SECTION 1 Scope\nA building permit shall comply with occupancy classification requirements.\n",
    )
    _write(
        tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "building-permit.md",
        "---\nid: concept-building-permit\n---\n",
    )
    _write(
        tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "occupancy-classification.md",
        "---\nid: concept-occupancy-classification\n---\n",
    )

    monkeypatch.setattr(rs, "get_repo_root", lambda: tmp_path)
    json_out = tmp_path / "dataset" / "extract.json"
    txt_out = tmp_path / "dataset" / "extract.txt"
    rc = run_extract_relationships_sections_one_inner(
        repo_root=tmp_path,
        relative_markdown_path="001-Laws/refined_markdown/RA-9514/fire.md",
        json_output_path=json_out,
        txt_output_path=txt_out,
        source_id_override="irr-fire-code",
    )
    assert rc == 0
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert payload["source_id"] == "irr-fire-code"
    assert txt_out.exists()
    assert not (tmp_path / "006_System-Manifests" / "runs" / "latest_relationship_extraction_sections.json").exists()


def test_review_relationships_supports_explicit_input_and_output_paths(tmp_path) -> None:
    extraction_path = tmp_path / "custom" / "extract.json"
    extraction_path.parent.mkdir(parents=True, exist_ok=True)
    extraction_path.write_text(
        json.dumps(
            {
                "generated_at": "2026-04-16T00:00:00Z",
                "source": "001-Laws/refined_markdown/RA-9514/fire.md",
                "relationships": [
                    {
                        "from": "irr-fire-code",
                        "type": "governs",
                        "to": "concept-building-permit",
                        "occurrences": 1,
                        "sections": ["section-1"],
                        "examples": ["sample"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    review_json = tmp_path / "dataset" / "review.json"
    review_txt = tmp_path / "dataset" / "review.txt"
    triage_json = tmp_path / "dataset" / "triage.json"
    high_conf_json = tmp_path / "dataset" / "high_conf.json"

    fake_review = {
        "candidate": {
            "from": "irr-fire-code",
            "type": "governs",
            "to": "concept-building-permit",
            "occurrences": 1,
            "sections": ["section-1"],
            "examples": ["sample"],
        },
        "review": {
            "decision": "keep",
            "confidence": 0.95,
            "reason": "clear",
            "suggested_type": None,
        },
    }

    with patch("vitruvius.ollama_review.warmup_model", return_value=True), patch(
        "vitruvius.ollama_review.review_relationship", return_value=fake_review
    ):
        rc = run_review_relationships_ollama(
            extraction_report_path=extraction_path,
            review_json_path=review_json,
            review_txt_path=review_txt,
            triage_report_path=triage_json,
            high_confidence_output_path=high_conf_json,
            skip_pre_review_filter=True,
            parallelism=1,
        )
    assert rc == 0
    assert review_json.exists()
    assert review_txt.exists()
    assert high_conf_json.exists()
    assert not (tmp_path / "006_System-Manifests" / "runs" / "latest_relationship_review_ollama.json").exists()


def test_second_pass_inner_supports_explicit_input_and_output_paths(tmp_path) -> None:
    tier_one_path = tmp_path / "dataset" / "review.json"
    tier_one_path.parent.mkdir(parents=True, exist_ok=True)
    tier_one_path.write_text(
        json.dumps(
            {
                "generated_at": "20260414T050000Z",
                "model": "gemma4:e4b",
                "source": "test",
                "total_candidates": 1,
                "completed_reviews": 1,
                "status": "completed",
                "summary": {},
                "reviews": [
                    {
                        "candidate": {
                            "from": "a",
                            "type": "governs",
                            "to": "b",
                            "occurrences": 1,
                            "sections": [],
                            "examples": [],
                        },
                        "review": {
                            "decision": "review_further",
                            "confidence": 0.5,
                            "reason": "unclear",
                            "suggested_type": None,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    merged_out = tmp_path / "dataset" / "merged.json"
    worklist_out = tmp_path / "dataset" / "worklist.json"
    with patch("vitruvius.ollama_review_second_pass.call_ollama", return_value='{"decision":"keep","confidence":0.95,"reason":"ok","suggested_type":null}'):
        result = run_second_pass_inner(
            repo_root=tmp_path,
            model="qwen3:30b",
            timeout_seconds=60,
            tier_one_report_path=tier_one_path,
            merged_report_path=merged_out,
            worklist_path=worklist_out,
        )
    assert result["total_second_pass"] == 1
    assert merged_out.exists()
    assert worklist_out.exists()
    assert not (tmp_path / "006_System-Manifests" / "runs" / "latest_relationship_review_merged.json").exists()


def test_run_promote_inner_supports_explicit_input_and_staging_output_dir(tmp_path) -> None:
    shared = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    _write(
        shared / "sources" / "fire.md",
        "---\nid: irr-fire-code\ntitle: Fire\npage_type: source\ntrust_level: primary\ncanonical_status: draft\nlast_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
    )
    _write(
        shared / "concepts" / "building-permit.md",
        "---\nid: concept-building-permit\ntitle: building-permit\npage_type: concept\ncanonical_status: draft\nlast_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
    )
    high_conf = tmp_path / "dataset" / "high_conf.json"
    high_conf.parent.mkdir(parents=True, exist_ok=True)
    high_conf.write_text(
        json.dumps(
            {
                "generated_at": "20260414T030000Z",
                "source_report_generated_at": "20260414T025500Z",
                "source_model": "gemma4:31b",
                "source": "fire",
                "threshold": 0.90,
                "count": 1,
                "candidates": [
                    {
                        "candidate": {
                            "from": "irr-fire-code",
                            "type": "governs",
                            "to": "concept-building-permit",
                            "occurrences": 1,
                            "sections": ["sec-1"],
                            "examples": ["sample"],
                        },
                        "review": {
                            "decision": "keep",
                            "confidence": 0.95,
                            "reason": "clear",
                            "suggested_type": None,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    rel_out = tmp_path / "dataset" / "relationships"
    audit_log = tmp_path / "dataset" / "promotion.log"
    result = run_promote_inner(
        repo_root=tmp_path,
        execute=True,
        rollback_batch_id=None,
        high_confidence_input_path=high_conf,
        relationships_output_dir=rel_out,
        audit_log_path=audit_log,
    )
    assert result["created"] == 1
    assert audit_log.exists()
    created = list(rel_out.glob("rel-*.md"))
    assert len(created) == 1
    assert not any((shared / "relationships").glob("rel-*.md")) if (shared / "relationships").exists() else True

def test_run_promote_inner_resolves_relative_dataset_paths_against_repo_root(tmp_path) -> None:
    shared = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    _write(
        shared / "sources" / "fire.md",
        "---\nid: irr-fire-code\ntitle: Fire\npage_type: source\ntrust_level: primary\ncanonical_status: draft\nlast_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
    )
    _write(
        shared / "concepts" / "building-permit.md",
        "---\nid: concept-building-permit\ntitle: building-permit\npage_type: concept\ncanonical_status: draft\nlast_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n",
    )
    high_conf = tmp_path / "dataset" / "high_conf.json"
    high_conf.parent.mkdir(parents=True, exist_ok=True)
    high_conf.write_text(
        json.dumps(
            {
                "generated_at": "20260414T030000Z",
                "source_report_generated_at": "20260414T025500Z",
                "source_model": "gemma4:31b",
                "source": "fire",
                "threshold": 0.90,
                "count": 1,
                "candidates": [
                    {
                        "candidate": {
                            "from": "irr-fire-code",
                            "type": "governs",
                            "to": "concept-building-permit",
                            "occurrences": 1,
                            "sections": ["sec-1"],
                            "examples": ["sample"],
                        },
                        "review": {
                            "decision": "keep",
                            "confidence": 0.95,
                            "reason": "clear",
                            "suggested_type": None,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result = run_promote_inner(
        repo_root=tmp_path,
        execute=True,
        rollback_batch_id=None,
        high_confidence_input_path=Path("dataset/high_conf.json"),
        relationships_output_dir=Path("dataset/relationships"),
        audit_log_path=Path("dataset/promotion.log"),
    )
    assert result["created"] == 1
    assert (tmp_path / "dataset" / "promotion.log").exists()
    assert len(list((tmp_path / "dataset" / "relationships").glob("rel-*.md"))) == 1

def test_extract_sections_inner_supports_concept_whitelist(tmp_path, monkeypatch) -> None:
    import vitruvius.relationships_sections as rs

    _write(
        tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "BP-344" / "access.md",
        "### Section 1. Accessible Ramps\nAccessible ramps shall be provided.\n### Section 2. Signage\nSignage shall be visible.\n",
    )
    ramp = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "accessible-ramps.md"
    sign = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / "signage.md"
    _write(ramp, "---\nid: concept-accessible-ramps\n---\n")
    _write(sign, "---\nid: concept-signage\n---\n")

    monkeypatch.setattr(rs, "get_repo_root", lambda: tmp_path)
    json_out = tmp_path / "dataset" / "extract.json"
    rc = run_extract_relationships_sections_one_inner(
        repo_root=tmp_path,
        relative_markdown_path="001-Laws/refined_markdown/BP-344/access.md",
        json_output_path=json_out,
        source_id_override="irr-bp344",
        concept_paths=[ramp],
    )
    assert rc == 0
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    relationship_targets = {item["to"] for item in payload["relationships"]}
    assert "concept-accessible-ramps" in relationship_targets
    assert "concept-signage" not in relationship_targets
