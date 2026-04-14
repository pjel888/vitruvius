"""Reflection parser — LLM <thought_process> block extraction (Task F.6)."""

from __future__ import annotations

import re
from dataclasses import dataclass


THOUGHT_BLOCK_PATTERN = re.compile(
    r"<thought_process>(.*?)</thought_process>",
    re.DOTALL | re.IGNORECASE,
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
