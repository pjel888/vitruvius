"""TransE link predictor — pure numpy, deterministic, JSON-persistable."""

from __future__ import annotations

import json
import textwrap
import warnings
from pathlib import Path

import numpy as np
import pytest

from vitruvius.extraction.kg_link_predictor import (
    DEFAULT_EMBED_DIM,
    DEFAULT_SEED,
    LinkCandidate,
    LinkPredictionReport,
    MIN_TRIPLES_NO_WARN,
    Triple,
    TransEModel,
    load_model,
    load_triples_from_canonical,
    predict_tail,
    save_model,
    score_triple,
    train_transe,
)


def _toy_triples() -> list[Triple]:
    return [
        Triple("france", "has_capital", "paris"),
        Triple("germany", "has_capital", "berlin"),
        Triple("japan", "has_capital", "tokyo"),
        Triple("spain", "has_capital", "madrid"),
        Triple("italy", "has_capital", "rome"),
    ]


def _bigger_triples() -> list[Triple]:
    countries = [
        "france",
        "germany",
        "japan",
        "spain",
        "italy",
        "korea",
        "brazil",
        "canada",
        "mexico",
        "argentina",
        "egypt",
        "kenya",
        "nigeria",
    ]
    capitals = [
        "paris",
        "berlin",
        "tokyo",
        "madrid",
        "rome",
        "seoul",
        "brasilia",
        "ottawa",
        "mexico_city",
        "buenos_aires",
        "cairo",
        "nairobi",
        "abuja",
    ]
    triples: list[Triple] = []
    for c, cap in zip(countries, capitals):
        triples.append(Triple(c, "has_capital", cap))
    continents = [
        ("france", "europe"),
        ("germany", "europe"),
        ("japan", "asia"),
        ("spain", "europe"),
        ("italy", "europe"),
        ("korea", "asia"),
        ("brazil", "south_america"),
        ("canada", "north_america"),
        ("mexico", "north_america"),
        ("argentina", "south_america"),
        ("egypt", "africa"),
        ("kenya", "africa"),
        ("nigeria", "africa"),
    ]
    for c, cont in continents:
        triples.append(Triple(c, "located_in", cont))
    return triples


def test_embeddings_have_correct_shape() -> None:
    triples = _bigger_triples()
    model = train_transe(triples, dim=16, epochs=10)
    assert model.entity_embeddings.shape == (model.n_entities, 16)
    assert model.relation_embeddings.shape == (model.n_relations, 16)
    assert model.dim == 16


def test_training_reduces_positive_triple_loss() -> None:
    triples = _bigger_triples()
    model_few = train_transe(triples, dim=16, epochs=1, seed=0)
    model_many = train_transe(triples, dim=16, epochs=50, seed=0)

    def total_pos_dist(m: TransEModel) -> float:
        return sum(score_triple(m, t.head, t.relation, t.tail) for t in triples)

    assert total_pos_dist(model_many) < total_pos_dist(model_few)


def test_link_prediction_ranks_known_tail_high() -> None:
    triples = _bigger_triples()
    model = train_transe(triples, dim=32, epochs=200, seed=0)
    report = predict_tail(model, "france", "has_capital", top_k=5)
    tails = [c.tail for c in report.candidates]
    assert "paris" in tails


def test_persists_embeddings_to_json(tmp_path: Path) -> None:
    triples = _bigger_triples()
    model = train_transe(triples, dim=8, epochs=5, seed=0)
    out = tmp_path / "model.json"
    save_model(model, out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert "entity_vocab" in data
    assert "entity_embeddings" in data
    assert len(data["entity_embeddings"]) == model.n_entities
    loaded = load_model(out)
    assert loaded.entity_vocab == model.entity_vocab
    assert loaded.relation_vocab == model.relation_vocab
    assert loaded.dim == model.dim
    np.testing.assert_allclose(
        loaded.entity_embeddings, model.entity_embeddings, atol=1e-10
    )
    np.testing.assert_allclose(
        loaded.relation_embeddings, model.relation_embeddings, atol=1e-10
    )


def test_deterministic_with_seeded_random() -> None:
    triples = _bigger_triples()
    m1 = train_transe(triples, dim=8, epochs=10, seed=42)
    m2 = train_transe(triples, dim=8, epochs=10, seed=42)
    np.testing.assert_array_equal(m1.entity_embeddings, m2.entity_embeddings)
    np.testing.assert_array_equal(m1.relation_embeddings, m2.relation_embeddings)


def test_different_seeds_produce_different_embeddings() -> None:
    triples = _bigger_triples()
    m1 = train_transe(triples, dim=8, epochs=10, seed=0)
    m2 = train_transe(triples, dim=8, epochs=10, seed=99)
    assert not np.array_equal(m1.entity_embeddings, m2.entity_embeddings)


def test_small_corpus_warns() -> None:
    triples = _toy_triples()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        train_transe(triples, dim=4, epochs=3)
    assert any(
        "undertrained" in str(w.message).lower() or "min" in str(w.message).lower()
        for w in caught
    )


def test_large_corpus_does_not_warn() -> None:
    triples = _bigger_triples()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        train_transe(triples, dim=4, epochs=3)
    assert not any(
        "undertrained" in str(w.message).lower() for w in caught
    )


def test_score_triple_unknown_entity_raises() -> None:
    model = train_transe(_bigger_triples(), dim=4, epochs=3)
    with pytest.raises(KeyError):
        score_triple(model, "nowhere", "has_capital", "paris")


def test_score_triple_unknown_relation_raises() -> None:
    model = train_transe(_bigger_triples(), dim=4, epochs=3)
    with pytest.raises(KeyError):
        score_triple(model, "france", "is_friends_with", "germany")


def test_predict_tail_unknown_head_returns_empty() -> None:
    model = train_transe(_bigger_triples(), dim=4, epochs=3)
    report = predict_tail(model, "unknown_place", "has_capital", top_k=5)
    assert report.candidates == ()
    assert report.query_head == "unknown_place"
    assert report.query_relation == "has_capital"


def test_predict_tail_unknown_relation_returns_empty() -> None:
    model = train_transe(_bigger_triples(), dim=4, epochs=3)
    report = predict_tail(model, "france", "is_friends_with", top_k=5)
    assert report.candidates == ()


def test_predict_tail_top_k_respected() -> None:
    model = train_transe(_bigger_triples(), dim=8, epochs=20, seed=0)
    report = predict_tail(model, "france", "has_capital", top_k=3)
    assert len(report.candidates) == 3
    # Ranks are 1-indexed and sorted ascending by score
    ranks = [c.rank for c in report.candidates]
    assert ranks == [1, 2, 3]
    scores = [c.score for c in report.candidates]
    assert scores == sorted(scores)


def test_link_candidate_fields_populated() -> None:
    model = train_transe(_bigger_triples(), dim=8, epochs=20, seed=0)
    report = predict_tail(model, "france", "has_capital", top_k=2)
    for cand in report.candidates:
        assert isinstance(cand, LinkCandidate)
        assert cand.head == "france"
        assert cand.relation == "has_capital"
        assert isinstance(cand.tail, str)
        assert cand.score >= 0.0


def test_load_triples_from_canonical_reads_frontmatter(tmp_path: Path) -> None:
    (tmp_path / "rel-a-governs-b.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: rel-a-governs-b
            from_entity: concept-a
            to_entity: concept-b
            relationship_type: governs
            ---

            Body.
            """
        )
    )
    (tmp_path / "rel-x-requires-y.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: rel-x-requires-y
            from_entity: concept-x
            to_entity: concept-y
            relationship_type: requires
            ---
            """
        )
    )
    (tmp_path / "bogus.md").write_text("no frontmatter\n")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        triples = load_triples_from_canonical(tmp_path)
    assert len(triples) == 2
    assert any(
        t.head == "concept-a" and t.tail == "concept-b" and t.relation == "governs"
        for t in triples
    )
    assert any(
        t.head == "concept-x" and t.tail == "concept-y" and t.relation == "requires"
        for t in triples
    )


def test_load_triples_from_canonical_skips_missing_fields(tmp_path: Path) -> None:
    (tmp_path / "missing-relationship-type.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: rel-c-d
            from_entity: concept-c
            to_entity: concept-d
            ---
            """
        )
    )
    (tmp_path / "good.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: rel-e-f
            from_entity: concept-e
            to_entity: concept-f
            relationship_type: affects
            ---
            """
        )
    )
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        triples = load_triples_from_canonical(tmp_path)
    assert len(triples) == 1
    assert triples[0].head == "concept-e"


def test_load_triples_from_canonical_missing_directory(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist"
    triples = load_triples_from_canonical(missing)
    assert triples == []


def test_entity_vocab_is_sorted() -> None:
    triples = _bigger_triples()
    model = train_transe(triples, dim=4, epochs=3)
    assert list(model.entity_vocab) == sorted(model.entity_vocab)
    assert list(model.relation_vocab) == sorted(model.relation_vocab)


def test_epochs_run_matches_request() -> None:
    triples = _bigger_triples()
    model = train_transe(triples, dim=4, epochs=7, seed=0)
    assert model.epochs_run == 7


def test_constants_are_documented() -> None:
    assert DEFAULT_EMBED_DIM == 50
    assert DEFAULT_SEED == 0
    assert MIN_TRIPLES_NO_WARN >= 10
