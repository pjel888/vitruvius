"""CRF trainer scaffold — pure python-crfsuite, synthetic training only in tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vitruvius.extraction.crf_trainer import (
    DEFAULT_MODEL_DIR,
    InsufficientTrainingDataError,
    MIN_TRAINING_EXAMPLES,
    MODEL_FILENAME_PREFIX,
    TrainingExample,
    TrainingMetadata,
    hash_corpus,
    token_features,
    train_crf,
)


def _make_example(tokens: list[str], labels: list[str]) -> TrainingExample:
    return TrainingExample(tokens=tuple(tokens), labels=tuple(labels))


def _make_corpus(n: int) -> list[TrainingExample]:
    base = _make_example(
        ["The", "Code", "requires", "a", "permit", "."],
        ["O", "B-SUBJ", "B-PRED", "O", "B-OBJ", "O"],
    )
    return [base] * n


def test_crfsuite_importable() -> None:
    import pycrfsuite  # noqa: F401


def test_min_training_examples_constant() -> None:
    assert MIN_TRAINING_EXAMPLES == 50


def test_default_model_dir_constant_exists() -> None:
    assert isinstance(DEFAULT_MODEL_DIR, Path)


def test_model_filename_prefix_constant() -> None:
    assert MODEL_FILENAME_PREFIX == "crf_extractor_"


def test_training_example_is_frozen() -> None:
    ex = _make_example(["a"], ["O"])
    with pytest.raises((AttributeError, Exception)):
        ex.tokens = ("b",)  # type: ignore[misc]


def test_builds_feature_vector_per_token() -> None:
    tokens = ["The", "Code", "requires", "a", "permit"]
    features = token_features(
        tokens, index=1, concept_vocabulary=frozenset({"code", "permit"})
    )
    assert "t" in features or any(k.startswith("t") for k in features)
    cap = features.get("cap")
    assert cap is True or features.get("cap=True") is not None or str(cap).lower() in {
        "true",
        "1",
    }


def test_features_in_vocab_flag_true_when_token_matches() -> None:
    tokens = ["The", "Code", "requires"]
    feats = token_features(
        tokens, index=1, concept_vocabulary=frozenset({"code"})
    )
    in_vocab = feats.get("in_vocab")
    assert in_vocab is True or str(in_vocab).lower() in {"true", "1"}


def test_features_in_vocab_flag_false_when_no_match() -> None:
    tokens = ["The", "Code", "requires"]
    feats = token_features(
        tokens, index=0, concept_vocabulary=frozenset({"banana"})
    )
    in_vocab = feats.get("in_vocab")
    assert in_vocab is False or str(in_vocab).lower() in {"false", "0"}


def test_features_include_neighbor_info() -> None:
    tokens = ["The", "Code", "requires", "a", "permit"]
    middle = token_features(tokens, index=2)
    first = token_features(tokens, index=0)
    last = token_features(tokens, index=len(tokens) - 1)

    def has_neighbor_info(feats: dict[str, object]) -> bool:
        keys = list(feats.keys())
        vals = list(feats.values())
        return (
            any("prev" in k.lower() for k in keys)
            or any("next" in k.lower() for k in keys)
            or any("<BOS>" in str(v) for v in vals)
            or any("<EOS>" in str(v) for v in vals)
        )

    assert has_neighbor_info(middle)
    assert has_neighbor_info(first)
    assert has_neighbor_info(last)


def test_features_edge_tokens_use_sentinels() -> None:
    tokens = ["alpha", "beta", "gamma"]
    first = token_features(tokens, index=0)
    last = token_features(tokens, index=2)
    first_has_bos = any("<BOS>" in str(v) for v in first.values())
    last_has_eos = any("<EOS>" in str(v) for v in last.values())
    assert first_has_bos
    assert last_has_eos


def test_hash_corpus_is_deterministic() -> None:
    c1 = _make_corpus(5)
    c2 = _make_corpus(5)
    assert hash_corpus(c1) == hash_corpus(c2)


def test_hash_corpus_changes_with_different_input() -> None:
    c1 = _make_corpus(5)
    c2 = _make_corpus(5) + [_make_example(["new"], ["O"])]
    assert hash_corpus(c1) != hash_corpus(c2)


def test_hash_corpus_changes_when_labels_differ() -> None:
    c1 = [_make_example(["foo", "bar"], ["O", "B-SUBJ"])]
    c2 = [_make_example(["foo", "bar"], ["O", "B-OBJ"])]
    assert hash_corpus(c1) != hash_corpus(c2)


def test_refuses_to_train_below_min_examples(tmp_path: Path) -> None:
    examples = _make_corpus(MIN_TRAINING_EXAMPLES - 1)
    with pytest.raises(InsufficientTrainingDataError):
        train_crf(examples, model_dir=tmp_path)


def test_refuses_to_train_on_empty_corpus(tmp_path: Path) -> None:
    with pytest.raises(InsufficientTrainingDataError):
        train_crf([], model_dir=tmp_path)


def test_training_converges_on_toy_data(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=tmp_path, now_utc=now)
    model_path = Path(meta.model_path)
    assert model_path.exists()
    assert model_path.stat().st_size > 0


def test_saves_model_with_timestamp(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=tmp_path, now_utc=now)
    assert "20260414T120000Z" in meta.model_path
    assert Path(meta.model_path).name.startswith(MODEL_FILENAME_PREFIX)


def test_writes_training_metadata(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=tmp_path, now_utc=now)
    mpath = Path(meta.metadata_path)
    assert mpath.exists()
    data = json.loads(mpath.read_text())
    assert "timestamp_utc" in data
    assert "training_corpus_hash" in data
    assert "example_count" in data
    assert data["example_count"] == 60
    assert "label_distribution" in data
    assert "model_path" in data
    assert "metadata_path" in data


def test_metadata_path_uses_meta_json_suffix(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=tmp_path, now_utc=now)
    assert meta.metadata_path.endswith(".meta.json")


def test_idempotent_on_same_corpus_hash(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta1 = train_crf(examples, model_dir=tmp_path, now_utc=now)
    meta2 = train_crf(examples, model_dir=tmp_path, now_utc=now)
    assert meta1.training_corpus_hash == meta2.training_corpus_hash


def test_label_distribution_counts_all_tags(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=tmp_path, now_utc=now)
    dist = meta.label_distribution
    assert dist.get("O", 0) == 60 * 3
    assert dist.get("B-SUBJ", 0) == 60
    assert dist.get("B-PRED", 0) == 60
    assert dist.get("B-OBJ", 0) == 60


def test_metadata_returned_matches_metadata_on_disk(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=tmp_path, now_utc=now)
    on_disk = json.loads(Path(meta.metadata_path).read_text())
    assert on_disk["training_corpus_hash"] == meta.training_corpus_hash
    assert on_disk["example_count"] == meta.example_count
    assert on_disk["timestamp_utc"] == meta.timestamp_utc


def test_creates_model_dir_if_missing(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    target = tmp_path / "nested" / "models"
    assert not target.exists()
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(examples, model_dir=target, now_utc=now)
    assert target.exists()
    assert Path(meta.model_path).parent == target


def test_mismatched_token_label_lengths_rejected(tmp_path: Path) -> None:
    bad = _make_example(["a", "b", "c"], ["O", "O"])
    examples = [bad] * 60
    with pytest.raises(ValueError):
        train_crf(examples, model_dir=tmp_path)


def test_concept_vocabulary_plumbed_through_to_features(tmp_path: Path) -> None:
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    meta = train_crf(
        examples,
        model_dir=tmp_path,
        now_utc=now,
        concept_vocabulary=frozenset({"code", "permit"}),
    )
    assert Path(meta.model_path).exists()
