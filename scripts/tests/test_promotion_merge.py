from vitruvius.promotion import merge_evidence, evidence_fingerprint, min_confidence


def test_evidence_fingerprint_stable():
    e = {
        "source_id": "law-pd-1096",
        "source_section_id": "sec-701",
        "evidence_snippet": "Every building...",
    }
    assert evidence_fingerprint(e) == evidence_fingerprint(e)


def test_merge_appends_new_evidence():
    existing = [{
        "source_id": "law-pd-1096", "source_section_id": "sec-701",
        "evidence_snippet": "A", "reviewer_confidence": 0.95, "review_decision": "keep",
        "reviewer_model": "gemma4:31b",
    }]
    new = [{
        "source_id": "law-pd-1096", "source_section_id": "sec-702",
        "evidence_snippet": "B", "reviewer_confidence": 0.91, "review_decision": "keep",
        "reviewer_model": "gemma4:31b",
    }]
    merged = merge_evidence(existing, new)
    assert len(merged) == 2


def test_merge_dedups_identical_evidence():
    existing = [{
        "source_id": "law-pd-1096", "source_section_id": "sec-701",
        "evidence_snippet": "A", "reviewer_confidence": 0.95, "review_decision": "keep",
        "reviewer_model": "gemma4:31b",
    }]
    merged = merge_evidence(existing, existing)
    assert len(merged) == 1


def test_merge_recomputes_min_confidence():
    ev = [
        {"reviewer_confidence": 0.95},
        {"reviewer_confidence": 0.91},
        {"reviewer_confidence": 0.99},
    ]
    assert min_confidence(ev) == 0.91
