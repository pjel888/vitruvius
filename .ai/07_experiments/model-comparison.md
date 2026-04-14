# Model Comparison Experiment — Relationship Review (Tier 1 + Tier 2)

> **Status:** Template / structure only. Populated during Sprint C, Phase 6B.
> **Owner:** Review track
> **Last Updated:** 2026-04-14
> **Plan reference:** `/.ai/01_roadmap/master-roadmap.md` Phase 6

## 1. Purpose
Empirically select the best local LLM for Tier 1 (primary reviewer) and Tier 2 (second-pass adjudicator) in the two-stage review architecture. The goal is to answer:

- Is `gemma4:31b` still the right Tier 1 default, or has a better local model shipped?
- What is the right Tier 2 pairing? The master roadmap currently proposes `qwen3:30b`, but the choice is open until this experiment runs.
- How much does the Tier 2 architectural diversity matter? (Same-family models may agree too often.)
- What is the calibration quality of each model's confidence scores?

## 2. Hypotheses
1. **H1.** Gemma4:31b's 90% confidence threshold is well-calibrated — at least 85% of `keep` decisions at conf≥0.90 are correct by human review.
2. **H2.** A smaller Tier 2 model (≤30B) can disagree usefully with Gemma — disagreement rate 10–20% on the uncertain subset.
3. **H3.** Same-family pairs (e.g., Gemma + Gemma smaller) agree too often to be a useful Tier 2.
4. **H4.** Adding Tier 2 reduces the `review_further` queue by ≥70%.
5. **H5.** Models with lower confidence scores (calibration aware) outperform models with uniformly high confidence.
6. **H6.** Prompt determinism (`temperature: 0`) is sufficient; chain-of-thought prompting does not materially improve calibration on this task.

## 3. Ground Truth Set

### 3.1 Composition (to be assembled)
A hand-labeled set of ≥200 relationship candidates from the PD 1096 review output, each labeled by a domain expert as:
- `label`: `keep` / `review_further` / `reject`
- `true_predicate`: the correct predicate if `label != reject` (may differ from the candidate predicate)
- `difficulty`: `easy` / `medium` / `hard` (expert judgement)
- `notes`: free-form rationale

### 3.2 Source
Candidates pulled from `006_System-Manifests/runs/latest_relationship_extraction_sections.json` across multiple PD 1096 extraction runs. Must cover all 7 predicates in the closed vocabulary.

### 3.3 Split
- **Development (70):** used for prompt tuning and manual sanity checks.
- **Test (130):** held out. Only touched for the final measurement. Never shown to the model during tuning.

## 4. Metrics

### 4.1 Per-Decision
- **Accuracy:** `decision == label` on test set.
- **Keep precision:** of model's `keep` decisions, how many are actually `label == keep`.
- **Keep recall:** of ground-truth `keep` cases, how many the model kept.
- **Reject precision / recall:** symmetric.
- **Auto-promote precision (the key metric):** of model's `(decision == keep AND confidence >= 0.90)`, how many are actually `keep`. Must be ≥98% to support auto-promotion without human review.

### 4.2 Calibration
- **Expected Calibration Error (ECE)** across confidence bins [0.0-0.1], [0.1-0.2], …, [0.9-1.0].
- **Brier score** for keep-vs-rest.
- **Confidence histogram** — are all decisions clustered at 0.95, or are they distributed?

### 4.3 Operational
- **Per-candidate latency** (s).
- **Total run time** (min) for the full 200-candidate set.
- **Peak memory** during model load and inference.
- **Timeout rate** — % of candidates exceeding `--timeout-seconds`.

### 4.4 Tier 2 Specific
- **Disagreement rate** with Tier 1 on the uncertain subset.
- **Post-Tier-2 human-escalation rate** — should be <5% of total candidates.
- **Review_further reduction** — should be ≥70%.

## 5. Model Set (candidates)

### 5.1 Tier 1 candidates
| ID | Size | Family | Notes |
|---|---|---|---|
| `gemma4:31b` | 31B | Gemma | Current default. Baseline to beat. |
| `qwen3:30b` | 30B | Qwen | Candidate. |
| `llama3.3:70b` | 70B | Llama | Too slow on Tier 1? Benchmark to find out. |
| `deepseek-v3:37b` | 37B | DeepSeek | Candidate. |

### 5.2 Tier 2 candidates (run only on the uncertain subset from Tier 1)
| ID | Size | Family | Rationale |
|---|---|---|---|
| `qwen3:30b` | 30B | Qwen | Roadmap default. |
| `qwen3:14b` | 14B | Qwen | Faster second pass. |
| `llama3.2:11b` | 11B | Llama | Architectural diversity from Gemma. |
| `deepseek-coder-v2:16b` | 16B | DeepSeek | Architectural diversity; code-trained models sometimes do better on structured output. |

### 5.3 Pairs Under Test
Only architectural-diverse pairings are scored. Same-family pairings (Gemma+Gemma) are included as a control to validate H3.

## 6. Protocol
1. **Freeze the prompt** (currently defined in `.ai/08_prompts/gemma-review.txt`). Same prompt for every Tier 1 model. Tier 2 prompt from `qwen-second-pass.txt`.
2. **Freeze the ground-truth set.** No changes during the run.
3. **Run each Tier 1 model** on all 200 candidates. Record the raw JSON output.
4. **Score against the ground truth** using the metrics in §4.
5. **For the top two Tier 1 candidates**, route their uncertain subsets through each Tier 2 candidate. Score the pair.
6. **Write results** to `results/model_comparison_YYYYMMDDTHHMMSSZ.json`.
7. **Document the winner** in decisions.md as `AD-XXX` and update the default model in `config/vitruvius.yaml`.

## 7. Result Template
```json
{
  "run_id": "",
  "generated_at_utc": "",
  "ground_truth_set_id": "",
  "prompt_version": "",
  "tier_one": {
    "<model_id>": {
      "per_candidate": [{"candidate_id": "", "model_decision": "", "model_confidence": 0.0, "label": ""}],
      "metrics": {
        "accuracy": 0.0,
        "keep_precision": 0.0,
        "keep_recall": 0.0,
        "reject_precision": 0.0,
        "reject_recall": 0.0,
        "auto_promote_precision": 0.0,
        "ece": 0.0,
        "brier": 0.0,
        "latency_p50_ms": 0,
        "latency_p95_ms": 0,
        "peak_memory_mb": 0,
        "timeout_rate": 0.0
      }
    }
  },
  "tier_two_pairs": {
    "<tier_one_id>__<tier_two_id>": {
      "disagreement_rate": 0.0,
      "review_further_reduction": 0.0,
      "post_tier2_human_escalation_rate": 0.0,
      "final_accuracy": 0.0
    }
  },
  "winner_tier_one": "",
  "winner_pair": ""
}
```

## 8. Decision Criteria

### 8.1 Tier 1
Winner is the model with the highest `auto_promote_precision` subject to:
- Accuracy ≥ 80% on the test set.
- Latency p95 ≤ 60s per candidate.
- ECE ≤ 0.10.

If multiple models tie, break by accuracy, then latency, then memory.

### 8.2 Tier 2 Pair
Winner is the pair with the lowest `post_tier2_human_escalation_rate` subject to:
- `review_further_reduction` ≥ 70%.
- `final_accuracy` ≥ 90%.
- Tier 2 latency p95 ≤ 90s.

## 9. Open Questions
- Whether to repeat the experiment quarterly as new models ship.
- Whether to include a cloud model (Claude, GPT, Gemini) as a reference ceiling — pure sanity check, not for production (principle P8: local-first).
- Whether to test a reasoning-model variant (`deepseek-r1`-style) given the higher latency budget Tier 2 has.

## 10. Related Experiments
- `parser-comparison.md` — parser benchmark for Phase 1B (parallel effort, different track).

## Changelog
- **2026-04-14** — Template created. Populated during Sprint C, Phase 6B.
