"""Two-stage review routing logic (Phase 6B).

Given Tier-1 Gemma decisions, `select_for_second_pass` filters candidates
that need Tier-2 adjudication. After Tier-2 runs, `route_adjudication`
decides whether the final action is auto_promote, suppress, or
human_review — per the decision table in .ai/08_prompts/qwen-second-pass.txt.
"""

from __future__ import annotations

from typing import Any


CONFIDENCE_CUTOFF = 0.90


def select_for_second_pass(tier_one_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the subset of Tier-1 items that need Tier-2 review."""
    selected: list[dict[str, Any]] = []
    for item in tier_one_items:
        review = item["review"]
        decision = review["decision"]
        confidence = float(review["confidence"])
        suggested = review.get("suggested_type")
        candidate_type = item["candidate"]["type"]

        if decision == "review_further":
            selected.append(item)
            continue

        if decision == "keep" and confidence < CONFIDENCE_CUTOFF:
            selected.append(item)
            continue

        if decision == "reject" and confidence < CONFIDENCE_CUTOFF:
            selected.append(item)
            continue

        if suggested is not None and suggested != candidate_type:
            selected.append(item)
            continue

    return selected


def route_adjudication(pair: dict[str, Any]) -> str:
    """Given a Tier-1 + Tier-2 pair, decide the final action.

    Returns one of: "auto_promote", "suppress", "human_review".
    """
    t1 = pair["tier_one"]
    t2 = pair.get("tier_two")

    t1_dec = t1["decision"]
    t1_conf = float(t1.get("confidence") or 0.0)
    t2_dec = t2["decision"] if t2 else None
    t2_conf = float((t2 or {}).get("confidence") or 0.0)

    if t1_dec == "keep" and t1_conf >= CONFIDENCE_CUTOFF:
        return "auto_promote"

    if t2_dec is None:
        return "human_review"

    if t1_dec == "keep":
        if t2_dec == "keep" and t2_conf >= CONFIDENCE_CUTOFF:
            return "auto_promote"
        return "human_review"

    if t1_dec == "reject":
        if t2_dec == "reject" and t2_conf >= CONFIDENCE_CUTOFF:
            return "suppress"
        return "human_review"

    if t1_dec == "review_further":
        if t2_dec == "reject" and t2_conf >= CONFIDENCE_CUTOFF:
            return "suppress"
        return "human_review"

    return "human_review"
