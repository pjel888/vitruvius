"""Sprint CLEANUP-1 Stream C4 — Phase 5E LLM candidate proposer.

Proposes relationship candidates via a local Ollama call. Output conforms
to the closed predicate vocabulary at scripts/vitruvius/rules/relationship_registry.yaml.

Gated behind `p5e_llm_extraction`. Flag-off is a strict no-op (no Ollama
call, empty list returned).

Perf call: orchestration + Ollama HTTP + JSON parse. Above the Rust Line
per AD-036. Python is the correct choice — moving this to Rust would gain
nothing because the bottleneck is the LLM call itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


ALLOWED_PREDICATES = frozenset(
    {"governs", "defines", "requires", "depends_on", "limits", "affects", "supersedes"}
)


@dataclass(frozen=True)
class ProposedCandidate:
    from_id: str
    predicate: str
    to_id: str
    evidence: str
    confidence: float
    source: str = "llm_proposer"  # distinguishes from regex candidates in merge


def propose_relationships_llm(
    *,
    section_text: str,
    section_id: str,
    source_id: str,
    model: str = "gemma4:31b",
    timeout_seconds: int = 120,
) -> List[ProposedCandidate]:
    """Call Ollama to propose relationship candidates for a single section.

    Returns an empty list on any error (Ollama unavailable, malformed JSON,
    contract violation, etc.) — the fallback-to-regex behavior is the
    safety net. Flag-off is a no-op.
    """
    raise NotImplementedError("Implemented in Task 10")
