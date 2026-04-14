"""Tier A (lossless) normalization rules.

These rules are always-on. They perform only reversible/lossless operations:
Unicode normalization, control-char stripping (except tab/newline), CRLF to LF,
trailing-whitespace trim, and blank-line collapse.

All Tier A rules MUST satisfy normalize(normalize(x)) == normalize(x).
"""

from __future__ import annotations

import re
import unicodedata


class UnicodeNFC:
    name = "unicode-nfc"
    tier = "A"
    phase = 1
    scope = ["document_text", "identifier", "filename", "metadata_fields"]
    gated_by: list[str] = []
    is_deterministic = True

    def apply(self, text: str) -> str:
        return unicodedata.normalize("NFC", text)


class StripControlChars:
    """Remove ASCII / Unicode control chars except tab, newline, carriage return.

    CR is removed later by NormalizeLineEndings. Keeping it here preserves
    Phase 1 vs Phase 2 separation: Phase 1 is encoding-only, Phase 2 is whitespace.
    """

    name = "strip-control-chars"
    tier = "A"
    phase = 1
    scope = ["document_text", "metadata_fields"]
    gated_by: list[str] = []
    is_deterministic = True

    _KEEP = {"\t", "\n", "\r"}

    def apply(self, text: str) -> str:
        return "".join(
            ch for ch in text
            if ch in self._KEEP or unicodedata.category(ch)[0] != "C"
        )


class NormalizeLineEndings:
    name = "normalize-line-endings"
    tier = "A"
    phase = 2
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    def apply(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n")


class CollapseTrailingWhitespace:
    name = "collapse-trailing-whitespace"
    tier = "A"
    phase = 2
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    _TRAILING = re.compile(r"[ \t]+(\n|$)")

    def apply(self, text: str) -> str:
        return self._TRAILING.sub(r"\1", text)


class CollapseConsecutiveBlankLines:
    """Collapse 3+ consecutive newlines to exactly 2 (one blank line)."""

    name = "collapse-consecutive-blank-lines"
    tier = "A"
    phase = 2
    scope = ["document_text"]
    gated_by: list[str] = []
    is_deterministic = True

    _MANY_BLANK = re.compile(r"\n{3,}")

    def apply(self, text: str) -> str:
        return self._MANY_BLANK.sub("\n\n", text)


TIER_A_RULES = [
    # Phase 1 (encoding): NFC first, then control-char strip (which may
    # expose new composition boundaries only NFC can handle).
    UnicodeNFC(),
    StripControlChars(),
    # Phase 2 (whitespace): line-endings MUST come before trailing-whitespace
    # and blank-line collapse, otherwise CRLF sequences slip through.
    NormalizeLineEndings(),
    CollapseTrailingWhitespace(),
    CollapseConsecutiveBlankLines(),
]
