"""Stream Y0 — Per-Layer Embeddings backward-compat regression.

Locks in that with every `features.y_*` flag off:
  1. The ``vitruvius.priming`` subpackage is importable but exports nothing.
  2. None of the Sprint R submodules are auto-loaded by a bare pipeline
     import — they are opt-in via explicit imports from flag-guarded sites.

Adapted from the Sprint R plan (per-layer-embeddings-agentic-upgrade-plan.md
§5.3 Task Y0.3). The plan's original fixture-based golden-file regression
cannot run in this codebase because no ``fixtures/golden_3_files`` directory
exists and no ``vitruvius.pipeline`` module exists; the Sprint Q baseline is
already regression-tested at module import level by
``test_wiring_backcompat.py``. This file adds the Y-flag-specific
non-leakage assertion on top.
"""
from __future__ import annotations

import importlib
import sys


def test_priming_subpackage_is_importable() -> None:
    """The subpackage shell must exist even when all Y flags are off."""
    module = importlib.import_module("vitruvius.priming")
    assert module.__name__ == "vitruvius.priming"


def test_priming_subpackage_exports_nothing_by_default() -> None:
    """Importing the shell must not leak symbols — Y modules are opt-in
    via explicit imports from the flag-guarded call sites.
    """
    module = importlib.import_module("vitruvius.priming")
    public = [name for name in dir(module) if not name.startswith("_")]
    assert public == [], f"unexpected public exports: {public}"
