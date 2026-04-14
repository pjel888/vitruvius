import json
from pathlib import Path
from unittest.mock import patch

from vitruvius.ollama_review_second_pass import (
    build_second_pass_prompt,
    compute_agreement_matrix,
    run_second_pass_inner,
)


def test_prompt_includes_tier_one_decision():
    candidate = {
        "from": "concept-a", "type": "governs", "to": "concept-b",
        "occurrences": 1, "sections": ["sec-1"], "examples": ["e"],
    }
    t1 = {"decision": "review_further", "confidence": 0.4, "reason": "unclear", "suggested_type": None}

    prompt_text = build_second_pass_prompt(candidate, t1, model_name="gemma4:31b")
    prompt = json.loads(prompt_text)

    assert prompt["tier_one_decision"]["decision"] == "review_further"
    assert prompt["tier_one_decision"]["model"] == "gemma4:31b"
    assert "agrees_with_tier_one" in prompt["output_schema"]


def test_agreement_matrix_shape():
    items = [
        {"tier_one": {"decision": "keep"}, "tier_two": {"decision": "keep"}},
        {"tier_one": {"decision": "keep"}, "tier_two": {"decision": "reject"}},
        {"tier_one": {"decision": "review_further"}, "tier_two": {"decision": "keep"}},
    ]
    m = compute_agreement_matrix(items)
    assert m["keep"]["keep"] == 1
    assert m["keep"]["reject"] == 1
    assert m["review_further"]["keep"] == 1


def _write_tier_one_report(tmp_path: Path, reviews: list[dict]) -> None:
    runs = tmp_path / "006_System-Manifests" / "runs"
    runs.mkdir(parents=True)
    report = {
        "generated_at": "20260414T050000Z",
        "model": "gemma4:e4b",
        "source": "test",
        "total_candidates": len(reviews),
        "completed_reviews": len(reviews),
        "status": "completed",
        "summary": {},
        "reviews": reviews,
    }
    (runs / "latest_relationship_review_ollama.json").write_text(
        json.dumps(report), encoding="utf-8"
    )


def test_run_second_pass_inner_routes_uncertain_subset(tmp_path):
    _write_tier_one_report(tmp_path, [
        # high-confidence keep — should be SKIPPED (auto-promote)
        {
            "candidate": {"from": "a", "type": "governs", "to": "b",
                          "occurrences": 1, "sections": [], "examples": []},
            "review": {"decision": "keep", "confidence": 0.95, "reason": "clear", "suggested_type": None},
        },
        # low-confidence keep — should be routed to Tier 2
        {
            "candidate": {"from": "c", "type": "requires", "to": "d",
                          "occurrences": 1, "sections": [], "examples": []},
            "review": {"decision": "keep", "confidence": 0.80, "reason": "weak", "suggested_type": None},
        },
    ])

    def fake_call(prompt, model, timeout_seconds):
        return '{"decision":"keep","confidence":0.95,"reason":"ok","suggested_type":null}'

    with patch("vitruvius.ollama_review_second_pass.call_ollama", side_effect=fake_call):
        result = run_second_pass_inner(
            repo_root=tmp_path,
            model="qwen3:30b",
            timeout_seconds=60,
        )

    # One was routed to Tier 2, and Tier-2 kept it at conf >=0.90, so
    # route_adjudication returns "auto_promote".
    assert result["total_second_pass"] == 1
    assert result["actions"]["auto_promote"] == 1

    # Merged report was written
    merged = tmp_path / "006_System-Manifests" / "runs" / "latest_relationship_review_merged.json"
    assert merged.exists()
    payload = json.loads(merged.read_text())
    assert payload["total_tier_one"] == 2
    assert payload["total_second_pass"] == 1
    assert "agreement_matrix" in payload


def test_run_second_pass_inner_handles_ollama_failure(tmp_path):
    _write_tier_one_report(tmp_path, [
        {
            "candidate": {"from": "a", "type": "governs", "to": "b",
                          "occurrences": 1, "sections": [], "examples": []},
            "review": {"decision": "review_further", "confidence": 0.5, "reason": "unclear", "suggested_type": None},
        },
    ])

    with patch("vitruvius.ollama_review_second_pass.call_ollama", side_effect=RuntimeError("ollama down")):
        result = run_second_pass_inner(
            repo_root=tmp_path,
            model="qwen3:30b",
            timeout_seconds=60,
        )

    # Failure routes to human_review (Tier-2 parse-error fallback)
    assert result["actions"]["human_review"] == 1
    assert result["actions"]["auto_promote"] == 0
