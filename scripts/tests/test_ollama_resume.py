import json

from vitruvius.ollama_review import load_resume_state


def test_load_resume_state_returns_empty_when_no_snapshot(tmp_path):
    state = load_resume_state(tmp_path)
    assert state["reviews"] == []
    assert state["status"] is None


def test_load_resume_state_reads_in_progress(tmp_path):
    snapshot = {
        "generated_at": "20260414T030000Z",
        "model": "gemma4:31b",
        "source": "s",
        "total_candidates": 5,
        "completed_reviews": 2,
        "status": "in_progress",
        "summary": {},
        "reviews": [
            {"candidate": {"from": "a", "type": "governs", "to": "b"}, "review": {}},
            {"candidate": {"from": "c", "type": "governs", "to": "d"}, "review": {}},
        ],
    }
    (tmp_path / "latest_relationship_review_ollama.json").write_text(
        json.dumps(snapshot), encoding="utf-8"
    )

    state = load_resume_state(tmp_path)

    assert state["status"] == "in_progress"
    assert len(state["reviews"]) == 2
    assert state["completed_count"] == 2


def test_load_resume_state_ignores_completed_snapshot(tmp_path):
    snapshot = {"status": "completed", "reviews": [{}, {}, {}]}
    (tmp_path / "latest_relationship_review_ollama.json").write_text(
        json.dumps(snapshot), encoding="utf-8"
    )
    state = load_resume_state(tmp_path)
    assert state["reviews"] == []
    assert state["status"] == "completed"
