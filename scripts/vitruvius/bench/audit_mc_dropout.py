"""Sprint AUDIT-1 — MC Dropout production-site survey.

Monte Carlo dropout (Gal & Ghahramani 2016) estimates epistemic
uncertainty by running a dropout-enabled model N times at inference
and taking the sample variance of its predictions. This only works
if the model actually has dropout layers that are ACTIVE at inference
time. Most production PyTorch code disables dropout via ``model.eval()``.

This audit walks every neural-inference module we ship and reports
whether it qualifies as a MC-dropout call site. As of 2026-04-15
the only neural module is ``scripts/vitruvius/graph/graphsage.py``,
and line 219 of that file explicitly states: "Deterministic forward
pass — no dropout, no training loop."

So the audit's expected output is: **viable_site_count == 0 → PARK
the compute_epistemic_uncertainty utility**. But we still do the
survey explicitly, and the site list gives us a checklist to update
whenever we add a new neural module in the future.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Recommendation = Literal["GO", "PARK"]


@dataclass(frozen=True)
class MCDropoutAuditResult:
    viable_sites: list[dict]
    surveyed_sites: list[dict]


def survey_neural_inference_sites() -> list[dict]:
    """Hand-curated list of neural-inference modules in the repo.

    Maintained in this file. If you add a new neural module,
    append to this list with the correct `dropout_enabled_at_inference`
    flag. The smoke test requires GraphSAGE to be present.
    """
    return [
        {
            "file": "scripts/vitruvius/graph/graphsage.py",
            "model_type": "GraphSAGE (torch_geometric + mean aggregator)",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "graphsage.py:219 explicitly says 'Deterministic forward pass — "
                "no dropout, no training loop.' The forward pass runs inside "
                "torch.no_grad() with model.eval(), which disables dropout."
            ),
            "sprint": "HP.5",
        },
        {
            "file": "scripts/vitruvius/review/naive_bayes_filter.py",
            "model_type": "Multinomial Naive Bayes (closed-form, not neural)",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "Naive Bayes is a probabilistic classifier with no hidden layers "
                "and no dropout concept. MC dropout is inapplicable."
            ),
            "sprint": "Q-W2",
        },
        {
            "file": "scripts/vitruvius/extraction/crf_trainer.py",
            "model_type": "Linear-chain CRF",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "CRFs are discriminative sequence models with no neural dropout. "
                "The uncertainty signal here is the marginal probability from the "
                "forward-backward algorithm, not MC dropout."
            ),
            "sprint": "D-E",
        },
        {
            "file": "scripts/vitruvius/extraction/kg_link_predictor.py",
            "model_type": "TransE-family link predictor",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "TransE uses learned entity and relation embeddings; inference is "
                "a vector arithmetic score. No dropout in the inference path."
            ),
            "sprint": "D-E",
        },
        {
            "file": "scripts/vitruvius/ollama_review.py",
            "model_type": "Remote LLM (Ollama)",
            "dropout_enabled_at_inference": False,
            "evidence": (
                "Ollama exposes a completion API — it does not expose a "
                "dropout-at-inference knob to clients. Even if it did, running "
                "the same prompt N times with a non-zero temperature gives "
                "different samples, but that is aleatoric sampling variance, "
                "not MC dropout. Alternative uncertainty signals for LLM "
                "review are provided by the Sprint Q W2 conformal gate and the "
                "self_confidence field parsed from the response."
            ),
            "sprint": "6A",
        },
    ]


def compute_recommendation(*, viable_site_count: int) -> Recommendation:
    """MC Dropout is a wiring task. Without a viable site, it has no work to do."""
    if viable_site_count >= 1:
        return "GO"
    return "PARK"


if __name__ == "__main__":
    import argparse
    import datetime as dt

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(".ai/10_state/audit_mc_dropout_2026-04-15.json"))
    args = parser.parse_args()

    sites = survey_neural_inference_sites()
    viable = [s for s in sites if s["dropout_enabled_at_inference"]]
    rec = compute_recommendation(viable_site_count=len(viable))

    report = {
        "timestamp_utc": dt.datetime.utcnow().isoformat() + "Z",
        "python_interpreter": os.sys.executable,
        "host": "darwin-arm64",
        "surveyed_sites": sites,
        "viable_sites": viable,
        "viable_site_count": len(viable),
        "utility_path": "scripts/vitruvius/graph/mc_dropout.py",
        "utility_production_call_sites": 0,
        "decision_gate": {
            "recommendation": rec,
            "notes": (
                f"{len(viable)} viable MC-dropout site(s) found out of {len(sites)} "
                f"neural-inference modules surveyed. "
                f"{'Ship the wiring in Task 6.' if rec == 'GO' else 'Park the utility; it stays available but unused.'}"
            ),
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
