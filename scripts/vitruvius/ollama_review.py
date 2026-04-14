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
    if cfgmod._features_block().get("w_llm_binary_mode", False):
        return _build_binary_prompt(candidate)
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

    return json.dumps(payload, ensure_ascii=False, indent=2)


class ContextBudgetExceeded(ValueError):
    """Raised when a prompt exceeds the configured num_ctx budget."""


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

            review_item = review_relationship(
                candidate,
                model=model,
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