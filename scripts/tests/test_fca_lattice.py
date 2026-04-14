"""FCA lattice builder — NextClosure enumeration + Hasse cover computation."""

from __future__ import annotations

import json
from pathlib import Path

from vitruvius.features import Features
from vitruvius.concepts.fca_lattice import (
    ConceptLattice,
    FormalConcept,
    HasseEdge,
    build_lattice,
)


# Classic textbook example: "living beings" with 4 objects and 4 attributes
# (adapted from Ganter & Wille, Formal Concept Analysis: Mathematical
# Foundations, p. 20).
CLASSIC_OBJECTS = ["fish", "frog", "dog", "bird"]
CLASSIC_ATTRS = ["needs_water", "lives_on_land", "can_fly", "has_legs"]
CLASSIC_INCIDENCE = [
    [1, 0, 0, 0],  # fish:  water only
    [1, 1, 0, 1],  # frog:  water, land, legs
    [0, 1, 0, 1],  # dog:   land, legs
    [0, 1, 1, 1],  # bird:  land, fly, legs
]


def test_small_binary_matrix_builds_correct_lattice() -> None:
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    # There should be at least a few concepts including the top and bottom
    assert len(lattice.concepts) >= 4
    # Every concept is internally consistent: its intent equals the attributes
    # shared by all objects in its extent
    for concept in lattice.concepts:
        for attr in concept.intent:
            attr_idx = CLASSIC_ATTRS.index(attr)
            for obj in concept.extent:
                obj_idx = CLASSIC_OBJECTS.index(obj)
                assert CLASSIC_INCIDENCE[obj_idx][attr_idx] == 1


def test_lattice_top_concept_has_full_extent() -> None:
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    top = max(lattice.concepts, key=lambda c: len(c.extent))
    assert set(top.extent) == set(CLASSIC_OBJECTS)
    # CLASSIC has no universally shared attribute
    assert top.intent == ()


def test_lattice_bottom_concept_has_all_attributes_in_intent() -> None:
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    bottom = max(lattice.concepts, key=lambda c: len(c.intent))
    assert bottom.extent == ()
    assert set(bottom.intent) == set(CLASSIC_ATTRS)


def test_hasse_edges_are_covering_relations_only() -> None:
    """No transitive edges: parent->mid->child must not also have parent->child."""
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    edges_set = {(e.parent_index, e.child_index) for e in lattice.edges}
    children_of: dict[int, set[int]] = {}
    for e in lattice.edges:
        children_of.setdefault(e.parent_index, set()).add(e.child_index)

    def has_path_length_at_least_2(src: int, dst: int) -> bool:
        if src == dst:
            return False
        frontier = children_of.get(src, set()) - {dst}
        visited = set(frontier)
        while frontier:
            new_frontier: set[int] = set()
            for node in frontier:
                for child in children_of.get(node, set()):
                    if child == dst:
                        return True
                    if child not in visited:
                        visited.add(child)
                        new_frontier.add(child)
            frontier = new_frontier
        return False

    for parent, child in edges_set:
        assert not has_path_length_at_least_2(parent, child), (
            f"transitive edge {parent}->{child} found"
        )


def test_deterministic_output() -> None:
    features = Features(flags={"d_fca_lattice": True})
    l1 = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    l2 = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    assert l1 == l2


def test_flag_off_returns_empty_lattice(tmp_path: Path) -> None:
    features = Features(flags={})
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
        runs_dir=runs_dir,
    )
    assert lattice.concepts == ()
    assert lattice.edges == ()
    assert not (runs_dir / "latest_fca_lattice.json").exists()


def test_writes_report_when_runs_dir_provided(tmp_path: Path) -> None:
    features = Features(flags={"d_fca_lattice": True})
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
        runs_dir=runs_dir,
    )
    out = runs_dir / "latest_fca_lattice.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert "concepts" in data
    assert "edges" in data


def test_empty_incidence_matrix_degenerate_case() -> None:
    """Zero objects: lattice has exactly one concept — ({}, M)."""
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=[],
        attributes=["a", "b"],
        incidence=[],
    )
    assert len(lattice.concepts) == 1
    assert lattice.concepts[0].extent == ()
    assert set(lattice.concepts[0].intent) == {"a", "b"}


def test_every_extent_and_intent_is_sorted() -> None:
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    for c in lattice.concepts:
        assert list(c.extent) == sorted(c.extent)
        assert list(c.intent) == sorted(c.intent)


def test_identity_incidence_every_object_has_every_attribute() -> None:
    """Universal-attribute matrix: lattice has exactly one concept — (G, M)."""
    features = Features(flags={"d_fca_lattice": True})
    objects = ["o1", "o2", "o3"]
    attrs = ["a", "b"]
    incidence = [[1, 1], [1, 1], [1, 1]]
    lattice = build_lattice(
        features=features,
        objects=objects,
        attributes=attrs,
        incidence=incidence,
    )
    assert len(lattice.concepts) == 1
    assert set(lattice.concepts[0].extent) == set(objects)
    assert set(lattice.concepts[0].intent) == set(attrs)
    assert lattice.edges == ()


def test_empty_attribute_set_degenerate_case() -> None:
    """No attributes: lattice has exactly one concept — (G, {})."""
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=["a", "b", "c"],
        attributes=[],
        incidence=[[], [], []],
    )
    assert len(lattice.concepts) == 1
    assert set(lattice.concepts[0].extent) == {"a", "b", "c"}
    assert lattice.concepts[0].intent == ()


def test_concept_intent_is_closed_under_galois() -> None:
    """For every concept, intent must equal closure(extent): the set of
    attributes shared by ALL objects in extent, AND no more.
    """
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    for concept in lattice.concepts:
        if not concept.extent:
            # empty extent → intent should be all attributes (by convention)
            assert set(concept.intent) == set(CLASSIC_ATTRS)
            continue
        obj_indices = [CLASSIC_OBJECTS.index(o) for o in concept.extent]
        shared: set[str] = set()
        for j, attr in enumerate(CLASSIC_ATTRS):
            if all(CLASSIC_INCIDENCE[i][j] == 1 for i in obj_indices):
                shared.add(attr)
        assert set(concept.intent) == shared


def test_edges_go_from_larger_extent_to_smaller_extent() -> None:
    features = Features(flags={"d_fca_lattice": True})
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
    )
    for edge in lattice.edges:
        parent = lattice.concepts[edge.parent_index]
        child = lattice.concepts[edge.child_index]
        assert set(child.extent) < set(parent.extent)
        assert set(parent.intent) < set(child.intent)


def test_report_json_structure_matches_dataclasses(tmp_path: Path) -> None:
    features = Features(flags={"d_fca_lattice": True})
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    lattice = build_lattice(
        features=features,
        objects=CLASSIC_OBJECTS,
        attributes=CLASSIC_ATTRS,
        incidence=CLASSIC_INCIDENCE,
        runs_dir=runs_dir,
    )
    out = runs_dir / "latest_fca_lattice.json"
    data = json.loads(out.read_text())
    assert len(data["concepts"]) == len(lattice.concepts)
    assert len(data["edges"]) == len(lattice.edges)
    for entry, concept in zip(data["concepts"], lattice.concepts):
        assert entry["extent"] == list(concept.extent)
        assert entry["intent"] == list(concept.intent)
    for entry, edge in zip(data["edges"], lattice.edges):
        assert entry["parent_index"] == edge.parent_index
        assert entry["child_index"] == edge.child_index


def test_dataclass_types_are_immutable() -> None:
    concept = FormalConcept(extent=("a",), intent=("x",))
    edge = HasseEdge(parent_index=0, child_index=1)
    try:
        concept.extent = ("b",)  # type: ignore[misc]
    except Exception:
        pass
    else:
        raise AssertionError("FormalConcept should be frozen")
    try:
        edge.parent_index = 5  # type: ignore[misc]
    except Exception:
        pass
    else:
        raise AssertionError("HasseEdge should be frozen")
