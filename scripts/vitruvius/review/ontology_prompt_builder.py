"""Ontology prompt builder — renders graph neighborhoods as LLM prompt fragments (Task F.3)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Sequence

from vitruvius.config import load_config


@dataclass(frozen=True)
class GraphEdgeSummary:
    from_id: str
    to_id: str
    predicate: str
    confidence: float | None = None


@dataclass(frozen=True)
class NeighborhoodPrompt:
    subject_neighborhood: tuple[GraphEdgeSummary, ...]
    object_neighborhood: tuple[GraphEdgeSummary, ...]
    rendered_text: str


def extract_neighborhood(
    edges: Sequence[GraphEdgeSummary],
    *,
    focal_node: str,
    max_hops: int = 2,
    max_edges_per_hop: int = 10,
) -> list[GraphEdgeSummary]:
    if not edges:
        return []

    # adjacency: node -> list of incident edges (stable order = input order)
    adjacency: dict[str, list[GraphEdgeSummary]] = {}
    for edge in edges:
        adjacency.setdefault(edge.from_id, []).append(edge)
        adjacency.setdefault(edge.to_id, []).append(edge)

    if focal_node not in adjacency:
        return []

    visited_nodes: set[str] = {focal_node}
    visited_edges: set[int] = set()
    result: list[GraphEdgeSummary] = []

    frontier: deque[tuple[str, int]] = deque([(focal_node, 0)])

    while frontier:
        node, hop = frontier.popleft()
        if hop >= max_hops:
            continue
        incident = adjacency.get(node, [])
        added_this_hop = 0
        for edge in incident:
            edge_key = id(edge)
            if edge_key in visited_edges:
                continue
            if added_this_hop >= max_edges_per_hop:
                break
            visited_edges.add(edge_key)
            result.append(edge)
            added_this_hop += 1
            next_node = edge.to_id if edge.from_id == node else edge.from_id
            if next_node not in visited_nodes:
                visited_nodes.add(next_node)
                frontier.append((next_node, hop + 1))

    return result


def _render_edge_line(edge: GraphEdgeSummary) -> str:
    conf_part = (
        f" (conf={edge.confidence:.2f})" if edge.confidence is not None else ""
    )
    return f"  - {edge.from_id} --[{edge.predicate}]--> {edge.to_id}{conf_part}"


def _render_section(header: str, edges: tuple[GraphEdgeSummary, ...]) -> str:
    if not edges:
        return f"{header}\n  (no adjacent edges)"
    lines = [header] + [_render_edge_line(e) for e in edges]
    return "\n".join(lines)


def build_neighborhood_prompt(
    *,
    candidate_subject: str,
    candidate_object: str,
    edges: Sequence[GraphEdgeSummary],
    max_hops: int = 2,
    max_edges_per_hop: int = 10,
    source_identity: "Any" = None,  # Stream Y1.4 — optional priming identity
) -> NeighborhoodPrompt:
    subject_edges = tuple(
        extract_neighborhood(
            edges,
            focal_node=candidate_subject,
            max_hops=max_hops,
            max_edges_per_hop=max_edges_per_hop,
        )
    )
    object_edges = tuple(
        extract_neighborhood(
            edges,
            focal_node=candidate_object,
            max_hops=max_hops,
            max_edges_per_hop=max_edges_per_hop,
        )
    )

    subject_header = f"Subject neighborhood ({candidate_subject}):"
    object_header = f"Object neighborhood ({candidate_object}):"

    sections = [
        _render_section(subject_header, subject_edges),
        _render_section(object_header, object_edges),
    ]
    if source_identity is not None:
        # Stream Y1.4 — prepend a deterministic SOURCE_IDENTITY block so
        # every downstream prompt builder gets the document's legal
        # context for free. Flag-OFF path (source_identity=None) is
        # byte-identical to the pre-Y1.4 render.
        identity_block = (
            f"SOURCE_IDENTITY[{source_identity.fingerprint}]: "
            f"{source_identity.prose}"
        )
        sections.insert(0, identity_block)

    rendered = "\n".join(sections)

    return NeighborhoodPrompt(
        subject_neighborhood=subject_edges,
        object_neighborhood=object_edges,
        rendered_text=rendered,
    )


# ---------------------------------------------------------------------------
# Stream S1.3 — neuro-symbolic <logic> directive
# ---------------------------------------------------------------------------
# When features.z_neuro_symbolic is true, reviewer prompts are appended
# with a `<logic-directive>` block that forces the LLM to emit a
# `<logic>` Datalog fact set the S1.2 Rust evaluator can verify. The
# flag-OFF path is byte-identical to the pre-Sprint-Z baseline.

_LOGIC_DIRECTIVE = (
    "\n\n<logic-directive>\n"
    "You MUST output a <logic> block containing Datalog facts of the form\n"
    "    predicate(subject, object).\n"
    "Use only these predicates: has_distance, requires_distance, less_than,\n"
    "applies_to. End the block with a single conclusion line of the form\n"
    "    conclusion: violates(building_X, rule_Y).\n"
    "The Rust Datalog evaluator will reject your verdict if the logic block\n"
    "fails to parse or fails to derive the conclusion from the facts.\n"
    "</logic-directive>\n"
)


def _neuro_symbolic_enabled() -> bool:
    """Return True iff ``features.z_neuro_symbolic`` is set in the repo config."""
    try:
        cfg = load_config()
    except Exception:
        return False
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    if not isinstance(flags, dict):
        return False
    return bool(flags.get("z_neuro_symbolic", False))


def _build_prompt_base(
    candidate_text: str,
    neighborhood: Sequence[dict[str, Any]],
) -> str:
    """Deterministic base prompt body used by :func:`build_prompt_with_neighborhood`.

    Keeps the Sprint Z neuro-symbolic directive out of the pre-S1.3
    rendering so the flag-OFF path in :func:`build_prompt_with_neighborhood`
    stays byte-identical to the historical baseline.

    The body is intentionally plain text — downstream reviewer code
    concatenates it with graph neighborhood blocks from
    :func:`build_neighborhood_prompt`.
    """
    lines: list[str] = ["Candidate:", candidate_text.strip()]
    if neighborhood:
        lines.append("")
        lines.append("Neighborhood context:")
        for entry in neighborhood:
            lines.append(f"  - {entry}")
    return "\n".join(lines)


def build_prompt_with_neighborhood(
    candidate_text: str,
    neighborhood: list[dict[str, Any]] | None = None,
) -> str:
    """Build a review prompt that optionally injects a neuro-symbolic directive.

    When ``features.z_neuro_symbolic`` is true, the prompt appends a
    ``<logic-directive>`` that forces the LLM to emit a ``<logic>``
    Datalog block the Sprint Z Stream S1.2 Rust evaluator can verify.
    When the flag is false the returned string is byte-identical to the
    pre-Sprint-Z baseline (the :func:`_build_prompt_base` output).

    Parameters
    ----------
    candidate_text:
        The raw candidate relationship text being reviewed.
    neighborhood:
        Optional list of graph neighborhood entries produced upstream.
        ``None`` and ``[]`` are treated identically.
    """
    base = _build_prompt_base(candidate_text, neighborhood or [])
    if _neuro_symbolic_enabled():
        return base + _LOGIC_DIRECTIVE
    return base
