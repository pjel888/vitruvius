"""Tier C — Jaro-Winkler OCR typo correction. Destructive, audited, flag-gated."""

from __future__ import annotations

import textwrap
from pathlib import Path

from vitruvius.features import Features
from vitruvius.normalization.rules_tier_c import (
    DEFAULT_STOPWORDS,
    build_vocabulary_from_concepts,
    correct_ocr_typos,
)


# Canonical vocabulary used by tests. Keep it small and explicit.
VOCAB = ["Building Official", "Building Permit", "Occupancy Classification"]


def test_replaces_bui1ding_officia1_with_building_official() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "The Bui1ding Officia1 shall issue the permit."
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert "Building" in corrected
    assert "Official" in corrected
    assert "Bui1ding" not in corrected
    assert "Officia1" not in corrected
    originals = {entry["original"] for entry in audit}
    assert "Bui1ding" in originals
    assert "Officia1" in originals


def test_ignores_standard_english_words() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "The building code is the foundation of public safety."
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    # 'the' / 'foundation' / 'safety' must survive the pass — they are either
    # stopwords (the), far from any vocab token (foundation, safety), or both.
    # Substring match is used intentionally: the trailing period on 'safety.'
    # is punctuation the tokenizer leaves alone, so a bare-word split check
    # would spuriously fail on 'safety.' vs 'safety'.
    lowered = corrected.lower()
    assert "the " in lowered
    assert "foundation" in lowered
    assert "safety" in lowered
    # And no audit entries should have been recorded for these words.
    untouched = {"the", "foundation", "safety"}
    recorded = {entry["original"].lower() for entry in audit}
    assert untouched.isdisjoint(recorded)


def test_ignores_very_short_tokens() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "an ab xyz"
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert corrected == text
    assert audit == []


def test_audit_entry_shape() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "Bui1ding Officia1"
    _, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert audit, "expected at least one replacement for audit inspection"
    for entry in audit:
        assert set(entry.keys()) >= {
            "rule",
            "original",
            "replaced",
            "similarity",
            "position",
        }
        assert entry["rule"] == "jaro_winkler_ocr_fix"
        assert isinstance(entry["similarity"], float)
        assert 0.92 <= entry["similarity"] <= 1.0
        assert isinstance(entry["position"], int) and entry["position"] >= 0


def test_flag_off_no_replacement() -> None:
    features = Features(flags={})
    text = "Bui1ding Officia1"
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert corrected == text
    assert audit == []


def test_flag_off_explicit_false_no_replacement() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": False})
    text = "Bui1ding Officia1"
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert corrected == text
    assert audit == []


def test_similarity_below_threshold_not_replaced() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "The Cement was applied."
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert "Cement" in corrected
    assert not any(entry["original"] == "Cement" for entry in audit)


def test_threshold_is_configurable() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "Bui1ding"
    _, audit = correct_ocr_typos(
        text, features=features, vocabulary=VOCAB, min_similarity=0.99
    )
    assert audit == []


def test_position_is_character_offset_of_original_token() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "Alpha Bui1ding beta"
    _, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    replacements = [e for e in audit if e["original"] == "Bui1ding"]
    assert replacements, "expected Bui1ding to be replaced"
    assert replacements[0]["position"] == text.index("Bui1ding")


def test_stopwords_are_never_replaced() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    stopwords = frozenset(DEFAULT_STOPWORDS | {"cement"})
    text = "The Cement was applied."
    _, audit = correct_ocr_typos(
        text,
        features=features,
        vocabulary=["Cenent"],
        stopwords=stopwords,
    )
    assert not any(entry["original"].lower() == "cement" for entry in audit)


def test_canonical_case_preserved_in_replacement() -> None:
    features = Features(flags={"c_tier_c_ocr_fix": True})
    text = "Bui1ding"
    corrected, audit = correct_ocr_typos(text, features=features, vocabulary=VOCAB)
    assert "Building" in corrected
    assert audit[0]["replaced"] == "Building"


def test_build_vocabulary_reads_concept_titles(tmp_path: Path) -> None:
    concepts = tmp_path / "concepts"
    concepts.mkdir()
    (concepts / "building-permit.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: concept-building-permit
            title: Building Permit
            page_type: concept
            ---

            # Building Permit
            """
        )
    )
    (concepts / "yards.md").write_text(
        textwrap.dedent(
            """\
            ---
            id: concept-yards
            title: Yards
            ---
            """
        )
    )
    vocab = build_vocabulary_from_concepts(concepts)
    assert "Building Permit" in vocab
    assert "Yards" in vocab
    assert vocab == sorted(set(vocab))


def test_build_vocabulary_skips_files_without_title(tmp_path: Path) -> None:
    concepts = tmp_path / "c"
    concepts.mkdir()
    (concepts / "no_title.md").write_text("# Just a heading, no frontmatter\n")
    vocab = build_vocabulary_from_concepts(concepts)
    assert vocab == []
