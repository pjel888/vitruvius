"""Sprint Z Stream S2 — Proposer/Inspector/Adjudicator adversarial swarm.

Three roles cooperate to harden a candidate relationship verdict:
  * Proposer: optimistic extractor — argues FOR keeping the candidate
  * Inspector: contrarian — argues AGAINST, hunts for contradictions
  * Adjudicator: tie-breaker — deterministic reconciler that picks the
    higher-confidence side, or falls back to a conservative reject on
    exact ties

Each role calls an :class:`~vitruvius.wiki.llm_client.LLMClient`
(test-stubbable). The Adjudicator is intentionally deterministic so
swarms are reproducible across runs.

The candidate dict shape matches the existing ``ollama_review.py``
contract::

    {
        "from": "concept-x",
        "type": "REQUIRES",
        "to": "concept-y",
        "examples": [{"text": "..."}],
        # plus optional: "occurrences", "sections", ...
    }

Stream flag: ``z_adversarial_swarm`` (defaults False). The module is
pure-Python and dependency-free — importing it has no side effects
and makes no network calls. Live LLM wiring lives at the call site.

Validation target from the governing plan: **Hallucination Capture
Rate ≥ 30%** — the ratio of candidates where the inspector
successfully overrides an optimistic proposer "keep" with a
high-confidence "reject".
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from vitruvius.wiki.llm_client import LLMClient


# ---------------------------------------------------------------------------
# Public data model
# ---------------------------------------------------------------------------
class SwarmRole(str, Enum):
    """The three cooperating roles in the adversarial swarm."""

    PROPOSER = "proposer"
    INSPECTOR = "inspector"
    ADJUDICATOR = "adjudicator"


#: Allowed decisions across every role. ``abstain`` is reserved for the
#: proposer/inspector when the LLM response is unparseable; the
#: adjudicator never emits abstain.
_ALLOWED_DECISIONS: frozenset[str] = frozenset({"keep", "reject", "abstain"})


@dataclass(frozen=True)
class RoleVerdict:
    """A single role's verdict on the candidate.

    Parameters
    ----------
    role:
        Which swarm role produced this verdict.
    decision:
        One of ``"keep"``, ``"reject"``, or ``"abstain"``.
    confidence:
        Clamped into the closed interval ``[0.0, 1.0]``.
    reason:
        Short human-readable rationale suitable for audit logs.
    """

    role: SwarmRole
    decision: str
    confidence: float
    reason: str

    def __post_init__(self) -> None:  # pragma: no cover - exercised indirectly
        if self.decision not in _ALLOWED_DECISIONS:
            raise ValueError(
                f"RoleVerdict.decision must be one of {sorted(_ALLOWED_DECISIONS)}; "
                f"got {self.decision!r}"
            )
        # Clamp confidence defensively — dataclass is frozen so use
        # object.__setattr__ to apply the clamp in-place.
        clamped = max(0.0, min(1.0, float(self.confidence)))
        if clamped != self.confidence:
            object.__setattr__(self, "confidence", clamped)


@dataclass(frozen=True)
class SwarmConsensus:
    """The final reconciled consensus across all three roles.

    Parameters
    ----------
    final_decision:
        ``"keep"`` or ``"reject"`` — the adjudicator never emits
        ``"abstain"`` so callers can treat this as a binary gate.
    contributing_verdicts:
        Tuple of every :class:`RoleVerdict` the orchestrator produced,
        in call order (proposer → inspector → adjudicator).
    hallucination_caught:
        ``True`` iff the inspector overrode an optimistic proposer
        ``"keep"`` with a high-confidence (> 0.7) ``"reject"``. This is
        the metric the governing plan tracks for the 30% Hallucination
        Capture Rate target.
    adjudication_reason:
        Short rationale from the adjudicator explaining how the tie
        was broken or why the roles agreed.
    """

    final_decision: str
    contributing_verdicts: tuple[RoleVerdict, ...]
    hallucination_caught: bool
    adjudication_reason: str


# ---------------------------------------------------------------------------
# Response parsing helpers
# ---------------------------------------------------------------------------
_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_llm_json(response: str) -> dict[str, Any]:
    """Extract a JSON object from a free-text LLM response.

    Returns an empty dict when nothing can be parsed — the calling
    role will then emit an ``abstain`` verdict. Accepts bare JSON,
    JSON wrapped in markdown fences, or JSON embedded in prose.
    """
    if not isinstance(response, str) or not response.strip():
        return {}
    match = _JSON_BLOCK_RE.search(response)
    if match is None:
        return {}
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return parsed


def _normalise_decision(raw: Any, *, allow_reject: bool = True) -> str:
    """Coerce a raw LLM decision field into the allowed vocabulary."""
    if not isinstance(raw, str):
        return "abstain"
    lowered = raw.strip().lower()
    if lowered in {"keep", "accept", "confirm", "true"}:
        return "keep"
    if allow_reject and lowered in {"reject", "deny", "contradict", "false"}:
        return "reject"
    if lowered == "reject" and not allow_reject:
        return "reject"
    return "abstain"


def _clamp_confidence(raw: Any, default: float = 0.0) -> float:
    """Clamp a raw confidence value into ``[0.0, 1.0]``."""
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(1.0, value))


def _candidate_signature(candidate: Mapping[str, Any]) -> str:
    """Return a compact ``from -> type -> to`` label for logging."""
    return (
        f"{candidate.get('from', '?')} -> "
        f"{candidate.get('type', '?')} -> "
        f"{candidate.get('to', '?')}"
    )


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------
def _build_proposer_prompt(candidate: Mapping[str, Any]) -> str:
    """Render the Proposer prompt — argues FOR keeping the candidate."""
    payload = {
        "role": "Proposer",
        "stance": "optimistic",
        "task": (
            "You are the Proposer in an adversarial review swarm. Argue FOR "
            "KEEPING the candidate relationship. Cite supporting evidence "
            "from the provided examples. Only emit 'reject' if the evidence "
            "flatly contradicts the candidate."
        ),
        "candidate": {
            "from": candidate.get("from"),
            "type": candidate.get("type"),
            "to": candidate.get("to"),
            "examples": list(candidate.get("examples", [])),
        },
        "output_schema": {
            "decision": "keep|reject|abstain",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation citing supporting evidence",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _build_inspector_prompt(
    candidate: Mapping[str, Any], proposer_verdict: RoleVerdict
) -> str:
    """Render the Inspector prompt — argues AGAINST the Proposer."""
    payload = {
        "role": "Inspector",
        "stance": "contrarian",
        "task": (
            "You are the Inspector in an adversarial review swarm. Your job "
            "is to find CONTRADICTIONS in the Proposer's argument below. "
            "Hunt for missing evidence, overreach, incorrect relationship "
            "type, and edge-case hallucinations. Only emit 'keep' if you "
            "cannot find any contradiction after careful scrutiny."
        ),
        "candidate": {
            "from": candidate.get("from"),
            "type": candidate.get("type"),
            "to": candidate.get("to"),
            "examples": list(candidate.get("examples", [])),
        },
        "proposer_argument": {
            "decision": proposer_verdict.decision,
            "confidence": proposer_verdict.confidence,
            "reason": proposer_verdict.reason,
        },
        "output_schema": {
            "decision": "keep|reject|abstain",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation citing contradictions or confirming lack of any",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Role runners
# ---------------------------------------------------------------------------
def run_proposer(
    *, candidate: Mapping[str, Any], llm_client: "LLMClient"
) -> RoleVerdict:
    """Run the Proposer role — optimistic extractor arguing FOR keeping.

    Parameters
    ----------
    candidate:
        The candidate relationship dict. Must contain at least ``from``,
        ``type``, and ``to``.
    llm_client:
        Any object conforming to the
        :class:`~vitruvius.wiki.llm_client.LLMClient` protocol. Tests
        pass a canned-response mock.
    """
    prompt = _build_proposer_prompt(candidate)
    try:
        response = llm_client.complete(prompt)
    except Exception as exc:  # pragma: no cover - defensive guard
        return RoleVerdict(
            role=SwarmRole.PROPOSER,
            decision="abstain",
            confidence=0.0,
            reason=f"Proposer LLM call failed: {exc}",
        )
    parsed = _parse_llm_json(response)
    decision = _normalise_decision(parsed.get("decision"))
    confidence = _clamp_confidence(parsed.get("confidence"))
    reason = parsed.get("reason") or (
        f"Proposer abstained on {_candidate_signature(candidate)} "
        "because the response was unparseable."
        if decision == "abstain"
        else f"Proposer argued '{decision}' for {_candidate_signature(candidate)}."
    )
    return RoleVerdict(
        role=SwarmRole.PROPOSER,
        decision=decision,
        confidence=confidence,
        reason=str(reason),
    )


def run_inspector(
    *,
    candidate: Mapping[str, Any],
    proposer_verdict: RoleVerdict,
    llm_client: "LLMClient",
) -> RoleVerdict:
    """Run the Inspector role — contrarian hunting for contradictions.

    Parameters
    ----------
    candidate:
        The candidate relationship dict.
    proposer_verdict:
        The Proposer's verdict, forwarded into the prompt so the
        Inspector has something concrete to attack.
    llm_client:
        Any :class:`~vitruvius.wiki.llm_client.LLMClient`-conformant
        object. Tests pass a canned-response mock.
    """
    prompt = _build_inspector_prompt(candidate, proposer_verdict)
    try:
        response = llm_client.complete(prompt)
    except Exception as exc:  # pragma: no cover - defensive guard
        return RoleVerdict(
            role=SwarmRole.INSPECTOR,
            decision="abstain",
            confidence=0.0,
            reason=f"Inspector LLM call failed: {exc}",
        )
    parsed = _parse_llm_json(response)
    decision = _normalise_decision(parsed.get("decision"))
    confidence = _clamp_confidence(parsed.get("confidence"))
    reason = parsed.get("reason") or (
        f"Inspector abstained on {_candidate_signature(candidate)} "
        "because the response was unparseable."
        if decision == "abstain"
        else f"Inspector returned '{decision}' for {_candidate_signature(candidate)}."
    )
    return RoleVerdict(
        role=SwarmRole.INSPECTOR,
        decision=decision,
        confidence=confidence,
        reason=str(reason),
    )


def run_adjudicator(
    *,
    candidate: Mapping[str, Any],
    proposer: RoleVerdict,
    inspector: RoleVerdict,
) -> RoleVerdict:
    """Run the deterministic Adjudicator role.

    Decision rules (applied in order):

    1. If Proposer and Inspector agree, pass that decision through with
       the arithmetic mean of their confidences.
    2. If they disagree, pick the side with strictly higher confidence.
    3. On an exact confidence tie, conservatively pick ``"reject"``.
    4. If either side abstains and the other does not, adopt the
       non-abstaining side's decision and confidence.
    5. If both sides abstain, emit ``"reject"`` with zero confidence.

    The Adjudicator never calls an LLM; the outcome is a pure function
    of the two inputs so swarms are reproducible.
    """
    signature = _candidate_signature(candidate)

    proposer_abstain = proposer.decision == "abstain"
    inspector_abstain = inspector.decision == "abstain"

    # Rule 5 — both abstained
    if proposer_abstain and inspector_abstain:
        return RoleVerdict(
            role=SwarmRole.ADJUDICATOR,
            decision="reject",
            confidence=0.0,
            reason=(
                f"Adjudicator rejected {signature} because both Proposer and "
                "Inspector abstained — no confident verdict available."
            ),
        )

    # Rule 4 — one abstained, one did not
    if proposer_abstain and not inspector_abstain:
        return RoleVerdict(
            role=SwarmRole.ADJUDICATOR,
            decision=inspector.decision,
            confidence=inspector.confidence,
            reason=(
                f"Adjudicator deferred to Inspector for {signature} "
                "because the Proposer abstained."
            ),
        )
    if inspector_abstain and not proposer_abstain:
        return RoleVerdict(
            role=SwarmRole.ADJUDICATOR,
            decision=proposer.decision,
            confidence=proposer.confidence,
            reason=(
                f"Adjudicator deferred to Proposer for {signature} "
                "because the Inspector abstained."
            ),
        )

    # Rule 1 — agreement
    if proposer.decision == inspector.decision:
        avg_conf = (proposer.confidence + inspector.confidence) / 2.0
        return RoleVerdict(
            role=SwarmRole.ADJUDICATOR,
            decision=proposer.decision,
            confidence=avg_conf,
            reason=(
                f"Adjudicator confirmed '{proposer.decision}' for {signature} — "
                f"Proposer ({proposer.confidence:.2f}) and Inspector "
                f"({inspector.confidence:.2f}) agreed."
            ),
        )

    # Rule 2/3 — disagreement
    if proposer.confidence > inspector.confidence:
        return RoleVerdict(
            role=SwarmRole.ADJUDICATOR,
            decision=proposer.decision,
            confidence=proposer.confidence,
            reason=(
                f"Adjudicator sided with Proposer '{proposer.decision}' for "
                f"{signature} over Inspector '{inspector.decision}' "
                f"({proposer.confidence:.2f} > {inspector.confidence:.2f})."
            ),
        )
    if inspector.confidence > proposer.confidence:
        return RoleVerdict(
            role=SwarmRole.ADJUDICATOR,
            decision=inspector.decision,
            confidence=inspector.confidence,
            reason=(
                f"Adjudicator sided with Inspector '{inspector.decision}' for "
                f"{signature} over Proposer '{proposer.decision}' "
                f"({inspector.confidence:.2f} > {proposer.confidence:.2f})."
            ),
        )

    # Rule 3 — exact tie breaks toward conservative reject
    return RoleVerdict(
        role=SwarmRole.ADJUDICATOR,
        decision="reject",
        confidence=proposer.confidence,  # == inspector.confidence
        reason=(
            f"Adjudicator broke a confidence tie on {signature} by rejecting "
            "conservatively (Proposer and Inspector disagreed at equal confidence)."
        ),
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
def run_swarm(
    *, candidate: Mapping[str, Any], llm_client: "LLMClient"
) -> SwarmConsensus:
    """Run the full Proposer → Inspector → Adjudicator pipeline.

    Calls the three roles in sequence and returns a
    :class:`SwarmConsensus` summarising the outcome. Sets
    ``hallucination_caught=True`` iff the inspector rejected (with
    confidence > 0.7) a candidate that the proposer wanted to keep —
    that is the hallucination-override signal the governing plan
    tracks to meet the 30% Hallucination Capture Rate target.

    Parameters
    ----------
    candidate:
        The candidate relationship dict.
    llm_client:
        A shared :class:`~vitruvius.wiki.llm_client.LLMClient` used for
        both the Proposer and Inspector calls. The Adjudicator does
        not use the client (it is deterministic).
    """
    proposer_verdict = run_proposer(candidate=candidate, llm_client=llm_client)
    inspector_verdict = run_inspector(
        candidate=candidate,
        proposer_verdict=proposer_verdict,
        llm_client=llm_client,
    )
    adjudicator_verdict = run_adjudicator(
        candidate=candidate,
        proposer=proposer_verdict,
        inspector=inspector_verdict,
    )

    hallucination_caught = (
        proposer_verdict.decision == "keep"
        and inspector_verdict.decision == "reject"
        and inspector_verdict.confidence > 0.7
    )

    return SwarmConsensus(
        final_decision=adjudicator_verdict.decision,
        contributing_verdicts=(
            proposer_verdict,
            inspector_verdict,
            adjudicator_verdict,
        ),
        hallucination_caught=hallucination_caught,
        adjudication_reason=adjudicator_verdict.reason,
    )


__all__ = [
    "SwarmRole",
    "RoleVerdict",
    "SwarmConsensus",
    "run_proposer",
    "run_inspector",
    "run_adjudicator",
    "run_swarm",
]
