from __future__ import annotations

import json

from ..graph.centrality import compute_centrality
from ..graph.community import detect_communities
from ..graph.contract import GraphSnapshot
from .nl_translator import ALLOWED_FUNCTIONS


_MAX_COMMUNITIES_IN_PROMPT = 20


def _top_k_central_ids(snapshot: GraphSnapshot, k: int) -> tuple[str, ...]:
    if k <= 0 or not snapshot.nodes:
        return ()
    report = compute_centrality(snapshot, kind="pagerank")
    ids = [nid for nid, _ in report.scores[:k]]
    return tuple(ids)


def _community_summaries(snapshot: GraphSnapshot) -> tuple[str, ...]:
    if not snapshot.nodes:
        return ()
    report = detect_communities(snapshot)
    summaries = [c.summary for c in report.communities[:_MAX_COMMUNITIES_IN_PROMPT]]
    return tuple(summaries)


def build_ontology_prompt(
    question: str,
    *,
    snapshot: GraphSnapshot,
    top_k_central: int = 50,
) -> str:
    central = _top_k_central_ids(snapshot, top_k_central)
    communities = _community_summaries(snapshot)
    payload = {
        "task": "Translate a natural-language question into a structured query call",
        "question": question,
        "allowed_functions": list(ALLOWED_FUNCTIONS),
        "known_entities": list(central),
        "community_summaries": list(communities),
        "output_schema": {
            "function": "one of allowed_functions",
            "arguments": {"subject": "one of known_entities"},
            "confidence": "0.0-1.0",
        },
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
