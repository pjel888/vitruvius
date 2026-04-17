from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

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
    (extra_folder / 'bp220.pdf').write_bytes(b'%PDF-1.4\n')

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
    (pd957 / 'pd957.pdf').write_bytes(b'%PDF-1.4\n')
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
    report_path = tmp_path / payload['report_path']
    assert report_path.exists()


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
    _seed_conversion_inventory(tmp_path, 'PD-957', 'pd957-law')
    _seed_conversion_inventory(tmp_path, 'PD-1185', 'pd1185-law')
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
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-957/pd957-law.md',
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
                        'expected_refined_markdown_path': '002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1185/pd1185-law.md',
                    }
                ],
            },
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
        '003_Canonical-Knowledge-Layer/shared/sources/pd957-law.md'
    )
    blocked_law = next(item for item in report['laws'] if item['folder_name'] == 'PD-1216')
    assert blocked_law['status'] == 'blocked_pending_ocr'
    assert blocked_law['blocked_file_reports'][0]['recommended_route'] == 'OCR_FIRST_THEN_OPENDATALOADER'
