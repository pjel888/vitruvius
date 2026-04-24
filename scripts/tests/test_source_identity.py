from __future__ import annotations

from pathlib import Path

from vitruvius.source_identity import canonical_source_id_for_relative_path
from vitruvius.source_paths import logical_source_key_for_relative_path


def test_logical_source_key_ignores_conversion_representation() -> None:
    assert logical_source_key_for_relative_path(
        "001-Laws/raw_markdown/PD-1096/National Building Code.md"
    ) == logical_source_key_for_relative_path(
        "001-Laws/refined_markdown/PD-1096/National Building Code.md"
    )
    assert logical_source_key_for_relative_path(
        "001-Laws/sidecar_json/PD-1096/National Building Code.json"
    ) == logical_source_key_for_relative_path(
        "001-Laws/refined_markdown/PD-1096/National Building Code.md"
    )


def test_canonical_source_id_for_relative_path_maps_non_pd_laws(tmp_path: Path) -> None:
    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md",
            repo_root=tmp_path,
        )
        == "irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines"
    )
    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/BP-344/2024 Revised Implementing Rules and Regulations Batas Pambansa Blg. 344 _ National Council on Disability Affairs.md",
            repo_root=tmp_path,
        )
        == "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344"
    )
    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/BP-220/Revised_IRR_BP220_2008.md",
            repo_root=tmp_path,
        )
        == "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220"
    )


def test_canonical_source_id_for_relative_path_uses_explicit_repo_root(tmp_path: Path) -> None:
    sources_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    sources_dir.mkdir(parents=True)
    (sources_dir / "fire-code.md").write_text(
        "---\n"
        "id: law-fire-code-of-the-philippines\n"
        "source_relative_markdown_path: 001-Laws/refined_markdown/PD-1185/PD 1185 - Fire Code of the Philippines 1977.md\n"
        "---\n\n"
        "# Fire Code\n",
        encoding="utf-8",
    )

    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/PD-1185/PD 1185 - Fire Code of the Philippines 1977.md",
            repo_root=tmp_path,
        )
        == "law-fire-code-of-the-philippines"
    )


def test_canonical_source_id_for_relative_path_matches_raw_refined_existing_source(
    tmp_path: Path,
) -> None:
    sources_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    sources_dir.mkdir(parents=True)
    (sources_dir / "national-building-code.md").write_text(
        "---\n"
        "id: law-national-building-code-existing\n"
        "source_relative_markdown_path: 001-Laws/raw_markdown/PD-1096/National Building Code.md\n"
        "---\n\n"
        "# National Building Code\n",
        encoding="utf-8",
    )

    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/PD-1096/National Building Code.md",
            repo_root=tmp_path,
        )
        == "law-national-building-code-existing"
    )
