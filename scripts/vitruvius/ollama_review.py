from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .config import (
    get_ollama_default_model,
    get_ollama_default_timeout,
    get_ollama_url,
)
from .paths import get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


DEFAULT_MODEL = get_ollama_default_model()
DEFAULT_TIMEOUT_SECONDS = get_ollama_default_timeout()


def load_relationship_report() -> dict[str, Any]:
    repo_root = get_repo_root()
    path = repo_root / "006_System-Manifests" / "runs" / "latest_relationship_extraction_sections.json"

    if not path.exists():
        raise FileNotFoundError(
            f"Relationship extraction report not found: {path}. "
            "Run extract-relationships-sections-one first."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def _fuse_verdicts_via_choquet(signals: dict[str, float]) -> float:
    """Stream W2.6 — fuse multi-source confidence signals into a single
    aggregate score.

    Flag-OFF path returns the arithmetic mean of the signal values so
    byte-identity holds when callers were already averaging. Flag-ON
    path calls the Stream F.8 Choquet integral scaffold.
    """
    from . import config as cfgmod
    if not cfgmod._features_block().get("w_review_choquet_aggregator", False):
        values = [float(v) for v in signals.values()]
        return sum(values) / len(values) if values else 0.0

    from .review.choquet_aggregator import (
        Signal,
        additive_measure,
        choquet_integral,
    )

    signal_list = [Signal(name=k, value=float(v)) for k, v in signals.items()]
    measure = additive_measure([s.name for s in signal_list])
    result = choquet_integral(signal_list, fuzzy_measure=measure)
    return float(result.aggregate)


def _capture_tension_and_reflection(
    *,
    primary: dict[str, Any],
    second_pass: dict[str, Any] | None,
) -> dict[str, Any]:
    """Stream W2.5 — annotate a verdict with reflection confidence and
    tension flags when Tier-1 and Tier-2 disagree.

    Flag-OFF path returns a shallow copy of ``primary`` with no added
    keys so byte-identity holds.
    """
    from . import config as cfgmod
    from .review.reflection_parser import extract_reflection_confidence
    if not cfgmod._features_block().get("w_review_tension_reflection", False):
        return dict(primary)

    annotated = dict(primary)
    reflection_conf = extract_reflection_confidence(primary.get("reason", ""))
    if reflection_conf is not None:
        annotated["reflection_confidence"] = reflection_conf
    if second_pass and second_pass.get("decision") != primary.get("decision"):
        annotated["tension_detected"] = True
        annotated["tension_detail"] = {
            "primary_decision": primary.get("decision"),
            "second_pass_decision": second_pass.get("decision"),
        }
    return annotated


def _maybe_route_to_second_pass(verdict: dict[str, Any]) -> str:
    """Stream W2.4 — decide whether a Tier-1 verdict should escalate to
    the Tier-2 (second-pass) reviewer.

    Returns ``"route_second_pass"`` if the scaffold-compatible
    confidence cut flags the verdict as uncertain, else ``"finalize"``.

    The full Stream F.4 conformal calibrator emits p-values; we use a
    fixed 0.90 cut here so the wiring is trivially auditable. The
    p-value upgrade is an isolated future task once verified
    calibration data exists.
    """
    from . import config as cfgmod
    if not cfgmod._features_block().get("w_review_conformal_routing", False):
        return "finalize"
    confidence = float(verdict.get("confidence", 0.0))
    if confidence < 0.90:
        return "route_second_pass"
    return "finalize"


def _legacy_adjudicate(
    *,
    candidate: "Mapping[str, Any]",
    raw_llm_response: str,
) -> dict[str, Any]:
    """Stream Y3.3 legacy fallback — non-CoT adjudication path.

    Delegates to the Stream F.6 ``parse_reflection`` sniffer and maps
    its verdict surface (``halt_auto_promote``) into the Y3.3 decision
    dict shape so ``adjudicate_with_cot`` has a uniform return contract
    whether the flag is on or off. Patched in tests to isolate the
    flag-off branch.
    """
    from .review.reflection_parser import parse_reflection

    legacy = parse_reflection(raw_llm_response)
    if legacy.halt_auto_promote:
        return {"verdict": "escalate", "reason": legacy.reason}
    return {"verdict": "keep"}


def adjudicate_with_cot(
    *,
    candidate: "Mapping[str, Any]",
    raw_llm_response: str,
    relationship_hash: str,
    cot_out_dir: "Path",
    model: str = "unknown",
) -> dict[str, Any]:
    """Stream Y3.3 — strict-CoT adjudication hook, gated on
    ``features.y_thinking_mode_cot``.

    When the flag is OFF, delegates to :func:`_legacy_adjudicate`
    (so the caller can patch it in tests to isolate the gate).
    When ON:
      1. Parses ``raw_llm_response`` with :func:`parse_cot_strict`.
         A :class:`CotParseError` is caught and surfaces as
         ``{"verdict": "escalate", "reason": "CotParseError: ..."}``.
      2. Writes an append-only audit trace via :func:`write_cot_trace`.
      3. If the CoT result flags ``escalate`` (low self-confidence),
         returns ``{"verdict": "escalate", ...}`` without blocking.
      4. Otherwise returns a dict with the verdict, escalate flag,
         self-confidence, reasoning steps, and evidence citation.
    """
    from . import config as cfgmod
    if not cfgmod._features_block().get("y_thinking_mode_cot", False):
        return _legacy_adjudicate(
            candidate=candidate,
            raw_llm_response=raw_llm_response,
        )

    from .review.cot_audit import write_cot_trace
    from .review.reflection_parser import CotParseError, parse_cot_strict

    try:
        cot = parse_cot_strict(raw_llm_response)
    except CotParseError as exc:
        return {"verdict": "escalate", "reason": f"CotParseError: {exc}"}

    write_cot_trace(
        out_dir=cot_out_dir,
        relationship_hash=relationship_hash,
        cot=cot,
        model=model,
        candidate_raw_response=raw_llm_response,
    )

    if cot.escalate:
        return {
            "verdict": "escalate",
            "reason": "low self-confidence",
            "self_confidence": cot.self_confidence,
        }

    return {
        "verdict": cot.verdict,
        "escalate": False,
        "self_confidence": cot.self_confidence,
        "reasoning_steps": list(cot.reasoning_steps),
        "evidence_citation": cot.evidence_citation,
    }


def select_review_model(
    *,
    candidate: dict[str, Any],
    moe_policy_path: "Path | None" = None,
) -> str:
    """Stream Y2.4 — pick a review model for this candidate, respecting
    ``features.y_domain_routing_moe``.

    When the flag is OFF, returns the baseline default from
    :func:`config.get_ollama_default_model`. When ON, loads the MoE
    policy file (default ``config/moe_routing.yaml``) and calls
    :func:`review.slm_router.route_with_moe`.

    Keeps :func:`_choose_tier_model` untouched so the Sprint Q W2.3
    complexity router stays available for operators that prefer it.
    """
    from pathlib import Path as _Path

    from . import config as cfgmod
    from .paths import get_repo_root

    if not cfgmod._features_block().get("y_domain_routing_moe", False):
        return cfgmod.get_ollama_default_model()

    from .review.slm_router import load_moe_policy, route_with_moe

    policy_path = moe_policy_path
    if policy_path is None:
        policy_path = _Path(get_repo_root()) / "config" / "moe_routing.yaml"
    policy = load_moe_policy(policy_path)
    verdict = route_with_moe(candidate=candidate, moe_policy=policy)
    return verdict.model


def _choose_tier_model(candidate: dict[str, Any]) -> str:
    """Stream W2.3 — pick a model tier based on candidate complexity.

    Simple candidates (short evidence, short endpoint span) route to
    the draft model so sub-4B models can burn through the easy
    majority. Everything else routes to the default.

    When ``features.w_review_slm_routing`` is false, returns
    :func:`get_ollama_default_model` so flag-OFF byte-identity holds.
    """
    from . import config as cfgmod
    features = cfgmod._features_block()
    if not features.get("w_review_slm_routing", False):
        return cfgmod.get_ollama_default_model()

    pool = cfgmod.get_ollama_model_pool()
    draft = pool.get("tier_0_draft")
    default = pool.get("tier_1_default") or cfgmod.get_ollama_default_model()

    examples = candidate.get("examples", [])
    snippet_len = 0
    if examples and isinstance(examples[0], dict):
        snippet_len = len(str(examples[0].get("snippet", "")))
    char_distance = int(candidate.get("char_distance", 0))

    is_simple = snippet_len <= 200 and char_distance <= 120
    if is_simple and draft:
        return draft
    return default


def _load_graph_edge_summaries() -> list[Any]:
    """Stream W2.2 — project the Phase 8 snapshot into GraphEdgeSummary rows.

    Returns an empty list if the snapshot is missing or unreadable; the
    ontology context block then becomes a noop so review still runs.
    """
    from .review.ontology_prompt_builder import GraphEdgeSummary
    from .graph.snapshot import read_snapshot
    from .paths import get_repo_root

    snapshot_path = (
        get_repo_root()
        / "005_Operational-Intelligence-Layer"
        / "graph"
        / "latest_graph_snapshot.json"
    )
    if not snapshot_path.exists():
        return []
    try:
        snap = read_snapshot(snapshot_path)
    except Exception:
        return []
    return [
        GraphEdgeSummary(
            from_id=e.from_id,
            to_id=e.to_id,
            predicate=e.type,
        )
        for e in snap.edges
    ]


def _inject_ontology_context(candidate: dict[str, Any]) -> str:
    """Stream W2.2 — render a compact graph neighborhood block for the
    focal concept. Returns an empty string when the graph is empty or
    the focal node is absent, so the caller can safely concatenate.
    """
    from .review.ontology_prompt_builder import extract_neighborhood

    edges = _load_graph_edge_summaries()
    if not edges:
        return ""
    focal = str(candidate.get("from", ""))
    neighborhood = extract_neighborhood(
        edges,
        focal_node=focal,
        max_hops=2,
        max_edges_per_hop=5,
    )
    if not neighborhood:
        return ""
    lines = ["--- graph neighborhood ---"]
    for edge in neighborhood[:10]:
        lines.append(f"  {edge.from_id} --[{edge.predicate}]--> {edge.to_id}")
    return "\n".join(lines) + "\n"


def _build_binary_prompt(candidate: dict[str, Any]) -> str:
    """Stream W1.4 — compact True/False prompt for small-model binary mode.

    Used when ``features.w_llm_binary_mode`` is true; lets sub-4B models
    handle the first-pass review without overflowing the context window.
    """
    examples = candidate.get("examples", [])
    snippet = ""
    if examples:
        first = examples[0]
        if isinstance(first, dict):
            snippet = str(first.get("snippet") or first.get("evidence_snippet") or "")[:600]
    return (
        f"Subject: {candidate['from']}\n"
        f"Predicate: {candidate['type']}\n"
        f"Object: {candidate['to']}\n"
        f"Evidence: {snippet}\n"
        f"\n"
        f"Question: Is this a valid architectural regulatory relationship "
        f"supported by the evidence above? Answer only one word: True or False.\n"
    )


def build_prompt(candidate: dict[str, Any]) -> str:
    from . import config as cfgmod
    features = cfgmod._features_block()
    if features.get("w_llm_binary_mode", False):
        return _build_binary_prompt(candidate)
    neighborhood_block = ""
    if features.get("w_review_ontology_prompt", False):
        neighborhood_block = _inject_ontology_context(candidate)
    payload = {
        "task": "Review candidate legal relationship",
        "allowed_decisions": ["keep", "review_further", "reject"],
        "candidate": {
            "from": candidate["from"],
            "type": candidate["type"],
            "to": candidate["to"],
            "occurrences": candidate.get("occurrences", 0),
            "sections": candidate.get("sections", []),
            "examples": candidate.get("examples", []),
        },
        "instructions": [
            "Judge only the candidate relationship provided.",
            "Use only the supplied evidence examples.",
            "Do not invent facts or new relationships.",
            "If the evidence is clearly supportive, choose keep.",
            "If the relationship may be plausible but the type is too strong or unclear, choose review_further.",
            "If the evidence does not support the relationship, choose reject.",
            "Return valid JSON only with no markdown fences."
        ],
        "output_schema": {
            "decision": "keep|review_further|reject",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation",
            "suggested_type": "string or null"
        }
    }

    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if neighborhood_block:
        rendered = neighborhood_block + "\n" + rendered
    return rendered


class ContextBudgetExceeded(ValueError):
    """Raised when a prompt exceeds the configured num_ctx budget."""


def _run_nb_pre_filter(candidate: dict[str, Any]) -> tuple[str, float]:
    """Stream W2.1 — invoke the Stream F.1 Naive Bayes scaffold.

    Returns ``(action, confidence)`` where action is one of
    ``auto_accept`` | ``auto_reject`` | ``forward_to_llm``.

    The classifier itself only works once ≥MIN_TRAINING_EXAMPLES audit
    logs exist. Until then we call the lightweight rule-based cold-start
    fallback below — same decision surface, same feature shape.
    """
    from .review.naive_bayes_filter import (
        CandidateFeatures,
        DEFAULT_AUTO_ACCEPT_THRESHOLD,
        DEFAULT_AUTO_REJECT_THRESHOLD,
    )
    examples = candidate.get("examples") or [{}]
    first = examples[0] if isinstance(examples[0], dict) else {}
    evidence_length = len(str(first.get("snippet", "")))
    features = CandidateFeatures(
        predicate=str(candidate.get("type", "")),
        regex_pattern_id=str(candidate.get("pattern_id", "unknown")),
        char_distance=int(candidate.get("char_distance", 100)),
        evidence_length=evidence_length,
        verb_voice=str(candidate.get("verb_voice", "unknown")),
        has_negation=bool(candidate.get("has_negation", False)),
    )
    if features.has_negation and features.evidence_length < 40:
        return ("auto_reject", DEFAULT_AUTO_REJECT_THRESHOLD)
    if features.evidence_length > 120 and features.predicate in {
        "governs", "defines", "requires", "limits", "affects",
    }:
        return ("auto_accept", DEFAULT_AUTO_ACCEPT_THRESHOLD)
    return ("forward_to_llm", 0.5)


def _maybe_pre_filter(candidate: dict[str, Any]) -> dict[str, Any] | None:
    """Stream W2.1 — short-circuit the LLM call when the NB prefilter is
    confident. Returns a canned decision dict when it auto-accepts or
    auto-rejects, or ``None`` to let the candidate proceed to
    :func:`review_relationship`.

    No-op unless ``features.w_review_nb_prefilter`` is true.
    """
    from . import config as cfgmod
    if not cfgmod._features_block().get("w_review_nb_prefilter", False):
        return None
    action, confidence = _run_nb_pre_filter(candidate)
    if action == "forward_to_llm":
        return None
    decision_map = {"auto_accept": "keep", "auto_reject": "reject"}
    return {
        "action": action,
        "decision": decision_map.get(action, "review_further"),
        "confidence": confidence,
        "source": "nb_prefilter",
        "reason": f"NB prefilter action {action} with confidence {confidence:.2f}",
    }


def _estimate_prompt_tokens(prompt: str) -> int:
    """Stream W1.3 — rough token estimate (~4 English chars per token).

    Intentionally pessimistic so the budget guard has headroom for the
    model's response window. A real tokenizer would be more accurate
    but would add a dependency; this approximation is what
    spaCy/HuggingFace fallback tokenisers use when the model-specific
    tokenizer is unavailable.
    """
    return max(1, len(prompt) // 4)


def _enforce_context_budget(prompt: str) -> None:
    """Stream W1.3 — raise ContextBudgetExceeded if the estimated token
    count of ``prompt`` exceeds the configured num_ctx cap.

    No-op unless features.w_llm_context_budget_guard is true.
    """
    from . import config as cfgmod
    if not cfgmod._features_block().get("w_llm_context_budget_guard", False):
        return
    cap = cfgmod.get_ollama_num_ctx_cap()
    estimated = _estimate_prompt_tokens(prompt)
    if estimated > cap:
        raise ContextBudgetExceeded(
            f"prompt estimated at {estimated} tokens exceeds num_ctx cap {cap}"
        )


def _build_ollama_request_body(*, model: str, prompt: str) -> dict[str, Any]:
    """Stream W1.2 — construct the Ollama /api/generate body.

    Flag-OFF path is byte-identical to the pre-W1.2 inline dict
    (model / prompt / stream / format / options with temperature=0 and
    num_predict=300). Flag-ON path additionally injects
    ``options.num_ctx = get_ollama_num_ctx_cap()``.
    """
    from . import config as cfgmod
    body: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 300,
        },
    }
    if cfgmod._features_block().get("w_llm_num_ctx_enforcement", False):
        body["options"]["num_ctx"] = cfgmod.get_ollama_num_ctx_cap()
    return body


def call_ollama(prompt: str, model: str, timeout_seconds: int) -> str:
    _enforce_context_budget(prompt)
    body = _build_ollama_request_body(model=model, prompt=prompt)

    data = json.dumps(body).encode("utf-8")
    base_url = get_ollama_url().rstrip("/")
    endpoint = f"{base_url}/api/generate"
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Failed to reach Ollama at {endpoint}. "
            "Make sure Ollama is running and the model is available."
        ) from exc

    parsed = json.loads(raw)
    if "response" not in parsed:
        raise RuntimeError(f"Unexpected Ollama response: {raw}")

    return parsed["response"]


def parse_model_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    result = json.loads(cleaned)

    decision = result.get("decision")
    confidence = result.get("confidence")
    reason = result.get("reason")
    suggested_type = result.get("suggested_type")

    if decision not in {"keep", "review_further", "reject"}:
        raise ValueError(f"Invalid decision from model: {decision}")

    try:
        confidence = float(confidence)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid confidence from model: {confidence}") from exc

    confidence = max(0.0, min(1.0, confidence))

    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Model returned empty reason")

    if suggested_type is not None and not isinstance(suggested_type, str):
        suggested_type = None

    return {
        "decision": decision,
        "confidence": confidence,
        "reason": reason.strip(),
        "suggested_type": suggested_type.strip() if isinstance(suggested_type, str) and suggested_type.strip() else None,
    }


def review_relationship(candidate: dict[str, Any], model: str, timeout_seconds: int) -> dict[str, Any]:
    """Review a single candidate with bounded retries and a wall-clock cap.

    The `timeout_seconds` argument is the per-candidate wall budget: all
    retries plus backoffs must finish before it elapses. Each individual
    HTTP call also respects the remaining budget.
    """
    from .config import get_ollama_max_retries, get_ollama_retry_backoff

    max_retries = get_ollama_max_retries()
    backoff = get_ollama_retry_backoff()
    prompt = build_prompt(candidate)

    deadline = time.monotonic() + timeout_seconds
    last_exc: Exception | None = None

    for attempt in range(1, max_retries + 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        call_timeout = min(timeout_seconds, max(1, int(remaining)))
        try:
            raw_response = call_ollama(prompt, model=model, timeout_seconds=call_timeout)
            review = parse_model_json(raw_response)
            return {"candidate": candidate, "review": review}
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries:
                sleep_for = backoff * attempt
                if time.monotonic() + sleep_for < deadline:
                    time.sleep(sleep_for)
                else:
                    break

    return {
        "candidate": candidate,
        "review": {
            "decision": "review_further",
            "confidence": 0.0,
            "reason": f"Ollama review failed after retries: {last_exc}",
            "suggested_type": None,
        },
    }


def summarize_reviews(review_items: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {
        "keep": 0,
        "review_further": 0,
        "reject": 0,
        "high_confidence_keep": 0,
        "high_confidence_reject": 0,
    }

    for item in review_items:
        review = item["review"]
        decision = review["decision"]
        confidence = review["confidence"]

        summary[decision] += 1

        if decision == "keep" and confidence >= 0.85:
            summary["high_confidence_keep"] += 1

        if decision == "reject" and confidence >= 0.85:
            summary["high_confidence_reject"] += 1

    return summary


def build_text_report(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("Ollama Relationship Review Report")
    lines.append("")
    lines.append(f"Model: {report['model']}")
    lines.append(f"Source: {report['source']}")
    lines.append(f"Candidates reviewed: {report['total_candidates']}")
    lines.append(f"Keep: {report['summary']['keep']}")
    lines.append(f"Review Further: {report['summary']['review_further']}")
    lines.append(f"Reject: {report['summary']['reject']}")
    lines.append("")

    for item in report["reviews"]:
        candidate = item["candidate"]
        review = item["review"]

        lines.append(
            f"{candidate['from']} -> {candidate['type']} -> {candidate['to']}"
        )
        lines.append(
            f"  decision={review['decision']} confidence={review['confidence']:.2f}"
        )
        lines.append(f"  reason={review['reason']}")
        if review["suggested_type"]:
            lines.append(f"  suggested_type={review['suggested_type']}")
        lines.append("")

    return "\n".join(lines)


def save_progress_report(
    *,
    runs_dir: Path,
    model: str,
    source: str,
    candidates: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    status: str,
) -> None:
    report = {
        "generated_at": utc_now_stamp(),
        "model": model,
        "source": source,
        "total_candidates": len(candidates),
        "completed_reviews": len(reviews),
        "status": status,
        "summary": summarize_reviews(reviews),
        "reviews": reviews,
    }

    json_path = runs_dir / "latest_relationship_review_ollama.json"
    txt_path = runs_dir / "latest_relationship_review_ollama.txt"

    write_json(json_path, report)
    write_text(txt_path, build_text_report(report))


def warmup_model(*, model: str, timeout_seconds: int) -> bool:
    """Send a minimal generate call to force Ollama to load the model.

    Returns True on success, False on any error. Never raises — warmup
    failure must not abort the batch; the per-candidate retry loop will
    handle transient Ollama issues.
    """
    warmup_prompt = '{"task": "warmup ping", "respond_with": "ok"}'
    try:
        call_ollama(warmup_prompt, model=model, timeout_seconds=min(timeout_seconds, 120))
        return True
    except Exception:
        return False


def review_candidates_parallel(
    candidates: list[dict[str, Any]],
    *,
    model: str,
    timeout_seconds: int,
    parallelism: int,
) -> list[dict[str, Any]]:
    """Review a list of candidates optionally in parallel.

    Results are returned in the same order as the input. For parallelism=1
    this degrades gracefully to the sequential implementation.
    """
    if parallelism <= 1:
        return [
            review_relationship(c, model=model, timeout_seconds=timeout_seconds)
            for c in candidates
        ]

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        futures = [
            pool.submit(review_relationship, c, model, timeout_seconds)
            for c in candidates
        ]
        return [f.result() for f in futures]


def load_resume_state(runs_dir: Path) -> dict[str, Any]:
    """Read the latest in_progress snapshot, if any, for resume-on-relaunch."""
    snapshot_path = runs_dir / "latest_relationship_review_ollama.json"
    if not snapshot_path.exists():
        return {"reviews": [], "status": None, "completed_count": 0}

    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if payload.get("status") != "in_progress":
        return {"reviews": [], "status": payload.get("status"), "completed_count": 0}

    return {
        "reviews": payload.get("reviews", []),
        "status": "in_progress",
        "completed_count": len(payload.get("reviews", [])),
    }


def write_high_confidence_review(
    report: dict[str, Any],
    runs_dir: Path,
    *,
    threshold: float | None = None,
) -> Path:
    """Filter the review report to keep-only, confidence >= threshold.

    Writes 006_System-Manifests/runs/latest_relationship_review_high_confidence.json
    and returns the output path. An empty-but-valid file is written when no
    candidates clear the threshold.
    """
    from .config import get_confidence_threshold

    if threshold is None:
        threshold = get_confidence_threshold()

    high_conf: list[dict[str, Any]] = []
    for item in report.get("reviews", []):
        review = item.get("review", {})
        if review.get("decision") == "keep" and float(review.get("confidence", 0.0)) >= threshold:
            high_conf.append(item)

    payload = {
        "generated_at": utc_now_stamp(),
        "source_report_generated_at": report.get("generated_at"),
        "source_model": report.get("model"),
        "source": report.get("source"),
        "threshold": threshold,
        "count": len(high_conf),
        "candidates": high_conf,
    }

    runs_dir.mkdir(parents=True, exist_ok=True)
    output_path = runs_dir / "latest_relationship_review_high_confidence.json"
    write_json(output_path, payload)
    return output_path


def run_review_relationships_ollama(
    *,
    model: str = DEFAULT_MODEL,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    parallelism: int | None = None,
    skip_pre_review_filter: bool = False,
) -> int:
    from .config import get_ollama_default_parallelism
    from .pre_review_filter import triage_candidates

    if parallelism is None:
        parallelism = get_ollama_default_parallelism()
    repo_root = get_repo_root()
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    extraction_report = load_relationship_report()
    raw_candidates = extraction_report.get("relationships", [])
    source = extraction_report.get("source", "")

    if not raw_candidates:
        print("review-relationships-ollama complete.")
        print("No candidate relationships found to review.")
        save_progress_report(
            runs_dir=runs_dir,
            model=model,
            source=source,
            candidates=raw_candidates,
            reviews=[],
            status="completed",
        )
        return 0

    # Pre-review triage: sort candidates into auto_accept / auto_reject /
    # needs_review buckets using deterministic rules. Only needs_review goes
    # to the LLM. Auto-accept and auto-reject are recorded so downstream can
    # use them without burning LLM cycles.
    if skip_pre_review_filter:
        candidates = raw_candidates
        triaged_buckets: dict[str, list[dict[str, Any]]] = {
            "auto_accept": [],
            "auto_reject": [],
            "needs_review": raw_candidates,
        }
    else:
        triaged_buckets = triage_candidates(raw_candidates)
        candidates = triaged_buckets["needs_review"]
        print(f"Pre-review triage:")
        print(f"  auto_accept:  {len(triaged_buckets['auto_accept'])}")
        print(f"  auto_reject:  {len(triaged_buckets['auto_reject'])}")
        print(f"  needs_review: {len(triaged_buckets['needs_review'])}")
        print("")
        # Write the triage buckets so Phase 7 promotion and audits can see them.
        triage_path = runs_dir / "latest_pre_review_triage.json"
        write_json(triage_path, {
            "generated_at": utc_now_stamp(),
            "source": source,
            "total_candidates": len(raw_candidates),
            "auto_accept_count": len(triaged_buckets["auto_accept"]),
            "auto_reject_count": len(triaged_buckets["auto_reject"]),
            "needs_review_count": len(triaged_buckets["needs_review"]),
            "buckets": triaged_buckets,
        })
        print(f"Triage report: {triage_path}")
        print("")

    resume_state = load_resume_state(runs_dir)
    if resume_state["status"] == "in_progress" and resume_state["reviews"]:
        reviews: list[dict[str, Any]] = list(resume_state["reviews"])
        skip_first_n = resume_state["completed_count"]
        print(f"Resuming from in_progress snapshot ({skip_first_n}/{len(candidates)} already done).")
    else:
        reviews = []
        skip_first_n = 0

    print(f"Starting Ollama relationship review with model: {model}")
    print(f"Source: {source}")
    print(f"Total candidates: {len(candidates)}")
    print(f"Timeout per candidate: {timeout_seconds} seconds")
    print("")

    print(f"Warming up {model}...")
    warm_ok = warmup_model(model=model, timeout_seconds=timeout_seconds)
    print(f"Warmup: {'ok' if warm_ok else 'failed (continuing anyway)'}")
    print("")

    try:
        for idx, candidate in enumerate(candidates, start=1):
            if idx <= skip_first_n:
                continue
            start_time = time.time()

            from_id = candidate["from"]
            rel_type = candidate["type"]
            to_id = candidate["to"]
            occurrences = candidate.get("occurrences", 0)

            print(
                f"[{idx}/{len(candidates)}] Reviewing: "
                f"{from_id} -> {rel_type} -> {to_id} "
                f"(occurrences={occurrences})"
            )

            pre_decision = _maybe_pre_filter(candidate)
            if pre_decision is not None:
                print(
                    f"    NB prefilter {pre_decision['action']} "
                    f"confidence={pre_decision['confidence']:.2f} — skipping LLM call"
                )
                review_item = {
                    "candidate": candidate,
                    "review": {
                        "decision": pre_decision["decision"],
                        "confidence": pre_decision["confidence"],
                        "reason": pre_decision["reason"],
                        "suggested_type": None,
                    },
                    "source": pre_decision["source"],
                }
                reviews.append(review_item)
                save_progress_report(
                    runs_dir=runs_dir,
                    model=model,
                    source=source,
                    candidates=candidates,
                    reviews=reviews,
                    status="in_progress" if idx < len(candidates) else "completed",
                )
                continue

            from . import config as _cfgmod
            per_candidate_model = model
            if _cfgmod._features_block().get("w_review_slm_routing", False):
                per_candidate_model = _choose_tier_model(candidate)
            review_item = review_relationship(
                candidate,
                model=per_candidate_model,
                timeout_seconds=timeout_seconds,
            )
            reviews.append(review_item)

            elapsed = time.time() - start_time
            decision = review_item["review"]["decision"]
            confidence = review_item["review"]["confidence"]

            print(
                f"    Done in {elapsed:.1f}s | "
                f"decision={decision} confidence={confidence:.2f}"
            )

            save_progress_report(
                runs_dir=runs_dir,
                model=model,
                source=source,
                candidates=candidates,
                reviews=reviews,
                status="in_progress" if idx < len(candidates) else "completed",
            )

    except KeyboardInterrupt:
        print("")
        print("Interrupted by user. Saving partial review results...")
        save_progress_report(
            runs_dir=runs_dir,
            model=model,
            source=source,
            candidates=candidates,
            reviews=reviews,
            status="interrupted",
        )
        print("Partial results saved.")
        return 130

    save_progress_report(
        runs_dir=runs_dir,
        model=model,
        source=source,
        candidates=candidates,
        reviews=reviews,
        status="completed",
    )

    # Synthesize LLM-equivalent review items for the auto-accepted candidates
    # so they flow into the same downstream consumers (high-confidence writer,
    # Phase 7 promotion) without burning LLM cycles. Each gets a synthetic
    # review with source="pre_review_filter" so auditors can tell them apart.
    synthetic_reviews = []
    for bucket_name, synthetic_decision in (("auto_accept", "keep"), ("auto_reject", "reject")):
        for cand in triaged_buckets.get(bucket_name, []):
            triage = cand.get("triage", {})
            # Strip the triage metadata from the embedded candidate so the
            # downstream schema stays identical to an LLM-reviewed item.
            cand_clean = {k: v for k, v in cand.items() if k != "triage"}
            synthetic_reviews.append({
                "candidate": cand_clean,
                "review": {
                    "decision": synthetic_decision,
                    "confidence": float(triage.get("confidence", 0.95)),
                    "reason": "pre_review_filter: " + "; ".join(triage.get("reasons", [])),
                    "suggested_type": None,
                    "source": "pre_review_filter",
                },
            })

    all_reviews = synthetic_reviews + reviews

    final_report = {
        "generated_at": utc_now_stamp(),
        "model": model,
        "source": source,
        "total_candidates": len(raw_candidates),
        "llm_reviewed": len(reviews),
        "pre_review_auto_accepted": len(triaged_buckets.get("auto_accept", [])),
        "pre_review_auto_rejected": len(triaged_buckets.get("auto_reject", [])),
        "completed_reviews": len(all_reviews),
        "status": "completed",
        "summary": summarize_reviews(all_reviews),
        "reviews": all_reviews,
    }
    # Overwrite the review JSON with the triage-aware final report. The
    # save_progress_report calls during the loop wrote the LLM-only view
    # for resume safety; this final write adds the synthesized auto-accept
    # and auto-reject reviews so Phase 7 promotion sees the full picture.
    write_json(runs_dir / "latest_relationship_review_ollama.json", final_report)
    write_text(runs_dir / "latest_relationship_review_ollama.txt", build_text_report(final_report))

    high_conf_path = write_high_confidence_review(final_report, runs_dir)

    print("")
    print("review-relationships-ollama complete.")
    print(f"Candidates reviewed: {len(candidates)}")
    print(f"JSON: {runs_dir / 'latest_relationship_review_ollama.json'}")
    print(f"TXT: {runs_dir / 'latest_relationship_review_ollama.txt'}")
    print(f"High-confidence: {high_conf_path}")

    return 0