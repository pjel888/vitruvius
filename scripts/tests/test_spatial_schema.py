"""Stream L.2 — spatial JSON schema validator tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.spatial.schema import (
    SPATIAL_SCHEMA_VERSION,
    SpatialSchemaError,
    validate_spatial_payload,
)


FIX_DIR = Path(__file__).resolve().parent / "fixtures" / "spatial"


def _load_sample() -> dict:
    return json.loads((FIX_DIR / "sample_residential_01_spatial.json").read_text())


def test_schema_version_constant() -> None:
    assert SPATIAL_SCHEMA_VERSION == "1.0.0"


def test_valid_sample_passes() -> None:
    payload = _load_sample()
    validate_spatial_payload(payload)


def test_missing_schema_version_is_rejected() -> None:
    payload = _load_sample()
    del payload["schema_version"]
    with pytest.raises(SpatialSchemaError, match="schema_version"):
        validate_spatial_payload(payload)


def test_wrong_schema_version_is_rejected() -> None:
    payload = _load_sample()
    payload["schema_version"] = "2.0.0"
    with pytest.raises(SpatialSchemaError, match="schema_version"):
        validate_spatial_payload(payload)


def test_missing_spatial_context_id_is_rejected() -> None:
    payload = _load_sample()
    del payload["spatial_context_id"]
    with pytest.raises(SpatialSchemaError, match="spatial_context_id"):
        validate_spatial_payload(payload)


def test_spatial_context_id_must_have_spatial_prefix() -> None:
    payload = _load_sample()
    payload["spatial_context_id"] = "model-01"
    with pytest.raises(SpatialSchemaError, match="spatial_context_id"):
        validate_spatial_payload(payload)


def test_instance_id_must_have_instance_prefix() -> None:
    payload = _load_sample()
    payload["instances"][0]["instance_id"] = "door-01"
    with pytest.raises(SpatialSchemaError, match="instance-"):
        validate_spatial_payload(payload)


def test_canonical_concept_id_must_have_concept_prefix() -> None:
    payload = _load_sample()
    payload["instances"][0]["canonical_concept_id"] = "fire-door"
    with pytest.raises(SpatialSchemaError, match="concept-"):
        validate_spatial_payload(payload)


def test_unknown_predicate_rejected() -> None:
    payload = _load_sample()
    payload["spatial_edges"][0]["predicate"] = "next_to"
    with pytest.raises(SpatialSchemaError, match="predicate"):
        validate_spatial_payload(payload)


def test_missing_required_instances_field_rejected() -> None:
    payload = _load_sample()
    del payload["instances"]
    with pytest.raises(SpatialSchemaError, match="instances"):
        validate_spatial_payload(payload)


def test_schema_load_round_trip_file_is_stable() -> None:
    payload = _load_sample()
    validate_spatial_payload(payload)
    reserialized = json.loads(json.dumps(payload))
    validate_spatial_payload(reserialized)


def test_non_dict_payload_rejected() -> None:
    with pytest.raises(SpatialSchemaError, match="dict"):
        validate_spatial_payload([])


def test_payload_non_numeric_edge_value_rejected() -> None:
    payload = _load_sample()
    payload["spatial_edges"][0]["value"] = "not-a-number"
    with pytest.raises(SpatialSchemaError, match="value"):
        validate_spatial_payload(payload)
