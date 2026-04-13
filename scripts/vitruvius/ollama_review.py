from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .paths import get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "gemma4:31b"
DEFAULT_TIMEOUT_SECONDS = 600


def load_relationship_report() -> dict[str, Any]:
    repo_root = get_repo_root()
    path = repo_root / "006_System-Manifests" / "runs" / "latest_relationship_extraction_sections.json"

    if not path.exists():
        raise FileNotFoundError(
            f"Relationship extraction report not found: {path}. "
            "Run extract-relationships-sections-one first."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def build_prompt(candidate: dict[str, Any]) -> str:
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


def call_ollama(prompt: str, model: str, timeout_seconds: int) -> str:
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 300,
        },
    }

    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Failed to reach Ollama at http://127.0.0.1:11434. "
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
    prompt = build_prompt(candidate)

    try:
        raw_response = call_ollama(prompt, model=model, timeout_seconds=timeout_seconds)
        review = parse_model_json(raw_response)
    except Exception as exc:
        review = {
            "decision": "review_further",
            "confidence": 0.0,
            "reason": f"Ollama review failed: {exc}",
            "suggested_type": None,
        }

    return {
        "candidate": candidate,
        "review": review,
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


def run_review_relationships_ollama(
    *,
    model: str = DEFAULT_MODEL,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> int:
    repo_root = get_repo_root()
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    extraction_report = load_relationship_report()
    candidates = extraction_report.get("relationships", [])
    source = extraction_report.get("source", "")

    if not candidates:
        print("review-relationships-ollama complete.")
        print("No candidate relationships found to review.")
        save_progress_report(
            runs_dir=runs_dir,
            model=model,
            source=source,
            candidates=candidates,
            reviews=[],
            status="completed",
        )
        return 0

    reviews: list[dict[str, Any]] = []

    print(f"Starting Ollama relationship review with model: {model}")
    print(f"Source: {source}")
    print(f"Total candidates: {len(candidates)}")
    print(f"Timeout per candidate: {timeout_seconds} seconds")
    print("")

    try:
        for idx, candidate in enumerate(candidates, start=1):
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

    print("")
    print("review-relationships-ollama complete.")
    print(f"Candidates reviewed: {len(candidates)}")
    print(f"JSON: {runs_dir / 'latest_relationship_review_ollama.json'}")
    print(f"TXT: {runs_dir / 'latest_relationship_review_ollama.txt'}")

    return 0