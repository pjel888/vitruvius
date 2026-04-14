"""Stream Y1.2 — prompt prefix injector tests."""
from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("sentence_transformers")

from vitruvius.priming.context_vector import SourceIdentity
from vitruvius.priming.prompt_prefix import PriorityLevel, inject_prefix


def _fake_identity() -> SourceIdentity:
    return SourceIdentity(
        fingerprint="deadbeefcafebabe",
        prose=(
            "This document is 'PD 1096 - National Building Code', a national "
            "law issued by Congress on 1977-02-19 under the jurisdiction of PH."
        ),
        vector=np.zeros(384, dtype=np.float32),
    )


def test_prefix_prepends_to_system_message() -> None:
    original = [{"role": "system", "content": "You are a legal reviewer."}]
    result = inject_prefix(original, identity=_fake_identity())
    assert result[0]["role"] == "system"
    assert "deadbeefcafebabe" in result[0]["content"]
    assert "PD 1096" in result[0]["content"]
    assert "You are a legal reviewer." in result[0]["content"]


def test_prefix_does_not_mutate_input() -> None:
    original = [{"role": "system", "content": "orig"}]
    _ = inject_prefix(original, identity=_fake_identity())
    assert original == [{"role": "system", "content": "orig"}]


def test_prefix_inserts_system_if_absent() -> None:
    original = [{"role": "user", "content": "review this"}]
    result = inject_prefix(original, identity=_fake_identity())
    assert result[0]["role"] == "system"
    assert result[1]["role"] == "user"
    assert "deadbeefcafebabe" in result[0]["content"]


def test_priority_level_high_adds_reminder() -> None:
    original = [{"role": "system", "content": "orig"}]
    result = inject_prefix(
        original,
        identity=_fake_identity(),
        priority=PriorityLevel.HIGH,
    )
    assert "DO NOT DRIFT" in result[0]["content"]
