from unittest.mock import patch

from vitruvius.canonicalize import build_structured_source_file


def test_builds_file_with_all_four_sections(tmp_path):
    refined = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "raw_markdown"
    refined.mkdir(parents=True)
    (refined / "sample.md").write_text(
        "# Sample Law\n\nThis law governs buildings.\n\n"
        "## Section 1\n\nAll buildings must have permits.\n\n"
        "## Section 2\n\nFire safety is mandatory.\n",
        encoding="utf-8",
    )
    (tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts").mkdir(parents=True)

    with patch("vitruvius.canonicalize.load_rules", return_value={"rules": []}):
        target, content = build_structured_source_file(
            repo_root=tmp_path,
            relative_markdown_path="001-Laws/raw_markdown/sample.md",
        )

    assert "## Overview" in content
    assert "## Coverage" in content
    assert "## Key Points" in content
    assert "## Referenced Concepts" in content
    assert "Section 1" in content  # header should appear in Coverage
    assert "Section 2" in content
