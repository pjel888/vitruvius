"""Follow-on tests for dedupe_by_endpoints: registry-aware predicate selection.

The 2026-04-14 post-dedup end-to-end experiment showed that the initial
priority-only picker chose `defines` for concept->concept edges, which
Rule 7 then rejected as incompatible. The fix: prefer predicates whose
(subject_type, object_type) is valid for the predicate in the registry.
Infer subject/object type from canonical ID prefix (law-* / irr-* /
source-* / irr-* -> source; concept-* -> concept; attribute-* -> attribute).
"""

from vitruvius.relationships_sections import dedupe_by_endpoints


def _cand(from_id, type_, to, occurrences=1):
    return {
        "from": from_id,
        "type": type_,
        "to": to,
        "occurrences": occurrences,
        "sections": [],
        "examples": [],
    }


def test_prefers_registry_compatible_predicate_over_priority():
    # concept->concept: `defines` is INCOMPATIBLE (needs source subject),
    # `requires` is compatible. Priority order would pick defines.
    cands = [
        _cand("concept-a", "defines", "concept-b", occurrences=1),
        _cand("concept-a", "requires", "concept-b", occurrences=1),
        _cand("concept-a", "affects", "concept-b", occurrences=1),
    ]
    result = dedupe_by_endpoints(cands)
    assert len(result) == 1
    assert result[0]["type"] in {"requires", "affects", "depends_on"}
    # `defines` must NOT be the winner for concept->concept
    assert result[0]["type"] != "defines"


def test_source_to_concept_still_uses_priority():
    # source->concept: `governs` and `defines` and `limits` and `affects`
    # are all compatible. Priority should still pick governs.
    cands = [
        _cand("law-pd-1096", "affects", "concept-a", occurrences=1),
        _cand("law-pd-1096", "governs", "concept-a", occurrences=1),
    ]
    result = dedupe_by_endpoints(cands)
    assert result[0]["type"] == "governs"


def test_falls_back_to_priority_when_no_compatible_predicate():
    # If NO predicate in the group is compatible, fall back to priority
    # order — the record will be rejected at Rule 7 but at least the
    # dedup doesn't silently discard it.
    cands = [
        _cand("attribute-foo", "defines", "attribute-bar", occurrences=1),
        _cand("attribute-foo", "requires", "attribute-bar", occurrences=1),
    ]
    result = dedupe_by_endpoints(cands)
    # Neither defines nor requires has attribute->attribute in the registry.
    # Falls back to priority: defines wins.
    assert result[0]["type"] == "defines"


def test_concept_to_concept_picks_compatible_by_priority():
    # Given multiple compatible predicates, still use priority among them.
    # concept->concept compatible: requires, depends_on, affects (per registry)
    cands = [
        _cand("concept-a", "affects", "concept-b", occurrences=1),
        _cand("concept-a", "depends_on", "concept-b", occurrences=1),
        _cand("concept-a", "requires", "concept-b", occurrences=1),
    ]
    result = dedupe_by_endpoints(cands)
    # requires > depends_on > affects in PREDICATE_PRIORITY
    assert result[0]["type"] == "requires"
