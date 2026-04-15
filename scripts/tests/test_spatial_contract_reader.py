"""Tests for the Sprint AUDIT-1 Task 5B integrity-verified contract reader.

Verifies parity with the TypeScript writer's integrity footer, detects
corruption, supports legacy files without footers in backward-compat mode,
and rejects them when the caller requires a footer.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from vitruvius.spatial.contract_reader import (
    INTEGRITY_FOOTER_PREFIX,
    ContractParseResult,
    IntegrityError,
    compute_body_sha256,
    parse_contract,
    split_body_and_footer,
)


def _make_body(context_id: str = "spatial-test-01") -> str:
    """Build a minimally valid contract body matching the TS writer shape."""
    payload = {
        "schema_version": "1.0.0",
        "spatial_context_id": context_id,
        "generated_at_utc": "2026-04-15T09:00:00Z",
        "source_daemon": "vitruvius-spatial-daemon@0.1.0",
        "instances": [
            {
                "instance_id": "instance-door-01",
                "canonical_concept_id": "concept-doors-and-exits",
            },
        ],
        "spatial_edges": [],
    }
    # Match TS writer: JSON.stringify(contract, null, 2) + "\n"
    return json.dumps(payload, indent=2) + "\n"


def _make_file(tmp_path: Path, body: str, *, digest: str | None = None) -> Path:
    """Write a contract file. If digest is provided, appends the footer."""
    path = tmp_path / "contract.json"
    if digest is None:
        path.write_text(body, encoding="utf-8")
    else:
        path.write_text(body + INTEGRITY_FOOTER_PREFIX + digest + "\n", encoding="utf-8")
    return path


def test_compute_body_sha256_matches_stdlib():
    body = _make_body()
    expected = hashlib.sha256(body.encode("utf-8")).hexdigest()
    assert compute_body_sha256(body) == expected


def test_split_body_and_footer_on_file_with_footer():
    body = _make_body()
    digest = compute_body_sha256(body)
    raw = body + INTEGRITY_FOOTER_PREFIX + digest + "\n"
    parsed_body, parsed_digest = split_body_and_footer(raw)
    assert parsed_body == body
    assert parsed_digest == digest


def test_split_body_and_footer_on_file_without_footer():
    body = _make_body()
    parsed_body, parsed_digest = split_body_and_footer(body)
    assert parsed_body == body
    assert parsed_digest is None


def test_parse_contract_happy_path(tmp_path: Path):
    body = _make_body()
    digest = compute_body_sha256(body)
    path = _make_file(tmp_path, body, digest=digest)
    result = parse_contract(path)
    assert isinstance(result, ContractParseResult)
    assert result.has_footer is True
    assert result.digest_expected == digest
    assert result.digest_actual == digest
    assert result.payload["spatial_context_id"] == "spatial-test-01"


def test_parse_contract_legacy_no_footer_allowed(tmp_path: Path):
    body = _make_body()
    path = _make_file(tmp_path, body, digest=None)
    result = parse_contract(path)
    assert result.has_footer is False
    assert result.digest_expected is None
    assert result.digest_actual == compute_body_sha256(body)
    assert result.payload["spatial_context_id"] == "spatial-test-01"


def test_parse_contract_legacy_no_footer_rejected_when_required(tmp_path: Path):
    body = _make_body()
    path = _make_file(tmp_path, body, digest=None)
    with pytest.raises(IntegrityError, match="no integrity footer"):
        parse_contract(path, require_footer=True)


def test_parse_contract_detects_body_corruption(tmp_path: Path):
    body = _make_body()
    digest = compute_body_sha256(body)
    # Corrupt body by replacing a field value BEFORE computing raw bytes.
    corrupt_body = body.replace("instance-door-01", "instance-door-02")
    assert corrupt_body != body
    path = tmp_path / "contract.json"
    path.write_text(
        corrupt_body + INTEGRITY_FOOTER_PREFIX + digest + "\n", encoding="utf-8"
    )
    with pytest.raises(IntegrityError, match="integrity failure"):
        parse_contract(path)


def test_parse_contract_detects_truncation(tmp_path: Path):
    body = _make_body()
    digest = compute_body_sha256(body)
    raw = body + INTEGRITY_FOOTER_PREFIX + digest + "\n"
    # Truncate mid-body (simulate a partial write before the footer line).
    truncated = raw[: len(raw) // 2]
    path = tmp_path / "contract.json"
    path.write_text(truncated, encoding="utf-8")
    # Either the JSON body fails to parse OR the integrity check fires.
    with pytest.raises((IntegrityError, json.JSONDecodeError)):
        parse_contract(path)


def test_parse_contract_detects_flipped_digest(tmp_path: Path):
    body = _make_body()
    # Produce a digest that is wrong but same length.
    bad_digest = "0" * 64
    path = _make_file(tmp_path, body, digest=bad_digest)
    with pytest.raises(IntegrityError, match="integrity failure"):
        parse_contract(path)
