from pathlib import Path

import yaml

from vitruvius.promotion_validator import (
    ValidationResult,
    build_canonical_index,
    normalize_relationship_trust,
    relationship_trust_metadata,
    validate_promotion_record,
)


FIXTURE = Path(__file__).parent / "fixtures" / "valid_record.yaml"


def load_valid():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def canonical_index():
    return {
        "law-pd-1096": {"type": "source", "canonical_status": "draft", "trust_level": "primary"},
        "concept-fire-resistive-construction": {
            "type": "concept", "canonical_status": "draft", "trust_level": None,
        },
        "concept-occupancy-classification": {
            "type": "concept", "canonical_status": "draft", "trust_level": None,
        },
    }


def test_normalize_relationship_trust_maps_unknown_to_unverified():
    assert normalize_relationship_trust("unknown") == "unverified"
    assert normalize_relationship_trust(None) == "unverified"
    assert normalize_relationship_trust("primary") == "primary"


def test_relationship_trust_metadata_preserves_raw_value():
    metadata = relationship_trust_metadata("unknown")

    assert metadata["trust_level"] == "unverified"
    assert metadata["raw_trust_level"] == "unknown"
    assert metadata["trust_level_was_normalized"] is True


def test_build_canonical_index_normalizes_unknown_source_trust(tmp_path):
    sources = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    concepts = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    sources.mkdir(parents=True)
    concepts.mkdir(parents=True)
    (sources / "law-x.md").write_text(
        "---\nid: law-x\ncanonical_status: draft\ntrust_level: unknown\n---\n",
        encoding="utf-8",
    )
    (concepts / "concept-y.md").write_text(
        "---\nid: concept-y\ncanonical_status: draft\n---\n",
        encoding="utf-8",
    )

    index = build_canonical_index(tmp_path)

    assert index["law-x"]["trust_level"] == "unverified"
    assert index["law-x"]["raw_trust_level"] == "unknown"
    assert index["law-x"]["trust_level_was_normalized"] is True
    assert index["concept-y"]["trust_level"] == "unverified"
    assert index["concept-y"]["raw_trust_level"] is None
    assert index["concept-y"]["trust_level_was_normalized"] is True


def registry():
    from vitruvius.promotion_validator import load_registry
    return load_registry()


# ---------- happy path ----------

def test_valid_record_passes():
    result = validate_promotion_record(load_valid(), registry(), canonical_index())
    assert result.passed, f"Unexpected errors: {result.errors}"
    assert result.errors == []


# ---------- structural rules 1-6 ----------

def test_rule_2_invalid_id_format():
    rec = load_valid()
    rec["id"] = "REL-BAD"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("id" in e.lower() for e in result.errors)


def test_rule_3_wrong_page_type():
    rec = load_valid()
    rec["page_type"] = "source"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("page_type" in e for e in result.errors)


def test_rule_4_unknown_predicate():
    rec = load_valid()
    rec["relationship_type"] = "frobnicates"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("frobnicates" in e for e in result.errors)


def test_rule_5_unknown_from_entity():
    rec = load_valid()
    rec["from_entity"] = "concept-does-not-exist"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("from_entity" in e for e in result.errors)


def test_rule_6_empty_evidence():
    rec = load_valid()
    rec["evidence"] = []
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("evidence" in e.lower() for e in result.errors)


# ---------- registry compatibility rule 7 ----------

def test_rule_7_incompatible_pair():
    rec = load_valid()
    # governs requires source->concept, not concept->concept
    rec["from_entity"] = "concept-occupancy-classification"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("compatibility" in e.lower() or "pair" in e.lower() for e in result.errors)


# ---------- evidence integrity rules 8-12 ----------

def test_rule_8_missing_source_section_id():
    rec = load_valid()
    rec["evidence"][0]["source_section_id"] = None
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("source_section_id" in e for e in result.errors)


def test_rule_9_empty_snippet():
    rec = load_valid()
    rec["evidence"][0]["evidence_snippet"] = ""
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("snippet" in e.lower() for e in result.errors)


def test_rule_10_evidence_source_not_in_index():
    rec = load_valid()
    rec["evidence"][0]["source_id"] = "law-mystery"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("source_id" in e for e in result.errors)


def test_rule_11_confidence_out_of_range():
    rec = load_valid()
    rec["evidence"][0]["reviewer_confidence"] = 1.5
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("confidence" in e.lower() for e in result.errors)


def test_rule_12_non_keep_decision():
    rec = load_valid()
    rec["evidence"][0]["review_decision"] = "review_further"
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("review_decision" in e or "keep" in e for e in result.errors)


# ---------- promotion threshold rule 13 ----------

def test_rule_13_below_threshold():
    rec = load_valid()
    rec["confidence_score"] = 0.80
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("threshold" in e.lower() or "0.90" in e for e in result.errors)


# ---------- trust propagation rule 14 ----------

def test_rule_14_trust_level_mismatch():
    rec = load_valid()
    rec["trust_level"] = "tertiary"  # actual min is primary
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("trust" in e.lower() for e in result.errors)


# ---------- audit integrity rules 15-16 ----------

def test_rule_15_missing_batch_id():
    rec = load_valid()
    rec["promotion_batch_id"] = ""
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("promotion_batch_id" in e for e in result.errors)


def test_rule_16_missing_last_promoted_utc():
    rec = load_valid()
    rec["last_promoted_utc"] = ""
    result = validate_promotion_record(rec, registry(), canonical_index())
    assert not result.passed
    assert any("last_promoted_utc" in e for e in result.errors)


# ---------- referential integrity rule 17 ----------

def test_rule_17_placeholder_endpoint_rejected():
    rec = load_valid()
    idx = canonical_index()
    idx["concept-fire-resistive-construction"]["canonical_status"] = "placeholder"
    result = validate_promotion_record(rec, registry(), idx)
    assert not result.passed
    assert any("placeholder" in e.lower() for e in result.errors)
