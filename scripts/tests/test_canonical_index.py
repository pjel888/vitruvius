from vitruvius.promotion_validator import build_canonical_index


def test_builds_index_from_fixture(tmp_path):
    root = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
    (root / "sources").mkdir(parents=True)
    (root / "concepts").mkdir(parents=True)

    (root / "sources" / "pd-1096.md").write_text(
        "---\nid: law-pd-1096\ntitle: PD 1096\npage_type: source\n"
        "trust_level: primary\ncanonical_status: draft\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n# X\n",
        encoding="utf-8",
    )
    (root / "concepts" / "occupancy-classification.md").write_text(
        "---\nid: concept-occupancy-classification\ntitle: Occupancy Classification\n"
        "page_type: concept\ncanonical_status: placeholder\n"
        "last_canonicalized_utc: 2026-04-14T00:00:00Z\n---\n# Y\n",
        encoding="utf-8",
    )

    index = build_canonical_index(tmp_path)

    assert index["law-pd-1096"]["type"] == "source"
    assert index["law-pd-1096"]["canonical_status"] == "draft"
    assert index["concept-occupancy-classification"]["type"] == "concept"
    assert index["concept-occupancy-classification"]["canonical_status"] == "placeholder"


def test_empty_index_when_dirs_missing(tmp_path):
    assert build_canonical_index(tmp_path) == {}
