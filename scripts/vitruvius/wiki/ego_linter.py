"""Sprint WIKI Stream WIKI.4.2 — ego-graph contradiction linter.

When a wiki page is updated, its depth-2 neighborhood (focal page
plus all pages it links to, directly or transitively) may become
logically inconsistent — e.g. the focal page says "Egress width
>= 1.2 m" but a neighbor cached "Egress width >= 0.9 m". This
module passes the focal page + its neighbors to an LLM (through
the :class:`~vitruvius.wiki.llm_client.LLMClient` Protocol) and asks
it to return a JSON list of contradictions. If the list is empty,
the linter returns ``None``.

Scope:
  * Pure structural check — no I/O beyond the injected LLM client.
  * Does not re-compute embeddings or re-run the synthesis loop.
  * Empty neighbor list short-circuits *without* calling the LLM
    (the phase-14 plan only requires contradiction detection
    against known neighbors; an orphan page has nothing to
    contradict).
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from vitruvius.wiki.kuzu_store import WikiPageRow
from vitruvius.wiki.llm_client import LLMClient


@dataclass(frozen=True)
class ContradictionReport:
    """Result of a single ego-graph lint pass.

    Attributes
    ----------
    focal_page_id
        The page_id of the page that was just updated / proposed.
    contradicting_neighbor_ids
        Neighbor page_ids the LLM flagged as incompatible with the
        focal page. Always a tuple so the report is hashable.
    reason
        Human-readable explanation synthesized by the LLM — suitable
        for surfacing in a review UI or CI comment.
    """

    focal_page_id: str
    contradicting_neighbor_ids: tuple[str, ...]
    reason: str


_LINT_PROMPT_TEMPLATE = """\
You are a consistency auditor for a knowledge wiki. Below is a focal
page followed by its depth-2 neighbors. Identify any neighbor whose
claims contradict the focal page — numeric disagreements,
definition drift, or flatly opposing assertions.

Respond with a single JSON object — no prose, no code fences — with
exactly this shape:

  {{"contradictions": [{{"neighbor_id": "...", "reason": "..."}}, ...]}}

If there are no contradictions, respond with
``{{"contradictions": []}}``.

Focal page:
  id={focal_id!r}
  title={focal_title!r}
  tags={focal_tags}
  linked_entities={focal_links}

Neighbors:
{neighbors}
"""


def _render_page(row: WikiPageRow) -> str:
    """Serialize a :class:`WikiPageRow` for inclusion in the prompt."""
    return (
        f"  - id={row.page_id!r}\n"
        f"    title={row.title!r}\n"
        f"    tags={list(row.tags)}\n"
        f"    linked_entities={list(row.linked_entities)}"
    )


def _build_lint_prompt(
    *, focal_page: WikiPageRow, neighbors: list[WikiPageRow]
) -> str:
    rendered = "\n".join(_render_page(n) for n in neighbors)
    return _LINT_PROMPT_TEMPLATE.format(
        focal_id=focal_page.page_id,
        focal_title=focal_page.title,
        focal_tags=list(focal_page.tags),
        focal_links=list(focal_page.linked_entities),
        neighbors=rendered,
    )


def lint_ego_graph(
    *,
    focal_page: WikiPageRow,
    neighbors: list[WikiPageRow],
    llm_client: LLMClient,
) -> ContradictionReport | None:
    """Run one ego-graph contradiction pass.

    Parameters
    ----------
    focal_page
        The page whose neighborhood should be checked — typically
        the page just produced by
        :func:`vitruvius.wiki.synthesis_loop.synthesize_wiki_page`.
    neighbors
        Depth-2 neighbors already fetched from Kuzu. May be empty,
        in which case the function short-circuits without touching
        the LLM.
    llm_client
        Any object conforming to :class:`LLMClient`.

    Returns
    -------
    ContradictionReport | None
        ``None`` when the LLM finds no contradictions (or when
        ``neighbors`` is empty). A :class:`ContradictionReport`
        with a non-empty ``contradicting_neighbor_ids`` otherwise.
    """
    if not neighbors:
        return None

    prompt = _build_lint_prompt(focal_page=focal_page, neighbors=neighbors)
    raw = llm_client.complete(prompt)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned non-JSON response for ego-graph lint: {raw!r}"
        ) from exc

    contradictions = payload.get("contradictions")
    if not isinstance(contradictions, list):
        raise ValueError(
            "LLM response missing required 'contradictions' array: "
            f"{payload!r}"
        )
    if not contradictions:
        return None

    neighbor_ids: list[str] = []
    reasons: list[str] = []
    for entry in contradictions:
        if not isinstance(entry, dict):
            raise ValueError(
                f"contradictions[] entry must be an object, got {entry!r}"
            )
        neighbor_id = entry.get("neighbor_id")
        reason = entry.get("reason", "")
        if not isinstance(neighbor_id, str) or not neighbor_id:
            raise ValueError(
                f"contradictions[] entry missing neighbor_id: {entry!r}"
            )
        neighbor_ids.append(neighbor_id)
        if isinstance(reason, str) and reason:
            reasons.append(f"{neighbor_id}: {reason}")

    return ContradictionReport(
        focal_page_id=focal_page.page_id,
        contradicting_neighbor_ids=tuple(neighbor_ids),
        reason="; ".join(reasons) if reasons else "contradictions reported",
    )


__all__ = ["ContradictionReport", "lint_ego_graph"]
