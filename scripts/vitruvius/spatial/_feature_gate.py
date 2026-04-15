"""Sprint RUST-MIG-1 Task 5 review fix — shared feature-gate helpers.

The Rust fast paths in ``spatial_edge_builder`` and ``proximity_jump``
(and, as of Task 6, the N4 Mahalanobis outlier detector) each need to
read ``config/vitruvius.yaml`` once per process to decide whether the
``rust_mig_spatial_kernels`` flag is on. Before this module existed
each caller carried its own byte-identical copy of the two helpers
below — a 2-copy drift risk that was about to become 3-copy drift.

Factoring the helpers out here keeps exactly one canonical copy:

* :func:`_resolve_config_path` — honour ``VITRUVIUS_CONFIG`` for
  hermetic tests, fall back to ``<cwd>/config/vitruvius.yaml``.
* :func:`_load_features_cached` — ``lru_cache``-wrapped feature-flag
  loader. Parity tests monkey-patch this attribute directly on each
  caller module (``_pj_module._load_features_cached`` or
  ``_seb_module._load_features_cached``), so callers must import the
  function as a plain module-level attribute — do NOT inline the
  ``load_features`` call inside their fast-path branches.

Naming: the leading underscore marks these as *internal* helpers.
They are deliberately NOT re-exported from
``vitruvius.spatial.__init__``.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from vitruvius.features import Features, load_features


def _resolve_config_path() -> Path:
    """Mirror of ``vitruvius.spatial.cli._resolve_config_path``.

    Honours ``VITRUVIUS_CONFIG`` for hermetic tests, falls back to
    ``<cwd>/config/vitruvius.yaml``. Kept local to this module so the
    spatial edge builder does not pull in the CLI command stack on
    the hot import path.
    """
    env_path = os.environ.get("VITRUVIUS_CONFIG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / "config" / "vitruvius.yaml"


@lru_cache(maxsize=1)
def _load_features_cached() -> Features:
    """Load the feature-flag block once per process.

    The parity test in ``test_spatial_edge_builder_parity.py``
    monkey-patches this function directly, so keep it as a plain
    module-level attribute — do NOT inline the ``load_features``
    call inside ``build_spatial_adjacency_edges`` or the test's
    flag flip will not take effect.
    """
    return load_features(_resolve_config_path())
