"""Stream L.3 — walk 001B_Spatial-Source-Layer and emit candidate records.

Walker is gated on features.l_spatial_ingestion. With the flag OFF, the
function is a no-op that returns an empty SpatialWalkResult. With the
flag ON, it scans *.json files (recursively), validates each against the
frozen schema, and emits per-instance / per-edge candidate records. Files
that fail validation are logged as warnings and skipped — a single bad
file never poisons the run.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..features import Features
from .schema import SpatialSchemaError, validate_spatial_payload


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SpatialCandidate:
    spatial_context_id: str
    instance_id: str
    canonical_concept_id: str
    bounding_box_min: tuple[float, float, float] | None
    bounding_box_max: tuple[float, float, float] | None
    source_file: str


@dataclass(frozen=True)
class SpatialEdgeCandidate:
    spatial_context_id: str
    source_instance: str
    predicate: str
    target_instance: str
    value: float | None
    unit: str | None
    source_file: str


@dataclass(frozen=True)
class SpatialWalkResult:
    instances: tuple[SpatialCandidate, ...]
    edges: tuple[SpatialEdgeCandidate, ...]
    files_processed: int


def _coerce_vec3(value: Any) -> tuple[float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        return None
    try:
        return (float(value[0]), float(value[1]), float(value[2]))
    except (TypeError, ValueError):
        return None


def _extract_bbox(
    instance: dict[str, Any],
) -> tuple[tuple[float, float, float] | None, tuple[float, float, float] | None]:
    bbox = instance.get("bounding_box")
    if not isinstance(bbox, dict):
        return (None, None)
    return (_coerce_vec3(bbox.get("min")), _coerce_vec3(bbox.get("max")))


def _candidates_from_payload(
    payload: dict[str, Any], source_file: str
) -> tuple[list[SpatialCandidate], list[SpatialEdgeCandidate]]:
    context_id = str(payload["spatial_context_id"])
    instances: list[SpatialCandidate] = []
    for inst in payload.get("instances", []):
        bmin, bmax = _extract_bbox(inst)
        instances.append(
            SpatialCandidate(
                spatial_context_id=context_id,
                instance_id=str(inst["instance_id"]),
                canonical_concept_id=str(inst["canonical_concept_id"]),
                bounding_box_min=bmin,
                bounding_box_max=bmax,
                source_file=source_file,
            )
        )
    edges: list[SpatialEdgeCandidate] = []
    for edge in payload.get("spatial_edges", []):
        raw_val = edge.get("value")
        value: float | None
        if isinstance(raw_val, (int, float)):
            value = float(raw_val)
        else:
            value = None
        unit = edge.get("unit")
        edges.append(
            SpatialEdgeCandidate(
                spatial_context_id=context_id,
                source_instance=str(edge["source_instance"]),
                predicate=str(edge["predicate"]),
                target_instance=str(edge["target_instance"]),
                value=value,
                unit=str(unit) if isinstance(unit, str) else None,
                source_file=source_file,
            )
        )
    return instances, edges


_EMPTY_RESULT = SpatialWalkResult(instances=(), edges=(), files_processed=0)


def walk_spatial_layer(
    spatial_root: Path,
    *,
    features: Features,
) -> SpatialWalkResult:
    if not features.is_enabled("l_spatial_ingestion"):
        return _EMPTY_RESULT

    if not spatial_root.exists():
        logger.warning("spatial walk target does not exist: %s", spatial_root)
        return _EMPTY_RESULT
    if not spatial_root.is_dir():
        logger.warning("spatial walk target is not a directory: %s", spatial_root)
        return _EMPTY_RESULT

    files = sorted(p for p in spatial_root.rglob("*.json") if p.is_file())
    all_instances: list[SpatialCandidate] = []
    all_edges: list[SpatialEdgeCandidate] = []
    files_processed = 0
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("skipping unreadable spatial file %s: %s", path, exc)
            continue
        try:
            validate_spatial_payload(payload)
        except SpatialSchemaError as exc:
            logger.warning("skipping invalid spatial file %s: %s", path, exc)
            continue
        try:
            rel = path.relative_to(spatial_root)
        except ValueError:
            rel = path
        source_file = str(rel)
        instances, edges = _candidates_from_payload(payload, source_file=source_file)
        all_instances.extend(instances)
        all_edges.extend(edges)
        files_processed += 1

    all_instances.sort(
        key=lambda c: (c.spatial_context_id, c.source_file, c.instance_id)
    )
    all_edges.sort(
        key=lambda e: (
            e.spatial_context_id,
            e.source_file,
            e.source_instance,
            e.target_instance,
            e.predicate,
        )
    )

    return SpatialWalkResult(
        instances=tuple(all_instances),
        edges=tuple(all_edges),
        files_processed=files_processed,
    )
