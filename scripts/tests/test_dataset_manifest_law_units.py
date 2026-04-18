from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from vitruvius.graph.dataset_manifest import (
    DatasetManifestError,
    build_run_paths,
    load_dataset_manifest,
    snapshot_metadata,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_repo(root: Path) -> Path:
    raw = root / "001_Raw-Source-Layer" / "001-Laws" / "PD-1096"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "stub.pdf").write_bytes(b"%PDF-1.4\n")

    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    _write(
        shared / "sources" / "law.md",
        (
            "---\n"
            "id: law-pd-1096\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n\n# body\n"
        ),
    )
    _write(
        shared / "concepts" / "building-permit.md",
        (
            "---\n"
            "id: concept-building-permit\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n\n# body\n"
        ),
    )
    _write(
        shared / "relationships" / "r.md",
        (
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
            "  evidence_snippet: permit\n"
            "  reviewer_confidence: 0.95\n"
            "---\n\n# body\n"
        ),
    )

    manifest = {
        "dataset_id": "demo-dataset",
        "dataset_kind": "demo",
        "raw_slice_anchors": [
            {
                "folder_name": "PD-1096",
                "raw_root": "001_Raw-Source-Layer/001-Laws/PD-1096",
                "entry_role": "authoritative",
                "authority_tier": "primary",
                "variant_family": "demo",
                "edition_or_source_note": "demo",
                "include_in_m1": True,
                "reason": "demo",
                "classified_raw_entries": [
                    {
                        "path": "001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf",
                        "folder_name": "PD-1096",
                        "entry_role": "authoritative",
                        "authority_tier": "primary",
                        "variant_family": "demo",
                        "edition_or_source_note": "demo",
                        "include_in_m1": True,
                        "reason": "demo",
                    }
                ],
            }
        ],
        "canonical_input_manifest": {
            "sources": [
                {
                    "path": "003_Canonical-Knowledge-Layer/shared/sources/law.md",
                    "folder_name": "PD-1096",
                    "entry_role": "authoritative",
                    "authority_tier": "primary",
                    "variant_family": "demo",
                    "edition_or_source_note": "demo",
                    "include_in_m1": True,
                    "reason": "demo",
                }
            ],
            "concepts": [
                {
                    "path": "003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md",
                    "folder_name": "PD-1096",
                    "entry_role": "derived",
                    "authority_tier": "derived",
                    "variant_family": "demo",
                    "edition_or_source_note": "demo",
                    "include_in_m1": True,
                    "reason": "demo",
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
                    "variant_family": "demo",
                    "edition_or_source_note": "demo",
                    "include_in_m1": True,
                    "reason": "demo",
                }
            ]
        },
        "graph_output_root": "005_Operational-Intelligence-Layer/graph/datasets/demo-dataset",
        "run_output_root": "006_System-Manifests/runs/datasets/demo-dataset",
        "query_snapshot_path_template": "005_Operational-Intelligence-Layer/graph/datasets/demo-dataset/{run_id}_graph_snapshot.json",
        "freshness_policy": {"mode": "exact"},
        "pilot_gate": {"require_manifest_validation": True},
        "law_units": [
            {
                "law_id": "pd-1096",
                "folder_name": "PD-1096",
                "raw_anchor_paths": [
                    "001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf",
                ],
                "authoritative_variant_paths": [
                    "001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf",
                ],
                "excluded_variant_paths": [],
                "admitted_source_paths": [
                    "003_Canonical-Knowledge-Layer/shared/sources/law.md",
                ],
                "admitted_concept_paths": [
                    "003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md",
                ],
                "admitted_relationship_paths": [
                    "003_Canonical-Knowledge-Layer/shared/relationships/r.md",
                ],
                "verification_checks": ["demo check"],
                "scope_notes": ["demo note"],
            }
        ],
    }
    manifest_path = root / "config" / "datasets" / "demo.yaml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return manifest_path


def test_load_dataset_manifest_supports_law_units_and_metadata(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    manifest = load_dataset_manifest(manifest_path, tmp_path)

    assert len(manifest.law_units) == 1
    law_unit = manifest.law_units[0]
    assert law_unit.law_id == "pd-1096"
    assert law_unit.folder_name == "PD-1096"
    assert law_unit.admitted_relationship_paths == (
        "003_Canonical-Knowledge-Layer/shared/relationships/r.md",
    )

    metadata = snapshot_metadata(
        manifest,
        repo_root=tmp_path,
        run_id="20260416T000000Z",
        snapshot_rel="005_Operational-Intelligence-Layer/graph/datasets/demo-dataset/x.json",
        integrity_rel="005_Operational-Intelligence-Layer/graph/datasets/demo-dataset/x_integrity.json",
    )
    assert metadata["contributing_law_ids"] == ["pd-1096"]
    assert metadata["law_units"][0]["law_id"] == "pd-1096"
    assert metadata["law_units"][0]["admitted_source_paths"] == [
        "003_Canonical-Knowledge-Layer/shared/sources/law.md"
    ]


def test_load_dataset_manifest_rejects_unselected_law_unit_paths(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["law_units"][0]["admitted_source_paths"] = [
        "003_Canonical-Knowledge-Layer/shared/sources/not-selected.md"
    ]
    _write(
        tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "sources" / "not-selected.md",
        (
            "---\n"
            "id: law-not-selected\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n\n# body\n"
        ),
    )
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    with pytest.raises(DatasetManifestError, match="references source path not selected"):
        load_dataset_manifest(manifest_path, tmp_path)


def test_build_run_paths_rejects_windows_unsafe_output_roots(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    manifest_payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest_payload["graph_output_root"] = "005_Operational-Intelligence-Layer/graph/datasets/demo:dataset"
    manifest_path.write_text(yaml.safe_dump(manifest_payload, sort_keys=False), encoding="utf-8")

    manifest = load_dataset_manifest(manifest_path, tmp_path)

    with pytest.raises(ValueError, match="Windows-forbidden filename characters"):
        build_run_paths(manifest, repo_root=tmp_path, run_id="20260416T000000Z")
