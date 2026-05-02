import hashlib
import json
import logging
from pathlib import Path

import pytest

import pipeline_cli
from vitruvius.kg import aec_relationship_improvement as ari


def _node(node_id, label, definition="", **extra):
    data = {
        "id": node_id,
        "canonical_id": node_id,
        "record_type": "backbone_node",
        "label": label,
        "pref_label": label,
        "definition": definition,
        "aliases": [],
        "path_code": node_id.replace(":", "."),
        "level": 2,
        "parent_path_code": "ROOT",
        "review_status": "admitted",
        "release_version": "test",
    }
    data.update(extra)
    return data


def _fixture(path: Path):
    payload = {
        "records": [
            _node("N:A", "Fire pump", "Pump serving fire protection systems.", discipline=["fire"]),
            _node("N:B", "Fire sprinkler", "Sprinkler protection equipment.", discipline=["fire"]),
            _node("N:C", "Air handling unit", "HVAC air handling equipment.", discipline=["hvac"]),
        ],
        "relationships": [
            {
                "from_id": "N:A",
                "to_id": "N:B",
                "predicate": "requires",
                "governed": True,
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _hierarchy_fixture(path: Path, *, child_first: bool = False):
    parent = _node("N:P", "Parent concept", "A broader taxonomy concept.", path_code="ARC", level=2)
    child = _node(
        "N:C",
        "Child concept",
        "A narrower taxonomy concept.",
        path_code="ARC.01",
        parent_path_code="ARC",
        level=3,
    )
    records = [child, parent] if child_first else [parent, child]
    payload = {"records": records, "relationships": []}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _decision(**overrides):
    data = {
        "edge_exists": True,
        "predicate": "requires",
        "direction": "A_to_B",
        "confidence": 0.9,
        "relation_type": "requirement",
        "relation_category": "governed_dependency",
        "relation_nature": ["functional"],
        "rationale": "The fire pump is required for the sprinkler system.",
        "evidence": "Labels and definitions both describe fire protection equipment.",
        "risk_flags": [],
        "review_recommendation": "accept_candidate",
    }
    data.update(overrides)
    return json.dumps(data)


def _embedding(values):
    return [float(v) for v in values]


def _config(tmp_path: Path, input_path: Path, **overrides):
    data = {
        "input_path": input_path,
        "output_root": tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays",
        "run_id": "20260501T000000Z",
        "stable_embedding_cache_path": tmp_path
        / "005_Operational-Intelligence-Layer"
        / "embeddings"
        / "aec-mepfs-backbone"
        / "qwen3-embedding_0.6b"
        / "node-embeddings.jsonl",
        "max_nodes": 3,
        "max_pairs": 1,
        "candidate_top_k": 1,
        "min_similarity": 0.1,
        "sleep_seconds": 0.0,
        "verifier_sleep_seconds": 0.0,
        "cloud_preflight": False,
    }
    data.update(overrides)
    return ari.RunConfig(**data)


def _reset_aec_logger_for_caplog():
    for handler in list(ari.logger.handlers):
        ari.logger.removeHandler(handler)
        handler.close()
    ari.logger.propagate = True


def test_loads_aec_nodes_and_relationships_from_fixture(tmp_path):
    path = tmp_path / "backbone.json"
    _fixture(path)

    nodes, relationships = ari.load_backbone_graph(path)

    assert [node["id"] for node in nodes] == ["N:A", "N:B", "N:C"]
    assert relationships == [
        {"from_id": "N:A", "to_id": "N:B", "predicate": "requires", "governed": True}
    ]


def test_builds_deterministic_node_text_and_text_hash():
    node = ari.make_node_view(
        _node(
            "N:A",
            "Fire pump",
            "Pump serving fire protection systems.",
            aliases=["fire service pump", "FSP"],
            source_family_ids=["NFPA"],
        )
    )

    first = ari.build_node_text(node)
    second = ari.build_node_text(node)

    assert first == second
    assert "ID: N:A" in first
    assert "Aliases: fire service pump, FSP" in first
    assert ari.sha256_text(first) == hashlib.sha256(first.encode("utf-8")).hexdigest()


def test_embedding_cache_hit_skips_ollama_call(tmp_path):
    node = ari.make_node_view(_node("N:A", "Fire pump"))
    text = ari.build_node_text(node)
    cache_path = tmp_path / "node-embeddings.jsonl"
    record = ari.EmbeddingRecord(
        node_id=node.id,
        embedding_model="qwen3-embedding:0.6b",
        embedding_dimensions=3,
        text_hash=ari.sha256_text(text),
        embedding=_embedding([1, 0, 0]),
        created_at_utc="2026-05-01T00:00:00Z",
    )
    ari.save_embedding_record_jsonl(cache_path, record)

    def fail_embed(_texts):
        raise AssertionError("embedder should not be called for cache hits")

    embeddings, stats = ari.get_or_create_embeddings(
        [node],
        "qwen3-embedding:0.6b",
        stable_cache_path=cache_path,
        run_cache_path=tmp_path / "run-cache.jsonl",
        embed_texts=fail_embed,
        store_text=False,
    )

    assert embeddings[node.id] == [1.0, 0.0, 0.0]
    assert stats["cache_hits"] == 1
    assert stats["cache_misses"] == 0


def test_embedding_cache_miss_calls_embedder_and_writes_jsonl(tmp_path):
    node = ari.make_node_view(_node("N:A", "Fire pump"))
    cache_path = tmp_path / "node-embeddings.jsonl"
    calls = []

    def fake_embed(texts):
        calls.append(texts)
        return [_embedding([0, 1, 0]) for _ in texts]

    embeddings, stats = ari.get_or_create_embeddings(
        [node],
        "qwen3-embedding:0.6b",
        stable_cache_path=cache_path,
        run_cache_path=tmp_path / "run-cache.jsonl",
        embed_texts=fake_embed,
        store_text=False,
    )

    assert calls and calls[0][0].startswith("ID: N:A")
    assert embeddings[node.id] == [0.0, 1.0, 0.0]
    assert stats["cache_hits"] == 0
    assert stats["cache_misses"] == 1
    written = [json.loads(line) for line in cache_path.read_text(encoding="utf-8").splitlines()]
    assert written[0]["node_id"] == "N:A"
    assert "text" not in written[0]


def test_candidate_generation_returns_top_k_pairs_without_all_pairs():
    nodes = [
        ari.make_node_view(_node("A", "A")),
        ari.make_node_view(_node("B", "B")),
        ari.make_node_view(_node("C", "C")),
        ari.make_node_view(_node("D", "D")),
    ]
    embeddings = {
        "A": _embedding([1, 0, 0]),
        "B": _embedding([0.99, 0.01, 0]),
        "C": _embedding([0, 1, 0]),
        "D": _embedding([0, 0.99, 0.01]),
    }

    pairs = list(
        ari.generate_candidate_pairs(
            nodes,
            embeddings,
            run_id="run",
            embedding_model="qwen3-embedding:0.6b",
            candidate_top_k=1,
            min_similarity=0.1,
            max_pairs=10,
            existing_pair_index=set(),
            include_existing_pairs=False,
        )
    )

    assert {pair.node_pair_key for pair in pairs} == {"A||B", "C||D"}
    assert len(pairs) < 6


def test_duplicate_existing_edge_prevention_uses_edge_key():
    edges = [
        {"from_id": "N:A", "to_id": "N:B", "predicate": "requires"},
        {"from_id": "N:B", "to_id": "N:C", "predicate": "part_of"},
    ]

    edge_keys = ari.build_existing_edge_keys(edges)
    pair_index = ari.build_existing_pair_index(edges)

    assert "N:A--requires--N:B" in edge_keys
    assert "N:A||N:B" in pair_index
    assert "N:B||N:C" in pair_index


def test_reversed_conflicts_with_duplicate_is_rejected_when_existing_pairs_included(tmp_path):
    input_path = tmp_path / "backbone.json"
    payload = _fixture(input_path)
    payload["relationships"] = [
        {"from_id": "N:B", "to_id": "N:A", "predicate": "conflicts_with", "governed": True}
    ]
    input_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(
            predicate="conflicts_with",
            direction="undirected",
            confidence=0.9,
        ),
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    rejected = [json.loads(line) for line in (output_dir / "rejected-relationships.jsonl").read_text().splitlines()]
    assert summary.accepted_count == 0
    assert rejected[0]["reason"] == "duplicate_edge"


def test_external_ollama_base_url_is_rejected():
    ari.ensure_local_ollama_base_url("http://localhost:11434")
    ari.ensure_local_ollama_base_url("http://127.0.0.1:11434")

    with pytest.raises(ari.ExternalNetworkDisabledError):
        ari.ensure_local_ollama_base_url("https://example.com")


def test_local_only_mode_makes_no_cloud_calls_even_with_cloud_env(tmp_path, monkeypatch):
    monkeypatch.setenv("KIMI_API_KEY", "secret-kimi")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def fail_cloud(**_kwargs):
        raise AssertionError("local_only must not call cloud providers")

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fail_cloud,
        sleep=lambda _seconds: None,
    )

    assert summary.accepted_count == 1
    assert summary.cloud_usage.cloud_call_count == 0


def test_local_only_rejects_explicit_cloud_provider(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    with pytest.raises(ari.CloudAIRequiredError):
        ari.run_relationship_improvement(
            _config(
                tmp_path,
                input_path,
                allow_cloud_ai=True,
                council_mode="local_only",
                judge_provider="deepseek",
            ),
            embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
            generate_text=lambda **_kwargs: _decision(),
            sleep=lambda _seconds: None,
        )


def test_adaptive_cloud_requires_allow_cloud_ai(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    with pytest.raises(ari.CloudAIRequiredError):
        ari.run_relationship_improvement(
            _config(tmp_path, input_path, council_mode="adaptive_cloud"),
            embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
            generate_text=lambda **_kwargs: _decision(),
            sleep=lambda _seconds: None,
        )


def test_deepseek_local_mode_exists_and_requires_allow_cloud_ai(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    config = _config(tmp_path, input_path, council_mode="deepseek_local")
    assert "deepseek_local" in ari.COUNCIL_MODES

    with pytest.raises(ari.CloudAIRequiredError):
        ari.run_relationship_improvement(
            config,
            embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
            generate_text=lambda **_kwargs: _decision(),
            sleep=lambda _seconds: None,
        )


def test_adaptive_cloud_no_longer_routes_to_kimi_by_default():
    config = ari.RunConfig(allow_cloud_ai=True, council_mode="adaptive_cloud")
    ari.validate_council_config(config)
    council = ari.RelationshipCouncil(config, generate_text=lambda **_kwargs: _decision())

    for role in ("judge", "verifier", "adjudicator"):
        assert all(provider != "kimi" for provider, _model in council._provider_priority(role))


def test_kimi_preflight_does_not_run_in_deepseek_local(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    monkeypatch.setenv("KIMI_API_KEY", "secret-kimi")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    models = []

    def fake_post(**kwargs):
        models.append(kwargs["payload"]["model"])
        assert kwargs["payload"]["model"] != "kimi-for-coding"
        return {"choices": [{"message": {"content": '{"ok": true}'}, "finish_reason": "stop"}], "usage": {}}

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            cloud_preflight=True,
            max_nodes=0,
            max_pairs=1,
        ),
        embed_texts=lambda texts: [],
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    assert summary.cloud_usage.deepseek_flash_call_count == 1
    assert models == ["deepseek-v4-flash"]


def test_deepseek_preflight_failure_falls_back_to_local(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_post(**kwargs):
        calls.append(kwargs)
        raise ari.CloudProviderError("deepseek", "disabled_auth_error", "bad key", retryable=False)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            cloud_preflight=True,
            include_existing_pairs=True,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    assert len(calls) == 1
    assert summary.accepted_count == 1
    assert summary.cloud_usage.local_fallback_call_count == 1


def test_audit_only_reads_prior_artifacts_without_generating_candidates(tmp_path, monkeypatch):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    run_id = "20260501T000000Z"
    output_root = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays"
    output_dir = output_root / run_id
    output_dir.mkdir(parents=True)
    prior_record = {
        "schema_version": "aec-relationship-improvement-candidate/v1",
        "run_id": run_id,
        "node_pair_key": "N:A||N:C",
        "node_a_id": "N:A",
        "node_b_id": "N:C",
        "similarity": 0.81,
        "judge_decision": json.loads(_decision(predicate="requires", direction="A_to_B")),
    }
    (output_dir / "accepted-relationships.jsonl").write_text(json.dumps(prior_record) + "\n", encoding="utf-8")
    def fail_embed(_texts):
        raise AssertionError("audit_only must not generate embeddings or similarity candidates")

    def fake_verifier(**_kwargs):
        return json.dumps(
            {
                "agrees": True,
                "corrected_edge_exists": True,
                "corrected_predicate": "requires",
                "corrected_direction": "A_to_B",
                "corrected_confidence": 0.91,
                "rationale": "Prior candidate remains supported.",
            }
        )

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            output_root=output_root,
            run_id=run_id,
            council_mode="audit_only",
            allow_cloud_ai=True,
            max_pairs=1,
        ),
        embed_texts=fail_embed,
        generate_text=lambda **_kwargs: _decision(),
        verifier_text=fake_verifier,
        sleep=lambda _seconds: None,
    )

    audit_lines = (output_dir / "relationship-council-audit.jsonl").read_text(encoding="utf-8").splitlines()
    similarity_lines = (output_dir / "similarity-candidates.jsonl").read_text(encoding="utf-8").splitlines()
    assert summary.processed_count == 1
    assert len(audit_lines) == 1
    assert json.loads(audit_lines[0])["verification_decision"]["agrees"] is True
    assert similarity_lines == []


def test_kimi_provider_requires_configured_api_key(monkeypatch):
    monkeypatch.delenv("KIMI_API_KEY", raising=False)

    with pytest.raises(ari.CloudProviderError) as excinfo:
        ari.call_kimi_chat_completion(
            config=ari.RunConfig(allow_cloud_ai=True),
            prompt="Return JSON only.",
            schema=ari.RelationshipDecision.model_json_schema(),
            post_json=lambda **_kwargs: {},
        )

    assert excinfo.value.reason == "disabled_auth_error"


def test_deepseek_provider_requires_configured_api_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    with pytest.raises(ari.CloudProviderError) as excinfo:
        ari.call_deepseek_chat_completion(
            config=ari.RunConfig(allow_cloud_ai=True),
            prompt="Return JSON only.",
            schema=ari.RelationshipDecision.model_json_schema(),
            model="deepseek-v4-flash",
            post_json=lambda **_kwargs: {},
        )

    assert excinfo.value.reason == "disabled_auth_error"


def test_kimi_code_request_shape_and_defaults():
    payload = ari.build_kimi_chat_payload(
        config=ari.RunConfig(),
        prompt="Return JSON only.",
        schema=ari.RelationshipDecision.model_json_schema(),
    )

    assert payload["model"] == "kimi-for-coding"
    assert payload["response_format"] == {"type": "json_object"}
    assert payload["thinking"] == {"type": "disabled"}
    assert payload["max_completion_tokens"] == 700
    assert "temperature" not in payload
    assert "top_p" not in payload


def test_kimi_invalid_max_completion_tokens_retries_with_max_tokens(monkeypatch):
    monkeypatch.setenv("KIMI_API_KEY", "secret-kimi")
    calls = []

    def fake_post(**kwargs):
        calls.append(kwargs["payload"])
        if len(calls) == 1:
            raise ari.CloudProviderError("kimi", "invalid_parameter", "bad parameter")
        return {
            "choices": [{"message": {"content": _decision(predicate="has_facet")}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7},
        }

    response = ari.call_kimi_chat_completion(
        config=ari.RunConfig(allow_cloud_ai=True),
        prompt="Return JSON only.",
        schema=ari.RelationshipDecision.model_json_schema(),
        post_json=fake_post,
    )

    assert "max_completion_tokens" in calls[0]
    assert "max_tokens" in calls[1]
    assert response.metadata["token_parameter"] == "max_tokens"


def test_deepseek_request_shape_and_defaults():
    payload = ari.build_deepseek_chat_payload(
        config=ari.RunConfig(),
        prompt="Return JSON only.",
        schema=ari.RelationshipDecision.model_json_schema(),
        model="deepseek-v4-flash",
    )

    assert payload["model"] == "deepseek-v4-flash"
    assert payload["response_format"] == {"type": "json_object"}
    assert payload["thinking"] == {"type": "disabled"}
    assert payload["max_tokens"] == 700
    assert payload["stream"] is False
    assert "JSON" in payload["messages"][0]["content"] or "JSON" in payload["messages"][1]["content"]
    assert '"edge_exists": true' in payload["messages"][1]["content"].lower()
    assert "num_ctx" not in json.dumps(payload)
    assert "num_predict" not in json.dumps(payload)
    assert "max_completion_tokens" not in payload


def test_deepseek_finish_reason_length_is_rejected():
    with pytest.raises(ari.CloudResponseRejectedError) as excinfo:
        ari.extract_chat_content(
            {"choices": [{"message": {"content": "{}"}, "finish_reason": "length"}]},
            "deepseek",
            "deepseek-v4-flash",
        )

    assert excinfo.value.reason == "deepseek_json_truncated"


def test_deepseek_empty_content_is_rejected():
    with pytest.raises(ari.CloudResponseRejectedError) as excinfo:
        ari.extract_chat_content(
            {"choices": [{"message": {"content": ""}, "finish_reason": "stop"}]},
            "deepseek",
            "deepseek-v4-flash",
        )

    assert excinfo.value.reason == "empty_deepseek_response"


def test_malformed_cloud_json_is_rejected_safely(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {"choices": [{"message": {"content": "not json"}, "finish_reason": "stop"}], "usage": {}}

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    rejected = [json.loads(line) for line in (output_dir / "rejected-relationships.jsonl").read_text().splitlines()]
    assert rejected[0]["reason"] == "malformed_json"


def test_deepseek_429_retries_then_falls_back_to_local(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    monkeypatch.delenv("KIMI_API_KEY", raising=False)
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_post(**_kwargs):
        calls.append(_kwargs)
        raise ari.CloudProviderError("deepseek", "disabled_rate_limit", "rate limited")

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            cloud_max_retries=1,
            cloud_backoff_seconds=0,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    assert len(calls) == 2
    assert summary.accepted_count == 1
    assert summary.cloud_usage.cloud_call_count == 2
    assert summary.cloud_usage.deepseek_flash_call_count == 2
    assert summary.cloud_usage.local_fallback_call_count == 1


def test_failed_deepseek_attempts_are_bounded_by_flash_cap(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_post(**_kwargs):
        calls.append(_kwargs)
        raise ari.CloudProviderError("deepseek", "disabled_rate_limit", "rate limited")

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            cloud_max_retries=2,
            cloud_backoff_seconds=0,
            deepseek_flash_max_calls=1,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    assert len(calls) == 1
    assert summary.accepted_count == 1
    assert summary.cloud_usage.cloud_call_count == 1
    assert summary.cloud_usage.deepseek_flash_call_count == 1
    assert summary.cloud_usage.local_fallback_call_count == 1


def test_failed_deepseek_preflight_attempts_are_bounded_by_flash_cap(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_post(**_kwargs):
        calls.append(_kwargs)
        raise ari.CloudProviderError("deepseek", "disabled_rate_limit", "rate limited")

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            cloud_preflight=True,
            cloud_max_retries=2,
            cloud_backoff_seconds=0,
            deepseek_flash_max_calls=1,
            max_nodes=0,
            max_pairs=0,
        ),
        embed_texts=lambda texts: [],
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    assert len(calls) == 1
    assert summary.cloud_usage.cloud_call_count == 1
    assert summary.cloud_usage.deepseek_flash_call_count == 1


def test_failed_deepseek_pro_attempts_use_configured_pro_cap(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    calls = []
    usage = ari.CloudUsage()

    def fake_post(**_kwargs):
        calls.append(_kwargs)
        raise ari.CloudProviderError("deepseek", "disabled_rate_limit", "rate limited")

    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="deepseek_local",
        adjudicator_provider="auto",
        deepseek_pro_model="deepseek-reasoner",
        deepseek_pro_max_calls=1,
        cloud_max_retries=2,
        cloud_backoff_seconds=0,
    )
    council = ari.RelationshipCouncil(
        config,
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        usage=usage,
        sleep=lambda _seconds: None,
    )

    envelope = council.adjudicate("Return JSON only.", ari.RelationshipDecision.model_json_schema())

    assert len(calls) == 1
    assert envelope.provider == "ollama"
    assert usage.cloud_call_count == 1
    assert usage.deepseek_pro_call_count == 1
    assert usage.deepseek_pro_adjudicator_call_count == 1
    assert usage.deepseek_flash_call_count == 0


def test_cloud_total_max_calls_zero_degrades_to_local(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            cloud_total_max_calls=0,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=lambda **_kwargs: (_ for _ in ()).throw(AssertionError("cloud cap should skip call")),
        sleep=lambda _seconds: None,
    )

    assert summary.accepted_count == 1
    assert summary.cloud_usage.cloud_call_count == 0
    assert summary.cloud_usage.local_fallback_call_count == 1


def test_accepted_record_includes_council_metadata(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {
            "choices": [{"message": {"content": _decision(direction="B_to_A", predicate="has_facet")}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 10,
                "prompt_cache_hit_tokens": 4,
                "prompt_cache_miss_tokens": 6,
                "completion_tokens": 5,
                "total_tokens": 15,
            },
        }

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    accepted_path = Path(summary.output_dir) / "accepted-relationships.jsonl"
    accepted = [json.loads(line) for line in accepted_path.read_text().splitlines()]
    assert accepted[0]["council_mode"] == "adaptive_cloud"
    assert accepted[0]["judge_provider"] == "deepseek"
    assert accepted[0]["judge_model"] == "deepseek-v4-flash"
    assert accepted[0]["generation_method"] == "adaptive_deepseek_local_relationship_improvement_v1"
    assert accepted[0]["provider_route"][0]["status"] == "success"
    assert summary.cloud_usage.deepseek_flash_call_count == 1


def test_deepseek_local_generation_method_and_metadata(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {
            "choices": [{"message": {"content": _decision(direction="B_to_A", predicate="has_facet")}, "finish_reason": "stop"}],
            "usage": {},
        }

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    accepted = _accepted_records(summary)
    assert accepted[0]["council_mode"] == "deepseek_local"
    assert accepted[0]["judge_provider"] == "deepseek"
    assert accepted[0]["judge_model"] == "deepseek-v4-flash"
    assert accepted[0]["generation_method"] == "deepseek_local_relationship_improvement_v1"


def test_reasoning_content_and_api_keys_are_not_stored(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {
            "choices": [
                {
                    "message": {
                        "content": _decision(direction="B_to_A", predicate="has_facet"),
                        "reasoning_content": "hidden reasoning",
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {},
        }

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    artifact_text = "\n".join(path.read_text(errors="ignore") for path in Path(summary.output_dir).iterdir() if path.is_file())
    assert "hidden reasoning" not in artifact_text
    assert "secret-deepseek" not in artifact_text


def test_auth_error_disables_cloud_provider_and_falls_back(tmp_path, monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("KIMI_API_KEY", raising=False)
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        sleep=lambda _seconds: None,
    )

    checkpoint = json.loads((Path(summary.output_dir) / "relationship-improvement-checkpoint.json").read_text())
    assert summary.accepted_count == 1
    assert summary.cloud_usage.local_fallback_call_count == 1
    assert checkpoint["provider_health"]["states"]["deepseek"] == "disabled_auth_error"


def test_provider_health_state_is_saved_in_checkpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    monkeypatch.delenv("KIMI_API_KEY", raising=False)
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            cloud_max_retries=0,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=lambda **_kwargs: (_ for _ in ()).throw(
            ari.CloudProviderError("deepseek", "disabled_rate_limit", "rate limited")
        ),
        sleep=lambda _seconds: None,
    )

    checkpoint = json.loads((Path(summary.output_dir) / "relationship-improvement-checkpoint.json").read_text())
    assert checkpoint["provider_health"]["states"]["deepseek"] in {"degraded", "disabled_rate_limit"}
    assert checkpoint["cloud_usage"]["local_fallback_call_count"] == 1


def test_provider_health_tracks_deepseek_flash_and_local_roles(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            cloud_total_max_calls=0,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=lambda **_kwargs: (_ for _ in ()).throw(AssertionError("cloud cap should skip call")),
        sleep=lambda _seconds: None,
    )

    checkpoint = json.loads((Path(summary.output_dir) / "relationship-improvement-checkpoint.json").read_text())
    assert checkpoint["provider_health"]["states"]["deepseek"] == "disabled_budget"
    assert "ollama_judge" in checkpoint["provider_health"]["last_latencies"]


def test_resume_loads_provider_usage_counters(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {
            "choices": [{"message": {"content": _decision(direction="B_to_A", predicate="has_facet")}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 10,
                "prompt_cache_hit_tokens": 4,
                "prompt_cache_miss_tokens": 6,
                "completion_tokens": 5,
                "total_tokens": 15,
            },
        }

    first = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="resume-cloud",
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )
    resumed = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="resume-cloud",
            resume=True,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        cloud_post_json=lambda **_kwargs: (_ for _ in ()).throw(AssertionError("resume should skip processed pair")),
        sleep=lambda _seconds: None,
    )

    assert first.cloud_usage.cloud_call_count == 1
    assert resumed.cloud_usage.cloud_call_count == 1
    assert resumed.skipped_count == 1


def test_provider_call_caps_are_enforced_without_network_calls(monkeypatch):
    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="adaptive_cloud",
        kimi_max_calls=1,
        deepseek_flash_max_calls=1,
        deepseek_pro_max_calls=1,
        cloud_total_max_calls=2,
    )
    usage = ari.CloudUsage(cloud_total_max_calls=2, kimi_max_calls=1)
    usage.kimi_call_count = 1
    usage.deepseek_flash_call_count = 1
    usage.deepseek_pro_call_count = 1
    usage.cloud_call_count = 2
    council = ari.RelationshipCouncil(config, generate_text=lambda **_kwargs: _decision(), usage=usage)

    assert council._provider_allowed("kimi", "kimi-for-coding")[0] is False
    assert council._provider_allowed("deepseek", "deepseek-v4-flash")[0] is False
    assert council._provider_allowed("deepseek", "deepseek-v4-pro")[0] is False


def test_deepseek_flash_max_calls_default_uses_buffer():
    config = ari.RunConfig(allow_cloud_ai=True, council_mode="deepseek_local", max_pairs=100)

    assert ari.effective_deepseek_flash_max_calls(config) == 150


def test_deepseek_flash_cap_warning_when_explicit_cap_is_too_tight(caplog, monkeypatch):
    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="deepseek_local",
        max_pairs=100,
        deepseek_flash_max_calls=100,
    )

    monkeypatch.setattr(ari.logger, "propagate", True)
    caplog.set_level(logging.WARNING, logger=ari.logger.name)
    ari.validate_council_config(config)

    assert "deepseek-flash-max-calls is <= max-pairs" in caplog.text


def test_deepseek_cap_exhaustion_triggers_local_fallback():
    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="deepseek_local",
        deepseek_flash_max_calls=1,
        cloud_preflight=False,
    )
    usage = ari.CloudUsage()
    usage.deepseek_flash_call_count = 1
    council = ari.RelationshipCouncil(config, generate_text=lambda **_kwargs: _decision(), usage=usage)

    envelope = council.judge("Return JSON only.", ari.RelationshipDecision.model_json_schema())

    assert envelope.provider == "ollama"
    assert envelope.local_fallback_used is True
    assert envelope.provider_failover_reason == "deepseek_flash_max_calls_exhausted"


def test_cloud_cost_budget_is_enforced_without_network_calls():
    config = ari.RunConfig(allow_cloud_ai=True, council_mode="adaptive_cloud", cloud_cost_budget_usd=0.01)
    usage = ari.CloudUsage(cloud_cost_budget_usd=0.01, cloud_estimated_cost_usd=0.01)
    council = ari.RelationshipCouncil(config, generate_text=lambda **_kwargs: _decision(), usage=usage)

    allowed, reason = council._provider_allowed("deepseek", "deepseek-v4-flash")

    assert allowed is False
    assert reason == "cloud_cost_budget_exhausted"


def test_kimi_provider_selection_is_disabled_without_experimental_flag():
    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="adaptive_cloud",
        judge_provider="kimi",
    )

    with pytest.raises(ari.CloudProviderError, match="Kimi Code chat completion is disabled"):
        ari.validate_council_config(config)


def test_kimi_can_only_route_when_experimental_flag_is_enabled(monkeypatch):
    monkeypatch.setenv("KIMI_API_KEY", "secret-kimi")
    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="adaptive_cloud",
        judge_provider="kimi",
        enable_kimi_experimental=True,
        kimi_estimated_cost_per_call_usd=0.01,
    )
    ari.validate_council_config(config)
    council = ari.RelationshipCouncil(
        config,
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=lambda **_kwargs: {
            "choices": [{"message": {"content": _decision(direction="B_to_A", predicate="has_facet")}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        },
        sleep=lambda _seconds: None,
    )

    envelope = council.judge("Return JSON only.", ari.RelationshipDecision.model_json_schema())

    assert envelope.provider == "kimi"
    assert council.usage.cloud_estimated_cost_usd == pytest.approx(0.01)


def test_high_impact_edges_trigger_deepseek_pro_adjudication(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    models_seen = []

    def fake_post(**kwargs):
        model = kwargs["payload"]["model"]
        models_seen.append(model)
        content = _decision(direction="B_to_A", predicate="requires", confidence=0.9)
        return {"choices": [{"message": {"content": content}, "finish_reason": "stop"}], "usage": {}}

    def fake_verifier(**_kwargs):
        return json.dumps(
            {
                "agrees": True,
                "corrected_edge_exists": True,
                "corrected_predicate": "requires",
                "corrected_direction": "B_to_A",
                "corrected_confidence": 0.91,
                "rationale": "Verified.",
            }
        )

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="adaptive_cloud",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
            high_impact_pro_adjudication=True,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        verifier_text=fake_verifier,
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    assert summary.accepted_count == 1
    assert "deepseek-v4-pro" in models_seen
    accepted = _accepted_records(summary)
    assert accepted[0]["adjudicator_provider"] == "deepseek"
    assert accepted[0]["adjudicator_model"] == "deepseek-v4-pro"


def test_dry_run_pending_only_does_not_modify_input_fixture(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    before = input_path.read_bytes()

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def fake_generate(**_kwargs):
        return _decision(direction="B_to_A")

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=fake_generate,
        sleep=lambda _seconds: None,
    )

    assert input_path.read_bytes() == before
    assert summary.accepted_count == 1


def test_resume_skips_processed_node_pair_key(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    output_root = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays"
    output_dir = output_root / "20260501T000000Z"
    output_dir.mkdir(parents=True)
    ari.save_checkpoint(
        output_dir / "relationship-improvement-checkpoint.json",
        ari.Checkpoint(
            run_id="20260501T000000Z",
            status="in_progress",
            input_path=str(input_path),
            output_dir=str(output_dir),
            embedding_model="qwen3-embedding:0.6b",
            judge_model="qwen3.5:9b",
            verifier_model="deepseek-r1:8b-0528-qwen3-q4_K_M",
            processed_pair_keys=["N:A||N:B"],
            accepted_edge_keys=[],
        ),
    )

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def fail_generate(**_kwargs):
        raise AssertionError("processed pair should be skipped on resume")

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, resume=True, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=fail_generate,
        sleep=lambda _seconds: None,
    )

    assert summary.skipped_count == 1
    assert summary.processed_count == 0


def test_global_ledger_second_run_with_same_manual_ledger_skips_prior_judged_pair(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    judge_calls = []
    shared_ledger_path = tmp_path / "shared-ledger.jsonl"

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def first_generate(**_kwargs):
        judge_calls.append("first")
        return _decision(
            edge_exists=False,
            predicate="none",
            direction="none",
            confidence=0.1,
            relation_type="none",
            relation_category="none",
            relation_nature=[],
            rationale="No clear governed relationship is supported.",
            evidence="none",
            review_recommendation="reject",
        )

    first = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-first",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
        ),
        embed_texts=fake_embed,
        generate_text=first_generate,
        sleep=lambda _seconds: None,
    )

    ledger_records = [json.loads(line) for line in shared_ledger_path.read_text(encoding="utf-8").splitlines()]
    assert first.processed_count == 1
    assert judge_calls == ["first"]
    assert ledger_records[0]["schema_version"] == "aec-relationship-discovery-ledger/v1"
    assert ledger_records[0]["node_pair_key"] == "N:A||N:B"
    assert ledger_records[0]["decision_status"] == "rejected"
    assert ledger_records[0]["embedding_model"] == "qwen3-embedding:0.6b"
    assert ledger_records[0]["accept_threshold"] == 0.85
    assert ledger_records[0]["verify_threshold"] == 0.65
    assert ledger_records[0]["candidate_top_k"] == 1
    assert ledger_records[0]["node_a_text_hash"]
    assert ledger_records[0]["node_b_text_hash"]

    def fail_generate(**_kwargs):
        raise AssertionError("global ledger should skip before judge call")

    second = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-second",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
        ),
        embed_texts=fake_embed,
        generate_text=fail_generate,
        sleep=lambda _seconds: None,
    )

    second_output = Path(second.output_dir)
    checkpoint = json.loads((second_output / "relationship-improvement-checkpoint.json").read_text())
    report = json.loads((second_output / "relationship-improvement-report.json").read_text())
    summary_text = (second_output / "relationship-improvement-summary.txt").read_text(encoding="utf-8")

    assert second.processed_count == 0
    assert second.skipped_count == 1
    assert second.skipped_global_ledger_count == 1
    assert checkpoint["skipped_global_ledger_count"] == 1
    assert report["skipped_global_ledger_count"] == 1
    assert report["quality_summary"]["skipped_global_ledger_count"] == 1
    assert "Skipped by global ledger: 1" in summary_text
    assert "New model calls: 0" in summary_text


def test_auto_global_ledger_path_is_campaign_specific_per_run_id(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def reject_generate(**_kwargs):
        calls.append("judge")
        return _decision(
            edge_exists=False,
            predicate="none",
            direction="none",
            confidence=0.1,
            relation_type="none",
            relation_category="none",
            relation_nature=[],
            rationale="No clear governed relationship is supported.",
            evidence="none",
            review_recommendation="reject",
        )

    first = ari.run_relationship_improvement(
        _config(tmp_path, input_path, run_id="campaign-one", include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )
    second = ari.run_relationship_improvement(
        _config(tmp_path, input_path, run_id="campaign-two", include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )

    first_ledger = Path(first.output_dir).parent / "campaign-one-ledger.jsonl"
    second_ledger = Path(second.output_dir).parent / "campaign-two-ledger.jsonl"
    assert first_ledger.exists()
    assert second_ledger.exists()
    assert first_ledger != second_ledger
    assert calls == ["judge", "judge"]
    assert second.processed_count == 1
    assert second.skipped_global_ledger_count == 0


def test_global_ledger_threshold_mismatch_warns_and_prevents_reuse(tmp_path, capsys):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    shared_ledger_path = tmp_path / "shared-threshold-ledger.jsonl"
    calls = []

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def reject_generate(**_kwargs):
        calls.append("judge")
        return _decision(
            edge_exists=False,
            predicate="none",
            direction="none",
            confidence=0.1,
            relation_type="none",
            relation_category="none",
            relation_nature=[],
            rationale="No clear governed relationship is supported.",
            evidence="none",
            review_recommendation="reject",
        )

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="threshold-first",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            accept_threshold=0.85,
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )

    second = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="threshold-second",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            accept_threshold=0.9,
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )
    captured = capsys.readouterr()

    assert calls == ["judge", "judge"]
    assert second.skipped_global_ledger_count == 0
    assert second.global_ledger_existing_pair_count == 1
    assert second.global_ledger_thresholds_match is False
    assert "thresholds differ" in captured.err


def test_force_ledger_reuse_allows_threshold_mismatch_skip(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    shared_ledger_path = tmp_path / "shared-forced-ledger.jsonl"

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def reject_generate(**_kwargs):
        return _decision(
            edge_exists=False,
            predicate="none",
            direction="none",
            confidence=0.1,
            relation_type="none",
            relation_category="none",
            relation_nature=[],
            rationale="No clear governed relationship is supported.",
            evidence="none",
            review_recommendation="reject",
        )

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="force-first",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            accept_threshold=0.85,
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )

    def fail_generate(**_kwargs):
        raise AssertionError("forced ledger reuse should skip before judge call")

    second = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="force-second",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            accept_threshold=0.9,
            force_ledger_reuse=True,
        ),
        embed_texts=fake_embed,
        generate_text=fail_generate,
        sleep=lambda _seconds: None,
    )

    assert second.processed_count == 0
    assert second.skipped_global_ledger_count == 1
    assert second.global_ledger_thresholds_match is False


def test_ignore_global_ledger_allows_rejudging_prior_pair(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []
    shared_ledger_path = tmp_path / "ignore-shared-ledger.jsonl"

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    reject_decision = lambda **_kwargs: _decision(
        edge_exists=False,
        predicate="none",
        direction="none",
        confidence=0.1,
        relation_type="none",
        relation_category="none",
        relation_nature=[],
        rationale="No clear governed relationship is supported.",
        evidence="none",
        review_recommendation="reject",
    )

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-ignore-first",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
        ),
        embed_texts=fake_embed,
        generate_text=reject_decision,
        sleep=lambda _seconds: None,
    )

    def counted_generate(**kwargs):
        calls.append(kwargs)
        return reject_decision(**kwargs)

    second = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-ignore-second",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            ignore_global_ledger=True,
        ),
        embed_texts=fake_embed,
        generate_text=counted_generate,
        sleep=lambda _seconds: None,
    )

    assert len(calls) == 1
    assert second.processed_count == 1
    assert second.skipped_global_ledger_count == 0


def test_global_ledger_decision_filter_controls_skips(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []
    shared_ledger_path = tmp_path / "filter-shared-ledger.jsonl"

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def reject_generate(**_kwargs):
        calls.append("judge")
        return _decision(
            edge_exists=False,
            predicate="none",
            direction="none",
            confidence=0.1,
            relation_type="none",
            relation_category="none",
            relation_nature=[],
            rationale="No clear governed relationship is supported.",
            evidence="none",
            review_recommendation="reject",
        )

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-filter-first",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )
    second = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-filter-second",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            global_ledger_decision_filter=("accepted", "candidate"),
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )

    assert calls == ["judge", "judge"]
    assert second.processed_count == 1
    assert second.skipped_global_ledger_count == 0


def test_global_ledger_requires_matching_embedding_model_and_node_text_hash(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []
    shared_ledger_path = tmp_path / "model-shared-ledger.jsonl"

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def reject_generate(**_kwargs):
        calls.append("judge")
        return _decision(
            edge_exists=False,
            predicate="none",
            direction="none",
            confidence=0.1,
            relation_type="none",
            relation_category="none",
            relation_nature=[],
            rationale="No clear governed relationship is supported.",
            evidence="none",
            review_recommendation="reject",
        )

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-model-first",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )
    second = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="ledger-model-second",
            include_existing_pairs=True,
            global_ledger_path=shared_ledger_path,
            embedding_model="different-embedding-model",
            stable_embedding_cache_path=tmp_path / "different-embedding-cache.jsonl",
        ),
        embed_texts=fake_embed,
        generate_text=reject_generate,
        sleep=lambda _seconds: None,
    )

    assert calls == ["judge", "judge"]
    assert second.processed_count == 1
    assert second.skipped_global_ledger_count == 0


def test_bad_llm_json_is_rejected_safely(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: "not json",
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    rejected = [json.loads(line) for line in (output_dir / "rejected-relationships.jsonl").read_text().splitlines()]
    assert summary.rejected_count == 1
    assert rejected[0]["reason"] == "malformed_json"


def test_blocked_predicate_is_rejected_safely(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(predicate="related_to"),
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    rejected = [json.loads(line) for line in (output_dir / "rejected-relationships.jsonl").read_text().splitlines()]
    assert rejected[0]["reason"] == "blocked_predicate"


def test_confidence_threshold_accepts_only_threshold_or_higher(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    low = ari.run_relationship_improvement(
        _config(tmp_path, input_path, run_id="low", include_existing_pairs=True, ignore_global_ledger=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(confidence=0.84, direction="B_to_A"),
        sleep=lambda _seconds: None,
    )
    high = ari.run_relationship_improvement(
        _config(tmp_path, input_path, run_id="high", include_existing_pairs=True, ignore_global_ledger=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(confidence=0.85, direction="B_to_A"),
        sleep=lambda _seconds: None,
    )

    assert low.accepted_count == 0
    assert high.accepted_count == 1


def _run_hierarchy_case(tmp_path, *, decision_json, run_id="hierarchy", child_first=False, **config_overrides):
    input_path = tmp_path / f"{run_id}.json"
    _hierarchy_fixture(input_path, child_first=child_first)
    return ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id=run_id,
            max_nodes=2,
            max_pairs=1,
            include_existing_pairs=True,
            **config_overrides,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: decision_json,
        sleep=lambda _seconds: None,
    )


def _accepted_records(summary):
    path = Path(summary.output_dir) / "accepted-relationships.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _candidate_records(summary):
    path = Path(summary.output_dir) / "candidate-relationships.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _rejected_records(summary):
    path = Path(summary.output_dir) / "rejected-relationships.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _validation_error_records(summary):
    path = Path(summary.output_dir) / "validation-errors.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_parent_broader_than_child_is_accepted(tmp_path):
    summary = _run_hierarchy_case(
        tmp_path,
        decision_json=_decision(predicate="broader_than", direction="A_to_B"),
    )

    accepted = _accepted_records(summary)
    assert summary.accepted_count == 1
    assert accepted[0]["from_id"] == "N:P"
    assert accepted[0]["to_id"] == "N:C"
    assert accepted[0]["predicate"] == "broader_than"
    assert accepted[0]["normalization_applied"] is False


def test_parent_narrower_than_child_is_normalized_to_parent_broader_than_child(tmp_path):
    summary = _run_hierarchy_case(
        tmp_path,
        run_id="normalize-parent",
        decision_json=_decision(predicate="narrower_than", direction="A_to_B"),
    )

    accepted = _accepted_records(summary)
    assert accepted[0]["edge_key"] == "N:P--broader_than--N:C"
    assert accepted[0]["normalization_applied"] is True
    assert accepted[0]["original_model_predicate"] == "narrower_than"
    assert accepted[0]["normalized_predicate"] == "broader_than"


def test_child_narrower_than_parent_is_normalized_to_parent_broader_than_child(tmp_path):
    summary = _run_hierarchy_case(
        tmp_path,
        run_id="normalize-child",
        child_first=True,
        decision_json=_decision(predicate="narrower_than", direction="A_to_B"),
    )

    accepted = _accepted_records(summary)
    assert accepted[0]["edge_key"] == "N:P--broader_than--N:C"
    assert accepted[0]["normalized_direction"] == "B_to_A"


def test_path_code_part_of_is_converted_to_hierarchy_when_enabled(tmp_path):
    summary = _run_hierarchy_case(
        tmp_path,
        run_id="part-of-convert",
        decision_json=_decision(predicate="part_of", direction="A_to_B"),
    )

    accepted = _accepted_records(summary)
    assert summary.accepted_count == 1
    assert accepted[0]["edge_key"] == "N:P--broader_than--N:C"
    assert accepted[0]["normalization_reason"] == "taxonomy_part_of_converted_to_hierarchy"
    assert summary.taxonomy_part_of_conversion_count == 1


def test_path_code_part_of_is_downgraded_when_conversion_disabled(tmp_path):
    summary = _run_hierarchy_case(
        tmp_path,
        run_id="part-of-downgrade",
        decision_json=_decision(predicate="part_of", direction="A_to_B"),
        convert_taxonomy_part_of=False,
    )

    candidates = _candidate_records(summary)
    assert summary.accepted_count == 0
    assert summary.candidate_review_count == 1
    assert candidates[0]["reason"] == "taxonomy_part_of_needs_review"
    assert candidates[0]["normalization_reason"] == "taxonomy_part_of_path_code_only_downgraded"


def test_verifier_is_only_called_for_uncertain_band_when_enabled(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    verifier_calls = []

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    def fake_verifier(**_kwargs):
        verifier_calls.append(_kwargs)
        return json.dumps(
            {
                "agrees": True,
                "corrected_edge_exists": True,
                "corrected_predicate": "requires",
                "corrected_direction": "B_to_A",
                "corrected_confidence": 0.9,
                "rationale": "Verified.",
            }
        )

    ari.run_relationship_improvement(
        _config(tmp_path, input_path, run_id="noverify", include_existing_pairs=True, ignore_global_ledger=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(confidence=0.7, direction="B_to_A"),
        verifier_text=fake_verifier,
        sleep=lambda _seconds: None,
    )
    assert verifier_calls == []

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="verify",
            verify_uncertain=True,
            include_existing_pairs=True,
            ignore_global_ledger=True,
        ),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(confidence=0.7, direction="B_to_A"),
        verifier_text=fake_verifier,
        sleep=lambda _seconds: None,
    )

    assert len(verifier_calls) == 1
    assert summary.accepted_count == 1


def test_verifier_output_parses_as_verification_decision_not_relationship_decision():
    raw = json.dumps(
        {
            "agrees": True,
            "corrected_edge_exists": True,
            "corrected_predicate": "requires",
            "corrected_direction": "A_to_B",
            "corrected_confidence": 0.87,
            "rationale": "Verifier agrees with the judge.",
        }
    )

    decision = ari.parse_verification_decision(raw)

    assert decision.agrees is True
    with pytest.raises(ari.MalformedModelJSONError):
        ari.parse_relationship_decision("not json")
    with pytest.raises(ari.RoleValidationError) as excinfo:
        ari.parse_verification_decision_for_role(_decision(), "verifier")
    assert excinfo.value.reason == "verifier_validation_error"


def test_accepted_relationship_record_has_candidate_provenance(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    node_a = ari.make_node_view(_node("N:A", "Fire pump"))
    node_b = ari.make_node_view(_node("N:B", "Fire sprinkler"))
    pair = ari.CandidatePair(
        run_id="run",
        node_pair_key="N:A||N:B",
        node_a_id="N:A",
        node_b_id="N:B",
        similarity=0.73,
        embedding_model="qwen3-embedding:0.6b",
        created_at_utc="2026-05-01T00:00:00Z",
    )
    decision = ari.parse_relationship_decision(_decision())

    record = ari.decision_to_edge_record(
        run_id="run",
        node_a=node_a,
        node_b=node_b,
        pair=pair,
        decision=decision,
        embedding_model="qwen3-embedding:0.6b",
        judge_model="qwen3.5:9b",
        verifier_model=None,
        verifier_decision=None,
        created_at_utc="2026-05-01T00:00:00Z",
    )

    assert record["generation_method"] == "local_ollama_relationship_improvement_v1"
    assert record["review_status"] == "candidate"
    assert record["governed"] is True


def test_output_files_are_written_under_semantic_overlays_run_id(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_embed(texts):
        return [_embedding([1, 0, 0]) for _ in texts]

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True),
        embed_texts=fake_embed,
        generate_text=lambda **_kwargs: _decision(),
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    assert output_dir.name == "20260501T000000Z"
    assert output_dir.parent.name == "semantic-overlays"
    for filename in [
        "relationship-improvement.log",
        "relationship-improvement-report.json",
        "relationship-improvement-checkpoint.json",
        "candidate-relationships.jsonl",
        "accepted-relationships.jsonl",
        "rejected-relationships.jsonl",
        "errors.jsonl",
        "node-embeddings.jsonl",
        "similarity-candidates.jsonl",
    ]:
        assert (output_dir / filename).exists()


def test_progress_mode_off_still_runs_existing_workflow(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True, progress_mode="off"),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A"),
        sleep=lambda _seconds: None,
    )

    assert summary.accepted_count == 1


def test_progress_mode_plain_prints_periodic_summaries(tmp_path, capsys):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            include_existing_pairs=True,
            progress_mode="plain",
            progress_log_every_seconds=0,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A"),
        sleep=lambda _seconds: None,
    )

    captured = capsys.readouterr()
    assert "[AEC-REL]" in captured.err
    assert captured.out == ""


def test_progress_mode_auto_falls_back_to_plain_when_rich_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(ari, "rich_is_available", lambda: False)
    config = _config(tmp_path, tmp_path / "missing.json", progress_mode="auto")

    reporter = ari.create_progress_reporter(config)

    assert isinstance(reporter, ari.PlainProgressReporter)


def test_progress_mode_rich_errors_clearly_when_rich_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(ari, "rich_is_available", lambda: False)
    config = _config(tmp_path, tmp_path / "missing.json", progress_mode="rich")

    with pytest.raises(RuntimeError, match="Rich progress UI requested"):
        ari.create_progress_reporter(config)


def test_checkpoint_includes_phase_and_progress_counters(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True, progress_mode="off"),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A"),
        sleep=lambda _seconds: None,
    )

    checkpoint = json.loads((Path(summary.output_dir) / "relationship-improvement-checkpoint.json").read_text())
    assert checkpoint["phase"] == "completed"
    assert checkpoint["nodes_selected"] == 3
    assert checkpoint["embedding_total"] == 3
    assert checkpoint["embedding_processed"] == 3
    assert checkpoint["candidate_pairs_generated"] == 1
    assert checkpoint["processed_pair_count"] == 1


def test_checkpoint_is_updated_after_each_processed_pair(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True, progress_mode="off"),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A"),
        sleep=lambda _seconds: None,
    )

    checkpoint = json.loads((Path(summary.output_dir) / "relationship-improvement-checkpoint.json").read_text())
    assert checkpoint["processed_pair_keys"] == ["N:A||N:B"]
    assert checkpoint["processed_pair_count"] == 1


def test_recent_events_are_bounded():
    checkpoint = ari.Checkpoint(
        run_id="run",
        status="in_progress",
        input_path="in",
        output_dir="out",
        embedding_model="embed",
        judge_model="judge",
        verifier_model="verify",
        recent_events=[{"i": index} for index in range(80)],
    )

    record = checkpoint.to_record()

    assert len(record["recent_events"]) == ari.MAX_RECENT_EVENTS
    assert record["recent_events"][0]["i"] == 30


def test_relationship_improvement_events_jsonl_is_written_and_sanitized(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True, progress_mode="off"),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A"),
        sleep=lambda _seconds: None,
    )

    events_path = Path(summary.output_dir) / "relationship-improvement-events.jsonl"
    text = events_path.read_text(encoding="utf-8")
    assert "aec-relationship-improvement-event/v1" in text
    assert "api_key" not in text.lower()
    assert "reasoning_content" not in text


def test_keyboard_interrupt_updates_checkpoint_to_interrupted(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def interrupt_generate(**_kwargs):
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        ari.run_relationship_improvement(
            _config(tmp_path, input_path, include_existing_pairs=True, progress_mode="off"),
            embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
            generate_text=interrupt_generate,
            sleep=lambda _seconds: None,
        )

    checkpoint = json.loads(
        (
            tmp_path
            / "006_System-Manifests"
            / "aec-mepfs-backbone"
            / "semantic-overlays"
            / "20260501T000000Z"
            / "relationship-improvement-checkpoint.json"
        ).read_text()
    )
    assert checkpoint["status"] == "interrupted"
    assert checkpoint["phase"] == "interrupted"


def test_watcher_reads_temp_run_directory_with_checkpoint_and_jsonl(tmp_path):
    output_dir = tmp_path / "run"
    output_dir.mkdir()
    ari.save_checkpoint(
        output_dir / "relationship-improvement-checkpoint.json",
        ari.Checkpoint(
            run_id="run",
            status="in_progress",
            input_path="input",
            output_dir=str(output_dir),
            embedding_model="embed",
            judge_model="judge",
            verifier_model="verify",
            processed_pair_count=2,
        ),
    )
    ari.append_jsonl(output_dir / "accepted-relationships.jsonl", {"edge_key": "A--requires--B"})

    snapshot = ari.load_watch_snapshot(output_dir)

    assert snapshot.run_id == "run"
    assert snapshot.status == "in_progress"
    assert snapshot.accepted_count == 1


def test_watcher_tolerates_missing_files(tmp_path):
    output_dir = tmp_path / "empty-run"
    output_dir.mkdir()

    snapshot = ari.load_watch_snapshot(output_dir)

    assert snapshot.run_id == "empty-run"
    assert snapshot.accepted_count == 0
    assert snapshot.status == "unknown"


def test_watcher_tolerates_partial_jsonl_trailing_line(tmp_path):
    output_dir = tmp_path / "run"
    output_dir.mkdir()
    (output_dir / "accepted-relationships.jsonl").write_text('{"edge_key": "ok"}\n{"edge_key": ', encoding="utf-8")

    snapshot = ari.load_watch_snapshot(output_dir)

    assert snapshot.accepted_count == 1
    assert snapshot.corrupt_jsonl_count == 0


def test_watcher_counts_non_trailing_corrupt_jsonl_line(tmp_path):
    output_dir = tmp_path / "run"
    output_dir.mkdir()
    (output_dir / "accepted-relationships.jsonl").write_text(
        '{"edge_key": "ok"}\n{"edge_key": \n{"edge_key": "ok2"}\n',
        encoding="utf-8",
    )

    snapshot = ari.load_watch_snapshot(output_dir)

    assert snapshot.accepted_count == 2
    assert snapshot.corrupt_jsonl_count == 1


def test_watcher_watch_latest_picks_newest_run_directory(tmp_path):
    old = tmp_path / "20260501T000000Z"
    new = tmp_path / "20260501T010000Z"
    old.mkdir()
    new.mkdir()

    resolved = ari.resolve_watch_output_dir(ari.WatchRunConfig(output_root=tmp_path, watch_latest=True), tmp_path)

    assert resolved == new


def test_watcher_exit_when_complete_exits(tmp_path):
    output_dir = tmp_path / "run"
    output_dir.mkdir()
    ari.save_checkpoint(
        output_dir / "relationship-improvement-checkpoint.json",
        ari.Checkpoint(
            run_id="run",
            status="completed",
            input_path="input",
            output_dir=str(output_dir),
            embedding_model="embed",
            judge_model="judge",
            verifier_model="verify",
        ),
    )

    result = ari.watch_relationship_run(
        ari.WatchRunConfig(output_dir=output_dir, progress_mode="plain", exit_when_complete=True),
        sleep=lambda _seconds: None,
    )

    assert result == 0


def test_watcher_does_not_treat_writing_report_checkpoint_as_complete(tmp_path):
    output_dir = tmp_path / "run"
    output_dir.mkdir()
    ari.save_checkpoint(
        output_dir / "relationship-improvement-checkpoint.json",
        ari.Checkpoint(
            run_id="run",
            status="completed",
            phase="writing_report",
            input_path="input",
            output_dir=str(output_dir),
            embedding_model="embed",
            judge_model="judge",
            verifier_model="verify",
        ),
    )

    snapshot = ari.load_watch_snapshot(output_dir)

    assert ari.watch_snapshot_is_complete(snapshot) is False


def test_rich_progress_reporter_instantiates_when_rich_available():
    if not ari.rich_is_available():
        pytest.skip("rich is not installed")

    reporter = ari.RichProgressReporter()
    reporter.close()


def test_progress_events_sanitize_api_keys_and_reasoning_content(tmp_path):
    output_dir = tmp_path / "run"
    files = {"events": output_dir / "relationship-improvement-events.jsonl"}
    checkpoint = ari.Checkpoint(
        run_id="run",
        status="in_progress",
        input_path="input",
        output_dir=str(output_dir),
        embedding_model="embed",
        judge_model="judge",
        verifier_model="verify",
    )
    reporter = ari.NullProgressReporter()

    ari.append_progress_event(
        files,
        checkpoint,
        reporter,
        ari.build_progress_event(
            run_id="run",
            phase="judging",
            event_type="error",
            message="sanitized event",
            counts={"api_key": "secret", "reasoning_content": "hidden"},
        ),
    )

    text = files["events"].read_text(encoding="utf-8")
    assert "secret" not in text
    assert "reasoning_content" not in text


def test_apply_raises_safety_error():
    with pytest.raises(ari.ApplyModeDeferredError):
        ari.ensure_apply_mode_is_deferred(True)


def test_pipeline_cli_accepts_final_relationship_improvement_flags():
    parser = pipeline_cli.build_parser()
    args = parser.parse_args(
        [
            "aec-improve-relationships",
            "--dry-run",
            "--council-mode",
            "deepseek_local",
            "--allow-cloud-ai",
            "--hierarchy-canonical-predicate",
            "broader_than",
            "--convert-taxonomy-part-of",
            "--progress-mode",
            "plain",
            "--cloud-preflight",
            "--deepseek-flash-call-buffer",
            "0.5",
            "--enable-safe-schema-repair",
            "--schema-repair-acceptance-policy",
            "needs_review_only",
            "--deepseek-retry-truncated-json",
            "--force-rich-in-git-bash",
            "--use-global-ledger",
            "--global-ledger-path",
            "006_System-Manifests/aec-mepfs-backbone/semantic-overlays/global-relationship-discovery-ledger.jsonl",
            "--global-ledger-decision-filter",
            "accepted,candidate,rejected,validation_error",
            "--force-ledger-reuse",
        ]
    )

    assert args.council_mode == "deepseek_local"
    assert args.hierarchy_canonical_predicate == "broader_than"
    assert args.convert_taxonomy_part_of is True
    assert args.progress_mode == "plain"
    assert args.cloud_preflight is True
    assert args.deepseek_flash_call_buffer == 0.5
    assert args.enable_safe_schema_repair is True
    assert args.deepseek_retry_truncated_json is True
    assert args.force_rich_in_git_bash is True
    assert args.use_global_ledger is True
    assert args.global_ledger_decision_filter == "accepted,candidate,rejected,validation_error"
    assert args.force_ledger_reuse is True


def test_pipeline_cli_accepts_run_persistence_and_final_ux_flags():
    parser = pipeline_cli.build_parser()
    args = parser.parse_args(
        [
            "aec-improve-relationships",
            "--council-mode",
            "deepseek_local",
            "--max-nodes",
            "0",
            "--max-pairs",
            "0",
            "--progress-mode",
            "plain",
            "--progress-refresh-per-second",
            "1.5",
            "--progress-log-every-seconds",
            "10",
            "--progress-show-recent",
            "6",
            "--progress-transient",
            "--no-progress",
            "--force-rich-in-git-bash",
            "--no-cloud-preflight",
            "--hierarchy-canonical-predicate",
            "broader_than",
            "--no-convert-taxonomy-part-of",
            "--no-enable-safe-schema-repair",
            "--schema-repair-acceptance-policy",
            "needs_review_only",
            "--no-deepseek-retry-truncated-json",
            "--enable-kimi-experimental",
            "--deepseek-flash-call-buffer",
            "0.25",
            "--ignore-global-ledger",
            "--no-use-global-ledger",
            "--global-ledger-decision-filter",
            "accepted,candidate",
            "--force-ledger-reuse",
            "--atomic-write-retries",
            "7",
            "--atomic-write-backoff-seconds",
            "0.01",
            "--atomic-write-max-backoff-seconds",
            "0.5",
            "--no-jsonl-fsync",
        ]
    )

    assert args.council_mode == "deepseek_local"
    assert args.max_nodes == 0
    assert args.max_pairs == 0
    assert args.progress_mode == "off"
    assert args.progress_refresh_per_second == 1.5
    assert args.progress_log_every_seconds == 10
    assert args.progress_show_recent == 6
    assert args.progress_transient is True
    assert args.force_rich_in_git_bash is True
    assert args.cloud_preflight is False
    assert args.hierarchy_canonical_predicate == "broader_than"
    assert args.convert_taxonomy_part_of is False
    assert args.enable_safe_schema_repair is False
    assert args.deepseek_retry_truncated_json is False
    assert args.enable_kimi_experimental is True
    assert args.deepseek_flash_call_buffer == 0.25
    assert args.ignore_global_ledger is True
    assert args.use_global_ledger is False
    assert args.global_ledger_decision_filter == "accepted,candidate"
    assert args.force_ledger_reuse is True
    assert args.atomic_write_retries == 7
    assert args.atomic_write_backoff_seconds == 0.01
    assert args.atomic_write_max_backoff_seconds == 0.5
    assert args.jsonl_fsync is False


def test_run_directory_bootstrap_exists_before_preflight(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    seen = []

    def fake_preflight(config, _council):
        seen.append("preflight")
        output_dir = config.output_root / config.run_id
        assert output_dir.exists()
        assert (output_dir / "run-started.json").exists()
        assert (output_dir / "relationship-improvement-checkpoint.json").exists()
        events = (output_dir / "relationship-improvement-events.jsonl").read_text(encoding="utf-8").splitlines()
        assert json.loads(events[0])["event_type"] == "run_started"
        return False

    monkeypatch.setattr(ari, "run_deepseek_preflight", fake_preflight)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="bootstrap-before-preflight",
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            max_nodes=0,
            max_pairs=0,
            cloud_preflight=True,
            progress_mode="off",
        ),
        embed_texts=lambda _texts: (_ for _ in ()).throw(AssertionError("no embeddings expected")),
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    assert seen == ["preflight"]
    assert output_dir.exists()
    assert (output_dir / "errors.jsonl").exists()


def test_no_model_zero_pair_run_creates_output_dir_without_cloud_opt_in(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="zero-pair-run",
            council_mode="deepseek_local",
            max_nodes=0,
            max_pairs=0,
            cloud_preflight=True,
            progress_mode="off",
        ),
        embed_texts=lambda _texts: (_ for _ in ()).throw(AssertionError("no embeddings expected")),
        generate_text=lambda **_kwargs: (_ for _ in ()).throw(AssertionError("no model calls expected")),
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    assert output_dir.exists()
    assert (output_dir / "run-started.json").exists()
    checkpoint = json.loads((output_dir / "relationship-improvement-checkpoint.json").read_text())
    assert checkpoint["status"] == "completed"
    assert checkpoint["processed_pair_count"] == 0


def test_output_path_is_printed_after_run_directory_ready(tmp_path, capsys):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="printed-path-order",
            max_nodes=0,
            max_pairs=0,
            progress_mode="plain",
        ),
        embed_texts=lambda _texts: [],
        sleep=lambda _seconds: None,
    )

    captured = capsys.readouterr()
    ready_index = captured.err.index("run_dir_ready=")
    run_index = captured.err.index("run=printed-path-order")
    assert ready_index < run_index
    printed_dir = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays" / "printed-path-order"
    assert printed_dir.exists()


def test_embedding_exception_leaves_fatal_artifacts_and_error_checkpoint(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    with pytest.raises(ari.RunFatalError):
        ari.run_relationship_improvement(
            _config(tmp_path, input_path, run_id="embedding-fatal", include_existing_pairs=True, progress_mode="off"),
            embed_texts=lambda _texts: (_ for _ in ()).throw(RuntimeError("embedding exploded")),
            sleep=lambda _seconds: None,
        )

    output_dir = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays" / "embedding-fatal"
    assert output_dir.exists()
    assert (output_dir / "run-started.json").exists()
    assert (output_dir / "fatal-error.json").exists()
    checkpoint = json.loads((output_dir / "relationship-improvement-checkpoint.json").read_text())
    assert checkpoint["status"] == "error"
    assert checkpoint["phase"] == "error"


def test_judging_exception_leaves_fatal_artifacts_and_error_checkpoint(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    with pytest.raises(ari.RunFatalError):
        ari.run_relationship_improvement(
            _config(tmp_path, input_path, run_id="judging-fatal", include_existing_pairs=True, progress_mode="off"),
            embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
            generate_text=lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("judge exploded")),
            sleep=lambda _seconds: None,
        )

    output_dir = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays" / "judging-fatal"
    checkpoint = json.loads((output_dir / "relationship-improvement-checkpoint.json").read_text())
    assert output_dir.exists()
    assert checkpoint["status"] == "error"
    assert (output_dir / "fatal-error.json").exists()


def test_resume_missing_run_id_fails_clearly_without_creating_directory(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    config = _config(
        tmp_path,
        input_path,
        run_id="missing-resume",
        resume=True,
        max_nodes=0,
        max_pairs=0,
        progress_mode="off",
    )

    with pytest.raises(ari.MissingRunDirectoryError, match="Cannot resume run missing-resume"):
        ari.run_relationship_improvement(config, embed_texts=lambda _texts: [])

    assert not (config.output_root / "missing-resume").exists()


def test_watcher_missing_run_prints_available_runs(tmp_path, capsys):
    (tmp_path / "20260501T000000Z").mkdir()
    (tmp_path / "20260501T010000Z").mkdir()

    result = ari.watch_relationship_run(
        ari.WatchRunConfig(output_root=tmp_path, run_id="missing", progress_mode="plain"),
        sleep=lambda _seconds: None,
        max_iterations=1,
    )

    captured = capsys.readouterr()
    assert result == 2
    assert "Run directory does not exist:" in captured.err
    assert "Available runs:" in captured.err
    assert "20260501T010000Z" in captured.err


def test_write_json_atomic_uses_unique_tmp_file_and_replace(tmp_path, monkeypatch):
    calls = []
    real_replace = ari.os.replace

    def fake_replace(src, dst):
        calls.append((Path(src), Path(dst)))
        real_replace(src, dst)

    monkeypatch.setattr(ari.os, "replace", fake_replace)
    target = tmp_path / "payload.json"

    ari.write_json_atomic(target, {"ok": True})

    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}
    assert calls
    assert calls[0][0].name.startswith("payload.json.")
    assert calls[0][0].name.endswith(".tmp")
    assert calls[0][0].name != "payload.json.tmp"
    assert calls[0][1] == target


def test_write_json_atomic_retries_permission_error_then_succeeds(tmp_path, monkeypatch, caplog):
    _reset_aec_logger_for_caplog()
    target = tmp_path / "payload.json"
    real_replace = ari.os.replace
    attempts = []
    sleeps = []

    def fake_replace(src, dst):
        attempts.append((Path(src), Path(dst)))
        if len(attempts) < 3:
            raise PermissionError("[WinError 5] Access is denied")
        return real_replace(src, dst)

    monkeypatch.setattr(ari.os, "replace", fake_replace)
    monkeypatch.setattr(ari.time, "sleep", lambda seconds: sleeps.append(seconds))
    caplog.set_level(logging.WARNING, logger=ari.logger.name)

    ari.write_json_atomic(
        target,
        {"ok": True},
        options=ari.AtomicWriteOptions(retries=4, backoff_seconds=0.01, max_backoff_seconds=0.05),
    )

    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}
    assert len(attempts) == 3
    assert sleeps == [0.01, 0.02]
    assert "Atomic JSON replace failed" in caplog.text
    assert "WinError 5" in caplog.text


def test_save_checkpoint_writes_fallback_after_repeated_permission_error(tmp_path, monkeypatch, caplog):
    _reset_aec_logger_for_caplog()
    checkpoint_path = tmp_path / "relationship-improvement-checkpoint.json"
    checkpoint = ari.Checkpoint(
        run_id="fallback-run",
        status="embedding",
        input_path="input.json",
        output_dir=str(tmp_path),
        embedding_model="qwen3-embedding:0.6b",
        judge_model="qwen3.5:9b",
        verifier_model="deepseek-r1:8b-0528-qwen3-q4_K_M",
        atomic_write_retries=2,
        atomic_write_backoff_seconds=0.01,
        atomic_write_max_backoff_seconds=0.01,
    )
    real_replace = ari.os.replace

    def fake_replace(src, dst):
        if Path(dst) == checkpoint_path:
            raise PermissionError("[WinError 5] Access is denied")
        return real_replace(src, dst)

    monkeypatch.setattr(ari.os, "replace", fake_replace)
    monkeypatch.setattr(ari.time, "sleep", lambda _seconds: None)
    caplog.set_level(logging.WARNING, logger=ari.logger.name)

    fallback_path = ari.save_checkpoint(checkpoint_path, checkpoint)

    fallback_dir = tmp_path / "checkpoint-fallbacks"
    fallbacks = sorted(fallback_dir.glob("relationship-improvement-checkpoint.*.json"))
    assert fallback_path in fallbacks
    assert json.loads(fallback_path.read_text(encoding="utf-8"))["run_id"] == "fallback-run"
    assert "fallback checkpoint written" in caplog.text


def test_workflow_continues_when_main_checkpoint_replace_fails_but_fallback_succeeds(tmp_path, monkeypatch):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    real_replace = ari.os.replace

    def fake_replace(src, dst):
        if Path(dst).name == "relationship-improvement-checkpoint.json":
            raise PermissionError("[WinError 5] Access is denied")
        return real_replace(src, dst)

    monkeypatch.setattr(ari.os, "replace", fake_replace)
    monkeypatch.setattr(ari.time, "sleep", lambda _seconds: None)

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            run_id="checkpoint-fallback-run",
            max_nodes=0,
            max_pairs=0,
            progress_mode="off",
            atomic_write_retries=1,
        ),
        embed_texts=lambda _texts: [],
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    assert summary.status == "completed"
    assert output_dir.exists()
    assert list((output_dir / "checkpoint-fallbacks").glob("relationship-improvement-checkpoint.*.json"))


def test_save_checkpoint_raises_when_main_and_fallback_writes_fail(tmp_path, monkeypatch):
    checkpoint_path = tmp_path / "relationship-improvement-checkpoint.json"
    checkpoint = ari.Checkpoint(
        run_id="fallback-fail",
        status="embedding",
        input_path="input.json",
        output_dir=str(tmp_path),
        embedding_model="qwen3-embedding:0.6b",
        judge_model="qwen3.5:9b",
        verifier_model="deepseek-r1:8b-0528-qwen3-q4_K_M",
        atomic_write_retries=1,
    )

    def fail_replace(_src, _dst):
        raise PermissionError("[WinError 5] Access is denied")

    monkeypatch.setattr(ari.os, "replace", fail_replace)
    monkeypatch.setattr(ari.time, "sleep", lambda _seconds: None)

    with pytest.raises(ari.CheckpointWriteError):
        ari.save_checkpoint(checkpoint_path, checkpoint)


def test_resume_loads_latest_fallback_checkpoint_when_main_missing(tmp_path, capsys):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    output_root = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays"
    output_dir = output_root / "resume-fallback"
    output_dir.mkdir(parents=True)
    fallback_dir = output_dir / "checkpoint-fallbacks"
    fallback_dir.mkdir()
    fallback_checkpoint = ari.Checkpoint(
        run_id="resume-fallback",
        status="in_progress",
        input_path=str(input_path),
        output_dir=str(output_dir),
        embedding_model="qwen3-embedding:0.6b",
        judge_model="qwen3.5:9b",
        verifier_model="deepseek-r1:8b-0528-qwen3-q4_K_M",
        processed_pair_keys=["N:A||N:B"],
        accepted_edge_keys=[],
    )
    ari.write_json_atomic(
        fallback_dir / "relationship-improvement-checkpoint.20260502T000000Z.000001.json",
        fallback_checkpoint.to_record(),
    )

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, run_id="resume-fallback", resume=True, include_existing_pairs=True, progress_mode="off"),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: (_ for _ in ()).throw(AssertionError("fallback checkpoint pair should skip")),
        sleep=lambda _seconds: None,
    )

    captured = capsys.readouterr()
    assert "Loaded fallback checkpoint:" in captured.err
    assert summary.skipped_count == 1


def test_no_fixed_checkpoint_tmp_path_remains():
    source = Path(ari.__file__).read_text(encoding="utf-8")

    assert "relationship-improvement-checkpoint.json.tmp" not in source
    assert 'f"{path.name}.tmp"' not in source


def test_jsonl_fsync_failure_warns_and_continues(tmp_path, monkeypatch, caplog):
    _reset_aec_logger_for_caplog()
    target = tmp_path / "events.jsonl"

    def fail_fsync(_fd):
        raise OSError("fsync denied")

    monkeypatch.setattr(ari.os, "fsync", fail_fsync)
    caplog.set_level(logging.WARNING, logger=ari.logger.name)

    ari.append_jsonl(target, {"ok": True})

    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}
    assert "JSONL fsync failed" in caplog.text


def test_fatal_error_artifacts_are_sanitized(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-secret-value")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    with pytest.raises(ari.RunFatalError):
        ari.run_relationship_improvement(
            _config(tmp_path, input_path, run_id="sanitized-fatal", include_existing_pairs=True, progress_mode="off"),
            embed_texts=lambda _texts: (_ for _ in ()).throw(
                RuntimeError("Bearer sk-test-secret-value reasoning_content hidden")
            ),
            sleep=lambda _seconds: None,
        )

    output_dir = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone" / "semantic-overlays" / "sanitized-fatal"
    artifact_text = "\n".join(path.read_text(errors="ignore") for path in output_dir.iterdir() if path.is_file())
    assert "sk-test-secret-value" not in artifact_text
    assert "Bearer sk-test-secret-value" not in artifact_text
    assert "reasoning_content" not in artifact_text


def test_relationship_workflow_contains_no_output_dir_rmtree_cleanup():
    source = Path(ari.__file__).read_text(encoding="utf-8")

    assert "rmtree" not in source
    assert "Remove-Item" not in source


def test_deepseek_local_checkpoint_distinguishes_local_and_effective_models(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {
            "choices": [{"message": {"content": _decision(direction="B_to_A", predicate="has_facet")}, "finish_reason": "stop"}],
            "usage": {},
        }

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    checkpoint = json.loads((Path(summary.output_dir) / "relationship-improvement-checkpoint.json").read_text())
    report = json.loads((Path(summary.output_dir) / "relationship-improvement-report.json").read_text())
    accepted = _accepted_records(summary)[0]
    assert checkpoint["local_judge_model"] == "qwen3.5:9b"
    assert checkpoint["effective_judge_model"] == "deepseek-v4-flash"
    assert report["provider_summary"]["effective_judge_model"] == "deepseek-v4-flash"
    assert accepted["generation_method"] == "deepseek_local_relationship_improvement_v1"
    assert accepted["judge_provider"] == "deepseek"
    assert accepted["judge_model"] == "deepseek-v4-flash"


def test_validation_errors_jsonl_is_written_for_judge_validation_error(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-secret-value")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    invalid = json.dumps(
        {
            "edge_exists": True,
            "predicate": "requires",
            "direction": "A_to_B",
            "confidence": "not-a-number",
            "relation_type": "requirement",
            "relation_category": "requirement",
            "relation_nature": ["functional"],
            "rationale": "A requires B.",
            "evidence": "Provided node records.",
            "risk_flags": [],
            "review_recommendation": "accept_candidate",
            "authorization": "Bearer sk-test-secret-value",
            "reasoning_content": "hidden",
        }
    )

    def fake_post(**_kwargs):
        return {"choices": [{"message": {"content": invalid}, "finish_reason": "stop"}], "usage": {}}

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    records = _validation_error_records(summary)
    rejected = _rejected_records(summary)
    report = json.loads((Path(summary.output_dir) / "relationship-improvement-report.json").read_text())
    artifact_text = "\n".join(path.read_text(errors="ignore") for path in Path(summary.output_dir).iterdir() if path.is_file())
    assert records[0]["role"] == "judge"
    assert records[0]["provider"] == "deepseek"
    assert records[0]["model"] == "deepseek-v4-flash"
    assert "confidence" in records[0]["failed_fields"]
    assert records[0]["raw_response_sha256"]
    assert rejected[0]["reason"] == "judge_validation_error"
    assert "confidence" in rejected[0]["failed_fields"]
    assert report["validation_errors_by_role"]["judge"] == 1
    assert "sk-test-secret-value" not in artifact_text
    assert "reasoning_content" not in artifact_text


def test_validation_errors_jsonl_is_written_for_adjudicator_validation_error(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_post(**kwargs):
        model = kwargs["payload"]["model"]
        calls.append(model)
        if model == "deepseek-v4-pro":
            return {
                "choices": [{"message": {"content": json.dumps({"agrees": True})}, "finish_reason": "stop"}],
                "usage": {},
            }
        return {
            "choices": [{"message": {"content": _decision(direction="B_to_A", predicate="requires")}, "finish_reason": "stop"}],
            "usage": {},
        }

    def fake_verifier(**_kwargs):
        return json.dumps(
            {
                "agrees": False,
                "corrected_edge_exists": True,
                "corrected_predicate": "requires",
                "corrected_direction": "B_to_A",
                "corrected_confidence": 0.86,
                "rationale": "Verifier disagrees enough to adjudicate.",
            }
        )

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_uncertain=True,
            verify_accepted_cloud=False,
            adjudicate_disagreements=True,
            high_impact_pro_adjudication=True,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(),
        verifier_text=fake_verifier,
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    records = _validation_error_records(summary)
    assert "deepseek-v4-pro" in calls
    assert records[0]["role"] == "adjudicator"
    assert records[0]["reason"] == "adjudicator_validation_error"


def test_safe_schema_repair_normalizes_harmless_shapes_without_fabricating_evidence():
    raw = {
        "edge_exists": True,
        "predicate": "Broader_Than",
        "direction": "a_to_b",
        "confidence": "0.87",
        "relation_category": "",
        "relation_nature": "hierarchical",
        "rationale": "Node A is broader.",
        "evidence": "Node A path_code=ARC; Node B path_code=ARC.01.",
        "review_recommendation": "accept_candidate",
    }

    normalized, steps = ari.normalize_relationship_decision_payload(raw, "judge")

    assert normalized["predicate"] == "broader_than"
    assert normalized["direction"] == "A_to_B"
    assert normalized["confidence"] == 0.87
    assert normalized["relation_nature"] == ["hierarchical"]
    assert normalized["risk_flags"] == []
    assert normalized["relation_type"] == "taxonomy_hierarchy"
    assert normalized["relation_category"] == "taxonomy"
    assert normalized["review_recommendation"] == "needs_review"
    assert "relation_nature_string_to_list" in steps
    assert "evidence" in normalized and normalized["evidence"]


def test_safe_schema_repair_does_not_map_ambiguous_from_to_direction():
    raw = {
        "edge_exists": True,
        "predicate": "requires",
        "direction": "from_to",
        "confidence": 0.9,
        "relation_type": "requirement",
        "relation_category": "requirement",
        "relation_nature": [],
        "rationale": "A requires B.",
        "evidence": "Node text supports a requirement.",
        "risk_flags": [],
        "review_recommendation": "accept_candidate",
    }
    normalized, steps = ari.normalize_relationship_decision_payload(raw, "judge")

    assert normalized["direction"] == "from_to"
    assert "direction_literal_normalized" not in steps
    with pytest.raises(ari.RoleValidationError):
        ari.parse_relationship_decision_for_role(json.dumps(raw), "judge", config=ari.RunConfig())


def test_safe_schema_repair_does_not_invent_missing_evidence():
    raw = {
        "edge_exists": True,
        "predicate": "requires",
        "direction": "A_to_B",
        "confidence": 0.9,
        "relation_type": "requirement",
        "relation_category": "requirement",
        "relation_nature": [],
        "rationale": "A requires B.",
        "risk_flags": [],
        "review_recommendation": "accept_candidate",
    }
    normalized, _steps = ari.normalize_relationship_decision_payload(raw, "judge")

    assert "evidence" not in normalized
    with pytest.raises(ari.RoleValidationError):
        ari.parse_relationship_decision_for_role(json.dumps(raw), "judge", config=ari.RunConfig())


def test_deepseek_prompts_separate_judge_verifier_and_adjudicator_schemas():
    node_a = ari.make_node_view(_node("A", "Parent", path_code="ARC"))
    node_b = ari.make_node_view(_node("B", "Child", path_code="ARC.01"))
    schema = ari.RelationshipDecision.model_json_schema()
    verifier_schema = ari.VerificationDecision.model_json_schema()
    judge_prompt = ari.build_judge_prompt(
        node_a=node_a,
        node_b=node_b,
        existing_direct_relationships=[],
        similarity=0.9,
        schema=schema,
    )
    verifier_prompt = ari.build_verifier_prompt(
        node_a=node_a,
        node_b=node_b,
        judge_decision=ari.parse_relationship_decision(_decision()),
        schema=verifier_schema,
    )
    adjudicator_prompt = ari.build_adjudicator_prompt(
        node_a=node_a,
        node_b=node_b,
        judge_decision=ari.parse_relationship_decision(_decision()),
        verifier_decision=None,
        schema=schema,
    )
    deepseek_messages = ari.build_cloud_messages(judge_prompt, schema, "deepseek")
    payload = ari.build_deepseek_chat_payload(config=ari.RunConfig(), prompt=judge_prompt, schema=schema, model="deepseek-v4-flash")

    combined = json.dumps(deepseek_messages)
    for key in ("edge_exists", "predicate", "direction", "confidence", "relation_nature", "risk_flags", "review_recommendation"):
        assert key in combined
    assert "JSON" in combined
    assert "VerificationDecision" in verifier_prompt
    assert "full RelationshipDecision" in adjudicator_prompt
    assert payload["response_format"] == {"type": "json_object"}
    assert "max_tokens" in payload
    assert "num_ctx" not in json.dumps(payload)
    assert "num_predict" not in json.dumps(payload)


def test_deepseek_truncated_json_retries_once_when_enabled(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    calls = []

    def fake_post(**kwargs):
        calls.append(kwargs["payload"]["max_tokens"])
        if len(calls) == 1:
            return {"choices": [{"message": {"content": "{"}, "finish_reason": "length"}], "usage": {}}
        return {"choices": [{"message": {"content": _decision()}, "finish_reason": "stop"}], "usage": {}}

    config = ari.RunConfig(
        allow_cloud_ai=True,
        council_mode="deepseek_local",
        cloud_max_retries=1,
        cloud_backoff_seconds=0,
        deepseek_sleep_seconds=0,
    )
    council = ari.RelationshipCouncil(
        config,
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    envelope = council.judge("Return JSON only.", ari.RelationshipDecision.model_json_schema())

    assert envelope.provider == "deepseek"
    assert calls == [700, 1050]
    assert council.usage.cloud_call_count == 2


def test_truncated_retry_diagnostic_can_be_written_to_validation_errors(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)
    calls = []

    def fake_post(**kwargs):
        calls.append(kwargs["payload"]["max_tokens"])
        if len(calls) == 1:
            return {"choices": [{"message": {"content": "{"}, "finish_reason": "length"}], "usage": {}}
        return {"choices": [{"message": {"content": _decision(direction="B_to_A", predicate="has_facet")}, "finish_reason": "stop"}], "usage": {}}

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            cloud_max_retries=1,
            cloud_backoff_seconds=0,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    records = _validation_error_records(summary)
    assert calls == [700, 1050]
    assert summary.accepted_count == 1
    assert records[0]["reason"] == "deepseek_json_truncated"
    assert records[0]["final_action"] == "retried"


def test_deepseek_empty_content_becomes_validation_artifact(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek")
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    def fake_post(**_kwargs):
        return {"choices": [{"message": {"content": ""}, "finish_reason": "stop"}], "usage": {}}

    summary = ari.run_relationship_improvement(
        _config(
            tmp_path,
            input_path,
            council_mode="deepseek_local",
            allow_cloud_ai=True,
            include_existing_pairs=True,
            verify_accepted_cloud=False,
        ),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(),
        cloud_post_json=fake_post,
        sleep=lambda _seconds: None,
    )

    records = _validation_error_records(summary)
    rejected = _rejected_records(summary)
    assert records[0]["reason"] == "empty_deepseek_response"
    assert records[0]["error_type"] == "empty_content"
    assert rejected[0]["reason"] == "empty_deepseek_response"


def test_report_summary_and_review_tsvs_are_written(tmp_path):
    input_path = tmp_path / "backbone.json"
    _fixture(input_path)

    summary = ari.run_relationship_improvement(
        _config(tmp_path, input_path, include_existing_pairs=True, progress_mode="off"),
        embed_texts=lambda texts: [_embedding([1, 0, 0]) for _ in texts],
        generate_text=lambda **_kwargs: _decision(direction="B_to_A", predicate="has_facet"),
        sleep=lambda _seconds: None,
    )

    output_dir = Path(summary.output_dir)
    report = json.loads((output_dir / "relationship-improvement-report.json").read_text())
    summary_text = (output_dir / "relationship-improvement-summary.txt").read_text(encoding="utf-8")
    accepted_tsv = (output_dir / "accepted-relationships-review.tsv").read_text(encoding="utf-8")
    rejected_tsv = (output_dir / "rejected-relationships-review.tsv").read_text(encoding="utf-8")
    assert "quality_summary" in report
    assert "provider_summary" in report
    assert "cost_summary" in report
    assert "performance_summary" in report
    assert "pending-only review artifacts" in summary_text
    assert "Validation errors: 0" in summary_text
    assert "250 nodes / 500 pairs" in summary_text
    assert accepted_tsv.splitlines()[0].startswith("edge_key\tfrom_id")
    assert len(accepted_tsv.splitlines()) == summary.accepted_count + 1
    assert "reasoning_content" not in accepted_tsv
    assert "reasoning_content" not in rejected_tsv


def test_progress_auto_uses_plain_under_git_bash_without_windows_terminal():
    mode = ari.resolve_progress_mode(
        "auto",
        stdout_is_tty=True,
        rich_available=True,
        env={"MSYSTEM": "MINGW64", "TERM": "xterm-256color"},
    )

    assert mode == "plain"


def test_progress_auto_can_use_rich_under_windows_terminal_git_bash():
    mode = ari.resolve_progress_mode(
        "auto",
        stdout_is_tty=True,
        rich_available=True,
        env={"MSYSTEM": "MINGW64", "WT_SESSION": "session"},
    )

    assert mode == "rich"


def test_watcher_reads_validation_error_counts(tmp_path):
    output_dir = tmp_path / "run"
    output_dir.mkdir()
    ari.save_checkpoint(
        output_dir / "relationship-improvement-checkpoint.json",
        ari.Checkpoint(
            run_id="run",
            status="in_progress",
            input_path="input",
            output_dir=str(output_dir),
            embedding_model="embed",
            judge_model="judge",
            verifier_model="verify",
        ),
    )
    ari.append_jsonl(
        output_dir / "validation-errors.jsonl",
        {"role": "judge", "provider": "deepseek", "reason": "judge_validation_error"},
    )

    snapshot = ari.load_watch_snapshot(output_dir)
    rendered = ari.render_watch_plain(snapshot)

    assert snapshot.validation_error_count == 1
    assert "validation_errors=1" in rendered


def test_sanitizer_redacts_tokens_and_reasoning_content(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-secret-value")
    payload = {
        "headers": {"Authorization": "Bearer sk-test-secret-value"},
        "text": "token sk-anothersecret12345",
        "reasoning_content": "hidden",
        "embedding": [1, 2, 3],
    }

    sanitized = ari.sanitize_for_artifact(payload)
    text = json.dumps(sanitized)

    assert "sk-test-secret-value" not in text
    assert "sk-anothersecret12345" not in text
    assert "reasoning_content" not in text
    assert "embedding" not in text
