from vitruvius.normalization import NormalizationEngine
from vitruvius.normalization.rules_tier_a import TIER_A_RULES
from vitruvius.normalization.rules_tier_b import (
    NormalizeSectionAbbreviation,
    NormalizeSetextToAtx,
    TIER_B_RULES,
    TrimHeadingWhitespace,
)


def test_normalize_section_abbreviation_expands_sec_prefix():
    rule = NormalizeSectionAbbreviation()
    assert rule.apply("SEC. 101") == "SECTION 101"
    assert rule.apply("Sec. 302 Building Permits") == "SECTION 302 Building Permits"
    # Already expanded, no change
    assert rule.apply("SECTION 101") == "SECTION 101"


def test_normalize_section_abbreviation_does_not_munge_sections_word():
    rule = NormalizeSectionAbbreviation()
    assert rule.apply("the sections below") == "the sections below"


def test_normalize_setext_to_atx_h1():
    rule = NormalizeSetextToAtx()
    setext = "Title\n=====\n\nBody"
    atx = rule.apply(setext)
    assert atx.startswith("# Title")


def test_normalize_setext_to_atx_h2():
    rule = NormalizeSetextToAtx()
    setext = "Subtitle\n--------\n\nBody"
    atx = rule.apply(setext)
    assert "## Subtitle" in atx


def test_trim_heading_whitespace():
    rule = TrimHeadingWhitespace()
    assert rule.apply("##   Spaced Header   ") == "## Spaced Header"
    assert rule.apply("#Tight") == "# Tight"
    # multi-line
    input_text = "# Top\n\n##    Sub"
    assert rule.apply(input_text) == "# Top\n\n## Sub"


def test_tier_b_pipeline_idempotent():
    engine = NormalizationEngine()
    for rule in TIER_A_RULES:
        engine.register(rule)
    for rule in TIER_B_RULES:
        engine.register(rule)

    raw = "SEC. 101 Title\n==============\n\n##   Body  \r\n\r\nEvery building\x00"
    once, _ = engine.run(raw)
    twice, _ = engine.run(once)
    assert once == twice
