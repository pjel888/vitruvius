"""Regression test: Stream A dependency bootstrap — every new lib is importable.

This test guards against accidental removal from requirements.txt and against
broken installs on the target 8GB M2 environment. It is split into two parts
to match the staged bootstrap (A1a core scientific stack, then A1b heavy ML
stack) — a failure on A1b does not hide a passing A1a.
"""

from __future__ import annotations

import importlib

import pytest


# A1a — core scientific stack (small, pure-C or pure-Python, installs in seconds)
CORE_PACKAGES = [
    "numpy",
    "scipy",
    "sklearn",         # scikit-learn imports as sklearn
    "rapidfuzz",
    "pycrfsuite",      # python-crfsuite imports as pycrfsuite
    "networkx",
    "community",       # python-louvain imports as community
    "ot",              # POT imports as ot
]


@pytest.mark.parametrize("pkg", CORE_PACKAGES)
def test_core_package_importable(pkg: str) -> None:
    importlib.import_module(pkg)
