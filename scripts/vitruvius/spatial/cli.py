"""Stream L.7 — CLI entry points for ingest-spatial + evaluate-spatial.

Both entry points lazily import the heavy modules (walker, schema,
constraint_solver) so pipeline_cli stays cheap when the spatial
commands are not in use. Config path is read from VITRUVIUS_CONFIG env
or defaults to config/vitruvius.yaml in the current working directory.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from ..features import Features, load_features


_SPATIAL_ROOT_DEFAULT = Path("001B_Spatial-Source-Layer")


def _resolve_config_path() -> Path:
    env_path = os.environ.get("VITRUVIUS_CONFIG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / "config" / "vitruvius.yaml"


def _load_features() -> Features:
    return load_features(_resolve_config_path())


def run_ingest_spatial() -> int:
    features = _load_features()
    if not features.is_enabled("l_spatial_ingestion"):
        print(
            "feature disabled — enable features.l_spatial_ingestion in config/vitruvius.yaml"
        )
        return 0

    from .walker import walk_spatial_layer

    spatial_root = Path.cwd() / _SPATIAL_ROOT_DEFAULT
    result = walk_spatial_layer(spatial_root, features=features)

    files_on_disk = 0
    if spatial_root.exists() and spatial_root.is_dir():
        files_on_disk = sum(1 for p in spatial_root.rglob("*.json") if p.is_file())
    skipped = max(files_on_disk - result.files_processed, 0)

    summary = {
        "files_processed": result.files_processed,
        "instance_count": len(result.instances),
        "edge_count": len(result.edges),
        "skipped_count": skipped,
        "context_ids": sorted({i.spatial_context_id for i in result.instances}),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def _parse_rules_file(rules_path: Path) -> dict[str, dict[str, object]]:
    raw = json.loads(rules_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"rules file {rules_path} must be a JSON object")
    return raw


def run_evaluate_spatial(
    *,
    concepts: str,
    observations_path: str,
    rules_path: str | None,
) -> int:
    features = _load_features()
    if not features.is_enabled("l_z3_constraint_solver"):
        print(
            "feature disabled — enable features.l_z3_constraint_solver in config/vitruvius.yaml"
        )
        return 0

    from .constraint_solver import ParametricConstraint, evaluate_batch

    concept_list = [slug.strip() for slug in concepts.split(",") if slug.strip()]
    if not concept_list:
        print(json.dumps({"error": "no concepts supplied via --concepts"}, indent=2))
        return 2

    obs_file = Path(observations_path)
    if not obs_file.exists():
        print(json.dumps({"error": f"observations file not found: {observations_path}"}, indent=2))
        return 2
    observations = json.loads(obs_file.read_text(encoding="utf-8"))
    if not isinstance(observations, dict):
        print(json.dumps({"error": "observations file must be a JSON object"}, indent=2))
        return 2

    rules: dict[str, dict[str, object]] = {}
    if rules_path:
        rules_file = Path(rules_path)
        if not rules_file.exists():
            print(json.dumps({"error": f"rules file not found: {rules_path}"}, indent=2))
            return 2
        rules = _parse_rules_file(rules_file)

    constraints: list[ParametricConstraint] = []
    missing_rules: list[str] = []
    for concept_id in concept_list:
        rule = rules.get(concept_id)
        if rule is None:
            missing_rules.append(concept_id)
            continue
        variable = str(rule.get("variable", concept_id))
        operator = str(rule.get("operator", ">="))
        threshold = float(rule.get("threshold", 0.0))  # type: ignore[arg-type]
        constraints.append(
            ParametricConstraint(
                concept_id=concept_id,
                variable=variable,
                operator=operator,
                threshold=threshold,
            )
        )

    results = evaluate_batch(constraints, observations)
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    payload = {
        "evaluated": len(results),
        "passed": passed,
        "failed": failed,
        "missing_rules": missing_rules,
        "results": [
            {
                "concept_id": r.concept_id,
                "variable": r.variable,
                "observed": r.observed,
                "passed": r.passed,
                "reason": r.reason,
            }
            for r in results
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if failed == 0 else 1
