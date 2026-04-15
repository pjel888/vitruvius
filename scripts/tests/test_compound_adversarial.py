"""Sprint Z Stream S2 — tests for the Proposer/Inspector/Adjudicator swarm.

Policy: these tests MUST NOT make live Ollama calls. Every test injects
a tiny ``_MockLLM`` that returns canned responses based on whether the
prompt came from the Proposer or the Inspector role. Running these
tests with ``OLLAMA_HOST=unreachable`` (or no network at all) must
still pass.
"""

from __future__ import annotations

import pytest

from vitruvius.compound.adversarial import (
    RoleVerdict,
    SwarmConsensus,
    SwarmRole,
    run_adjudicator,
    run_inspector,
    run_proposer,
    run_swarm,
)


# ---------------------------------------------------------------------------
# Mock LLM
# ---------------------------------------------------------------------------
class _MockLLM:
    """Canned-response LLM client for swarm tests.

    Sniffs the ``role`` field inside the prompt to decide whether to
    return the Proposer-side or Inspector-side canned response.
    Recording ``prompts`` for assertions lets tests verify the
    orchestrator called the right roles in the right order.
    """

    def __init__(
        self,
        *,
        proposer_response: str,
        inspector_response: str,
    ) -> None:
        self.proposer_response = proposer_response
        self.inspector_response = inspector_response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if '"role": "Proposer"' in prompt:
            return self.proposer_response
        if '"role": "Inspector"' in prompt:
            return self.inspector_response
        raise AssertionError(
            "Prompt did not carry a recognisable role header; this mock "
            "only handles Proposer or Inspector prompts."
        )


_CANDIDATE = {
    "from": "building-permit",
    "type": "REQUIRES",
    "to": "environmental-clearance",
    "examples": [
        {"text": "§5.1 — a building permit shall only issue after ECC."}
    ],
    "occurrences": 2,
    "sections": ["§5.1"],
}


# ---------------------------------------------------------------------------
# Case 1 — Proposer basic shape
# ---------------------------------------------------------------------------
def test_proposer_returns_role_verdict() -> None:
    """A well-formed LLM response should produce a PROPOSER RoleVerdict
    with a clamped confidence in the closed interval [0, 1]."""
    llm = _MockLLM(
        proposer_response=(
            '{"decision": "keep", "confidence": 0.82, '
            '"reason": "§5.1 explicitly binds the two concepts."}'
        ),
        inspector_response="{}",  # unused in this test
    )

    verdict = run_proposer(candidate=_CANDIDATE, llm_client=llm)

    assert isinstance(verdict, RoleVerdict)
    assert verdict.role is SwarmRole.PROPOSER
    assert verdict.decision == "keep"
    assert 0.0 <= verdict.confidence <= 1.0
    assert verdict.confidence == pytest.approx(0.82)
    assert "§5.1" in verdict.reason
    # Proposer prompt must have been sent exactly once
    assert len(llm.prompts) == 1
    assert '"role": "Proposer"' in llm.prompts[0]


# ---------------------------------------------------------------------------
# Case 2 — Inspector finds contradictions and rejects
# ---------------------------------------------------------------------------
def test_inspector_disagrees_lowers_confidence_or_rejects() -> None:
    """When the Inspector finds contradictions it must emit a reject
    verdict (not silently accept the Proposer's argument)."""
    proposer_verdict = RoleVerdict(
        role=SwarmRole.PROPOSER,
        decision="keep",
        confidence=0.9,
        reason="§5.1 supports this.",
    )
    llm = _MockLLM(
        proposer_response="{}",  # unused — we call run_inspector directly
        inspector_response=(
            '{"decision": "reject", "confidence": 0.88, '
            '"reason": "§5.1 actually says the permit precedes ECC, not the reverse. '
            "The Proposer's argument inverts the dependency."
            '"}'
        ),
    )

    verdict = run_inspector(
        candidate=_CANDIDATE,
        proposer_verdict=proposer_verdict,
        llm_client=llm,
    )

    assert isinstance(verdict, RoleVerdict)
    assert verdict.role is SwarmRole.INSPECTOR
    assert verdict.decision == "reject"
    assert verdict.confidence == pytest.approx(0.88)
    assert "inverts" in verdict.reason or "precedes" in verdict.reason
    assert len(llm.prompts) == 1
    assert '"role": "Inspector"' in llm.prompts[0]


# ---------------------------------------------------------------------------
# Case 3 — Adjudicator passes through agreement
# ---------------------------------------------------------------------------
def test_adjudicator_agreement_passes_through() -> None:
    """When Proposer and Inspector agree, the Adjudicator should pass
    the agreed decision through with the mean of their confidences."""
    proposer = RoleVerdict(
        role=SwarmRole.PROPOSER,
        decision="keep",
        confidence=0.8,
        reason="Proposer keeps.",
    )
    inspector = RoleVerdict(
        role=SwarmRole.INSPECTOR,
        decision="keep",
        confidence=0.6,
        reason="Inspector concurs.",
    )

    verdict = run_adjudicator(
        candidate=_CANDIDATE, proposer=proposer, inspector=inspector
    )

    assert verdict.role is SwarmRole.ADJUDICATOR
    assert verdict.decision == "keep"
    assert verdict.confidence == pytest.approx(0.7)  # (0.8 + 0.6) / 2
    assert "agreed" in verdict.reason.lower() or "confirmed" in verdict.reason.lower()


# ---------------------------------------------------------------------------
# Case 4 — Adjudicator picks higher confidence on disagreement
# ---------------------------------------------------------------------------
def test_adjudicator_disagreement_picks_higher_confidence() -> None:
    """When Proposer and Inspector disagree, the higher-confidence side wins.
    Proposer keep@0.9 vs Inspector reject@0.6 → final should be keep."""
    proposer = RoleVerdict(
        role=SwarmRole.PROPOSER,
        decision="keep",
        confidence=0.9,
        reason="Strong supporting evidence.",
    )
    inspector = RoleVerdict(
        role=SwarmRole.INSPECTOR,
        decision="reject",
        confidence=0.6,
        reason="Weaker contradictions.",
    )

    verdict = run_adjudicator(
        candidate=_CANDIDATE, proposer=proposer, inspector=inspector
    )

    assert verdict.role is SwarmRole.ADJUDICATOR
    assert verdict.decision == "keep"
    assert verdict.confidence == pytest.approx(0.9)
    assert "proposer" in verdict.reason.lower()


# ---------------------------------------------------------------------------
# Case 5 — Adjudicator tie-breaks toward reject
# ---------------------------------------------------------------------------
def test_adjudicator_tie_breaks_toward_reject() -> None:
    """On an exact confidence tie between keep and reject the Adjudicator
    must conservatively reject (hallucination prevention)."""
    proposer = RoleVerdict(
        role=SwarmRole.PROPOSER,
        decision="keep",
        confidence=0.8,
        reason="Proposer keep at 0.8.",
    )
    inspector = RoleVerdict(
        role=SwarmRole.INSPECTOR,
        decision="reject",
        confidence=0.8,
        reason="Inspector reject at 0.8.",
    )

    verdict = run_adjudicator(
        candidate=_CANDIDATE, proposer=proposer, inspector=inspector
    )

    assert verdict.role is SwarmRole.ADJUDICATOR
    assert verdict.decision == "reject"
    assert "conservatively" in verdict.reason.lower() or "tie" in verdict.reason.lower()


# ---------------------------------------------------------------------------
# Case 6 — End-to-end hallucination_caught signal
# ---------------------------------------------------------------------------
def test_run_swarm_sets_hallucination_caught_when_inspector_overrides_keep() -> None:
    """End-to-end: Proposer argues keep@0.9, Inspector overrides with
    reject@0.85 (> 0.7 threshold) → hallucination_caught must be True
    AND final_decision must be reject because 0.85 > 0.9 is False,
    but the spec says the override raises the hallucination flag
    regardless of which side actually wins the adjudication."""
    llm = _MockLLM(
        proposer_response=(
            '{"decision": "keep", "confidence": 0.9, '
            '"reason": "Optimistic reading of §5.1."}'
        ),
        inspector_response=(
            '{"decision": "reject", "confidence": 0.85, '
            '"reason": "The Proposer misread the ordering of the clauses."}'
        ),
    )

    consensus = run_swarm(candidate=_CANDIDATE, llm_client=llm)

    assert isinstance(consensus, SwarmConsensus)
    # Three contributing verdicts in call order
    assert len(consensus.contributing_verdicts) == 3
    roles = [v.role for v in consensus.contributing_verdicts]
    assert roles == [SwarmRole.PROPOSER, SwarmRole.INSPECTOR, SwarmRole.ADJUDICATOR]
    # Hallucination override signal
    assert consensus.hallucination_caught is True
    # Adjudicator picks the higher-confidence side (Proposer@0.9 > Inspector@0.85)
    # so final_decision is "keep" — but the hallucination flag still
    # fires because the inspector met the override criteria. This is
    # the audit signal the governing plan tracks.
    assert consensus.final_decision == "keep"
    # The proposer and inspector prompts should each have been sent once
    assert len(llm.prompts) == 2
    assert '"role": "Proposer"' in llm.prompts[0]
    assert '"role": "Inspector"' in llm.prompts[1]


# ---------------------------------------------------------------------------
# Case 7 — Inspector override low confidence does NOT flag hallucination
# ---------------------------------------------------------------------------
def test_run_swarm_no_hallucination_flag_when_inspector_confidence_too_low() -> None:
    """An Inspector reject with confidence <= 0.7 must NOT set the
    hallucination_caught flag — the governing plan requires a high-
    confidence override to count toward the 30% capture rate."""
    llm = _MockLLM(
        proposer_response=(
            '{"decision": "keep", "confidence": 0.9, "reason": "Looks fine."}'
        ),
        inspector_response=(
            '{"decision": "reject", "confidence": 0.5, '
            '"reason": "Weak contradiction, not sure."}'
        ),
    )

    consensus = run_swarm(candidate=_CANDIDATE, llm_client=llm)

    assert consensus.hallucination_caught is False
    assert consensus.final_decision == "keep"  # higher confidence wins


# ---------------------------------------------------------------------------
# Case 8 — Confidence clamping
# ---------------------------------------------------------------------------
def test_proposer_clamps_out_of_range_confidence() -> None:
    """If the LLM returns a confidence outside [0, 1], the Proposer must
    clamp it rather than propagate the invalid value."""
    llm = _MockLLM(
        proposer_response=(
            '{"decision": "keep", "confidence": 1.7, "reason": "Overconfident."}'
        ),
        inspector_response="{}",
    )

    verdict = run_proposer(candidate=_CANDIDATE, llm_client=llm)

    assert verdict.confidence == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Case 9 — Unparseable response yields abstain
# ---------------------------------------------------------------------------
def test_proposer_abstains_on_unparseable_response() -> None:
    """A response that does not contain JSON should produce an abstain
    verdict — never a silent keep."""
    llm = _MockLLM(
        proposer_response="I am just a wandering narrative with no JSON inside.",
        inspector_response="{}",
    )

    verdict = run_proposer(candidate=_CANDIDATE, llm_client=llm)

    assert verdict.decision == "abstain"
    assert verdict.confidence == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Case 10 — Adjudicator defers to non-abstaining side when one abstains
# ---------------------------------------------------------------------------
def test_adjudicator_defers_to_non_abstaining_side() -> None:
    """When one side abstains and the other does not, the Adjudicator
    must adopt the non-abstaining side's decision."""
    proposer = RoleVerdict(
        role=SwarmRole.PROPOSER,
        decision="abstain",
        confidence=0.0,
        reason="Unparseable Proposer.",
    )
    inspector = RoleVerdict(
        role=SwarmRole.INSPECTOR,
        decision="reject",
        confidence=0.72,
        reason="Clear contradiction in §5.1.",
    )

    verdict = run_adjudicator(
        candidate=_CANDIDATE, proposer=proposer, inspector=inspector
    )

    assert verdict.decision == "reject"
    assert verdict.confidence == pytest.approx(0.72)
    assert "proposer abstained" in verdict.reason.lower()
