from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import yaml


def test_build_skip_review_high_confidence_payload_preserves_candidates() -> None:
    import pipeline_cli

    payload = pipeline_cli._build_skip_review_high_confidence_payload(
        extract_report={
            "generated_at": "2026-04-24T00:00:00Z",
            "source": "demo-source",
            "relationships": [
                {"from": "law-a", "to": "concept-b", "type": "governs"},
                {"from": "law-a", "to": "concept-c", "type": "defines"},
            ],
        },
        source_id="law-a",
    )

    assert payload["count"] == 2
    assert len(payload["candidates"]) == 2
    assert all(item["review"]["decision"] == "keep" for item in payload["candidates"])
    assert payload["candidates"][0]["candidate"]["type"] == "governs"


def test_convert_and_refine_for_kg_pipeline_uses_ocr_for_scanned_pdf(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pipeline_cli
    import vitruvius.conversion as conversion
    import vitruvius.detection as detection
    import vitruvius.normalization.refine as refine

    raw_pdf = tmp_path / "001_Raw-Source-Layer" / "001-Laws" / "PD-1" / "demo.pdf"
    raw_pdf.parent.mkdir(parents=True, exist_ok=True)
    raw_pdf.write_bytes(b"%PDF-1.4\n%raw\n")

    monkeypatch.setattr(
        detection,
        "detect_pdf_type",
        lambda path, sample_pages=5: {
            "result": "LIKELY_SCANNED_PDF",
            "recommended_route": "OCR_THEN_OPENDATALOADER",
        },
    )

    calls: dict[str, object] = {}

    def fake_ocr(input_path: str, output_path: str, **kwargs) -> None:
        calls["ocr_input"] = input_path
        calls["ocr_output"] = output_path
        Path(output_path).write_bytes(b"%PDF-1.4\n%ocr\n")

    def fake_convert_pdf_at_path(pdf_path: Path, logical_relative_source_path: str, **kwargs):
        calls["convert_pdf_path"] = str(pdf_path)
        calls["logical_relative_source_path"] = logical_relative_source_path
        calls["convert_kwargs"] = kwargs
        return {
            "markdown_output_relative": "001-Laws/raw_markdown/PD-1/demo.md",
            "json_output_relative": "001-Laws/raw_json/PD-1/demo.json",
            "status": "converted",
        }

    monkeypatch.setattr(conversion, "convert_pdf_at_path", fake_convert_pdf_at_path)
    monkeypatch.setattr(conversion, "run_convert_one", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("run_convert_one should not be used for scanned PDFs")))
    monkeypatch.setattr(refine, "run_refine_one", lambda relative_markdown_path: 0)
    monkeypatch.setitem(sys.modules, "ocrmypdf", SimpleNamespace(ocr=fake_ocr))

    result = pipeline_cli._convert_and_refine_for_kg_pipeline(
        repo_root=tmp_path,
        relative_source_path="001-Laws/PD-1/demo.pdf",
    )

    assert result["used_ocr"] is True
    assert result["converted"] is True
    assert result["refined"] is True
    assert str(raw_pdf) == calls["ocr_input"]
    assert str(tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "ocr_pdf" / "PD-1" / "demo.pdf") == calls["ocr_output"]
    assert calls["logical_relative_source_path"] == "001-Laws/PD-1/demo.pdf"


def test_review_relationships_ollama_writes_empty_high_confidence_file_for_zero_candidates(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import vitruvius.ollama_review as review

    monkeypatch.chdir(tmp_path)
    extraction_report = tmp_path / "extract.json"
    extraction_report.write_text(
        json.dumps(
            {
                "generated_at": "2026-04-24T00:00:00Z",
                "source": "demo-source",
                "relationships": [],
            }
        ),
        encoding="utf-8",
    )
    high_conf = tmp_path / "high_conf.json"
    review_json = tmp_path / "review.json"
    review_txt = tmp_path / "review.txt"

    rc = review.run_review_relationships_ollama(
        extraction_report_path=extraction_report,
        review_json_path=review_json,
        review_txt_path=review_txt,
        high_confidence_output_path=high_conf,
    )

    assert rc == 0
    payload = json.loads(high_conf.read_text(encoding="utf-8"))
    assert payload["count"] == 0
    assert payload["candidates"] == []


def test_source_matches_subjects_uses_source_relative_markdown_path(
    tmp_path: Path,
) -> None:
    import pipeline_cli

    source_md = tmp_path / "source.md"
    source_md.write_text(
        "---\n"
        "id: demo\n"
        "source_relative_markdown_path: 003-Theory/refined_markdown/demo.md\n"
        "---\n\n"
        "# Demo\n",
        encoding="utf-8",
    )

    assert pipeline_cli._source_matches_subjects(source_md, {"003-Theory"}, tmp_path) is True
    assert pipeline_cli._source_matches_subjects(source_md, {"001-Laws"}, tmp_path) is False


def test_build_structured_source_file_disambiguates_same_title_sources(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import vitruvius.canonicalize as canonicalize

    repo_root = tmp_path
    first_refined = repo_root / "002_Raw-Conversion-Layer" / "003-Theory" / "refined_markdown" / "TOA 1.md"
    second_refined = repo_root / "002_Raw-Conversion-Layer" / "003-Theory" / "refined_markdown" / "TOA 2.md"
    first_refined.parent.mkdir(parents=True, exist_ok=True)
    first_refined.write_text("# TOA\n\nBody one\n", encoding="utf-8")
    second_refined.write_text("# TOA\n\nBody two\n", encoding="utf-8")

    rules_dir = repo_root / "scripts" / "vitruvius" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    (rules_dir / "canonical_rules.yaml").write_text("rules: []\n", encoding="utf-8")
    (repo_root / "006_System-Manifests" / "registries").mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(canonicalize, "get_repo_root", lambda: repo_root)

    first_target, first_content = canonicalize.build_structured_source_file(
        repo_root=repo_root,
        relative_markdown_path="003-Theory/refined_markdown/TOA 1.md",
    )
    first_target.write_text(first_content, encoding="utf-8")

    second_target, second_content = canonicalize.build_structured_source_file(
        repo_root=repo_root,
        relative_markdown_path="003-Theory/refined_markdown/TOA 2.md",
    )

    assert first_target.name == "toa.md"
    assert second_target.name != "toa.md"
    assert second_target.name.startswith("source-toa")
    assert "id: source-toa-" in second_content


def test_canonical_source_id_for_relative_path_prefers_existing_canonical_source(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import vitruvius.source_identity as source_identity
    import vitruvius.paths as paths
    import vitruvius.canonicalize as canonicalize

    repo_root = tmp_path
    sources_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    sources_dir.joinpath("demo.md").write_text(
        "---\n"
        "id: law-demo-existing\n"
        "source_relative_markdown_path: 001-Laws/refined_markdown/demo.md\n"
        "---\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(paths, "get_repo_root", lambda: repo_root)
    monkeypatch.setattr(source_identity, "get_repo_root", lambda: repo_root)
    monkeypatch.setattr(canonicalize, "build_plan", lambda relative_path: {"canonical_id": "law-demo-new"})

    assert source_identity.canonical_source_id_for_relative_path("001-Laws/refined_markdown/demo.md") == "law-demo-existing"


def test_build_structured_source_file_renders_yaml_safe_frontmatter(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import vitruvius.canonicalize as canonicalize

    repo_root = tmp_path
    refined = repo_root / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "demo.md"
    refined.parent.mkdir(parents=True, exist_ok=True)
    refined.write_text("# Demo: Example\n", encoding="utf-8")

    rules_dir = repo_root / "scripts" / "vitruvius" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    (rules_dir / "canonical_rules.yaml").write_text("rules: []\n", encoding="utf-8")
    (repo_root / "006_System-Manifests" / "registries").mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(canonicalize, "get_repo_root", lambda: repo_root)
    monkeypatch.setattr(canonicalize, "extract_title_from_content", lambda text, fallback: "Notes: Demo\tTitle")

    _target, content = canonicalize.build_structured_source_file(
        repo_root=repo_root,
        relative_markdown_path="001-Laws/refined_markdown/demo.md",
    )

    end = content.find("\n---", 3)
    frontmatter = yaml.safe_load(content[3:end].strip())
    assert frontmatter["title"] == "Notes: Demo\tTitle"


def test_audit_log_ref_for_record_allows_paths_outside_repo(tmp_path: Path) -> None:
    from vitruvius.promotion import _audit_log_ref_for_record

    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    outside_log = tmp_path / "outside.log"

    assert _audit_log_ref_for_record(outside_log, repo_root) == str(outside_log)

    inside_log = repo_root / "006_System-Manifests" / "runs" / "audit.log"
    assert _audit_log_ref_for_record(inside_log, repo_root) == "006_System-Manifests/runs/audit.log"


def test_conversion_path_matches_nested_subjects() -> None:
    import pipeline_cli

    subject_set = {"001-Laws/PD-1096"}
    assert pipeline_cli._conversion_path_matches_subjects(
        "001-Laws/refined_markdown/PD-1096/PD 1096 - National Building Code.md",
        subject_set,
    ) is True
    assert pipeline_cli._conversion_path_matches_subjects(
        "001-Laws/raw_markdown/PD-1096/Rule 7 _ 8.md",
        subject_set,
    ) is True
    assert pipeline_cli._conversion_path_matches_subjects(
        "001-Laws/sidecar_json/PD-1096/PD 1096 - National Building Code.json",
        subject_set,
    ) is True
    assert pipeline_cli._conversion_path_matches_subjects(
        "001-Laws/refined_markdown/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.md",
        subject_set,
    ) is False


def test_run_kg_pipeline_full_path_runs_ocr_queue_and_execute_before_refine(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pipeline_cli
    import vitruvius.config as cfg
    import vitruvius.conversion as conversion
    import vitruvius.normalization.refine as refine
    import vitruvius.ocr as ocr
    import vitruvius.paths as paths
    import vitruvius.kg.unified_snapshot_builder as usb

    calls: list[str] = []

    monkeypatch.setattr(paths, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(cfg, "is_kg_enabled", lambda: True)
    monkeypatch.setattr(cfg, "resolve_review_model", lambda explicit_model=None, preset=None: "demo-model")
    monkeypatch.setattr(cfg, "resolve_review_preset", lambda preset=None: {})
    monkeypatch.setattr(cfg, "get_ollama_default_timeout", lambda: 1)
    monkeypatch.setattr(cfg, "get_ollama_default_parallelism", lambda: 1)
    monkeypatch.setattr(cfg, "is_kg_neo4j_backend", lambda: False)

    monkeypatch.setattr(pipeline_cli, "run_pipeline", lambda: calls.append("run_pipeline") or 0)
    monkeypatch.setattr(conversion, "run_convert", lambda: calls.append("run_convert") or 0)
    monkeypatch.setattr(ocr, "run_ocr_queue", lambda: calls.append("run_ocr_queue") or 0)
    monkeypatch.setattr(ocr, "run_ocr_execute", lambda: calls.append("run_ocr_execute") or 0)
    monkeypatch.setattr(refine, "run_refine", lambda: calls.append("run_refine") or 0)

    class FakeSnapshot:
        def entity_counts(self):
            return {
                "document_versions": 0,
                "sections": 0,
                "chunks": 0,
                "evidence_spans": 0,
                "canonical_nodes": 0,
                "relationship_assertions": 0,
                "placement_assertions": 0,
                "merge_assertions": 0,
                "fast_edges": 0,
            }

    class FakeBuilder:
        def __init__(self, repo_root: Path):
            self.repo_root = repo_root
            self._warnings = []

        def build(self):
            calls.append("build_snapshot")
            return FakeSnapshot()

        def write_snapshot(self, snapshot, out_path=None):
            target = out_path or (self.repo_root / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2" / "snapshot.json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("{}", encoding="utf-8")
            return target

    monkeypatch.setattr(usb, "UnifiedSnapshotBuilder", FakeBuilder)

    rc = pipeline_cli.run_kg_pipeline()

    assert rc == 0
    assert calls[:5] == [
        "run_pipeline",
        "run_convert",
        "run_ocr_queue",
        "run_ocr_execute",
        "run_refine",
    ]


def test_run_kg_pipeline_phase3_report_uses_relationship_and_promotion_counts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pipeline_cli
    import vitruvius.config as cfg
    import vitruvius.paths as paths
    import vitruvius.conversion as conversion
    import vitruvius.normalization.refine as refine
    import vitruvius.canonicalize as canonicalize
    import vitruvius.ollama_review as review
    import vitruvius.promotion as promotion
    import vitruvius.relationships_sections as rel_sections
    import vitruvius.kg.unified_snapshot_builder as usb

    repo_root = tmp_path
    (repo_root / "006_System-Manifests" / "runs").mkdir(parents=True, exist_ok=True)
    refined = repo_root / "002_Raw-Conversion-Layer" / "003-Theory" / "refined_markdown" / "demo.md"
    refined.parent.mkdir(parents=True, exist_ok=True)
    refined.write_text("# Demo\n", encoding="utf-8")

    source_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    source_dir.mkdir(parents=True, exist_ok=True)
    source_dir.joinpath("demo.md").write_text(
        "---\n"
        "id: source-demo\n"
        "title: Demo\n"
        "page_type: source\n"
        "canonical_status: draft\n"
        "source_relative_markdown_path: 003-Theory/refined_markdown/demo.md\n"
        "---\n\n# Demo\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(paths, "get_repo_root", lambda: repo_root)
    monkeypatch.setattr(cfg, "is_kg_enabled", lambda: True)
    monkeypatch.setattr(cfg, "resolve_review_model", lambda explicit_model=None, preset=None: "demo-model")
    monkeypatch.setattr(cfg, "resolve_review_preset", lambda preset=None: {})
    monkeypatch.setattr(cfg, "get_ollama_default_timeout", lambda: 1)
    monkeypatch.setattr(cfg, "get_ollama_default_parallelism", lambda: 1)
    monkeypatch.setattr(cfg, "is_kg_neo4j_backend", lambda: False)
    monkeypatch.setattr(pipeline_cli, "run_pipeline", lambda: 0)
    monkeypatch.setattr(conversion, "run_convert", lambda: 0)
    monkeypatch.setattr(refine, "run_refine", lambda: 0)
    monkeypatch.setattr(canonicalize, "run_canonicalize", lambda: 0)

    def fake_extract(**kwargs):
        Path(kwargs["json_output_path"]).write_text(
            json.dumps(
                {
                    "generated_at": "now",
                    "source": kwargs["relative_markdown_path"],
                    "source_id": kwargs["source_id_override"],
                    "total_sections": 1,
                    "total_relationships": 2,
                    "relationships": [
                        {"from": "source-demo", "to": "concept-a", "type": "governs"},
                        {"from": "source-demo", "to": "concept-b", "type": "defines"},
                    ],
                }
            ),
            encoding="utf-8",
        )
        Path(kwargs["txt_output_path"]).write_text("ok\n", encoding="utf-8")
        return 0

    def fake_review(**kwargs):
        Path(kwargs["review_json_path"]).write_text(
            json.dumps(
                {
                    "generated_at": "now",
                    "model": "demo-model",
                    "source": "003-Theory/refined_markdown/demo.md",
                    "total_candidates": 2,
                    "completed_reviews": 2,
                    "status": "completed",
                    "summary": {"keep": 1, "review_further": 1, "reject": 0, "high_confidence_keep": 1, "high_confidence_reject": 0},
                    "reviews": [],
                }
            ),
            encoding="utf-8",
        )
        Path(kwargs["high_confidence_output_path"]).write_text(
            json.dumps(
                {
                    "generated_at": "now",
                    "source_report_generated_at": "now",
                    "source_model": "demo-model",
                    "source": "003-Theory/refined_markdown/demo.md",
                    "threshold": 0.9,
                    "count": 1,
                    "candidates": [
                        {
                            "candidate": {"from": "source-demo", "to": "concept-a", "type": "governs"},
                            "review": {"decision": "keep", "confidence": 0.95, "reason": "ok", "suggested_type": None},
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return 0

    monkeypatch.setattr(rel_sections, "run_extract_relationships_sections_one_inner", fake_extract)
    monkeypatch.setattr(review, "run_review_relationships_ollama", fake_review)
    monkeypatch.setattr(
        promotion,
        "run_promote_inner",
        lambda **kwargs: {
            "batch_id": "batch",
            "total_candidates": 1,
            "created": 1,
            "merged": 0,
            "skipped": 0,
            "rejected": 0,
            "errors": [],
        },
    )

    class FakeSnapshot:
        def entity_counts(self):
            return {
                "document_versions": 1,
                "sections": 1,
                "chunks": 1,
                "evidence_spans": 0,
                "canonical_nodes": 1,
                "relationship_assertions": 1,
                "placement_assertions": 0,
                "merge_assertions": 0,
                "fast_edges": 1,
            }

    class FakeBuilder:
        def __init__(self, repo_root: Path):
            self.repo_root = repo_root
            self._warnings = []

        def build(self):
            return FakeSnapshot()

        def write_snapshot(self, snapshot, out_path=None):
            target = out_path or (self.repo_root / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2" / "snapshot.json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("{}", encoding="utf-8")
            return target

    monkeypatch.setattr(usb, "UnifiedSnapshotBuilder", FakeBuilder)

    rc = pipeline_cli.run_kg_pipeline(subjects=["003-Theory"])
    assert rc == 0

    report_files = sorted((repo_root / "006_System-Manifests" / "runs").glob("kg_pipeline_report_*.json"))
    payload = json.loads(report_files[-1].read_text(encoding="utf-8"))
    phase3 = payload["phases"][2]
    assert phase3["sources_total"] == 1
    assert phase3["extracted_relationships"] == 2
    assert phase3["high_confidence_candidates"] == 1
    assert phase3["promoted"] == 1
    assert phase3["promoted_sources"] == 1
    assert phase3["promotion_candidates"] == 1
    assert phase3["promotion_created"] == 1
    assert phase3["promotion_merged"] == 0
    assert phase3["zero_relationship_sources"] == 0
    assert phase3["zero_high_confidence_sources"] == 0
