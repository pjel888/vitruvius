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


# A1b — heavy ML stack (large, pulls torch; installs in minutes).
HEAVY_PACKAGES = [
    "spacy",
    "sentence_transformers",
]


@pytest.mark.parametrize("pkg", HEAVY_PACKAGES)
def test_heavy_package_importable(pkg: str) -> None:
    importlib.import_module(pkg)


def test_spacy_english_model_loadable() -> None:
    """The en_core_web_sm model is downloaded and loads without network."""
    import spacy

    # This fails with OSError if the model is not downloaded. Do not
    # auto-download in the test — downloads belong in requirements setup.
    nlp = spacy.load("en_core_web_sm")
    # Sanity: the model should tag a simple sentence with a ROOT.
    doc = nlp("The building code requires a permit.")
    assert any(tok.dep_ == "ROOT" for tok in doc)
