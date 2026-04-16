"""Tier-2 Second-Pass Review (Phase 6B).

Runs only on the uncertain subset of Tier-1 (Gemma) decisions: review_further,
low-confidence keeps and rejects, and predicate disagreements. Produces a
merged adjudication report and a human-escalation worklist.

See .ai/08_prompts/qwen-second-pass.txt for the prompt spec.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import get_ollama_default_timeout
from .ollama_review import call_ollama, parse_model_json
from .paths import get_repo_root
from .reports import write_json
from .review_routing import route_adjudication, select_for_second_pass
from .utils import utc_now_stamp


DEFAULT_SECOND_PASS_MODEL = "qwen3:30b"


def build_second_pass_prompt(
    candidate: dict[str, Any],
    tier_one: dict[str, Any],
    *,
    model_name: str,
) -> str:
    """Build the Tier-2 adjudication prompt per qwen-second-pass.txt."""
    payload = {
        "task": "Second-pass adjudication of a legal relationship candidate",
        "allowed_decisions": ["keep", "review_further", "reject"],
        "candidate": {
            "from": candidate["from"],
            "type": candidate["type"],
            "to": candidate["to"],
            "occurrences": candidate.get("occurrences", 0),
            "sections": candidate.get("sections", []),
            "examples": candidate.get("examples", []),
        },
        "tier_one_decision": {
            "model": model_name,
            "decision": tier_one["decision"],
            "confidence": tier_one["confidence"],
            "reason": tier_one.get("reason", ""),
            "suggested_type": tier_one.get("suggested_type"),
        },
        "instructions": [
            "You are a second-pass adjudicator. A different model has already reviewed this candidate.",
            "Independently assess the candidate using only the supplied evidence examples.",
            "Consider but do not blindly defer to the Tier 1 decision.",
            "If you disagree with Tier 1, say so explicitly in your reason.",
            "If the evidence clearly supports the candidate and the predicate, choose keep with high confidence.",
            "If the predicate is wrong but the endpoints are right, choose review_further and set suggested_type.",
            "If the evidence is irrelevant, weak, or contradicts the claim, choose reject.",
            "Do not invent facts. Do not propose new subjects or objects.",
            "Return valid JSON only with no markdown fences.",
        ],
        "output_schema": {
            "decision": "keep|review_further|reject",
            "confidence": "number from 0.0 to 1.0",
            "reason": "short explanation",
            "suggested_type": "string or null",
            "agrees_with_tier_one": "boolean",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def compute_agreement_matrix(items: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Return a 3x3 agreement matrix: tier_one decision x tier_two decision."""
    axes = ("keep", "review_further", "reject")
    matrix = {a: {b: 0 for b in axes} for a in axes}
    for item in items:
        t1 = item["tier_one"]["decision"]
        t2 = (item.get("tier_two") or {}).get("decision")
        if t1 in matrix and t2 in matrix[t1]:
            matrix[t1][t2] += 1
    return matrix


def _adjudicate_one(item: dict[str, Any], *, model: str, timeout: int) -> dict[str, Any]:
    candidate = item["candidate"]
    tier_one = item["review"]

    prompt = build_second_pass_prompt(candidate, tier_one, model_name=model)
    try:
        raw = call_ollama(prompt, model=model, timeout_seconds=timeout)
        tier_two = parse_model_json(raw)
        tier_two["agrees_with_tier_one"] = (
            tier_two["decision"] == tier_one["decision"]
            and (tier_two.get("suggested_type") or None) == (tier_one.get("suggested_type") or None)
        )
    except Exception as exc:
        tier_two = {
            "decision": "review_further",
            "confidence": 0.0,
            "reason": f"Qwen second pass failed: {exc}",
            "suggested_type": None,
            "agrees_with_tier_one": False,
        }

    adjudicated = {
        "candidate": candidate,
        "tier_one": tier_one,
        "tier_two": tier_two,
    }
    adjudicated["action"] = route_adjudication({
        "tier_one": tier_one,
        "tier_two": tier_two,
    })
    return adjudicated


def _load_tier_one_report(repo_root: Path, report_path: Path | None = None) -> dict[str, Any]:
    path = report_path or (
        repo_root / "006_System-Manifests" / "runs" / "latest_relationship_review_ollama.json"
    )
    if not path.exists():
        raise FileNotFoundError(
            f"Tier 1 review report not found: {path}. Run review-relationships-ollama first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def run_second_pass_inner(
    *,
    repo_root: Path,
    model: str,
    timeout_seconds: int,
    tier_one_report_path: Path | None = None,
    merged_report_path: Path | None = None,
    worklist_path: Path | None = None,
) -> dict[str, Any]:
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    tier_one_report = _load_tier_one_report(repo_root, tier_one_report_path)
    tier_one_items = tier_one_report.get("reviews", [])
    selected = select_for_second_pass(tier_one_items)

    adjudicated: list[dict[str, Any]] = []
    for item in selected:
        adjudicated.append(_adjudicate_one(item, model=model, timeout=timeout_seconds))

    action_counts: dict[str, int] = {"auto_promote": 0, "suppress": 0, "human_review": 0}
    disagreement = 0
    for a in adjudicated:
        action_counts[a["action"]] = action_counts.get(a["action"], 0) + 1
        if not a["tier_two"].get("agrees_with_tier_one", False):
            disagreement += 1

    merged_report = {
        "generated_at": utc_now_stamp(),
        "tier_one_model": tier_one_report.get("model"),
        "tier_two_model": model,
        "total_tier_one": len(tier_one_items),
        "total_second_pass": len(selected),
        "disagreement_rate": (disagreement / len(adjudicated)) if adjudicated else 0.0,
        "actions": action_counts,
        "agreement_matrix": compute_agreement_matrix(adjudicated),
        "items": adjudicated,
    }

    merged_report_path = merged_report_path or (
        runs_dir / "latest_relationship_review_merged.json"
    )
    write_json(merged_report_path, merged_report)

    worklist = [a for a in adjudicated if a["action"] == "human_review"]
    worklist_path = worklist_path or (
        runs_dir / "latest_human_escalation_worklist.json"
    )
    write_json(
        worklist_path,
        {
            "generated_at": utc_now_stamp(),
            "count": len(worklist),
            "items": worklist,
        },
    )

    return merged_report


def run_second_pass(
    *,
    model: str | None = None,
    timeout_seconds: int | None = None,
    tier_one_report_path: Path | None = None,
    merged_report_path: Path | None = None,
    worklist_path: Path | None = None,
) -> int:
    if model is None:
        model = DEFAULT_SECOND_PASS_MODEL
    if timeout_seconds is None:
        timeout_seconds = get_ollama_default_timeout()

    repo_root = get_repo_root()
    try:
        merged = run_second_pass_inner(
            repo_root=repo_root,
            model=model,
            timeout_seconds=timeout_seconds,
            tier_one_report_path=tier_one_report_path,
            merged_report_path=merged_report_path,
            worklist_path=worklist_path,
        )
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Tier-2 review complete (model: {model})")
    print(f"  total_tier_one:    {merged['total_tier_one']}")
    print(f"  total_second_pass: {merged['total_second_pass']}")
    print(f"  actions:           {merged['actions']}")
    print(f"  disagreement_rate: {merged['disagreement_rate']:.2%}")
    return 0
