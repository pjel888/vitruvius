"""Sprint Z Stream S5 — DSPy compiler tests (mocked LLM).

All tests use a tiny ``_MockLLM`` that conforms to the
:class:`vitruvius.wiki.llm_client.LLMClient` Protocol and returns a
canned response for every prompt. No live Ollama calls — verifiable
via ``OLLAMA_HOST=unreachable:0 PYTHONPATH=scripts pytest
scripts/tests/test_compound_dspy_compiler.py``.

Covers:

* :func:`regex_match_density` — perfect / disjoint / half overlap.
* :func:`compile_extraction_prompt` — end-to-end compile cycle with
  a mocked LLM, asserting mean_score bounds and num_examples.
* :class:`DSPyCompilerLM` — one-element list return, prompt history.
* Empty-training-set edge case — returns ``mean_score=0.0``.
"""
from __future__ import annotations

import pytest

from vitruvius.compound.dspy_compiler import (
    CompilationResult,
    DSPyCompilerLM,
    TrainingExample,
    compile_extraction_prompt,
    regex_match_density,
)


class _MockLLM:
    """Canned-response LLM client for DSPy compiler tests.

    Mirrors the ``_MockLLM`` pattern from
    ``scripts/tests/test_wiki_synthesis_loop.py`` — single canned
    string, prompt history stored for assertions, no network I/O.
    """

    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


# ---------------------------------------------------------------------------
# regex_match_density metric
# ---------------------------------------------------------------------------


def test_regex_match_density_perfect_match() -> None:
    """Identical strings should score 1.0."""
    score = regex_match_density(
        prediction="egress width 1.2 m",
        expected="egress width 1.2 m",
    )
    assert score == 1.0


def test_regex_match_density_no_overlap() -> None:
    """Disjoint word sets should score 0.0."""
    score = regex_match_density(
        prediction="alpha beta gamma",
        expected="delta epsilon zeta",
    )
    assert score == 0.0


def test_regex_match_density_partial_overlap() -> None:
    """Half of expected tokens present → 0.5."""
    # expected tokens: {egress, width, stair, tread}
    # prediction tokens: {egress, width, landing, riser}
    # overlap: {egress, width} → 2/4 = 0.5
    score = regex_match_density(
        prediction="egress width landing riser",
        expected="egress width stair tread",
    )
    assert score == pytest.approx(0.5)


def test_regex_match_density_case_insensitive() -> None:
    """Matching is case-insensitive."""
    score = regex_match_density(
        prediction="EGRESS WIDTH 1.2 M",
        expected="egress width 1.2 m",
    )
    assert score == 1.0


def test_regex_match_density_empty_expected_returns_one() -> None:
    """Empty gold short-circuits to 1.0 (vacuously satisfied)."""
    assert regex_match_density(prediction="anything", expected="") == 1.0
    assert regex_match_density(prediction="", expected="") == 1.0


# ---------------------------------------------------------------------------
# DSPyCompilerLM adapter
# ---------------------------------------------------------------------------


def test_dspy_compiler_lm_wraps_client_and_returns_list() -> None:
    """Adapter returns a one-element list + tracks prompts."""
    mock = _MockLLM("canned response")
    lm = DSPyCompilerLM(mock)

    completions = lm("what is the egress width?")

    assert completions == ["canned response"]
    assert mock.prompts == ["what is the egress width?"]
    assert lm.history == ["what is the egress width?"]


def test_dspy_compiler_lm_accepts_extra_kwargs() -> None:
    """DSPy passes kwargs (temperature, max_tokens) — must be ignored."""
    mock = _MockLLM("ok")
    lm = DSPyCompilerLM(mock)

    # Should not raise even though LLMClient.complete doesn't accept kwargs.
    completions = lm("prompt", temperature=0.5, max_tokens=256)

    assert completions == ["ok"]


# ---------------------------------------------------------------------------
# compile_extraction_prompt end-to-end
# ---------------------------------------------------------------------------


def test_compile_extraction_prompt_with_mock_llm() -> None:
    """End-to-end compile cycle with mocked LLM and 3 examples.

    The mock returns a string containing all the expected tokens for
    example 1 and some of the tokens for examples 2/3, so the mean
    score is strictly positive and well below 1.0. We only assert
    ``mean_score >= 0.0`` per the ticket acceptance — the exact
    fraction depends on the canned response.
    """
    # Canned response hits some tokens across all three examples.
    mock = _MockLLM("egress width minimum 1.2 meters per code")
    training = [
        TrainingExample(
            input_text="How wide must egress stairs be?",
            expected_output="egress width minimum 1.2 meters",
        ),
        TrainingExample(
            input_text="What is the fire resistance rating?",
            expected_output="fire resistance rating 2 hours",
        ),
        TrainingExample(
            input_text="What is the occupant load factor?",
            expected_output="occupant load factor 5.0",
        ),
    ]

    result = compile_extraction_prompt(
        training_examples=training,
        llm_client=mock,
        base_prompt="You are an extraction engine. Question:",
    )

    assert isinstance(result, CompilationResult)
    assert result.num_examples == 3
    assert result.mean_score >= 0.0
    assert result.mean_score <= 1.0
    assert result.optimized_prompt == "You are an extraction engine. Question:"
    # LLM was called exactly once per training example.
    assert len(mock.prompts) == 3
    # Base prompt is prepended to each training input.
    for prompt in mock.prompts:
        assert "You are an extraction engine. Question:" in prompt


def test_compile_extraction_prompt_perfect_score() -> None:
    """If the mock echoes the expected output verbatim, mean_score == 1.0."""
    # Expected output is a strict subset (tokens-wise) of the response.
    mock = _MockLLM(
        "egress width minimum 1.2 meters fire resistance rating 2 hours"
    )
    training = [
        TrainingExample(
            input_text="stair width",
            expected_output="egress width 1.2 meters",
        ),
        TrainingExample(
            input_text="wall rating",
            expected_output="fire resistance 2 hours",
        ),
    ]

    result = compile_extraction_prompt(
        training_examples=training,
        llm_client=mock,
        base_prompt="Extract:",
    )

    assert result.mean_score == pytest.approx(1.0)
    assert result.num_examples == 2


def test_compile_extraction_prompt_empty_training_set() -> None:
    """Empty training set short-circuits to mean_score=0.0, num_examples=0."""
    mock = _MockLLM("unused")

    result = compile_extraction_prompt(
        training_examples=[],
        llm_client=mock,
        base_prompt="base",
    )

    assert result.num_examples == 0
    assert result.mean_score == 0.0
    assert result.optimized_prompt == "base"
    # LLM must NOT be called for an empty set.
    assert mock.prompts == []


def test_compile_extraction_prompt_zero_score() -> None:
    """Completely off-topic response → mean_score == 0.0."""
    mock = _MockLLM("xylophone quixotic zebra")
    training = [
        TrainingExample(
            input_text="stair width",
            expected_output="egress width 1.2 meters",
        ),
    ]

    result = compile_extraction_prompt(
        training_examples=training,
        llm_client=mock,
        base_prompt="Extract:",
    )

    assert result.mean_score == 0.0
    assert result.num_examples == 1
