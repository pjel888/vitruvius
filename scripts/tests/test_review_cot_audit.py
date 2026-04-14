"""Stream Y3.2 — CoT audit writer tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.review.cot_audit import CotAuditSummary, write_cot_trace
from vitruvius.review.reflection_parser import CotResult


def test_write_trace_creates_file_with_deterministic_name(tmp_path: Path) -> None:
    result = CotResult(
        verdict="keep",
        self_confidence=0.91,
        reasoning_steps=["step 1", "step 2"],
        evidence_citation="setback 3m",
    )
    path = write_cot_trace(
        out_dir=tmp_path,
        relationship_hash="abc123deadbeef",
        cot=result,
        model="qwen2.5:7b",
        candidate_raw_response="<think>...</think>VERDICT: keep",
    )
    assert path.exists()
    assert path.name.endswith("_abc123deadbeef.json")
    payload = json.loads(path.read_text())
    assert payload["verdict"] == "keep"
    assert payload["self_confidence"] == 0.91
    assert payload["relationship_hash"] == "abc123deadbeef"
    assert payload["model"] == "qwen2.5:7b"


def test_audit_summary_counts_verdicts(tmp_path: Path) -> None:
    import time
    for i, v in enumerate(["keep", "keep", "reject", "keep", "abstain"]):
        write_cot_trace(
            out_dir=tmp_path,
            relationship_hash=f"hash{i:03d}",
            cot=CotResult(
                verdict=v,
                self_confidence=0.8,
                reasoning_steps=["x"],
                evidence_citation="y",
            ),
            model="m",
            candidate_raw_response="",
        )
        # Ensure unique timestamp per file even on fast hardware.
        time.sleep(0.01)
    summary = CotAuditSummary.from_directory(tmp_path)
    assert summary.total == 5
    assert summary.verdict_counts == {"keep": 3, "reject": 1, "abstain": 1}
    assert summary.mean_self_confidence == pytest.approx(0.8)


# ---------------------------------------------------------------------------
# Stream Y3.4 — ple-cotrace-dump CLI handler
# ---------------------------------------------------------------------------
def test_cli_ple_cotrace_dump_emits_summary(tmp_path: Path, capsys) -> None:
    from vitruvius.review.cot_audit import run_ple_cotrace_dump

    # Seed a synthetic trace
    write_cot_trace(
        out_dir=tmp_path,
        relationship_hash="h1",
        cot=CotResult(
            verdict="keep",
            self_confidence=0.9,
            reasoning_steps=["s"],
            evidence_citation="citation text here",
        ),
        model="m",
        candidate_raw_response="",
    )
    rc = run_ple_cotrace_dump(cot_dir=tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "total: 1" in out
    assert "keep: 1" in out
