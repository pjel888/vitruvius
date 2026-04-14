"""spaCy SVO dependency parser — lazy-loaded, vocabulary-filtered triplets."""

from __future__ import annotations

import pytest

from vitruvius.extraction.spacy_dep_parser import (
    SPACY_MODEL_NAME,
    SvoCandidate,
    _get_nlp,
    extract_svo_triplets,
)


@pytest.fixture(scope="module")
def _model_loaded_once():
    _get_nlp()
    yield


def test_extracts_simple_svo(_model_loaded_once) -> None:
    text = "The Code requires a building permit."
    results = extract_svo_triplets(text)
    assert results
    assert any(
        "code" in r.subject.lower()
        and r.verb in {"require", "requires"}
        and "permit" in r.object.lower()
        for r in results
    )


def test_handles_passive_voice(_model_loaded_once) -> None:
    text = "A building permit is required by the Code."
    results = extract_svo_triplets(text)
    assert results
    assert any("permit" in r.subject.lower() for r in results)


def test_filters_to_concept_vocabulary(_model_loaded_once) -> None:
    text = "The Code requires a building permit. Elephants love bananas."
    vocab = ["building permit", "national code"]
    results = extract_svo_triplets(text, concept_vocabulary=vocab)
    assert not any("banana" in r.object.lower() for r in results)
    assert any("permit" in r.object.lower() for r in results)


def test_preserves_source_section_id(_model_loaded_once) -> None:
    text = "The Code requires a permit."
    results = extract_svo_triplets(text, source_section_id="sec-301")
    assert results
    for r in results:
        assert r.source_section_id == "sec-301"


def test_lazy_model_loading(monkeypatch) -> None:
    call_count = {"n": 0}

    class _FakeDoc:
        sents = ()

    class _FakeNlp:
        def __call__(self, text):
            return _FakeDoc()

    def counting_load(name, *args, **kwargs):
        call_count["n"] += 1
        return _FakeNlp()

    import spacy

    monkeypatch.setattr(spacy, "load", counting_load)
    _get_nlp.cache_clear()

    from vitruvius.extraction import spacy_dep_parser as _  # noqa: F401

    assert call_count["n"] == 0

    extract_svo_triplets("Test text.")
    assert call_count["n"] == 1

    extract_svo_triplets("Another sentence.")
    assert call_count["n"] == 1

    _get_nlp.cache_clear()


def test_empty_text_returns_empty_list(_model_loaded_once) -> None:
    assert extract_svo_triplets("") == []
    assert extract_svo_triplets("   \n  ") == []


def test_no_verbs_returns_empty_list(_model_loaded_once) -> None:
    results = extract_svo_triplets("Fire safety.")
    assert results == []


def test_sentence_offsets_recorded(_model_loaded_once) -> None:
    text = "First sentence. The Code requires a permit. Third sentence."
    results = extract_svo_triplets(text)
    assert results
    for r in results:
        assert 0 <= r.sentence_start < r.sentence_end <= len(text)
        reconstructed = text[r.sentence_start : r.sentence_end]
        assert r.sentence.strip() in reconstructed or reconstructed.strip() == r.sentence.strip()
        assert reconstructed.strip().endswith(".")


def test_svo_candidate_is_frozen(_model_loaded_once) -> None:
    text = "The Code requires a permit."
    results = extract_svo_triplets(text)
    assert results
    candidate = results[0]
    assert isinstance(candidate, SvoCandidate)
    with pytest.raises((AttributeError, Exception)):
        candidate.subject = "mutated"  # type: ignore[misc]


def test_spacy_model_name_constant() -> None:
    assert SPACY_MODEL_NAME == "en_core_web_sm"


def test_vocabulary_case_insensitive_filter(_model_loaded_once) -> None:
    text = "The CODE requires a PERMIT."
    vocab = ["Building Permit"]
    results = extract_svo_triplets(text, concept_vocabulary=vocab)
    assert any("permit" in r.object.lower() for r in results)


def test_default_source_section_id_is_empty(_model_loaded_once) -> None:
    text = "The Code requires a permit."
    results = extract_svo_triplets(text)
    assert results
    assert all(r.source_section_id == "" for r in results)
