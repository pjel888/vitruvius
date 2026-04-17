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


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


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


def admit_completed_manifest_to_family(
    *,
    repo_root: Path,
    family: str,
    catalog_path: Path,
    lane_id: str,
    manifest_path: Path,
) -> dict[str, Any]:
    normalized_lane_id = lane_id.strip()
    if not normalized_lane_id:
        raise ValueError('lane_id must not be empty')
    resolved_profile_path = resolve_completed_aggregate_profile_path(
        repo_root=repo_root,
        family=family,
        catalog_path=catalog_path,
    )
    profile = load_completed_aggregate_profile(repo_root=repo_root, profile_path=resolved_profile_path)
    completed_ledger_path = repo_root / str(profile['completed_ledger'])
    manifest_index_path = repo_root / str(profile['manifest_index'])
    resolved_manifest_path = manifest_path if manifest_path.is_absolute() else repo_root / manifest_path
    if not resolved_manifest_path.exists():
        raise ValueError(f'manifest path does not exist: {resolved_manifest_path}')

    completed_payload = load_yaml_payload(completed_ledger_path)
    completed_lanes = completed_payload.get('completed_lanes')
    if not isinstance(completed_lanes, list):
        completed_lanes = []
    if normalized_lane_id not in {
        str(item.get('lane_id') or '')
        for item in completed_lanes
        if isinstance(item, dict)
    }:
        completed_lanes.append({'lane_id': normalized_lane_id})
    completed_payload['completed_lanes'] = sorted(
        [item for item in completed_lanes if isinstance(item, dict) and str(item.get('lane_id') or '').strip()],
        key=lambda item: str(item.get('lane_id') or ''),
    )
    write_yaml_payload(completed_ledger_path, completed_payload)

    manifest_index_payload = load_yaml_payload(manifest_index_path)
    manifests = manifest_index_payload.get('manifests')
    if not isinstance(manifests, list):
        manifests = []
    normalized_manifest_rel = str(resolved_manifest_path.relative_to(repo_root))
    updated_manifests: list[dict[str, Any]] = []
    replaced = False
    for item in manifests:
        if not isinstance(item, dict):
            continue
        if str(item.get('lane_id') or '') == normalized_lane_id:
            updated_manifests.append({'lane_id': normalized_lane_id, 'manifest': normalized_manifest_rel})
            replaced = True
        else:
            updated_manifests.append(item)
    if not replaced:
        updated_manifests.append({'lane_id': normalized_lane_id, 'manifest': normalized_manifest_rel})
    manifest_index_payload['manifests'] = sorted(
        [
            item for item in updated_manifests
            if isinstance(item, dict)
            and str(item.get('lane_id') or '').strip()
            and str(item.get('manifest') or '').strip()
        ],
        key=lambda item: str(item.get('lane_id') or ''),
    )
    write_yaml_payload(manifest_index_path, manifest_index_payload)
    return {
        'family': family,
        'profile_path': resolved_profile_path,
        'completed_ledger_path': completed_ledger_path,
        'manifest_index_path': manifest_index_path,
        'lane_id': normalized_lane_id,
        'manifest_path': resolved_manifest_path,
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


def check_completed_aggregate_family_readiness(
    *,
    repo_root: Path,
    family: str,
    catalog_path: Path,
) -> dict[str, Any]:
    from .graph.dataset_manifest import DatasetManifestError, load_dataset_manifest

    resolved_profile_path = resolve_completed_aggregate_profile_path(
        repo_root=repo_root,
        family=family,
        catalog_path=catalog_path,
    )
    profile = load_completed_aggregate_profile(repo_root=repo_root, profile_path=resolved_profile_path)
    completed_ledger_path = repo_root / str(profile['completed_ledger'])
    manifest_index_path = repo_root / str(profile['manifest_index'])
    completed_payload = load_yaml_payload(completed_ledger_path)
    completed_lane_count = len([
        item for item in completed_payload.get('completed_lanes') or []
        if isinstance(item, dict) and str(item.get('lane_id') or '').strip()
    ])
    manifest_paths = completed_manifest_paths(
        repo_root=repo_root,
        completed_ledger_path=completed_ledger_path,
        manifest_index_path=manifest_index_path,
    )

    blockers: list[str] = []
    if completed_lane_count == 0:
        blockers.append('no completed lanes admitted')
    if not manifest_paths:
        blockers.append('no completed manifests resolved from ledger/index')

    aggregate_payload: dict[str, Any] | None = None
    out_manifest_path = repo_root / str(profile['out_manifest'])
    aggregate_error: str | None = None
    dataset_manifest_valid = False
    dataset_manifest_error: str | None = None
    if not blockers:
        try:
            out_manifest_path, aggregate_payload, _profile = build_generic_completed_aggregate_manifest_from_profile(
                repo_root=repo_root,
                profile_path=resolved_profile_path,
            )
            try:
                load_dataset_manifest(out_manifest_path, repo_root)
                dataset_manifest_valid = True
            except DatasetManifestError as exc:
                dataset_manifest_error = str(exc)
                blockers.append(f'dataset manifest invalid: {dataset_manifest_error}')
        except Exception as exc:  # noqa: BLE001
            aggregate_error = str(exc)
            blockers.append(f'aggregate build failed: {aggregate_error}')

    source_count = 0
    concept_count = 0
    relationship_count = 0
    raw_slice_anchor_count = 0
    law_unit_count = 0
    if aggregate_payload is not None:
        source_count = len(aggregate_payload['canonical_input_manifest']['sources'])
        concept_count = len(aggregate_payload['canonical_input_manifest']['concepts'])
        relationship_count = len(aggregate_payload['relationship_input_manifest']['relationships'])
        raw_slice_anchor_count = len(aggregate_payload['raw_slice_anchors'])
        law_unit_count = len(aggregate_payload['law_units'])
        if raw_slice_anchor_count == 0:
            blockers.append('aggregate manifest has no raw slice anchors')
        if source_count == 0:
            blockers.append('aggregate manifest has no canonical sources')
        if relationship_count == 0:
            blockers.append('aggregate manifest has no relationship inputs')

    return {
        'family': family,
        'profile_path': str(resolved_profile_path.relative_to(repo_root)),
        'completed_ledger_path': str(completed_ledger_path.relative_to(repo_root)),
        'manifest_index_path': str(manifest_index_path.relative_to(repo_root)),
        'completed_lane_count': completed_lane_count,
        'resolved_manifest_count': len(manifest_paths),
        'law_unit_count': law_unit_count,
        'source_count': source_count,
        'concept_count': concept_count,
        'relationship_count': relationship_count,
        'raw_slice_anchor_count': raw_slice_anchor_count,
        'ready_to_run': not blockers and dataset_manifest_valid,
        'blockers': blockers,
        'aggregate_manifest_path': (
            str(out_manifest_path.relative_to(repo_root))
            if aggregate_payload is not None and out_manifest_path.exists()
            else None
        ),
        'aggregate_build_error': aggregate_error,
        'dataset_manifest_valid': dataset_manifest_valid,
        'dataset_manifest_error': dataset_manifest_error,
    }


def inspect_completed_aggregate_lane_sources(
    *,
    repo_root: Path,
    manifest_path: Path,
    sample_pages: int = 5,
) -> dict[str, Any]:
    from .constants import CONVERSION_LAYER_NAME, RAW_LAYER_NAME
    from .conversion import SUPPORTED_DIRECT_INPUT_EXTENSIONS
    from .detection import detect_pdf_type
    from .paths import build_conversion_relative_paths, build_ocr_pdf_relative_path

    resolved_manifest_path = manifest_path if manifest_path.is_absolute() else repo_root / manifest_path
    payload = load_yaml_payload(resolved_manifest_path)
    raw_slice = payload.get('raw_slice_anchors')
    if not isinstance(raw_slice, list) or not raw_slice:
        raise ValueError('lane manifest requires non-empty raw_slice_anchors for source inspection')

    selected_files: list[Path] = []
    seen: set[Path] = set()
    for anchor in raw_slice:
        if not isinstance(anchor, dict):
            continue
        for item in anchor.get('classified_raw_entries') or []:
            if not isinstance(item, dict):
                continue
            rel_path = item.get('path')
            if not isinstance(rel_path, str) or not rel_path.strip():
                continue
            abs_path = (repo_root / rel_path).resolve()
            if abs_path.is_file() and abs_path not in seen:
                seen.add(abs_path)
                selected_files.append(abs_path)

    if not selected_files:
        raise ValueError('lane manifest raw_slice_anchors/classified_raw_entries resolved no existing files')

    file_reports: list[dict[str, Any]] = []
    supported_direct_input_count = 0
    text_pdf_count = 0
    likely_scanned_count = 0
    ocr_required_count = 0
    refined_markdown_ready_count = 0

    for file_path in selected_files:
        rel_repo = _relative(file_path, repo_root)
        rel_raw = file_path.relative_to(repo_root / RAW_LAYER_NAME).as_posix()
        ext = file_path.suffix.lower()
        supported = ext in SUPPORTED_DIRECT_INPUT_EXTENSIONS
        detection: dict[str, Any] | None = None
        detection_error: str | None = None
        expected_raw_markdown_path: str | None = None
        expected_sidecar_json_path: str | None = None
        expected_refined_markdown_path: str | None = None
        expected_ocr_pdf_path: str | None = None
        refined_markdown_exists = False

        if supported:
            supported_direct_input_count += 1
            markdown_path_rel, json_path_rel = build_conversion_relative_paths(rel_raw)
            refined_path_rel = Path(*[
                'refined_markdown' if part == 'raw_markdown' else part
                for part in markdown_path_rel.parts
            ])
            ocr_pdf_path_rel = build_ocr_pdf_relative_path(rel_raw)
            expected_raw_markdown_path = (Path(CONVERSION_LAYER_NAME) / markdown_path_rel).as_posix()
            expected_sidecar_json_path = (Path(CONVERSION_LAYER_NAME) / json_path_rel).as_posix()
            expected_refined_markdown_path = (Path(CONVERSION_LAYER_NAME) / refined_path_rel).as_posix()
            expected_ocr_pdf_path = (Path(CONVERSION_LAYER_NAME) / ocr_pdf_path_rel).as_posix()
            refined_markdown_exists = (repo_root / expected_refined_markdown_path).exists()
            if refined_markdown_exists:
                refined_markdown_ready_count += 1

        if ext == '.pdf':
            try:
                detection = detect_pdf_type(file_path, sample_pages=sample_pages)
                if detection.get('result') == 'TEXT_PDF':
                    text_pdf_count += 1
                if detection.get('result') == 'LIKELY_SCANNED_PDF':
                    likely_scanned_count += 1
                if detection.get('recommended_route') != 'OPENDATALOADER_DIRECT':
                    ocr_required_count += 1
            except Exception as exc:  # noqa: BLE001
                detection_error = str(exc)

        file_reports.append({
            'raw_path': rel_repo,
            'extension': ext,
            'supported_direct_input': supported,
            'detection_result': detection.get('result') if detection else None,
            'recommended_route': detection.get('recommended_route') if detection else None,
            'detection_error': detection_error,
            'expected_raw_markdown_path': expected_raw_markdown_path,
            'expected_sidecar_json_path': expected_sidecar_json_path,
            'expected_refined_markdown_path': expected_refined_markdown_path,
            'expected_ocr_pdf_path': expected_ocr_pdf_path,
            'refined_markdown_exists': refined_markdown_exists,
        })

    return {
        'manifest_path': _relative(resolved_manifest_path, repo_root),
        'dataset_id': str(payload.get('dataset_id') or ''),
        'dataset_kind': str(payload.get('dataset_kind') or ''),
        'raw_file_count': len(selected_files),
        'supported_direct_input_count': supported_direct_input_count,
        'text_pdf_count': text_pdf_count,
        'likely_scanned_count': likely_scanned_count,
        'ocr_required_count': ocr_required_count,
        'refined_markdown_ready_count': refined_markdown_ready_count,
        'file_reports': file_reports,
    }


def prepare_completed_aggregate_lane_sources(
    *,
    repo_root: Path,
    manifest_path: Path,
    sample_pages: int = 5,
    allow_ocr: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    from .laws_readiness import _prepare_raw_file, _raw_file_preparation_summary

    resolved_manifest_path = manifest_path if manifest_path.is_absolute() else repo_root / manifest_path
    payload = load_yaml_payload(resolved_manifest_path)
    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    dataset_id = str(payload.get('dataset_id') or resolved_manifest_path.stem)
    run_output_root_rel = str(payload.get('run_output_root') or f'006_System-Manifests/runs/datasets/{dataset_id}')
    run_output_root = repo_root / run_output_root_rel
    report_path = run_output_root / 'source_prep' / run_id / 'completed_aggregate_lane_source_prep_report.json'

    raw_slice = payload.get('raw_slice_anchors')
    if not isinstance(raw_slice, list) or not raw_slice:
        raise ValueError('lane manifest requires non-empty raw_slice_anchors for source preparation')

    selected_files: list[Path] = []
    seen: set[Path] = set()
    for anchor in raw_slice:
        if not isinstance(anchor, dict):
            continue
        for item in anchor.get('classified_raw_entries') or []:
            if not isinstance(item, dict):
                continue
            rel_path = item.get('path')
            if not isinstance(rel_path, str) or not rel_path.strip():
                continue
            abs_path = (repo_root / rel_path).resolve()
            if abs_path.is_file() and abs_path not in seen:
                seen.add(abs_path)
                selected_files.append(abs_path)

    if not selected_files:
        raise ValueError('lane manifest raw_slice_anchors/classified_raw_entries resolved no existing files')

    file_reports: list[dict[str, Any]] = []
    raw_file_count = len(selected_files)
    supported_direct_input_count = 0
    prepared_count = 0
    ocr_required_count = 0
    failed_count = 0

    for file_path in selected_files:
        if dry_run:
            file_report = _raw_file_preparation_summary(
                repo_root=repo_root,
                file_path=file_path,
                sample_pages=sample_pages,
            )
        else:
            file_report = _prepare_raw_file(
                repo_root=repo_root,
                file_path=file_path,
                sample_pages=sample_pages,
                allow_ocr=allow_ocr,
            )
        file_reports.append(file_report)
        if file_report.get('supported_direct_input'):
            supported_direct_input_count += 1
        status = str(file_report.get('status') or '')
        if dry_run:
            if file_report.get('recommended_route') and file_report.get('recommended_route') != 'OPENDATALOADER_DIRECT':
                ocr_required_count += 1
        else:
            if status == 'prepared':
                prepared_count += 1
            elif status == 'ocr_required':
                ocr_required_count += 1
            elif status.endswith('_failed') or status == 'detection_failed':
                failed_count += 1

    summary = {
        'action': 'prepare-completed-aggregate-lane-sources' if not dry_run else 'prepare-completed-aggregate-lane-sources-dry-run',
        'dataset_id': dataset_id,
        'manifest_path': _relative(resolved_manifest_path, repo_root),
        'run_id': run_id,
        'dry_run': dry_run,
        'allow_ocr': allow_ocr,
        'raw_file_count': raw_file_count,
        'supported_direct_input_count': supported_direct_input_count,
        'prepared_count': prepared_count if not dry_run else 0,
        'ocr_required_count': ocr_required_count,
        'failed_count': failed_count if not dry_run else 0,
        'report_path': _relative(report_path, repo_root),
        'files': file_reports,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary


def source_admit_completed_aggregate_lane_dry_run(
    *,
    repo_root: Path,
    manifest_path: Path,
    source_prep_report_path: Path | None = None,
) -> dict[str, Any]:
    from .laws_readiness import (
        _admission_status_for_folder,
        _candidate_source_page_plan,
        _next_step_for_admission_status,
        _select_prepared_source_candidates,
    )

    resolved_manifest_path = manifest_path if manifest_path.is_absolute() else repo_root / manifest_path
    payload = load_yaml_payload(resolved_manifest_path)
    dataset_id = str(payload.get('dataset_id') or resolved_manifest_path.stem)
    run_output_root_rel = str(payload.get('run_output_root') or f'006_System-Manifests/runs/datasets/{dataset_id}')
    run_output_root = repo_root / run_output_root_rel

    if source_prep_report_path is None:
        candidates = sorted((run_output_root / 'source_prep').glob('*/completed_aggregate_lane_source_prep_report.json'))
        if not candidates:
            raise ValueError('no completed aggregate lane source-prep reports found; run prepare-completed-aggregate-lane-sources first')
        resolved_source_prep_report_path = candidates[-1]
    else:
        resolved_source_prep_report_path = (
            source_prep_report_path if source_prep_report_path.is_absolute() else repo_root / source_prep_report_path
        )
    source_prep_payload = json.loads(resolved_source_prep_report_path.read_text(encoding='utf-8'))
    files = source_prep_payload.get('files')
    if not isinstance(files, list):
        raise ValueError('source prep report requires a files list')

    prepared_files = [
        report for report in files
        if isinstance(report, dict) and (
            report.get('status') == 'prepared'
            or (
                source_prep_payload.get('dry_run') is True
                and report.get('supported_direct_input') is True
                and isinstance(report.get('expected_refined_markdown_path'), str)
            )
        )
    ]
    blocked_files = [
        report for report in files
        if isinstance(report, dict) and (
            report.get('status') == 'ocr_required'
            or (
                source_prep_payload.get('dry_run') is True
                and report.get('recommended_route')
                and report.get('recommended_route') != 'OPENDATALOADER_DIRECT'
            )
        )
    ]
    failed_files = [
        report for report in files
        if isinstance(report, dict) and str(report.get('status') or '').endswith('_failed')
    ]

    normalized_prepared_files: list[dict[str, Any]] = []
    for report in prepared_files:
        normalized = dict(report)
        if source_prep_payload.get('dry_run') is True:
            normalized.setdefault('status', 'prepared')
            normalized.setdefault('raw_path', report.get('raw_path'))
            if isinstance(report.get('expected_refined_markdown_path'), str):
                normalized['expected_refined_markdown_path'] = report.get('expected_refined_markdown_path')
        normalized_prepared_files.append(normalized)

    candidate_source_pages, excluded_prepared_file_reports, admission_guardrails = _select_prepared_source_candidates(
        repo_root=repo_root,
        prepared_files=normalized_prepared_files,
    )
    status = _admission_status_for_folder(
        candidate_source_pages=candidate_source_pages,
        blocked_file_reports=blocked_files,
        failed_file_reports=failed_files,
    )

    return {
        'action': 'source-admit-completed-aggregate-lane-dry-run',
        'dataset_id': dataset_id,
        'manifest_path': _relative(resolved_manifest_path, repo_root),
        'source_prep_report_path': _relative(resolved_source_prep_report_path, repo_root),
        'status': status,
        'candidate_source_page_count': len(candidate_source_pages),
        'candidate_source_pages': candidate_source_pages,
        'excluded_prepared_count': len(excluded_prepared_file_reports),
        'excluded_prepared_file_reports': excluded_prepared_file_reports,
        'blocked_file_reports': blocked_files,
        'failed_file_reports': failed_files,
        'admission_guardrails': admission_guardrails,
        'next_step': _next_step_for_admission_status(status),
    }


def scaffold_completed_aggregate_lane_manifest(
    *,
    repo_root: Path,
    family: str,
    catalog_path: Path,
    lane_id: str,
    raw_root: Path,
    out_manifest_path: Path | None = None,
    max_files: int = 5,
    extensions: list[str] | None = None,
) -> dict[str, Any]:
    if max_files <= 0:
        raise ValueError('max_files must be positive')
    normalized_lane_id = lane_id.strip()
    if not normalized_lane_id:
        raise ValueError('lane_id must not be empty')

    resolved_profile_path = resolve_completed_aggregate_profile_path(
        repo_root=repo_root,
        family=family,
        catalog_path=catalog_path,
    )
    profile = load_completed_aggregate_profile(repo_root=repo_root, profile_path=resolved_profile_path)
    resolved_raw_root = raw_root if raw_root.is_absolute() else repo_root / raw_root
    if not resolved_raw_root.exists() or not resolved_raw_root.is_dir():
        raise ValueError(f'raw_root is not a directory: {resolved_raw_root}')

    from .conversion import SUPPORTED_DIRECT_INPUT_EXTENSIONS

    allowed_extensions = {
        ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
        for ext in (extensions or list(SUPPORTED_DIRECT_INPUT_EXTENSIONS))
    }
    selected_files = [
        path for path in sorted(resolved_raw_root.iterdir())
        if path.is_file() and not path.name.startswith('.') and path.suffix.lower() in allowed_extensions
    ][:max_files]
    if not selected_files:
        raise ValueError('no raw files matched the requested root/extensions')

    resolved_out_manifest_path = (
        out_manifest_path
        if out_manifest_path is not None and out_manifest_path.is_absolute()
        else repo_root / (out_manifest_path or Path(f'config/datasets/{normalized_lane_id}.yaml'))
    )
    raw_root_rel = str(resolved_raw_root.relative_to(repo_root))
    classified_entries = []
    law_units = []
    for index, file_path in enumerate(selected_files, start=1):
        file_rel = str(file_path.relative_to(repo_root))
        classified_entries.append({
            'path': file_rel,
            'folder_name': family,
            'entry_role': 'authoritative',
            'authority_tier': 'primary',
            'variant_family': f'{normalized_lane_id}-starter',
            'edition_or_source_note': f'Starter lane scaffold from {file_path.name}.',
            'include_in_m1': True,
            'reason': f'Starter lane scaffold for {normalized_lane_id}',
        })
        law_units.append({
            'law_id': f'{normalized_lane_id}-{index}',
            'folder_name': family,
            'raw_anchor_paths': [file_rel],
            'refined_markdown_paths': [],
            'authoritative_variant_paths': [file_rel],
            'excluded_variant_paths': [],
            'admitted_source_paths': [],
            'admitted_concept_paths': [],
            'admitted_relationship_paths': [],
            'verification_checks': [],
            'scope_notes': [f'Starter lane scaffold from {file_path.name}'],
        })

    payload = {
        'dataset_id': normalized_lane_id,
        'dataset_kind': str(profile['dataset_kind']),
        'scope_notes': [
            f'Starter lane scaffold for family {family}.',
            f'Raw root: {raw_root_rel}.',
            'Canonical sources and relationship inputs still need truthful admission before execution.',
        ],
        'raw_slice_anchors': [
            {
                'folder_name': family,
                'raw_root': raw_root_rel,
                'entry_role': 'authoritative',
                'authority_tier': 'primary',
                'variant_family': f'{normalized_lane_id}-starter',
                'edition_or_source_note': f'Starter lane scaffold for {normalized_lane_id}.',
                'include_in_m1': True,
                'reason': f'Starter lane scaffold for {normalized_lane_id}',
                'classified_raw_entries': classified_entries,
            }
        ],
        'canonical_input_manifest': {
            'sources': [],
            'concepts': [],
        },
        'relationship_input_manifest': {
            'relationships': [],
        },
        'graph_output_root': f'005_Operational-Intelligence-Layer/graph/datasets/{normalized_lane_id}',
        'run_output_root': f'006_System-Manifests/runs/datasets/{normalized_lane_id}',
        'query_snapshot_path_template': f'005_Operational-Intelligence-Layer/graph/datasets/{normalized_lane_id}' + '/{run_id}_graph_snapshot.json',
        'freshness_policy': {'mode': 'exact'},
        'pilot_gate': {
            'require_manifest_validation': True,
            'source_to_graph_execute_ready': False,
            'derived_from_tranche_id': normalized_lane_id,
            'derived_run_id': utc_now_stamp().split('T')[0],
        },
        'law_units': law_units,
    }
    write_yaml_payload(resolved_out_manifest_path, payload)
    return {
        'family': family,
        'lane_id': normalized_lane_id,
        'profile_path': resolved_profile_path,
        'raw_root': resolved_raw_root,
        'out_manifest_path': resolved_out_manifest_path,
        'selected_files': selected_files,
        'payload': payload,
    }
