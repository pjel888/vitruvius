from vitruvius.normalization import NormalizationEngine
from vitruvius.normalization.rules_tier_a import (
    CollapseConsecutiveBlankLines,
    CollapseTrailingWhitespace,
    NormalizeLineEndings,
    StripControlChars,
    TIER_A_RULES,
    UnicodeNFC,
)


def test_unicode_nfc_composes_decomposed_form():
    # "é" as "e" + combining acute
    decomposed = "e\u0301"
    nfc = UnicodeNFC().apply(decomposed)
    assert nfc == "\u00e9"
    assert len(nfc) == 1


def test_strip_control_chars_removes_nulls_but_keeps_tab_newline():
    rule = StripControlChars()
    assert rule.apply("hello\x00world") == "helloworld"
    assert rule.apply("a\tb\nc\rd") == "a\tb\nc\rd"
    assert rule.apply("bell\x07") == "bell"


def test_normalize_line_endings_handles_crlf_and_cr():
    rule = NormalizeLineEndings()
    assert rule.apply("a\r\nb\rc\nd") == "a\nb\nc\nd"


def test_collapse_trailing_whitespace():
    rule = CollapseTrailingWhitespace()
    assert rule.apply("hello   \nworld\t\n") == "hello\nworld\n"


def test_collapse_consecutive_blank_lines():
    rule = CollapseConsecutiveBlankLines()
    assert rule.apply("a\n\n\n\nb") == "a\n\nb"
    assert rule.apply("a\n\nb") == "a\n\nb"


def test_all_tier_a_rules_are_idempotent_on_mixed_text():
    engine = NormalizationEngine()
    for rule in TIER_A_RULES:
        engine.register(rule)

    raw = "Hëllo\r\n\r\n\r\nwörld   \n\n\n\x00foo\t"
    once, _ = engine.run(raw)
    twice, _ = engine.run(once)
    assert once == twice, "Tier A rules must be idempotent"


def test_tier_a_pipeline_cleans_realistic_noise():
    engine = NormalizationEngine()
    for rule in TIER_A_RULES:
        engine.register(rule)

    raw = "Section 701\r\n\r\n\r\nEvery building shall be classified\x00...  \r\n"
    clean, audit = engine.run(raw)
    assert "\x00" not in clean
    assert "\r" not in clean
    assert "\n\n\n" not in clean
    assert "  \n" not in clean
    assert len(audit) == 5  # five Tier A rules ran
