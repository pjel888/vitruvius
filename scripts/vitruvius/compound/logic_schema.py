"""Stream S1.1 — Pydantic schema for LLM-emitted logic proofs.

The neuro-symbolic bridge forces LLM outputs into a structured Datalog
triple shape. The Rust evaluator in Stream S1.2 (``vitruvius_datalog_rs``)
consumes lists of :class:`LogicTriple` objects rendered as
``predicate(subject, object)`` strings. The schema is deliberately
minimal: we only need (subject, predicate, object) triples and an
overall conclusion string that the evaluator turns into a goal.

The strict field validation is the whole point — a free-form LLM
response will fail the round-trip and be rejected upstream. This is
the "firewall" referenced in the Sprint Z plan.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class LogicTriple(BaseModel):
    """A single Datalog-style fact: ``subject predicate object``.

    Every field is trimmed and required to be non-empty. Empty
    strings raise :class:`ValueError` so malformed LLM output is
    caught at parse time, before ever reaching the Rust evaluator.
    """

    subject: str = Field(
        ..., description="Datalog atom — no whitespace, lowercased"
    )
    predicate: str = Field(
        ..., description="Relation name from the Vitruvius logic ontology"
    )
    object: str = Field(..., description="Datalog atom — lowercased")

    @field_validator("subject", "predicate", "object")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("LogicTriple fields must be non-empty strings")
        return value.strip()


class LogicProof(BaseModel):
    """A bundle of triples the LLM claims prove a conclusion.

    Must contain at least one triple and a non-empty conclusion
    string. The conclusion is free-form text — the Rust evaluator
    parses the triples as facts and returns a Boolean verdict.
    """

    triples: list[LogicTriple] = Field(..., min_length=1)
    conclusion: str = Field(..., min_length=1)

    @field_validator("conclusion")
    @classmethod
    def _non_empty_conclusion(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("LogicProof.conclusion must be non-empty")
        return value.strip()
