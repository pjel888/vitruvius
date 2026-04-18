"""Tests for the markdown section extractor."""

from __future__ import annotations

import pytest

from vitruvius.parsers.section_extractor import derive_section_map


class TestDeriveSectionMap:

    def test_empty_string_returns_empty(self) -> None:
        assert derive_section_map("") == []

    def test_no_headings_returns_empty(self) -> None:
        text = "This is just plain text.\nNo headings here.\n"
        assert derive_section_map(text) == []

    def test_single_heading(self) -> None:
        text = "# Title\n\nSome body text.\n"
        sections = derive_section_map(text)
        assert len(sections) == 1
        assert sections[0].title == "Title"
        assert sections[0].level == 1
        assert sections[0].line_start == 1
        assert sections[0].line_end == 3
        assert sections[0].char_start is not None
        assert sections[0].char_end is not None
        assert sections[0].char_end > sections[0].char_start

    def test_multiple_headings(self) -> None:
        text = (
            "# Overview\n\n"
            "This is the overview.\n\n"
            "## Details\n\n"
            "More details here.\n"
        )
        sections = derive_section_map(text)
        assert len(sections) == 2
        assert sections[0].title == "Overview"
        assert sections[0].level == 1
        assert sections[1].title == "Details"
        assert sections[1].level == 2

    def test_headings_with_frontmatter(self) -> None:
        text = (
            "---\n"
            "id: test-doc\n"
            "---\n\n"
            "# Section One\n\n"
            "Body one.\n\n"
            "## Section Two\n\n"
            "Body two.\n"
        )
        sections = derive_section_map(text)
        assert len(sections) == 2
        assert sections[0].title == "Section One"
        assert sections[1].title == "Section Two"

    def test_char_offsets_are_monotonic(self) -> None:
        text = (
            "# First\n\n"
            "Body of first.\n\n"
            "# Second\n\n"
            "Body of second.\n"
        )
        sections = derive_section_map(text)
        assert len(sections) == 2
        assert sections[0].char_start < sections[0].char_end
        assert sections[1].char_start < sections[1].char_end
        assert sections[0].char_end <= sections[1].char_start

    def test_deep_headings(self) -> None:
        text = (
            "# H1\n"
            "## H2\n"
            "### H3\n"
            "#### H4\n"
            "##### H5\n"
            "###### H6\n"
        )
        sections = derive_section_map(text)
        assert len(sections) == 6
        for i, sec in enumerate(sections, start=1):
            assert sec.level == i

    def test_heading_with_extra_whitespace(self) -> None:
        text = "#   Spaced Out   \n\nBody.\n"
        sections = derive_section_map(text)
        assert len(sections) == 1
        assert sections[0].title == "Spaced Out"
