from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

CLI = Path(__file__).resolve().parent.parent / 'pipeline_cli.py'


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, 'PYTHONPATH': 'scripts'}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def _seed_repo(root: Path) -> Path:
    raw = root / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1096'
    raw.mkdir(parents=True, exist_ok=True)
    (raw / 'stub.pdf').write_bytes(b'%PDF-1.4\n')

    shared = root / '003_Canonical-Knowledge-Layer' / 'shared'
    _write(shared / 'sources' / 'law.md', (
        '---\n'
        'id: law-pd-1096\n'
        'trust_level: primary\n'
        'last_canonicalized_utc: 2026-04-01T00:00:00Z\n'
        '---\n\n# body\n'
    ))
    _write(shared / 'concepts' / 'building-permit.md', (
        '---\n'
        'id: concept-building-permit\n'
        'canonical_status: enriched\n'
        'concept_status: enriched\n'
        'last_canonicalized_utc: 2026-04-01T00:00:00Z\n'
        'enriched_at_utc: 2026-04-01T00:00:00Z\n'
        'regulatory_basis:\n'
        '- source_id: law-pd-1096\n'
        '  section_id: sec-301\n'
        '  evidence_snippet: permit\n'
        '---\n\n# body\n'
    ))
    _write(shared / 'relationships' / 'r.md', (
        '---\n'
        'id: rel-pd-1096-governs-building-permit\n'
        'page_type: relationship\n'
        'relationship_type: governs\n'
        'from_entity: law-pd-1096\n'
        'to_entity: concept-building-permit\n'
        'canonical_status: promoted\n'
        'evidence:\n'
        '- source_id: law-pd-1096\n'
        '  source_section_id: sec-301\n'
        '  evidence_snippet: permit\n'
        '  reviewer_confidence: 0.95\n'
        '---\n\n# body\n'
    ))

    manifest = {
        'dataset_id': 'demo-dataset',
        'dataset_kind': 'demo',
        'raw_slice_anchors': [
            {
                'folder_name': 'PD-1096',
                'raw_root': '001_Raw-Source-Layer/001-Laws/PD-1096',
                'entry_role': 'authoritative',
                'authority_tier': 'primary',
                'variant_family': 'demo',
                'edition_or_source_note': 'demo',
                'include_in_m1': True,
                'reason': 'demo',
                'classified_raw_entries': [],
            }
        ],
        'canonical_input_manifest': {
            'sources': [
                {
                    'path': '003_Canonical-Knowledge-Layer/shared/sources/law.md',
                    'folder_name': 'PD-1096',
                    'entry_role': 'authoritative',
                    'authority_tier': 'primary',
                    'variant_family': 'demo',
                    'edition_or_source_note': 'demo',
                    'include_in_m1': True,
                    'reason': 'demo',
                }
            ],
            'concepts': [
                {
                    'path': '003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md',
                    'folder_name': 'PD-1096',
                    'entry_role': 'derived',
                    'authority_tier': 'derived',
                    'variant_family': 'demo',
                    'edition_or_source_note': 'demo',
                    'include_in_m1': True,
                    'reason': 'demo',
                }
            ],
        },
        'relationship_input_manifest': {
            'relationships': [
                {
                    'path': '003_Canonical-Knowledge-Layer/shared/relationships/r.md',
                    'folder_name': 'PD-1096',
                    'entry_role': 'authoritative',
                    'authority_tier': 'approved',
                    'variant_family': 'demo',
                    'edition_or_source_note': 'demo',
                    'include_in_m1': True,
                    'reason': 'demo',
                }
            ]
        },
        'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/demo-dataset',
        'run_output_root': '006_System-Manifests/runs/datasets/demo-dataset',
        'query_snapshot_path_template': '005_Operational-Intelligence-Layer/graph/datasets/demo-dataset/{run_id}_graph_snapshot.json',
        'freshness_policy': {'mode': 'exact'},
        'pilot_gate': {'require_manifest_validation': True},
    }
    manifest_path = root / 'config' / 'datasets' / 'demo.yaml'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding='utf-8')
    return manifest_path


def test_run_dataset_graph_writes_pipeline_report_and_keeps_global_latest_absent(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    result = _run_cli(
        [
            'run-dataset-graph',
            '--dataset-manifest', str(manifest_path),
            '--structured-check', 'what_governs:concept-building-permit',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    pipeline_report = tmp_path / payload['pipeline_report_path']
    assert pipeline_report.exists()
    report = json.loads(pipeline_report.read_text(encoding='utf-8'))
    assert report['dataset_id'] == 'demo-dataset'
    assert report['structured_checks'][0]['rc'] == 0
    assert (tmp_path / payload['snapshot_path']).exists()
    assert (tmp_path / payload['owl_path']).exists()
    assert not (tmp_path / '005_Operational-Intelligence-Layer' / 'graph' / 'latest_graph_snapshot.json').exists()
