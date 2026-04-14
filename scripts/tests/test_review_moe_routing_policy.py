"""Stream Y2.3 — MoE routing policy loader tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.review.domain_classifier import Domain
from vitruvius.review.slm_router import load_moe_policy


def test_load_valid_policy(tmp_path: Path) -> None:
    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text(
        "geometric: qwen2.5:3b\n"
        "administrative: qwen2.5:7b\n"
        "occupancy: qwen2.5:7b\n"
        "safety: qwen2.5:7b\n"
        "fees: qwen2.5:3b\n"
        "other: qwen2.5:7b\n"
    )
    policy = load_moe_policy(policy_file)
    assert policy[Domain.GEOMETRIC] == "qwen2.5:3b"
    assert policy[Domain.ADMINISTRATIVE] == "qwen2.5:7b"
    assert len(policy) == 6


def test_load_policy_missing_domain_raises(tmp_path: Path) -> None:
    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text("geometric: x\nadministrative: y\n")  # incomplete
    with pytest.raises(ValueError, match="missing domain"):
        load_moe_policy(policy_file)


def test_default_config_file_loads(tmp_path: Path) -> None:
    """The shipped config/moe_routing.yaml should load without errors."""
    shipped = Path(__file__).resolve().parent.parent.parent / "config" / "moe_routing.yaml"
    if not shipped.exists():
        pytest.skip("config/moe_routing.yaml not shipped yet")
    policy = load_moe_policy(shipped)
    assert len(policy) == 6
    for domain in Domain:
        assert domain in policy
