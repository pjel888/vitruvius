"""Stream D.3 — Formal Concept Analysis lattice builder.

Enumerates every formal concept of a binary object-attribute context via
Ganter's NextClosure (1984), then builds the Hasse diagram of immediate
covers. See .ai/09_archive/plans/statistical-architectural-upgrade-plan.md §8.4
(archived 2026-04-15).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from ..features import Features


_FLAG_NAME = "d_fca_lattice"
_OUTPUT_FILENAME = "latest_fca_lattice.json"


@dataclass(frozen=True)
class FormalConcept:
    extent: tuple[str, ...]
    intent: tuple[str, ...]


@dataclass(frozen=True)
class HasseEdge:
    parent_index: int
    child_index: int


@dataclass(frozen=True)
class ConceptLattice:
    concepts: tuple[FormalConcept, ...]
    edges: tuple[HasseEdge, ...]


def _object_intents(incidence: Sequence[Sequence[int]], n_attrs: int) -> list[frozenset[int]]:
    result: list[frozenset[int]] = []
    for row in incidence:
        attrs = {j for j in range(n_attrs) if j < len(row) and row[j] == 1}
        result.append(frozenset(attrs))
    return result


def _closure(
    attr_set: frozenset[int],
    obj_intents: list[frozenset[int]],
    all_attrs: frozenset[int],
) -> frozenset[int]:
    # extent(attr_set) = { g : attr_set ⊆ obj_intents[g] }
    # closure(attr_set) = intent(extent(attr_set))
    #                   = intersection of obj_intents[g] for g in extent
    extent_indices = [g for g, intent in enumerate(obj_intents) if attr_set <= intent]
    if not extent_indices:
        return all_attrs
    result = obj_intents[extent_indices[0]]
    for g in extent_indices[1:]:
        result = result & obj_intents[g]
    return result


def _extent_of(
    attr_set: frozenset[int],
    obj_intents: list[frozenset[int]],
) -> frozenset[int]:
    return frozenset(g for g, intent in enumerate(obj_intents) if attr_set <= intent)


def _next_closure(
    current: frozenset[int],
    n_attrs: int,
    obj_intents: list[frozenset[int]],
    all_attrs: frozenset[int],
) -> frozenset[int] | None:
    # Enumerate closed sets in lexicographic order over attribute indices
    # 0..n_attrs-1 using Ganter's NextClosure (1984).
    for i in reversed(range(n_attrs)):
        if i in current:
            continue
        prefix = frozenset(m for m in current if m < i)
        candidate = prefix | {i}
        closed = _closure(candidate, obj_intents, all_attrs)
        # Reject if closure introduced any element < i not already in current.
        smaller_new = {m for m in closed if m < i and m not in current}
        if not smaller_new:
            return closed
    return None


def _enumerate_concepts(
    n_attrs: int,
    obj_intents: list[frozenset[int]],
) -> list[frozenset[int]]:
    all_attrs = frozenset(range(n_attrs))
    intents: list[frozenset[int]] = []
    current = _closure(frozenset(), obj_intents, all_attrs)
    intents.append(current)
    while True:
        nxt = _next_closure(current, n_attrs, obj_intents, all_attrs)
        if nxt is None:
            break
        intents.append(nxt)
        current = nxt
    return intents


def _compute_hasse_edges(extents: list[frozenset[int]]) -> list[tuple[int, int]]:
    # Parent has strictly larger extent than child. A parent p directly
    # covers child c iff extents[p] ⊃ extents[c] AND no intermediate
    # concept m exists with extents[p] ⊃ extents[m] ⊃ extents[c].
    n = len(extents)
    edges: list[tuple[int, int]] = []
    for p in range(n):
        for c in range(n):
            if p == c:
                continue
            if not (extents[c] < extents[p]):
                continue
            # Check no intermediate
            has_intermediate = False
            for m in range(n):
                if m == p or m == c:
                    continue
                if extents[c] < extents[m] < extents[p]:
                    has_intermediate = True
                    break
            if not has_intermediate:
                edges.append((p, c))
    return edges


def _build_concepts(
    intents: list[frozenset[int]],
    obj_intents: list[frozenset[int]],
    objects: Sequence[str],
    attributes: Sequence[str],
) -> tuple[list[FormalConcept], list[frozenset[int]]]:
    extents = [_extent_of(intent, obj_intents) for intent in intents]
    # Order concepts by extent size ascending, then by sorted extent names.
    order = sorted(
        range(len(intents)),
        key=lambda k: (
            len(extents[k]),
            tuple(sorted(objects[i] for i in extents[k])),
            tuple(sorted(attributes[j] for j in intents[k])),
        ),
    )
    ordered_extents = [extents[k] for k in order]
    ordered_intents = [intents[k] for k in order]
    concepts = [
        FormalConcept(
            extent=tuple(sorted(objects[i] for i in ordered_extents[idx])),
            intent=tuple(sorted(attributes[j] for j in ordered_intents[idx])),
        )
        for idx in range(len(ordered_extents))
    ]
    return concepts, ordered_extents


def _write_report(runs_dir: Path, lattice: ConceptLattice) -> None:
    payload = {
        "concepts": [
            {"extent": list(c.extent), "intent": list(c.intent)}
            for c in lattice.concepts
        ],
        "edges": [
            {"parent_index": e.parent_index, "child_index": e.child_index}
            for e in lattice.edges
        ],
    }
    out = runs_dir / _OUTPUT_FILENAME
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build_lattice(
    *,
    features: Features,
    objects: Sequence[str],
    attributes: Sequence[str],
    incidence: Sequence[Sequence[int]],
    runs_dir: Path | None = None,
) -> ConceptLattice:
    """Build a formal concept lattice via NextClosure.

    Flag OFF ⇒ empty lattice, no writes. Flag ON enumerates every closed
    attribute set, emits formal concepts plus Hasse edges, and optionally
    writes runs/latest_fca_lattice.json.
    """
    if not features.is_enabled(_FLAG_NAME):
        return ConceptLattice(concepts=(), edges=())

    n_attrs = len(attributes)
    obj_intents = _object_intents(incidence, n_attrs)
    intents = _enumerate_concepts(n_attrs, obj_intents)
    concepts, ordered_extents = _build_concepts(intents, obj_intents, objects, attributes)
    raw_edges = _compute_hasse_edges(ordered_extents)
    raw_edges.sort()
    edges = tuple(HasseEdge(parent_index=p, child_index=c) for p, c in raw_edges)
    lattice = ConceptLattice(concepts=tuple(concepts), edges=edges)
    if runs_dir is not None:
        _write_report(runs_dir, lattice)
    return lattice
