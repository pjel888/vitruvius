"""Stream S1.3 — ontology prompt builder appends a <logic> directive
when ``features.z_neuro_symbolic`` is enabled.

The flag-OFF path MUST remain byte-identical to the pre-Sprint-Z
baseline so the rest of the review pipeline sees no drift.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius import config as cfgmod
from vitruvius.review.ontology_prompt_builder import (
    build_prompt_with_neighborhood,
)


@pytest.fixture
def tmp_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True)

    def _write(flag_on: bool) -> None:
        cfg.write_text(
            "features:\n"
            f"  z_neuro_symbolic: {'true' if flag_on else 'false'}\n",
            encoding="utf-8",
        )
        cfgmod.load_config.cache_clear()

    monkeypatch.setattr(cfgmod, "get_repo_root", lambda: tmp_path)
    cfgmod.load_config.cache_clear()
    try:
        yield cfg, _write
    finally:
        cfgmod.load_config.cache_clear()


def test_prompt_contains_logic_directive_when_flag_on(tmp_config) -> None:
    _, write = tmp_config
    write(True)

    prompt = build_prompt_with_neighborhood(
        candidate_text="Building A has a side setback of 1.8m.",
        neighborhood=[],
    )
    assert "<logic-directive>" in prompt
    assert "Datalog" in prompt or "datalog" in prompt
    assert "has_distance" in prompt
    assert "applies_to" in prompt


def test_prompt_omits_logic_directive_when_flag_off(tmp_config) -> None:
    _, write = tmp_config
    write(False)

    prompt = build_prompt_with_neighborhood(
        candidate_text="Building A has a side setback of 1.8m.",
        neighborhood=[],
    )
    assert "<logic" not in prompt
    assert "Datalog" not in prompt


def test_prompt_flag_off_is_byte_identical_to_base(tmp_config) -> None:
    """The flag-OFF path MUST be byte-identical to the pre-S1.3 baseline.

    We reach into the module to pull the private base-prompt builder
    and compare its output to the public API's output with the flag
    disabled.
    """
    from vitruvius.review import ontology_prompt_builder as mod

    _, write = tmp_config
    write(False)

    candidate = "Building A has a side setback of 1.8m."
    base = mod._build_prompt_base(candidate, [])
    public = build_prompt_with_neighborhood(candidate_text=candidate, neighborhood=[])
    assert base == public


def test_prompt_flag_on_appends_directive_after_base(tmp_config) -> None:
    """When the flag is on the directive is appended, and the base prefix
    is preserved byte-identically."""
    from vitruvius.review import ontology_prompt_builder as mod

    _, write = tmp_config
    write(True)

    candidate = "Building A has a side setback of 1.8m."
    base = mod._build_prompt_base(candidate, [])
    public = build_prompt_with_neighborhood(
        candidate_text=candidate, neighborhood=[]
    )
    assert public.startswith(base)
    assert public != base
    assert public == base + mod._LOGIC_DIRECTIVE
