"""Shannon entropy character classifier — pure stdlib, deterministic, tests <1s."""

from __future__ import annotations

import math

from vitruvius.parsers.shannon_classifier import (
    character_entropy,
    is_garbled,
    classify_by_entropy,
)


def test_character_entropy_of_empty_string_is_zero() -> None:
    assert character_entropy("") == 0.0


def test_character_entropy_of_repeated_single_char_is_zero() -> None:
    assert character_entropy("aaaaa") == 0.0


def test_character_entropy_of_uniform_distribution_reaches_log2_n() -> None:
    text = "abcdefgh"
    assert math.isclose(character_entropy(text), 3.0, abs_tol=1e-9)


def test_character_entropy_of_english_text_is_moderate() -> None:
    text = "The National Building Code of the Philippines is Presidential Decree 1096."
    h = character_entropy(text)
    assert 3.5 < h < 4.8


def test_is_garbled_flags_high_entropy_text() -> None:
    garbled = "".join(chr(i) for i in range(1, 200))
    assert is_garbled(garbled, threshold=4.5) is True


def test_is_garbled_accepts_clean_english() -> None:
    clean = "Section 804. Setbacks. Every building shall comply with the following."
    assert is_garbled(clean, threshold=4.5) is False


def test_classify_clean_english_as_clean() -> None:
    assert classify_by_entropy("Section 804. Setbacks.") == "clean"


def test_classify_garbled_text_as_garbled_or_noisy() -> None:
    garbled = "B@1ld!ng 0ff1c*a1 \\x03\\x07\\x0f ???"
    result = classify_by_entropy(garbled)
    assert result in {"noisy", "garbled"}


def test_classify_high_entropy_text_as_garbled() -> None:
    text = "".join(chr(i) for i in range(1, 256))
    assert classify_by_entropy(text) == "garbled"


def test_character_entropy_handles_control_characters() -> None:
    text = "\x00\x01\x02\x03"
    h = character_entropy(text)
    assert math.isclose(h, 2.0, abs_tol=1e-9)


def test_character_entropy_never_negative() -> None:
    for text in ["", "a", "ab", "abc", "The quick brown fox."]:
        assert character_entropy(text) >= 0.0


def test_is_garbled_custom_threshold() -> None:
    text = "abcdefgh"
    assert is_garbled(text, threshold=2.5) is True
    assert is_garbled(text, threshold=3.5) is False
