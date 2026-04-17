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


def write_yaml_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')


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


def load_completed_aggregate_profile(*, repo_root: Path, profile_path: Path) -> dict[str, Any]:
    resolved_profile_path = profile_path if profile_path.is_absolute() else repo_root / profile_path
    payload = load_yaml_payload(resolved_profile_path)
    required_keys = (
        'dataset_id',
        'dataset_kind',
        'completed_ledger',
        'manifest_index',
        'out_manifest',
        'graph_output_root',
        'run_output_root',
        'query_snapshot_template',
    )
    missing = [key for key in required_keys if not isinstance(payload.get(key), str) or not str(payload.get(key)).strip()]
    if missing:
        raise ValueError(f"aggregate profile missing required string keys: {', '.join(missing)}")
    payload['profile_path'] = str(resolved_profile_path)
    payload['scope_notes'] = [str(note) for note in payload.get('scope_notes') or [] if isinstance(note, str)]
    payload['lane_note_template'] = str(payload.get('lane_note_template') or 'Aggregate lane: {lane_id}')
    return payload


def load_completed_aggregate_profile_catalog(
    *,
    repo_root: Path,
    catalog_path: Path,
) -> dict[str, Any]:
    resolved_catalog_path = catalog_path if catalog_path.is_absolute() else repo_root / catalog_path
    payload = load_yaml_payload(resolved_catalog_path)
    profiles = payload.get('profiles')
    if not isinstance(profiles, list):
        raise ValueError("aggregate profile catalog must define a 'profiles' list")
    return {
        'catalog_path': str(resolved_catalog_path),
        'profiles': [item for item in profiles if isinstance(item, dict)],
    }


def resolve_completed_aggregate_profile_path(
    *,
    repo_root: Path,
    family: str,
    catalog_path: Path,
) -> Path:
    catalog = load_completed_aggregate_profile_catalog(repo_root=repo_root, catalog_path=catalog_path)
    for item in catalog['profiles']:
        if str(item.get('family') or '') != family:
            continue
        profile_path = item.get('profile')
        if not isinstance(profile_path, str) or not profile_path.strip():
            raise ValueError(f"aggregate profile catalog entry for family '{family}' is missing a profile path")
        resolved_profile_path = repo_root / profile_path
        if not resolved_profile_path.exists():
            raise ValueError(f"aggregate profile path for family '{family}' does not exist: {profile_path}")
        return resolved_profile_path
    raise ValueError(f"no aggregate profile registered for family '{family}'")


def register_completed_aggregate_family(
    *,
    repo_root: Path,
    family: str,
    profile_path: Path,
    catalog_path: Path,
    dataset_id: str,
    dataset_kind: str,
    completed_ledger: str,
    manifest_index: str,
    out_manifest: str,
    graph_output_root: str,
    run_output_root: str,
    query_snapshot_template: str,
    scope_notes: list[str] | None = None,
    lane_note_template: str | None = None,
    status: str = 'ready',
    note: str | None = None,
) -> tuple[Path, Path, dict[str, Any], dict[str, Any]]:
    if not family.strip():
        raise ValueError('family must not be empty')
    resolved_profile_path = profile_path if profile_path.is_absolute() else repo_root / profile_path
    resolved_catalog_path = catalog_path if catalog_path.is_absolute() else repo_root / catalog_path
    profile_payload: dict[str, Any] = {
        'dataset_id': dataset_id,
        'dataset_kind': dataset_kind,
        'completed_ledger': completed_ledger,
        'manifest_index': manifest_index,
        'out_manifest': out_manifest,
        'graph_output_root': graph_output_root,
        'run_output_root': run_output_root,
        'query_snapshot_template': query_snapshot_template,
    }
    if scope_notes:
        profile_payload['scope_notes'] = [str(note_item) for note_item in scope_notes if str(note_item).strip()]
    if lane_note_template:
        profile_payload['lane_note_template'] = lane_note_template
    write_yaml_payload(resolved_profile_path, profile_payload)

    if resolved_catalog_path.exists():
        catalog_payload = load_yaml_payload(resolved_catalog_path)
    else:
        catalog_payload = {'profiles': []}
    profiles = catalog_payload.get('profiles')
    if not isinstance(profiles, list):
        profiles = []

    normalized_profile_path = str(resolved_profile_path.relative_to(repo_root))
    new_entry: dict[str, Any] = {
        'family': family,
        'profile': normalized_profile_path,
        'status': status,
    }
    if note:
        new_entry['note'] = note

    updated_profiles: list[dict[str, Any]] = []
    replaced = False
    for item in profiles:
        if not isinstance(item, dict):
            continue
        if str(item.get('family') or '') == family:
            updated_profiles.append(new_entry)
            replaced = True
        else:
            updated_profiles.append(item)
    if not replaced:
        updated_profiles.append(new_entry)
    catalog_payload['profiles'] = sorted(
        updated_profiles,
        key=lambda item: (str(item.get('family') or '')),
    )
    write_yaml_payload(resolved_catalog_path, catalog_payload)
    return resolved_profile_path, resolved_catalog_path, profile_payload, new_entry


def scaffold_completed_aggregate_family(
    *,
    repo_root: Path,
    family: str,
    catalog_path: Path,
    dataset_id: str | None = None,
    dataset_kind: str = 'aggregate',
    profile_path: Path | None = None,
    completed_ledger_path: Path | None = None,
    manifest_index_path: Path | None = None,
    out_manifest: str | None = None,
    graph_output_root: str | None = None,
    run_output_root: str | None = None,
    query_snapshot_template: str | None = None,
    scope_notes: list[str] | None = None,
    lane_note_template: str | None = None,
    status: str = 'scaffolded',
    note: str | None = None,
) -> dict[str, Any]:
    normalized_family = family.strip()
    if not normalized_family:
        raise ValueError('family must not be empty')

    normalized_dataset_id = dataset_id or f'{normalized_family}-aggregate'
    normalized_profile_path = profile_path or Path(f'config/datasets/{normalized_family}-mvp-profile.yaml')
    normalized_completed_ledger_path = completed_ledger_path or Path(f'config/datasets/{normalized_family}-completed-lanes.yaml')
    normalized_manifest_index_path = manifest_index_path or Path(f'config/datasets/{normalized_family}-manifest-index.yaml')
    normalized_out_manifest = out_manifest or f'006_System-Manifests/runs/datasets/{normalized_dataset_id}/latest_dataset_manifest.yaml'
    normalized_graph_output_root = graph_output_root or f'005_Operational-Intelligence-Layer/graph/datasets/{normalized_dataset_id}'
    normalized_run_output_root = run_output_root or f'006_System-Manifests/runs/datasets/{normalized_dataset_id}'
    normalized_query_snapshot_template = query_snapshot_template or (
        f'005_Operational-Intelligence-Layer/graph/datasets/{normalized_dataset_id}' + '/{run_id}_graph_snapshot.json'
    )

    resolved_completed_ledger_path = (
        normalized_completed_ledger_path
        if normalized_completed_ledger_path.is_absolute()
        else repo_root / normalized_completed_ledger_path
    )
    resolved_manifest_index_path = (
        normalized_manifest_index_path
        if normalized_manifest_index_path.is_absolute()
        else repo_root / normalized_manifest_index_path
    )
    if not resolved_completed_ledger_path.exists():
        write_yaml_payload(resolved_completed_ledger_path, {'completed_lanes': []})
    if not resolved_manifest_index_path.exists():
        write_yaml_payload(resolved_manifest_index_path, {'manifests': []})

    resolved_profile_path, resolved_catalog_path, profile_payload, catalog_entry = register_completed_aggregate_family(
        repo_root=repo_root,
        family=normalized_family,
        profile_path=normalized_profile_path,
        catalog_path=catalog_path,
        dataset_id=normalized_dataset_id,
        dataset_kind=dataset_kind,
        completed_ledger=str(resolved_completed_ledger_path.relative_to(repo_root)),
        manifest_index=str(resolved_manifest_index_path.relative_to(repo_root)),
        out_manifest=normalized_out_manifest,
        graph_output_root=normalized_graph_output_root,
        run_output_root=normalized_run_output_root,
        query_snapshot_template=normalized_query_snapshot_template,
        scope_notes=scope_notes,
        lane_note_template=lane_note_template,
        status=status,
        note=note,
    )
    return {
        'family': normalized_family,
        'profile_path': resolved_profile_path,
        'catalog_path': resolved_catalog_path,
        'completed_ledger_path': resolved_completed_ledger_path,
        'manifest_index_path': resolved_manifest_index_path,
        'profile_payload': profile_payload,
        'catalog_entry': catalog_entry,
    }


def build_generic_completed_aggregate_manifest_from_profile(
    *,
    repo_root: Path,
    profile_path: Path,
) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    profile = load_completed_aggregate_profile(repo_root=repo_root, profile_path=profile_path)
    completed_ledger_path = repo_root / str(profile['completed_ledger'])
    manifest_index_path = repo_root / str(profile['manifest_index'])
    out_manifest_path = repo_root / str(profile['out_manifest'])
    lane_note_template = str(profile['lane_note_template'])
    aggregate_payload = build_generic_completed_aggregate_manifest(
        repo_root=repo_root,
        completed_ledger_path=completed_ledger_path,
        manifest_index_path=manifest_index_path,
        out_manifest_path=out_manifest_path,
        dataset_id=str(profile['dataset_id']),
        dataset_kind=str(profile['dataset_kind']),
        graph_output_root=str(profile['graph_output_root']),
        run_output_root=str(profile['run_output_root']),
        query_snapshot_path_template=str(profile['query_snapshot_template']),
        scope_notes=list(profile['scope_notes']),
        lane_note_builder=lambda lane_id: lane_note_template.format(lane_id=lane_id),
        folder_name_resolver=lambda item: str(item.get('raw_folder_name') or item.get('folder_name') or ''),
    )
    return out_manifest_path, aggregate_payload, profile


def run_generic_completed_aggregate_from_profile(
    *,
    repo_root: Path,
    profile_path: Path,
    dry_run: bool = False,
    review_preset: str | None = None,
    review_model: str | None = None,
    review_timeout_seconds: int | None = None,
    review_parallelism: int | None = None,
    export_owl: bool = True,
) -> int:
    from .dataset_pipeline import run_dataset_source_to_graph_pipeline

    out_manifest_path, aggregate_payload, _profile = build_generic_completed_aggregate_manifest_from_profile(
        repo_root=repo_root,
        profile_path=profile_path,
    )
    print_aggregate_manifest_summary(
        repo_root=repo_root,
        out_manifest_path=out_manifest_path,
        aggregate_payload=aggregate_payload,
    )
    return run_dataset_source_to_graph_pipeline(
        dataset_manifest=str(out_manifest_path.relative_to(repo_root)),
        dry_run=dry_run,
        review_preset=review_preset,
        review_model=review_model,
        review_timeout_seconds=review_timeout_seconds,
        review_parallelism=review_parallelism,
        export_owl=export_owl,
    )
