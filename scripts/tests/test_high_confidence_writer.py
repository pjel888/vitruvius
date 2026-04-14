import json

from vitruvius.ollama_review import write_high_confidence_review


def test_filters_keep_at_or_above_threshold(tmp_path):
    report = {
        "generated_at": "20260414T030000Z",
        "model": "gemma4:31b",
        "source": "003/shared/sources/test.md",
        "total_candidates": 3,
        "completed_reviews": 3,
        "status": "completed",
        "summary": {},
        "reviews": [
            {
                "candidate": {"from": "concept-a", "type": "governs", "to": "concept-b",
                              "sections": ["sec-1"], "examples": ["e1"], "occurrences": 1},
                "review": {"decision": "keep", "confidence": 0.95, "reason": "clear",
                           "suggested_type": None},
            },
            {
                "candidate": {"from": "concept-c", "type": "affects", "to": "concept-d",
                              "sections": ["sec-2"], "examples": ["e2"], "occurrences": 1},
                "review": {"decision": "keep", "confidence": 0.80, "reason": "weak",
                           "suggested_type": None},
            },
            {
                "candidate": {"from": "concept-e", "type": "requires", "to": "concept-f",
                              "sections": ["sec-3"], "examples": ["e3"], "occurrences": 1},
                "review": {"decision": "reject", "confidence": 0.99, "reason": "no",
                           "suggested_type": None},
            },
        ],
    }

    output = write_high_confidence_review(report, tmp_path, threshold=0.90)

    assert output.exists()
    payload = json.loads(output.read_text())
    assert payload["count"] == 1
    assert payload["threshold"] == 0.90
    assert payload["source_model"] == "gemma4:31b"
    assert payload["candidates"][0]["candidate"]["from"] == "concept-a"


def test_empty_when_nothing_passes_threshold(tmp_path):
    report = {
        "generated_at": "20260414T030000Z",
        "model": "gemma4:31b",
        "source": "s",
        "total_candidates": 1,
        "completed_reviews": 1,
        "status": "completed",
        "summary": {},
        "reviews": [
            {
                "candidate": {"from": "a", "type": "governs", "to": "b",
                              "sections": [], "examples": [], "occurrences": 1},
                "review": {"decision": "keep", "confidence": 0.5, "reason": "meh",
                           "suggested_type": None},
            }
        ],
    }
    output = write_high_confidence_review(report, tmp_path, threshold=0.90)
    payload = json.loads(output.read_text())
    assert payload["count"] == 0
    assert payload["candidates"] == []
