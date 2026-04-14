import json
from pathlib import Path

from vitruvius.normalization.refine import refine_one_inner, build_refined_paths


def test_build_refined_paths_mirrors_source_structure():
    refined_md, manifest = build_refined_paths("001-Laws/raw_markdown/PD-1096/foo.md")
    assert refined_md == Path("001-Laws/refined_markdown/PD-1096/foo.md")
    assert manifest == Path("001-Laws/refined_markdown/PD-1096/foo.refined.json")


def test_refine_one_inner_emits_cleaned_markdown_and_manifest(tmp_path):
    # Seed a messy raw markdown file.
    conversion = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "raw_markdown" / "PD-1096"
    conversion.mkdir(parents=True)
    raw = conversion / "sample.md"
    raw.write_text(
        "SEC. 101 Title\r\n"
        "==============\r\n"
        "\r\n"
        "\r\n"
        "##   Sub   \r\n"
        "\r\n"
        "Every building shall be classified\x00\r\n",
        encoding="utf-8",
    )

    rc = refine_one_inner(
        repo_root=tmp_path,
        relative_markdown_path="001-Laws/raw_markdown/PD-1096/sample.md",
    )
    assert rc == 0

    refined = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "PD-1096" / "sample.md"
    manifest = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "PD-1096" / "sample.refined.json"

    assert refined.exists()
    assert manifest.exists()

    clean = refined.read_text(encoding="utf-8")
    assert "# SECTION 101 Title" in clean
    assert "## Sub" in clean
    assert "\x00" not in clean
    assert "\r" not in clean

    m = json.loads(manifest.read_text(encoding="utf-8"))
    assert m["source_relative_path"] == "001-Laws/raw_markdown/PD-1096/sample.md"
    assert m["rules_count"] >= 8
    assert isinstance(m["rules_applied"], list)
    assert m["manual_review"] is False
    assert m["chars_before"] > m["chars_after"]


def test_refine_one_inner_is_idempotent(tmp_path):
    conversion = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "raw_markdown"
    conversion.mkdir(parents=True)
    raw = conversion / "sample.md"
    raw.write_text("# Already clean\n\nBody.\n", encoding="utf-8")

    refine_one_inner(
        repo_root=tmp_path,
        relative_markdown_path="001-Laws/raw_markdown/sample.md",
    )
    refined = tmp_path / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown" / "sample.md"
    first = refined.read_bytes()

    refine_one_inner(
        repo_root=tmp_path,
        relative_markdown_path="001-Laws/raw_markdown/sample.md",
    )
    second = refined.read_bytes()
    assert first == second


def test_refine_one_inner_missing_source_returns_error(tmp_path):
    rc = refine_one_inner(
        repo_root=tmp_path,
        relative_markdown_path="nonexistent/raw_markdown/missing.md",
    )
    assert rc == 1
