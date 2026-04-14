from vitruvius.relationships_sections import dedupe_by_endpoints


def _cand(from_id, type_, to, occurrences=1, sections=None, examples=None):
    return {
        "from": from_id,
        "type": type_,
        "to": to,
        "occurrences": occurrences,
        "sections": sections or [],
        "examples": examples or [],
    }


def test_empty_list_returns_empty():
    assert dedupe_by_endpoints([]) == []


def test_single_candidate_passes_through_with_empty_alternates():
    result = dedupe_by_endpoints([_cand("a", "governs", "b")])
    assert len(result) == 1
    assert result[0]["from"] == "a"
    assert result[0]["type"] == "governs"
    assert result[0]["to"] == "b"
    assert result[0]["alternate_predicates"] == []


def test_keeps_highest_occurrence_per_endpoint_pair():
    cands = [
        _cand("a", "affects", "b", occurrences=1),
        _cand("a", "requires", "b", occurrences=5),
        _cand("a", "limits", "b", occurrences=2),
    ]
    result = dedupe_by_endpoints(cands)
    assert len(result) == 1
    assert result[0]["type"] == "requires"
    assert result[0]["occurrences"] == 5
    assert sorted(result[0]["alternate_predicates"]) == ["affects", "limits"]


def test_breaks_occurrence_ties_by_priority_order():
    cands = [
        _cand("a", "affects", "b", occurrences=1),
        _cand("a", "requires", "b", occurrences=1),
        _cand("a", "governs", "b", occurrences=1),
    ]
    result = dedupe_by_endpoints(cands)
    # governs > requires > affects in priority
    assert result[0]["type"] == "governs"
    assert set(result[0]["alternate_predicates"]) == {"requires", "affects"}


def test_different_endpoint_pairs_kept_separate():
    cands = [
        _cand("a", "governs", "b"),
        _cand("a", "governs", "c"),
        _cand("x", "governs", "b"),
    ]
    result = dedupe_by_endpoints(cands)
    endpoint_pairs = {(c["from"], c["to"]) for c in result}
    assert endpoint_pairs == {("a", "b"), ("a", "c"), ("x", "b")}


def test_merges_sections_and_examples_from_dropped_candidates():
    cands = [
        _cand("a", "affects", "b", occurrences=3, sections=["sec-1"], examples=["ex1"]),
        _cand("a", "requires", "b", occurrences=5, sections=["sec-2"], examples=["ex2"]),
    ]
    result = dedupe_by_endpoints(cands)
    assert len(result) == 1
    assert result[0]["type"] == "requires"
    # Sections and examples from all candidates for this pair are merged
    assert set(result[0]["sections"]) == {"sec-1", "sec-2"}
    assert set(result[0]["examples"]) == {"ex1", "ex2"}
