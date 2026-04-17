from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import yaml
from pypdf import PdfWriter

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


def _seed_conversion_inventory(root: Path, folder_name: str, stem: str) -> None:
    for rel_path, payload in (
        (
            root / '002_Raw-Conversion-Layer' / '001-Laws' / 'refined_markdown' / folder_name / f'{stem}.md',
            '---\nid: source-demo\n---\n\n# refined\n',
        ),
        (
            root / '002_Raw-Conversion-Layer' / '001-Laws' / 'raw_markdown' / folder_name / f'{stem}.md',
            '# raw\n',
        ),
        (
            root / '002_Raw-Conversion-Layer' / '001-Laws' / 'sidecar_json' / folder_name / f'{stem}.json',
            '{}\n',
        ),
    ):
        _write(rel_path, payload)


def _seed_conversion_inventory_path(root: Path, folder_name: str, filename: str, *, refined_payload: str | None = None) -> None:
    refined_text = refined_payload or '---\nid: source-demo\n---\n\n# refined\n'
    for rel_path, payload in (
        (
            root / '002_Raw-Conversion-Layer' / '001-Laws' / 'refined_markdown' / folder_name / f'{filename}.md',
            refined_text,
        ),
        (
            root / '002_Raw-Conversion-Layer' / '001-Laws' / 'raw_markdown' / folder_name / f'{filename}.md',
            '# raw\n',
        ),
        (
            root / '002_Raw-Conversion-Layer' / '001-Laws' / 'sidecar_json' / folder_name / f'{filename}.json',
            '{}\n',
        ),
    ):
        _write(rel_path, payload)


def _seed_refined_with_headers(root: Path, folder_name: str, stem: str, header_count: int) -> None:
    lines = [f"## Section {idx}. Example Heading" for idx in range(1, header_count + 1)]
    _write(
        root / '002_Raw-Conversion-Layer' / '001-Laws' / 'refined_markdown' / folder_name / f'{stem}.md',
        "\n".join(lines) + "\n",
    )


def _write_source_prep_report(root: Path, tranche_id: str, run_id: str, folders: list[dict]) -> Path:
    report_path = (
        root
        / '006_System-Manifests'
        / 'runs'
        / 'datasets'
        / tranche_id
        / run_id
        / 'laws_tranche_source_prep_report.json'
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(
            {
                'action': 'run-laws-tranche-source-prep',
                'run_id': run_id,
                'execute': True,
                'phase_11_gate': 'gated',
                'phase_11_generic_expansion_gated': True,
                'tranche_id': tranche_id,
                'prepared_count': sum(folder.get('prepared_count', 0) for folder in folders),
                'ocr_required_count': sum(folder.get('ocr_required_count', 0) for folder in folders),
                'failed_count': sum(folder.get('failed_count', 0) for folder in folders),
                'folders': folders,
            },
            indent=2,
        ),
        encoding='utf-8',
    )
    return report_path


def _write_valid_pdf(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with path.open('wb') as fp:
        writer.write(fp)


def _write_pdf_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


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
                'classified_raw_entries': [
                    {
                        'path': '001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf',
                        'folder_name': 'PD-1096',
                        'entry_role': 'authoritative',
                        'authority_tier': 'primary',
                        'variant_family': 'demo',
                        'edition_or_source_note': 'demo',
                        'include_in_m1': True,
                        'reason': 'demo',
                    }
                ],
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
                'classified_raw_entries': [
                    {
                        'path': '001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf',
                        'folder_name': 'PD-1096',
                        'entry_role': 'authoritative',
                        'authority_tier': 'primary',
                        'variant_family': 'demo',
                        'edition_or_source_note': 'demo',
                        'include_in_m1': True,
                        'reason': 'demo',
                    }
                ],
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
        'law_units': [
            {
                'law_id': 'pd-1096',
                'folder_name': 'PD-1096',
                'raw_anchor_paths': [
                    '001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf',
                ],
                'authoritative_variant_paths': [
                    '001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf',
                ],
                'excluded_variant_paths': [],
                'admitted_source_paths': [
                    '003_Canonical-Knowledge-Layer/shared/sources/law.md',
                ],
                'admitted_concept_paths': [
                    '003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md',
                ],
                'admitted_relationship_paths': [
                    '003_Canonical-Knowledge-Layer/shared/relationships/r.md',
                ],
                'verification_checks': ['demo scoped path remains covered'],
                'scope_notes': ['Demo law-unit repetition contract for M4 runtime support.'],
            }
        ],
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
    assert report['law_unit_count'] == 1
    assert report['contributing_law_ids'] == ['pd-1096']
    assert report['structured_checks'][0]['rc'] == 0
    assert (tmp_path / payload['snapshot_path']).exists()
    assert (tmp_path / payload['owl_path']).exists()
    assert not (tmp_path / '005_Operational-Intelligence-Layer' / 'graph' / 'latest_graph_snapshot.json').exists()


def test_run_dataset_graph_rejects_malformed_structured_check_cleanly(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    result = _run_cli(
        [
            'run-dataset-graph',
            '--dataset-manifest', str(manifest_path),
            '--structured-check', 'badformat',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert 'FUNCTION:SUBJECT' in payload['error']
    assert result.stderr == ''


def test_run_dataset_source_to_graph_rejects_visualize_during_dry_run(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    result = _run_cli(
        [
            'run-dataset-source-to-graph',
            '--dataset-manifest', str(manifest_path),
            '--dry-run',
            '--visualize',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert '--visualize / --open-browser' in payload['error']


def test_run_laws_pilot_dry_run_uses_bounded_manifest(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    result = _run_cli(
        [
            'run-laws-pilot',
            '--dry-run',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-dataset-source-to-graph'
    assert payload['dataset_id'] == 'demo-dataset'
    assert payload['dry_run'] is True


def test_run_laws_pilot_dry_run_applies_8gb_review_preset(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    result = _run_cli(
        [
            'run-laws-pilot',
            '--dry-run',
            '--review-preset', 'm2-8gb-safe',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['review_runtime']['model'] == 'qwen2.5:7b'
    assert payload['review_runtime']['parallelism'] == 1
    assert payload['review_runtime']['preset']['name'] == 'm2-8gb-safe'


def test_run_laws_pilot_dry_run_rejects_open_browser(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    result = _run_cli(
        [
            'run-laws-pilot',
            '--dry-run',
            '--open-browser',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert '--visualize / --open-browser' in payload['error']


def test_run_laws_pilot_emits_progress_when_enabled(tmp_path: Path, monkeypatch) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    monkeypatch.setenv('VITRUVIUS_CLI_PROGRESS', '1')
    result = _run_cli(
        [
            'run-laws-pilot',
            '--dry-run',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert '[vitruvius] Loaded dataset manifest demo-dataset from config/datasets/laws-core-bundle-m1.yaml' in result.stderr


def test_run_laws_all_dry_run_reports_inventory_and_gate(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    extra_folder = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'BP-220'
    extra_folder.mkdir(parents=True, exist_ok=True)
    duplicate_bytes = b'%PDF-1.4\nshared duplicate\n'
    _write_pdf_bytes(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1096' / 'stub.pdf', duplicate_bytes)
    _write_pdf_bytes(extra_folder / 'bp220.pdf', duplicate_bytes)

    result = _run_cli(
        [
            'run-laws-all-dry-run',
            '--review-preset', 'm2-8gb-safe',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-all-dry-run'
    assert payload['dry_run'] is True
    assert payload['phase_11_gate'] == 'gated'
    assert payload['raw_law_folder_count'] == 2
    assert payload['raw_pdf_count'] == 2
    assert payload['bounded_manifest_law_unit_count'] == 1
    assert payload['review_runtime']['preset']['name'] == 'm2-8gb-safe'
    assert payload['duplicate_cluster_count'] == 1
    assert payload['duplicate_law_folders'] == ['BP-220', 'PD-1096']
    report_path = tmp_path / payload['report_path']
    assert report_path.exists()


def test_run_laws_all_dry_run_flags_structure_concept_guardrail(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    _seed_refined_with_headers(tmp_path, 'PD-1096', 'deep-structure', 25)

    result = _run_cli(
        [
            'run-laws-all-dry-run',
            '--review-preset', 'm2-8gb-safe',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert 'PD-1096' in payload['structure_guardrail_law_folders']
    report_path = tmp_path / payload['report_path']
    report = json.loads(report_path.read_text(encoding='utf-8'))
    law = next(item for item in report['laws'] if item['folder_name'] == 'PD-1096')
    assert law['structural_header_count'] >= 25
    assert 'rich_structure_low_concept_admission' in law['structure_guardrails']


def test_run_laws_tranche_dry_run_reports_candidate_inventory_and_guardrails(tmp_path: Path) -> None:
    manifest_path = _seed_repo(tmp_path)
    laws_manifest = tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml'
    laws_manifest.write_text(manifest_path.read_text(encoding='utf-8'), encoding='utf-8')
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'candidate_law_folders': [
                    {'folder_name': 'PD-957', 'reason': 'housing adjacency'},
                    {'folder_name': 'PD-1096', 'reason': 'pilot overlap for control'},
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    pd957 = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957'
    pd957.mkdir(parents=True, exist_ok=True)
    duplicate_bytes = b'%PDF-1.4\nshared duplicate\n'
    _write_pdf_bytes(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1096' / 'stub.pdf', duplicate_bytes)
    _write_pdf_bytes(pd957 / 'pd957.pdf', duplicate_bytes)
    _seed_refined_with_headers(tmp_path, 'PD-1096', 'deep-structure', 25)

    result = _run_cli(
        [
            'run-laws-tranche-dry-run',
            '--tranche-manifest', str(tranche_manifest),
            '--review-preset', 'm2-8gb-safe',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-tranche-dry-run'
    assert payload['tranche_id'] == 'laws-tranche-1'
    assert payload['candidate_law_folder_count'] == 2
    assert payload['pilot_covered_law_count'] == 1
    assert payload['inventory_only_law_count'] == 1
    assert payload['review_runtime']['preset']['name'] == 'm2-8gb-safe'
    assert 'PD-1096' in payload['structure_guardrail_law_folders']
    assert payload['duplicate_cluster_count'] == 1
    assert payload['duplicate_law_folders'] == ['PD-1096', 'PD-957']
    report_path = tmp_path / payload['report_path']
    assert report_path.exists()


def test_run_laws_duplicate_dry_run_reports_exact_clusters(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    extra_folder = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'BP-220'
    extra_folder.mkdir(parents=True, exist_ok=True)
    duplicate_bytes = b'%PDF-1.4\nsame document\n'
    _write_pdf_bytes(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1096' / 'stub.pdf', duplicate_bytes)
    _write_pdf_bytes(extra_folder / 'bp220-law.pdf', duplicate_bytes)

    result = _run_cli(
        [
            'run-laws-duplicate-dry-run',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-duplicate-dry-run'
    assert payload['duplicate_cluster_count'] == 1
    assert payload['duplicate_law_folders'] == ['BP-220', 'PD-1096']
    report = json.loads((tmp_path / payload['report_path']).read_text(encoding='utf-8'))
    cluster = report['duplicate_clusters'][0]
    assert cluster['law_folders'] == ['BP-220', 'PD-1096']
    assert len(cluster['raw_paths']) == 2


def test_run_laws_duplicate_dry_run_respects_manifest_scoped_variants(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    lgu = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'LGU'
    lgu.mkdir(parents=True, exist_ok=True)
    _write_pdf_bytes(lgu / 'target-zoning.pdf', b'%PDF-1.4\nzoning\n')
    _write_pdf_bytes(lgu / 'target-clup.pdf', b'%PDF-1.4\nclup\n')
    duplicate_bytes = b'%PDF-1.4\nsame duplicate elsewhere in folder\n'
    _write_pdf_bytes(lgu / 'unrelated-duplicate-a.pdf', duplicate_bytes)
    _write_pdf_bytes(lgu / 'unrelated-duplicate-b.pdf', duplicate_bytes)

    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-lgu.yaml'
    tranche_manifest.parent.mkdir(parents=True, exist_ok=True)
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-lgu',
                'candidate_law_folders': [
                    {
                        'folder_name': 'LGU',
                        'reason': 'scoped shard',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/LGU/target-zoning.pdf',
                            '001_Raw-Source-Layer/001-Laws/LGU/target-clup.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/LGU/target-zoning.pdf',
                            '001_Raw-Source-Layer/001-Laws/LGU/target-clup.pdf',
                        ],
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    result = _run_cli(
        [
            'run-laws-duplicate-dry-run',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['duplicate_cluster_count'] == 0
    assert payload['duplicate_law_folders'] == []


def test_run_laws_tranche_dry_run_respects_manifest_scoped_variants_for_duplicates(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    lgu = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'LGU'
    lgu.mkdir(parents=True, exist_ok=True)
    _write_pdf_bytes(lgu / 'target-zoning.pdf', b'%PDF-1.4\nzoning\n')
    _write_pdf_bytes(lgu / 'target-clup.pdf', b'%PDF-1.4\nclup\n')
    duplicate_bytes = b'%PDF-1.4\nsame duplicate elsewhere in folder\n'
    _write_pdf_bytes(lgu / 'unrelated-duplicate-a.pdf', duplicate_bytes)
    _write_pdf_bytes(lgu / 'unrelated-duplicate-b.pdf', duplicate_bytes)

    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-lgu.yaml'
    tranche_manifest.parent.mkdir(parents=True, exist_ok=True)
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-lgu',
                'candidate_law_folders': [
                    {
                        'folder_name': 'LGU',
                        'reason': 'scoped shard',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/LGU/target-zoning.pdf',
                            '001_Raw-Source-Layer/001-Laws/LGU/target-clup.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/LGU/target-zoning.pdf',
                            '001_Raw-Source-Layer/001-Laws/LGU/target-clup.pdf',
                        ],
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    result = _run_cli(
        [
            'run-laws-tranche-dry-run',
            '--tranche-manifest', str(tranche_manifest),
            '--review-preset', 'm2-8gb-safe',
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['duplicate_cluster_count'] == 0
    assert payload['duplicate_law_folders'] == []


def test_run_laws_tranche_source_prep_dry_run_reports_expected_outputs(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'candidate_law_folders': [
                    {'folder_name': 'PD-957', 'reason': 'housing adjacency'},
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    pdf_path = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'pd957.pdf'
    _write_valid_pdf(pdf_path)

    result = _run_cli(
        [
            'run-laws-tranche-source-prep-dry-run',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-tranche-source-prep-dry-run'
    assert payload['candidate_law_folder_count'] == 1
    assert payload['raw_file_count'] == 1
    assert payload['supported_direct_input_count'] == 1
    report_path = tmp_path / payload['report_path']
    report = json.loads(report_path.read_text(encoding='utf-8'))
    folder = report['folders'][0]
    assert folder['folder_name'] == 'PD-957'
    assert folder['raw_file_count'] == 1
    file_report = folder['file_reports'][0]
    assert file_report['raw_path'].endswith('PD-957/pd957.pdf')
    assert file_report['supported_direct_input'] is True
    assert file_report['expected_raw_markdown_path'].endswith('002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-957/pd957.md')
    assert file_report['expected_sidecar_json_path'].endswith('002_Raw-Conversion-Layer/001-Laws/sidecar_json/PD-957/pd957.json')
    assert file_report['expected_refined_markdown_path'].endswith('002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/pd957.md')


def test_run_laws_tranche_source_prep_respects_manifest_variant_scope(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-7.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-7',
                'candidate_law_folders': [
                    {
                        'folder_name': 'RA-1378',
                        'reason': 'plumbing law adjacency',
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/RA-1378/MASTER PLUMBING LAW.pdf',
                        ],
                        'excluded_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/RA-1378/Board of Master Plumber.doc',
                            '001_Raw-Source-Layer/001-Laws/RA-1378/Board of Master Plumber.pdf',
                        ],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'MASTER PLUMBING LAW.pdf')
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'Board of Master Plumber.pdf')
    _write(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'Board of Master Plumber.doc', 'legacy doc')

    result = _run_cli(
        [
            'run-laws-tranche-source-prep-dry-run',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    report = json.loads((tmp_path / payload['report_path']).read_text(encoding='utf-8'))
    folder = report['folders'][0]
    assert folder['raw_file_count'] == 1
    assert [item['raw_path'] for item in folder['file_reports']] == [
        '001_Raw-Source-Layer/001-Laws/RA-1378/MASTER PLUMBING LAW.pdf'
    ]


def test_run_laws_tranche_source_prep_exec_respects_manifest_variant_scope(tmp_path: Path, monkeypatch, capsys) -> None:
    from vitruvius import laws_readiness as lr

    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-7.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-7',
                'candidate_law_folders': [
                    {
                        'folder_name': 'RA-1378',
                        'reason': 'plumbing law adjacency',
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/RA-1378/MASTER PLUMBING LAW.pdf',
                        ],
                        'excluded_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/RA-1378/188541488-Revised-National-Plumbing-Code-of-the-Philippines.pdf',
                            '001_Raw-Source-Layer/001-Laws/RA-1378/Board of Master Plumber.pdf',
                            '001_Raw-Source-Layer/001-Laws/RA-1378/Board of Master Plumber.doc',
                        ],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'MASTER PLUMBING LAW.pdf')
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / '188541488-Revised-National-Plumbing-Code-of-the-Philippines.pdf'
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'Board of Master Plumber.pdf')
    _write(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'Board of Master Plumber.doc', 'legacy doc')

    seen_paths: list[str] = []

    def fake_prepare_raw_file(*, repo_root: Path, file_path: Path, sample_pages: int, allow_ocr: bool) -> dict[str, object]:
        del sample_pages, allow_ocr
        raw_path = lr._relative(file_path, repo_root)
        seen_paths.append(raw_path)
        return {
            'raw_path': raw_path,
            'status': 'prepared',
            'supported_direct_input': True,
            'detection_result': 'TEXT_PDF',
            'recommended_route': 'OPENDATALOADER_DIRECT',
            'expected_raw_markdown_path': 'dummy/raw.md',
            'expected_sidecar_json_path': 'dummy/sidecar.json',
            'expected_refined_markdown_path': 'dummy/refined.md',
            'convert_output': '',
            'refine_output': '',
        }

    monkeypatch.setattr(lr, '_prepare_raw_file', fake_prepare_raw_file)
    monkeypatch.chdir(tmp_path)

    assert lr.run_laws_tranche_source_prep(tranche_manifest=str(tranche_manifest)) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload['raw_file_count'] == 1
    assert payload['prepared_count'] == 1
    assert payload['failed_count'] == 0
    assert seen_paths == ['001_Raw-Source-Layer/001-Laws/RA-1378/MASTER PLUMBING LAW.pdf']


def test_run_laws_tranche_source_prep_uses_raw_folder_name_override(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-12.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-12',
                'candidate_law_folders': [
                    {
                        'folder_name': 'DHSUD',
                        'raw_folder_name': 'HLURB-DHSUD',
                        'reason': 'dhsud guidance split',
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/HLURB-DHSUD/Open Space Development Guidelines.pdf',
                        ],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'HLURB-DHSUD' / 'Open Space Development Guidelines.pdf')

    result = _run_cli(
        [
            'run-laws-tranche-source-prep-dry-run',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    report = json.loads((tmp_path / payload['report_path']).read_text(encoding='utf-8'))
    folder = report['folders'][0]
    assert folder['folder_name'] == 'DHSUD'
    assert folder['raw_root_present'] is True
    assert folder['raw_file_count'] == 1
    assert folder['file_reports'][0]['raw_path'] == '001_Raw-Source-Layer/001-Laws/HLURB-DHSUD/Open Space Development Guidelines.pdf'


def test_build_laws_completed_aggregate_manifest_merges_completed_manifests(tmp_path: Path, monkeypatch) -> None:
    from vitruvius import laws_readiness as lr

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)

    core_manifest = {
        'dataset_id': 'laws-core-bundle-m1',
        'dataset_kind': 'laws-core-bundle',
        'scope_notes': ['core'],
        'raw_slice_anchors': [
            {
                'folder_name': 'PD-1096',
                'raw_root': '001_Raw-Source-Layer/001-Laws/PD-1096',
                'entry_role': 'authoritative',
                'authority_tier': 'primary',
                'variant_family': 'core',
                'edition_or_source_note': 'core',
                'include_in_m1': True,
                'reason': 'core lane',
                'classified_raw_entries': [
                    {
                        'path': '001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf',
                        'folder_name': 'PD-1096',
                        'entry_role': 'authoritative',
                        'authority_tier': 'primary',
                        'variant_family': 'core',
                        'edition_or_source_note': 'core',
                        'include_in_m1': True,
                        'reason': 'core lane',
                    }
                ],
            }
        ],
        'canonical_input_manifest': {
            'sources': [
                {
                    'path': '003_Canonical-Knowledge-Layer/shared/sources/law.md',
                    'folder_name': 'PD-1096',
                    'entry_role': 'authoritative',
                    'authority_tier': 'primary',
                    'variant_family': 'core',
                    'edition_or_source_note': 'core',
                    'include_in_m1': True,
                    'reason': 'core lane',
                }
            ],
            'concepts': [
                {
                    'path': '003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md',
                    'folder_name': 'PD-1096',
                    'entry_role': 'derived',
                    'authority_tier': 'derived',
                    'variant_family': 'core',
                    'edition_or_source_note': 'core',
                    'include_in_m1': True,
                    'reason': 'core lane',
                }
            ],
        },
        'relationship_input_manifest': {
            'relationships': [
                {
                    'path': '003_Canonical-Knowledge-Layer/shared/relationships/rel-law-governs-concept-building-permit.md',
                    'folder_name': 'PD-1096',
                    'entry_role': 'authoritative',
                    'authority_tier': 'approved',
                    'variant_family': 'core',
                    'edition_or_source_note': 'core',
                    'include_in_m1': True,
                    'reason': 'core lane',
                }
            ]
        },
        'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1',
        'run_output_root': '006_System-Manifests/runs/datasets/laws-core-bundle-m1',
        'query_snapshot_path_template': '005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/{run_id}_graph_snapshot.json',
        'freshness_policy': {'mode': 'exact'},
        'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
        'law_units': [
            {
                'law_id': 'pd-1096',
                'folder_name': 'PD-1096',
                'raw_anchor_paths': ['001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf'],
                'refined_markdown_paths': [],
                'authoritative_variant_paths': ['001_Raw-Source-Layer/001-Laws/PD-1096/stub.pdf'],
                'excluded_variant_paths': [],
                'admitted_source_paths': ['003_Canonical-Knowledge-Layer/shared/sources/law.md'],
                'admitted_concept_paths': ['003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md'],
                'admitted_relationship_paths': ['003_Canonical-Knowledge-Layer/shared/relationships/rel-law-governs-concept-building-permit.md'],
                'verification_checks': [],
                'scope_notes': [],
            }
        ],
    }
    (tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml').write_text(
        yaml.safe_dump(core_manifest, sort_keys=False),
        encoding='utf-8',
    )

    tranche_manifest = {
        'tranche_id': 'laws-tranche-12',
        'candidate_law_folders': [
            {
                'folder_name': 'DHSUD',
                'raw_folder_name': 'HLURB-DHSUD',
                'reason': 'dhsud guidance',
                'raw_anchor_paths': ['001_Raw-Source-Layer/001-Laws/HLURB-DHSUD/Open Space Development Guidelines.pdf'],
                'authoritative_variant_paths': ['001_Raw-Source-Layer/001-Laws/HLURB-DHSUD/Open Space Development Guidelines.pdf'],
                'excluded_variant_paths': [],
                'refined_markdown_paths': ['002_Raw-Conversion-Layer/001-Laws/refined_markdown/HLURB-DHSUD/Open Space Development Guidelines.md'],
                'admitted_source_paths': ['003_Canonical-Knowledge-Layer/shared/sources/law.md'],
                'admitted_concept_paths': ['003_Canonical-Knowledge-Layer/shared/concepts/building-permit.md'],
                'admitted_relationship_paths': ['003_Canonical-Knowledge-Layer/shared/relationships/rel-law-governs-concept-building-permit.md'],
                'verification_checks': ['ok'],
                'scope_notes': ['dhsud'],
            }
        ],
    }
    (tmp_path / 'config' / 'datasets' / 'laws-tranche-12.yaml').write_text(
        yaml.safe_dump(tranche_manifest, sort_keys=False),
        encoding='utf-8',
    )

    (tmp_path / 'config' / 'datasets' / 'laws-completed-lanes.yaml').write_text(
        yaml.safe_dump(
            {
                'completed_lanes': [
                    {'lane_id': 'laws-core-bundle-pilot'},
                    {'lane_id': 'laws-tranche-12'},
                ]
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'laws-manifest-index.yaml').write_text(
        yaml.safe_dump(
            {
                'manifests': [
                    {'lane_id': 'laws-core-bundle-pilot', 'manifest': 'config/datasets/laws-core-bundle-m1.yaml'},
                    {'lane_id': 'laws-tranche-12', 'manifest': 'config/datasets/laws-tranche-12.yaml'},
                ]
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    monkeypatch.chdir(tmp_path)
    rc = lr.build_laws_completed_aggregate_manifest()
    assert rc == 0
    payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'laws-completed-aggregate.yaml').read_text(encoding='utf-8'))
    assert payload['dataset_id'] == 'laws-completed-aggregate'
    assert len(payload['law_units']) == 2
    assert any(unit['folder_name'] == 'HLURB-DHSUD' for unit in payload['law_units'])


def test_run_laws_completed_aggregate_invokes_dataset_pipeline(tmp_path: Path, monkeypatch) -> None:
    from vitruvius import laws_readiness as lr

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'laws-core-bundle-m1.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'laws-core-bundle-m1',
                'dataset_kind': 'laws-core-bundle',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1',
                'run_output_root': '006_System-Manifests/runs/datasets/laws-core-bundle-m1',
                'query_snapshot_path_template': 'x/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'laws-completed-lanes.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'laws-core-bundle-pilot'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'laws-manifest-index.yaml').write_text(
        yaml.safe_dump({'manifests': [{'lane_id': 'laws-core-bundle-pilot', 'manifest': 'config/datasets/laws-core-bundle-m1.yaml'}]}, sort_keys=False),
        encoding='utf-8',
    )

    seen: dict[str, object] = {}

    def fake_run_dataset_source_to_graph_pipeline(**kwargs):
        seen.update(kwargs)
        return 0

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('vitruvius.dataset_pipeline.run_dataset_source_to_graph_pipeline', fake_run_dataset_source_to_graph_pipeline)
    rc = lr.run_laws_completed_aggregate(dry_run=True, review_preset='m2-8gb-safe')
    assert rc == 0
    assert seen['dataset_manifest'] == 'config/datasets/laws-completed-aggregate.yaml'
    assert seen['dry_run'] is True
    assert seen['review_preset'] == 'm2-8gb-safe'


def test_run_laws_tranche_source_prep_handles_ocr_required_pdf(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'candidate_law_folders': [
                    {'folder_name': 'PD-957', 'reason': 'housing adjacency'},
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    pdf_path = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'pd957.pdf'
    _write_valid_pdf(pdf_path)

    result = _run_cli(
        [
            'run-laws-tranche-source-prep',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-tranche-source-prep'
    assert payload['raw_file_count'] == 1
    assert payload['supported_direct_input_count'] == 1
    assert payload['ocr_required_count'] == 1
    assert payload['prepared_count'] == 0


def test_prepare_raw_file_allow_ocr_runs_ocr_then_convert_and_refine(tmp_path: Path, monkeypatch) -> None:
    from vitruvius import laws_readiness as lr

    raw_pdf = tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1216' / 'pd1216.pdf'
    _write_valid_pdf(raw_pdf)

    monkeypatch.setattr(
        lr,
        'detect_pdf_type',
        lambda path, sample_pages=5: {
            'result': 'LIKELY_SCANNED_PDF',
            'recommended_route': 'OCR_FIRST_THEN_OPENDATALOADER',
        },
    )

    def fake_ocr(input_path: str, output_path: str, **kwargs) -> None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(b'%PDF-1.4\n%ocr output\n')

    monkeypatch.setitem(sys.modules, 'ocrmypdf', SimpleNamespace(ocr=fake_ocr))

    def fake_convert_pdf_at_path(pdf_path: Path, logical_relative_source_path: str, **kwargs):
        markdown_rel, json_rel = lr.build_conversion_relative_paths(logical_relative_source_path)
        _write(tmp_path / '002_Raw-Conversion-Layer' / markdown_rel, '# raw from ocr\n')
        _write(tmp_path / '002_Raw-Conversion-Layer' / json_rel, '{}\n')
        return {
            'markdown_output_relative': markdown_rel.as_posix(),
            'json_output_relative': json_rel.as_posix(),
        }

    monkeypatch.setattr(lr, 'convert_pdf_at_path', fake_convert_pdf_at_path)

    def fake_refine_one(*, relative_markdown_path: str) -> int:
        refined_rel = lr._refined_markdown_relative_path(Path(relative_markdown_path))
        _write(tmp_path / '002_Raw-Conversion-Layer' / refined_rel, '# refined from ocr\n')
        return 0

    monkeypatch.setattr(lr, 'run_refine_one', fake_refine_one)

    result = lr._prepare_raw_file(
        repo_root=tmp_path,
        file_path=raw_pdf,
        sample_pages=5,
        allow_ocr=True,
    )
    assert result['status'] == 'prepared'
    assert result['recommended_route'] == 'OCR_FIRST_THEN_OPENDATALOADER'
    assert result['expected_ocr_pdf_path'].endswith('002_Raw-Conversion-Layer/001-Laws/ocr_pdf/PD-1216/pd1216.pdf')
    assert (tmp_path / result['expected_ocr_pdf_path']).exists()
    assert (tmp_path / result['expected_raw_markdown_path']).exists()
    assert (tmp_path / result['expected_refined_markdown_path']).exists()


def test_run_laws_tranche_source_admission_dry_run_reports_ready_vs_blocked_split(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'candidate_law_folders': [
                    {'folder_name': 'PD-957', 'reason': 'housing adjacency'},
                    {'folder_name': 'PD-1216', 'reason': 'open-space adjacency'},
                    {'folder_name': 'PD-1185', 'reason': 'fire adjacency'},
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _seed_conversion_inventory_path(
        tmp_path,
        'PD-957',
        'PD 957 IRR - Subdivision and Condominium IRR',
        refined_payload='# REVISED IMPLEMENTING RULES AND REGULATIONS FOR PD 957\n',
    )
    _seed_conversion_inventory_path(
        tmp_path,
        'PD-1185',
        'PD 1185 - Fire Code of the Philippines 1977',
        refined_payload='# FIRE CODE OF THE PHILIPPINES\n',
    )
    source_prep_report = _write_source_prep_report(
        tmp_path,
        'laws-tranche-1',
        '20260417T022819Z',
        [
            {
                'folder_name': 'PD-957',
                'prepared_count': 1,
                'ocr_required_count': 0,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md',
                    }
                ],
            },
            {
                'folder_name': 'PD-1216',
                'prepared_count': 0,
                'ocr_required_count': 1,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'ocr_required',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-1216/pd1216.pdf',
                        'recommended_route': 'OCR_FIRST_THEN_OPENDATALOADER',
                    }
                ],
            },
            {
                'folder_name': 'PD-1185',
                'prepared_count': 1,
                'ocr_required_count': 0,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-1185/PD 1185 - Fire Code of the Philippines 1977.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1185/PD 1185 - Fire Code of the Philippines 1977.md',
                    }
                ],
            },
        ],
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 IRR - Subdivision and Condominium IRR.pdf'
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1185' / 'PD 1185 - Fire Code of the Philippines 1977.pdf'
    )

    result = _run_cli(
        [
            'run-laws-tranche-source-admission-dry-run',
            '--tranche-manifest', str(tranche_manifest),
            '--source-prep-report', str(source_prep_report),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-tranche-source-admission-dry-run'
    assert payload['admission_review_ready_law_folders'] == ['PD-957', 'PD-1185']
    assert payload['blocked_law_folders'] == ['PD-1216']
    assert payload['source_to_graph_execute_ready'] is False
    assert payload['candidate_source_page_count'] == 2
    report_path = tmp_path / payload['report_path']
    report = json.loads(report_path.read_text(encoding='utf-8'))
    ready_law = next(item for item in report['laws'] if item['folder_name'] == 'PD-957')
    assert ready_law['status'] == 'ready_for_admission_review'
    assert ready_law['candidate_source_page_count'] == 1
    assert ready_law['candidate_source_pages'][0]['canonical_source_path'].endswith(
        '003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md'
    )
    blocked_law = next(item for item in report['laws'] if item['folder_name'] == 'PD-1216')
    assert blocked_law['status'] == 'blocked_pending_ocr'
    assert blocked_law['blocked_file_reports'][0]['recommended_route'] == 'OCR_FIRST_THEN_OPENDATALOADER'


def test_run_laws_tranche_source_admission_exec_collapses_duplicate_pd957_variants_and_keeps_blocked_laws(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'candidate_law_folders': [
                    {'folder_name': 'PD-957', 'reason': 'housing adjacency'},
                    {'folder_name': 'PD-1216', 'reason': 'open-space adjacency'},
                    {'folder_name': 'PD-1185', 'reason': 'fire adjacency'},
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    duplicate_pdf_bytes = b'%PDF-1.4\\n% identical pd957 bytes\\n'
    _write_pdf_bytes(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 - Subdivision _ Condominium Buyer_s Act.pdf',
        duplicate_pdf_bytes,
    )
    _write_pdf_bytes(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf',
        duplicate_pdf_bytes,
    )
    _write_pdf_bytes(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 IRR - Subdivision and Condominium IRR.pdf',
        duplicate_pdf_bytes,
    )
    _write_pdf_bytes(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 - Subdivision Law Illustrated Slides (Pedro Santos Jr).pdf',
        b'%PDF-1.4\\n% slide deck bytes\\n',
    )
    _write_pdf_bytes(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1185' / 'PD 1185 - Fire Code of the Philippines 1977.pdf',
        b'%PDF-1.4\\n% fire code bytes\\n',
    )

    for filename in (
        'PD 957 - Subdivision _ Condominium Buyer_s Act',
        'PD 957 - Subdivision and Condominium Buyers Protective Decree',
        'PD 957 IRR - Subdivision and Condominium IRR',
        'PD 957 - Subdivision Law Illustrated Slides (Pedro Santos Jr)',
    ):
        refined_payload = (
            '# REVISED IMPLEMENTING RULES AND REGULATIONS FOR PD 957\\n'
            if 'Illustrated Slides' not in filename
            else '# PRESIDENTIAL DECREE 957\\n\\nStudy slides\\n'
        )
        _seed_conversion_inventory_path(tmp_path, 'PD-957', filename, refined_payload=refined_payload)
    _seed_conversion_inventory_path(
        tmp_path,
        'PD-1185',
        'PD 1185 - Fire Code of the Philippines 1977',
        refined_payload='# FIRE CODE OF THE PHILIPPINES\\n',
    )

    source_prep_report = _write_source_prep_report(
        tmp_path,
        'laws-tranche-1',
        '20260417T022819Z',
        [
            {
                'folder_name': 'PD-957',
                'prepared_count': 4,
                'ocr_required_count': 0,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision _ Condominium Buyer_s Act.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 - Subdivision _ Condominium Buyer_s Act.md',
                    },
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 - Subdivision and Condominium Buyers Protective Decree.md',
                    },
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md',
                    },
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision Law Illustrated Slides (Pedro Santos Jr).pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 - Subdivision Law Illustrated Slides (Pedro Santos Jr).md',
                    },
                ],
            },
            {
                'folder_name': 'PD-1216',
                'prepared_count': 0,
                'ocr_required_count': 1,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'ocr_required',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf',
                        'recommended_route': 'OCR_FIRST_THEN_OPENDATALOADER',
                    }
                ],
            },
            {
                'folder_name': 'PD-1185',
                'prepared_count': 1,
                'ocr_required_count': 0,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/PD-1185/PD 1185 - Fire Code of the Philippines 1977.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1185/PD 1185 - Fire Code of the Philippines 1977.md',
                    }
                ],
            },
        ],
    )

    result = _run_cli(
        [
            'run-laws-tranche-source-admission',
            '--tranche-manifest', str(tranche_manifest),
            '--source-prep-report', str(source_prep_report),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-tranche-source-admission'
    assert payload['admitted_source_page_count'] == 2
    assert payload['blocked_law_folders'] == ['PD-1216']
    report_path = tmp_path / payload['report_path']
    report = json.loads(report_path.read_text(encoding='utf-8'))
    pd957 = next(item for item in report['laws'] if item['folder_name'] == 'PD-957')
    assert pd957['admitted_source_count'] == 1
    assert pd957['candidate_source_page_count'] == 1
    assert pd957['excluded_prepared_count'] == 3
    assert pd957['admitted_source_paths'] == [
        '003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md'
    ]
    assert set(pd957['excluded_prepared_file_reports'][idx]['excluded_reason'] for idx in range(3)) == {
        'duplicate_sha256_alias',
        'study_aid_variant',
    }
    assert (tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'revised-implementing-rules-and-regulations-for-pd-957.md').exists()
    assert (tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'fire-code-of-the-philippines.md').exists()
    assert not (tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'pd-1216-open-space-requirements-in-subdivisions.md').exists()

    updated_manifest = yaml.safe_load(tranche_manifest.read_text(encoding='utf-8'))
    pd957_entry = next(item for item in updated_manifest['candidate_law_folders'] if item['folder_name'] == 'PD-957')
    assert pd957_entry['source_admission_state'] == 'admitted'
    assert pd957_entry['admitted_source_paths'] == [
        '003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md'
    ]
    assert pd957_entry['authoritative_variant_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf'
    ]
    assert '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision Law Illustrated Slides (Pedro Santos Jr).pdf' in pd957_entry['excluded_variant_paths']
    pd1216_entry = next(item for item in updated_manifest['candidate_law_folders'] if item['folder_name'] == 'PD-1216')
    assert pd1216_entry['source_admission_state'] == 'blocked_pending_ocr'
    assert pd1216_entry['blocked_raw_anchor_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf'
    ]


def test_source_admission_summary_respects_manifest_authoritative_and_excluded_variants(tmp_path: Path) -> None:
    from vitruvius import laws_readiness as lr

    selected_raw = '001_Raw-Source-Layer/001-Laws/PD-1067/Water Code of PH IRR 2005.pdf'
    excluded_raw = '001_Raw-Source-Layer/001-Laws/PD-1067/PD 1067 IRR - Water Code Implementing Rules.pdf'

    summary = lr._summarize_source_admission_folder(
        repo_root=tmp_path,
        item={
            'folder_name': 'PD-1067',
            'reason': 'water adjacency',
            'authoritative_variant_paths': [selected_raw],
            'excluded_variant_paths': [excluded_raw],
        },
        source_prep_folder={
            'raw_file_count': 2,
            'prepared_count': 2,
            'ocr_required_count': 0,
            'failed_count': 0,
            'file_reports': [
                {
                    'status': 'prepared',
                    'raw_path': selected_raw,
                    'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1067/Water Code of PH IRR 2005.md',
                },
                {
                    'status': 'prepared',
                    'raw_path': excluded_raw,
                    'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1067/PD 1067 IRR - Water Code Implementing Rules.md',
                },
            ],
        },
    )

    assert summary['candidate_source_page_count'] == 1
    assert summary['candidate_source_pages'][0]['raw_path'] == selected_raw
    assert summary['excluded_prepared_count'] == 1
    assert summary['excluded_prepared_file_reports'][0]['raw_path'] == excluded_raw
    assert summary['excluded_prepared_file_reports'][0]['excluded_reason'] == 'manifest_excluded_variant'


def test_run_laws_tranche_source_admission_dry_run_marks_ra1378_ready_when_source_prep_is_manifest_scoped(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-7.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-7',
                'candidate_law_folders': [
                    {
                        'folder_name': 'RA-1378',
                        'reason': 'plumbing law adjacency',
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/RA-1378/MASTER PLUMBING LAW.pdf',
                        ],
                        'excluded_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/RA-1378/188541488-Revised-National-Plumbing-Code-of-the-Philippines.pdf',
                            '001_Raw-Source-Layer/001-Laws/RA-1378/Board of Master Plumber.pdf',
                            '001_Raw-Source-Layer/001-Laws/RA-1378/Board of Master Plumber.doc',
                        ],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'MASTER PLUMBING LAW.pdf')
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / '188541488-Revised-National-Plumbing-Code-of-the-Philippines.pdf'
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'Board of Master Plumber.pdf')
    _write(tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'RA-1378' / 'Board of Master Plumber.doc', 'legacy doc')
    _seed_conversion_inventory_path(
        tmp_path,
        'RA-1378',
        'MASTER PLUMBING LAW',
        refined_payload='# PLUMBING LAW\n',
    )
    source_prep_report = _write_source_prep_report(
        tmp_path,
        'laws-tranche-7',
        'demo-run',
        [
            {
                'folder_name': 'RA-1378',
                'prepared_count': 1,
                'ocr_required_count': 0,
                'failed_count': 0,
                'file_reports': [
                    {
                        'status': 'prepared',
                        'raw_path': '001_Raw-Source-Layer/001-Laws/RA-1378/MASTER PLUMBING LAW.pdf',
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/RA-1378/MASTER PLUMBING LAW.md',
                    }
                ],
            }
        ],
    )

    result = _run_cli(
        [
            'run-laws-tranche-source-admission-dry-run',
            '--tranche-manifest', str(tranche_manifest),
            '--source-prep-report', str(source_prep_report),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['admission_review_ready_law_folders'] == ['RA-1378']
    assert payload['mixed_readiness_law_folders'] == []
    assert payload['blocked_law_folders'] == []

    report = json.loads((tmp_path / payload['report_path']).read_text(encoding='utf-8'))
    ra1378 = report['laws'][0]
    assert ra1378['folder_name'] == 'RA-1378'
    assert ra1378['status'] == 'ready_for_admission_review'
    assert ra1378['candidate_source_page_count'] == 1
    assert ra1378['excluded_prepared_count'] == 0
    assert ra1378['failed_count'] == 0


def test_source_admission_manifest_writeback_preserves_raw_anchor_intent_for_blocked_laws(tmp_path: Path) -> None:
    from vitruvius import laws_readiness as lr

    manifest_path = tmp_path / 'config' / 'datasets' / 'laws-tranche-3.yaml'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-3',
                'candidate_law_folders': [
                    {
                        'folder_name': 'PD-1151',
                        'reason': 'environmental policy adjacency',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-1151/PD 1151 - PD 1152 Environmental Code.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-1151/PD 1151 - PD 1152 Environmental Code.pdf',
                        ],
                        'excluded_variant_paths': [],
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    report_path = tmp_path / '006_System-Manifests' / 'runs' / 'datasets' / 'laws-tranche-3' / 'demo' / 'laws_tranche_source_admission_report.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('{}', encoding='utf-8')

    lr._write_source_admission_back_to_manifest(
        manifest_path=manifest_path,
        report_path=report_path,
        run_id='demo-run',
        folder_reports=[
            {
                'folder_name': 'PD-1151',
                'executed_source_admission_state': 'not_admitted',
                'admitted_source_paths': [],
                'admitted_source_pages': [],
                'excluded_prepared_file_reports': [],
                'blocked_file_reports': [],
                'admission_guardrails': [
                    'canonical rule missing for prepared variant PD 1151 - PD 1152 Environmental Code.md; source admission stays blocked until the rule exists'
                ],
            }
        ],
    )

    updated = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))
    entry = updated['candidate_law_folders'][0]
    assert entry['raw_anchor_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-1151/PD 1151 - PD 1152 Environmental Code.pdf',
    ]
    assert entry['authoritative_variant_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-1151/PD 1151 - PD 1152 Environmental Code.pdf',
    ]


def test_run_laws_tranche_source_to_graph_dry_run_stages_only_admitted_members(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'review_model_preset': 'm2-8gb-safe',
                'candidate_law_folders': [
                    {
                        'folder_name': 'PD-957',
                        'reason': 'housing adjacency',
                        'source_admission_state': 'admitted',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        ],
                        'excluded_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision _ Condominium Buyer_s Act.pdf',
                        ],
                        'refined_markdown_paths': [
                            '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md',
                        ],
                        'admitted_source_paths': [
                            '003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md',
                        ],
                        'admitted_concept_paths': [
                            '003_Canonical-Knowledge-Layer/shared/concepts/subdivision-project.md',
                        ],
                        'admitted_relationship_paths': [
                            '003_Canonical-Knowledge-Layer/shared/relationships/rel-irr-pd-957-governs-concept-subdivision-project.md',
                        ],
                        'verification_checks': ['pd-957 admitted'],
                        'scope_notes': ['pd-957 admitted note'],
                    },
                    {
                        'folder_name': 'PD-1216',
                        'reason': 'open-space adjacency',
                        'source_admission_state': 'blocked_pending_ocr',
                        'raw_anchor_paths': [],
                        'authoritative_variant_paths': [],
                        'excluded_variant_paths': [],
                        'refined_markdown_paths': [],
                        'admitted_source_paths': [],
                        'blocked_raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf',
                        ],
                        'verification_checks': ['pd-1216 blocked'],
                        'scope_notes': [],
                    },
                    {
                        'folder_name': 'PD-1185',
                        'reason': 'fire adjacency',
                        'source_admission_state': 'admitted',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-1185/PD 1185 - Fire Code of the Philippines 1977.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-1185/PD 1185 - Fire Code of the Philippines 1977.pdf',
                        ],
                        'excluded_variant_paths': [],
                        'refined_markdown_paths': [
                            '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1185/PD 1185 - Fire Code of the Philippines 1977.md',
                        ],
                        'admitted_source_paths': [
                            '003_Canonical-Knowledge-Layer/shared/sources/fire-code-of-the-philippines.md',
                        ],
                        'verification_checks': ['pd-1185 admitted'],
                        'scope_notes': ['pd-1185 admitted note'],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 IRR - Subdivision and Condominium IRR.pdf'
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 - Subdivision _ Condominium Buyer_s Act.pdf'
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1185' / 'PD 1185 - Fire Code of the Philippines 1977.pdf'
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-1216' / 'PD 1216 - Open Space Requirements in Subdivisions.pdf'
    )

    _seed_conversion_inventory_path(
        tmp_path,
        'PD-957',
        'PD 957 IRR - Subdivision and Condominium IRR',
        refined_payload='# REVISED IMPLEMENTING RULES AND REGULATIONS FOR PD 957\n',
    )
    _seed_conversion_inventory_path(
        tmp_path,
        'PD-1185',
        'PD 1185 - Fire Code of the Philippines 1977',
        refined_payload='# FIRE CODE OF THE PHILIPPINES\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'revised-implementing-rules-and-regulations-for-pd-957.md',
        '---\nid: irr-revised-implementing-rules-and-regulations-for-pd-957\ntitle: Revised Implementing Rules and Regulations for PD 957\ntrust_level: primary\n---\n\n# body\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'concepts' / 'subdivision-project.md',
        '---\nid: concept-subdivision-project\ncanonical_status: enriched\nconcept_status: enriched\n---\n\n# body\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'relationships' / 'rel-irr-pd-957-governs-concept-subdivision-project.md',
        '---\nid: rel-irr-pd-957-governs-concept-subdivision-project\npage_type: relationship\nrelationship_type: governs\nfrom_entity: irr-revised-implementing-rules-and-regulations-for-pd-957\nto_entity: concept-subdivision-project\ncanonical_status: promoted\n---\n\n# body\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'fire-code-of-the-philippines.md',
        '---\nid: law-fire-code-of-the-philippines\ntitle: Fire Code of the Philippines\ntrust_level: primary\n---\n\n# body\n',
    )

    result = _run_cli(
        [
            'run-laws-tranche-source-to-graph-dry-run',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['action'] == 'run-laws-tranche-source-to-graph-dry-run'
    assert payload['staged_law_folders'] == ['PD-957', 'PD-1185']
    assert payload['blocked_law_folders'] == ['PD-1216']
    assert payload['planned_stage_count'] == 2
    assert payload['source_to_graph_execute_ready'] is False
    assert payload['raw_alias_law_folders'] == ['PD-957']
    assert 'PD-957' in payload['guardrail_law_folders']
    report = json.loads((tmp_path / payload['report_path']).read_text(encoding='utf-8'))
    assert report['inner_source_to_graph_summary']['planned_stage_count'] == 2
    assert report['raw_alias_law_folders'] == ['PD-957']
    pd957_visibility = next(item for item in report['law_folder_variant_visibility'] if item['folder_name'] == 'PD-957')
    assert pd957_visibility['staged_for_source_to_graph'] is True
    assert pd957_visibility['authoritative_variant_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
    ]
    assert pd957_visibility['excluded_variant_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision _ Condominium Buyer_s Act.pdf',
    ]
    assert any(flag.startswith('exact_duplicate_sha256:') for flag in pd957_visibility['duplicate_guardrails'])
    assert 'conflicting_law_irr_filename_semantics' in pd957_visibility['duplicate_guardrails']
    pd1216_visibility = next(item for item in report['law_folder_variant_visibility'] if item['folder_name'] == 'PD-1216')
    assert pd1216_visibility['staged_for_source_to_graph'] is False
    assert pd1216_visibility['blocked_raw_anchor_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-1216/PD 1216 - Open Space Requirements in Subdivisions.pdf',
    ]
    derived_manifest = yaml.safe_load((tmp_path / payload['derived_manifest_path']).read_text(encoding='utf-8'))
    assert [unit['folder_name'] for unit in derived_manifest['law_units']] == ['PD-957', 'PD-1185']
    pd_957_unit = next(unit for unit in derived_manifest['law_units'] if unit['folder_name'] == 'PD-957')
    assert pd_957_unit['admitted_concept_paths'] == [
        '003_Canonical-Knowledge-Layer/shared/concepts/subdivision-project.md'
    ]
    assert pd_957_unit['admitted_relationship_paths'] == [
        '003_Canonical-Knowledge-Layer/shared/relationships/rel-irr-pd-957-governs-concept-subdivision-project.md'
    ]
    assert derived_manifest['canonical_input_manifest']['concepts'] == [
        {
            'path': '003_Canonical-Knowledge-Layer/shared/concepts/subdivision-project.md',
            'folder_name': 'PD-957',
            'entry_role': 'derived',
            'authority_tier': 'derived',
            'variant_family': 'pd-957-canonical-concept',
            'edition_or_source_note': 'Existing shared canonical concept selected explicitly for tranche source-to-graph dry-run staging.',
            'include_in_m1': True,
            'reason': 'Explicit truth-bearing canonical concept input carried through from tranche admission state.',
        }
    ]


def test_run_laws_tranche_source_to_graph_dry_run_reduces_shallow_representation_when_pd957_has_three_concepts(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'review_model_preset': 'm2-8gb-safe',
                'candidate_law_folders': [
                    {
                        'folder_name': 'PD-957',
                        'reason': 'housing adjacency',
                        'source_admission_state': 'admitted',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        ],
                        'excluded_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf',
                        ],
                        'refined_markdown_paths': [
                            '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md',
                        ],
                        'admitted_source_paths': [
                            '003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md',
                        ],
                        'admitted_concept_paths': [
                            '003_Canonical-Knowledge-Layer/shared/concepts/a.md',
                            '003_Canonical-Knowledge-Layer/shared/concepts/b.md',
                            '003_Canonical-Knowledge-Layer/shared/concepts/c.md',
                        ],
                        'admitted_relationship_paths': [
                            '003_Canonical-Knowledge-Layer/shared/relationships/rel-a.md',
                            '003_Canonical-Knowledge-Layer/shared/relationships/rel-b.md',
                            '003_Canonical-Knowledge-Layer/shared/relationships/rel-c.md',
                        ],
                        'verification_checks': [],
                        'scope_notes': [],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 IRR - Subdivision and Condominium IRR.pdf'
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf'
    )
    _seed_conversion_inventory_path(
        tmp_path,
        'PD-957',
        'PD 957 IRR - Subdivision and Condominium IRR',
        refined_payload='\n'.join([f'### Section {i}' for i in range(1, 80)]) + '\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'revised-implementing-rules-and-regulations-for-pd-957.md',
        '---\nid: irr-revised-implementing-rules-and-regulations-for-pd-957\ntitle: Revised Implementing Rules and Regulations for PD 957\ntrust_level: primary\n---\n\n# body\n',
    )
    for concept_name in ('a', 'b', 'c'):
        _write(
            tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'concepts' / f'{concept_name}.md',
            f'---\nid: concept-{concept_name}\ncanonical_status: enriched\nconcept_status: enriched\n---\n\n# body\n',
        )
        _write(
            tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'relationships' / f'rel-{concept_name}.md',
            f'---\nid: rel-{concept_name}\npage_type: relationship\nrelationship_type: governs\nfrom_entity: irr-revised-implementing-rules-and-regulations-for-pd-957\nto_entity: concept-{concept_name}\ncanonical_status: promoted\n---\n\n# body\n',
        )

    result = _run_cli(
        [
            'run-laws-tranche-source-to-graph-dry-run',
            '--tranche-manifest', str(tranche_manifest),
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload['shallow_representation_count'] == 0
    derived_manifest = yaml.safe_load((tmp_path / payload['derived_manifest_path']).read_text(encoding='utf-8'))
    assert len(derived_manifest['relationship_input_manifest']['relationships']) == 3


def test_run_laws_tranche_source_to_graph_execute_wrapper_reports_success(tmp_path: Path, monkeypatch) -> None:
    from vitruvius import laws_readiness as lr
    from vitruvius import dataset_pipeline as dp

    _seed_repo(tmp_path)
    tranche_manifest = tmp_path / 'config' / 'datasets' / 'laws-tranche-1.yaml'
    tranche_manifest.write_text(
        yaml.safe_dump(
            {
                'tranche_id': 'laws-tranche-1',
                'review_model_preset': 'm2-8gb-safe',
                'candidate_law_folders': [
                    {
                        'folder_name': 'PD-957',
                        'reason': 'housing adjacency',
                        'source_admission_state': 'admitted',
                        'raw_anchor_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        ],
                        'authoritative_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 IRR - Subdivision and Condominium IRR.pdf',
                        ],
                        'excluded_variant_paths': [
                            '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf',
                        ],
                        'refined_markdown_paths': [
                            '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md',
                        ],
                        'admitted_source_paths': [
                            '003_Canonical-Knowledge-Layer/shared/sources/revised-implementing-rules-and-regulations-for-pd-957.md',
                        ],
                        'admitted_concept_paths': [],
                        'admitted_relationship_paths': [],
                        'verification_checks': [],
                        'scope_notes': [],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 IRR - Subdivision and Condominium IRR.pdf'
    )
    _write_valid_pdf(
        tmp_path / '001_Raw-Source-Layer' / '001-Laws' / 'PD-957' / 'PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf'
    )
    _seed_conversion_inventory_path(
        tmp_path,
        'PD-957',
        'PD 957 IRR - Subdivision and Condominium IRR',
        refined_payload='# REVISED IMPLEMENTING RULES AND REGULATIONS FOR PD 957\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'revised-implementing-rules-and-regulations-for-pd-957.md',
        '---\nid: irr-revised-implementing-rules-and-regulations-for-pd-957\ntitle: Revised Implementing Rules and Regulations for PD 957\ntrust_level: primary\n---\n\n# body\n',
    )
    monkeypatch.chdir(tmp_path)

    def fake_execute(*, dataset_manifest: str, dry_run: bool, review_preset: str | None = None, **kwargs) -> int:
        payload = {
            'action': 'run-dataset-source-to-graph',
            'dataset_id': 'laws-tranche-1-source-to-graph-execute',
            'run_id': 'fake-run',
            'generated_relationship_count': 2,
            'filtered_relationship_count': 0,
            'manual_review_required_count': 0,
            'summary_auto_withheld_count': 0,
            'shallow_representation_count': 0,
            'pipeline_report_path': 'fake/source_to_graph_run_report.json',
            'graph_snapshot_path': 'fake/graph_snapshot.json',
            'graph_build_report_path': 'fake/build_graph_dataset_report.json',
        }
        print(json.dumps(payload))
        return 0

    monkeypatch.setattr(dp, 'run_dataset_source_to_graph_pipeline', fake_execute)

    rc, output = lr._capture_text_handler(
        lambda: lr.run_laws_tranche_source_to_graph(
            tranche_manifest=str(tranche_manifest),
            review_preset='m2-8gb-safe',
        )
    )
    assert rc == 0
    payload = json.loads(output)
    assert payload['action'] == 'run-laws-tranche-source-to-graph'
    assert payload['execute'] is True
    assert payload['staged_law_folders'] == ['PD-957']
    assert payload['generated_relationship_count'] == 2
    assert payload['raw_alias_law_folders'] == ['PD-957']
    report = json.loads((tmp_path / payload['report_path']).read_text(encoding='utf-8'))
    assert report['raw_alias_law_folders'] == ['PD-957']
    visibility = report['law_folder_variant_visibility'][0]
    assert visibility['folder_name'] == 'PD-957'
    assert visibility['excluded_variant_paths'] == [
        '001_Raw-Source-Layer/001-Laws/PD-957/PD 957 - Subdivision and Condominium Buyers Protective Decree.pdf',
    ]


def test_generic_completed_manifest_paths_returns_existing_manifests(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import completed_manifest_paths

    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'done-a.yaml').write_text('x: 1\n', encoding='utf-8')
    (tmp_path / 'config' / 'datasets' / 'done-b.yaml').write_text('x: 1\n', encoding='utf-8')
    (tmp_path / 'config' / 'datasets' / 'completed.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'a'}, {'lane_id': 'b'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'index.yaml').write_text(
        yaml.safe_dump({'manifests': [
            {'lane_id': 'a', 'manifest': 'config/datasets/done-a.yaml'},
            {'lane_id': 'b', 'manifest': 'config/datasets/done-b.yaml'},
        ]}, sort_keys=False),
        encoding='utf-8',
    )

    paths = completed_manifest_paths(
        repo_root=tmp_path,
        completed_ledger_path=tmp_path / 'config' / 'datasets' / 'completed.yaml',
        manifest_index_path=tmp_path / 'config' / 'datasets' / 'index.yaml',
    )
    assert [path.name for path in paths] == ['done-a.yaml', 'done-b.yaml']


def test_resolve_completed_aggregate_profile_path_returns_registered_profile(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import resolve_completed_aggregate_profile_path

    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'profile.yaml').write_text('dataset_id: demo\n', encoding='utf-8')
    (tmp_path / 'config' / 'datasets' / 'catalog.yaml').write_text(
        yaml.safe_dump(
            {
                'profiles': [
                    {'family': 'demo', 'profile': 'config/datasets/profile.yaml'},
                ]
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    resolved = resolve_completed_aggregate_profile_path(
        repo_root=tmp_path,
        family='demo',
        catalog_path=tmp_path / 'config' / 'datasets' / 'catalog.yaml',
    )
    assert resolved == tmp_path / 'config' / 'datasets' / 'profile.yaml'


def test_register_completed_aggregate_family_writes_profile_and_catalog(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import register_completed_aggregate_family

    repo_root = tmp_path
    resolved_profile_path, resolved_catalog_path, profile_payload, catalog_entry = register_completed_aggregate_family(
        repo_root=repo_root,
        family='demo',
        profile_path=Path('config/datasets/demo-profile.yaml'),
        catalog_path=Path('config/datasets/catalog.yaml'),
        dataset_id='demo-dataset',
        dataset_kind='demo-aggregate',
        completed_ledger='config/datasets/demo-completed.yaml',
        manifest_index='config/datasets/demo-index.yaml',
        out_manifest='006_System-Manifests/runs/datasets/demo/latest_dataset_manifest.yaml',
        graph_output_root='005_Operational-Intelligence-Layer/graph/datasets/demo',
        run_output_root='006_System-Manifests/runs/datasets/demo',
        query_snapshot_template='005_Operational-Intelligence-Layer/graph/datasets/demo/{run_id}_graph_snapshot.json',
        scope_notes=['demo scope'],
        lane_note_template='Demo lane: {lane_id}',
        status='demo',
        note='Demo onboarding family.',
    )
    assert resolved_profile_path == tmp_path / 'config' / 'datasets' / 'demo-profile.yaml'
    assert resolved_catalog_path == tmp_path / 'config' / 'datasets' / 'catalog.yaml'
    assert profile_payload['dataset_id'] == 'demo-dataset'
    profile_disk = yaml.safe_load(resolved_profile_path.read_text(encoding='utf-8'))
    assert profile_disk['dataset_id'] == 'demo-dataset'
    catalog_disk = yaml.safe_load(resolved_catalog_path.read_text(encoding='utf-8'))
    assert catalog_disk['profiles'][0]['family'] == 'demo'
    assert catalog_entry['status'] == 'demo'


def test_scaffold_completed_aggregate_family_writes_starter_files(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import scaffold_completed_aggregate_family

    result = scaffold_completed_aggregate_family(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
        dataset_kind='history-aggregate',
        note='History demo family.',
    )
    completed_ledger_payload = yaml.safe_load(result['completed_ledger_path'].read_text(encoding='utf-8'))
    manifest_index_payload = yaml.safe_load(result['manifest_index_path'].read_text(encoding='utf-8'))
    profile_payload = yaml.safe_load(result['profile_path'].read_text(encoding='utf-8'))
    assert completed_ledger_payload == {'completed_lanes': []}
    assert manifest_index_payload == {'manifests': []}
    assert profile_payload['dataset_id'] == 'history-demo-aggregate'
    assert result['catalog_entry']['family'] == 'history-demo'


def test_admit_completed_manifest_to_family_updates_ledger_and_index(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import admit_completed_manifest_to_family, scaffold_completed_aggregate_family

    scaffold_completed_aggregate_family(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
        dataset_kind='history-aggregate',
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '002-History' / 'example.pdf')
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'history-demo-source.md',
        '---\nid: source-history-demo\n---\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'relationships' / 'history-demo-rel.md',
        '---\nid: rel-history-demo\nfrom: source-history-demo\nto: source-history-demo\npredicate: cites\n---\n',
    )
    manifest_path = tmp_path / 'config' / 'datasets' / 'history-lane-1.yaml'
    manifest_path.write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'history-lane-1',
                'dataset_kind': 'history-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/history-lane-1',
                'run_output_root': 'runs/history-lane-1',
                'query_snapshot_path_template': 'graph/history-lane-1/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    result = admit_completed_manifest_to_family(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
        lane_id='history-lane-1',
        manifest_path=Path('config/datasets/history-lane-1.yaml'),
    )
    completed_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-completed-lanes.yaml').read_text(encoding='utf-8'))
    manifest_index_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-manifest-index.yaml').read_text(encoding='utf-8'))
    assert completed_payload['completed_lanes'] == [{'lane_id': 'history-lane-1'}]
    assert manifest_index_payload['manifests'] == [{'lane_id': 'history-lane-1', 'manifest': 'config/datasets/history-lane-1.yaml'}]
    assert result['lane_id'] == 'history-lane-1'


def test_check_completed_aggregate_family_readiness_reports_blockers(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import check_completed_aggregate_family_readiness, scaffold_completed_aggregate_family

    scaffold_completed_aggregate_family(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
        dataset_kind='history-aggregate',
    )
    readiness = check_completed_aggregate_family_readiness(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
    )
    assert readiness['ready_to_run'] is False
    assert 'no completed lanes admitted' in readiness['blockers']
    assert 'no completed manifests resolved from ledger/index' in readiness['blockers']


def test_check_completed_aggregate_family_readiness_reports_ready_family(tmp_path: Path) -> None:
    from vitruvius.aggregate_manifest import (
        admit_completed_manifest_to_family,
        check_completed_aggregate_family_readiness,
        scaffold_completed_aggregate_family,
    )

    scaffold_completed_aggregate_family(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
        dataset_kind='history-aggregate',
    )
    _write_valid_pdf(tmp_path / '001_Raw-Source-Layer' / '002-History' / 'example.pdf')
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'sources' / 'history-demo-source.md',
        '---\nid: source-history-demo\n---\n',
    )
    _write(
        tmp_path / '003_Canonical-Knowledge-Layer' / 'shared' / 'relationships' / 'history-demo-rel.md',
        '---\nid: rel-history-demo\nfrom: source-history-demo\nto: source-history-demo\npredicate: cites\n---\n',
    )
    manifest_path = tmp_path / 'config' / 'datasets' / 'history-lane-1.yaml'
    manifest_path.write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'history-lane-1',
                'dataset_kind': 'history-aggregate',
                'raw_slice_anchors': [
                    {
                        'folder_name': 'history-demo',
                        'raw_root': '001_Raw-Source-Layer/002-History',
                        'entry_role': 'authoritative',
                        'authority_tier': 'primary',
                        'variant_family': 'history-demo',
                        'edition_or_source_note': 'history demo root',
                        'include_in_m1': True,
                        'reason': 'history demo lane',
                        'classified_raw_entries': [
                            {
                                'path': '001_Raw-Source-Layer/002-History/example.pdf',
                                'folder_name': 'history-demo',
                                'entry_role': 'authoritative',
                                'authority_tier': 'primary',
                                'variant_family': 'history-demo',
                                'edition_or_source_note': 'history demo entry',
                                'include_in_m1': True,
                                'reason': 'history demo lane',
                            }
                        ],
                    }
                ],
                'canonical_input_manifest': {
                    'sources': [
                        {
                            'path': '003_Canonical-Knowledge-Layer/shared/sources/history-demo-source.md',
                            'folder_name': 'history-demo',
                            'entry_role': 'authoritative',
                            'authority_tier': 'primary',
                            'variant_family': 'history-demo-source',
                            'edition_or_source_note': 'history demo source',
                            'include_in_m1': True,
                            'reason': 'history demo lane',
                        }
                    ],
                    'concepts': [],
                },
                'relationship_input_manifest': {
                    'relationships': [
                        {
                            'path': '003_Canonical-Knowledge-Layer/shared/relationships/history-demo-rel.md',
                            'folder_name': 'history-demo',
                            'entry_role': 'authoritative',
                            'authority_tier': 'approved',
                            'variant_family': 'history-demo-rel',
                            'edition_or_source_note': 'history demo relationship',
                            'include_in_m1': True,
                            'reason': 'history demo lane',
                        }
                    ]
                },
                'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/history-lane-1',
                'run_output_root': '006_System-Manifests/runs/datasets/history-lane-1',
                'query_snapshot_path_template': '005_Operational-Intelligence-Layer/graph/datasets/history-lane-1/{run_id}_graph_snapshot.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [
                    {
                        'law_id': 'history-lane-1',
                        'folder_name': 'history-demo',
                        'raw_anchor_paths': ['001_Raw-Source-Layer/002-History/example.pdf'],
                        'refined_markdown_paths': [],
                        'authoritative_variant_paths': ['001_Raw-Source-Layer/002-History/example.pdf'],
                        'excluded_variant_paths': [],
                        'admitted_source_paths': ['003_Canonical-Knowledge-Layer/shared/sources/history-demo-source.md'],
                        'admitted_concept_paths': [],
                        'admitted_relationship_paths': ['003_Canonical-Knowledge-Layer/shared/relationships/history-demo-rel.md'],
                        'verification_checks': [],
                        'scope_notes': [],
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    admit_completed_manifest_to_family(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
        lane_id='history-lane-1',
        manifest_path=Path('config/datasets/history-lane-1.yaml'),
    )
    readiness = check_completed_aggregate_family_readiness(
        repo_root=tmp_path,
        family='history-demo',
        catalog_path=Path('config/datasets/catalog.yaml'),
    )
    assert readiness['ready_to_run'] is True
    assert readiness['blockers'] == []
    assert readiness['completed_lane_count'] == 1
    assert readiness['resolved_manifest_count'] == 1


def test_pipeline_cli_build_completed_aggregate_manifest_writes_manifest(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'done-a.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'done-a',
                'dataset_kind': 'laws-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/a',
                'run_output_root': 'runs/a',
                'query_snapshot_path_template': 'graph/a/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'completed.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'lane-a'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'index.yaml').write_text(
        yaml.safe_dump({'manifests': [{'lane_id': 'lane-a', 'manifest': 'config/datasets/done-a.yaml'}]}, sort_keys=False),
        encoding='utf-8',
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'build-completed-aggregate-manifest',
            '--completed-ledger', 'config/datasets/completed.yaml',
            '--manifest-index', 'config/datasets/index.yaml',
            '--dataset-id', 'generic-demo',
            '--dataset-kind', 'laws-aggregate',
            '--out', 'config/datasets/generic-demo.yaml',
            '--graph-output-root', '005_Operational-Intelligence-Layer/graph/datasets/generic-demo',
            '--run-output-root', '006_System-Manifests/runs/datasets/generic-demo',
            '--query-snapshot-template', '005_Operational-Intelligence-Layer/graph/datasets/generic-demo/{run_id}_graph_snapshot.json',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'generic-demo.yaml').read_text(encoding='utf-8'))
    assert payload['dataset_id'] == 'generic-demo'
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['action'] == 'build-completed-aggregate-manifest'
    assert stdout_payload['dataset_manifest_path'] == 'config/datasets/generic-demo.yaml'


def test_pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'done-a.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'done-a',
                'dataset_kind': 'laws-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/a',
                'run_output_root': 'runs/a',
                'query_snapshot_path_template': 'graph/a/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'completed.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'lane-a'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'index.yaml').write_text(
        yaml.safe_dump({'manifests': [{'lane_id': 'lane-a', 'manifest': 'config/datasets/done-a.yaml'}]}, sort_keys=False),
        encoding='utf-8',
    )

    seen: dict[str, object] = {}

    def fake_run_dataset_source_to_graph_pipeline(**kwargs):
        seen.update(kwargs)
        return 0

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('vitruvius.dataset_pipeline.run_dataset_source_to_graph_pipeline', fake_run_dataset_source_to_graph_pipeline)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'run-completed-aggregate',
            '--completed-ledger', 'config/datasets/completed.yaml',
            '--manifest-index', 'config/datasets/index.yaml',
            '--dataset-id', 'generic-demo',
            '--dataset-kind', 'laws-aggregate',
            '--out', 'config/datasets/generic-demo.yaml',
            '--graph-output-root', '005_Operational-Intelligence-Layer/graph/datasets/generic-demo',
            '--run-output-root', '006_System-Manifests/runs/datasets/generic-demo',
            '--query-snapshot-template', '005_Operational-Intelligence-Layer/graph/datasets/generic-demo/{run_id}_graph_snapshot.json',
            '--dry-run',
            '--review-preset', 'm2-8gb-safe',
            '--skip-export-owl',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    assert seen['dataset_manifest'] == 'config/datasets/generic-demo.yaml'
    assert seen['dry_run'] is True
    assert seen['review_preset'] == 'm2-8gb-safe'
    assert seen['export_owl'] is False
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['dataset_manifest_path'] == 'config/datasets/generic-demo.yaml'


def test_pipeline_cli_build_completed_aggregate_from_profile_writes_manifest(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'done-a.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'done-a',
                'dataset_kind': 'laws-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/a',
                'run_output_root': 'runs/a',
                'query_snapshot_path_template': 'graph/a/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'completed.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'lane-a'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'index.yaml').write_text(
        yaml.safe_dump({'manifests': [{'lane_id': 'lane-a', 'manifest': 'config/datasets/done-a.yaml'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'profile.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'generic-profile-demo',
                'dataset_kind': 'laws-aggregate',
                'completed_ledger': 'config/datasets/completed.yaml',
                'manifest_index': 'config/datasets/index.yaml',
                'out_manifest': 'config/datasets/profile-out.yaml',
                'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/profile-out',
                'run_output_root': '006_System-Manifests/runs/datasets/profile-out',
                'query_snapshot_template': '005_Operational-Intelligence-Layer/graph/datasets/profile-out/{run_id}_graph_snapshot.json',
                'scope_notes': ['profile based aggregate'],
                'lane_note_template': 'Profile aggregate lane: {lane_id}',
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'build-completed-aggregate-from-profile',
            '--profile', 'config/datasets/profile.yaml',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'profile-out.yaml').read_text(encoding='utf-8'))
    assert payload['dataset_id'] == 'generic-profile-demo'
    assert payload['scope_notes'] == ['profile based aggregate']
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['dataset_manifest_path'] == 'config/datasets/profile-out.yaml'


def test_pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'register-completed-aggregate-family',
            '--family', 'demo',
            '--profile', 'config/datasets/demo-profile.yaml',
            '--catalog', 'config/datasets/catalog.yaml',
            '--dataset-id', 'demo-dataset',
            '--dataset-kind', 'demo-aggregate',
            '--completed-ledger', 'config/datasets/demo-completed.yaml',
            '--manifest-index', 'config/datasets/demo-index.yaml',
            '--out-manifest', '006_System-Manifests/runs/datasets/demo/latest_dataset_manifest.yaml',
            '--graph-output-root', '005_Operational-Intelligence-Layer/graph/datasets/demo',
            '--run-output-root', '006_System-Manifests/runs/datasets/demo',
            '--query-snapshot-template', '005_Operational-Intelligence-Layer/graph/datasets/demo/{run_id}_graph_snapshot.json',
            '--scope-note', 'demo scope',
            '--lane-note-template', 'Demo lane: {lane_id}',
            '--status', 'demo',
            '--note', 'Demo onboarding family.',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    profile_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'demo-profile.yaml').read_text(encoding='utf-8'))
    assert profile_payload['dataset_id'] == 'demo-dataset'
    catalog_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'catalog.yaml').read_text(encoding='utf-8'))
    assert catalog_payload['profiles'][0]['family'] == 'demo'
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['action'] == 'register-completed-aggregate-family'
    assert stdout_payload['family'] == 'demo'


def test_pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'scaffold-completed-aggregate-family',
            '--family', 'history-demo',
            '--catalog', 'config/datasets/catalog.yaml',
            '--dataset-kind', 'history-aggregate',
            '--note', 'History demo family.',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    completed_ledger_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-completed-lanes.yaml').read_text(encoding='utf-8'))
    manifest_index_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-manifest-index.yaml').read_text(encoding='utf-8'))
    profile_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-mvp-profile.yaml').read_text(encoding='utf-8'))
    assert completed_ledger_payload == {'completed_lanes': []}
    assert manifest_index_payload == {'manifests': []}
    assert profile_payload['dataset_id'] == 'history-demo-aggregate'
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['action'] == 'scaffold-completed-aggregate-family'
    assert stdout_payload['family'] == 'history-demo'


def test_pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'history-lane-1.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'history-lane-1',
                'dataset_kind': 'history-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/history-lane-1',
                'run_output_root': 'runs/history-lane-1',
                'query_snapshot_path_template': 'graph/history-lane-1/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'scaffold-completed-aggregate-family',
            '--family', 'history-demo',
            '--catalog', 'config/datasets/catalog.yaml',
            '--dataset-kind', 'history-aggregate',
        ],
    )
    assert pipeline_cli.main() == 0
    capsys.readouterr()

    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'admit-completed-aggregate-manifest',
            '--family', 'history-demo',
            '--catalog', 'config/datasets/catalog.yaml',
            '--lane-id', 'history-lane-1',
            '--manifest', 'config/datasets/history-lane-1.yaml',
        ],
    )
    rc = pipeline_cli.main()
    assert rc == 0
    completed_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-completed-lanes.yaml').read_text(encoding='utf-8'))
    manifest_index_payload = yaml.safe_load((tmp_path / 'config' / 'datasets' / 'history-demo-manifest-index.yaml').read_text(encoding='utf-8'))
    assert completed_payload['completed_lanes'] == [{'lane_id': 'history-lane-1'}]
    assert manifest_index_payload['manifests'] == [{'lane_id': 'history-lane-1', 'manifest': 'config/datasets/history-lane-1.yaml'}]
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['action'] == 'admit-completed-aggregate-manifest'
    assert stdout_payload['family'] == 'history-demo'


def test_pipeline_cli_check_completed_aggregate_family_reports_blockers(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'scaffold-completed-aggregate-family',
            '--family', 'history-demo',
            '--catalog', 'config/datasets/catalog.yaml',
            '--dataset-kind', 'history-aggregate',
        ],
    )
    assert pipeline_cli.main() == 0
    capsys.readouterr()

    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'check-completed-aggregate-family',
            '--family', 'history-demo',
            '--catalog', 'config/datasets/catalog.yaml',
        ],
    )
    rc = pipeline_cli.main()
    assert rc == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['action'] == 'check-completed-aggregate-family'
    assert stdout_payload['ready_to_run'] is False
    assert 'no completed lanes admitted' in stdout_payload['blockers']


def test_pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'done-a.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'done-a',
                'dataset_kind': 'laws-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/a',
                'run_output_root': 'runs/a',
                'query_snapshot_path_template': 'graph/a/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'completed.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'lane-a'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'index.yaml').write_text(
        yaml.safe_dump({'manifests': [{'lane_id': 'lane-a', 'manifest': 'config/datasets/done-a.yaml'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'profile.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'generic-profile-demo',
                'dataset_kind': 'laws-aggregate',
                'completed_ledger': 'config/datasets/completed.yaml',
                'manifest_index': 'config/datasets/index.yaml',
                'out_manifest': 'config/datasets/profile-out.yaml',
                'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/profile-out',
                'run_output_root': '006_System-Manifests/runs/datasets/profile-out',
                'query_snapshot_template': '005_Operational-Intelligence-Layer/graph/datasets/profile-out/{run_id}_graph_snapshot.json',
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    seen: dict[str, object] = {}

    def fake_run_dataset_source_to_graph_pipeline(**kwargs):
        seen.update(kwargs)
        return 0

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('vitruvius.dataset_pipeline.run_dataset_source_to_graph_pipeline', fake_run_dataset_source_to_graph_pipeline)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'run-completed-aggregate-from-profile',
            '--profile', 'config/datasets/profile.yaml',
            '--dry-run',
            '--review-preset', 'm2-8gb-safe',
            '--skip-export-owl',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    assert seen['dataset_manifest'] == 'config/datasets/profile-out.yaml'
    assert seen['dry_run'] is True
    assert seen['review_preset'] == 'm2-8gb-safe'
    assert seen['export_owl'] is False
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['dataset_manifest_path'] == 'config/datasets/profile-out.yaml'


def test_pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    import pipeline_cli

    _seed_repo(tmp_path)
    (tmp_path / 'config' / 'datasets').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'config' / 'datasets' / 'done-a.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'done-a',
                'dataset_kind': 'laws-aggregate',
                'raw_slice_anchors': [],
                'canonical_input_manifest': {'sources': [], 'concepts': []},
                'relationship_input_manifest': {'relationships': []},
                'graph_output_root': 'graph/a',
                'run_output_root': 'runs/a',
                'query_snapshot_path_template': 'graph/a/{run_id}.json',
                'freshness_policy': {'mode': 'exact'},
                'pilot_gate': {'require_manifest_validation': True, 'source_to_graph_execute_ready': False},
                'law_units': [],
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'completed.yaml').write_text(
        yaml.safe_dump({'completed_lanes': [{'lane_id': 'lane-a'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'index.yaml').write_text(
        yaml.safe_dump({'manifests': [{'lane_id': 'lane-a', 'manifest': 'config/datasets/done-a.yaml'}]}, sort_keys=False),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'profile.yaml').write_text(
        yaml.safe_dump(
            {
                'dataset_id': 'family-demo',
                'dataset_kind': 'laws-aggregate',
                'completed_ledger': 'config/datasets/completed.yaml',
                'manifest_index': 'config/datasets/index.yaml',
                'out_manifest': 'config/datasets/family-out.yaml',
                'graph_output_root': '005_Operational-Intelligence-Layer/graph/datasets/family-out',
                'run_output_root': '006_System-Manifests/runs/datasets/family-out',
                'query_snapshot_template': '005_Operational-Intelligence-Layer/graph/datasets/family-out/{run_id}_graph_snapshot.json',
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    (tmp_path / 'config' / 'datasets' / 'catalog.yaml').write_text(
        yaml.safe_dump(
            {
                'profiles': [
                    {'family': 'demo', 'profile': 'config/datasets/profile.yaml'},
                ]
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )

    seen: dict[str, object] = {}

    def fake_run_dataset_source_to_graph_pipeline(**kwargs):
        seen.update(kwargs)
        return 0

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('vitruvius.dataset_pipeline.run_dataset_source_to_graph_pipeline', fake_run_dataset_source_to_graph_pipeline)
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'pipeline_cli.py',
            'run-completed-aggregate-family',
            '--family', 'demo',
            '--catalog', 'config/datasets/catalog.yaml',
            '--dry-run',
            '--review-preset', 'm2-8gb-safe',
            '--skip-export-owl',
        ],
    )

    rc = pipeline_cli.main()
    assert rc == 0
    assert seen['dataset_manifest'] == 'config/datasets/family-out.yaml'
    assert seen['dry_run'] is True
    assert seen['review_preset'] == 'm2-8gb-safe'
    assert seen['export_owl'] is False
    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload['dataset_manifest_path'] == 'config/datasets/family-out.yaml'
