# 05 LLM Review Layer

## Model
gemma4:31b via Ollama

## Role
Review candidate relationships, not generate them.

## Output
- decision: keep / review_further / reject
- confidence
- reason
- suggested_type

## Pipeline
Extraction → LLM Review → Human Spot Check

## Philosophy
- Deterministic first
- AI validates, not invents

## Result
Scalable review without manual bottlenecks.


Generated: 2026-04-13T09:19:33.876131