"""Stream S1.1 — Pydantic logic schema for neuro-symbolic bridge."""

from __future__ import annotations

import json

import pytest

from vitruvius.compound.logic_schema import LogicProof, LogicTriple


def test_logic_triple_round_trip() -> None:
    triple = LogicTriple(
        subject="building_42", predicate="violates", object="setback_rule_3"
    )
    payload = triple.model_dump_json()
    restored = LogicTriple.model_validate_json(payload)
    assert restored == triple
    assert json.loads(payload) == {
        "subject": "building_42",
        "predicate": "violates",
        "object": "setback_rule_3",
    }


def test_logic_proof_round_trip() -> None:
    proof = LogicProof(
        triples=[
            LogicTriple(
                subject="building_42", predicate="has_distance", object="1.8"
            ),
            LogicTriple(
                subject="setback_rule_3",
                predicate="requires_distance",
                object="2.0",
            ),
        ],
        conclusion="building_42 violates setback_rule_3",
    )
    payload = proof.model_dump_json()
    restored = LogicProof.model_validate_json(payload)
    assert restored == proof
    assert len(restored.triples) == 2
    assert restored.conclusion.endswith("setback_rule_3")


def test_logic_triple_rejects_empty_subject() -> None:
    with pytest.raises(ValueError):
        LogicTriple(subject="", predicate="violates", object="setback_rule_3")


def test_logic_triple_rejects_whitespace_only_predicate() -> None:
    with pytest.raises(ValueError):
        LogicTriple(subject="building_42", predicate="   ", object="rule_3")


def test_logic_triple_trims_whitespace() -> None:
    triple = LogicTriple(
        subject="  building_42  ",
        predicate="violates",
        object="\trule_3\n",
    )
    assert triple.subject == "building_42"
    assert triple.object == "rule_3"


def test_logic_proof_rejects_empty_triple_list() -> None:
    with pytest.raises(ValueError):
        LogicProof(triples=[], conclusion="building_42 ok")


def test_logic_proof_rejects_empty_conclusion() -> None:
    with pytest.raises(ValueError):
        LogicProof(
            triples=[
                LogicTriple(
                    subject="b", predicate="has_distance", object="1.0"
                )
            ],
            conclusion="",
        )
