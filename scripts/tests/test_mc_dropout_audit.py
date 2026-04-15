"""Smoke test for the MC Dropout audit."""
from __future__ import annotations

from pathlib import Path


def test_mc_dropout_audit_survey_runs(tmp_path: Path) -> None:
    from vitruvius.bench.audit_mc_dropout import (
        MCDropoutAuditResult,
        survey_neural_inference_sites,
        compute_recommendation,
    )

    sites = survey_neural_inference_sites()
    assert isinstance(sites, list)
    # The audit must return at least the GraphSAGE entry, which is
    # the only neural module in the repo.
    assert any(s["file"].endswith("graphsage.py") for s in sites)

    # Each site must carry the dropout_enabled_at_inference flag.
    for s in sites:
        assert "dropout_enabled_at_inference" in s
        assert isinstance(s["dropout_enabled_at_inference"], bool)

    result = MCDropoutAuditResult(
        viable_sites=[s for s in sites if s["dropout_enabled_at_inference"]],
        surveyed_sites=sites,
    )
    assert isinstance(result.viable_sites, list)


def test_mc_dropout_recommendation() -> None:
    from vitruvius.bench.audit_mc_dropout import compute_recommendation

    # No viable sites → PARK
    assert compute_recommendation(viable_site_count=0) == "PARK"
    # One viable site → GO (wire it in)
    assert compute_recommendation(viable_site_count=1) == "GO"
    # Multiple viable sites → GO
    assert compute_recommendation(viable_site_count=3) == "GO"
