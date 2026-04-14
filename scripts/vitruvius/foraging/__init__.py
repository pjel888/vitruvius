"""Epistemic foraging (Sprint H Stream O) — scaffold only.

Ships:
  * :mod:`vitruvius.foraging.watched_sources` — YAML loader for the
    declarative registry of external sources the pipeline should
    *eventually* monitor.
  * :mod:`vitruvius.foraging.drift_detector` — thin shim that reuses
    Stream C.4's Mahalanobis outlier detector to flag a source's
    vector drift.
  * :mod:`vitruvius.foraging.duplicate_detector` — SHA-256 content
    hash stub so a newly fetched document can be deduped against
    what's already in the raw layer.

**This subpackage does not perform any network fetches.** Adding a
live HTTP fetcher requires a security review per the plan's §2.2
reopen condition (see .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md).
"""
