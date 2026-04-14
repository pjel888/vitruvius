"""Tier B (structural) normalization rules.

These rules standardize Markdown structure. They are always-on for Markdown
scope but make small semantic-looking changes like `SEC. 101` to `SECTION 101`.
Because they match regex patterns exactly, they are deterministic and
idempotent.
"""

from __future__ import annotations

import re


class NormalizeSectionAbbreviation:
    """`SEC. 101` or `Sec. 101` to `SECTION 101`.

    Matches only when followed by a digit. Does not affect the word
    "sections" or other uses of `sec`.
    """

    name = "normalize-section-abbreviation"
    tier = "B"
    phase = 3
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    _PATTERN = re.compile(r"\b[Ss][Ee][Cc]\.\s+(?=\d)")

    def apply(self, text: str) -> str:
        return self._PATTERN.sub("SECTION ", text)


class NormalizeSetextToAtx:
    """Convert Setext-style H1/H2 headers to ATX-style.

    Setext H1:           Setext H2:
        Title                Title
        =====                -----

    Become:
        # Title              ## Title
    """

    name = "normalize-setext-to-atx"
    tier = "B"
    phase = 3
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    # Match a non-blank line followed by a line of at least 3 `=` (H1) or `-` (H2).
    _H1 = re.compile(r"^(?P<title>[^\n]+)\n=+[ \t]*$", re.MULTILINE)
    _H2 = re.compile(r"^(?P<title>[^\n]+)\n-+[ \t]*$", re.MULTILINE)

    def apply(self, text: str) -> str:
        text = self._H1.sub(lambda m: f"# {m.group('title').strip()}", text)
        text = self._H2.sub(lambda m: f"## {m.group('title').strip()}", text)
        return text


class TrimHeadingWhitespace:
    """`##   Foo   ` to `## Foo`. Ensures exactly one space between hashes and the title."""

    name = "trim-heading-whitespace"
    tier = "B"
    phase = 3
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    _HEADING = re.compile(r"^(#{1,6})[ \t]*(.*?)[ \t]*$", re.MULTILINE)

    def apply(self, text: str) -> str:
        def _fix(m: re.Match) -> str:
            hashes, title = m.group(1), m.group(2).strip()
            if not title:
                return hashes
            return f"{hashes} {title}"
        return self._HEADING.sub(_fix, text)


TIER_B_RULES = [
    # Order within phase 3: convert Setext first (so subsequent rules see ATX),
    # then expand section abbreviations, then normalize heading whitespace last
    # (so it cleans up the ATX headers produced above).
    NormalizeSetextToAtx(),
    NormalizeSectionAbbreviation(),
    TrimHeadingWhitespace(),
]
