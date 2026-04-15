"""Sprint CLEANUP-1 Stream C4.3 — merge regex + LLM relationship candidates.

The merger combines regex-extracted candidates (Phase 5 baseline) with
LLM-proposed candidates (Phase 5E) into a single list, deduped by
(from_id, predicate, to_id). On overlap, the regex candidate wins
because it has a longer track record of passing Phase 6A/6B review.

Gated behind `p5e_llm_extraction`. Flag-off is a no-op (the merger is
not called, and the caller uses the regex list as-is).

Perf call: dict ops over small lists (typically <100 candidates per
section). Above the Rust Line (AD-036).
"""

from __future__ import annotations

from typing import Iterable, List

from vitruvius.relationships.llm_proposer import ProposedCandidate


def _candidate_key(c: dict) -> tuple:
    return (c.get("from", ""), c.get("type", ""), c.get("to", ""))


def merge_regex_and_llm(
    regex_candidates: List[dict],
    llm_candidates: Iterable[ProposedCandidate],
) -> List[dict]:
    """Return a single list with regex + LLM candidates, deduped by endpoint/predicate.

    Regex candidates win on overlap (they preserve their `occurrences`,
    `sections`, and `examples` fields). LLM candidates are converted into
    the regex dict shape with `source: "llm_proposer"` so downstream
    code can distinguish them.
    """
    merged: dict[tuple, dict] = {}

    for r in regex_candidates:
        # Tag regex-origin candidates so downstream audit can distinguish them
        # from LLM-proposed ones. `source: "regex"` satisfies the merger
        # contract; test_merge_regex_only tolerates missing (via .get)
        # while test_merge_deduplicates_overlapping_endpoints requires the key.
        if "source" not in r:
            r = {**r, "source": "regex"}
        merged[_candidate_key(r)] = r

    for llm in llm_candidates:
        key = (llm.from_id, llm.predicate, llm.to_id)
        if key in merged:
            continue  # regex wins
        merged[key] = {
            "from": llm.from_id,
            "type": llm.predicate,
            "to": llm.to_id,
            "occurrences": 1,
            "sections": [],
            "examples": [llm.evidence],
            "source": "llm_proposer",
            "llm_confidence": llm.confidence,
        }

    return list(merged.values())
