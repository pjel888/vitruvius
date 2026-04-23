from vitruvius.cloud_review_adjudication import (
    apply_cloud_adjudication,
    call_cloud_adjudicator,
    should_escalate_to_cloud,
)


def _item(decision="keep", confidence=0.95, occurrences=1):
    return {
        "candidate": {
            "from": "law-pd-1096",
            "type": "governs",
            "to": "concept-building-permit",
            "occurrences": occurrences,
            "sections": ["sec-302"],
            "examples": [{"snippet": "No building permit shall be issued unless..."}],
        },
        "review": {
            "decision": decision,
            "confidence": confidence,
            "reason": "local review",
            "suggested_type": None,
        },
    }


def test_cloud_escalation_selects_review_further_and_low_confidence_and_high_value():
    assert should_escalate_to_cloud(_item(decision="review_further", confidence=0.99, occurrences=1), low_confidence_threshold=0.90, high_value_occurrences_threshold=3) is True
    assert should_escalate_to_cloud(_item(decision="keep", confidence=0.50, occurrences=1), low_confidence_threshold=0.90, high_value_occurrences_threshold=3) is True
    assert should_escalate_to_cloud(_item(decision="keep", confidence=0.95, occurrences=3), low_confidence_threshold=0.90, high_value_occurrences_threshold=3) is True
    assert should_escalate_to_cloud(_item(decision="keep", confidence=0.95, occurrences=1), low_confidence_threshold=0.90, high_value_occurrences_threshold=3) is False


def test_apply_cloud_adjudication_is_noop_when_disabled():
    report = {
        "model": "llama3.1:8b",
        "summary": {"keep": 1, "review_further": 0, "reject": 0, "high_confidence_keep": 1, "high_confidence_reject": 0},
        "reviews": [_item()],
    }
    updated = apply_cloud_adjudication(report, settings={"enabled": False}, parse_model_json_fn=lambda text: text)
    assert updated is report


def test_apply_cloud_adjudication_overrides_review_and_preserves_local_review(monkeypatch):
    from vitruvius import cloud_review_adjudication as cra

    monkeypatch.setattr(cra, "call_cloud_adjudicator", lambda **_: '{"decision":"reject","confidence":0.96,"reason":"cloud","suggested_type":null}')
    report = {
        "model": "llama3.1:8b",
        "summary": {"keep": 1, "review_further": 0, "reject": 0, "high_confidence_keep": 1, "high_confidence_reject": 0},
        "reviews": [_item(decision="review_further", confidence=0.40)],
    }
    updated = apply_cloud_adjudication(
        report,
        settings={
            "enabled": True,
            "provider": "openai_compatible",
            "model": "gpt-5",
            "api_base_url": "https://example.com",
            "api_key": "secret",
            "timeout_seconds": 30,
            "prefer_adjudicated_decision": True,
            "low_confidence_threshold": 0.90,
            "high_value_occurrences_threshold": 3,
        },
        parse_model_json_fn=lambda text: __import__("json").loads(text),
    )
    item = updated["reviews"][0]
    assert item["local_review"]["decision"] == "review_further"
    assert item["review"]["decision"] == "reject"
    assert item["cloud_review"]["source"] == "cloud_adjudicator"
    assert updated["summary"]["reject"] == 1


def test_apply_cloud_adjudication_recomputes_summary_when_cloud_fails(monkeypatch):
    from vitruvius import cloud_review_adjudication as cra

    monkeypatch.setattr(cra, "call_cloud_adjudicator", lambda **_: (_ for _ in ()).throw(RuntimeError("boom")))
    report = {
        "model": "llama3.1:8b",
        "summary": {"keep": 1, "review_further": 0, "reject": 0, "high_confidence_keep": 1, "high_confidence_reject": 0},
        "reviews": [_item(decision="review_further", confidence=0.40, occurrences=4)],
    }
    updated = apply_cloud_adjudication(
        report,
        settings={
            "enabled": True,
            "provider": "openai_compatible",
            "model": "gpt-5",
            "api_base_url": "https://example.com",
            "api_key": "secret",
            "timeout_seconds": 30,
            "prefer_adjudicated_decision": True,
            "low_confidence_threshold": 0.90,
            "high_value_occurrences_threshold": 3,
        },
        parse_model_json_fn=lambda text: __import__("json").loads(text),
    )
    assert updated["summary"]["review_further"] == 1
    assert updated["summary"]["keep"] == 0


def test_call_cloud_adjudicator_routes_gemini(monkeypatch):
    from vitruvius import cloud_review_adjudication as cra

    monkeypatch.setattr(cra, "_call_gemini", lambda **_: '{"decision":"keep","confidence":0.91,"reason":"gemini","suggested_type":null}')
    result = call_cloud_adjudicator(
        prompt="hi",
        settings={"provider": "gemini", "model": "gemini-2.5-pro", "api_key": "secret", "timeout_seconds": 30},
    )
    assert '"decision":"keep"' in result
