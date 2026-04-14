"""Stream L.2 — JSON Schema validator for the spatial contract.

The schema is inlined here rather than read from disk so the validator has
no filesystem side-effects. The authoritative spec lives in
.ai/06_specs/spatial-schema.md — that file and this constant must stay in
sync (enforced by a lint check in later tasks).
"""
from __future__ import annotations

from typing import Any


SPATIAL_SCHEMA_VERSION = "1.0.0"


class SpatialSchemaError(ValueError):
    """Raised when a payload does not conform to the frozen contract."""


SPATIAL_JSON_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://vitruvius.local/schemas/spatial-contract-v1.json",
    "title": "Vitruvius Spatial Contract",
    "type": "object",
    "required": [
        "schema_version",
        "spatial_context_id",
        "generated_at_utc",
        "instances",
        "spatial_edges",
    ],
    "properties": {
        "schema_version": {"type": "string", "enum": [SPATIAL_SCHEMA_VERSION]},
        "spatial_context_id": {
            "type": "string",
            "pattern": "^spatial-[a-z0-9][a-z0-9-]*$",
        },
        "generated_at_utc": {"type": "string"},
        "source_daemon": {"type": "string"},
        "instances": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["instance_id", "canonical_concept_id"],
                "properties": {
                    "instance_id": {
                        "type": "string",
                        "pattern": "^instance-[a-z0-9][a-z0-9-]*$",
                    },
                    "canonical_concept_id": {
                        "type": "string",
                        "pattern": "^concept-[a-z0-9][a-z0-9-]*$",
                    },
                    "bounding_box": {
                        "type": "object",
                        "required": ["min", "max"],
                        "properties": {
                            "min": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3,
                            },
                            "max": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3,
                            },
                        },
                    },
                },
            },
        },
        "spatial_edges": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source_instance", "predicate", "target_instance"],
                "properties": {
                    "source_instance": {
                        "type": "string",
                        "pattern": "^instance-",
                    },
                    "predicate": {
                        "type": "string",
                        "enum": [
                            "spatial_intersects",
                            "spatial_clearance",
                            "spatial_adjacent_to",
                            "spatial_contains",
                        ],
                    },
                    "target_instance": {
                        "type": "string",
                        "pattern": "^instance-",
                    },
                    "value": {"type": "number"},
                    "unit": {
                        "type": "string",
                        "enum": ["meters", "millimeters", "feet", "inches"],
                    },
                },
            },
        },
    },
}


def _format_error_path(error: Any) -> str:
    parts: list[str] = []
    for elem in error.absolute_path:
        parts.append(str(elem))
    return ".".join(parts) if parts else "<root>"


def _translate_error(error: Any) -> str:
    path = _format_error_path(error)
    validator = error.validator
    if validator == "required":
        missing = error.message.split("'")[1] if "'" in error.message else error.message
        return f"missing required field: {missing}"
    if validator == "pattern":
        return f"{path} pattern mismatch: {error.message}"
    if validator == "enum":
        return f"{path} enum mismatch: {error.message}"
    if validator == "type":
        return f"{path} type mismatch: {error.message}"
    return f"{path}: {error.message}"


def validate_spatial_payload(payload: Any) -> None:
    if not isinstance(payload, dict):
        raise SpatialSchemaError(
            f"payload must be a dict (got {type(payload).__name__})"
        )
    try:
        from jsonschema import Draft7Validator
    except ImportError as exc:
        raise SpatialSchemaError(
            "jsonschema is not installed; install jsonschema>=4.0 to validate spatial payloads"
        ) from exc

    validator = Draft7Validator(SPATIAL_JSON_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.absolute_path))
    if not errors:
        return

    messages = [_translate_error(err) for err in errors]
    combined = "; ".join(messages)

    hints: list[str] = []
    for err in errors:
        path = _format_error_path(err)
        if err.validator == "required":
            missing = err.message.split("'")[1] if "'" in err.message else ""
            hints.append(missing)
        if "schema_version" in path:
            hints.append("schema_version")
        if "spatial_context_id" in path:
            hints.append("spatial_context_id")
        if "instance_id" in path or "instance-" in err.message:
            hints.append("instance-")
        if "canonical_concept_id" in path or "concept-" in err.message:
            hints.append("concept-")
        if "predicate" in path:
            hints.append("predicate")
        if "instances" in path and err.validator == "required":
            hints.append("instances")
        if "value" in path:
            hints.append("value")

    hint_suffix = " [" + ", ".join(dict.fromkeys(hints)) + "]" if hints else ""
    raise SpatialSchemaError(f"spatial payload invalid: {combined}{hint_suffix}")
