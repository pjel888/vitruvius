"""Quality scoring for the Architecture/Civil/Structural Backbone focus area."""

from __future__ import annotations

import argparse
import json
import re
from collections import deque
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from vitruvius.kg.architecture_civil_structural_enrichment import GENERATION_METHOD
from vitruvius.kg.backbone_graph_quality import analyze_backbone_graph_quality

REPORT_SCHEMA_VERSION = "aec-mepfs-architecture-civil-structural-quality-score/v1"
DEFAULT_FIXTURE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_SOURCE_RIGHTS_PATH = Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
DEFAULT_READINESS_FIXTURE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json")
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality")
REPORT_FILENAME = "architecture-civil-structural-quality-report.json"
RAW_SOURCE_ROOT = Path("001_Raw-Source-Layer")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

REQUIRED_RELATION_TYPES = {
    "constrains_accessible_route_slope_and_cross_slope",
    "coordinates_finished_floor_elevation",
    "discharges_roof_runoff_to_site_network",
    "directs_surface_runoff",
    "derives_bearing_pressure_basis",
    "translates_soil_capacity_to_foundation_design",
    "transfers_gravity_load_to",
    "transfers_lateral_load_to_collector",
    "requires_diaphragm_opening_coordination",
    "requires_slab_opening_review",
    "transfers_wind_load_to_frame",
    "resists_lateral_earth_pressure",
    "requires_rear_drainage_or_pressure_relief",
    "covers_structural_movement_joint",
    "constrains_foundation_layout_and_clearance",
    "constrains_finished_floor_elevation_interface",
    "constrains_grading_slope_stability",
    "qualifies_utility_conflict_evidence_strength",
    "supports_pavement_structure_performance",
    "constrains_accessible_route_transition_geometry",
    "requires_access_for_inlet_sediment_maintenance",
    "creates_civil_asset_record_for_handover",
    "requires_public_way_crossing_tie_in_review",
    "sets_culvert_hydrology_basis",
    "requires_flood_and_scour_hazard_review",
    "sensitive_to_subgrade_settlement_variability",
    "sets_flood_elevation_ahj_adoption_basis",
    "requires_local_rainfall_basis_confirmation",
    "gates_structural_criteria_by_authority_basis",
    "gates_live_load_basis_before_application",
    "requires_drainage_inlet_maintenance_plan",
    "requires_adopted_wind_load_basis",
    "requires_adopted_seismic_load_basis",
}
REQUIRED_CASE_IDS = {f"RES-ACS-{index:03d}" for index in range(1, 19)}
TRAVERSAL_CHECKS = [
    ("ARC.SPC.CIR.ASR", "CIV.SDV.ACC.PSG", 3),
    ("ARC.ENV.ROF.RDI", "CIV.DRN.DET", 4),
    ("GEO.SIS.GTI", "STR.FND.SHL.FTG", 4),
    ("STR.RCS.SBC.SLS", "GEO.FOE.ABP", 4),
    ("STR.LOA.LAT.WND", "STR.RCS.SWC.COR", 5),
    ("ARC.BLD.STR.FOC", "STR.WSD.DIC.DPO", 2),
    ("STR.FND.SHL.RTW", "CIV.DRN.CON.PDR", 2),
    ("STR.SSS.CBP.MJT", "ARC.DET.ENV.WCI", 2),
    ("CIV.MIS.UCC.SUC", "GEO.EXC.SHR", 2),
    ("COM.APP.FHA", "CIV.SDV.GRD.FFE", 3),
    ("GEO.RSS.SLS", "STR.FND.SHL.RTW", 2),
    ("CIV.MIS.UCC.TPH", "STR.FND.SHL.FTG", 4),
    ("CIV.PAV.SBG", "CIV.SDV.ACC.EVA", 3),
    ("CIV.SDV.ACC.CRG", "ARC.SPC.CIR.ASR", 2),
    ("CIV.DRN.CON.SMA", "OPS.AST.REG.CAR", 2),
    ("COM.APP.AHJ", "STR.LOA.LAT.WND", 2),
    ("CIV.RDC.PED.ATI", "CIV.DRN.CON.SRO", 3),
    ("CIV.HDI.CCD.CDI", "GEO.HAZ.FLO", 2),
    ("STR.LOA.CBG", "STR.LOA.LAT.WND", 2),
    ("CIV.DRN.CON.CBI", "OPS.MNT.PMA", 2),
]


def score_architecture_civil_structural_quality(
    backbone_payload: dict[str, Any],
    source_rights_payload: dict[str, Any],
    readiness_payload: dict[str, Any],
) -> dict[str, Any]:
    records = _dict_list(backbone_payload.get("records"))
    relationships = _dict_list(backbone_payload.get("relationships"))
    introduced_nodes = [row for row in records if row.get("generation_method") == GENERATION_METHOD]
    introduced_edges = [row for row in relationships if row.get("generation_method") == GENERATION_METHOD]
    source_ids = {
        str(row.get("source_id") or "")
        for row in _dict_list(source_rights_payload.get("source_rights_registry"))
        if row.get("source_id")
    }
    graph_quality = analyze_backbone_graph_quality(
        backbone_payload,
        introduced_generation_method=GENERATION_METHOD,
        source_rights_payload=source_rights_payload,
    )

    node_complete = sum(
        1
        for row in introduced_nodes
        if len(str(row.get("definition") or "")) >= 30
        and _list_strings(row.get("source_family_ids"))
        and _list_strings(row.get("discipline"))
        and _list_strings(row.get("lifecycle_phase"))
        and row.get("semantic_node_kind")
    )
    node_score = _points(node_complete, len(introduced_nodes), 20)

    edge_complete = sum(
        1
        for row in introduced_edges
        if row.get("relation_type")
        and row.get("relation_category")
        and _list_strings(row.get("source_family_ids"))
        and len(str(row.get("rationale") or "")) >= 30
        and 0 <= float(row.get("weight", -1)) <= 1
        and 0 <= float(row.get("confidence_score", -1)) <= 1
    )
    edge_score = _points(edge_complete, len(introduced_edges), 20)

    relation_types = {str(row.get("relation_type") or "") for row in introduced_edges}
    traversal_results = _traversal_results(records, relationships)
    traversal_passes = sum(1 for result in traversal_results if result["ok"])
    cross_score = min(
        20.0,
        _points(len(REQUIRED_RELATION_TYPES & relation_types), len(REQUIRED_RELATION_TYPES), 10)
        + _points(traversal_passes, len(traversal_results), 10),
    )

    used_source_ids = {
        source_id
        for row in [*introduced_nodes, *introduced_edges]
        for source_id in _list_strings(row.get("source_family_ids"))
    }
    source_rows_with_currentness = sum(
        1
        for row in _dict_list(source_rights_payload.get("source_rights_registry"))
        if row.get("source_id") in used_source_ids and row.get("currentness_check_date")
    )
    source_score = min(
        15.0,
        _points(len(used_source_ids - source_ids) == 0, True, 7.5)
        + _points(source_rows_with_currentness, max(len(used_source_ids), 1), 7.5),
    )

    case_ids = {str(row.get("case_id") or "") for row in _dict_list(readiness_payload.get("resolver_golden_cases"))}
    validation_score = min(
        15.0,
        (7.5 if graph_quality["ok"] else 0.0)
        + _points(len(REQUIRED_CASE_IDS & case_ids), len(REQUIRED_CASE_IDS), 7.5),
    )
    hygiene_score = 10.0 if not graph_quality["errors"] and graph_quality["metrics"]["orphan_node_count"] == 0 else 0.0

    dimensions = {
        "node_completeness": round(node_score, 2),
        "edge_specificity": round(edge_score, 2),
        "cross_taxonomy_reasoning_paths": round(cross_score, 2),
        "provenance_source_coverage": round(source_score, 2),
        "validation_test_coverage": round(validation_score, 2),
        "duplicate_orphan_hygiene": round(hygiene_score, 2),
    }
    total = round(sum(dimensions.values()), 2)
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": total >= 90
        and min(dimensions.values()) >= 7.5
        and graph_quality["ok"]
        and all(result["ok"] for result in traversal_results),
        "generated_at_utc": _utc_now(),
        "quality_score": {
            "total": total,
            "target": 90,
            "dimensions": dimensions,
            "dimension_max_points": {
                "node_completeness": 20,
                "edge_specificity": 20,
                "cross_taxonomy_reasoning_paths": 20,
                "provenance_source_coverage": 15,
                "validation_test_coverage": 15,
                "duplicate_orphan_hygiene": 10,
            },
        },
        "metrics": {
            "introduced_node_count": len(introduced_nodes),
            "introduced_relationship_count": len(introduced_edges),
            "required_relation_type_coverage": sorted(REQUIRED_RELATION_TYPES & relation_types),
            "missing_required_relation_types": sorted(REQUIRED_RELATION_TYPES - relation_types),
            "required_resolver_case_coverage": sorted(REQUIRED_CASE_IDS & case_ids),
            "missing_required_resolver_cases": sorted(REQUIRED_CASE_IDS - case_ids),
            "used_source_ids": sorted(used_source_ids),
        },
        "traversal_results": traversal_results,
        "graph_quality_ok": graph_quality["ok"],
        "graph_quality_errors": graph_quality["errors"],
        "graph_quality_warnings": graph_quality["warnings"],
    }


def run_quality_score_report(
    fixture_path: str | Path = DEFAULT_FIXTURE_PATH,
    *,
    source_rights_path: str | Path = DEFAULT_SOURCE_RIGHTS_PATH,
    readiness_fixture_path: str | Path = DEFAULT_READINESS_FIXTURE_PATH,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    root = _repo_root(repo_root)
    fixture = _resolve_file(root, Path(fixture_path))
    source_file = _resolve_file(root, Path(source_rights_path))
    readiness_file = _resolve_file(root, Path(readiness_fixture_path))
    resolved_run_id = _run_id(run_id)
    report_path = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)
    report = score_architecture_civil_structural_quality(
        _load_json_object(fixture),
        _load_json_object(source_file),
        _load_json_object(readiness_file),
    )
    report["run_id"] = resolved_run_id
    report["fixture_path"] = _relative_to_root(fixture, root)
    report["source_rights_path"] = _relative_to_root(source_file, root)
    report["readiness_fixture_path"] = _relative_to_root(readiness_file, root)
    report["report_path"] = _relative_to_root(report_path, root)
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score Architecture/Civil/Structural Backbone graph quality.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH))
    parser.add_argument("--source-rights", default=str(DEFAULT_SOURCE_RIGHTS_PATH))
    parser.add_argument("--readiness-fixture", default=str(DEFAULT_READINESS_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)
    try:
        report = run_quality_score_report(
            args.fixture,
            source_rights_path=args.source_rights,
            readiness_fixture_path=args.readiness_fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
        )
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _traversal_results(records: list[dict[str, Any]], relationships: list[dict[str, Any]]) -> list[dict[str, Any]]:
    id_by_path = {str(row.get("path_code") or ""): str(row.get("id") or "") for row in records}
    outgoing: dict[str, list[str]] = {}
    for row in relationships:
        outgoing.setdefault(str(row.get("from_id") or ""), []).append(str(row.get("to_id") or ""))
    results = []
    for from_path, to_path, max_depth in TRAVERSAL_CHECKS:
        start = id_by_path.get(from_path)
        end = id_by_path.get(to_path)
        ok = bool(start and end and _reachable(outgoing, start, end, max_depth))
        results.append({"from_path": from_path, "to_path": to_path, "max_depth": max_depth, "ok": ok})
    return results


def _reachable(outgoing: dict[str, list[str]], start: str, end: str, max_depth: int) -> bool:
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        node, depth = queue.popleft()
        if node == end:
            return True
        if depth >= max_depth:
            continue
        for child in outgoing.get(node, []):
            if child in seen:
                continue
            seen.add(child)
            queue.append((child, depth + 1))
    return False


def _points(numerator: Any, denominator: Any, points: float) -> float:
    if isinstance(denominator, bool):
        return points if numerator == denominator else 0.0
    if not denominator:
        return points
    return points * min(float(numerator) / float(denominator), 1.0)


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _list_strings(value: Any) -> list[str]:
    return [str(item).strip() for item in value if str(item).strip()] if isinstance(value, list) else []


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_file(root: Path, path: Path) -> Path:
    resolved = path if path.is_absolute() else root / path
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{path}: path must stay inside repository root") from exc
    if not resolved.is_file():
        raise FileNotFoundError(f"{path}: file does not exist")
    return resolved


def _resolve_report_path(root: Path, run_id: str, output_path: Path | None) -> Path:
    target = output_path if output_path is not None else REPORT_ROOT / run_id / REPORT_FILENAME
    resolved = target if target.is_absolute() else root / target
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{target}: output path must stay inside repository root") from exc
    _reject_raw_source_output(root, resolved, target)
    expected_root = (root / REPORT_ROOT).resolve()
    try:
        resolved.relative_to(expected_root)
    except ValueError as exc:
        raise ValueError(f"{target}: output path must stay inside {REPORT_ROOT.as_posix()}") from exc
    if resolved.name != REPORT_FILENAME:
        raise ValueError(f"{target}: output filename must be {REPORT_FILENAME}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def _reject_raw_source_output(root: Path, resolved: Path, target: Path) -> None:
    raw_root = (root / RAW_SOURCE_ROOT).resolve()
    try:
        resolved.relative_to(raw_root)
    except ValueError:
        return
    raise ValueError(f"{target}: output path must not be inside immutable raw source custody layer {RAW_SOURCE_ROOT.as_posix()}")


def _repo_root(repo_root: str | Path | None) -> Path:
    return Path(repo_root).resolve() if repo_root is not None else Path.cwd().resolve()


def _run_id(run_id: str | None) -> str:
    value = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.match(value):
        raise ValueError("run_id contains unsupported characters")
    return value


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
