"""Stream L.3 — walker for 001B_Spatial-Source-Layer."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.features import Features
from vitruvius.spatial.walker import (
    SpatialCandidate,
    SpatialEdgeCandidate,
    SpatialWalkResult,
    walk_spatial_layer,
)


def _features(enabled: bool) -> Features:
    return Features(flags={"l_spatial_ingestion": enabled})


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_payload(context_id: str, *, door_id: str = "fire-door-01") -> dict:
    return {
        "schema_version": "1.0.0",
        "spatial_context_id": context_id,
        "generated_at_utc": "2026-04-15T09:00:00Z",
        "instances": [
            {
                "instance_id": "instance-egress-corridor-01",
                "canonical_concept_id": "concept-means-of-egress",
                "bounding_box": {
                    "min": [0.0, 0.0, 0.0],
                    "max": [10.0, 1.1, 2.4],
                },
            },
            {
                "instance_id": f"instance-{door_id}",
                "canonical_concept_id": "concept-doors-and-exits",
            },
        ],
        "spatial_edges": [
            {
                "source_instance": "instance-egress-corridor-01",
                "predicate": "spatial_clearance",
                "target_instance": f"instance-{door_id}",
                "value": 1.1,
                "unit": "meters",
            }
        ],
    }


def test_walker_flag_off_returns_empty(tmp_path: Path) -> None:
    _write(tmp_path / "a.json", _make_payload("spatial-a-01"))
    result = walk_spatial_layer(tmp_path, features=_features(False))
    assert isinstance(result, SpatialWalkResult)
    assert result.instances == ()
    assert result.edges == ()
    assert result.files_processed == 0


def test_walker_flag_on_single_file(tmp_path: Path) -> None:
    _write(tmp_path / "residential.json", _make_payload("spatial-residential-01"))
    result = walk_spatial_layer(tmp_path, features=_features(True))
    assert result.files_processed == 1
    assert len(result.instances) == 2
    assert len(result.edges) == 1
    inst = next(i for i in result.instances if i.instance_id == "instance-egress-corridor-01")
    assert isinstance(inst, SpatialCandidate)
    assert inst.canonical_concept_id == "concept-means-of-egress"
    assert inst.bounding_box_min == (0.0, 0.0, 0.0)
    assert inst.bounding_box_max == (10.0, 1.1, 2.4)
    assert inst.source_file.endswith("residential.json")
    edge = result.edges[0]
    assert isinstance(edge, SpatialEdgeCandidate)
    assert edge.source_instance == "instance-egress-corridor-01"
    assert edge.predicate == "spatial_clearance"
    assert edge.value == 1.1
    assert edge.unit == "meters"


def test_walker_nested_dirs(tmp_path: Path) -> None:
    _write(tmp_path / "a" / "nested.json", _make_payload("spatial-nested-01"))
    _write(tmp_path / "b" / "c" / "deep.json", _make_payload("spatial-deep-01"))
    result = walk_spatial_layer(tmp_path, features=_features(True))
    assert result.files_processed == 2
    context_ids = {i.spatial_context_id for i in result.instances}
    assert context_ids == {"spatial-nested-01", "spatial-deep-01"}


def test_walker_skips_invalid_files_with_warning(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    _write(tmp_path / "good.json", _make_payload("spatial-good-01"))
    (tmp_path / "bad.json").write_text('{"schema_version": "1.0.0"}', encoding="utf-8")
    with caplog.at_level("WARNING"):
        result = walk_spatial_layer(tmp_path, features=_features(True))
    assert result.files_processed == 1
    assert any("bad.json" in rec.getMessage() for rec in caplog.records)


def test_walker_empty_dir_returns_empty(tmp_path: Path) -> None:
    result = walk_spatial_layer(tmp_path, features=_features(True))
    assert result.instances == ()
    assert result.edges == ()
    assert result.files_processed == 0


def test_walker_missing_dir_returns_empty_with_warning(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    missing = tmp_path / "nonexistent"
    with caplog.at_level("WARNING"):
        result = walk_spatial_layer(missing, features=_features(True))
    assert result.instances == ()
    assert result.files_processed == 0


def test_walker_deterministic_sort(tmp_path: Path) -> None:
    _write(tmp_path / "z.json", _make_payload("spatial-z-01", door_id="door-zzz"))
    _write(tmp_path / "a.json", _make_payload("spatial-a-01", door_id="door-aaa"))
    _write(tmp_path / "m.json", _make_payload("spatial-m-01", door_id="door-mmm"))
    r1 = walk_spatial_layer(tmp_path, features=_features(True))
    r2 = walk_spatial_layer(tmp_path, features=_features(True))
    assert r1 == r2
    assert [i.spatial_context_id for i in r1.instances if "egress" in i.instance_id] == [
        "spatial-a-01",
        "spatial-m-01",
        "spatial-z-01",
    ]


def test_walker_result_is_frozen(tmp_path: Path) -> None:
    _write(tmp_path / "a.json", _make_payload("spatial-a-01"))
    result = walk_spatial_layer(tmp_path, features=_features(True))
    with pytest.raises(Exception):
        result.instances[0].instance_id = "new-id"  # type: ignore[misc]
    with pytest.raises(Exception):
        result.edges[0].predicate = "spatial_contains"  # type: ignore[misc]


def test_walker_multiple_files_aggregated(tmp_path: Path) -> None:
    _write(tmp_path / "a.json", _make_payload("spatial-a-01", door_id="door-a"))
    _write(tmp_path / "b.json", _make_payload("spatial-b-01", door_id="door-b"))
    _write(tmp_path / "c.json", _make_payload("spatial-c-01", door_id="door-c"))
    result = walk_spatial_layer(tmp_path, features=_features(True))
    assert result.files_processed == 3
    assert len(result.instances) == 6
    assert len(result.edges) == 3
