from __future__ import annotations

import json
from pathlib import Path

from vitruvius.kg.architecture_taxonomy_enrichment import (
    GENERATION_METHOD,
    PLACEHOLDER_SUFFIXES,
    enrich,
)

FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "aec_mepfs_backbone"
    / "admitted_backbone_nodes_l1_l2.json"
)


def _payload() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_architecture_enrichment_is_idempotent_on_admitted_fixture() -> None:
    payload = _payload()

    enriched, report = enrich(payload)

    assert report["ok"] is True
    assert report["added_architecture_real_l4_count"] == 0
    assert report["already_enriched_architecture_l3_parent_count"] == 146
    assert len(enriched["records"]) == len(payload["records"])
    assert len(enriched["relationships"]) == len(payload["relationships"])


def test_architecture_enrichment_fixture_has_no_arc_l4_scaffold_labels() -> None:
    payload = _payload()
    arc_l4 = [
        record
        for record in payload["records"]
        if record["path_code"].startswith("ARC") and record["level"] == 4
    ]

    assert len(arc_l4) == 976
    assert not [
        record["path_code"]
        for record in arc_l4
        if record["label"].endswith((*PLACEHOLDER_SUFFIXES, " Topics"))
    ]
    assert sum(
        1 for record in arc_l4 if record.get("generation_method") == GENERATION_METHOD
    ) == 878
    assert {
        "ARC.REG.SGP.SPC",
        "ARC.PRC.LEG.SSA",
        "ARC.COD.BCA.OCR",
        "ARC.HIS.SEA.BKS",
        "ARC.WAC.MSW.GRV",
        "ARC.DTS.CPT.VFU",
    } <= {record["path_code"] for record in arc_l4}
