from unittest.mock import patch
import re

from vitruvius.ollama_review import review_candidates_parallel


def test_returns_results_in_order():
    candidates = [
        {"from": f"c-{i}", "type": "governs", "to": f"c-{i+1}", "sections": [], "examples": []}
        for i in range(5)
    ]

    def stub(prompt, model, timeout_seconds):
        match = re.search(r'"from": "([^"]+)"', prompt)
        assert match is not None
        from_id = match.group(1)
        return f'{{"decision":"keep","confidence":0.95,"reason":"{from_id}","suggested_type":null}}'

    with patch("vitruvius.ollama_review.call_ollama", side_effect=stub):
        results = review_candidates_parallel(
            candidates, model="gemma4:31b", timeout_seconds=60, parallelism=2
        )

    assert len(results) == 5
    assert [r["candidate"]["from"] for r in results] == [c["from"] for c in candidates]
    assert [r["review"]["reason"] for r in results] == [f"c-{i}" for i in range(5)]


def test_parallelism_one_is_sequential():
    candidates = [
        {"from": f"c-{i}", "type": "governs", "to": "x", "sections": [], "examples": []}
        for i in range(3)
    ]

    def stub(prompt, model, timeout_seconds):
        return '{"decision":"keep","confidence":0.95,"reason":"ok","suggested_type":null}'

    with patch("vitruvius.ollama_review.call_ollama", side_effect=stub):
        results = review_candidates_parallel(
            candidates, model="gemma4:31b", timeout_seconds=60, parallelism=1
        )
    assert len(results) == 3
