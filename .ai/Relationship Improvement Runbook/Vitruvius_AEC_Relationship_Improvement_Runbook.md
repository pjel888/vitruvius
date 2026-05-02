# Vitruvius AEC Relationship Improvement Runbook

**Document purpose:** This runbook explains the Vitruvius AEC relationship-improvement workflow in both human-readable and technical terms. It covers the current **Stage 1 Discovery** script, how it uses local Ollama models and optional DeepSeek cloud models, how to run it safely for long periods, what artifacts it writes, how to inspect results, and what to do before scaling to larger runs.

**Audience:** You, future codebase AI agents, and human reviewers/stewards who need to understand what the workflow does before accepting any relationship candidates into the real graph.

**Last updated:** 2026-05-02
**Recommended default mode for long unattended local runs:** `local_only`
**Recommended default mode for faster quality-assisted runs:** `deepseek_local` with fallback to local Ollama
**Recommended terminal progress mode on Windows Git Bash:** `--progress-mode plain`

---

## Table of contents

1. [The big picture](#1-the-big-picture)
2. [The three-stage lifecycle](#2-the-three-stage-lifecycle)
3. [What the current Python workflow actually does](#3-what-the-current-python-workflow-actually-does)
4. [What it does not do yet](#4-what-it-does-not-do-yet)
5. [Your current local model inventory](#5-your-current-local-model-inventory)
6. [Local-only versus DeepSeek-local mode](#6-local-only-versus-deepseek-local-mode)
7. [Why embeddings are used first](#7-why-embeddings-are-used-first)
8. [Relationship decision logic](#8-relationship-decision-logic)
9. [Hierarchy, broader/narrower, and `part_of` guardrails](#9-hierarchy-broadernarrower-and-part_of-guardrails)
10. [Safety model: why this is pending-only](#10-safety-model-why-this-is-pending-only)
11. [Output artifacts and how to read them](#11-output-artifacts-and-how-to-read-them)
12. [What the successful DeepSeek-local test showed](#12-what-the-successful-deepseek-local-test-showed)
13. [Running without DeepSeek credits](#13-running-without-deepseek-credits)
14. [Long-running local-only strategy](#14-long-running-local-only-strategy)
15. [DeepSeek-local strategy with local fallback](#15-deepseek-local-strategy-with-local-fallback)
16. [Windows Git Bash and Ollama setup](#16-windows-git-bash-and-ollama-setup)
17. [Machine safety and thermal safety](#17-machine-safety-and-thermal-safety)
18. [Recommended commands](#18-recommended-commands)
19. [Progress UI, watcher, and output inspection](#19-progress-ui-watcher-and-output-inspection)
20. [Run directory persistence and why explicit run IDs matter](#20-run-directory-persistence-and-why-explicit-run-ids-matter)
21. [Reviewing accepted candidates](#21-reviewing-accepted-candidates)
22. [Scaling plan](#22-scaling-plan)
23. [Troubleshooting](#23-troubleshooting)
24. [Future improvements](#24-future-improvements)
25. [Glossary](#25-glossary)
26. [Reference notes and sources](#26-reference-notes-and-sources)

---

## 1. The big picture

Vitruvius has a large AEC-MEPFS Backbone graph with roughly **10,018 nodes** and **13,670 existing relationships** in the current admitted fixture. The goal of the relationship-improvement workflow is to find possible missing or better relationships between nodes.

In simple terms:

```text
Existing AEC nodes
â†’ turn each node into embedding vectors
â†’ find nearby/related node pairs
â†’ ask AI whether a governed relationship should exist
â†’ validate/correct the AI output
â†’ write pending review artifacts
â†’ do not change the real graph yet
```

The important word is **pending**.

The script is not a graph editor. It is a **relationship discovery and review-candidate generator**.

It can be run with:

- **Local-only models** through Ollama.
- **DeepSeek cloud models** when you have API credits.
- **DeepSeek-local mode**, which uses DeepSeek first and falls back to local models when cloud credits, limits, or rate limits are reached.

The script is designed so that you can run it overnight, over a weekend, or gradually over several days without immediately changing the Explorer knowledge graph or the admitted Backbone file.

---

## 2. The three-stage lifecycle

The relationship-improvement process should be understood as three separate stages.

| Stage | Name | What happens | Visible in Explorer? | Mutates the real graph? |
|---|---|---|---|---|
| 1 | Discovery | AI finds candidate relationships and writes review artifacts. | Not by default | No |
| 2 | Pending visualized overlay | Explorer displays candidate edges as dashed/review-only overlay edges. | Yes, as overlay | No |
| 3 | Accepted/admitted | Human/steward-approved candidates are promoted into the active graph. | Yes, as real graph edges | Yes |

Your current script is **Stage 1**.

That means:

```text
It improves the relationship intelligence layer.
It does not yet improve what you see in the Explorer knowledge graph.
```

For Explorer to show these edges, you need either:

1. A **Stage 2 overlay viewer** that reads candidate artifacts from `semantic-overlays/<run_id>/`, or
2. A **Stage 3 admission workflow** that promotes reviewed candidates into the real graph.

The safer next visible step is Stage 2: visualize pending edges without admitting them.

---

## 3. What the current Python workflow actually does

The command is:

```bash
PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships ...
```

At a high level, it does this:

1. Loads the AEC Backbone file:
   ```text
   scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
   ```

2. Reads:
   ```text
   records       = nodes
   relationships = existing edges
   ```

3. Builds compact text for each selected node using fields such as:
   ```text
   id
   label
   pref_label
   definition
   aliases
   path_code
   level
   parent_path_code
   discipline
   lifecycle_phase
   source_family_ids
   ```

4. Embeds nodes using:
   ```text
   qwen3-embedding:0.6b
   ```

5. Generates likely candidate node pairs using cosine similarity.

6. Sends only likely candidate pairs to the relationship judge.

7. Validates the model response through schema rules and deterministic graph rules.

8. Writes pending artifacts into:
   ```text
   006_System-Manifests/aec-mepfs-backbone/semantic-overlays/<run_id>/
   ```

9. Does not mutate:
   ```text
   admitted_backbone_nodes_l1_l2.json
   Neo4j
   Postgres
   Explorer state
   active graph files
   ```

The scriptâ€™s job is to produce high-quality candidates, not to declare truth.

---

## 4. What it does not do yet

The script does **not**:

- Change the Explorer knowledge graph.
- Add the candidate edges to the official graph.
- Write to Neo4j.
- Write to Postgres.
- Modify the admitted AEC fixture.
- Replace the active graph.
- Automatically admit AI-created relationships as `steward_admitted`.
- Use Kimi by default.
- Browse the internet.
- Fetch external URLs.
- Run every possible node pair through the LLM.

This is intentional.

The current system is built to be conservative because an LLM can propose a plausible but wrong relationship. The workflow creates reviewable artifacts first.

---

## 5. Your current local model inventory

Your local Ollama models are:

```text
deepseek-r1:8b-0528-qwen3-q4_K_M    5.2 GB
qwen3-embedding:0.6b                639 MB
qwen3.5:9b                          6.6 GB
nomic-embed-text:latest             274 MB
qwen2.5:3b                          1.9 GB
llama3.1:8b                         4.9 GB
gemma4:e4b                          listed locally
```

Recommended role assignment:

| Model | Best role | Notes |
|---|---|---|
| `qwen3-embedding:0.6b` | Primary embedding model | Fast, small, and returns 1024-dimensional vectors in your test run. |
| `qwen3.5:9b` | Main local relationship judge | Good balance of accuracy and local GPU fit. |
| `deepseek-r1:8b-0528-qwen3-q4_K_M` | Local verifier/adjudicator | Slower but useful when uncertain decisions need review. |
| `llama3.1:8b` | Backup local judge | Stable fallback. |
| `qwen2.5:3b` | Lightweight fallback | Use on weaker machines or if thermal load is a problem. |
| `nomic-embed-text:latest` | Backup embedding model | Useful if Qwen embedding model has issues. |
| `gemma4:e4b` | Audit/tie-break model | Use sparingly if it is heavier on the machine. |

---

## 6. Local-only versus DeepSeek-local mode

There are two main modes you should use.

### 6.1 `local_only`

This mode uses no cloud credits.

It uses:

```text
Ollama embeddings
Ollama judge
optional Ollama verifier
```

It is slower, but it can run indefinitely as long as the computer stays on and Ollama is running.

Use this when:

- You want zero API cost.
- DeepSeek credits are exhausted.
- You want privacy/local-only processing.
- You want to leave another computer running for a long time.

### 6.2 `deepseek_local`

This mode uses DeepSeek when available, then falls back to local Ollama.

It uses:

```text
qwen3-embedding:0.6b locally
DeepSeek V4 Flash as primary judge
DeepSeek V4 Pro sparingly as adjudicator
qwen3.5:9b as local fallback judge
deepseek-r1:8b as local fallback verifier/adjudicator
```

Use this when:

- You have DeepSeek credits.
- You want faster throughput.
- You want higher-quality judgment on candidate relationships.
- You still want fallback if cloud calls fail.

DeepSeekâ€™s current API docs list `deepseek-v4-flash` and `deepseek-v4-pro` with JSON output support, 1M context length, and OpenAI-compatible base URL `https://api.deepseek.com`.[^deepseek-pricing]

---

## 7. Why embeddings are used first

With about 10,018 nodes, comparing every node to every other node would be huge.

Approximate all-pairs count:

```text
10,018 Ã— 10,017 / 2 = 50,175,153 possible pairs
```

That is too much for a local LLM or even a cheap cloud LLM.

So the script uses embeddings first.

Embeddings are numerical vectors that represent semantic meaning. The script compares vectors to find likely related nodes before asking a judge model to classify a relationship. Ollama documents embeddings as vectors useful for semantic search and retrieval-style workflows.[^ollama-embed]

This means the expensive part only runs on likely pairs.

Instead of:

```text
50 million model calls
```

you run something like:

```text
5,000 candidate pair calls
```

or:

```text
50,000 candidate pair calls
```

depending on your settings.

---

## 8. Relationship decision logic

For each candidate pair, the model is asked whether a governed relationship should exist.

The decision schema expects fields like:

```json
{
  "edge_exists": true,
  "predicate": "broader_than",
  "direction": "A_to_B",
  "confidence": 0.91,
  "relation_type": "taxonomy_hierarchy",
  "relation_category": "taxonomy",
  "relation_nature": ["hierarchical"],
  "rationale": "Node A is the broader parent category of Node B.",
  "evidence": "Node A path_code=ACC; Node B path_code=ACC.ABE.",
  "risk_flags": [],
  "review_recommendation": "accept_candidate"
}
```

Allowed predicates are:

```text
applicable_in_jurisdiction
broader_than
conflicts_with
constrains
evidenced_by
governs
has_facet
maps_to_external_standard
narrower_than
part_of
requires
supersedes
```

Blocked predicates are:

```text
affects
connected_to
related_to
similar_to
```

The blocked predicates are too vague. The point is to build a governed AEC graph, not a loose semantic web of â€œkind of relatedâ€ nodes.

---

## 9. Hierarchy, broader/narrower, and `part_of` guardrails

The first adaptive run found a real issue: the AI sometimes understood hierarchy but chose the wrong predicate direction.

Example of a wrong candidate pattern:

```text
parent --narrower_than--> child
```

The deterministic correction is:

```text
parent --broader_than--> child
```

This is why the workflow now uses `path_code` and `level` as a hard guard.

If:

```text
B.path_code starts with A.path_code + "."
```

then:

```text
A is broader than B
B is narrower than A
```

The current preferred canonical representation is:

```text
parent --broader_than--> child
```

This follows the general SKOS idea that broader/narrower are inverse hierarchical relationships.[^skos-primer]

### Why `part_of` is guarded

`part_of` is not the same as taxonomy hierarchy.

A path-code parent/child relationship means:

```text
A is a broader taxonomy category than B
```

It does not automatically mean:

```text
B is physically or compositionally part of A
```

So if the only evidence is path-code hierarchy, the script should not accept `part_of`. It should convert the relationship into the canonical hierarchy predicate or downgrade it to review.

---

## 10. Safety model: why this is pending-only

The workflow is pending-only because:

1. LLMs can make plausible mistakes.
2. The graph has governance implications.
3. Some relationships are regulatory, safety-critical, or directional.
4. A wrong edge can mislead retrieval, graph traversal, or downstream reasoning.
5. You need a human/steward review phase before admission.

The script writes:

```text
candidate artifacts
accepted-by-workflow candidates
rejected candidates
validation error records
logs
checkpoints
reports
```

It does not write active graph edges.

This is the correct safety posture.

The phrase â€œaccepted relationshipâ€ in the output means:

```text
accepted by the discovery workflow as a strong candidate
```

It does **not** mean:

```text
accepted into the official graph
```

---

## 11. Output artifacts and how to read them

Each run writes into:

```text
006_System-Manifests/aec-mepfs-backbone/semantic-overlays/<run_id>/
```

Important files:

| File | Purpose |
|---|---|
| `relationship-improvement.log` | Main run log. |
| `relationship-improvement-checkpoint.json` | Resume/progress state. |
| `relationship-improvement-report.json` | Final summary metrics. |
| `relationship-improvement-events.jsonl` | Event stream for watcher/progress. |
| `similarity-candidates.jsonl` | Candidate pairs selected by embedding similarity. |
| `accepted-relationships.jsonl` | Strong AI candidates that passed final guards. |
| `candidate-relationships.jsonl` | Needs-review candidates. |
| `rejected-relationships.jsonl` | Rejected pairs and reasons. |
| `validation-errors.jsonl` | Schema/JSON/model-output validation diagnostics. |
| `accepted-relationships-review.tsv` | Human-friendly review table. |
| `rejected-relationships-review.tsv` | Human-friendly rejected table. |
| `relationship-improvement-summary.txt` | Human-readable run summary. |
| `fatal-error.json` | Should exist only if the run crashes. |
| `run-started.json` | Should be created at run start after the persistence fix. |

### How to count artifacts

```bash
RUN_ID=<RUN_ID>
OUT="006_System-Manifests/aec-mepfs-backbone/semantic-overlays/$RUN_ID"

ls -lah "$OUT"
wc -l "$OUT"/*.jsonl
```

### How to read the report

```bash
python -m json.tool "$OUT/relationship-improvement-report.json"
```

### How to inspect accepted candidates

```bash
head -n 5 "$OUT/accepted-relationships.jsonl"
column -t -s $'\t' "$OUT/accepted-relationships-review.tsv" | less -S
```

---

## 12. What the successful DeepSeek-local test showed

A successful test run completed with:

```text
run_id: 20260502T005618Z
mode: deepseek_local
nodes selected: 50
candidate pairs: 100
processed pairs: 100
accepted: 12
needs_review: 1
rejected: 87
errors: 0
cloud calls: 105
DeepSeek Flash calls: 101
DeepSeek Pro calls: 4
local fallback calls: 0
estimated DeepSeek cost: about $0.031329
budget: $1.00
hierarchy normalizations: 4
taxonomy part_of conversions: 0
```

This is a good test result.

What it means:

- The workflow can complete a 100-pair run.
- DeepSeek was stable.
- Kimi was not needed and remains disabled.
- The hierarchy normalization is working.
- Cost was tiny relative to the test budget.
- The output remained pending-only.

The only remaining concerns from that run were validation diagnostics and run-directory persistence on a later run.

---

## 13. Running without DeepSeek credits

Yes, you can run without DeepSeek.

Use:

```text
--council-mode local_only
```

That uses only local Ollama models. It does not need internet and does not consume API credits.

This is the mode to use for a long unattended run on another computer.

The tradeoff:

```text
local_only = slower, free, private, unlimited by credits
deepseek_local = faster, higher-quality cloud judge, credit-limited
```

If you run `deepseek_local` and DeepSeek credits or limits run out, the script can fall back to local models if these flags are enabled:

```bash
--fallback-to-local-on-cloud-exhaustion
--fallback-to-local-on-cloud-error
--fallback-to-local-on-rate-limit
```

But if you are deliberately trying to run for a very long time, use `local_only` from the beginning.

---

## 14. Long-running local-only strategy

For long unattended runs:

1. Use a fixed `RUN_ID`.
2. Start with a reasonable `--max-pairs`.
3. Use `--resume` when continuing.
4. Increase `--max-pairs` over time.
5. Keep progress mode plain.
6. Keep local model calls sequential.
7. Avoid verifier at first.
8. Review accepted outputs before scaling further.

### Why same run ID matters

If you start a new run ID every time, the script may rediscover some of the same pairs.

If you use:

```text
same run_id + --resume
```

then it can skip pairs already processed in that run.

Example long-run ID:

```bash
RUN_ID=local_backbone_longrun_001
```

Start with:

```text
5,000 pairs
```

Then resume with:

```text
10,000 pairs
25,000 pairs
50,000 pairs
```

---

## 15. DeepSeek-local strategy with local fallback

Use `deepseek_local` when you want speed and are comfortable sending node text to DeepSeek.

The intended routing is:

```text
Embeddings:
  local Ollama qwen3-embedding:0.6b

Primary judge:
  DeepSeek V4 Flash

Adjudicator:
  DeepSeek V4 Pro sparingly

Fallback judge:
  local Ollama qwen3.5:9b

Fallback verifier/adjudicator:
  local Ollama deepseek-r1:8b
```

DeepSeek JSON mode should use:

```json
{
  "response_format": {"type": "json_object"},
  "thinking": {"type": "disabled"},
  "max_tokens": 700,
  "stream": false
}
```

DeepSeekâ€™s JSON mode documentation says to set `response_format`, include the word â€œjsonâ€ and an example shape in the prompt, and set `max_tokens` high enough to avoid truncation.[^deepseek-json]

The script should still validate the result. JSON mode means â€œvalid JSON string,â€ not â€œguaranteed correct graph relationship.â€

---

## 16. Windows Git Bash and Ollama setup

On Windows, Ollama inherits user/system environment variables after Ollama is restarted.[^ollama-faq]

Use Git Bash to set the conservative Ollama server settings through PowerShell:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "
[Environment]::SetEnvironmentVariable('OLLAMA_MAX_LOADED_MODELS','1','User');
[Environment]::SetEnvironmentVariable('OLLAMA_NUM_PARALLEL','1','User');
[Environment]::SetEnvironmentVariable('OLLAMA_CONTEXT_LENGTH','4096','User');
[Environment]::SetEnvironmentVariable('OLLAMA_KEEP_ALIVE','0','User');
[Environment]::SetEnvironmentVariable('OLLAMA_FLASH_ATTENTION','1','User');
[Environment]::SetEnvironmentVariable('OLLAMA_KV_CACHE_TYPE','q8_0','User');
"
```

Then restart Ollama:

```text
Taskbar tray â†’ Ollama â†’ Quit
Start Menu â†’ Ollama
```

Verify:

```bash
powershell.exe -NoProfile -Command "
'OLLAMA_MAX_LOADED_MODELS=' + [Environment]::GetEnvironmentVariable('OLLAMA_MAX_LOADED_MODELS','User');
'OLLAMA_NUM_PARALLEL=' + [Environment]::GetEnvironmentVariable('OLLAMA_NUM_PARALLEL','User');
'OLLAMA_CONTEXT_LENGTH=' + [Environment]::GetEnvironmentVariable('OLLAMA_CONTEXT_LENGTH','User');
'OLLAMA_KEEP_ALIVE=' + [Environment]::GetEnvironmentVariable('OLLAMA_KEEP_ALIVE','User');
'OLLAMA_FLASH_ATTENTION=' + [Environment]::GetEnvironmentVariable('OLLAMA_FLASH_ATTENTION','User');
'OLLAMA_KV_CACHE_TYPE=' + [Environment]::GetEnvironmentVariable('OLLAMA_KV_CACHE_TYPE','User');
"
```

### Verify model GPU placement

```bash
curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5:9b","prompt":"Reply with only: ok","stream":false,"think":false,"keep_alive":"60s"}'

ollama ps
```

You want:

```text
PROCESSOR 100% GPU
CONTEXT   4096
```

Ollama documents that `ollama ps` shows whether the model is loaded fully on GPU, CPU, or split between both.[^ollama-faq]

---

## 17. Machine safety and thermal safety

Your main machine:

```text
CPU: i9
RAM: 64 GB
GPU: RTX 4070, 12 GB VRAM
```

Safe local settings:

```text
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_NUM_PARALLEL=1
OLLAMA_CONTEXT_LENGTH=4096
OLLAMA_KEEP_ALIVE=0
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
```

Why this matters:

- One loaded model reduces VRAM pressure.
- One parallel request reduces heat and memory spikes.
- A 4096 context is conservative for 12 GB VRAM.
- `keep_alive=0` unloads models quickly.
- Lower concurrency is better for unattended overnight runs.

Ollamaâ€™s context docs warn that larger context length increases memory requirements and recommend checking offloading using `ollama ps`.[^ollama-context]

### If using a weaker second computer

Use:

```bash
--judge-model qwen2.5:3b
```

instead of:

```bash
--judge-model qwen3.5:9b
```

It will be less accurate but easier on the machine.

### Thermal best practices

For unattended runs:

- Keep the PC on a hard surface with airflow.
- Disable sleep.
- Make sure fans are clean.
- Prefer `--sleep-seconds 2` or more.
- Avoid verifier at first.
- Use `--progress-mode plain`.
- Use `ollama ps` occasionally.
- Use Windows Task Manager or GPU monitoring tools to verify temperatures.

---

## 18. Recommended commands

### 18.1 Local-only 50-node smoke test

```bash
PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --council-mode local_only \
  --max-nodes 50 \
  --max-pairs 100 \
  --candidate-top-k 10 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --embedding-model qwen3-embedding:0.6b \
  --judge-model qwen3.5:9b \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain \
  --sleep-seconds 2
```

### 18.2 Local-only long run

```bash
RUN_ID=local_backbone_longrun_001

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode local_only \
  --max-nodes 1000 \
  --max-pairs 5000 \
  --candidate-top-k 20 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --embedding-model qwen3-embedding:0.6b \
  --judge-model qwen3.5:9b \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain \
  --sleep-seconds 2
```

### 18.3 Resume the local-only long run

```bash
RUN_ID=local_backbone_longrun_001

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --resume \
  --council-mode local_only \
  --max-nodes 1000 \
  --max-pairs 10000 \
  --candidate-top-k 20 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --embedding-model qwen3-embedding:0.6b \
  --judge-model qwen3.5:9b \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain \
  --sleep-seconds 2
```

### 18.4 Local-only with local verifier

This is slower but stronger.

```bash
RUN_ID=local_verified_001

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode local_only \
  --max-nodes 1000 \
  --max-pairs 5000 \
  --candidate-top-k 20 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --verify-threshold 0.65 \
  --verify-uncertain \
  --embedding-model qwen3-embedding:0.6b \
  --judge-model qwen3.5:9b \
  --verifier-model deepseek-r1:8b-0528-qwen3-q4_K_M \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain \
  --sleep-seconds 2 \
  --verifier-sleep-seconds 3
```

### 18.5 DeepSeek-local 50-node test

```bash
export DEEPSEEK_API_KEY="$(powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" | tr -d '\r')"

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --council-mode deepseek_local \
  --allow-cloud-ai \
  --cloud-preflight \
  --max-nodes 50 \
  --max-pairs 100 \
  --candidate-top-k 10 \
  --cloud-cost-budget-usd 1.00 \
  --deepseek-flash-max-calls 150 \
  --deepseek-pro-max-calls 5 \
  --adjudicator-provider auto \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain
```

### 18.6 DeepSeek-local 250-node next run

```bash
export DEEPSEEK_API_KEY="$(powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" | tr -d '\r')"

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --council-mode deepseek_local \
  --allow-cloud-ai \
  --cloud-preflight \
  --max-nodes 250 \
  --max-pairs 500 \
  --candidate-top-k 10 \
  --verify-uncertain \
  --adjudicate-disagreements \
  --high-impact-pro-adjudication \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --deepseek-flash-max-calls 750 \
  --deepseek-pro-max-calls 20 \
  --cloud-total-max-calls 800 \
  --cloud-cost-budget-usd 2.00 \
  --progress-mode plain \
  --sleep-seconds 2 \
  --deepseek-sleep-seconds 1
```

### 18.7 DeepSeek-local 1000-node run

```bash
export DEEPSEEK_API_KEY="$(powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" | tr -d '\r')"

RUN_ID=deepseek_local_1000_001

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode deepseek_local \
  --allow-cloud-ai \
  --cloud-preflight \
  --max-nodes 1000 \
  --max-pairs 5000 \
  --candidate-top-k 20 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --verify-threshold 0.65 \
  --verify-uncertain \
  --adjudicate-disagreements \
  --high-impact-pro-adjudication \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --embedding-model qwen3-embedding:0.6b \
  --judge-provider auto \
  --verifier-provider auto \
  --adjudicator-provider auto \
  --deepseek-base-url https://api.deepseek.com \
  --deepseek-flash-model deepseek-v4-flash \
  --deepseek-pro-model deepseek-v4-pro \
  --deepseek-api-key-env DEEPSEEK_API_KEY \
  --deepseek-flash-max-calls 7500 \
  --deepseek-pro-max-calls 100 \
  --cloud-total-max-calls 7600 \
  --cloud-cost-budget-usd 10.00 \
  --fallback-to-local-on-cloud-exhaustion \
  --fallback-to-local-on-cloud-error \
  --fallback-to-local-on-rate-limit \
  --progress-mode plain \
  --sleep-seconds 2 \
  --deepseek-sleep-seconds 1 \
  --resume
```

---

## 19. Progress UI, watcher, and output inspection

Use plain mode in Git Bash:

```bash
--progress-mode plain
```

Rich mode can display repeated panels in Git Bash unless the terminal supports in-place redraw well. The safer default is plain mode.

### Watch latest run

If the watcher command exists:

```bash
PYTHONPATH=scripts python scripts/pipeline_cli.py aec-watch-relationship-run \
  --watch-latest \
  --progress-mode plain
```

### Watch a specific run

```bash
PYTHONPATH=scripts python scripts/pipeline_cli.py aec-watch-relationship-run \
  --run-id <RUN_ID> \
  --progress-mode plain
```

### Manually inspect a run

```bash
RUN_ID=<RUN_ID>
OUT="006_System-Manifests/aec-mepfs-backbone/semantic-overlays/$RUN_ID"

ls -lah "$OUT"
python -m json.tool "$OUT/relationship-improvement-report.json"
tail -n 50 "$OUT/relationship-improvement.log"
wc -l "$OUT"/*.jsonl
```

---

## 20. Run directory persistence and why explicit run IDs matter

A later run printed an output path for:

```text
20260502T020143Z
```

but the directory was not visible afterward.

That should not happen. A robust version of the script should create the output directory immediately, before preflight or model calls, and write:

```text
run-started.json
relationship-improvement-checkpoint.json
relationship-improvement-events.jsonl
```

before any long-running work.

Until that is verified, use explicit run IDs and immediately check that the folder exists.

### No-model directory smoke test

```bash
RUN_ID=debug_run_dir_$(date -u +%Y%m%dT%H%M%SZ)

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode local_only \
  --max-nodes 0 \
  --max-pairs 0 \
  --progress-mode plain

test -d "006_System-Manifests/aec-mepfs-backbone/semantic-overlays/$RUN_ID" && echo "RUN DIR EXISTS"

ls -lah "006_System-Manifests/aec-mepfs-backbone/semantic-overlays/$RUN_ID"
```

The folder should exist every time.

---

## 21. Reviewing accepted candidates

Do not blindly accept candidates into the real graph.

Review in this order:

1. Open:
   ```text
   accepted-relationships-review.tsv
   ```

2. Check:
   ```text
   edge_key
   predicate
   confidence_score
   raw_similarity
   rationale
   evidence
   normalization_applied
   final_guard_checks
   ```

3. Verify that:
   - `broader_than` edges follow path hierarchy.
   - `part_of` is not used for taxonomy-only relationships.
   - `requires`, `constrains`, `governs`, and `supersedes` have clear evidence.
   - `conflicts_with` truly indicates incompatibility.
   - The rationale is not just generic language.
   - Evidence quotes come from node fields.

4. Move questionable edges to manual review.

5. Only after review should a future Stage 3 admission workflow promote selected candidates.

---

## 22. Scaling plan

Recommended scaling sequence:

```text
Step 1:  50 nodes / 100 pairs
Step 2:  250 nodes / 500 pairs
Step 3:  1000 nodes / 5000 pairs
Step 4:  1000 nodes / 10000 pairs
Step 5:  5000 nodes / 25000 pairs
Step 6:  10018 nodes / 50000+ pairs
```

Do not jump directly to full scale until:

- The output directory creation bug is fixed.
- Validation errors are understandable.
- Accepted candidate quality looks good.
- You have reviewed a sample of accepted candidates.
- The machine stays stable on long runs.
- You know whether you want DeepSeek or local-only.

For local-only, the main cost is time.

For DeepSeek-local, the main cost is API usage. DeepSeek reports token usage fields such as `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens`, `completion_tokens`, and `total_tokens`; these should be used for cost reporting.[^deepseek-api]

---

## 23. Troubleshooting

### Problem: DeepSeek credits run out

Use:

```bash
--council-mode local_only
```

or keep:

```bash
--fallback-to-local-on-cloud-exhaustion
```

### Problem: DeepSeek returns malformed schema

Check:

```text
validation-errors.jsonl
rejected-relationships.jsonl
relationship-improvement-report.json
```

The script should keep running and reject unsafe model outputs.

### Problem: Kimi 403

Kimi Code is disabled by default. Do not use it for this workflow unless a future compatible endpoint is available.

### Problem: Rich progress output repeats panels

Use:

```bash
--progress-mode plain
```

### Problem: output directory missing

Use explicit run IDs and run the no-model directory smoke test. The directory should be created before model calls.

### Problem: local model spills into CPU

Check:

```bash
ollama ps
```

If not `100% GPU`, reduce model size, context, or use:

```bash
--judge-model qwen2.5:3b
```

### Problem: local-only run is too slow

Options:

- Reduce `--max-pairs`.
- Increase `--min-similarity`.
- Reduce `--candidate-top-k`.
- Disable `--verify-uncertain`.
- Use `qwen2.5:3b`.
- Use DeepSeek-local for bulk judging when credits are available.

---

## 24. Future improvements

Useful future improvements:

1. **Stage 2 Explorer overlay**
   - Show candidate edges visually without admission.
   - Use dashed edges, confidence labels, and review buttons.

2. **Global processed-pair ledger**
   - Avoid repeating the same pair across different run IDs.

3. **Relationship candidate ranking**
   - Sort by confidence, novelty, importance, and predicate type.

4. **Human review queue**
   - Allow accept/reject/escalate decisions.

5. **Stage 3 admission workflow**
   - Backup active graph.
   - Apply reviewed candidates.
   - Validate graph quality.
   - Write a new admitted graph artifact.

6. **Automated quality dashboards**
   - Acceptance rate.
   - Validation error rate.
   - Cost per accepted candidate.
   - Normalization counts.
   - Predicate distribution.

7. **Offline marathon mode**
   - Run local-only in windows.
   - Automatically pause on high thermal load.
   - Resume after cooling period.

8. **Graph coverage analysis**
   - Identify underconnected clusters.
   - Prioritize nodes with weak interrelationship coverage.

---

## 25. Glossary

### AEC-MEPFS

Architecture, Engineering, Construction, Mechanical, Electrical, Plumbing, Fire Safety.

### Backbone node

A governed node in the AEC-MEPFS taxonomy/knowledge backbone.

### Edge / relationship

A directed or governed connection between two nodes.

### Predicate

The main relationship type, such as `broader_than`, `requires`, or `governs`.

### Candidate pair

A pair of nodes selected by embedding similarity for relationship evaluation.

### Accepted candidate

A relationship proposal that passed model judgment and deterministic validation. It is not yet admitted into the real graph.

### Pending artifact

A file written under `semantic-overlays/<run_id>/` for review.

### Stage 1 Discovery

AI-assisted candidate generation.

### Stage 2 Pending overlay

Explorer visualization of pending candidates without graph mutation.

### Stage 3 Admitted graph

Reviewed candidates are promoted into the official graph.

### Embedding

A numeric vector representation of text.

### Cosine similarity

A way to measure how similar two embedding vectors are.

### DeepSeek Flash

The cheaper/faster DeepSeek model used for bulk judging.

### DeepSeek Pro

The stronger DeepSeek model used sparingly for adjudication.

### Local fallback

Switching to local Ollama models when cloud calls fail, hit caps, or run out of budget.

### Hierarchy normalization

A deterministic correction that ensures parent/child path-code relationships use the correct broader/narrower direction.

### `part_of` guard

A validation rule that prevents taxonomy hierarchy from being mislabeled as compositional containment.

---

## 26. Reference notes and sources

The runbook relies on three kinds of evidence:

1. **Your local Vitruvius test artifacts**
   - Completed run `20260502T005618Z`.
   - Earlier adaptive run `20260501T163117Z`.
   - Uploaded checkpoint/report/pasted terminal logs.

2. **Official Ollama documentation**
   - Windows environment variables and `ollama ps` GPU/CPU processor display.
   - Context length and memory requirements.
   - Local generate endpoint, structured output, `think`, and `keep_alive`.

3. **Official DeepSeek documentation**
   - Model names, context length, JSON output support, pricing.
   - JSON output mode requirements.
   - Token usage fields and finish reasons.

4. **W3C SKOS documentation**
   - Broader/narrower inverse relationship semantics.

### Source links

[^ollama-faq]: Ollama FAQ: Windows environment variables, `ollama ps` GPU/CPU display, local data notes. https://docs.ollama.com/faq

[^ollama-context]: Ollama context length docs: larger context increases memory requirements; `ollama ps` shows processor/context. https://docs.ollama.com/context-length

[^ollama-generate]: Ollama generate API: `format`, `stream`, `think`, `keep_alive`, generation options. https://docs.ollama.com/api/generate

[^ollama-structured]: Ollama structured outputs: JSON schema enforcement for structured model responses. https://docs.ollama.com/capabilities/structured-outputs

[^ollama-embed]: Ollama embedding API/capabilities. https://docs.ollama.com/capabilities/embeddings

[^deepseek-pricing]: DeepSeek Models & Pricing: `deepseek-v4-flash`, `deepseek-v4-pro`, 1M context, JSON output, pricing, V4 Pro discount note. https://api-docs.deepseek.com/quick_start/pricing

[^deepseek-v4]: DeepSeek V4 Preview Release: Flash/Pro roles and 1M context. https://api-docs.deepseek.com/news/news260424

[^deepseek-json]: DeepSeek JSON Output guide: use `response_format: {"type":"json_object"}`, include the word JSON and an example, set `max_tokens` to avoid truncation. https://api-docs.deepseek.com/guides/json_mode

[^deepseek-api]: DeepSeek Create Chat Completion API: model choices, thinking mode, `max_tokens`, `response_format`, finish reasons, usage token fields. https://api-docs.deepseek.com/api/create-chat-completion

[^skos-primer]: W3C SKOS Primer: `skos:broader` and `skos:narrower` are inverse hierarchical relations. https://www.w3.org/TR/skos-primer/

---

## Appendix A â€” Minimal local-only marathon checklist

Before leaving a computer running:

```text
[ ] Ollama is running.
[ ] `ollama ps` shows 100% GPU when model is loaded.
[ ] Windows sleep is disabled.
[ ] Fans/airflow are okay.
[ ] Use `--progress-mode plain`.
[ ] Use a fixed `RUN_ID`.
[ ] Use `--resume` when continuing.
[ ] Start with 1000 nodes / 5000 pairs, not full graph.
[ ] Review accepted TSV before scaling.
[ ] Confirm output directory exists.
[ ] Keep pending-only mode.
```

Command:

```bash
RUN_ID=local_backbone_longrun_001

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id "$RUN_ID" \
  --council-mode local_only \
  --max-nodes 1000 \
  --max-pairs 5000 \
  --candidate-top-k 20 \
  --min-similarity 0.35 \
  --accept-threshold 0.85 \
  --embedding-model qwen3-embedding:0.6b \
  --judge-model qwen3.5:9b \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain \
  --sleep-seconds 2
```

---

## Appendix B â€” Minimal DeepSeek-local checklist

```text
[ ] DEEPSEEK_API_KEY is set in Git Bash.
[ ] Cloud budget is low for first test.
[ ] DeepSeek Flash cap is higher than max-pairs.
[ ] DeepSeek Pro cap is small.
[ ] Fallback flags are enabled.
[ ] Kimi remains disabled.
[ ] Progress mode is plain.
```

Command:

```bash
export DEEPSEEK_API_KEY="$(powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" | tr -d '\r')"

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --council-mode deepseek_local \
  --allow-cloud-ai \
  --cloud-preflight \
  --max-nodes 50 \
  --max-pairs 100 \
  --candidate-top-k 10 \
  --cloud-cost-budget-usd 1.00 \
  --deepseek-flash-max-calls 150 \
  --deepseek-pro-max-calls 5 \
  --adjudicator-provider auto \
  --hierarchy-canonical-predicate broader_than \
  --convert-taxonomy-part-of \
  --progress-mode plain
```

---

## Appendix C â€” The important principle

The right philosophy is:

```text
Let embeddings find possible neighbors.
Let the model judge only likely pairs.
Let deterministic graph rules correct hierarchy.
Let schema validation reject unsafe output.
Let humans review accepted candidates.
Only later admit selected edges into the real graph.
```

This gives you slow, safe, compounding improvement without turning the system into an uncontrolled graph mutation agent.
