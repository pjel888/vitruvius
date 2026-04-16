from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

pytest.importorskip("rdflib")


CLI = Path(__file__).resolve().parent.parent / "pipeline_cli.py"


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": "scripts"}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_dataset_repo(root: Path) -> Path:
    raw_base = root / "001_Raw-Source-Layer" / "001-Laws"
    for folder in ("PD-1096", "RA-9514", "BP-344", "BP-220"):
        folder_root = raw_base / folder
        folder_root.mkdir(parents=True, exist_ok=True)
        (folder_root / f"{folder}-source.pdf").write_bytes(b"%PDF-1.4\n")

    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    _write(shared / "sources" / "pd-1096.md", (
        "---\n"
        "id: law-pd-1096\n"
        "trust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    _write(shared / "concepts" / "building-permit.md", (
        "---\n"
        "id: concept-building-permit\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    _write(shared / "relationships" / "r.md", (
        "---\n"
        "id: rel-pd-1096-governs-building-permit\n"
        "page_type: relationship\n"
        "relationship_type: governs\n"
        "from_entity: law-pd-1096\n"
        "to_entity: concept-building-permit\n"
        "canonical_status: promoted\n"
        "evidence:\n"
        "- source_id: law-pd-1096\n"
        "  source_section_id: sec-301\n"
        "  evidence_snippet: No person shall erect any building without a permit.\n"
        "  reviewer_confidence: 0.95\n"
        "---\n\n# body\n"
    ))

    manifest = {
        "dataset_id": "laws-core-bundle-m1",
        "dataset_kind": "laws-mini-bundle",
        "scope_notes": [
            "Bounded M1 proof only.",
            "No generic Phase 11 expansion implied.",
        ],
        "raw_slice_anchors": [
            {
                "folder_name": folder,
                "raw_root": f"001_Raw-Source-Layer/001-Laws/{folder}",
                "entry_role": "authoritative",
                "authority_tier": "primary",
                "variant_family": folder.lower(),
                "edition_or_source_note": "Core bundle folder anchor",
                "include_in_m1": True,
                "reason": "Pilot validation target",
            }
            for folder in ("PD-1096", "RA-9514", "BP-344", "BP-220")
        ],
        "canonical_input_manifest": {
            "sources": [
                {
                    "path": "003_Canonical-Knowledge-Layer/shared/sources/pd-1096.md",
                    "folder_name": "PD-1096",
                    "entry_role": "authoritative",
                    "authority_tier": "primary",
                    "variant_family": "pd-1096-law",
                    "edition_or_source_note": "Selected scoped canonical law source",
                    "include_in_m1": True,
                    "reason": "Current truth-bearing source input",
                }
            ],
            "concepts": [
                {
                    "path": "003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md",
                    "folder_name": "PD-1096",
                    "entry_role": "derived",
                    "authority_tier": "derived",
                    "variant_family": "pd-1096-concept",
                    "edition_or_source_note": "Selected scoped canonical concept",
                    "include_in_m1": True,
                    "reason": "Current truth-bearing concept input",
                }
            ],
        },
        "relationship_input_manifest": {
            "relationships": [
                {
                    "path": "003_Canonical-Knowledge-Layer/shared/relationships/r.md",
                    "folder_name": "PD-1096",
                    "entry_role": "authoritative",
                    "authority_tier": "approved",
                    "variant_family": "pd-1096-relationship",
                    "edition_or_source_note": "Selected approved relationship input",
                    "include_in_m1": True,
                    "reason": "Current scoped promoted relationship input",
                }
            ]
        },
        "graph_output_root": "005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1",
        "run_output_root": "006_System-Manifests/runs/datasets/laws-core-bundle-m1",
        "query_snapshot_path_template": "005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/{run_id}_graph_snapshot.json",
        "freshness_policy": {
            "mode": "exact-manifest-hash-and-input-fingerprint",
            "require_explicit_snapshot_selection": True,
        },
        "pilot_gate": {
            "require_manifest_validation": True,
            "require_bounded_inputs": True,
            "require_bounded_outputs": True,
            "require_scoped_query": True,
            "require_low_spec_budget": True,
        },
    }
    manifest_path = root / "config" / "datasets" / "laws-core-bundle-m1.yaml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return manifest_path


def test_build_graph_with_dataset_manifest_writes_isolated_outputs(tmp_path: Path) -> None:
    manifest_path = _seed_dataset_repo(tmp_path)

    result = _run_cli(["build-graph", "--dataset-manifest", str(manifest_path)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr

    payload = json.loads(result.stdout)
    snapshot_path = tmp_path / payload["snapshot_path"]
    integrity_path = tmp_path / payload["integrity_report_path"]
    build_report_path = tmp_path / payload["build_report_path"]

    assert snapshot_path.exists()
    assert integrity_path.exists()
    assert build_report_path.exists()
    assert not (tmp_path / "005_Operational-Intelligence-Layer" / "graph" / "latest_graph_snapshot.json").exists()
    assert payload["dataset_id"] == "laws-core-bundle-m1"

    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    metadata = snapshot["metadata"]
    assert metadata["dataset_id"] == "laws-core-bundle-m1"
    assert metadata["run_id"]
    assert metadata["manifest_hash"]
    assert metadata["selected_snapshot_path"] == payload["snapshot_path"]

    report = json.loads(build_report_path.read_text(encoding="utf-8"))
    assert report["incomplete"] is True
    folder_rows = {row["folder_name"]: row for row in report["coverage"]}
    assert set(folder_rows) == {"PD-1096", "RA-9514", "BP-344", "BP-220"}
    assert folder_rows["PD-1096"]["status"] == "covered"
    assert folder_rows["RA-9514"]["status"] == "blocked"
    assert report["thin_graph_metrics"]["edge_type_diversity"]["count"] == 1


def test_build_graph_marks_source_only_dataset_rows_partial(tmp_path: Path) -> None:
    manifest_path = _seed_dataset_repo(tmp_path)
    source_path = (
        tmp_path
        / "003_Canonical-Knowledge-Layer"
        / "shared"
        / "sources"
        / "ra-9514.md"
    )
    _write(
        source_path,
        (
            "---\n"
            "id: irr-fire-code\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n\n# body\n"
        ),
    )

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["canonical_input_manifest"]["sources"].append(
        {
            "path": "003_Canonical-Knowledge-Layer/shared/sources/ra-9514.md",
            "folder_name": "RA-9514",
            "entry_role": "authoritative",
            "authority_tier": "primary",
            "variant_family": "ra-9514-law",
            "edition_or_source_note": "Selected scoped canonical law source",
            "include_in_m1": True,
            "reason": "Current truth-bearing source input",
        }
    )
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    result = _run_cli(["build-graph", "--dataset-manifest", str(manifest_path)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr

    payload = json.loads(result.stdout)
    report = json.loads((tmp_path / payload["build_report_path"]).read_text(encoding="utf-8"))
    folder_rows = {row["folder_name"]: row for row in report["coverage"]}
    assert report["incomplete"] is True
    assert folder_rows["RA-9514"]["status"] == "partial"
    assert folder_rows["RA-9514"]["node_count_contributed"] == 1
    assert folder_rows["RA-9514"]["edge_count_contributed"] == 0


def test_query_structured_with_explicit_dataset_snapshot_shows_provenance(tmp_path: Path) -> None:
    manifest_path = _seed_dataset_repo(tmp_path)
    build = _run_cli(["build-graph", "--dataset-manifest", str(manifest_path)], cwd=tmp_path)
    assert build.returncode == 0, build.stderr
    payload = json.loads(build.stdout)

    result = _run_cli(
        [
            "query-structured",
            "--snapshot", payload["snapshot_path"],
            "--function", "what_governs",
            "--subject", "concept-building-permit",
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert "Snapshot provenance:" in result.stdout
    assert "dataset_id: laws-core-bundle-m1" in result.stdout
    assert "manifest_hash:" in result.stdout
    assert "law-pd-1096" in result.stdout


def test_export_graph_owl_accepts_explicit_snapshot_and_output_path(tmp_path: Path) -> None:
    manifest_path = _seed_dataset_repo(tmp_path)
    build = _run_cli(["build-graph", "--dataset-manifest", str(manifest_path)], cwd=tmp_path)
    assert build.returncode == 0, build.stderr
    payload = json.loads(build.stdout)

    out_path = tmp_path / "005_Operational-Intelligence-Layer" / "graph" / "datasets" / "laws-core-bundle-m1" / "custom.ttl"
    result = _run_cli(
        [
            "export-graph-owl",
            "--snapshot", payload["snapshot_path"],
            "--out", str(out_path.relative_to(tmp_path)),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert out_path.exists()
    assert "@prefix" in out_path.read_text(encoding="utf-8")
