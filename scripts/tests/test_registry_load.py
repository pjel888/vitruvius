from vitruvius.promotion_validator import load_registry


def test_registry_has_seven_predicates():
    registry = load_registry()
    predicates = registry["predicates"]
    expected = {"governs", "defines", "requires", "depends_on", "limits", "affects", "supersedes"}
    assert set(predicates.keys()) == expected


def test_governs_allows_source_to_concept():
    registry = load_registry()
    pairs = registry["predicates"]["governs"]["allowed_pairs"]
    assert {"subject_type": "source", "object_type": "concept"} in pairs


def test_requires_allows_concept_to_concept():
    registry = load_registry()
    pairs = registry["predicates"]["requires"]["allowed_pairs"]
    assert {"subject_type": "concept", "object_type": "concept"} in pairs
