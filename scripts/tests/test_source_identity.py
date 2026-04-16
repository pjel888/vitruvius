from __future__ import annotations

from vitruvius.source_identity import canonical_source_id_for_relative_path


def test_canonical_source_id_for_relative_path_maps_non_pd_laws() -> None:
    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/RA-9514/RA9514-RIRR-rev-2019.md"
        )
        == "irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines"
    )
    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/BP-344/2024 Revised Implementing Rules and Regulations Batas Pambansa Blg. 344 _ National Council on Disability Affairs.md"
        )
        == "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344"
    )
    assert (
        canonical_source_id_for_relative_path(
            "001-Laws/refined_markdown/BP-220/Revised_IRR_BP220_2008.md"
        )
        == "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220"
    )
