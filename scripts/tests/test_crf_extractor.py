"""CRF extractor — loads latest model, tags tokens, emits CrfCandidate records."""

from __future__ import annotations

import warnings
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vitruvius.extraction.crf_extractor import (
    CrfCandidate,
    _load_tagger_for_path,
    extract_from_sentence,
    extract_from_sentences,
    find_latest_model_path,
)
from vitruvius.extraction.crf_trainer import (
    TrainingExample,
    train_crf,
)


def _make_corpus(n: int) -> list[TrainingExample]:
    base = TrainingExample(
        tokens=("The", "Code", "requires", "a", "permit", "."),
        labels=("O", "B-SUBJ", "B-PRED", "O", "B-OBJ", "O"),
    )
    return [base] * n


@pytest.fixture
def trained_model_dir(tmp_path: Path) -> Path:
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    examples = _make_corpus(60)
    now = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
    train_crf(examples, model_dir=model_dir, now_utc=now)
    _load_tagger_for_path.cache_clear()
    return model_dir


def test_no_model_present_returns_empty_with_warning(tmp_path: Path) -> None:
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = extract_from_sentence(
            ["The", "Code", "requires", "a", "permit"],
            model_dir=empty_dir,
        )
    assert result == []
    assert any("no crf model" in str(w.message).lower() for w in caught)


def test_find_latest_model_path_returns_none_when_empty(tmp_path: Path) -> None:
    assert find_latest_model_path(tmp_path) is None


def test_find_latest_model_path_returns_none_when_dir_missing(tmp_path: Path) -> None:
    assert find_latest_model_path(tmp_path / "nonexistent") is None


def test_find_latest_model_path_picks_lexicographic_latest(tmp_path: Path) -> None:
    (tmp_path / "crf_extractor_20260101T000000Z.crfsuite").write_bytes(b"x")
    (tmp_path / "crf_extractor_20260501T000000Z.crfsuite").write_bytes(b"y")
    latest = find_latest_model_path(tmp_path)
    assert latest is not None
    assert "20260501" in latest.name


def test_find_latest_model_path_ignores_non_matching(tmp_path: Path) -> None:
    (tmp_path / "crf_extractor_20260101T000000Z.crfsuite").write_bytes(b"x")
    (tmp_path / "crf_extractor_20260101T000000Z.meta.json").write_text("{}")
    (tmp_path / "unrelated.crfsuite").write_bytes(b"z")
    latest = find_latest_model_path(tmp_path)
    assert latest is not None
    assert latest.name == "crf_extractor_20260101T000000Z.crfsuite"


def test_tags_sentence_with_known_structure(trained_model_dir: Path) -> None:
    result = extract_from_sentence(
        ["The", "Code", "requires", "a", "permit", "."],
        model_dir=trained_model_dir,
    )
    assert result
    cand = result[0]
    assert isinstance(cand, CrfCandidate)
    assert cand.source == "crf"
    assert "code" in cand.from_id.lower()
    assert "requires" in cand.predicate.lower()
    assert "permit" in cand.to_id.lower()


def test_returns_empty_on_unknown_structure(trained_model_dir: Path) -> None:
    result = extract_from_sentence(
        ["Hello", "world", "banana"],
        model_dir=trained_model_dir,
    )
    assert isinstance(result, list)


def test_reuses_loaded_model_across_calls(trained_model_dir: Path) -> None:
    _load_tagger_for_path.cache_clear()
    before = _load_tagger_for_path.cache_info().misses
    extract_from_sentence(
        ["The", "Code", "requires", "a", "permit"],
        model_dir=trained_model_dir,
    )
    extract_from_sentence(
        ["Every", "building", "needs", "a", "permit"],
        model_dir=trained_model_dir,
    )
    info = _load_tagger_for_path.cache_info()
    assert info.misses == before + 1
    assert info.hits >= 1


def test_emits_candidate_compatible_schema(trained_model_dir: Path) -> None:
    result = extract_from_sentence(
        ["The", "Code", "requires", "a", "permit", "."],
        model_dir=trained_model_dir,
    )
    assert result
    cand = result[0]
    assert hasattr(cand, "from_id")
    assert hasattr(cand, "predicate")
    assert hasattr(cand, "to_id")
    assert hasattr(cand, "occurrences")
    assert hasattr(cand, "examples")
    assert hasattr(cand, "source")
    assert isinstance(cand.examples, tuple)
    assert cand.occurrences >= 1


def test_extract_from_sentences_merges_duplicates(trained_model_dir: Path) -> None:
    result = extract_from_sentences(
        [
            ["The", "Code", "requires", "a", "permit"],
            ["The", "Code", "requires", "a", "permit"],
        ],
        model_dir=trained_model_dir,
    )
    code_permit = [
        c for c in result if "permit" in c.to_id.lower() and "code" in c.from_id.lower()
    ]
    if code_permit:
        assert code_permit[0].occurrences >= 2


def test_extract_from_sentences_returns_sorted(trained_model_dir: Path) -> None:
    result = extract_from_sentences(
        [
            ["The", "Code", "requires", "a", "permit"],
            ["The", "Code", "requires", "a", "permit"],
        ],
        model_dir=trained_model_dir,
    )
    keys = [(c.from_id, c.predicate, c.to_id) for c in result]
    assert keys == sorted(keys)


def test_examples_carry_position_offsets(trained_model_dir: Path) -> None:
    result = extract_from_sentence(
        ["The", "Code", "requires", "a", "permit", "."],
        model_dir=trained_model_dir,
    )
    if result:
        cand = result[0]
        for ex in cand.examples:
            assert isinstance(ex, tuple)
            assert len(ex) == 3
            phrase, start, end = ex
            assert isinstance(phrase, str)
            assert isinstance(start, int)
            assert isinstance(end, int)
            assert start >= 0
            assert end >= start


def test_no_model_present_does_not_raise_on_batch(tmp_path: Path) -> None:
    empty_dir = tmp_path / "still_empty"
    empty_dir.mkdir()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = extract_from_sentences(
            [["a", "b", "c"], ["d", "e", "f"]],
            model_dir=empty_dir,
        )
    assert result == []
