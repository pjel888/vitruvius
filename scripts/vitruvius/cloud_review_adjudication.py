from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Mapping


def should_escalate_to_cloud(
    review_item: Mapping[str, Any],
    *,
    low_confidence_threshold: float,
    high_value_occurrences_threshold: int,
) -> bool:
    candidate = review_item.get("candidate", {})
    review = review_item.get("review", {})
    decision = str(review.get("decision", "review_further"))
    confidence = float(review.get("confidence", 0.0))
    occurrences = int(candidate.get("occurrences", 0) or 0)

    return (
        decision == "review_further"
        or confidence < low_confidence_threshold
        or occurrences >= high_value_occurrences_threshold
    )


def build_cloud_adjudication_prompt(
    candidate: Mapping[str, Any],
    local_review: Mapping[str, Any],
    *,
    local_model: str,
) -> str:
    payload = {
        "task": "Cloud adjudication of a legal relationship candidate",
        "allowed_decisions": ["keep", "review_further", "reject"],
        "candidate": {
            "from": candidate.get("from"),
            "type": candidate.get("type"),
            "to": candidate.get("to"),
            "occurrences": candidate.get("occurrences", 0),
            "sections": candidate.get("sections", []),
            "examples": candidate.get("examples", []),
        },
        "local_review": {
            "model": local_model,
            "decision": local_review.get("decision"),
            "confidence": local_review.get("confidence"),
            "reason": local_review.get("reason", ""),
            "suggested_type": local_review.get("suggested_type"),
        },
        "instructions": [
            "You are an adjudication pass that reviews a locally produced verdict.",
            "Use only the supplied evidence examples and candidate data.",
            "Do not invent new endpoints or facts.",
            "If the local review is wrong or too weak, say so explicitly in your reason.",
            "If the evidence is clear and supports the predicate, choose keep.",
            "If the endpoints may be right but the predicate is too strong or unclear, choose review_further and set suggested_type if appropriate.",
            "If the evidence is weak, irrelevant, or contradictory, choose reject.",
            "Return valid JSON only with no markdown fences.",
        ],
        "output_schema": {
            "decision": "keep|review_further|reject",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation",
            "suggested_type": "string or null",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _call_openai_compatible(*, prompt: str, settings: Mapping[str, Any]) -> str:
    api_base_url = str(settings.get("api_base_url") or "").rstrip("/")
    api_key = str(settings.get("api_key") or "")
    model = str(settings.get("model") or "")
    timeout_seconds = int(settings.get("timeout_seconds") or 60)
    if not api_base_url or not api_key or not model:
        raise RuntimeError("Cloud adjudication is missing api_base_url, api_key, or model")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        f"{api_base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Cloud adjudication request failed: {exc}") from exc

    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError(f"Cloud adjudication returned no choices: {body}")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError(f"Cloud adjudication returned empty content: {body}")
    return content


def _call_gemini(*, prompt: str, settings: Mapping[str, Any]) -> str:
    api_key = str(settings.get("api_key") or "")
    model = str(settings.get("model") or "")
    timeout_seconds = int(settings.get("timeout_seconds") or 60)
    if not api_key or not model:
        raise RuntimeError("Gemini adjudication is missing api_key or model")

    query = urllib.parse.urlencode({"key": api_key})
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?{query}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
        },
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Gemini adjudication request failed: {exc}") from exc

    candidates = body.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini adjudication returned no candidates: {body}")
    parts = (((candidates[0] or {}).get("content") or {}).get("parts") or [])
    if not parts or not isinstance(parts[0].get("text"), str):
        raise RuntimeError(f"Gemini adjudication returned no text: {body}")
    return str(parts[0]["text"])


def call_cloud_adjudicator(*, prompt: str, settings: Mapping[str, Any]) -> str:
    provider = str(settings.get("provider") or "openai_compatible")
    if provider == "gemini":
        return _call_gemini(prompt=prompt, settings=settings)
    return _call_openai_compatible(prompt=prompt, settings=settings)


def _summarize_reviews(review_items: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "keep": 0,
        "review_further": 0,
        "reject": 0,
        "high_confidence_keep": 0,
        "high_confidence_reject": 0,
    }
    for item in review_items:
        review = item.get("review", {})
        decision = str(review.get("decision", "review_further"))
        confidence = float(review.get("confidence", 0.0))
        if decision not in {"keep", "review_further", "reject"}:
            continue
        summary[decision] += 1
        if decision == "keep" and confidence >= 0.85:
            summary["high_confidence_keep"] += 1
        if decision == "reject" and confidence >= 0.85:
            summary["high_confidence_reject"] += 1
    return summary


def apply_cloud_adjudication(
    report: dict[str, Any],
    *,
    settings: Mapping[str, Any],
    parse_model_json_fn,
) -> dict[str, Any]:
    if not settings.get("enabled"):
        return report

    local_model = str(report.get("model") or "unknown")
    prefer_adjudicated = bool(settings.get("prefer_adjudicated_decision", True))
    low_confidence_threshold = float(settings.get("low_confidence_threshold", 0.90))
    high_value_occurrences_threshold = int(settings.get("high_value_occurrences_threshold", 3))

    selected_count = 0
    successful_count = 0
    failed_count = 0
    updated_reviews: list[dict[str, Any]] = []

    for item in report.get("reviews", []):
        if not should_escalate_to_cloud(
            item,
            low_confidence_threshold=low_confidence_threshold,
            high_value_occurrences_threshold=high_value_occurrences_threshold,
        ):
            updated_reviews.append(item)
            continue

        selected_count += 1
        candidate = item.get("candidate", {})
        local_review = item.get("review", {})
        prompt = build_cloud_adjudication_prompt(candidate, local_review, local_model=local_model)

        annotated = dict(item)
        annotated["local_review"] = dict(local_review)
        try:
          raw = call_cloud_adjudicator(prompt=prompt, settings=settings)
          cloud_review = parse_model_json_fn(raw)
          cloud_review["source"] = "cloud_adjudicator"
          annotated["cloud_review"] = cloud_review
          annotated["cloud_adjudication"] = {
              "provider": settings.get("provider"),
              "model": settings.get("model"),
              "selected": True,
              "status": "applied",
          }
          if prefer_adjudicated:
              annotated["review"] = cloud_review
          successful_count += 1
        except Exception as exc:
          annotated["cloud_adjudication"] = {
              "provider": settings.get("provider"),
              "model": settings.get("model"),
              "selected": True,
              "status": "failed",
              "reason": str(exc),
          }
          failed_count += 1
        updated_reviews.append(annotated)

    updated_report = dict(report)
    updated_report["reviews"] = updated_reviews
    updated_report["summary"] = _summarize_reviews(updated_reviews)
    updated_report["cloud_adjudication"] = {
        "enabled": True,
        "provider": settings.get("provider"),
        "model": settings.get("model"),
        "selected_count": selected_count,
        "successful_count": successful_count,
        "failed_count": failed_count,
        "prefer_adjudicated_decision": prefer_adjudicated,
        "low_confidence_threshold": low_confidence_threshold,
        "high_value_occurrences_threshold": high_value_occurrences_threshold,
    }
    return updated_report
