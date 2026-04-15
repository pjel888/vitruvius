"""Sprint Z Stream S5 — DSPy prompt compilation.

Wraps DSPy's Predict + Signature primitives in a thin interface that
plays nicely with the existing LLMClient Protocol from
:mod:`vitruvius.wiki.llm_client`. The compiler optimises a prompt
against a training set of ``(input, expected_output)`` pairs using a
regex-match density metric.

DSPy's bootstrap fewshot compiler is the only optimiser used in this
narrow ship — more elaborate teleprompters (e.g.
``BootstrapFewShotWithRandomSearch``, ``COPRO``) land in a later
commit once a real training corpus (LGU ordinances, fire-code
excerpts) is wired up. For now the deliverable is:

1. :class:`DSPyCompilerLM` — adapter that wraps an
   :class:`~vitruvius.wiki.llm_client.LLMClient` instance and exposes
   the minimal ``__call__`` surface DSPy's :class:`dspy.BaseLM`
   expects. Implemented from scratch (no ``dspy.LM`` inheritance) so
   that tests can exercise it without touching DSPy's litellm-backed
   network path.
2. :func:`regex_match_density` — pure-stdlib metric that counts
   word-token overlap between the model's prediction and the gold
   expected output. Case-insensitive, empty-gold short-circuits to
   ``1.0``.
3. :func:`compile_extraction_prompt` — runs a single forward pass
   over the training set and returns a :class:`CompilationResult`
   with the mean metric score. The "compilation" collapses to a
   forward pass + average; a future commit can swap the body for
   ``dspy.BootstrapFewShot(...).compile(...)`` once we have a live
   corpus and can tolerate the extra minute of training time.

Tests mock the LLM via a tiny ``complete``-only class — no live
Ollama round trips. See :mod:`scripts.tests.test_compound_dspy_compiler`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

from vitruvius.wiki.llm_client import LLMClient

__all__ = [
    "DSPyCompilerLM",
    "TrainingExample",
    "CompilationResult",
    "regex_match_density",
    "compile_extraction_prompt",
]


_WORD_RE = re.compile(r"\w+", re.UNICODE)


class DSPyCompilerLM:
    """Adapter that exposes an :class:`LLMClient` to DSPy.

    DSPy's :class:`dspy.BaseLM` expects ``__call__(prompt, **kwargs)``
    to return a ``list[str]`` of completions. This adapter wraps a
    single ``LLMClient.complete`` call and returns a one-element list
    — sufficient for the Stream S5 narrow-slice where we only need a
    single-sample forward pass per training example.

    The adapter deliberately does **not** inherit from ``dspy.BaseLM``
    so that the hot path (compile_extraction_prompt) doesn't pull in
    DSPy's litellm/caching machinery during tests. A follow-on commit
    can subclass ``dspy.BaseLM`` once we need bootstrap-fewshot
    traces.

    Parameters
    ----------
    client:
        Any object conforming to
        :class:`vitruvius.wiki.llm_client.LLMClient` — only
        ``complete(prompt)`` is used.
    model:
        Optional display name, surfaced for DSPy telemetry /
        introspection. Defaults to ``"vitruvius-llm-client"``.
    """

    def __init__(self, client: LLMClient, *, model: str = "vitruvius-llm-client") -> None:
        self.client = client
        self.model = model
        # Track prompts for test assertions — mirrors the ``prompts``
        # list on _MockLLM in the WIKI test suite.
        self.history: list[str] = []

    def __call__(self, prompt: str, **kwargs: object) -> list[str]:
        """Return a one-element list with the LLM's completion.

        Matches the ``list[str]`` return shape that DSPy's modules
        (Predict, ChainOfThought) expect from a
        :class:`dspy.BaseLM`. Additional keyword arguments are
        accepted for API compatibility and silently ignored — the
        underlying ``LLMClient`` protocol is deliberately thin.
        """
        self.history.append(prompt)
        response = self.client.complete(prompt)
        return [response]


@dataclass(frozen=True)
class TrainingExample:
    """One ``(input, expected_output)`` pair for prompt compilation.

    Frozen so that :func:`compile_extraction_prompt` can safely
    enumerate the training set without worrying about mid-compilation
    mutation.
    """

    input_text: str
    expected_output: str


@dataclass(frozen=True)
class CompilationResult:
    """Output of a DSPy prompt compilation run.

    Attributes
    ----------
    optimized_prompt:
        The prompt text that scored best on the training set. In the
        narrow-slice implementation this is the base prompt unchanged
        — the real DSPy bootstrap fewshot will return a demo-augmented
        prompt in a follow-on.
    mean_score:
        Arithmetic mean of :func:`regex_match_density` across all
        training examples. ``0.0`` when the training set is empty.
    num_examples:
        Count of training examples processed. Matches
        ``len(training_examples)``.
    """

    optimized_prompt: str
    mean_score: float
    num_examples: int


def regex_match_density(prediction: str, expected: str) -> float:
    """Fraction of ``expected`` word tokens that appear in ``prediction``.

    Case-insensitive, pure stdlib, no fuzzy matching. Empty
    ``expected`` short-circuits to ``1.0`` (vacuously satisfied —
    there are no gold tokens to miss). This matches the Stream S5.2
    "regex-match density" metric described in the phase-12 plan.

    The metric is unordered and position-agnostic: it counts how many
    unique word tokens from ``expected`` occur anywhere in
    ``prediction``. That makes it a coarse-grained extraction signal
    — enough to detect whether the model is emitting the right
    entities, not sensitive to exact phrasing.

    Parameters
    ----------
    prediction:
        Raw model output.
    expected:
        Gold-standard string from the training example.

    Returns
    -------
    float
        A value in ``[0.0, 1.0]``.
    """
    expected_tokens = {tok.lower() for tok in _WORD_RE.findall(expected)}
    if not expected_tokens:
        return 1.0
    prediction_tokens = {tok.lower() for tok in _WORD_RE.findall(prediction)}
    matched = expected_tokens & prediction_tokens
    return len(matched) / len(expected_tokens)


def compile_extraction_prompt(
    *,
    training_examples: Sequence[TrainingExample],
    llm_client: LLMClient,
    base_prompt: str,
) -> CompilationResult:
    """Run one forward pass over ``training_examples`` and score it.

    This is the narrow-slice DSPy compiler: we format each training
    input into ``base_prompt``, ask the LLM to complete, score the
    output against the expected gold string with
    :func:`regex_match_density`, and return the mean.

    A future commit will swap the body for
    ``dspy.BootstrapFewShot(metric=...).compile(...)`` — the API
    shape of this function (kwargs-only, returning
    :class:`CompilationResult`) is designed to stay stable when that
    upgrade lands.

    Parameters
    ----------
    training_examples:
        Sequence of :class:`TrainingExample` pairs. An empty sequence
        returns a :class:`CompilationResult` with ``mean_score=0.0``
        and ``num_examples=0``.
    llm_client:
        Any :class:`LLMClient` — tests pass a mock, production will
        pass the Ollama wrapper.
    base_prompt:
        The seed extraction prompt. The input text is appended with
        a newline separator; callers that need more elaborate
        templating should pre-format their ``base_prompt``.

    Returns
    -------
    CompilationResult
        The compiled prompt + mean score across the training set.
    """
    lm = DSPyCompilerLM(llm_client)
    num_examples = len(training_examples)

    if num_examples == 0:
        return CompilationResult(
            optimized_prompt=base_prompt,
            mean_score=0.0,
            num_examples=0,
        )

    total_score = 0.0
    for example in training_examples:
        full_prompt = f"{base_prompt}\n{example.input_text}"
        completions = lm(full_prompt)
        prediction = completions[0] if completions else ""
        total_score += regex_match_density(prediction, example.expected_output)

    mean_score = total_score / num_examples
    return CompilationResult(
        optimized_prompt=base_prompt,
        mean_score=mean_score,
        num_examples=num_examples,
    )
