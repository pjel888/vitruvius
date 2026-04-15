"""Sprint Q Task 5 — live-wiring PD 1096 bench smoke test.

These cases import :func:`run_livewiring_bench` and drive it with the
Ollama call and the flag-on config patched out, so the suite never
touches a real LLM endpoint. The goal is only to assert:

1. The harness can be imported without side effects.
2. The summary dict has the contractual 5 keys + ``notes``.
3. Invoking the harness does NOT mutate ``config/vitruvius.yaml`` on
   disk (flag restoration is byte-identical).
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from vitruvius.bench.run_livewiring_bench import (
    STREAM_W_FLAGS,
    flag_on_config,
    run_livewiring_bench,
)
from vitruvius.paths import get_repo_root


EXPECTED_SUMMARY_KEYS = {
    "peak_rss_mb",
    "wall_seconds",
    "candidates_reviewed",
    "ms_per_candidate",
    "flag_on_config_snapshot",
}


def _fake_review_report() -> dict[str, object]:
    """Minimal review JSON shaped the way ollama_review writes it."""
    return {
        "generated_at": "2026-04-15T00:00:00Z",
        "model": "gemma4:e4b",
        "source": "test://fake",
        "total_candidates": 3,
        "llm_reviewed": 3,
        "completed_reviews": 3,
        "status": "completed",
        "summary": {},
        "reviews": [
            {"candidate": {}, "review": {"decision": "keep", "confidence": 0.9}},
            {"candidate": {}, "review": {"decision": "reject", "confidence": 0.9}},
            {"candidate": {}, "review": {"decision": "keep", "confidence": 0.9}},
        ],
    }


def test_run_livewiring_bench_returns_expected_summary_shape(tmp_path: Path) -> None:
    """Assert the summary dict has every contractual key plus ``notes``.

    Patches out:
    - ``_require_extraction_report`` so the bench does not need
      ``latest_relationship_extraction_sections.json`` on disk.
    - ``run_review_relationships_ollama`` so no live Ollama call fires.
    - ``_read_review_report`` so the count/latency path runs on a
      synthetic 3-candidate report.
    - ``flag_on_config`` so we do not depend on ``config/vitruvius.yaml``
      being readable from the test working directory (the stub still
      yields a config dict so the summary snapshot is populated).
    """
    fake_flag_on_cfg = {
        "features": {flag: True for flag in STREAM_W_FLAGS},
        "review": {"ollama": {"default_model": "gemma4:e4b"}},
    }

    # Build a tiny dummy context manager so the inner body still runs.
    class _DummyCtx:
        def __enter__(self) -> dict[str, object]:
            return fake_flag_on_cfg

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

    with patch(
        "vitruvius.bench.run_livewiring_bench._require_extraction_report",
        return_value=tmp_path / "fake.json",
    ), patch(
        "vitruvius.bench.run_livewiring_bench.flag_on_config",
        return_value=_DummyCtx(),
    ), patch(
        "vitruvius.ollama_review.run_review_relationships_ollama",
        return_value=0,
    ), patch(
        "vitruvius.bench.run_livewiring_bench._read_review_report",
        return_value=_fake_review_report(),
    ):
        summary = run_livewiring_bench(sampler_interval_s=0.05)

    # Every contractual key is present.
    assert EXPECTED_SUMMARY_KEYS.issubset(summary.keys())
    # ``notes`` is always present (empty string when clean).
    assert "notes" in summary
    # Shape checks on the numeric fields.
    assert summary["candidates_reviewed"] == 3
    assert summary["wall_seconds"] >= 0.0
    assert summary["peak_rss_mb"] > 0.0
    assert summary["ms_per_candidate"] >= 0.0
    # Snapshot must show every w_* flag as True.
    features = summary["flag_on_config_snapshot"].get("features", {})
    for flag in STREAM_W_FLAGS:
        assert features.get(flag) is True, f"{flag} missing from flag_on snapshot"


def test_flag_on_config_does_not_mutate_yaml_on_disk() -> None:
    """After exiting the flag_on_config context manager, the on-disk
    ``config/vitruvius.yaml`` must still have every ``w_*`` flag set to
    ``false``. This is the non-breaking-contract guarantee.
    """
    yaml_path = get_repo_root() / "config" / "vitruvius.yaml"
    before = yaml_path.read_text(encoding="utf-8")

    with flag_on_config() as cfg:
        # Inside the context, the flag-on snapshot is True for every flag.
        for flag in STREAM_W_FLAGS:
            assert cfg["features"][flag] is True

    after = yaml_path.read_text(encoding="utf-8")
    assert before == after, (
        "flag_on_config mutated config/vitruvius.yaml on disk; "
        "the context manager must leave the file untouched."
    )
