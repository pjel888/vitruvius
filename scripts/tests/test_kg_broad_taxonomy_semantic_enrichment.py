from __future__ import annotations

import json
from pathlib import Path

from vitruvius.kg.broad_taxonomy_semantic_enrichment import (
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


def test_broad_taxonomy_enrichment_is_idempotent_on_admitted_fixture() -> None:
    payload = _payload()

    enriched, report = enrich(payload)

    assert report["ok"] is True
    assert report["added_non_architecture_real_l4_count"] == 0
    assert report["already_enriched_non_architecture_l3_parent_count"] == 1247
    assert len(enriched["records"]) == len(payload["records"])
    assert len(enriched["relationships"]) == len(payload["relationships"])


def test_broad_taxonomy_fixture_has_no_l4_scaffold_labels() -> None:
    payload = _payload()
    l4_records = [record for record in payload["records"] if record["level"] == 4]
    broad_records = [
        record
        for record in l4_records
        if record.get("generation_method") == GENERATION_METHOD
    ]

    assert len(broad_records) == 6240
    assert not [
        record["path_code"]
        for record in l4_records
        if record["label"].endswith(PLACEHOLDER_SUFFIXES)
    ]
    root_counts: dict[str, int] = {}
    parent_counts: dict[str, int] = {}
    for record in broad_records:
        root = record["path_code"].split(".")[0]
        root_counts[root] = root_counts.get(root, 0) + 1
        parent_counts[record["parent_path_code"]] = (
            parent_counts.get(record["parent_path_code"], 0) + 1
        )

    assert len(root_counts) == 23
    assert root_counts["LAW"] == 450
    assert root_counts["HIS"] == 550
    assert len(parent_counts) == 1248
    assert set(parent_counts.values()) == {5}
