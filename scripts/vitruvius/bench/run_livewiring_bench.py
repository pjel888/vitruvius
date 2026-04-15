"""Live PD 1096 bench harness — Sprint Q Task 5 (AD-024 addendum).

Runs ``review-relationships-ollama`` against the already-ingested
PD 1096 IRR candidates with every Stream W (``w_*``) feature flag
temporarily flipped ON **in memory only** (the on-disk
``config/vitruvius.yaml`` is never modified).

Captures:
- Peak process RSS (MB) via a background psutil sampler.
- Wall-clock duration (seconds).
- Per-candidate latency (ms/candidate) derived from the output of
  ``latest_relationship_review_ollama.json``.
- The flag-on config snapshot used for the run.

Public API:
    run_livewiring_bench() -> dict
        Runs the live bench end-to-end and returns the summary dict.

CLI:
    PYTHONPATH=scripts python3 -m vitruvius.bench.run_livewiring_bench

The harness is informational — it never raises on a peak RSS overshoot.
If the 5 GB target is breached the summary notes it in the ``notes`` key
and the exit code is still 0.
"""
from __future__ import annotations

import copy
import json
import resource
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator
from unittest.mock import patch

import yaml

try:
    import psutil  # type: ignore[import-not-found]
except ImportError:
    psutil = None

from vitruvius.paths import get_repo_root


# 12 Stream W flags from config/vitruvius.yaml.
# Keep in lockstep with the ``features.w_*`` block in the YAML.
STREAM_W_FLAGS: tuple[str, ...] = (
    "w_llm_model_pool",
    "w_llm_num_ctx_enforcement",
    "w_llm_context_budget_guard",
    "w_llm_binary_mode",
    "w_review_nb_prefilter",
    "w_review_ontology_prompt",
    "w_review_slm_routing",
    "w_review_conformal_routing",
    "w_review_tension_reflection",
    "w_review_choquet_aggregator",
    "w_promotion_stringency_gate",
    "w_graph_governing_standard",
)


# Default bench model. Must be locally pulled in Ollama.
DEFAULT_BENCH_MODEL = "gemma4:e4b"
DEFAULT_BENCH_TIMEOUT_SECONDS = 600
# Target ceiling for the informational "notes" marker. Not a hard assertion.
PEAK_RSS_CEILING_MB = 5 * 1024


def _load_config_from_disk() -> dict[str, Any]:
    """Read the current on-disk ``config/vitruvius.yaml`` (bypassing the
    lru_cache) so the bench can build a mutated copy without affecting
    other callers.
    """
    path = get_repo_root() / "config" / "vitruvius.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _build_flag_on_config(
    *, base: dict[str, Any], model: str = DEFAULT_BENCH_MODEL
) -> dict[str, Any]:
    """Return a deep copy of ``base`` with every ``w_*`` flag flipped to
    True and the model pool / default_model rewritten to ``model``.

    The model pool is rewritten so that ``w_review_slm_routing`` + the
    Stream W1.1 tier routing does not dispatch to ``phi3:mini`` or
    ``qwen2.5:7b`` (neither of which are guaranteed to be pulled on the
    live bench host).
    """
    cfg = copy.deepcopy(base)
    features = cfg.setdefault("features", {})
    for flag in STREAM_W_FLAGS:
        features[flag] = True
    # Collapse the tier pool onto the bench model so every routing path
    # still resolves to a locally available Ollama model.
    review = cfg.setdefault("review", {}).setdefault("ollama", {})
    review["default_model"] = model
    review["model_pool"] = {
        "tier_0_draft": model,
        "tier_1_default": model,
        "tier_2_heavy": model,
    }
    return cfg


@contextmanager
def flag_on_config(
    *, model: str = DEFAULT_BENCH_MODEL
) -> Iterator[dict[str, Any]]:
    """Context manager that temporarily makes ``vitruvius.config.load_config``
    return an in-memory config with every ``w_*`` flag set to True.

    The on-disk ``config/vitruvius.yaml`` is never touched. The
    ``load_config`` lru_cache is cleared on entry and exit so no stale
    cached dict leaks across the boundary.

    Yields:
        The mutated config dict (for test introspection / snapshotting).
    """
    from vitruvius import config as cfgmod

    base_on_disk = _load_config_from_disk()
    flag_on = _build_flag_on_config(base=base_on_disk, model=model)

    # Clear cached dict so the old value is not observed mid-bench.
    cfgmod.load_config.cache_clear()

    # Patch ``load_config`` so every code path (ollama_review,
    # _features_block, get_ollama_default_model, ...) observes the
    # flag-on view. ``_features_block`` is implemented as
    # ``load_config().get('features', {})`` so patching ``load_config``
    # alone is sufficient to flip every flag.
    with patch.object(cfgmod, "load_config", return_value=flag_on):
        try:
            yield flag_on
        finally:
            # Clear cache on exit too — if any call during the patch
            # bypassed the mock (unlikely, but defensive), the next
            # un-patched lookup should re-read from disk.
            cfgmod.load_config.cache_clear()


class _RssSampler:
    """Background thread sampling ``psutil.Process().memory_info().rss``
    every ``interval_s`` seconds and tracking the peak in MB.

    Start with :meth:`start`, stop with :meth:`stop`, read the peak
    from :attr:`peak_rss_mb` after stopping.
    """

    def __init__(self, *, interval_s: float = 0.5) -> None:
        self._interval_s = interval_s
        self._proc: Any | None = psutil.Process() if psutil is not None else None
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self.peak_rss_mb: float = 0.0
        self.backend = "psutil" if self._proc is not None else "resource.getrusage"

    def _rss_mb(self) -> float:
        """Return RSS in MB using the best available backend."""
        if self._proc is not None:
            return self._proc.memory_info().rss / (1024 * 1024)

        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform == "darwin":
            return rss / (1024 * 1024)
        return rss / 1024

    def _run(self) -> None:
        # Seed with the current RSS so even a zero-sample run returns
        # something sensible.
        self.peak_rss_mb = max(self.peak_rss_mb, self._rss_mb())
        while not self._stop_event.is_set():
            try:
                rss_mb = self._rss_mb()
            except Exception:
                break
            if rss_mb > self.peak_rss_mb:
                self.peak_rss_mb = rss_mb
            # Wait the interval but wake early on stop.
            if self._stop_event.wait(self._interval_s):
                break

    def start(self) -> None:
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, name="livewiring-rss-sampler", daemon=True
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None


def _require_extraction_report() -> Path:
    """Return the path to the PD 1096 extraction sections JSON, raising
    ``FileNotFoundError`` with a loud message if it is missing.
    """
    path = (
        get_repo_root()
        / "006_System-Manifests"
        / "runs"
        / "latest_relationship_extraction_sections.json"
    )
    if not path.exists():
        raise FileNotFoundError(
            "Live bench requires "
            "006_System-Manifests/runs/latest_relationship_extraction_sections.json "
            "to exist. Re-run `extract-relationships-one` on the PD 1096 IRR and "
            "copy the output into that path before invoking the bench."
        )
    return path


def _read_review_report() -> dict[str, Any]:
    path = (
        get_repo_root()
        / "006_System-Manifests"
        / "runs"
        / "latest_relationship_review_ollama.json"
    )
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _count_reviewed_candidates(report: dict[str, Any]) -> int:
    # Prefer the top-level count the review module writes explicitly;
    # fall back to len(reviews) when the field is missing.
    total = report.get("completed_reviews")
    if isinstance(total, int) and total > 0:
        return total
    return len(report.get("reviews", []))


def run_livewiring_bench(
    *,
    model: str = DEFAULT_BENCH_MODEL,
    timeout_seconds: int = DEFAULT_BENCH_TIMEOUT_SECONDS,
    sampler_interval_s: float = 0.5,
) -> dict[str, Any]:
    """Run the live PD 1096 review bench with every ``w_*`` flag on and
    return a one-block summary dict.

    The ``config/vitruvius.yaml`` file is never mutated.

    Returns:
        dict with keys:
            peak_rss_mb: float (MB)
            wall_seconds: float
            candidates_reviewed: int
            ms_per_candidate: float
            flag_on_config_snapshot: dict (the in-memory config used)
            notes: str (empty when clean; populated on overshoot)

    Raises:
        FileNotFoundError: if the extraction sections JSON is missing.
    """
    _require_extraction_report()

    sampler = _RssSampler(interval_s=sampler_interval_s)
    sampler.start()
    start = time.perf_counter()
    with flag_on_config(model=model) as flag_on:
        from vitruvius.ollama_review import run_review_relationships_ollama

        exit_code = run_review_relationships_ollama(
            model=model,
            timeout_seconds=timeout_seconds,
            parallelism=1,
        )
    wall_seconds = time.perf_counter() - start
    sampler.stop()

    report = _read_review_report()
    candidates_reviewed = _count_reviewed_candidates(report)
    ms_per_candidate = (
        (wall_seconds * 1000.0) / candidates_reviewed if candidates_reviewed else 0.0
    )

    notes_parts: list[str] = []
    if exit_code != 0:
        notes_parts.append(f"review exit_code={exit_code}")
    if sampler.peak_rss_mb > PEAK_RSS_CEILING_MB:
        notes_parts.append(
            f"peak_rss_mb={sampler.peak_rss_mb:.1f} exceeds "
            f"{PEAK_RSS_CEILING_MB} MB informational ceiling"
        )

    return {
        "peak_rss_mb": round(sampler.peak_rss_mb, 2),
        "wall_seconds": round(wall_seconds, 3),
        "candidates_reviewed": candidates_reviewed,
        "ms_per_candidate": round(ms_per_candidate, 2),
        "flag_on_config_snapshot": flag_on,
        "notes": "; ".join(notes_parts),
    }


def main() -> int:
    summary = run_livewiring_bench()
    # Trim the snapshot for terminal output — the raw dict is enormous.
    printable = {
        "peak_rss_mb": summary["peak_rss_mb"],
        "wall_seconds": summary["wall_seconds"],
        "candidates_reviewed": summary["candidates_reviewed"],
        "ms_per_candidate": summary["ms_per_candidate"],
        "flag_on_config_snapshot": {
            "features": summary["flag_on_config_snapshot"].get("features", {}),
            "review": summary["flag_on_config_snapshot"].get("review", {}),
        },
        "notes": summary["notes"],
    }
    print(json.dumps(printable, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
