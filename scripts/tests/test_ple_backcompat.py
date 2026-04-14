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
    """The subpackage's ``__init__.py`` must not eagerly import submodules.

    We check the source of ``__init__.py`` rather than ``dir(module)`` so
    the assertion is independent of which submodules other tests have
    already imported this session. Y modules are opt-in via explicit
    imports from the flag-guarded call sites — enforced by keeping the
    ``__init__.py`` free of any ``from .X import Y`` / ``import .X``
    statements.
    """
    import inspect

    module = importlib.import_module("vitruvius.priming")
    source = inspect.getsource(module)
    for line in source.splitlines():
        stripped = line.strip()
        # Ignore comments and docstrings
        if stripped.startswith("#") or not stripped:
            continue
        # The shell must not contain any submodule imports.
        assert not (
            stripped.startswith("from .") or stripped.startswith("import .")
        ), (
            f"vitruvius/priming/__init__.py must not auto-import submodules; "
            f"found: {stripped!r}"
        )
