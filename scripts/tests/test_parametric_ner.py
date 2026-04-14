"""Parametric NER — regex-anchored (entity, operator, value, unit) extractor."""

from __future__ import annotations

from vitruvius.parsers.parametric_ner import (
    Parameter,
    extract_parameters,
)


def test_extracts_min_setback_tuple() -> None:
    text = "The minimum setback shall be 2.0 meters from the property line."
    params = extract_parameters(text)
    assert any(
        p.entity.lower().endswith("setback")
        and p.operator == ">="
        and p.value == 2.0
        and p.unit == "meters"
        for p in params
    ), f"no min-setback match in {params}"


def test_extracts_max_footprint_percent() -> None:
    text = "Maximum allowable footprint is 60 percent of the lot area."
    params = extract_parameters(text)
    assert any(
        "footprint" in p.entity.lower()
        and p.operator == "<="
        and p.value == 60.0
        and p.unit == "percent"
        for p in params
    ), f"no max-footprint match in {params}"


def test_ignores_pure_narrative() -> None:
    text = "Every building shall comply with fire safety requirements."
    assert extract_parameters(text) == []


def test_preserves_evidence_offsets() -> None:
    text = "Minimum exit width shall be 1.2 meters."
    params = extract_parameters(text)
    assert params
    p = params[0]
    assert text[p.start : p.end] == p.evidence
    assert "Minimum" in p.evidence or "minimum" in p.evidence


def test_max_uses_at_most() -> None:
    text = "The occupancy load shall be at most 50 persons per floor."
    params = extract_parameters(text)
    assert any(
        p.operator == "<=" and p.value == 50.0 and p.unit == "occupants"
        for p in params
    )


def test_unit_normalisation_percent() -> None:
    text = "Maximum lot coverage shall be 70%."
    params = extract_parameters(text)
    assert params
    assert params[0].unit == "percent"


def test_unit_normalisation_meters_abbr() -> None:
    text = "Minimum yard depth shall be 3 m."
    params = extract_parameters(text)
    assert params
    assert params[0].unit == "meters"


def test_multiple_matches_return_in_document_order() -> None:
    text = (
        "The minimum setback shall be 2.0 meters. "
        "Maximum footprint is 60 percent. "
        "Minimum parking shall be 1 slot per unit."
    )
    params = extract_parameters(text)
    starts = [p.start for p in params]
    assert starts == sorted(starts)
    assert len(params) >= 2


def test_case_insensitive_anchor() -> None:
    text = "MAXIMUM setback IS 3 METERS."
    params = extract_parameters(text)
    assert params
    assert params[0].operator == "<="
    assert params[0].value == 3.0
    assert params[0].unit == "meters"


def test_equal_to_operator() -> None:
    text = "The ceiling height shall be exactly 2.7 meters."
    params = extract_parameters(text)
    assert any(
        p.operator == "==" and p.value == 2.7 and p.unit == "meters"
        for p in params
    )


def test_at_least_anchor_maps_to_ge() -> None:
    text = "Parking spaces shall be at least 10 per building."
    params = extract_parameters(text)
    assert params
    assert params[0].operator == ">="
    assert params[0].value == 10.0


def test_sqm_normalisation() -> None:
    text = "Minimum gross floor area shall be 120 sqm."
    params = extract_parameters(text)
    assert params
    assert params[0].unit == "sqm"
    assert params[0].operator == ">="
    assert params[0].value == 120.0


def test_parameter_is_frozen_dataclass() -> None:
    p = Parameter(
        entity="setback",
        operator=">=",
        value=2.0,
        unit="meters",
        start=0,
        end=10,
        evidence="minimum",
    )
    try:
        p.value = 3.0  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("Parameter should be frozen")
