from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .utils import utc_now_stamp


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise ValueError(f"expected YAML mapping in {path}")
    return payload


def dedupe_manifest_entries(entries: list[dict[str, Any]], *, keys: tuple[str, ...]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for entry in entries:
        value = tuple(str(entry.get(key) or '') for key in keys)
        if any(not part for part in value) or value in seen:
            continue
        seen.add(value)
        deduped.append(entry)
    return deduped


def completed_manifest_paths(
    *,
    repo_root: Path,
    completed_ledger_path: Path,
    manifest_index_path: Path,
    completed_lane_key: str = 'completed_lanes',
    lane_id_key: str = 'lane_id',
    manifest_list_key: str = 'manifests',
    manifest_path_key: str = 'manifest',
) -> list[Path]:
    completed_payload = load_yaml_payload(completed_ledger_path)
    completed_lane_ids = [
        str(item.get(lane_id_key))
        for item in completed_payload.get(completed_lane_key) or []
        if isinstance(item, dict) and isinstance(item.get(lane_id_key), str)
    ]
    manifest_index = load_yaml_payload(manifest_index_path)
    lane_to_manifest = {
        str(item.get(lane_id_key)): repo_root / str(item.get(manifest_path_key))
        for item in manifest_index.get(manifest_list_key) or []
        if isinstance(item, dict)
        and isinstance(item.get(lane_id_key), str)
        and isinstance(item.get(manifest_path_key), str)
    }
    return [manifest_path for lane_id in completed_lane_ids if (manifest_path := lane_to_manifest.get(lane_id)) is not None and manifest_path.exists()]


def build_completed_aggregate_manifest(
    *,
    repo_root: Path,
    manifest_paths: list[Path],
    out_manifest_path: Path,
    dataset_id: str,
    dataset_kind: str,
    graph_output_root: str,
    run_output_root: str,
    query_snapshot_path_template: str,
    scope_notes: list[str],
    lane_note_builder,
    folder_name_resolver,
) -> dict[str, Any]:
    source_entries: list[dict[str, Any]] = []
    concept_entries: list[dict[str, Any]] = []
    relationship_entries: list[dict[str, Any]] = []
    raw_anchor_by_folder: dict[str, dict[str, Any]] = {}
    law_units: list[dict[str, Any]] = []
    seen_law_ids: set[str] = set()

    for manifest_path in manifest_paths:
        payload = load_yaml_payload(manifest_path)
        lane_id = manifest_path.stem
        if isinstance(payload.get('law_units'), list):
            raw_slice_anchors = payload.get('raw_slice_anchors') or []
            if isinstance(raw_slice_anchors, list):
                for anchor in raw_slice_anchors:
                    if not isinstance(anchor, dict):
                        continue
                    folder_name = str(anchor.get('folder_name') or '')
                    raw_root = str(anchor.get('raw_root') or '')
                    if not folder_name or not raw_root:
                        continue
                    aggregate_anchor = raw_anchor_by_folder.setdefault(
                        folder_name,
                        {
                            'folder_name': folder_name,
                            'raw_root': raw_root,
                            'entry_role': anchor.get('entry_role', 'authoritative'),
                            'authority_tier': anchor.get('authority_tier', 'primary'),
                            'variant_family': f'{dataset_id}-aggregate',
                            'edition_or_source_note': f'{dataset_id} aggregate raw anchor grouping.',
                            'include_in_m1': True,
                            'reason': lane_note_builder(lane_id),
                            'classified_raw_entries': [],
                        },
                    )
                    existing_paths = {
                        str(item.get('path'))
                        for item in aggregate_anchor.get('classified_raw_entries', [])
                        if isinstance(item, dict) and isinstance(item.get('path'), str)
                    }
                    for classified in anchor.get('classified_raw_entries') or []:
                        if not isinstance(classified, dict):
                            continue
                        rel_path = classified.get('path')
                        if not isinstance(rel_path, str) or rel_path in existing_paths:
                            continue
                        aggregate_anchor['classified_raw_entries'].append(classified)
                        existing_paths.add(rel_path)

            canonical_input = payload.get('canonical_input_manifest') or {}
            if isinstance(canonical_input, dict):
                source_entries.extend([
                    entry for entry in canonical_input.get('sources') or []
                    if isinstance(entry, dict) and isinstance(entry.get('path'), str)
                ])
                concept_entries.extend([
                    entry for entry in canonical_input.get('concepts') or []
                    if isinstance(entry, dict) and isinstance(entry.get('path'), str)
                ])

            relationship_input = payload.get('relationship_input_manifest') or {}
            if isinstance(relationship_input, dict):
                relationship_entries.extend([
                    entry for entry in relationship_input.get('relationships') or []
                    if isinstance(entry, dict) and isinstance(entry.get('path'), str)
                ])

            for index, law_unit in enumerate(payload.get('law_units') or [], start=1):
                if not isinstance(law_unit, dict):
                    continue
                unit = dict(law_unit)
                law_id = str(unit.get('law_id') or f'{lane_id}-{index}')
                while law_id in seen_law_ids:
                    law_id = f'{law_id}-{index}'
                seen_law_ids.add(law_id)
                unit['law_id'] = law_id
                notes = [str(note) for note in unit.get('scope_notes') or [] if isinstance(note, str)]
                lane_note = lane_note_builder(lane_id)
                if lane_note not in notes:
                    notes.append(lane_note)
                unit['scope_notes'] = notes
                law_units.append(unit)
            continue

        for index, item in enumerate(payload.get('candidate_law_folders') or [], start=1):
            if not isinstance(item, dict):
                continue
            raw_folder_name = folder_name_resolver(item)
            raw_anchor_paths = [str(path) for path in item.get('raw_anchor_paths') or [] if isinstance(path, str)]
            authoritative_variant_paths = [str(path) for path in item.get('authoritative_variant_paths') or [] if isinstance(path, str)]
            excluded_variant_paths = [str(path) for path in item.get('excluded_variant_paths') or [] if isinstance(path, str)]
            refined_markdown_paths = [str(path) for path in item.get('refined_markdown_paths') or [] if isinstance(path, str)]
            admitted_source_paths = [str(path) for path in item.get('admitted_source_paths') or [] if isinstance(path, str)]
            admitted_concept_paths = [str(path) for path in item.get('admitted_concept_paths') or [] if isinstance(path, str)]
            admitted_relationship_paths = [str(path) for path in item.get('admitted_relationship_paths') or [] if isinstance(path, str)]
            verification_checks = [str(v) for v in item.get('verification_checks') or [] if isinstance(v, str)]
            scope_notes_item = [str(v) for v in item.get('scope_notes') or [] if isinstance(v, str)]
            aggregate_anchor = raw_anchor_by_folder.setdefault(
                raw_folder_name,
                {
                    'folder_name': raw_folder_name,
                    'raw_root': f'001_Raw-Source-Layer/001-Laws/{raw_folder_name}',
                    'entry_role': 'authoritative',
                    'authority_tier': 'primary',
                    'variant_family': f'{dataset_id}-aggregate',
                    'edition_or_source_note': f'{dataset_id} aggregate raw anchor grouping.',
                    'include_in_m1': True,
                    'reason': lane_note_builder(lane_id),
                    'classified_raw_entries': [],
                },
            )
            existing_paths = {
                str(entry.get('path'))
                for entry in aggregate_anchor.get('classified_raw_entries', [])
                if isinstance(entry, dict) and isinstance(entry.get('path'), str)
            }
            for rel_path in authoritative_variant_paths or raw_anchor_paths:
                if rel_path in existing_paths:
                    continue
                aggregate_anchor['classified_raw_entries'].append({
                    'path': rel_path,
                    'folder_name': raw_folder_name,
                    'entry_role': 'authoritative',
                    'authority_tier': 'primary',
                    'variant_family': f'{dataset_id}-aggregate',
                    'edition_or_source_note': f'{dataset_id} aggregate member from {lane_id}.',
                    'include_in_m1': True,
                    'reason': lane_note_builder(lane_id),
                })
                existing_paths.add(rel_path)
            for rel_path in excluded_variant_paths:
                if rel_path in existing_paths:
                    continue
                aggregate_anchor['classified_raw_entries'].append({
                    'path': rel_path,
                    'folder_name': raw_folder_name,
                    'entry_role': 'reference',
                    'authority_tier': 'adjacent',
                    'variant_family': f'{dataset_id}-aggregate-excluded',
                    'edition_or_source_note': f'Excluded variant retained from {lane_id}.',
                    'include_in_m1': True,
                    'reason': f'Excluded aggregate variant from lane {lane_id}',
                })
                existing_paths.add(rel_path)

            for rel_path in admitted_source_paths:
                source_entries.append({
                    'path': rel_path,
                    'folder_name': raw_folder_name,
                    'entry_role': 'authoritative',
                    'authority_tier': 'primary',
                    'variant_family': f'{lane_id}-source',
                    'edition_or_source_note': f'{dataset_id} aggregate source from {lane_id}.',
                    'include_in_m1': True,
                    'reason': lane_note_builder(lane_id),
                })
            for rel_path in admitted_concept_paths:
                concept_entries.append({
                    'path': rel_path,
                    'folder_name': raw_folder_name,
                    'entry_role': 'derived',
                    'authority_tier': 'derived',
                    'variant_family': f'{lane_id}-concept',
                    'edition_or_source_note': f'{dataset_id} aggregate concept from {lane_id}.',
                    'include_in_m1': True,
                    'reason': lane_note_builder(lane_id),
                })
            for rel_path in admitted_relationship_paths:
                relationship_entries.append({
                    'path': rel_path,
                    'folder_name': raw_folder_name,
                    'entry_role': 'authoritative',
                    'authority_tier': 'approved',
                    'variant_family': f'{lane_id}-relationship',
                    'edition_or_source_note': f'{dataset_id} aggregate relationship from {lane_id}.',
                    'include_in_m1': True,
                    'reason': lane_note_builder(lane_id),
                })
            law_id = lane_id.replace('laws-tranche-', '').replace('laws-', '').replace('-remediation', '')
            if len(payload.get('candidate_law_folders') or []) > 1:
                law_id = f'{law_id}-{index}'
            while law_id in seen_law_ids:
                law_id = f'{law_id}-{index}'
            seen_law_ids.add(law_id)
            law_units.append({
                'law_id': law_id,
                'folder_name': raw_folder_name,
                'raw_anchor_paths': raw_anchor_paths or authoritative_variant_paths,
                'refined_markdown_paths': refined_markdown_paths,
                'authoritative_variant_paths': authoritative_variant_paths or raw_anchor_paths,
                'excluded_variant_paths': excluded_variant_paths,
                'admitted_source_paths': admitted_source_paths,
                'admitted_concept_paths': admitted_concept_paths,
                'admitted_relationship_paths': admitted_relationship_paths,
                'verification_checks': verification_checks,
                'scope_notes': [*scope_notes_item, lane_note_builder(lane_id)],
            })

    aggregate_payload = {
        'dataset_id': dataset_id,
        'dataset_kind': dataset_kind,
        'scope_notes': scope_notes,
        'raw_slice_anchors': list(raw_anchor_by_folder.values()),
        'canonical_input_manifest': {
            'sources': dedupe_manifest_entries(source_entries, keys=('path', 'folder_name')),
            'concepts': dedupe_manifest_entries(concept_entries, keys=('path', 'folder_name')),
        },
        'relationship_input_manifest': {
            'relationships': dedupe_manifest_entries(relationship_entries, keys=('path', 'folder_name')),
        },
        'graph_output_root': graph_output_root,
        'run_output_root': run_output_root,
        'query_snapshot_path_template': query_snapshot_path_template,
        'freshness_policy': {'mode': 'exact'},
        'pilot_gate': {
            'require_manifest_validation': True,
            'source_to_graph_execute_ready': False,
            'derived_from_tranche_id': f'{dataset_id}-aggregate',
            'derived_run_id': utc_now_stamp().split('T')[0],
        },
        'law_units': law_units,
    }
    out_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out_manifest_path.write_text(yaml.safe_dump(aggregate_payload, sort_keys=False), encoding='utf-8')
    return aggregate_payload


def print_aggregate_manifest_summary(*, repo_root: Path, out_manifest_path: Path, aggregate_payload: dict[str, Any]) -> None:
    print(json.dumps({
        'action': 'build-completed-aggregate-manifest',
        'dataset_manifest_path': str(out_manifest_path.relative_to(repo_root)),
        'law_unit_count': len(aggregate_payload['law_units']),
        'source_count': len(aggregate_payload['canonical_input_manifest']['sources']),
        'concept_count': len(aggregate_payload['canonical_input_manifest']['concepts']),
        'relationship_count': len(aggregate_payload['relationship_input_manifest']['relationships']),
        'raw_slice_anchor_count': len(aggregate_payload['raw_slice_anchors']),
    }, indent=2))


def build_generic_completed_aggregate_manifest(
    *,
    repo_root: Path,
    completed_ledger_path: Path,
    manifest_index_path: Path,
    out_manifest_path: Path,
    dataset_id: str,
    dataset_kind: str,
    graph_output_root: str,
    run_output_root: str,
    query_snapshot_path_template: str,
    scope_notes: list[str],
    lane_note_builder,
    folder_name_resolver,
) -> dict[str, Any]:
    manifest_paths = completed_manifest_paths(
        repo_root=repo_root,
        completed_ledger_path=completed_ledger_path,
        manifest_index_path=manifest_index_path,
    )
    if not manifest_paths:
        raise ValueError('no completed manifests found to aggregate')
    return build_completed_aggregate_manifest(
        repo_root=repo_root,
        manifest_paths=manifest_paths,
        out_manifest_path=out_manifest_path,
        dataset_id=dataset_id,
        dataset_kind=dataset_kind,
        graph_output_root=graph_output_root,
        run_output_root=run_output_root,
        query_snapshot_path_template=query_snapshot_path_template,
        scope_notes=scope_notes,
        lane_note_builder=lane_note_builder,
        folder_name_resolver=folder_name_resolver,
    )
