"""Stream W4.2 — every w_* flag OFF → byte-identical to current main."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.graph.builder import build_snapshot
from vitruvius.graph.snapshot import _snapshot_to_dict

FIX = Path(__file__).resolve().parent / "fixtures" / "wiring"


def _seed(root: Path) -> None:
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    (shared / "sources").mkdir(parents=True)
    (shared / "concepts").mkdir(parents=True)
    (shared / "relationships").mkdir(parents=True)
    (shared / "sources" / "pd-1096.md").write_text(
        "---\nid: law-pd-1096\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    (shared / "concepts" / "building-permit.md").write_text(
        "---\nid: concept-building-permit\npage_type: concept\n"
        "canonical_status: enriched\n"
        "stringency_vector: qualitative\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n",
        encoding="utf-8",
    )
    (shared / "relationships" / "r.md").write_text(
        "---\nid: rel-pd-1096-governs-concept-building-permit\n"
        "page_type: relationship\nrelationship_type: governs\n"
        "from_entity: law-pd-1096\nto_entity: concept-building-permit\n"
        "canonical_status: promoted\n---\n",
        encoding="utf-8",
    )


def test_flag_off_snapshot_matches_frozen_fixture(monkeypatch, tmp_path: Path) -> None:
    _seed(tmp_path)
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {})

    snapshot = build_snapshot(
        tmp_path / "003_Canonical-Knowledge-Layer" / "shared",
        now="2026-04-15T00:00:00Z",
    )
    actual = _snapshot_to_dict(snapshot)
    expected = json.loads((FIX / "expected_flag_off_snapshot.json").read_text())
    assert actual == expected, (
        "Flag-OFF behaviour drifted. Check that every wiring change is "
        "gated behind a `w_*` flag."
    )
