"""Sprint CLEANUP-1 Stream C4 — Phase 5E LLM candidate proposer.

Proposes relationship candidates via a local Ollama call. Output conforms
to the closed predicate vocabulary at scripts/vitruvius/rules/relationship_registry.yaml.

Gated behind `p5e_llm_extraction`. Flag-off is a strict no-op (no Ollama
call, empty list returned).

Perf call: orchestration + Ollama HTTP + JSON parse. Above the Rust Line
per AD-036. Python is the correct choice — moving this to Rust would gain
nothing because the bottleneck is the LLM call itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


ALLOWED_PREDICATES = frozenset(
    {"governs", "defines", "requires", "depends_on", "limits", "affects", "supersedes"}
)


@dataclass(frozen=True)
class ProposedCandidate:
    from_id: str
    predicate: str
    to_id: str
    evidence: str
    confidence: float
    source: str = "llm_proposer"  # distinguishes from regex candidates in merge


def _load_prompt_template() -> str:
    """Load the Phase 5E prompt template from .ai/08_prompts/."""
    from vitruvius.paths import get_repo_root

    prompt_path = (
        get_repo_root() / ".ai" / "08_prompts" / "gemma-phase-5e-proposer.txt"
    )
    return prompt_path.read_text(encoding="utf-8")


def _build_prompt(*, section_text: str, section_id: str, source_id: str) -> str:
    """Compose the final prompt payload — prepend the template + JSON input block."""
    template = _load_prompt_template()
    input_block = (
        f"\n\nINPUT SECTION ID: {section_id}\n"
        f"INPUT SOURCE ID: {source_id}\n"
        f"INPUT TEXT:\n\"\"\"\n{section_text}\n\"\"\"\n"
        f"\nYour response must be a JSON array only. Do not include explanation."
    )
    return template + input_block


def _call_ollama(
    *,
    prompt: str,
    model: str,
    timeout_seconds: int,
) -> str:
    """Thin wrapper around the Ollama /api/generate endpoint.

    Kept as a module-level function so tests can monkeypatch it.
    Reuses the Vitruvius config for the Ollama URL.
    """
    import urllib.request
    import json

    from vitruvius.config import load_config

    cfg = load_config()
    url = cfg.get("review", {}).get("ollama", {}).get(
        "url", "http://127.0.0.1:11434"
    )

    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "temperature": 0,
            "num_predict": 400,
            "format": "json",
            "stream": False,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        f"{url}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("response", "")


def propose_relationships_llm(
    *,
    section_text: str,
    section_id: str,
    source_id: str,
    model: str = "gemma4:31b",
    timeout_seconds: int = 120,
) -> List[ProposedCandidate]:
    """Call Ollama to propose relationship candidates for a single section.

    Returns an empty list on any error. The fallback-to-regex behavior is the
    safety net — a broken LLM path never fails the pipeline, it just produces
    no proposer output.
    """
    import json

    try:
        prompt = _build_prompt(
            section_text=section_text,
            section_id=section_id,
            source_id=source_id,
        )
        raw_response = _call_ollama(
            prompt=prompt, model=model, timeout_seconds=timeout_seconds
        )
    except Exception:
        return []

    try:
        parsed = json.loads(raw_response)
    except (json.JSONDecodeError, ValueError):
        return []

    if not isinstance(parsed, list):
        return []

    candidates: List[ProposedCandidate] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        predicate = item.get("type")
        if predicate not in ALLOWED_PREDICATES:
            continue  # reject contract violations
        from_id = item.get("from")
        to_id = item.get("to")
        evidence = item.get("evidence", "")
        confidence = item.get("confidence", 0.0)
        if not isinstance(from_id, str) or not isinstance(to_id, str):
            continue
        if not isinstance(evidence, str):
            continue
        try:
            confidence_f = max(0.0, min(1.0, float(confidence)))
        except (TypeError, ValueError):
            confidence_f = 0.0
        candidates.append(
            ProposedCandidate(
                from_id=from_id,
                predicate=predicate,
                to_id=to_id,
                evidence=evidence[:200],
                confidence=confidence_f,
            )
        )

    return candidates
