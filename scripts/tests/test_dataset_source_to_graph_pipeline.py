from __future__ import annotations

import json
from pathlib import Path

import yaml

from vitruvius.dataset_pipeline import run_dataset_source_to_graph_pipeline


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def _seed_repo(root: Path) -> Path:
    raw = root / '001_Raw-Source-Layer' / '001-Laws' / 'RA-9514'
    raw.mkdir(parents=True, exist_ok=True)
    (raw / 'RA9514-RIRR-rev-2019.pdf').write_bytes(b'%PDF-1.4\n')

    refined = root / '002_Raw-Conversion-Layer' / '001-Laws' / 'refined_markdown' / 'RA-9514'
    refined.mkdir(parents=True, exist_ok=True)
    (refined / 'RA9514-RIRR-rev-2019.md').write_text('SECTION 1\nMeans of egress shall comply.\n', encoding='utf-8')

    shared = root / '003_Canonical-Knowledge-Layer' / 'shared'
    _write(shared / 'sources' / 'fire.md', (
        '---\n'
        'id: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
        'trust_level: primary\n'
        'last_canonicalized_utc: 2026-04-01T00:00:00Z\n'
        '---\n\n# body\n'
    ))
    _write(shared / 'concepts' / 'means-of-egress.md', (
        '---\n'
        'id: concept-means-of-egress\n'
        'canonical_status: enriched\n'
        'concept_status: enriched\n'
        'last_canonicalized_utc: 2026-04-01T00:00:00Z\n'
        'enriched_at_utc: 2026-04-01T00:00:00Z\n'
        'regulatory_basis:\n'
        '- source_id: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
        '  section_id: sec-1\n'
        '  evidence_snippet: means of egress\n'
        '---\n\n# body\n'
    ))
    _write(shared / 'relationships' / 'seed.md', (
        '---\n'
        'id: rel-seed\n'
        'page_type: relationship\n'
        'relationship_type: governs\n'
        'from_entity: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
        'to_entity: concept-means-of-egress\n'
        'canonical_status: promoted\n'
        'evidence:\n'
        '- source_id: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
        '  source_section_id: sec-1\n'
        '  evidence_snippet: means of egress\n'
        '  reviewer_confidence: 0.95\n'
        '---\n\n# body\n'
    ))

    manifest = {
        'dataset_id': 'demo-dataset',
        'dataset_kind': 'demo',
        'raw_slice_anchors': [
            {
                'folder_name': 'RA-9514',
                'raw_root': '001_Raw-Source-Layer/001-Laws/RA-9514',
                'entry_role': 'authoritative',
                'authority_tier': 'primary',
                'variant_family': 'demo',
                'edition_or_source_note': 'demo',
                'include_in_m1': True,
                'reason': 'demo',
                'classified_raw_entries': [
                    {
                        'path': '001_Raw-Source-Layer/001-Laws/RA-9514/RA9514-RIRR-rev-2019.pdf',
                        'folder_name': 'RA-9514',
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
                    'path': '003_Canonical-Knowledge-Layer/shared/sources/fire.md',
                    'folder_name': 'RA-9514',
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
                    'path': '003_Canonical-Knowledge-Layer/shared/concepts/means-of-egress.md',
                    'folder_name': 'RA-9514',
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
                    'path': '003_Canonical-Knowledge-Layer/shared/relationships/seed.md',
                    'folder_name': 'RA-9514',
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
                'law_id': 'ra-9514',
                'folder_name': 'RA-9514',
                'raw_anchor_paths': ['001_Raw-Source-Layer/001-Laws/RA-9514/RA9514-RIRR-rev-2019.pdf'],
                'refined_markdown_paths': ['002_Raw-Conversion-Layer/001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md'],
                'authoritative_variant_paths': ['001_Raw-Source-Layer/001-Laws/RA-9514/RA9514-RIRR-rev-2019.pdf'],
                'excluded_variant_paths': [],
                'admitted_source_paths': ['003_Canonical-Knowledge-Layer/shared/sources/fire.md'],
                'admitted_concept_paths': ['003_Canonical-Knowledge-Layer/shared/concepts/means-of-egress.md'],
                'admitted_relationship_paths': ['003_Canonical-Knowledge-Layer/shared/relationships/seed.md'],
                'verification_checks': ['demo'],
                'scope_notes': ['demo'],
            }
        ],
    }
    manifest_path = root / 'config' / 'datasets' / 'demo.yaml'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding='utf-8')
    return manifest_path


def test_run_dataset_source_to_graph_pipeline_writes_derived_manifest_and_report(tmp_path, monkeypatch) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    import vitruvius.dataset_pipeline as dp

    monkeypatch.setattr(dp, 'run_canonicalize_one', lambda **kwargs: 0)

    def fake_extract(**kwargs):
        out = kwargs['json_output_path']
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            'generated_at': '20260416T000000Z',
            'source': kwargs['relative_markdown_path'],
            'source_id': kwargs['source_id_override'],
            'total_sections': 1,
            'total_relationships': 1,
            'relationships': [
                {
                    'from': kwargs['source_id_override'],
                    'type': 'governs',
                    'to': 'concept-means-of-egress',
                    'occurrences': 1,
                    'sections': ['section-1'],
                    'examples': ['means of egress'],
                }
            ],
        }), encoding='utf-8')
        kwargs['txt_output_path'].write_text('ok', encoding='utf-8')
        return 0

    def fake_review(**kwargs):
        kwargs['review_json_path'].write_text(json.dumps({'ok': True}), encoding='utf-8')
        kwargs['review_txt_path'].write_text('ok', encoding='utf-8')
        kwargs['triage_report_path'].write_text(json.dumps({'ok': True}), encoding='utf-8')
        kwargs['high_confidence_output_path'].write_text(json.dumps({
            'generated_at': '20260416T000000Z',
            'source_report_generated_at': '20260416T000000Z',
            'source_model': 'fake',
            'source': 'demo',
            'threshold': 0.9,
            'count': 1,
            'candidates': [],
        }), encoding='utf-8')
        return 0

    def fake_promote(**kwargs):
        rel_dir = kwargs['relationships_output_dir']
        rel_dir.mkdir(parents=True, exist_ok=True)
        rel_path = rel_dir / 'rel-generated.md'
        rel_path.write_text(
            '---\n'
            'id: rel-generated\n'
            'page_type: relationship\n'
            'relationship_type: governs\n'
            'from_entity: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
            'to_entity: concept-means-of-egress\n'
            'canonical_status: promoted\n'
            'evidence:\n'
            '- source_id: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
            '  source_section_id: section-1\n'
            '  evidence_snippet: means of egress\n'
            '  reviewer_confidence: 0.95\n'
            '---\n\n# body\n',
            encoding='utf-8',
        )
        noisy_path = rel_dir / 'rel-noisy.md'
        noisy_path.write_text(
            '---\n'
            'id: rel-noisy\n'
            'page_type: relationship\n'
            'relationship_type: requires\n'
            'from_entity: concept-means-of-egress\n'
            'to_entity: concept-stairs\n'
            'canonical_status: promoted\n'
            'evidence:\n'
            '- source_id: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
            '  source_section_id: section-1\n'
            '  evidence_snippet: noisy\n'
            '  reviewer_confidence: 0.95\n'
            '---\n\n# body\n',
            encoding='utf-8',
        )
        kwargs['audit_log_path'].write_text('audit', encoding='utf-8')
        return {'created': 2, 'rejected': 0, 'errors': []}

    def fake_build_graph(*, dataset_manifest: str, dry_run: bool = False):
        payload = yaml.safe_load(Path(dataset_manifest).read_text(encoding='utf-8'))
        rels = payload['relationship_input_manifest']['relationships']
        out = {
            'run_id': '20260416T111111Z',
            'snapshot_path': '005_Operational-Intelligence-Layer/graph/datasets/demo-dataset/20260416T111111Z_graph_snapshot.json',
            'build_report_path': '006_System-Manifests/runs/datasets/demo-dataset/20260416T111111Z_build_graph_dataset_report.json',
            'relationship_count_seen': len(rels),
        }
        print(json.dumps(out))
        return 0

    monkeypatch.setattr(dp, 'run_extract_relationships_sections_one_inner', fake_extract)
    monkeypatch.setattr(dp, 'run_review_relationships_ollama', fake_review)
    monkeypatch.setattr(dp, 'run_promote_inner', fake_promote)
    monkeypatch.setattr(dp, 'run_build_graph', fake_build_graph)
    monkeypatch.setattr(dp, 'run_export_graph_owl', lambda **kwargs: 0)
    monkeypatch.setattr(dp, 'run_query_structured', lambda **kwargs: 0)

    rc = run_dataset_source_to_graph_pipeline(dataset_manifest=str(manifest_path), export_owl=False)
    assert rc == 0

    reports = sorted((tmp_path / '006_System-Manifests' / 'runs' / 'datasets' / 'demo-dataset' / 'source_to_graph').glob('*/source_to_graph_run_report.json'))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding='utf-8'))
    assert report['generated_relationship_count'] == 1
    assert report['filtered_relationship_count'] == 1
    assert report['source_quality_summary']['severity_counts']['low'] == 1
    assert report['source_quality_summary']['manual_review_required_paths'] == []
    assert len(report['source_quality_summary']['benchmark_source_hints']) == 1
    assert 'source_quality' in report['stage_results'][0]
    assert report['stage_results'][0]['source_quality']['useful_text_line_count'] >= 1
    assert report['stage_results'][0]['source_quality']['severity'] in {'low','medium','high'}
    assert isinstance(report['stage_results'][0]['source_quality']['recommendations'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['benchmark_source_hints'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['benchmark_source_hints'], list)
    derived_manifest = tmp_path / report['derived_manifest_path']
    assert derived_manifest.exists()
    derived_payload = yaml.safe_load(derived_manifest.read_text(encoding='utf-8'))
    rel_paths = [entry['path'] for entry in derived_payload['relationship_input_manifest']['relationships']]
    assert any(path.endswith('rel-generated.md') for path in rel_paths)
    assert not any(path.endswith('rel-noisy.md') for path in rel_paths)
    assert report['graph']['snapshot_path'].endswith('_graph_snapshot.json')


def test_run_dataset_source_to_graph_pipeline_dry_run_writes_plan_only(tmp_path, monkeypatch) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    import vitruvius.dataset_pipeline as dp

    rc = run_dataset_source_to_graph_pipeline(dataset_manifest=str(manifest_path), dry_run=True, export_owl=False)
    assert rc == 0

    reports = sorted((tmp_path / '006_System-Manifests' / 'runs' / 'datasets' / 'demo-dataset' / 'source_to_graph').glob('*/source_to_graph_run_report.json'))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding='utf-8'))
    assert report['dry_run'] is True
    assert report['source_quality_summary']['severity_counts']['low'] == 1
    assert report['source_quality_summary']['manual_review_required_paths'] == []
    assert len(report['source_quality_summary']['benchmark_source_hints']) == 1
    assert report['source_quality_summary']['manual_review_required_paths'] == []
    assert len(report['source_quality_summary']['benchmark_source_hints']) == 1
    assert len(report['stage_results']) == 1
    assert 'planned_extract_json' in report['stage_results'][0]
    assert report['stage_results'][0]['normalized_refined_markdown_path'] == '001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md'
    assert 'source_quality' in report['stage_results'][0]
    assert report['stage_results'][0]['source_quality']['useful_text_line_count'] >= 1
    assert report['stage_results'][0]['source_quality']['severity'] in {'low','medium','high'}
    assert isinstance(report['stage_results'][0]['source_quality']['recommendations'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['benchmark_source_hints'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['benchmark_source_hints'], list)
    assert report['stage_results'][0]['source_quality']['severity'] in {'low','medium','high'}
    assert isinstance(report['stage_results'][0]['source_quality']['recommendations'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['benchmark_source_hints'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['benchmark_source_hints'], list)
    assert isinstance(report['stage_results'][0]['source_quality']['recommendations'], list)
    assert 'source_quality_path' in report['stage_results'][0]
    assert not (tmp_path / '006_System-Manifests' / 'runs' / 'datasets' / 'demo-dataset' / 'source_to_graph' / reports[0].parent.name / 'promoted_relationships').exists()


def test_run_dataset_source_to_graph_pipeline_dry_run_flags_high_severity_ra_9514_sources(tmp_path, monkeypatch) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    refined_path = (
        tmp_path
        / '002_Raw-Conversion-Layer'
        / '001-Laws'
        / 'refined_markdown'
        / 'RA-9514'
        / 'RA9514-RIRR-rev-2019.md'
    )
    refined_path.write_text(
        '\n'.join([
            'https://noise.example/cover',
            'https://noise.example/toc',
            'GOVPH',
            'TABLE OF CONTENTS',
            'SECTION 1 Means of egress shall comply.',
        ]),
        encoding='utf-8',
    )

    rc = run_dataset_source_to_graph_pipeline(dataset_manifest=str(manifest_path), dry_run=True, export_owl=False)
    assert rc == 0

    reports = sorted((tmp_path / '006_System-Manifests' / 'runs' / 'datasets' / 'demo-dataset' / 'source_to_graph').glob('*/source_to_graph_run_report.json'))
    report = json.loads(reports[0].read_text(encoding='utf-8'))
    summary = report['source_quality_summary']
    assert summary['severity_counts']['high'] == 1
    assert summary['high_severity_paths'] == ['001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md']
    assert summary['manual_review_required_paths'] == ['001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md']
    assert summary['benchmark_source_hints'] == [
        {
            'label': 'BFP RA 9514 revised IRR page',
            'url': 'https://bfp.gov.ph/revised-irr-of-ra-9514-the-fire-code-of-the-philippines/',
            'note': 'Official BFP page for the revised IRR; useful when scanned/local extraction is noisy.',
        }
    ]
    assert report['stage_results'][0]['source_quality']['manual_review_recommended'] is True


def test_run_dataset_source_to_graph_pipeline_normalizes_prefixed_refined_paths(tmp_path, monkeypatch) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    import vitruvius.dataset_pipeline as dp

    calls = []
    monkeypatch.setattr(dp, 'run_canonicalize_one', lambda **kwargs: calls.append(kwargs['relative_markdown_path']) or 0)

    def fake_extract(**kwargs):
        kwargs['json_output_path'].write_text(json.dumps({'generated_at':'x','source':kwargs['relative_markdown_path'],'source_id':kwargs['source_id_override'],'total_sections':0,'total_relationships':0,'relationships':[]}), encoding='utf-8')
        kwargs['txt_output_path'].write_text('ok', encoding='utf-8')
        return 0

    monkeypatch.setattr(dp, 'run_extract_relationships_sections_one_inner', fake_extract)

    def fake_review_noop(**kwargs):
        kwargs['review_json_path'].write_text('{}', encoding='utf-8')
        kwargs['review_txt_path'].write_text('ok', encoding='utf-8')
        kwargs['triage_report_path'].write_text('{}', encoding='utf-8')
        kwargs['high_confidence_output_path'].write_text(json.dumps({'generated_at':'x','source_report_generated_at':'x','source_model':'x','source':'x','threshold':0.9,'count':0,'candidates':[]}), encoding='utf-8')
        return 0

    monkeypatch.setattr(dp, 'run_review_relationships_ollama', fake_review_noop)

    monkeypatch.setattr(dp, 'run_promote_inner', lambda **kwargs: {'created': 0, 'rejected': 0, 'errors': []})
    monkeypatch.setattr(dp, 'run_build_graph', lambda **kwargs: print(json.dumps({'run_id':'x','snapshot_path':'a','build_report_path':'b'})) or 0)
    monkeypatch.setattr(dp, 'run_export_graph_owl', lambda **kwargs: 0)
    monkeypatch.setattr(dp, 'run_query_structured', lambda **kwargs: 0)

    rc = dp.run_dataset_source_to_graph_pipeline(dataset_manifest=str(manifest_path), export_owl=False)
    assert rc == 0
    assert calls == ['001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md']


def test_run_dataset_source_to_graph_pipeline_dedupes_generated_relationship_paths(tmp_path, monkeypatch) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    import vitruvius.dataset_pipeline as dp

    monkeypatch.setattr(dp, 'run_canonicalize_one', lambda **kwargs: 0)

    def fake_extract(**kwargs):
        kwargs['json_output_path'].write_text(json.dumps({'generated_at':'x','source':kwargs['relative_markdown_path'],'source_id':kwargs['source_id_override'],'total_sections':0,'total_relationships':0,'relationships':[]}), encoding='utf-8')
        kwargs['txt_output_path'].write_text('ok', encoding='utf-8')
        return 0

    def fake_review(**kwargs):
        kwargs['review_json_path'].write_text('{}', encoding='utf-8')
        kwargs['review_txt_path'].write_text('ok', encoding='utf-8')
        kwargs['triage_report_path'].write_text('{}', encoding='utf-8')
        kwargs['high_confidence_output_path'].write_text(json.dumps({'generated_at':'x','source_report_generated_at':'x','source_model':'x','source':'x','threshold':0.9,'count':0,'candidates':[]}), encoding='utf-8')
        return 0

    def fake_promote(**kwargs):
        rel_dir = kwargs['relationships_output_dir']
        rel_dir.mkdir(parents=True, exist_ok=True)
        rel_path = rel_dir / 'rel-generated.md'
        rel_path.write_text(
            '---\n'
            'id: rel-generated\n'
            'page_type: relationship\n'
            'relationship_type: governs\n'
            'from_entity: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
            'to_entity: concept-means-of-egress\n'
            'canonical_status: promoted\n'
            'evidence:\n'
            '- source_id: irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines\n'
            '  source_section_id: section-1\n'
            '  evidence_snippet: means of egress\n'
            '  reviewer_confidence: 0.95\n'
            '---\n\n# body\n',
            encoding='utf-8',
        )
        kwargs['audit_log_path'].write_text('audit', encoding='utf-8')
        return {'created': 1, 'rejected': 0, 'errors': []}

    monkeypatch.setattr(dp, 'run_extract_relationships_sections_one_inner', fake_extract)
    monkeypatch.setattr(dp, 'run_review_relationships_ollama', fake_review)
    monkeypatch.setattr(dp, 'run_promote_inner', fake_promote)
    monkeypatch.setattr(dp, 'run_build_graph', lambda **kwargs: print(json.dumps({'run_id':'x','snapshot_path':'a','build_report_path':'b'})) or 0)
    monkeypatch.setattr(dp, 'run_export_graph_owl', lambda **kwargs: 0)
    monkeypatch.setattr(dp, 'run_query_structured', lambda **kwargs: 0)

    # duplicate the refined path intentionally to prove dedupe behavior
    payload = yaml.safe_load(Path(manifest_path).read_text(encoding='utf-8'))
    payload['law_units'][0]['refined_markdown_paths'].append(payload['law_units'][0]['refined_markdown_paths'][0])
    Path(manifest_path).write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')

    rc = dp.run_dataset_source_to_graph_pipeline(dataset_manifest=str(manifest_path), export_owl=False)
    assert rc == 0
    reports = sorted((tmp_path / '006_System-Manifests' / 'runs' / 'datasets' / 'demo-dataset' / 'source_to_graph').glob('*/source_to_graph_run_report.json'))
    report = json.loads(reports[0].read_text(encoding='utf-8'))
    derived_manifest = tmp_path / report['derived_manifest_path']
    derived_payload = yaml.safe_load(derived_manifest.read_text(encoding='utf-8'))
    rel_paths = [entry['path'] for entry in derived_payload['relationship_input_manifest']['relationships'] if entry['path'].endswith('rel-generated.md')]
    assert len(rel_paths) == 1


def test_source_quality_summary_aggregates_benchmark_hints() -> None:
    from vitruvius.dataset_pipeline import _source_quality_summary

    summary = _source_quality_summary([
        {
            'source_id': 'source-a',
            'normalized_refined_markdown_path': 'a.md',
            'source_quality': {
                'severity': 'high',
                'manual_review_recommended': True,
                'recommendations': ['manual review'],
                'image_line_count': 12,
                'table_line_count': 34,
                'noise_line_count': 1,
                'structural_heading_count': 5,
                'useful_text_ratio': 0.71,
                'benchmark_source_hints': [
                    {'label': 'Hint A', 'url': 'https://example.com/a', 'note': 'a'},
                    {'label': 'Hint B', 'url': 'https://example.com/b', 'note': 'b'},
                ],
            },
        },
        {
            'source_id': 'source-b',
            'normalized_refined_markdown_path': 'b.md',
            'source_quality': {
                'severity': 'medium',
                'manual_review_recommended': False,
                'recommendations': ['watch closely'],
                'image_line_count': 0,
                'table_line_count': 10,
                'noise_line_count': 0,
                'structural_heading_count': 8,
                'useful_text_ratio': 0.91,
                'benchmark_source_hints': [
                    {'label': 'Hint A', 'url': 'https://example.com/a', 'note': 'a'},
                ],
            },
        },
    ])
    assert summary['severity_counts']['high'] == 1
    assert summary['severity_counts']['medium'] == 1
    assert summary['manual_review_required_paths'] == ['a.md']
    assert len(summary['benchmark_source_hints']) == 2


def test_source_quality_summary_dedupes_repeated_high_severity_paths() -> None:
    from vitruvius.dataset_pipeline import _source_quality_summary

    summary = _source_quality_summary([
        {
            'normalized_refined_markdown_path': 'a.md',
            'source_quality': {
                'severity': 'high',
                'manual_review_recommended': True,
                'benchmark_source_hints': [],
            },
        },
        {
            'normalized_refined_markdown_path': 'a.md',
            'source_quality': {
                'severity': 'high',
                'manual_review_recommended': True,
                'benchmark_source_hints': [],
            },
        },
    ])

    assert summary['severity_counts']['high'] == 2
    assert summary['high_severity_paths'] == ['a.md']
    assert summary['manual_review_required_paths'] == ['a.md']


def test_run_dataset_source_to_graph_pipeline_dry_run_rejects_visualize_flags(tmp_path, monkeypatch, capsys) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    rc = run_dataset_source_to_graph_pipeline(
        dataset_manifest=str(manifest_path),
        dry_run=True,
        visualize_graph=True,
        export_owl=False,
    )
    assert rc == 2
    payload = json.loads(capsys.readouterr().out)
    assert "--visualize / --open-browser" in payload["error"]


def test_run_dataset_source_to_graph_pipeline_can_visualize_and_open_browser(tmp_path, monkeypatch, capsys) -> None:
    manifest_path = _seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    import vitruvius.dataset_pipeline as dp
    import vitruvius.graph.visualize as visualize_mod

    monkeypatch.setattr(dp, 'run_canonicalize_one', lambda **kwargs: 0)

    def fake_extract(**kwargs):
        kwargs['json_output_path'].write_text(json.dumps({
            'generated_at': 'x',
            'source': kwargs['relative_markdown_path'],
            'source_id': kwargs['source_id_override'],
            'total_sections': 0,
            'total_relationships': 0,
            'relationships': [],
        }), encoding='utf-8')
        kwargs['txt_output_path'].write_text('ok', encoding='utf-8')
        return 0

    def fake_review(**kwargs):
        kwargs['review_json_path'].write_text('{}', encoding='utf-8')
        kwargs['review_txt_path'].write_text('ok', encoding='utf-8')
        kwargs['triage_report_path'].write_text('{}', encoding='utf-8')
        kwargs['high_confidence_output_path'].write_text(json.dumps({
            'generated_at': 'x',
            'source_report_generated_at': 'x',
            'source_model': 'x',
            'source': 'x',
            'threshold': 0.9,
            'count': 0,
            'candidates': [],
        }), encoding='utf-8')
        return 0

    def fake_promote(**kwargs):
        rel_dir = kwargs['relationships_output_dir']
        rel_dir.mkdir(parents=True, exist_ok=True)
        rel_path = rel_dir / 'rel-generated.md'
        rel_path.write_text(
            '---\n'
            'id: rel-generated\n'
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
            '---\n\n# body\n',
            encoding='utf-8',
        )
        kwargs['audit_log_path'].write_text('audit', encoding='utf-8')
        return {'created': 1, 'rejected': 0, 'errors': []}

    monkeypatch.setattr(dp, 'run_extract_relationships_sections_one_inner', fake_extract)
    monkeypatch.setattr(dp, 'run_review_relationships_ollama', fake_review)
    monkeypatch.setattr(dp, 'run_promote_inner', fake_promote)
    monkeypatch.setattr(dp, 'run_build_graph', lambda **kwargs: print(json.dumps({
        'run_id': '20260416T111111Z',
        'snapshot_path': '005_Operational-Intelligence-Layer/graph/datasets/demo-dataset/20260416T111111Z_graph_snapshot.json',
        'build_report_path': '006_System-Manifests/runs/datasets/demo-dataset/20260416T111111Z_build_graph_dataset_report.json',
    })) or 0)
    monkeypatch.setattr(dp, 'run_export_graph_owl', lambda **kwargs: 0)
    monkeypatch.setattr(dp, 'run_query_structured', lambda **kwargs: 0)
    monkeypatch.setattr(visualize_mod, 'run_visualize_graph', lambda **kwargs: print(json.dumps({
        'action': 'visualize-graph',
        'snapshot_path': kwargs['snapshot_path'],
        'out_path': 'tmp/demo.html',
        'dataset_id': 'demo-dataset',
        'run_id': '20260416T111111Z',
        'node_count': 2,
        'edge_count': 1,
    })) or 0)

    opened: list[str] = []
    monkeypatch.setattr(dp.webbrowser, 'open', lambda url: opened.append(url) or True)

    rc = dp.run_dataset_source_to_graph_pipeline(
        dataset_manifest=str(manifest_path),
        export_owl=False,
        visualize_graph=True,
        open_browser=True,
    )

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload['visualization_html_path'] == 'tmp/demo.html'
    assert payload['browser_opened'] is True
    assert opened and opened[0].startswith('file://')
