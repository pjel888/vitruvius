from vitruvius.promotion import build_relationship_id, short_hash, build_promotion_batch_id


def test_build_relationship_id_is_deterministic():
    rid1 = build_relationship_id("law-pd-1096", "governs", "concept-fire-resistive-construction")
    rid2 = build_relationship_id("law-pd-1096", "governs", "concept-fire-resistive-construction")
    assert rid1 == rid2
    assert rid1.startswith("rel-")


def test_build_relationship_id_includes_predicate():
    rid = build_relationship_id("law-pd-1096", "requires", "concept-x")
    assert "requires" in rid


def test_short_hash_is_stable():
    assert short_hash("abc") == short_hash("abc")
    assert len(short_hash("abc")) == 8
    assert all(c in "0123456789abcdef" for c in short_hash("abc"))


def test_build_promotion_batch_id_shape():
    bid = build_promotion_batch_id()
    # 20260414T030000Z_a1b2c3d4
    parts = bid.split("_")
    assert len(parts) == 2
    assert parts[0].endswith("Z")
    assert len(parts[1]) == 8
