"""Reflection parser — LLM <thought_process> block extraction (Task F.6).

Stream W2.5 also exposes ``extract_reflection_confidence`` — a narrow
percentage-regex adapter used when the live-wiring path wants just the
self-confidence number without materialising a full ``ReflectionVerdict``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


THOUGHT_BLOCK_PATTERN = re.compile(
    r"<thought_process>(.*?)</thought_process>",
    re.DOTALL | re.IGNORECASE,
)


def extract_reflection_confidence(reason_text: str) -> float | None:
    """Stream W2.5 adapter — pull a percentage confidence from free text.

    Matches patterns like ``"I am 75% confident"`` and returns 0.75.
    Returns ``None`` when no percentage is found. Used by
    ``ollama_review._capture_tension_and_reflection`` to annotate
    verdicts with the model's self-reported confidence when
    ``features.w_review_tension_reflection`` is true.
    """
    if not reason_text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", reason_text)
    if match:
        try:
            return float(match.group(1)) / 100.0
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------------------
# Stream Y3.1 — strict Chain-of-Thought parser.
#
# Upgrades the optional <thought_process> sniffer above into a mandatory
# gate for every LLM verdict. The legacy ``parse_reflection`` is
# untouched — ``parse_cot_strict`` is the new strict path that callers
# must use when ``features.y_thinking_mode_cot`` is true.
# ---------------------------------------------------------------------------


class CotParseError(ValueError):
    """Raised when a strict CoT parse fails validation."""


@dataclass(frozen=True)
class CotResult:
    verdict: str                       # "keep" | "reject" | "abstain"
    self_confidence: float
    reasoning_steps: list[str]
    evidence_citation: str
    escalate: bool = False


_Y3_THINK_RE = re.compile(r"<think>(.*?)</think>", re.DOTALL | re.IGNORECASE)
_Y3_VERDICT_RE = re.compile(r"VERDICT\s*:\s*(keep|reject|abstain)", re.IGNORECASE)
_Y3_CONFIDENCE_RE = re.compile(
    r"self[-\s]?confidence\s*[:=]?\s*([0-9]*\.?[0-9]+)",
    re.IGNORECASE,
)
_Y3_STEP_RE = re.compile(
    r"step\s*\d+[:.]\s*(.+?)(?=\s*step\s*\d+[:.]|self[-\s]?confidence|$)",
    re.IGNORECASE | re.DOTALL,
)
_Y3_CITATION_RE = re.compile(r"""['"]([^'"]{5,})['"]""")


def parse_cot_strict(raw: str, *, escalate_below: float = 0.70) -> CotResult:
    """Parse an LLM response under strict CoT discipline.

    Required artifacts:
      - A ``<think>...</think>`` block.
      - At least one reasoning step labelled ``Step N:`` inside the
        think block.
      - A quoted evidence citation of ≥5 chars inside the think block.
      - A ``Self-confidence: <float>`` line inside the think block.
      - A ``VERDICT: <keep|reject|abstain>`` line OUTSIDE the think block.

    Any missing artifact raises :class:`CotParseError`. Self-confidence
    below ``escalate_below`` sets ``result.escalate = True`` without
    raising so the caller can decide whether to block the verdict or
    route it to a second-pass reviewer.
    """
    think_match = _Y3_THINK_RE.search(raw)
    if not think_match:
        raise CotParseError("no <think> block in response")
    think_body = think_match.group(1).strip()

    outside_think = _Y3_THINK_RE.sub("", raw)
    verdict_match = _Y3_VERDICT_RE.search(outside_think)
    if not verdict_match:
        raise CotParseError("no VERDICT line outside <think> block")

    conf_match = _Y3_CONFIDENCE_RE.search(think_body)
    if not conf_match:
        raise CotParseError("no self-confidence in <think> block")
    confidence = float(conf_match.group(1))

    steps = [s.strip() for s in _Y3_STEP_RE.findall(think_body) if s.strip()]
    if not steps:
        raise CotParseError("no reasoning steps in <think> block")

    citation_match = _Y3_CITATION_RE.search(think_body)
    if not citation_match:
        raise CotParseError("no evidence citation in <think> block")

    return CotResult(
        verdict=verdict_match.group(1).lower(),
        self_confidence=confidence,
        reasoning_steps=steps,
        evidence_citation=citation_match.group(1),
        escalate=confidence < escalate_below,
    )
CONFIDENCE_PATTERN = re.compile(
    r"\bconfidence[:\s]+(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)
HEDGE_WORDS: frozenset[str] = frozenset(
    {
        "might",
        "maybe",
        "possibly",
        "unclear",
        "uncertain",
        "not sure",
        "perhaps",
        "hesitant",
    }
)


@dataclass(frozen=True)
class ReflectionVerdict:
    thought_block: str | None
    self_confidence: float | None
    hedge_words_found: tuple[str, ...]
    halt_auto_promote: bool
    reason: str


def _find_hedges(block_lower: str) -> tuple[str, ...]:
    found = [word for word in HEDGE_WORDS if word in block_lower]
    return tuple(sorted(found))


def parse_reflection(
    llm_response: str,
    *,
    min_confidence_to_promote: float = 0.7,
) -> ReflectionVerdict:
    match = THOUGHT_BLOCK_PATTERN.search(llm_response)
    if match is None:
        return ReflectionVerdict(
            thought_block=None,
            self_confidence=None,
            hedge_words_found=(),
            halt_auto_promote=False,
            reason="no thought block",
        )

    block = match.group(1).strip()
    block_lower = block.lower()

    conf_match = CONFIDENCE_PATTERN.search(block)
    self_confidence: float | None = None
    if conf_match is not None:
        try:
            self_confidence = float(conf_match.group(1))
        except ValueError:
            self_confidence = None

    hedges = _find_hedges(block_lower)

    halt = False
    reasons: list[str] = []
    if self_confidence is not None and self_confidence < min_confidence_to_promote:
        halt = True
        reasons.append(
            f"self_confidence={self_confidence:.2f} < {min_confidence_to_promote}"
        )
    if len(hedges) >= 2:
        halt = True
        reasons.append(f"hedges={list(hedges)}")

    if not reasons:
        reasons.append("no halt signals")

    return ReflectionVerdict(
        thought_block=block,
        self_confidence=self_confidence,
        hedge_words_found=hedges,
        halt_auto_promote=halt,
        reason="; ".join(reasons),
    )
