"""Pending-only AEC Backbone relationship improvement workflow.

This module proposes relationship-improvement artifacts for steward review.
It deliberately never mutates active graph files, Neo4j, or Postgres.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import math
import os
import re
import sys
import time
import traceback
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import UTC, datetime
from ipaddress import ip_address
from pathlib import Path
from typing import Any, Callable, Iterator, Literal
from urllib.parse import urlparse

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from vitruvius.paths import get_repo_root


DEFAULT_INPUT_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_OUTPUT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/semantic-overlays")
DEFAULT_EMBEDDING_MODEL = "qwen3-embedding:0.6b"
DEFAULT_JUDGE_MODEL = "qwen3.5:9b"
DEFAULT_VERIFIER_MODEL = "deepseek-r1:8b-0528-qwen3-q4_K_M"
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_KIMI_BASE_URL = "https://api.kimi.com/coding/v1"
DEFAULT_KIMI_MODEL = "kimi-for-coding"
DEFAULT_KIMI_API_KEY_ENV = "KIMI_API_KEY"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_DEEPSEEK_FLASH_MODEL = "deepseek-v4-flash"
DEFAULT_DEEPSEEK_PRO_MODEL = "deepseek-v4-pro"
DEFAULT_DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"

COUNCIL_MODES = (
    "local_only",
    "deepseek_local",
    "cloud_first",
    "adaptive_cloud",
    "local_first_cloud_verify",
    "audit_only",
)
PROVIDERS = ("ollama", "kimi", "deepseek")
PROVIDER_CHOICES = ("ollama", "kimi", "deepseek", "auto")
ADJUDICATOR_PROVIDER_CHOICES = ("none", "ollama", "kimi", "deepseek", "auto")
DEEPSEEK_LOCAL_MODES = ("deepseek_local", "adaptive_cloud")
DEEPSEEK_ENABLED_MODES = ("deepseek_local", "adaptive_cloud", "cloud_first", "local_first_cloud_verify", "audit_only")
PROGRESS_MODES = ("auto", "rich", "plain", "off")
RUN_PHASES = (
    "loading",
    "embedding",
    "candidate_generation",
    "judging",
    "verifying",
    "adjudicating",
    "writing_report",
    "completed",
    "interrupted",
    "error",
)
MAX_RECENT_EVENTS = 50
MAX_RAW_RESPONSE_EXCERPT_CHARS = 1000
KIMI_ALLOWED_BASE_URLS = {
    "https://api.kimi.com/coding/v1",
    "https://api.moonshot.ai/v1",
    "https://api.moonshot.cn/v1",
}
DEEPSEEK_ALLOWED_BASE_URLS = {"https://api.deepseek.com"}
HIGH_IMPACT_PREDICATES = {
    "applicable_in_jurisdiction",
    "conflicts_with",
    "constrains",
    "governs",
    "requires",
    "supersedes",
}
HIGH_IMPACT_TERMS = ("safety", "safety-critical", "regulatory", "risk", "failure")

DEEPSEEK_PRICE_PER_MILLION = {
    "deepseek-v4-flash": {
        "input_cache_hit": 0.0028,
        "input_cache_miss": 0.14,
        "output": 0.28,
    },
    "deepseek-v4-pro": {
        "input_cache_hit": 0.003625,
        "input_cache_miss": 0.435,
        "output": 0.87,
    },
}

ALLOWED_PREDICATES = (
    "applicable_in_jurisdiction",
    "broader_than",
    "conflicts_with",
    "constrains",
    "evidenced_by",
    "governs",
    "has_facet",
    "maps_to_external_standard",
    "narrower_than",
    "part_of",
    "requires",
    "supersedes",
)
BLOCKED_PREDICATES = {"affects", "connected_to", "related_to", "similar_to"}
DECISION_PREDICATES = ("none", *ALLOWED_PREDICATES)
HIERARCHY_CANONICAL_PREDICATES = ("broader_than", "narrower_than")

PREDICATE_LITERAL = Literal[
    "none",
    "applicable_in_jurisdiction",
    "broader_than",
    "conflicts_with",
    "constrains",
    "evidenced_by",
    "governs",
    "has_facet",
    "maps_to_external_standard",
    "narrower_than",
    "part_of",
    "requires",
    "supersedes",
]
DIRECTION_LITERAL = Literal["A_to_B", "B_to_A", "undirected", "none"]

GENERATION_METHOD = "local_ollama_relationship_improvement_v1"
PROVENANCE_NOTE = "Proposed by local Ollama relationship-improvement run; pending steward review."

logger = logging.getLogger("vitruvius.kg.aec_relationship_improvement")


class ApplyModeDeferredError(RuntimeError):
    """Raised when a caller requests active graph mutation for this v1 workflow."""


class ExternalNetworkDisabledError(RuntimeError):
    """Raised when a configured model endpoint is not a loopback HTTP endpoint."""


class CloudAIRequiredError(RuntimeError):
    """Raised when cloud council mode is requested without explicit opt-in."""


class CloudProviderError(RuntimeError):
    """Raised for cloud provider failures that can trigger fallback."""

    def __init__(
        self,
        provider: str,
        reason: str,
        message: str,
        *,
        status_code: int | None = None,
        retryable: bool = True,
    ) -> None:
        super().__init__(message)
        self.provider = provider
        self.reason = reason
        self.status_code = status_code
        self.retryable = retryable


class CloudResponseRejectedError(ValueError):
    """Raised when a provider response is syntactically present but unsafe to use."""

    def __init__(
        self,
        reason: str,
        message: str,
        *,
        provider: str | None = None,
        model: str | None = None,
        raw_response: str | None = None,
        finish_reason: str | None = None,
        usage: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.reason = reason
        self.provider = provider
        self.model = model
        self.raw_response = raw_response
        self.finish_reason = finish_reason
        self.usage = usage or {}


class MalformedModelJSONError(ValueError):
    """Raised when a model response is not parseable JSON."""


class BlockedPredicateError(ValueError):
    """Raised when a model emits an explicitly blocked predicate."""


class UnsafeDecisionError(ValueError):
    """Raised when a parsed decision violates governed relationship rules."""


class RoleValidationError(ValueError):
    """Raised when a specific council role emits an invalid decision."""

    def __init__(
        self,
        reason: str,
        message: str,
        *,
        role: str | None = None,
        raw_response: str | None = None,
        error_type: str = "semantic_validation_error",
        pydantic_errors: list[dict[str, Any]] | None = None,
        failed_fields: list[str] | None = None,
        repair_attempted: bool = False,
        repair_successful: bool = False,
        normalization_steps: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.reason = reason
        self.role = role
        self.raw_response = raw_response
        self.error_type = error_type
        self.pydantic_errors = pydantic_errors or []
        self.failed_fields = failed_fields or []
        self.repair_attempted = repair_attempted
        self.repair_successful = repair_successful
        self.normalization_steps = normalization_steps or []


@dataclass(frozen=True)
class BackboneNodeView:
    id: str
    canonical_id: str = ""
    record_type: str = ""
    label: str = ""
    pref_label: str = ""
    definition: str = ""
    aliases: tuple[str, ...] = ()
    path_code: str = ""
    level: str = ""
    parent_path_code: str = ""
    review_status: str = ""
    release_version: str = ""
    discipline: tuple[str, ...] = ()
    lifecycle_phase: tuple[str, ...] = ()
    source_family_ids: tuple[str, ...] = ()
    semantic_overlay_category: str = ""
    generation_method: str = ""
    provenance_note: str = ""
    visibility: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    def compact_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "canonical_id": self.canonical_id,
            "record_type": self.record_type,
            "label": self.label,
            "pref_label": self.pref_label,
            "definition": self.definition,
            "aliases": list(self.aliases),
            "path_code": self.path_code,
            "level": self.level,
            "parent_path_code": self.parent_path_code,
            "review_status": self.review_status,
            "release_version": self.release_version,
            "discipline": list(self.discipline),
            "lifecycle_phase": list(self.lifecycle_phase),
            "source_family_ids": list(self.source_family_ids),
            "semantic_overlay_category": self.semantic_overlay_category,
            "generation_method": self.generation_method,
            "provenance_note": self.provenance_note,
            "visibility": self.visibility,
        }


@dataclass(frozen=True)
class ExistingEdgeView:
    from_id: str
    to_id: str
    predicate: str
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def edge_key(self) -> str:
        return build_edge_key(self.from_id, self.predicate, self.to_id)

    @property
    def pair_key(self) -> str:
        return build_pair_key(self.from_id, self.to_id)


class EmbeddingRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "aec-node-embedding/v1"
    node_id: str
    embedding_model: str
    embedding_dimensions: int
    text_hash: str
    text: str | None = None
    embedding: list[float]
    created_at_utc: str

    @field_validator("embedding_dimensions")
    @classmethod
    def _positive_dimensions(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("embedding_dimensions must be positive")
        return value

    @model_validator(mode="after")
    def _dimension_matches_embedding(self) -> "EmbeddingRecord":
        if len(self.embedding) != self.embedding_dimensions:
            raise ValueError("embedding length does not match embedding_dimensions")
        return self


@dataclass(frozen=True)
class CandidatePair:
    run_id: str
    node_pair_key: str
    node_a_id: str
    node_b_id: str
    similarity: float
    embedding_model: str
    created_at_utc: str

    def to_record(self) -> dict[str, Any]:
        return {
            "schema_version": "aec-relationship-candidate-pair/v1",
            "run_id": self.run_id,
            "node_pair_key": self.node_pair_key,
            "node_a_id": self.node_a_id,
            "node_b_id": self.node_b_id,
            "similarity": self.similarity,
            "embedding_model": self.embedding_model,
            "created_at_utc": self.created_at_utc,
        }


class RelationshipDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge_exists: bool
    predicate: PREDICATE_LITERAL
    direction: DIRECTION_LITERAL
    confidence: float = Field(ge=0.0, le=1.0)
    relation_type: str
    relation_category: str
    relation_nature: list[str]
    rationale: str
    evidence: str
    risk_flags: list[str]
    review_recommendation: Literal["accept_candidate", "needs_review", "reject"]

    @model_validator(mode="after")
    def _governed_relationship_rules(self) -> "RelationshipDecision":
        if not self.edge_exists:
            if self.predicate != "none":
                raise ValueError("predicate must be none when edge_exists is false")
            if self.direction != "none":
                raise ValueError("direction must be none when edge_exists is false")
            if self.confidence > 0.49 and self.review_recommendation != "needs_review":
                raise ValueError("confidence must be <= 0.49 when edge_exists is false unless needs_review")
            return self
        if self.predicate == "none":
            raise ValueError("predicate must not be none when edge_exists is true")
        if self.direction == "none":
            raise ValueError("direction must not be none when edge_exists is true")
        if self.direction == "undirected" and self.predicate != "conflicts_with":
            raise ValueError("undirected is only allowed for conflicts_with")
        if not self.rationale.strip():
            raise ValueError("rationale is required when edge_exists is true")
        if not self.evidence.strip():
            raise ValueError("evidence is required when edge_exists is true")
        return self


class VerificationDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agrees: bool
    corrected_edge_exists: bool
    corrected_predicate: PREDICATE_LITERAL
    corrected_direction: DIRECTION_LITERAL
    corrected_confidence: float = Field(ge=0.0, le=1.0)
    rationale: str

    @model_validator(mode="after")
    def _verification_rules(self) -> "VerificationDecision":
        if not self.corrected_edge_exists:
            if self.corrected_predicate != "none":
                raise ValueError("corrected_predicate must be none when corrected_edge_exists is false")
            if self.corrected_direction != "none":
                raise ValueError("corrected_direction must be none when corrected_edge_exists is false")
        if self.corrected_direction == "undirected" and self.corrected_predicate != "conflicts_with":
            raise ValueError("undirected is only allowed for conflicts_with")
        return self


@dataclass
class ProviderRouteStep:
    role: str
    provider: str
    model: str
    status: str
    reason: str | None = None

    def to_record(self) -> dict[str, Any]:
        record = {
            "role": self.role,
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
        }
        if self.reason:
            record["reason"] = self.reason
        return record


@dataclass
class ProviderEnvelope:
    raw_text: str
    provider: str
    model: str
    route: list[ProviderRouteStep]
    local_fallback_used: bool = False
    provider_failover_reason: str | None = None
    finish_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_metadata(self) -> dict[str, Any]:
        return {
            "provider_route": [step.to_record() for step in self.route],
            "local_fallback_used": self.local_fallback_used,
            "provider_failover_reason": self.provider_failover_reason,
            "finish_reason": self.finish_reason,
            "metadata": sanitize_for_artifact(self.metadata),
        }


@dataclass
class CloudChatResponse:
    provider: str
    model: str
    content: str
    finish_reason: str | None
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CloudUsage:
    cloud_call_count: int = 0
    cloud_total_max_calls: int | None = None
    cloud_cost_budget_usd: float | None = None
    cloud_estimated_cost_usd: float = 0.0
    kimi_call_count: int = 0
    kimi_max_calls: int | None = None
    kimi_disabled: bool = True
    kimi_disabled_reason: str = "disabled_for_relationship_workflow"
    kimi_prompt_tokens: int = 0
    kimi_completion_tokens: int = 0
    kimi_total_tokens: int = 0
    deepseek_call_count: int = 0
    deepseek_flash_call_count: int = 0
    deepseek_flash_judge_call_count: int = 0
    deepseek_flash_verifier_call_count: int = 0
    deepseek_flash_adjudicator_call_count: int = 0
    deepseek_pro_call_count: int = 0
    deepseek_pro_adjudicator_call_count: int = 0
    deepseek_prompt_tokens: int = 0
    deepseek_prompt_cache_hit_tokens: int = 0
    deepseek_prompt_cache_miss_tokens: int = 0
    deepseek_completion_tokens: int = 0
    deepseek_total_tokens: int = 0
    deepseek_reasoning_tokens: int = 0
    deepseek_estimated_cost_usd: float = 0.0
    local_fallback_call_count: int = 0
    provider_failover_events: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_record(cls, data: dict[str, Any] | None) -> "CloudUsage":
        if not data:
            return cls()
        fields = {name for name in cls.__dataclass_fields__}
        values = {key: data.get(key) for key in fields if key in data}
        values["provider_failover_events"] = list(data.get("provider_failover_events") or [])
        return cls(**values)

    def to_record(self) -> dict[str, Any]:
        return {
            "cloud_call_count": self.cloud_call_count,
            "cloud_total_max_calls": self.cloud_total_max_calls,
            "cloud_cost_budget_usd": self.cloud_cost_budget_usd,
            "cloud_estimated_cost_usd": self.cloud_estimated_cost_usd,
            "kimi_call_count": self.kimi_call_count,
            "kimi_max_calls": self.kimi_max_calls,
            "kimi_disabled": self.kimi_disabled,
            "kimi_disabled_reason": self.kimi_disabled_reason,
            "kimi_prompt_tokens": self.kimi_prompt_tokens,
            "kimi_completion_tokens": self.kimi_completion_tokens,
            "kimi_total_tokens": self.kimi_total_tokens,
            "deepseek_call_count": self.deepseek_call_count,
            "deepseek_flash_call_count": self.deepseek_flash_call_count,
            "deepseek_flash_judge_call_count": self.deepseek_flash_judge_call_count,
            "deepseek_flash_verifier_call_count": self.deepseek_flash_verifier_call_count,
            "deepseek_flash_adjudicator_call_count": self.deepseek_flash_adjudicator_call_count,
            "deepseek_pro_call_count": self.deepseek_pro_call_count,
            "deepseek_pro_adjudicator_call_count": self.deepseek_pro_adjudicator_call_count,
            "deepseek_prompt_tokens": self.deepseek_prompt_tokens,
            "deepseek_prompt_cache_hit_tokens": self.deepseek_prompt_cache_hit_tokens,
            "deepseek_prompt_cache_miss_tokens": self.deepseek_prompt_cache_miss_tokens,
            "deepseek_completion_tokens": self.deepseek_completion_tokens,
            "deepseek_total_tokens": self.deepseek_total_tokens,
            "deepseek_reasoning_tokens": self.deepseek_reasoning_tokens,
            "deepseek_estimated_cost_usd": self.deepseek_estimated_cost_usd,
            "local_fallback_call_count": self.local_fallback_call_count,
            "provider_failover_events": self.provider_failover_events,
        }

    def record_local_fallback(self, role: str, reason: str) -> None:
        self.local_fallback_call_count += 1
        self.provider_failover_events.append(
            {
                "role": role,
                "provider": "ollama",
                "reason": reason,
                "created_at_utc": utc_now(),
            }
        )

    def record_cloud_attempt(
        self,
        provider: str,
        model: str,
        *,
        role: str | None = None,
        deepseek_tier: str | None = None,
    ) -> None:
        self.cloud_call_count += 1
        if provider == "kimi":
            self.kimi_call_count += 1
            return
        if provider == "deepseek":
            self.deepseek_call_count += 1
            is_pro = deepseek_tier == "pro" or (deepseek_tier is None and (model == DEFAULT_DEEPSEEK_PRO_MODEL or model.endswith("-pro")))
            if is_pro:
                self.deepseek_pro_call_count += 1
                if role == "adjudicator":
                    self.deepseek_pro_adjudicator_call_count += 1
            else:
                self.deepseek_flash_call_count += 1
                if role == "judge":
                    self.deepseek_flash_judge_call_count += 1
                elif role == "verifier":
                    self.deepseek_flash_verifier_call_count += 1
                elif role == "adjudicator":
                    self.deepseek_flash_adjudicator_call_count += 1

    def record_cloud_usage(self, provider: str, model: str, usage: dict[str, Any]) -> None:
        if provider == "kimi":
            self.kimi_prompt_tokens += int(usage.get("prompt_tokens") or 0)
            self.kimi_completion_tokens += int(usage.get("completion_tokens") or 0)
            self.kimi_total_tokens += int(usage.get("total_tokens") or 0)
            cost = usage.get("_estimated_cost_usd")
            if cost is not None:
                self.cloud_estimated_cost_usd += float(cost)
            return
        if provider == "deepseek":
            prompt_tokens = int(usage.get("prompt_tokens") or 0)
            completion_tokens = int(usage.get("completion_tokens") or 0)
            total_tokens = int(usage.get("total_tokens") or 0)
            cache_hit_tokens = int(usage.get("prompt_cache_hit_tokens") or 0)
            cache_miss_tokens = int(usage.get("prompt_cache_miss_tokens") or 0)
            reasoning_tokens = int(usage.get("reasoning_tokens") or 0)
            self.deepseek_prompt_tokens += prompt_tokens
            self.deepseek_prompt_cache_hit_tokens += cache_hit_tokens
            self.deepseek_prompt_cache_miss_tokens += cache_miss_tokens
            self.deepseek_completion_tokens += completion_tokens
            self.deepseek_total_tokens += total_tokens
            self.deepseek_reasoning_tokens += reasoning_tokens
            cost = estimate_deepseek_cost_usd(model, usage)
            if cost is not None:
                self.deepseek_estimated_cost_usd += cost
                self.cloud_estimated_cost_usd += cost

    def record_cloud_call(
        self,
        provider: str,
        model: str,
        usage: dict[str, Any],
        *,
        role: str | None = None,
        deepseek_tier: str | None = None,
    ) -> None:
        self.record_cloud_attempt(provider, model, role=role, deepseek_tier=deepseek_tier)
        self.record_cloud_usage(provider, model, usage)


@dataclass
class ProviderHealth:
    states: dict[str, str] = field(default_factory=dict)
    failure_counts: dict[str, int] = field(default_factory=dict)
    last_errors: dict[str, str] = field(default_factory=dict)
    last_latencies: dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_record(cls, data: dict[str, Any] | None) -> "ProviderHealth":
        if not data:
            return cls()
        return cls(
            states=dict(data.get("states") or {}),
            failure_counts={key: int(value) for key, value in dict(data.get("failure_counts") or {}).items()},
            last_errors={key: _as_text(value) for key, value in dict(data.get("last_errors") or {}).items()},
            last_latencies={key: float(value) for key, value in dict(data.get("last_latencies") or {}).items()},
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "states": self.states,
            "failure_counts": self.failure_counts,
            "last_errors": self.last_errors,
            "last_latencies": self.last_latencies,
        }

    def status(self, provider: str) -> str:
        return self.states.get(provider, "healthy")

    def is_available(self, provider: str) -> bool:
        return not self.status(provider).startswith("disabled") and self.status(provider) != "exhausted"

    def mark_failure(self, provider: str, status: str, threshold: int) -> None:
        self.failure_counts[provider] = self.failure_counts.get(provider, 0) + 1
        self.last_errors[provider] = status
        if status.startswith("disabled") or status == "exhausted":
            self.states[provider] = status
        elif self.failure_counts[provider] >= threshold:
            self.states[provider] = status
        else:
            self.states[provider] = "degraded"

    def mark_success(self, provider: str) -> None:
        self.failure_counts[provider] = 0
        if self.states.get(provider) in {"degraded", "disabled_timeout", "disabled_rate_limit"}:
            self.states[provider] = "healthy"

    def record_latency(self, provider: str, seconds: float) -> None:
        self.last_latencies[provider] = round(float(seconds), 3)


@dataclass
class Checkpoint:
    run_id: str
    status: str
    input_path: str
    output_dir: str
    embedding_model: str
    judge_model: str
    verifier_model: str | None
    council_mode: str = "local_only"
    local_judge_model: str = DEFAULT_JUDGE_MODEL
    local_verifier_model: str = DEFAULT_VERIFIER_MODEL
    primary_judge_provider: str | None = None
    primary_judge_model: str | None = None
    fallback_judge_provider: str | None = None
    fallback_judge_model: str | None = None
    primary_verifier_provider: str | None = None
    primary_verifier_model: str | None = None
    fallback_verifier_provider: str | None = None
    fallback_verifier_model: str | None = None
    primary_adjudicator_provider: str | None = None
    primary_adjudicator_model: str | None = None
    fallback_adjudicator_provider: str | None = None
    fallback_adjudicator_model: str | None = None
    effective_judge_provider: str | None = None
    effective_judge_model: str | None = None
    effective_verifier_provider: str | None = None
    effective_verifier_model: str | None = None
    effective_adjudicator_provider: str | None = None
    effective_adjudicator_model: str | None = None
    processed_pair_keys: list[str] = field(default_factory=list)
    accepted_edge_keys: list[str] = field(default_factory=list)
    rejected_pair_count: int = 0
    error_count: int = 0
    cloud_usage: CloudUsage = field(default_factory=CloudUsage)
    provider_health: ProviderHealth = field(default_factory=ProviderHealth)
    last_provider_used: str | None = None
    deepseek_flash_max_calls: int | None = None
    deepseek_pro_max_calls: int | None = None
    hierarchy_normalization_count: int = 0
    taxonomy_part_of_conversion_count: int = 0
    validation_guard_downgrade_count: int = 0
    phase: str = "loading"
    started_at_utc: str = field(default_factory=lambda: utc_now())
    elapsed_seconds: float = 0.0
    nodes_loaded: int = 0
    nodes_selected: int = 0
    embedding_total: int = 0
    embedding_processed: int = 0
    embedding_cache_hits: int = 0
    embedding_cache_misses: int = 0
    embedding_dimensions: int | None = None
    candidate_pairs_generated: int = 0
    candidate_pairs_total_estimate: int | None = None
    max_pairs: int = 0
    processed_pair_count: int = 0
    accepted_count: int = 0
    candidate_count: int = 0
    rejected_count: int = 0
    current_pair_key: str | None = None
    current_provider: str | None = None
    current_model: str | None = None
    current_operation: str | None = None
    avg_embedding_seconds: float | None = None
    avg_judge_seconds: float | None = None
    avg_verifier_seconds: float | None = None
    avg_adjudicator_seconds: float | None = None
    pairs_per_minute: float | None = None
    estimated_seconds_remaining: float | None = None
    recent_events: list[dict[str, Any]] = field(default_factory=list)
    validation_error_count: int = 0
    validation_errors_by_role: dict[str, int] = field(default_factory=dict)
    validation_errors_by_provider: dict[str, int] = field(default_factory=dict)
    validation_errors_by_field: dict[str, int] = field(default_factory=dict)
    progress_mode_effective: str | None = None
    last_updated_at_utc: str = field(default_factory=lambda: utc_now())
    schema_version: str = "aec-relationship-improvement-checkpoint/v1"

    def to_record(self) -> dict[str, Any]:
        usage = self.cloud_usage.to_record()
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "status": self.status,
            "phase": self.phase,
            "input_path": self.input_path,
            "output_dir": self.output_dir,
            "started_at_utc": self.started_at_utc,
            "elapsed_seconds": self.elapsed_seconds,
            "embedding_model": self.embedding_model,
            "judge_model": self.judge_model,
            "verifier_model": self.verifier_model,
            "council_mode": self.council_mode,
            "local_judge_model": self.local_judge_model,
            "local_verifier_model": self.local_verifier_model,
            "primary_judge_provider": self.primary_judge_provider,
            "primary_judge_model": self.primary_judge_model,
            "fallback_judge_provider": self.fallback_judge_provider,
            "fallback_judge_model": self.fallback_judge_model,
            "primary_verifier_provider": self.primary_verifier_provider,
            "primary_verifier_model": self.primary_verifier_model,
            "fallback_verifier_provider": self.fallback_verifier_provider,
            "fallback_verifier_model": self.fallback_verifier_model,
            "primary_adjudicator_provider": self.primary_adjudicator_provider,
            "primary_adjudicator_model": self.primary_adjudicator_model,
            "fallback_adjudicator_provider": self.fallback_adjudicator_provider,
            "fallback_adjudicator_model": self.fallback_adjudicator_model,
            "effective_judge_provider": self.effective_judge_provider,
            "effective_judge_model": self.effective_judge_model,
            "effective_verifier_provider": self.effective_verifier_provider,
            "effective_verifier_model": self.effective_verifier_model,
            "effective_adjudicator_provider": self.effective_adjudicator_provider,
            "effective_adjudicator_model": self.effective_adjudicator_model,
            "processed_pair_keys": self.processed_pair_keys,
            "accepted_edge_keys": self.accepted_edge_keys,
            "nodes_loaded": self.nodes_loaded,
            "nodes_selected": self.nodes_selected,
            "embedding_total": self.embedding_total,
            "embedding_processed": self.embedding_processed,
            "embedding_cache_hits": self.embedding_cache_hits,
            "embedding_cache_misses": self.embedding_cache_misses,
            "embedding_dimensions": self.embedding_dimensions,
            "candidate_pairs_generated": self.candidate_pairs_generated,
            "candidate_pairs_total_estimate": self.candidate_pairs_total_estimate,
            "max_pairs": self.max_pairs,
            "processed_pair_count": self.processed_pair_count,
            "accepted_count": self.accepted_count,
            "candidate_count": self.candidate_count,
            "rejected_pair_count": self.rejected_pair_count,
            "rejected_count": self.rejected_count,
            "error_count": self.error_count,
            "current_pair_key": self.current_pair_key,
            "current_provider": self.current_provider,
            "current_model": self.current_model,
            "current_operation": self.current_operation,
            "cloud_call_count": usage["cloud_call_count"],
            "cloud_total_max_calls": usage["cloud_total_max_calls"],
            "cloud_cost_budget_usd": usage["cloud_cost_budget_usd"],
            "cloud_estimated_cost_usd": usage["cloud_estimated_cost_usd"],
            "kimi_call_count": usage["kimi_call_count"],
            "kimi_max_calls": usage["kimi_max_calls"],
            "deepseek_flash_call_count": usage["deepseek_flash_call_count"],
            "deepseek_flash_judge_call_count": usage["deepseek_flash_judge_call_count"],
            "deepseek_flash_verifier_call_count": usage["deepseek_flash_verifier_call_count"],
            "deepseek_flash_adjudicator_call_count": usage["deepseek_flash_adjudicator_call_count"],
            "deepseek_flash_max_calls": self.deepseek_flash_max_calls,
            "deepseek_pro_call_count": usage["deepseek_pro_call_count"],
            "deepseek_pro_adjudicator_call_count": usage["deepseek_pro_adjudicator_call_count"],
            "deepseek_pro_max_calls": self.deepseek_pro_max_calls,
            "local_fallback_call_count": usage["local_fallback_call_count"],
            "hierarchy_normalization_count": self.hierarchy_normalization_count,
            "taxonomy_part_of_conversion_count": self.taxonomy_part_of_conversion_count,
            "validation_guard_downgrade_count": self.validation_guard_downgrade_count,
            "cloud_usage": usage,
            "provider_health": self.provider_health.to_record(),
            "cloud_budget_remaining_usd": cloud_budget_remaining_usd(self.cloud_usage),
            "avg_embedding_seconds": self.avg_embedding_seconds,
            "avg_judge_seconds": self.avg_judge_seconds,
            "avg_verifier_seconds": self.avg_verifier_seconds,
            "avg_adjudicator_seconds": self.avg_adjudicator_seconds,
            "pairs_per_minute": self.pairs_per_minute,
            "estimated_seconds_remaining": self.estimated_seconds_remaining,
            "recent_events": self.recent_events[-MAX_RECENT_EVENTS:],
            "validation_error_count": self.validation_error_count,
            "validation_errors_by_role": self.validation_errors_by_role,
            "validation_errors_by_provider": self.validation_errors_by_provider,
            "validation_errors_by_field": self.validation_errors_by_field,
            "progress_mode_effective": self.progress_mode_effective,
            "last_provider_used": self.last_provider_used,
            "last_updated_at_utc": self.last_updated_at_utc,
        }


@dataclass
class RunConfig:
    input_path: Path = DEFAULT_INPUT_PATH
    output_root: Path = DEFAULT_OUTPUT_ROOT
    run_id: str | None = None
    dry_run: bool = True
    resume: bool = False
    max_nodes: int = 1000
    max_pairs: int = 5000
    candidate_top_k: int = 20
    min_similarity: float = 0.35
    accept_threshold: float = 0.85
    verify_threshold: float = 0.65
    verify_uncertain: bool = False
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    judge_model: str = DEFAULT_JUDGE_MODEL
    verifier_model: str | None = DEFAULT_VERIFIER_MODEL
    ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL
    sleep_seconds: float = 2.0
    verifier_sleep_seconds: float = 3.0
    embedding_batch_size: int = 1
    num_ctx: int = 4096
    num_predict: int = 500
    temperature: float = 0.1
    think: bool = False
    include_existing_pairs: bool = False
    store_embedding_text: bool = False
    stable_embedding_cache_path: Path | None = None
    no_stable_embedding_cache: bool = False
    apply: bool = False
    allow_cloud_ai: bool = False
    council_mode: str = "local_only"
    cloud_cost_budget_usd: float | None = None
    cloud_total_max_calls: int | None = None
    cloud_timeout_seconds: int = 120
    cloud_max_retries: int = 2
    cloud_backoff_seconds: float = 10.0
    cloud_circuit_breaker_failures: int = 3
    cloud_redact_fields: tuple[str, ...] = ()
    judge_provider: str = "auto"
    verifier_provider: str = "auto"
    adjudicator_provider: str = "none"
    kimi_base_url: str = DEFAULT_KIMI_BASE_URL
    kimi_model: str = DEFAULT_KIMI_MODEL
    kimi_api_key_env: str = DEFAULT_KIMI_API_KEY_ENV
    kimi_disable_thinking: bool = True
    kimi_max_tokens: int = 700
    kimi_sleep_seconds: float = 2.0
    kimi_max_calls: int | None = None
    kimi_estimated_cost_per_call_usd: float = 0.0
    kimi_verify_accepted_sample_rate: float = 0.25
    kimi_verify_uncertain: bool | None = None
    allow_custom_kimi_base_url: bool = False
    enable_kimi_experimental: bool = False
    deepseek_base_url: str = DEFAULT_DEEPSEEK_BASE_URL
    deepseek_flash_model: str = DEFAULT_DEEPSEEK_FLASH_MODEL
    deepseek_pro_model: str = DEFAULT_DEEPSEEK_PRO_MODEL
    deepseek_api_key_env: str = DEFAULT_DEEPSEEK_API_KEY_ENV
    deepseek_disable_thinking: bool = True
    deepseek_reasoning_effort: str = "high"
    deepseek_max_tokens: int = 700
    deepseek_sleep_seconds: float = 1.0
    deepseek_flash_max_calls: int | None = None
    deepseek_pro_max_calls: int | None = None
    deepseek_flash_call_buffer: float = 0.50
    allow_custom_deepseek_base_url: bool = False
    cloud_preflight: bool = True
    deepseek_retry_truncated_json: bool = True
    hierarchy_canonical_predicate: str = "broader_than"
    convert_taxonomy_part_of: bool = True
    enable_safe_schema_repair: bool = True
    schema_repair_acceptance_policy: str = "needs_review_only"
    verify_accepted_cloud: bool | None = None
    verify_accepted_sample_rate: float = 0.25
    adjudicate_disagreements: bool | None = None
    high_impact_pro_adjudication: bool = True
    fallback_to_local_on_cloud_exhaustion: bool = True
    fallback_to_local_on_cloud_error: bool = True
    fallback_to_local_on_rate_limit: bool = True
    stop_on_cloud_auth_error: bool = False
    strict_cloud_only: bool = False
    reset_cloud_budget_for_resume: bool = False
    progress_mode: str = "auto"
    progress_refresh_per_second: float = 2.0
    progress_log_every_seconds: float = 30.0
    progress_show_recent: int = 8
    progress_transient: bool = False
    force_rich_in_git_bash: bool = False
    progress_mode_effective: str | None = None
    watch_run: str | None = None


@dataclass
class RunSummary:
    run_id: str
    output_dir: str
    nodes_loaded: int
    existing_relationships_loaded: int
    candidate_pair_count: int = 0
    processed_count: int = 0
    skipped_count: int = 0
    accepted_count: int = 0
    candidate_review_count: int = 0
    rejected_count: int = 0
    error_count: int = 0
    rejection_counts: dict[str, int] = field(default_factory=dict)
    embedding_cache_hits: int = 0
    embedding_cache_misses: int = 0
    embedding_dimensions: int | None = None
    cloud_usage: CloudUsage = field(default_factory=CloudUsage)
    provider_health: ProviderHealth = field(default_factory=ProviderHealth)
    status: str = "completed"
    hierarchy_normalization_count: int = 0
    taxonomy_part_of_conversion_count: int = 0
    validation_guard_downgrade_count: int = 0
    validation_error_count: int = 0
    validation_errors_by_role: dict[str, int] = field(default_factory=dict)
    validation_errors_by_provider: dict[str, int] = field(default_factory=dict)
    validation_errors_by_field: dict[str, int] = field(default_factory=dict)
    local_judge_model: str = DEFAULT_JUDGE_MODEL
    local_verifier_model: str = DEFAULT_VERIFIER_MODEL
    primary_judge_provider: str | None = None
    primary_judge_model: str | None = None
    fallback_judge_provider: str | None = None
    fallback_judge_model: str | None = None
    primary_verifier_provider: str | None = None
    primary_verifier_model: str | None = None
    fallback_verifier_provider: str | None = None
    fallback_verifier_model: str | None = None
    primary_adjudicator_provider: str | None = None
    primary_adjudicator_model: str | None = None
    fallback_adjudicator_provider: str | None = None
    fallback_adjudicator_model: str | None = None
    effective_judge_provider: str | None = None
    effective_judge_model: str | None = None
    effective_verifier_provider: str | None = None
    effective_verifier_model: str | None = None
    effective_adjudicator_provider: str | None = None
    effective_adjudicator_model: str | None = None
    progress_mode_effective: str | None = None
    avg_judge_seconds: float | None = None
    avg_verifier_seconds: float | None = None
    avg_adjudicator_seconds: float | None = None
    pairs_per_minute: float | None = None
    elapsed_seconds: float | None = None
    recommendations: list[str] = field(default_factory=list)

    def to_record(self) -> dict[str, Any]:
        processed = max(0, self.processed_count)
        quality_summary = {
            "accepted_count": self.accepted_count,
            "candidate_review_count": self.candidate_review_count,
            "rejected_count": self.rejected_count,
            "error_count": self.error_count,
            "validation_error_count": self.validation_error_count,
            "acceptance_rate": round(self.accepted_count / processed, 6) if processed else 0.0,
            "needs_review_rate": round(self.candidate_review_count / processed, 6) if processed else 0.0,
            "rejection_rate": round(self.rejected_count / processed, 6) if processed else 0.0,
            "hierarchy_normalization_count": self.hierarchy_normalization_count,
            "taxonomy_part_of_conversion_count": self.taxonomy_part_of_conversion_count,
            "validation_guard_downgrade_count": self.validation_guard_downgrade_count,
        }
        provider_summary = {
            "primary_judge_provider": self.primary_judge_provider,
            "primary_judge_model": self.primary_judge_model,
            "fallback_judge_provider": self.fallback_judge_provider,
            "fallback_judge_model": self.fallback_judge_model,
            "effective_judge_provider": self.effective_judge_provider,
            "effective_judge_model": self.effective_judge_model,
            "effective_verifier_provider": self.effective_verifier_provider,
            "effective_verifier_model": self.effective_verifier_model,
            "effective_adjudicator_provider": self.effective_adjudicator_provider,
            "effective_adjudicator_model": self.effective_adjudicator_model,
            "local_fallback_call_count": self.cloud_usage.local_fallback_call_count,
            "provider_failover_events": self.cloud_usage.provider_failover_events,
        }
        cost_summary = {
            "cloud_estimated_cost_usd": self.cloud_usage.cloud_estimated_cost_usd,
            "cloud_cost_budget_usd": self.cloud_usage.cloud_cost_budget_usd,
            "budget_remaining_usd": cloud_budget_remaining_usd(self.cloud_usage),
            "deepseek_prompt_cache_hit_tokens": self.cloud_usage.deepseek_prompt_cache_hit_tokens,
            "deepseek_prompt_cache_miss_tokens": self.cloud_usage.deepseek_prompt_cache_miss_tokens,
            "deepseek_completion_tokens": self.cloud_usage.deepseek_completion_tokens,
            "deepseek_reasoning_tokens": self.cloud_usage.deepseek_reasoning_tokens,
        }
        performance_summary = {
            "elapsed_seconds": self.elapsed_seconds,
            "pairs_per_minute": self.pairs_per_minute,
            "avg_judge_seconds": self.avg_judge_seconds,
            "avg_verifier_seconds": self.avg_verifier_seconds,
            "avg_adjudicator_seconds": self.avg_adjudicator_seconds,
        }
        return {
            "schema_version": "aec-relationship-improvement-report/v1",
            "run_id": self.run_id,
            "output_dir": self.output_dir,
            "nodes_loaded": self.nodes_loaded,
            "existing_relationships_loaded": self.existing_relationships_loaded,
            "candidate_pair_count": self.candidate_pair_count,
            "processed_count": self.processed_count,
            "skipped_count": self.skipped_count,
            "accepted_count": self.accepted_count,
            "candidate_review_count": self.candidate_review_count,
            "rejected_count": self.rejected_count,
            "error_count": self.error_count,
            "rejection_counts": self.rejection_counts,
            "embedding_cache_hits": self.embedding_cache_hits,
            "embedding_cache_misses": self.embedding_cache_misses,
            "embedding_dimensions": self.embedding_dimensions,
            "cloud_usage": self.cloud_usage.to_record(),
            "provider_health": self.provider_health.to_record(),
            "local_judge_model": self.local_judge_model,
            "local_verifier_model": self.local_verifier_model,
            "primary_judge_provider": self.primary_judge_provider,
            "primary_judge_model": self.primary_judge_model,
            "fallback_judge_provider": self.fallback_judge_provider,
            "fallback_judge_model": self.fallback_judge_model,
            "primary_verifier_provider": self.primary_verifier_provider,
            "primary_verifier_model": self.primary_verifier_model,
            "fallback_verifier_provider": self.fallback_verifier_provider,
            "fallback_verifier_model": self.fallback_verifier_model,
            "primary_adjudicator_provider": self.primary_adjudicator_provider,
            "primary_adjudicator_model": self.primary_adjudicator_model,
            "fallback_adjudicator_provider": self.fallback_adjudicator_provider,
            "fallback_adjudicator_model": self.fallback_adjudicator_model,
            "effective_judge_provider": self.effective_judge_provider,
            "effective_judge_model": self.effective_judge_model,
            "effective_verifier_provider": self.effective_verifier_provider,
            "effective_verifier_model": self.effective_verifier_model,
            "effective_adjudicator_provider": self.effective_adjudicator_provider,
            "effective_adjudicator_model": self.effective_adjudicator_model,
            "validation_error_count": self.validation_error_count,
            "validation_errors_by_role": self.validation_errors_by_role,
            "validation_errors_by_provider": self.validation_errors_by_provider,
            "validation_errors_by_field": self.validation_errors_by_field,
            "quality_summary": quality_summary,
            "provider_summary": provider_summary,
            "cost_summary": cost_summary,
            "performance_summary": performance_summary,
            "recommendations": self.recommendations,
            "progress_mode_effective": self.progress_mode_effective,
            "hierarchy_normalization_count": self.hierarchy_normalization_count,
            "taxonomy_part_of_conversion_count": self.taxonomy_part_of_conversion_count,
            "validation_guard_downgrade_count": self.validation_guard_downgrade_count,
            "status": self.status,
            "completed_at_utc": utc_now(),
        }


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def seconds_since_utc(value: str | None) -> float | None:
    timestamp = parse_utc_timestamp(value)
    if timestamp is None:
        return None
    return max(0.0, (datetime.now(UTC) - timestamp).total_seconds())


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "unknown"
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def default_run_id() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def secret_values_from_env() -> list[str]:
    values: list[str] = []
    for name in ("DEEPSEEK_API_KEY", "KIMI_API_KEY", "MOONSHOT_API_KEY"):
        value = os.environ.get(name)
        if value and len(value) >= 8:
            values.append(value)
    return values


def redact_secret_text(text: str) -> str:
    redacted = text
    redacted = re.sub(r"reasoning_content", "[REDACTED_REASONING_FIELD]", redacted, flags=re.IGNORECASE)
    for secret in secret_values_from_env():
        redacted = redacted.replace(secret, "[REDACTED_SECRET]")
    redacted = re.sub(r"Bearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", redacted, flags=re.IGNORECASE)
    redacted = re.sub(r"\bsk-[A-Za-z0-9][A-Za-z0-9._-]{8,}\b", "sk-[REDACTED]", redacted)
    return redacted


def sanitize_for_artifact(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if (
                "api_key" in lowered
                or "authorization" in lowered
                or "reasoning_content" in lowered
                or lowered == "embedding"
                or lowered.endswith("_embedding")
            ):
                continue
            sanitized[key] = sanitize_for_artifact(item)
        return sanitized
    if isinstance(value, list):
        return [sanitize_for_artifact(item) for item in value]
    if isinstance(value, str):
        return redact_secret_text(value)
    return value


def truncate_error_text(text: str, limit: int = 500) -> str:
    cleaned = text.replace("\r", " ").replace("\n", " ")
    return cleaned[:limit] + ("..." if len(cleaned) > limit else "")


def update_rolling_average(previous: float | None, sample: float, count: int) -> float:
    if count <= 1 or previous is None:
        return round(float(sample), 3)
    return round(((previous * (count - 1)) + float(sample)) / count, 3)


def estimate_deepseek_cost_usd(model: str, usage: dict[str, Any]) -> float | None:
    prices = DEEPSEEK_PRICE_PER_MILLION.get(model)
    if prices is None:
        return None
    required = ("prompt_cache_hit_tokens", "prompt_cache_miss_tokens", "completion_tokens")
    if any(key not in usage for key in required):
        return None
    return (
        float(usage.get("prompt_cache_hit_tokens") or 0) * prices["input_cache_hit"] / 1_000_000
        + float(usage.get("prompt_cache_miss_tokens") or 0) * prices["input_cache_miss"] / 1_000_000
        + float(usage.get("completion_tokens") or 0) * prices["output"] / 1_000_000
    )


def cloud_budget_remaining_usd(usage: CloudUsage) -> float | None:
    if usage.cloud_cost_budget_usd is None:
        return None
    return max(0.0, usage.cloud_cost_budget_usd - usage.cloud_estimated_cost_usd)


def generation_method_for_council_mode(council_mode: str) -> str:
    return {
        "local_only": "local_ollama_relationship_improvement_v1",
        "deepseek_local": "deepseek_local_relationship_improvement_v1",
        "adaptive_cloud": "adaptive_deepseek_local_relationship_improvement_v1",
        "cloud_first": "deepseek_local_relationship_improvement_v1",
        "local_first_cloud_verify": "local_first_deepseek_verify_relationship_improvement_v1",
        "audit_only": "relationship_council_audit_v1",
    }.get(council_mode, GENERATION_METHOD)


def effective_cloud_cost_budget(config: RunConfig) -> float | None:
    if config.cloud_cost_budget_usd is not None:
        return config.cloud_cost_budget_usd
    if config.allow_cloud_ai and config.council_mode in DEEPSEEK_LOCAL_MODES:
        return 5.0
    return None


def effective_cloud_total_max_calls(config: RunConfig) -> int | None:
    if config.cloud_total_max_calls is not None:
        return config.cloud_total_max_calls
    if config.council_mode in DEEPSEEK_LOCAL_MODES:
        return 1000
    return None


def effective_kimi_max_calls(config: RunConfig) -> int | None:
    if not config.enable_kimi_experimental:
        return None
    if config.kimi_max_calls is not None:
        return config.kimi_max_calls
    if config.council_mode == "adaptive_cloud":
        return 300
    return None


def effective_deepseek_flash_max_calls(config: RunConfig) -> int | None:
    if config.deepseek_flash_max_calls is not None:
        return config.deepseek_flash_max_calls
    if config.council_mode in DEEPSEEK_LOCAL_MODES:
        return int(math.ceil(max(0, config.max_pairs) * (1.0 + max(0.0, config.deepseek_flash_call_buffer))))
    return None


def effective_deepseek_pro_max_calls(config: RunConfig) -> int | None:
    if config.deepseek_pro_max_calls is not None:
        return config.deepseek_pro_max_calls
    if config.council_mode in DEEPSEEK_LOCAL_MODES:
        return 50
    return None


def provider_priority_for_role(config: RunConfig, role: str) -> list[tuple[str, str]]:
    if config.council_mode == "local_only":
        return [("ollama", config.judge_model if role == "judge" else (config.verifier_model or DEFAULT_VERIFIER_MODEL))]
    requested = {
        "judge": config.judge_provider,
        "verifier": config.verifier_provider,
        "adjudicator": config.adjudicator_provider,
    }[role]
    if requested != "auto":
        if requested == "kimi":
            return [("kimi", config.kimi_model)]
        if requested == "deepseek":
            return [("deepseek", config.deepseek_pro_model if role == "adjudicator" else config.deepseek_flash_model)]
        if requested == "ollama":
            return [("ollama", config.judge_model if role == "judge" else (config.verifier_model or DEFAULT_VERIFIER_MODEL))]
        return [(requested, "")]
    if config.council_mode == "cloud_first":
        if role == "judge":
            return [("deepseek", config.deepseek_flash_model), ("ollama", config.judge_model)]
        if role == "adjudicator":
            return [("deepseek", config.deepseek_pro_model), ("ollama", config.verifier_model or DEFAULT_VERIFIER_MODEL)]
        return [("ollama", config.verifier_model or DEFAULT_VERIFIER_MODEL), ("deepseek", config.deepseek_flash_model)]
    if config.council_mode == "local_first_cloud_verify":
        if role == "judge":
            return [("ollama", config.judge_model)]
        if role == "adjudicator":
            return [("deepseek", config.deepseek_pro_model), ("ollama", config.verifier_model or DEFAULT_VERIFIER_MODEL)]
        return [("deepseek", config.deepseek_flash_model), ("ollama", config.verifier_model or DEFAULT_VERIFIER_MODEL)]
    if role == "judge":
        return [("deepseek", config.deepseek_flash_model), ("ollama", config.judge_model)]
    if role == "adjudicator":
        return [("deepseek", config.deepseek_pro_model), ("ollama", config.verifier_model or DEFAULT_VERIFIER_MODEL)]
    return [("ollama", config.verifier_model or DEFAULT_VERIFIER_MODEL), ("deepseek", config.deepseek_flash_model)]


def role_model_metadata(config: RunConfig) -> dict[str, Any]:
    data: dict[str, Any] = {
        "local_judge_model": config.judge_model,
        "local_verifier_model": config.verifier_model or DEFAULT_VERIFIER_MODEL,
    }
    for role in ("judge", "verifier", "adjudicator"):
        priority = provider_priority_for_role(config, role)
        primary = priority[0] if priority else (None, None)
        fallback = priority[1] if len(priority) > 1 else (None, None)
        data[f"primary_{role}_provider"] = primary[0]
        data[f"primary_{role}_model"] = primary[1]
        data[f"fallback_{role}_provider"] = fallback[0]
        data[f"fallback_{role}_model"] = fallback[1]
        data[f"effective_{role}_provider"] = primary[0]
        data[f"effective_{role}_model"] = primary[1]
    return data


def ensure_apply_mode_is_deferred(apply: bool) -> None:
    if apply:
        raise ApplyModeDeferredError(
            "Apply mode is intentionally deferred for safety. This v1 writes pending artifacts only."
        )


def ensure_local_ollama_base_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "http":
        raise ExternalNetworkDisabledError("Internet/external model endpoints are disabled in v1; use local HTTP Ollama.")
    host = (parsed.hostname or "").rstrip(".").lower()
    if host == "localhost":
        return
    try:
        if ip_address(host).is_loopback:
            return
    except ValueError:
        pass
    raise ExternalNetworkDisabledError("Internet/external model endpoints are disabled in v1; use local HTTP Ollama.")


def validate_council_config(config: RunConfig) -> None:
    if config.council_mode not in COUNCIL_MODES:
        raise ValueError(f"Unknown council mode: {config.council_mode}")
    if config.hierarchy_canonical_predicate not in HIERARCHY_CANONICAL_PREDICATES:
        raise ValueError(f"Unknown hierarchy canonical predicate: {config.hierarchy_canonical_predicate}")
    if config.schema_repair_acceptance_policy not in {"needs_review_only", "allow_accept_after_final_guard"}:
        raise ValueError(f"Unknown schema repair acceptance policy: {config.schema_repair_acceptance_policy}")
    if any(
        provider == "kimi"
        for provider in (config.judge_provider, config.verifier_provider, config.adjudicator_provider)
    ) and not config.enable_kimi_experimental:
        raise CloudProviderError(
            "kimi",
            "disabled_for_relationship_workflow",
            "Kimi Code chat completion is disabled for this workflow because the Kimi Code endpoint is restricted to coding-agent integrations. Use DeepSeek or local Ollama.",
            retryable=False,
        )
    cloud_requested = config.council_mode != "local_only" or any(
        provider in {"kimi", "deepseek"}
        for provider in (config.judge_provider, config.verifier_provider, config.adjudicator_provider)
    )
    if cloud_requested and not config.allow_cloud_ai:
        raise CloudAIRequiredError("--allow-cloud-ai is required for DeepSeek council calls.")
    if config.council_mode == "local_only" and config.adjudicator_provider == "auto":
        config.adjudicator_provider = "none"
    if config.council_mode == "local_only" and any(
        provider in {"kimi", "deepseek"}
        for provider in (config.judge_provider, config.verifier_provider, config.adjudicator_provider)
    ):
        raise CloudAIRequiredError("local_only mode forbids Kimi or DeepSeek providers; choose a cloud council mode.")
    if config.council_mode in DEEPSEEK_LOCAL_MODES:
        if config.verify_uncertain is False:
            config.verify_uncertain = True
        if config.verify_accepted_cloud is None:
            config.verify_accepted_cloud = False
        if config.adjudicate_disagreements is None:
            config.adjudicate_disagreements = True
        if config.adjudicator_provider == "none":
            config.adjudicator_provider = "auto"
    elif config.council_mode == "cloud_first":
        if config.adjudicate_disagreements is None:
            config.adjudicate_disagreements = True
        if config.adjudicator_provider == "none":
            config.adjudicator_provider = "auto"
        if config.verify_accepted_cloud is None:
            config.verify_accepted_cloud = False
    elif config.council_mode == "local_first_cloud_verify":
        if config.verify_accepted_cloud is None:
            config.verify_accepted_cloud = False
        if config.adjudicate_disagreements is None:
            config.adjudicate_disagreements = True
        if config.adjudicator_provider == "none":
            config.adjudicator_provider = "auto"
    else:
        if config.verify_accepted_cloud is None:
            config.verify_accepted_cloud = False
        if config.adjudicate_disagreements is None:
            config.adjudicate_disagreements = False
    if config.kimi_verify_uncertain is None:
        config.kimi_verify_uncertain = False
    if config.deepseek_flash_max_calls is not None and config.deepseek_flash_max_calls <= config.max_pairs and config.council_mode in DEEPSEEK_LOCAL_MODES:
        logger.warning(
            "deepseek-flash-max-calls is <= max-pairs; verification/fallback use may exhaust the Flash cap and trigger local Ollama fallback."
        )
    if config.allow_cloud_ai:
        if config.enable_kimi_experimental:
            ensure_allowed_cloud_base_url(
                "kimi",
                config.kimi_base_url,
                KIMI_ALLOWED_BASE_URLS,
                config.allow_custom_kimi_base_url,
            )
        ensure_allowed_cloud_base_url(
            "deepseek",
            config.deepseek_base_url,
            DEEPSEEK_ALLOWED_BASE_URLS,
            config.allow_custom_deepseek_base_url,
        )


def ensure_allowed_cloud_base_url(
    provider: str,
    base_url: str,
    allowed: set[str],
    allow_custom: bool,
) -> None:
    normalized = base_url.rstrip("/")
    if allow_custom or normalized in allowed:
        return
    raise CloudProviderError(
        provider,
        "disabled_custom_base_url",
        f"Custom {provider} base URL is disabled for v1.",
        retryable=False,
    )


def resolve_path(path: Path | str, repo_root: Path | None = None) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    root = repo_root or get_repo_root()
    return root / candidate


def load_backbone_graph(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Backbone graph payload must be an object: {path}")
    records = payload.get("records", [])
    relationships = payload.get("relationships", [])
    if not isinstance(records, list):
        raise ValueError("Backbone graph records must be a list")
    if not isinstance(relationships, list):
        raise ValueError("Backbone graph relationships must be a list")
    return records, relationships


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def _as_text_tuple(value: Any) -> tuple[str, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, (list, tuple, set)):
        return tuple(_as_text(item) for item in value if _as_text(item) != "")
    return (_as_text(value),)


def make_node_view(raw: dict[str, Any]) -> BackboneNodeView:
    node_id = _as_text(raw.get("id"))
    if not node_id:
        raise ValueError("Backbone node is missing id")
    return BackboneNodeView(
        id=node_id,
        canonical_id=_as_text(raw.get("canonical_id")),
        record_type=_as_text(raw.get("record_type")),
        label=_as_text(raw.get("label")),
        pref_label=_as_text(raw.get("pref_label")),
        definition=_as_text(raw.get("definition")),
        aliases=_as_text_tuple(raw.get("aliases")),
        path_code=_as_text(raw.get("path_code")),
        level=_as_text(raw.get("level")),
        parent_path_code=_as_text(raw.get("parent_path_code")),
        review_status=_as_text(raw.get("review_status")),
        release_version=_as_text(raw.get("release_version")),
        discipline=_as_text_tuple(raw.get("discipline")),
        lifecycle_phase=_as_text_tuple(raw.get("lifecycle_phase")),
        source_family_ids=_as_text_tuple(raw.get("source_family_ids")),
        semantic_overlay_category=_as_text(raw.get("semantic_overlay_category")),
        generation_method=_as_text(raw.get("generation_method")),
        provenance_note=_as_text(raw.get("provenance_note")),
        visibility=_as_text(raw.get("visibility")),
        raw=raw,
    )


def make_edge_view(raw: dict[str, Any]) -> ExistingEdgeView | None:
    from_id = _as_text(raw.get("from_id"))
    to_id = _as_text(raw.get("to_id"))
    predicate = _as_text(raw.get("predicate"))
    if not from_id or not to_id or not predicate:
        return None
    return ExistingEdgeView(from_id=from_id, to_id=to_id, predicate=predicate, raw=raw)


def build_node_text(node: BackboneNodeView) -> str:
    label = node.label or node.pref_label
    lines = [
        f"ID: {node.id}",
        f"Label: {label}",
        f"Preferred Label: {node.pref_label}",
        f"Definition: {node.definition}",
        f"Aliases: {', '.join(node.aliases)}",
        f"Path Code: {node.path_code}",
        f"Level: {node.level}",
        f"Parent Path Code: {node.parent_path_code}",
        f"Discipline: {', '.join(node.discipline)}",
        f"Lifecycle Phase: {', '.join(node.lifecycle_phase)}",
        f"Source Families: {', '.join(node.source_family_ids)}",
    ]
    return "\n".join(lines)


def safe_model_name(model: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", model)
    return safe.strip("._-") or "model"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_pair_key(left: str, right: str) -> str:
    first, second = sorted((left, right))
    return f"{first}||{second}"


def build_edge_key(from_id: str, predicate: str, to_id: str) -> str:
    return f"{from_id}--{predicate}--{to_id}"


def is_duplicate_edge_record(
    candidate_edge: dict[str, Any],
    existing_edge_keys: set[str],
    accepted_edge_keys: list[str] | set[str],
) -> bool:
    all_keys = set(existing_edge_keys)
    all_keys.update(accepted_edge_keys)
    edge_key = _as_text(candidate_edge.get("edge_key"))
    if edge_key in all_keys:
        return True
    if candidate_edge.get("predicate") == "conflicts_with":
        reverse_key = build_edge_key(
            _as_text(candidate_edge.get("to_id")),
            "conflicts_with",
            _as_text(candidate_edge.get("from_id")),
        )
        return reverse_key in all_keys
    return False


def build_existing_edge_keys(edges: list[dict[str, Any]] | list[ExistingEdgeView]) -> set[str]:
    keys: set[str] = set()
    for edge in edges:
        view = edge if isinstance(edge, ExistingEdgeView) else make_edge_view(edge)
        if view is not None:
            keys.add(view.edge_key)
    return keys


def build_existing_pair_index(edges: list[dict[str, Any]] | list[ExistingEdgeView]) -> set[str]:
    keys: set[str] = set()
    for edge in edges:
        view = edge if isinstance(edge, ExistingEdgeView) else make_edge_view(edge)
        if view is not None:
            keys.add(view.pair_key)
    return keys


def load_embedding_cache(path: Path) -> dict[tuple[str, str, str], EmbeddingRecord]:
    records: dict[tuple[str, str, str], EmbeddingRecord] = {}
    if not path.exists():
        return records
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = EmbeddingRecord.model_validate(json.loads(line))
        except Exception as exc:
            logger.warning("Skipping invalid embedding cache record %s:%d: %s", path, line_number, exc)
            continue
        records[(record.node_id, record.embedding_model, record.text_hash)] = record
    return records


def save_embedding_record_jsonl(path: Path, record: EmbeddingRecord) -> None:
    payload = record.model_dump(exclude_none=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(sanitize_for_artifact(obj), ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def iter_jsonl_objects(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    if not path.exists():
        return
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError(f"{path}:{line_number} JSONL record must be an object")
        yield line_number, data


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp")
    tmp_path.write_text(
        json.dumps(sanitize_for_artifact(obj), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    tmp_path.replace(path)


def build_progress_event(
    *,
    run_id: str,
    phase: str,
    event_type: str,
    message: str,
    pair_key: str | None = None,
    edge_key: str | None = None,
    provider: str | None = None,
    model: str | None = None,
    confidence: float | None = None,
    reason: str | None = None,
    counts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return sanitize_for_artifact(
        {
            "schema_version": "aec-relationship-improvement-event/v1",
            "run_id": run_id,
            "created_at_utc": utc_now(),
            "phase": phase,
            "event_type": event_type,
            "message": truncate_error_text(message, 300),
            "pair_key": pair_key,
            "edge_key": edge_key,
            "provider": provider,
            "model": model,
            "confidence": confidence,
            "reason": reason,
            "counts": counts or {},
        }
    )


def append_progress_event(
    files: dict[str, Path],
    checkpoint: Checkpoint,
    reporter: "ProgressReporter",
    event: dict[str, Any],
) -> None:
    append_jsonl(files["events"], event)
    checkpoint.recent_events.append(event)
    checkpoint.recent_events = checkpoint.recent_events[-MAX_RECENT_EVENTS:]
    reporter.record_event(
        _as_text(event.get("event_type")) or "event",
        _as_text(event.get("message")),
        event,
    )


class ProgressReporter:
    def start_run(self, config: RunConfig, run_id: str, output_dir: Path) -> None:
        pass

    def set_phase(self, name: str, detail: str | None = None) -> None:
        pass

    def set_totals(self, nodes: int | None = None, pairs: int | None = None, candidates: int | None = None) -> None:
        pass

    def update_embeddings(
        self,
        processed: int | None = None,
        hits: int | None = None,
        misses: int | None = None,
        dimensions: int | None = None,
    ) -> None:
        pass

    def update_candidates(
        self,
        generated: int | None = None,
        skipped_existing: int | None = None,
        skipped_duplicate: int | None = None,
    ) -> None:
        pass

    def update_pair_processed(
        self,
        pair_key: str,
        status: str,
        provider_route: list[dict[str, Any]] | None = None,
    ) -> None:
        pass

    def update_decision(
        self,
        result_type: str,
        edge_key: str | None = None,
        reason: str | None = None,
        confidence: float | None = None,
    ) -> None:
        pass

    def update_cloud_usage(self, usage: CloudUsage) -> None:
        pass

    def update_provider_health(self, health: ProviderHealth) -> None:
        pass

    def update_checkpoint_age(self, seconds: float | None) -> None:
        pass

    def record_event(self, level: str, message: str, metadata: dict[str, Any] | None = None) -> None:
        pass

    def finish(self, summary: RunSummary | None) -> None:
        pass

    def close(self) -> None:
        pass


class NullProgressReporter(ProgressReporter):
    pass


class PlainProgressReporter(ProgressReporter):
    def __init__(self, *, log_every_seconds: float = 30.0, stream: Any | None = None) -> None:
        self.log_every_seconds = max(0.0, float(log_every_seconds))
        self.stream = stream or sys.stderr
        self.started_at = time.monotonic()
        self.last_summary_at = 0.0
        self.phase = "loading"
        self.run_id = ""
        self.output_dir = ""
        self.nodes = None
        self.pairs = None
        self.embeddings_processed = 0
        self.embedding_hits = 0
        self.embedding_misses = 0
        self.candidates = 0
        self.processed_pairs = 0
        self.accepted = 0
        self.review = 0
        self.rejected = 0
        self.errors = 0
        self.provider = "unknown"
        self.cloud_calls = 0
        self.deepseek_flash_calls = 0
        self.deepseek_pro_calls = 0
        self.cloud_cost = 0.0
        self.fallbacks = 0
        self.rejection_counts: dict[str, int] = {}

    def _write(self, message: str) -> None:
        print(message, file=self.stream, flush=True)

    def start_run(self, config: RunConfig, run_id: str, output_dir: Path) -> None:
        self.run_id = run_id
        self.output_dir = str(output_dir)
        self._write(f"[AEC-REL] run={run_id} mode={config.council_mode} pending_only=true output={output_dir}")

    def set_phase(self, name: str, detail: str | None = None) -> None:
        self.phase = name
        suffix = f" detail={detail}" if detail else ""
        self._write(f"[AEC-REL] phase={name}{suffix}")

    def set_totals(self, nodes: int | None = None, pairs: int | None = None, candidates: int | None = None) -> None:
        if nodes is not None:
            self.nodes = nodes
        if pairs is not None:
            self.pairs = pairs
        if candidates is not None:
            self.candidates = candidates

    def update_embeddings(
        self,
        processed: int | None = None,
        hits: int | None = None,
        misses: int | None = None,
        dimensions: int | None = None,
    ) -> None:
        if processed is not None:
            self.embeddings_processed = processed
        if hits is not None:
            self.embedding_hits = hits
        if misses is not None:
            self.embedding_misses = misses
        self._maybe_summary()

    def update_candidates(
        self,
        generated: int | None = None,
        skipped_existing: int | None = None,
        skipped_duplicate: int | None = None,
    ) -> None:
        if generated is not None:
            self.candidates = generated
        self._maybe_summary()

    def update_pair_processed(
        self,
        pair_key: str,
        status: str,
        provider_route: list[dict[str, Any]] | None = None,
    ) -> None:
        self.processed_pairs += 1
        if provider_route:
            last = provider_route[-1]
            self.provider = _as_text(last.get("model")) or _as_text(last.get("provider")) or self.provider
        self._maybe_summary(force=status in {"accepted", "error"})

    def update_decision(
        self,
        result_type: str,
        edge_key: str | None = None,
        reason: str | None = None,
        confidence: float | None = None,
    ) -> None:
        if result_type == "accepted":
            self.accepted += 1
        elif result_type == "needs_review":
            self.review += 1
        elif result_type == "rejected":
            self.rejected += 1
            if reason:
                self.rejection_counts[reason] = self.rejection_counts.get(reason, 0) + 1
        elif result_type == "error":
            self.errors += 1
        if result_type == "accepted" and edge_key:
            self._write(f"[AEC-REL] accepted edge={edge_key} confidence={confidence}")
        self._maybe_summary()

    def update_cloud_usage(self, usage: CloudUsage) -> None:
        self.cloud_calls = usage.cloud_call_count
        self.deepseek_flash_calls = usage.deepseek_flash_call_count
        self.deepseek_pro_calls = usage.deepseek_pro_call_count
        self.cloud_cost = usage.cloud_estimated_cost_usd
        self.fallbacks = usage.local_fallback_call_count
        self._maybe_summary()

    def record_event(self, level: str, message: str, metadata: dict[str, Any] | None = None) -> None:
        if level in {"phase_started", "accepted", "provider_failover", "rate_limit", "retry", "error", "summary"}:
            self._write(f"[AEC-REL] event={level} {truncate_error_text(message, 220)}")

    def finish(self, summary: RunSummary | None) -> None:
        if summary is None:
            return
        self.accepted = summary.accepted_count
        self.review = summary.candidate_review_count
        self.rejected = summary.rejected_count
        self.errors = summary.error_count
        self.processed_pairs = summary.processed_count
        self._maybe_summary(force=True)

    def _maybe_summary(self, *, force: bool = False) -> None:
        now = time.monotonic()
        if not force and self.log_every_seconds > 0 and now - self.last_summary_at < self.log_every_seconds:
            return
        self.last_summary_at = now
        elapsed = now - self.started_at
        eta = None
        if self.pairs and self.processed_pairs > 0:
            remaining = max(0, self.pairs - self.processed_pairs)
            eta = elapsed / self.processed_pairs * remaining
        self._write(
            "[AEC-REL] "
            f"phase={self.phase} "
            f"pairs={self.processed_pairs}/{self.pairs if self.pairs is not None else '?'} "
            f"accepted={self.accepted} rejected={self.rejected} review={self.review} errors={self.errors} "
            f"cloud_calls={self.cloud_calls} flash={self.deepseek_flash_calls} pro={self.deepseek_pro_calls} "
            f"cost=${self.cloud_cost:.6f} fallback={self.fallbacks} "
            f"provider={self.provider} elapsed={format_duration(elapsed)} eta={format_duration(eta)}"
        )


class RichProgressReporter(PlainProgressReporter):
    def __init__(
        self,
        *,
        refresh_per_second: float = 2.0,
        show_recent: int = 8,
        transient: bool = False,
        console: Any | None = None,
    ) -> None:
        super().__init__(log_every_seconds=0, stream=sys.stderr)
        try:
            from rich.console import Console
            from rich.live import Live
            from rich.panel import Panel
            from rich.table import Table
        except ImportError as exc:
            raise RuntimeError("Rich progress UI requested but rich is not installed. Install with: pip install rich") from exc
        self._Console = Console
        self._Live = Live
        self._Panel = Panel
        self._Table = Table
        self.console = console or Console(stderr=True)
        self.refresh_per_second = max(0.2, float(refresh_per_second))
        self.show_recent = max(1, int(show_recent))
        self.transient = transient
        self.live: Any | None = None
        self.recent_events: list[dict[str, Any]] = []

    def _write(self, message: str) -> None:
        if self.live is None:
            self.console.print(message)

    def start_run(self, config: RunConfig, run_id: str, output_dir: Path) -> None:
        self.run_id = run_id
        self.output_dir = str(output_dir)
        self.phase = "loading"
        self.live = self._Live(
            self._render(),
            console=self.console,
            refresh_per_second=self.refresh_per_second,
            transient=self.transient,
        )
        self.live.start()

    def set_phase(self, name: str, detail: str | None = None) -> None:
        self.phase = name if detail is None else f"{name}: {detail}"
        self._refresh()

    def update_embeddings(self, processed: int | None = None, hits: int | None = None, misses: int | None = None, dimensions: int | None = None) -> None:
        super().update_embeddings(processed, hits, misses, dimensions)
        self._refresh()

    def update_candidates(self, generated: int | None = None, skipped_existing: int | None = None, skipped_duplicate: int | None = None) -> None:
        super().update_candidates(generated, skipped_existing, skipped_duplicate)
        self._refresh()

    def update_pair_processed(self, pair_key: str, status: str, provider_route: list[dict[str, Any]] | None = None) -> None:
        super().update_pair_processed(pair_key, status, provider_route)
        self._refresh()

    def update_decision(self, result_type: str, edge_key: str | None = None, reason: str | None = None, confidence: float | None = None) -> None:
        super().update_decision(result_type, edge_key, reason, confidence)
        self._refresh()

    def update_cloud_usage(self, usage: CloudUsage) -> None:
        super().update_cloud_usage(usage)
        self._refresh()

    def record_event(self, level: str, message: str, metadata: dict[str, Any] | None = None) -> None:
        event = dict(metadata or {})
        event["event_type"] = level
        event["message"] = message
        self.recent_events.append(sanitize_for_artifact(event))
        self.recent_events = self.recent_events[-self.show_recent :]
        self._refresh()

    def finish(self, summary: RunSummary | None) -> None:
        super().finish(summary)
        self._refresh()

    def close(self) -> None:
        if self.live is not None:
            self.live.update(self._render())
            self.live.stop()
            self.live = None

    def _refresh(self) -> None:
        if self.live is not None:
            self.live.update(self._render())

    def _render(self) -> Any:
        table = self._Table.grid(expand=True)
        table.add_column(ratio=1)
        table.add_column(ratio=1)
        elapsed = format_duration(time.monotonic() - self.started_at)
        table.add_row("Vitruvius AEC Relationship Improvement", f"run={self.run_id}")
        table.add_row("phase", self.phase)
        table.add_row("output", truncate_error_text(self.output_dir, 120))
        table.add_row("elapsed", elapsed)
        metrics = self._Table(title="Metrics")
        metrics.add_column("metric")
        metrics.add_column("value")
        for key, value in [
            ("pairs", f"{self.processed_pairs}/{self.pairs if self.pairs is not None else '?'}"),
            ("embeddings", f"{self.embeddings_processed}/{self.nodes if self.nodes is not None else '?'}"),
            ("candidates", str(self.candidates)),
            ("accepted", str(self.accepted)),
            ("needs_review", str(self.review)),
            ("rejected", str(self.rejected)),
            ("errors", str(self.errors)),
            ("cloud_calls", str(self.cloud_calls)),
            ("deepseek_flash", str(self.deepseek_flash_calls)),
            ("deepseek_pro", str(self.deepseek_pro_calls)),
            ("cloud_cost", f"${self.cloud_cost:.6f}"),
            ("local_fallbacks", str(self.fallbacks)),
            ("provider", self.provider),
        ]:
            metrics.add_row(key, value)
        events = self._Table(title="Recent Events")
        events.add_column("time")
        events.add_column("type")
        events.add_column("message")
        for event in self.recent_events[-self.show_recent :]:
            events.add_row(
                _as_text(event.get("created_at_utc"))[-9:],
                _as_text(event.get("event_type")),
                truncate_error_text(_as_text(event.get("message")), 90),
            )
        outer = self._Table.grid(expand=True)
        outer.add_column(ratio=1)
        outer.add_column(ratio=1)
        outer.add_row(metrics, events)
        root = self._Table.grid(expand=True)
        root.add_column()
        root.add_row(table)
        root.add_row(outer)
        return self._Panel.fit(root, title="Pending-only relationship discovery")


def rich_is_available() -> bool:
    try:
        __import__("rich")
        return True
    except ImportError:
        return False


def create_progress_reporter(config: RunConfig) -> ProgressReporter:
    mode = resolve_progress_mode(config.progress_mode, force_rich_in_git_bash=config.force_rich_in_git_bash)
    config.progress_mode_effective = mode
    if mode == "off":
        return NullProgressReporter()
    if mode == "plain":
        return PlainProgressReporter(log_every_seconds=config.progress_log_every_seconds)
    if mode == "rich":
        if not rich_is_available():
            raise RuntimeError("Rich progress UI requested but rich is not installed. Install with: pip install rich")
        return RichProgressReporter(
            refresh_per_second=config.progress_refresh_per_second,
            show_recent=config.progress_show_recent,
            transient=config.progress_transient,
        )
    return PlainProgressReporter(log_every_seconds=config.progress_log_every_seconds)


def running_in_git_bash(env: dict[str, str] | None = None) -> bool:
    env = env or os.environ
    return bool(env.get("MSYSTEM") or env.get("MINGW_CHOST"))


def rich_terminal_compatible(*, force_rich_in_git_bash: bool = False, env: dict[str, str] | None = None) -> bool:
    env = env or os.environ
    if running_in_git_bash(env) and not force_rich_in_git_bash:
        if not env.get("WT_SESSION"):
            return False
    return True


def resolve_progress_mode(
    requested: str,
    *,
    force_rich_in_git_bash: bool = False,
    stdout_is_tty: bool | None = None,
    env: dict[str, str] | None = None,
    rich_available: bool | None = None,
) -> str:
    if requested == "off":
        return "off"
    if requested == "plain":
        return "plain"
    if requested == "rich":
        return "rich"
    available = rich_is_available() if rich_available is None else rich_available
    is_tty = sys.stdout.isatty() if stdout_is_tty is None else stdout_is_tty
    if available and is_tty and rich_terminal_compatible(force_rich_in_git_bash=force_rich_in_git_bash, env=env):
        return "rich"
    return "plain"


@dataclass
class WatchRunConfig:
    run_id: str | None = None
    output_root: Path = DEFAULT_OUTPUT_ROOT
    output_dir: Path | None = None
    progress_mode: str = "auto"
    refresh_seconds: float = 2.0
    show_recent: int = 12
    exit_when_complete: bool = False
    watch_latest: bool = False
    force_rich_in_git_bash: bool = False


@dataclass
class WatchRunSnapshot:
    output_dir: Path
    run_id: str
    checkpoint: dict[str, Any] = field(default_factory=dict)
    report: dict[str, Any] = field(default_factory=dict)
    accepted_count: int = 0
    rejected_count: int = 0
    candidate_count: int = 0
    error_count: int = 0
    validation_error_count: int = 0
    audit_count: int = 0
    corrupt_jsonl_count: int = 0
    latest_records: list[dict[str, Any]] = field(default_factory=list)
    latest_validation_errors: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    checkpoint_age_seconds: float | None = None

    @property
    def status(self) -> str:
        return _as_text(self.checkpoint.get("status") or self.report.get("status") or "unknown")


def safe_read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def read_jsonl_records_tolerant(path: Path, *, limit: int | None = None) -> tuple[list[dict[str, Any]], int]:
    if not path.exists():
        return [], 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return [], 0
    records: list[dict[str, Any]] = []
    corrupt_count = 0
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            if line_number == len(lines):
                continue
            corrupt_count += 1
            continue
        if isinstance(data, dict):
            records.append(sanitize_for_artifact(data))
    if limit is not None:
        return records[-limit:], corrupt_count
    return records, corrupt_count


def resolve_watch_output_dir(config: WatchRunConfig, repo_root: Path | None = None) -> Path:
    repo_root = repo_root or get_repo_root()
    if config.output_dir is not None:
        return resolve_path(config.output_dir, repo_root)
    output_root = resolve_path(config.output_root, repo_root)
    if config.watch_latest:
        candidates = sorted((path for path in output_root.iterdir() if path.is_dir()), reverse=True) if output_root.exists() else []
        if not candidates:
            raise FileNotFoundError(f"No run directories found under {output_root}")
        return candidates[0]
    if config.run_id:
        run_candidate = Path(config.run_id)
        if run_candidate.exists() or any(sep in config.run_id for sep in ("/", "\\")):
            return resolve_path(run_candidate, repo_root)
        return output_root / config.run_id
    raise ValueError("Specify --run-id, --output-dir, or --watch-latest")


def load_watch_snapshot(output_dir: Path, *, show_recent: int = 12) -> WatchRunSnapshot:
    checkpoint = safe_read_json(output_dir / "relationship-improvement-checkpoint.json")
    report = safe_read_json(output_dir / "relationship-improvement-report.json")
    accepted, accepted_corrupt = read_jsonl_records_tolerant(output_dir / "accepted-relationships.jsonl")
    rejected, rejected_corrupt = read_jsonl_records_tolerant(output_dir / "rejected-relationships.jsonl")
    candidates, candidates_corrupt = read_jsonl_records_tolerant(output_dir / "candidate-relationships.jsonl")
    errors, errors_corrupt = read_jsonl_records_tolerant(output_dir / "errors.jsonl")
    validation_errors, validation_corrupt = read_jsonl_records_tolerant(output_dir / "validation-errors.jsonl")
    audit, audit_corrupt = read_jsonl_records_tolerant(output_dir / "relationship-council-audit.jsonl")
    events, events_corrupt = read_jsonl_records_tolerant(output_dir / "relationship-improvement-events.jsonl", limit=show_recent)
    latest_records = (accepted[-show_recent:] + candidates[-show_recent:] + rejected[-show_recent:] + errors[-show_recent:])[-show_recent:]
    run_id = _as_text(checkpoint.get("run_id") or report.get("run_id") or output_dir.name)
    return WatchRunSnapshot(
        output_dir=output_dir,
        run_id=run_id,
        checkpoint=checkpoint,
        report=report,
        accepted_count=len(accepted),
        rejected_count=len(rejected),
        candidate_count=len(candidates),
        error_count=len(errors),
        validation_error_count=len(validation_errors),
        audit_count=len(audit),
        corrupt_jsonl_count=sum(
            [
                accepted_corrupt,
                rejected_corrupt,
                candidates_corrupt,
                errors_corrupt,
                validation_corrupt,
                audit_corrupt,
                events_corrupt,
            ]
        ),
        latest_records=latest_records,
        latest_validation_errors=validation_errors[-show_recent:],
        events=events,
        checkpoint_age_seconds=seconds_since_utc(_as_text(checkpoint.get("last_updated_at_utc"))),
    )


def render_watch_plain(snapshot: WatchRunSnapshot) -> str:
    usage = snapshot.checkpoint.get("cloud_usage") or snapshot.report.get("cloud_usage") or {}
    return (
        "[AEC-REL-WATCH] "
        f"run={snapshot.run_id} status={snapshot.status} phase={snapshot.checkpoint.get('phase', 'unknown')} "
        f"processed={snapshot.checkpoint.get('processed_pair_count', len(snapshot.checkpoint.get('processed_pair_keys') or []))} "
        f"accepted={snapshot.accepted_count} review={snapshot.candidate_count} rejected={snapshot.rejected_count} errors={snapshot.error_count} "
        f"validation_errors={snapshot.validation_error_count} "
        f"corrupt_jsonl={snapshot.corrupt_jsonl_count} "
        f"cloud_calls={usage.get('cloud_call_count', 0)} cost=${float(usage.get('cloud_estimated_cost_usd') or 0.0):.6f} "
        f"fallback={usage.get('local_fallback_call_count', 0)} checkpoint_age={format_duration(snapshot.checkpoint_age_seconds)} "
        f"output={snapshot.output_dir}"
    )


def render_watch_rich(snapshot: WatchRunSnapshot) -> Any:
    from rich.panel import Panel
    from rich.table import Table
    usage = snapshot.checkpoint.get("cloud_usage") or snapshot.report.get("cloud_usage") or {}
    health = snapshot.checkpoint.get("provider_health") or {}
    table = Table(title="Vitruvius AEC Relationship Run Watcher")
    table.add_column("metric")
    table.add_column("value")
    for key, value in [
        ("run_id", snapshot.run_id),
        ("status", snapshot.status),
        ("phase", _as_text(snapshot.checkpoint.get("phase")) or "unknown"),
        ("checkpoint_age", format_duration(snapshot.checkpoint_age_seconds)),
        ("processed", _as_text(snapshot.checkpoint.get("processed_pair_count"))),
        ("accepted", str(snapshot.accepted_count)),
        ("needs_review", str(snapshot.candidate_count)),
        ("rejected", str(snapshot.rejected_count)),
        ("errors", str(snapshot.error_count)),
        ("validation_errors", str(snapshot.validation_error_count)),
        ("audit_records", str(snapshot.audit_count)),
        ("corrupt_jsonl", str(snapshot.corrupt_jsonl_count)),
        ("cloud_calls", _as_text(usage.get("cloud_call_count"))),
        ("deepseek_flash", _as_text(usage.get("deepseek_flash_call_count"))),
        ("deepseek_pro", _as_text(usage.get("deepseek_pro_call_count"))),
        ("cloud_cost", f"${float(usage.get('cloud_estimated_cost_usd') or 0.0):.6f}"),
        ("budget_remaining", _as_text(snapshot.checkpoint.get("cloud_budget_remaining_usd")) or "unknown"),
        ("provider_health", json.dumps(health.get("states", {}), sort_keys=True)),
        ("output", str(snapshot.output_dir)),
    ]:
        table.add_row(key, value)
    events = Table(title="Recent Events")
    events.add_column("time")
    events.add_column("type")
    events.add_column("message")
    for event in snapshot.events[-12:]:
        events.add_row(
            _as_text(event.get("created_at_utc"))[-9:],
            _as_text(event.get("event_type")),
            truncate_error_text(_as_text(event.get("message")), 100),
        )
    for event in snapshot.latest_validation_errors[-3:]:
        events.add_row(
            _as_text(event.get("created_at_utc"))[-9:],
            "validation_error",
            truncate_error_text(
                f"{event.get('role')} {event.get('provider')} {event.get('reason')} {event.get('failed_fields')}",
                100,
            ),
        )
    root = Table.grid(expand=True)
    root.add_column()
    root.add_row(table)
    root.add_row(events)
    return Panel.fit(root, title="Read-only watcher")


def watch_snapshot_is_complete(snapshot: WatchRunSnapshot) -> bool:
    if snapshot.report.get("status") == "completed":
        return True
    return snapshot.checkpoint.get("status") == "completed" and snapshot.checkpoint.get("phase") != "writing_report"


def watch_relationship_run(
    config: WatchRunConfig,
    *,
    sleep: Callable[[float], None] = time.sleep,
    max_iterations: int | None = None,
) -> int:
    output_dir = resolve_watch_output_dir(config)
    mode = config.progress_mode
    if mode == "off":
        return 0
    if mode == "auto":
        mode = resolve_progress_mode(
            "auto",
            force_rich_in_git_bash=config.force_rich_in_git_bash,
            stdout_is_tty=sys.stdout.isatty(),
        )
    if mode == "rich" and not rich_is_available():
        raise RuntimeError("Rich progress UI requested but rich is not installed. Install with: pip install rich")

    if mode == "rich":
        from rich.console import Console
        from rich.live import Live
        console = Console(stderr=True)
        with Live(console=console, refresh_per_second=max(0.2, 1.0 / max(config.refresh_seconds, 0.1))) as live:
            iterations = 0
            while True:
                snapshot = load_watch_snapshot(output_dir, show_recent=config.show_recent)
                live.update(render_watch_rich(snapshot))
                iterations += 1
                if config.exit_when_complete and watch_snapshot_is_complete(snapshot):
                    break
                if max_iterations is not None and iterations >= max_iterations:
                    break
                sleep(config.refresh_seconds)
        return 0

    iterations = 0
    while True:
        snapshot = load_watch_snapshot(output_dir, show_recent=config.show_recent)
        print(render_watch_plain(snapshot), file=sys.stderr, flush=True)
        iterations += 1
        if config.exit_when_complete and watch_snapshot_is_complete(snapshot):
            break
        if max_iterations is not None and iterations >= max_iterations:
            break
        sleep(config.refresh_seconds)
    return 0


def get_or_create_embeddings(
    nodes: list[BackboneNodeView],
    embedding_model: str,
    *,
    stable_cache_path: Path | None,
    run_cache_path: Path | None,
    embed_texts: Callable[[list[str]], list[list[float]]],
    store_text: bool,
    batch_size: int = 1,
    progress_callback: Callable[[int, int, int, int | None, float | None], None] | None = None,
) -> tuple[dict[str, list[float]], dict[str, int | None]]:
    cache: dict[tuple[str, str, str], EmbeddingRecord] = {}
    if stable_cache_path is not None:
        cache.update(load_embedding_cache(stable_cache_path))
    if run_cache_path is not None and run_cache_path != stable_cache_path:
        cache.update(load_embedding_cache(run_cache_path))

    embeddings: dict[str, list[float]] = {}
    pending: list[tuple[BackboneNodeView, str, str]] = []
    dimensions: int | None = None
    hits = 0
    misses = 0

    for node in nodes:
        text = build_node_text(node)
        text_hash = sha256_text(text)
        record = cache.get((node.id, embedding_model, text_hash))
        if record is not None:
            if dimensions is None:
                dimensions = record.embedding_dimensions
            elif record.embedding_dimensions != dimensions:
                raise ValueError("Mixed embedding dimensions found in cache")
            embeddings[node.id] = [float(value) for value in record.embedding]
            hits += 1
        else:
            pending.append((node, text, text_hash))
            misses += 1
        if progress_callback is not None:
            progress_callback(len(embeddings), hits, misses, dimensions, None)

    effective_batch_size = max(1, int(batch_size or 1))
    for start in range(0, len(pending), effective_batch_size):
        batch = pending[start : start + effective_batch_size]
        texts = [item[1] for item in batch]
        batch_started = time.monotonic()
        vectors = embed_texts(texts)
        batch_latency = time.monotonic() - batch_started
        if len(vectors) != len(batch):
            raise ValueError("Embedding provider returned a different number of vectors than requested")
        for (node, text, text_hash), vector in zip(batch, vectors, strict=True):
            clean_vector = [float(value) for value in vector]
            if not clean_vector:
                raise ValueError(f"Empty embedding returned for node {node.id}")
            vector_dimensions = len(clean_vector)
            if dimensions is None:
                dimensions = vector_dimensions
            elif vector_dimensions != dimensions:
                raise ValueError("Mixed embedding dimensions returned by embedding provider")
            record = EmbeddingRecord(
                node_id=node.id,
                embedding_model=embedding_model,
                embedding_dimensions=vector_dimensions,
                text_hash=text_hash,
                text=text if store_text else None,
                embedding=clean_vector,
                created_at_utc=utc_now(),
            )
            embeddings[node.id] = clean_vector
            if stable_cache_path is not None:
                save_embedding_record_jsonl(stable_cache_path, record)
            if run_cache_path is not None and run_cache_path != stable_cache_path:
                save_embedding_record_jsonl(run_cache_path, record)
            if progress_callback is not None:
                progress_callback(len(embeddings), hits, misses, dimensions, batch_latency / max(1, len(batch)))

    return embeddings, {
        "cache_hits": hits,
        "cache_misses": misses,
        "embedding_dimensions": dimensions,
    }


def call_ollama_embed(
    *,
    base_url: str,
    model: str,
    inputs: list[str],
    num_ctx: int,
    timeout_seconds: int = 600,
) -> list[list[float]]:
    payload = {
        "model": model,
        "input": inputs if len(inputs) != 1 else inputs[0],
        "keep_alive": 0,
        "options": {"num_ctx": num_ctx},
    }
    response = _post_ollama_json(base_url, "/api/embed", payload, timeout_seconds)
    if "embeddings" in response:
        embeddings = response["embeddings"]
    elif "embedding" in response:
        embeddings = [response["embedding"]]
    else:
        raise ValueError("Ollama embed response did not include embeddings")
    if len(inputs) == 1 and embeddings and isinstance(embeddings[0], (int, float)):
        embeddings = [embeddings]
    if not isinstance(embeddings, list):
        raise ValueError("Ollama embeddings payload must be a list")
    return [[float(value) for value in embedding] for embedding in embeddings]


def call_ollama_generate(
    *,
    base_url: str,
    model: str,
    prompt: str,
    schema: dict[str, Any],
    think: bool,
    num_ctx: int,
    temperature: float,
    num_predict: int,
    timeout_seconds: int = 600,
) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": bool(think),
        "keep_alive": 0,
        "format": schema,
        "options": {
            "num_ctx": num_ctx,
            "temperature": temperature,
            "num_predict": num_predict,
        },
    }
    response = _post_ollama_json(base_url, "/api/generate", payload, timeout_seconds)
    return _as_text(response.get("response", ""))


def _post_ollama_json(
    base_url: str,
    endpoint: str,
    payload: dict[str, Any],
    timeout_seconds: int,
) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}{endpoint}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def make_ollama_embedder(config: RunConfig) -> Callable[[list[str]], list[list[float]]]:
    def embed_texts(texts: list[str]) -> list[list[float]]:
        try:
            return call_ollama_embed(
                base_url=config.ollama_base_url,
                model=config.embedding_model,
                inputs=texts,
                num_ctx=config.num_ctx,
            )
        except Exception:
            if len(texts) <= 1:
                raise
            logger.warning("Batch embedding failed; falling back to single-node embedding calls", exc_info=True)
            vectors: list[list[float]] = []
            for text in texts:
                vectors.extend(
                    call_ollama_embed(
                        base_url=config.ollama_base_url,
                        model=config.embedding_model,
                        inputs=[text],
                        num_ctx=config.num_ctx,
                    )
                )
            return vectors

    return embed_texts


def make_ollama_generator(config: RunConfig) -> Callable[..., str]:
    def generate_text(*, prompt: str, model: str, schema: dict[str, Any]) -> str:
        return call_ollama_generate(
            base_url=config.ollama_base_url,
            model=model,
            prompt=prompt,
            schema=schema,
            think=config.think,
            num_ctx=config.num_ctx,
            temperature=config.temperature,
            num_predict=config.num_predict,
        )

    return generate_text


def get_api_key(env_var: str, provider: str) -> str:
    key = os.getenv(env_var, "")
    if not key:
        raise CloudProviderError(
            provider,
            "disabled_auth_error",
            f"{provider} API key env var is not set: {env_var}",
            retryable=False,
        )
    return key


RELATIONSHIP_DECISION_REJECT_EXAMPLE = {
    "edge_exists": False,
    "predicate": "none",
    "direction": "none",
    "confidence": 0.0,
    "relation_type": "none",
    "relation_category": "none",
    "relation_nature": [],
    "rationale": "No clear governed relationship is supported by the provided node records.",
    "evidence": "none",
    "risk_flags": [],
    "review_recommendation": "reject",
}

RELATIONSHIP_DECISION_ACCEPT_EXAMPLE = {
    "edge_exists": True,
    "predicate": "broader_than",
    "direction": "A_to_B",
    "confidence": 0.91,
    "relation_type": "taxonomy_hierarchy",
    "relation_category": "taxonomy",
    "relation_nature": ["hierarchical"],
    "rationale": "Node A is the broader parent category of Node B based on path_code and level.",
    "evidence": "Node A path_code=ACC; Node B path_code=ACC.ABE.",
    "risk_flags": [],
    "review_recommendation": "accept_candidate",
}

VERIFICATION_DECISION_EXAMPLE = {
    "agrees": True,
    "corrected_edge_exists": True,
    "corrected_predicate": "requires",
    "corrected_direction": "A_to_B",
    "corrected_confidence": 0.87,
    "rationale": "Short verification rationale grounded only in the node records.",
}


def schema_kind(schema: dict[str, Any]) -> str:
    properties = schema.get("properties") if isinstance(schema, dict) else {}
    if isinstance(properties, dict) and "corrected_edge_exists" in properties:
        return "verification"
    return "relationship"


def build_cloud_messages(prompt: str, schema: dict[str, Any], provider: str) -> list[dict[str, str]]:
    kind = schema_kind(schema)
    if kind == "verification":
        examples = [VERIFICATION_DECISION_EXAMPLE]
        schema_name = "VerificationDecision"
        system = (
            "Return JSON only. The response must be one JSON object. Do not include markdown. "
            "Do not include comments. Do not include prose before or after JSON. Be conservative. "
            "Do not invent facts beyond the provided node records or judge decision. "
            "Use exactly the keys shown in the example. All required keys must be present. "
            "Use corrected_confidence as a number from 0.0 to 1.0. "
            "Use corrected_predicate exactly as one allowed predicate or none. "
            "Use corrected_direction exactly as A_to_B, B_to_A, undirected, or none. "
            "If corrected_edge_exists is false, corrected_predicate and corrected_direction must be none."
        )
    else:
        examples = [RELATIONSHIP_DECISION_REJECT_EXAMPLE, RELATIONSHIP_DECISION_ACCEPT_EXAMPLE]
        schema_name = "RelationshipDecision"
        system = (
            "Return JSON only. The response must be one JSON object. Do not include markdown. "
            "Do not include comments. Do not include prose before or after JSON. Be conservative. "
            "Do not invent facts beyond the provided node records. Do not use blocked predicates. "
            "Use only allowed predicates. If no clear governed relationship exists, return edge_exists=false. "
            "Do not use part_of for taxonomy path hierarchy; use broader_than or narrower_than for path-code hierarchy. "
            "Use exactly the keys shown in the example. All required keys must be present. "
            'Use [] for empty arrays. Use "none" for predicate and direction when edge_exists is false. '
            "Use confidence as a number from 0.0 to 1.0. Use relation_nature and risk_flags as arrays of strings. "
            "Use review_recommendation exactly as one of: accept_candidate, needs_review, reject. "
            "Include evidence and rationale. Do not output prose outside JSON."
        )
    if provider == "deepseek":
        system += " The response must be valid JSON and must fit within max_tokens."
    user = (
        f"{prompt}\n\nReturn JSON only as one {schema_name} object. "
        "Use these exact object shape examples:\n"
        f"{json.dumps(examples, sort_keys=True)}\n\nSchema:\n{json.dumps(schema, sort_keys=True)}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def build_kimi_chat_payload(
    *,
    config: RunConfig,
    prompt: str,
    schema: dict[str, Any],
    use_max_tokens: bool = False,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": config.kimi_model,
        "messages": build_cloud_messages(prompt, schema, "kimi"),
        "response_format": {"type": "json_object"},
        "thinking": {"type": "disabled"} if config.kimi_disable_thinking else {"type": "enabled"},
    }
    if use_max_tokens:
        payload["max_tokens"] = config.kimi_max_tokens
    else:
        payload["max_completion_tokens"] = config.kimi_max_tokens
    return payload


def build_deepseek_chat_payload(
    *,
    config: RunConfig,
    prompt: str,
    schema: dict[str, Any],
    model: str,
) -> dict[str, Any]:
    thinking = {"type": "disabled"}
    payload: dict[str, Any] = {
        "model": model,
        "messages": build_cloud_messages(prompt, schema, "deepseek"),
        "thinking": thinking,
        "response_format": {"type": "json_object"},
        "max_tokens": config.deepseek_max_tokens,
        "stream": False,
    }
    if not config.deepseek_disable_thinking:
        payload["thinking"] = {"type": "enabled"}
        payload["reasoning_effort"] = config.deepseek_reasoning_effort
    return payload


def build_cloud_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def post_cloud_json(
    *,
    base_url: str,
    payload: dict[str, Any],
    api_key: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=body,
        headers=build_cloud_headers(api_key),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = ""
        try:
            body_text = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body_text = ""
        raise map_http_error_to_provider_error("cloud", exc.code, body_text) from exc
    except TimeoutError as exc:
        raise CloudProviderError("cloud", "disabled_timeout", "Cloud provider timed out") from exc
    except OSError as exc:
        raise CloudProviderError("cloud", "network_error", truncate_error_text(str(exc))) from exc


def map_http_error_to_provider_error(provider: str, status_code: int, body_text: str) -> CloudProviderError:
    lowered = body_text.lower()
    if status_code in {401, 403}:
        return CloudProviderError(provider, "disabled_auth_error", "Cloud provider authentication failed.", status_code=status_code, retryable=False)
    if status_code == 429:
        return CloudProviderError(provider, "disabled_rate_limit", "Cloud provider rate limited the request.", status_code=status_code)
    if any(token in lowered for token in ("quota", "insufficient balance", "membership expired", "exhausted")):
        return CloudProviderError(provider, "exhausted", "Cloud provider quota is exhausted.", status_code=status_code, retryable=False)
    if "max_completion_tokens" in lowered or "invalid parameter" in lowered:
        return CloudProviderError(provider, "invalid_parameter", "Cloud provider rejected a request parameter.", status_code=status_code)
    return CloudProviderError(provider, "provider_http_error", f"Cloud provider HTTP {status_code}.", status_code=status_code)


def extract_chat_content(response: dict[str, Any], provider: str, model: str) -> CloudChatResponse:
    raw_excerpt_source = json.dumps(sanitize_for_artifact(response), ensure_ascii=False, sort_keys=True)
    usage = sanitize_for_artifact(response.get("usage") or {})
    choices = response.get("choices") or []
    if not choices:
        raise CloudResponseRejectedError(
            f"empty_{provider}_response",
            f"{provider} response contained no choices",
            provider=provider,
            model=model,
            raw_response=raw_excerpt_source,
            usage=usage,
        )
    first = choices[0] or {}
    finish_reason = first.get("finish_reason")
    if provider == "deepseek":
        if finish_reason == "length":
            raise CloudResponseRejectedError(
                "deepseek_json_truncated",
                "DeepSeek response ended because max tokens were reached.",
                provider=provider,
                model=model,
                raw_response=raw_excerpt_source,
                finish_reason=_as_text(finish_reason),
                usage=usage,
            )
        if finish_reason in {"content_filter", "insufficient_system_resource"}:
            raise CloudResponseRejectedError(
                f"deepseek_{finish_reason}",
                f"DeepSeek finish_reason={finish_reason}",
                provider=provider,
                model=model,
                raw_response=raw_excerpt_source,
                finish_reason=_as_text(finish_reason),
                usage=usage,
            )
    message = first.get("message") or {}
    content = _as_text(message.get("content"))
    if provider == "deepseek" and not content.strip():
        raise CloudResponseRejectedError(
            "empty_deepseek_response",
            "DeepSeek returned empty content.",
            provider=provider,
            model=model,
            raw_response=raw_excerpt_source,
            finish_reason=_as_text(finish_reason),
            usage=usage,
        )
    return CloudChatResponse(
        provider=provider,
        model=model,
        content=content,
        finish_reason=_as_text(finish_reason),
        usage=usage,
        metadata={"finish_reason": finish_reason},
    )


def call_kimi_chat_completion(
    *,
    config: RunConfig,
    prompt: str,
    schema: dict[str, Any],
    post_json: Callable[..., dict[str, Any]] | None = None,
) -> CloudChatResponse:
    api_key = get_api_key(config.kimi_api_key_env, "kimi")
    post_json = post_json or post_cloud_json
    payload = build_kimi_chat_payload(config=config, prompt=prompt, schema=schema)
    try:
        response = post_json(
            base_url=config.kimi_base_url,
            payload=payload,
            api_key=api_key,
            timeout_seconds=config.cloud_timeout_seconds,
        )
        metadata = {"token_parameter": "max_completion_tokens"}
    except CloudProviderError as exc:
        if exc.reason != "invalid_parameter":
            raise
        retry_payload = build_kimi_chat_payload(config=config, prompt=prompt, schema=schema, use_max_tokens=True)
        response = post_json(
            base_url=config.kimi_base_url,
            payload=retry_payload,
            api_key=api_key,
            timeout_seconds=config.cloud_timeout_seconds,
        )
        metadata = {"token_parameter": "max_tokens"}
    chat = extract_chat_content(response, "kimi", config.kimi_model)
    chat.metadata.update(metadata)
    return chat


def call_deepseek_chat_completion(
    *,
    config: RunConfig,
    prompt: str,
    schema: dict[str, Any],
    model: str,
    post_json: Callable[..., dict[str, Any]] | None = None,
) -> CloudChatResponse:
    api_key = get_api_key(config.deepseek_api_key_env, "deepseek")
    post_json = post_json or post_cloud_json
    payload = build_deepseek_chat_payload(config=config, prompt=prompt, schema=schema, model=model)
    response = post_json(
        base_url=config.deepseek_base_url,
        payload=payload,
        api_key=api_key,
        timeout_seconds=config.cloud_timeout_seconds,
    )
    return extract_chat_content(response, "deepseek", model)


def should_run_deepseek_preflight(config: RunConfig) -> bool:
    if not config.cloud_preflight or not config.allow_cloud_ai:
        return False
    if config.council_mode == "local_only":
        return any(
            provider == "deepseek"
            for provider in (config.judge_provider, config.verifier_provider, config.adjudicator_provider)
        )
    if config.council_mode in DEEPSEEK_ENABLED_MODES:
        return True
    return any(
        provider == "deepseek"
        for provider in (config.judge_provider, config.verifier_provider, config.adjudicator_provider)
    )


def run_deepseek_preflight(config: RunConfig, council: RelationshipCouncil) -> bool:
    schema = {
        "type": "object",
        "properties": {"ok": {"type": "boolean"}},
        "required": ["ok"],
        "additionalProperties": False,
    }
    prompt = 'Return JSON only with this exact shape: {"ok": true}'
    try:
        allowed, reason = council._provider_allowed("deepseek", config.deepseek_flash_model, role="preflight")
        if not allowed:
            council.usage.provider_failover_events.append(
                {
                    "role": "preflight",
                    "provider": "deepseek",
                    "model": config.deepseek_flash_model,
                    "reason": reason,
                    "created_at_utc": utc_now(),
                }
            )
            return False
        response = council._call_cloud("deepseek", config.deepseek_flash_model, prompt, schema, role="preflight")
        data = _parse_json_object(response.content)
        if data.get("ok") is not True:
            raise CloudResponseRejectedError("deepseek_preflight_failed", "DeepSeek preflight did not return ok=true.")
        council.usage.record_cloud_usage("deepseek", config.deepseek_flash_model, response.usage)
        council.health.mark_success("deepseek")
        council.health.mark_success("deepseek_flash")
        return True
    except CloudProviderError as exc:
        status = council._health_status_for_error(exc)
        council.health.mark_failure("deepseek", status, config.cloud_circuit_breaker_failures)
        council.health.mark_failure("deepseek_flash", status, config.cloud_circuit_breaker_failures)
        council.usage.provider_failover_events.append(
            {
                "role": "preflight",
                "provider": "deepseek",
                "model": config.deepseek_flash_model,
                "reason": exc.reason,
                "status_code": exc.status_code,
                "created_at_utc": utc_now(),
            }
        )
        if config.strict_cloud_only:
            raise
        return False
    except (CloudResponseRejectedError, MalformedModelJSONError) as exc:
        council.health.mark_failure("deepseek", "degraded", config.cloud_circuit_breaker_failures)
        council.health.mark_failure("deepseek_flash", "degraded", config.cloud_circuit_breaker_failures)
        council.usage.provider_failover_events.append(
            {
                "role": "preflight",
                "provider": "deepseek",
                "model": config.deepseek_flash_model,
                "reason": getattr(exc, "reason", "deepseek_preflight_failed"),
                "created_at_utc": utc_now(),
            }
        )
        if config.strict_cloud_only:
            raise CloudProviderError("deepseek", "deepseek_preflight_failed", str(exc), retryable=False) from exc
        return False


def normalize_embeddings(embeddings: dict[str, list[float]]) -> dict[str, list[float]]:
    normalized: dict[str, list[float]] = {}
    for node_id, vector in embeddings.items():
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            normalized[node_id] = [0.0 for _ in vector]
        else:
            normalized[node_id] = [value / norm for value in vector]
    return normalized


def generate_candidate_pairs(
    nodes: list[BackboneNodeView],
    embeddings: dict[str, list[float]],
    *,
    run_id: str,
    embedding_model: str,
    candidate_top_k: int,
    min_similarity: float,
    max_pairs: int,
    existing_pair_index: set[str],
    include_existing_pairs: bool,
) -> Any:
    if not nodes:
        return
    normalized = normalize_embeddings(embeddings)
    node_ids = [node.id for node in nodes if node.id in normalized]
    if not node_ids:
        return
    matrix = np.array([normalized[node_id] for node_id in node_ids], dtype=float)
    if matrix.ndim != 2:
        raise ValueError("Embedding matrix must be two-dimensional")

    seen_pairs: set[str] = set()
    emitted = 0
    top_k = max(1, int(candidate_top_k))
    max_pairs = max(0, int(max_pairs))
    for row_index, node_a_id in enumerate(node_ids):
        scores = matrix @ matrix[row_index]
        scores[row_index] = -np.inf
        order = np.lexsort((np.arange(len(scores)), -scores))
        kept = 0
        for candidate_index in order:
            if kept >= top_k or emitted >= max_pairs:
                break
            similarity = float(scores[candidate_index])
            if not math.isfinite(similarity) or similarity < min_similarity:
                continue
            node_b_id = node_ids[int(candidate_index)]
            pair_key = build_pair_key(node_a_id, node_b_id)
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            kept += 1
            if not include_existing_pairs and pair_key in existing_pair_index:
                continue
            emitted += 1
            yield CandidatePair(
                run_id=run_id,
                node_pair_key=pair_key,
                node_a_id=node_a_id,
                node_b_id=node_b_id,
                similarity=similarity,
                embedding_model=embedding_model,
                created_at_utc=utc_now(),
            )
            if emitted >= max_pairs:
                break


def _strip_json_fences(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def _parse_json_object(raw: str) -> dict[str, Any]:
    text = _strip_json_fences(raw)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise MalformedModelJSONError("Model output was not valid JSON") from None
        try:
            data = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise MalformedModelJSONError(str(exc)) from exc
    if not isinstance(data, dict):
        raise MalformedModelJSONError("Model output JSON must be an object")
    predicate = data.get("predicate", data.get("corrected_predicate"))
    if predicate in BLOCKED_PREDICATES:
        raise BlockedPredicateError(f"Blocked predicate emitted: {predicate}")
    return data


def pydantic_errors_to_records(exc: ValidationError) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for error in exc.errors():
        records.append(
            {
                "loc": [str(part) for part in error.get("loc", ())],
                "msg": _as_text(error.get("msg")),
                "type": _as_text(error.get("type")),
            }
        )
    return records


def failed_fields_from_pydantic_errors(errors: list[dict[str, Any]]) -> list[str]:
    fields: list[str] = []
    seen: set[str] = set()
    for error in errors:
        loc = error.get("loc") or []
        if loc:
            field = _as_text(loc[0])
            if field and field not in seen:
                seen.add(field)
                fields.append(field)
    return fields


def normalize_relationship_decision_payload(
    raw: dict[str, Any],
    role: str,
    *,
    accept_threshold: float = 0.85,
    acceptance_policy: str = "needs_review_only",
) -> tuple[dict[str, Any], list[str]]:
    """Apply conservative, deterministic schema-shape repairs before validation."""

    data = dict(raw)
    steps: list[str] = []

    for key, value in list(data.items()):
        if isinstance(value, str):
            trimmed = value.strip()
            if trimmed != value:
                data[key] = trimmed
                steps.append(f"{key}_trimmed")

    predicate = data.get("predicate")
    if isinstance(predicate, str):
        normalized = predicate.strip().lower()
        if normalized != predicate:
            data["predicate"] = normalized
            steps.append("predicate_lowercased")

    direction = data.get("direction")
    if isinstance(direction, str):
        mapping = {
            "a_to_b": "A_to_B",
            "atob": "A_to_B",
            "b_to_a": "B_to_A",
            "btoa": "B_to_A",
            "undirected": "undirected",
            "none": "none",
        }
        cleaned = direction.strip()
        normalized_direction = mapping.get(cleaned.lower())
        if normalized_direction and normalized_direction != direction:
            data["direction"] = normalized_direction
            steps.append("direction_literal_normalized")

    confidence = data.get("confidence")
    if isinstance(confidence, str):
        try:
            data["confidence"] = float(confidence.strip())
            steps.append("confidence_string_to_float")
        except ValueError:
            pass

    relation_nature = data.get("relation_nature")
    if relation_nature is None:
        data["relation_nature"] = []
        steps.append("missing_relation_nature_to_empty_list")
    elif isinstance(relation_nature, str):
        value = relation_nature.strip()
        data["relation_nature"] = [value] if value else []
        steps.append("relation_nature_string_to_list")

    risk_flags = data.get("risk_flags")
    if risk_flags is None:
        data["risk_flags"] = []
        steps.append("missing_risk_flags_to_empty_list")
    elif isinstance(risk_flags, str):
        value = risk_flags.strip()
        data["risk_flags"] = [value] if value else []
        steps.append("risk_flags_string_to_list")

    predicate_text = _as_text(data.get("predicate"))
    edge_exists = bool(data.get("edge_exists"))
    if not data.get("relation_type"):
        if not edge_exists:
            data["relation_type"] = "none"
        elif predicate_text in {"broader_than", "narrower_than", "part_of"}:
            data["relation_type"] = "taxonomy_hierarchy"
        else:
            data["relation_type"] = predicate_text or "candidate_relationship"
        steps.append("missing_relation_type_filled")

    if not data.get("relation_category"):
        if not edge_exists:
            data["relation_category"] = "none"
        elif predicate_text in {"broader_than", "narrower_than", "part_of"}:
            data["relation_category"] = "taxonomy"
        else:
            data["relation_category"] = "other"
        steps.append("missing_relation_category_filled")

    if not data.get("review_recommendation"):
        if not edge_exists:
            data["review_recommendation"] = "reject"
        elif isinstance(data.get("confidence"), (int, float)) and float(data.get("confidence")) >= accept_threshold:
            data["review_recommendation"] = "needs_review"
        else:
            data["review_recommendation"] = "needs_review"
        steps.append("missing_review_recommendation_filled")

    if steps and acceptance_policy == "needs_review_only" and data.get("edge_exists") is True:
        if data.get("review_recommendation") == "accept_candidate":
            data["review_recommendation"] = "needs_review"
            steps.append("schema_repair_forced_needs_review")

    return data, steps


def parse_relationship_decision(
    raw: str,
    *,
    role: str = "judge",
    config: RunConfig | None = None,
) -> RelationshipDecision:
    data = _parse_json_object(raw)
    repair_attempted = False
    repair_steps: list[str] = []
    if config is None or config.enable_safe_schema_repair:
        repair_attempted = True
        data, repair_steps = normalize_relationship_decision_payload(
            data,
            role,
            accept_threshold=config.accept_threshold if config else 0.85,
            acceptance_policy=config.schema_repair_acceptance_policy if config else "needs_review_only",
        )
        if data.get("predicate") in BLOCKED_PREDICATES:
            raise BlockedPredicateError(f"Blocked predicate emitted: {data.get('predicate')}")
    try:
        decision = RelationshipDecision.model_validate(data)
    except ValidationError as exc:
        error_records = pydantic_errors_to_records(exc)
        error = UnsafeDecisionError(str(exc))
        error.pydantic_errors = error_records  # type: ignore[attr-defined]
        error.failed_fields = failed_fields_from_pydantic_errors(error_records)  # type: ignore[attr-defined]
        error.repair_attempted = repair_attempted  # type: ignore[attr-defined]
        error.repair_successful = False  # type: ignore[attr-defined]
        error.normalization_steps = repair_steps  # type: ignore[attr-defined]
        raise error from exc
    return decision


def parse_verification_decision(raw: str) -> VerificationDecision:
    data = _parse_json_object(raw)
    try:
        return VerificationDecision.model_validate(data)
    except ValidationError as exc:
        error_records = pydantic_errors_to_records(exc)
        error = UnsafeDecisionError(str(exc))
        error.pydantic_errors = error_records  # type: ignore[attr-defined]
        error.failed_fields = failed_fields_from_pydantic_errors(error_records)  # type: ignore[attr-defined]
        raise error from exc


def parse_relationship_decision_for_role(raw: str, role: str, *, config: RunConfig | None = None) -> RelationshipDecision:
    try:
        return parse_relationship_decision(raw, role=role, config=config)
    except UnsafeDecisionError as exc:
        raise RoleValidationError(
            f"{role}_validation_error",
            str(exc),
            role=role,
            raw_response=raw,
            error_type="pydantic_validation_error",
            pydantic_errors=getattr(exc, "pydantic_errors", []),
            failed_fields=getattr(exc, "failed_fields", []),
            repair_attempted=bool(getattr(exc, "repair_attempted", False)),
            repair_successful=False,
            normalization_steps=list(getattr(exc, "normalization_steps", [])),
        ) from exc


def parse_verification_decision_for_role(raw: str, role: str = "verifier") -> VerificationDecision:
    try:
        return parse_verification_decision(raw)
    except UnsafeDecisionError as exc:
        raise RoleValidationError(
            f"{role}_validation_error",
            str(exc),
            role=role,
            raw_response=raw,
            error_type="pydantic_validation_error",
            pydantic_errors=getattr(exc, "pydantic_errors", []),
            failed_fields=getattr(exc, "failed_fields", []),
        ) from exc


def validate_relationship_decision(decision: RelationshipDecision) -> None:
    if decision.predicate in BLOCKED_PREDICATES:
        raise BlockedPredicateError(f"Blocked predicate emitted: {decision.predicate}")
    if decision.edge_exists and decision.predicate not in ALLOWED_PREDICATES:
        raise UnsafeDecisionError(f"Predicate is not allowed: {decision.predicate}")
    if decision.direction == "undirected" and decision.predicate != "conflicts_with":
        raise UnsafeDecisionError("undirected is only allowed for conflicts_with")


def build_judge_prompt(
    *,
    node_a: BackboneNodeView,
    node_b: BackboneNodeView,
    existing_direct_relationships: list[dict[str, Any]],
    similarity: float,
    schema: dict[str, Any],
) -> str:
    existing = existing_direct_relationships if existing_direct_relationships else "none"
    return (
        "You are reviewing candidate relationships in the Vitruvius AEC-MEPFS Backbone graph.\n\n"
        "Decide whether a governed relationship should be proposed between Node A and Node B.\n\n"
        "You must be conservative.\n\n"
        "Only propose an edge if the relationship is clear from the node labels, definitions, "
        "aliases, taxonomy path, level, parent path, discipline, lifecycle phase, or source-family metadata.\n\n"
        "Do not infer speculative, vague, or merely associative relationships.\n\n"
        "Do not use part_of for simple taxonomy path hierarchy; use broader_than or narrower_than for path-code hierarchy.\n\n"
        "Allowed predicates:\n"
        + "\n".join(f"- {predicate}" for predicate in ALLOWED_PREDICATES)
        + "\n\nBlocked predicates:\n"
        + "\n".join(f"- {predicate}" for predicate in sorted(BLOCKED_PREDICATES))
        + "\n\nDirection rules:\n"
        "- A_to_B means from_id = Node A and to_id = Node B.\n"
        "- B_to_A means from_id = Node B and to_id = Node A.\n"
        "- undirected is only allowed when the predicate is conflicts_with.\n"
        "- none means no edge should be proposed.\n\n"
        "Predicate guidance:\n"
        "- broader_than / narrower_than: taxonomy hierarchy only when one concept is clearly broader/narrower.\n"
        "- part_of: compositional containment, not loose association and not taxonomy placement.\n"
        "- requires: one concept depends on the other as a requirement.\n"
        "- constrains: one concept limits or imposes conditions on the other.\n"
        "- governs: a rule, code, policy, or standard governs another concept.\n"
        "- applicable_in_jurisdiction: jurisdiction-specific applicability.\n"
        "- evidenced_by: one item is evidence/source support for the other.\n"
        "- has_facet: one node expresses a facet/aspect of the other.\n"
        "- maps_to_external_standard: explicit standard mapping.\n"
        "- conflicts_with: actual contradiction or incompatibility.\n"
        "- supersedes: replacement/version precedence.\n\n"
        "Return JSON matching the schema exactly.\n\n"
        "If no edge should be proposed:\n"
        '- edge_exists = false\n- predicate = "none"\n- direction = "none"\n'
        "- confidence <= 0.49\n- rationale explains why not\n\n"
        f"Node A:\n{json.dumps(node_a.compact_json(), ensure_ascii=False, sort_keys=True)}\n\n"
        f"Node B:\n{json.dumps(node_b.compact_json(), ensure_ascii=False, sort_keys=True)}\n\n"
        f"Existing direct relationships between these nodes:\n{json.dumps(existing, ensure_ascii=False, sort_keys=True)}\n\n"
        f"Similarity score:\n{similarity:.6f}\n\n"
        f"JSON schema:\n{json.dumps(schema, ensure_ascii=False, sort_keys=True)}"
    )


def build_verifier_prompt(
    *,
    node_a: BackboneNodeView,
    node_b: BackboneNodeView,
    judge_decision: RelationshipDecision,
    schema: dict[str, Any],
) -> str:
    return (
        "You are verifying an uncertain Vitruvius AEC-MEPFS Backbone relationship decision.\n"
        "Return a VerificationDecision JSON object only, not a full RelationshipDecision.\n"
        "Be conservative. Correct the decision only when the node records support the correction.\n\n"
        "Allowed predicates:\n"
        + "\n".join(f"- {predicate}" for predicate in ALLOWED_PREDICATES)
        + "\n\nNode A:\n"
        + json.dumps(node_a.compact_json(), ensure_ascii=False, sort_keys=True)
        + "\n\nNode B:\n"
        + json.dumps(node_b.compact_json(), ensure_ascii=False, sort_keys=True)
        + "\n\nJudge decision:\n"
        + json.dumps(judge_decision.model_dump(), ensure_ascii=False, sort_keys=True)
        + "\n\nReturn JSON matching this schema exactly:\n"
        + json.dumps(schema, ensure_ascii=False, sort_keys=True)
    )


def build_adjudicator_prompt(
    *,
    node_a: BackboneNodeView,
    node_b: BackboneNodeView,
    judge_decision: RelationshipDecision,
    verifier_decision: VerificationDecision | None,
    schema: dict[str, Any],
) -> str:
    return (
        "You are adjudicating a Vitruvius AEC-MEPFS Backbone relationship decision.\n"
        "Return a full RelationshipDecision JSON object, not a verifier agrees/corrected object.\n"
        "Be conservative. Do not invent facts beyond the provided node records. "
        "Use part_of only for compositional containment, not taxonomy path hierarchy.\n\n"
        "Node A:\n"
        + json.dumps(node_a.compact_json(), ensure_ascii=False, sort_keys=True)
        + "\n\nNode B:\n"
        + json.dumps(node_b.compact_json(), ensure_ascii=False, sort_keys=True)
        + "\n\nJudge decision:\n"
        + json.dumps(judge_decision.model_dump(), ensure_ascii=False, sort_keys=True)
        + "\n\nVerifier decision:\n"
        + json.dumps(verifier_decision.model_dump() if verifier_decision else None, ensure_ascii=False, sort_keys=True)
        + "\n\nReturn a full RelationshipDecision JSON object matching this schema exactly:\n"
        + json.dumps(schema, ensure_ascii=False, sort_keys=True)
    )


def _union_tuple_values(*values: tuple[str, ...]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for group in values:
        for value in group:
            if value and value not in seen:
                seen.add(value)
                result.append(value)
    return result


def endpoint_ids_for_direction(node_a: BackboneNodeView, node_b: BackboneNodeView, direction: str) -> tuple[str, str] | None:
    if direction == "A_to_B":
        return node_a.id, node_b.id
    if direction == "B_to_A":
        return node_b.id, node_a.id
    if direction == "undirected":
        return node_a.id, node_b.id
    return None


def decision_to_edge_record(
    *,
    run_id: str,
    node_a: BackboneNodeView,
    node_b: BackboneNodeView,
    pair: CandidatePair,
    decision: RelationshipDecision,
    embedding_model: str,
    judge_model: str,
    verifier_model: str | None,
    verifier_decision: VerificationDecision | None,
    created_at_utc: str,
    council_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    endpoints = endpoint_ids_for_direction(node_a, node_b, decision.direction)
    if endpoints is None or (decision.direction == "undirected" and decision.predicate != "conflicts_with"):
        raise UnsafeDecisionError("Cannot build accepted edge record for direction none")
    from_id, to_id = endpoints

    confidence = float(decision.confidence)
    metadata = council_metadata or {}
    edge_key = build_edge_key(from_id, decision.predicate, to_id)
    original_model_edge_key = None
    if metadata.get("normalization_applied"):
        original_predicate = _as_text(metadata.get("original_model_predicate"))
        original_direction = _as_text(metadata.get("original_model_direction"))
        original_endpoints = endpoint_ids_for_direction(node_a, node_b, original_direction)
        if original_predicate and original_endpoints is not None:
            original_model_edge_key = build_edge_key(original_endpoints[0], original_predicate, original_endpoints[1])
    return {
        "schema_version": "aec-relationship-improvement-candidate/v1",
        "run_id": run_id,
        "node_pair_key": pair.node_pair_key,
        "edge_key": edge_key,
        "final_edge_key": edge_key,
        "original_model_edge_key": original_model_edge_key,
        "from_id": from_id,
        "to_id": to_id,
        "predicate": decision.predicate,
        "governed": True,
        "direction": "from_to",
        "relation_type": decision.relation_type,
        "relation_category": decision.relation_category,
        "relation_nature": decision.relation_nature,
        "weight": confidence,
        "confidence_score": confidence,
        "discipline": _union_tuple_values(node_a.discipline, node_b.discipline),
        "lifecycle_phase": _union_tuple_values(node_a.lifecycle_phase, node_b.lifecycle_phase),
        "source_family_ids": _union_tuple_values(node_a.source_family_ids, node_b.source_family_ids),
        "rationale": decision.rationale,
        "provenance_note": PROVENANCE_NOTE,
        "generation_method": metadata.get(
            "generation_method",
            generation_method_for_council_mode(metadata.get("council_mode", "local_only")),
        ),
        "review_status": "candidate",
        "semantic_overlay_category": "relationship_improvement_candidate",
        "applicability_basis": None,
        "jurisdiction_context": None,
        "design_basis_status": "candidate",
        "embedding_model": embedding_model,
        "judge_model": metadata.get("judge_model", judge_model),
        "verifier_model": metadata.get("verifier_model", verifier_model),
        "raw_similarity": pair.similarity,
        "created_at_utc": created_at_utc,
        "node_a_id": node_a.id,
        "node_b_id": node_b.id,
        "judge_decision": decision.model_dump(),
        "verifier_decision": verifier_decision.model_dump() if verifier_decision else None,
        "council_mode": metadata.get("council_mode", "local_only"),
        "judge_provider": metadata.get("judge_provider", "ollama"),
        "effective_judge_provider": metadata.get("effective_judge_provider"),
        "effective_judge_model": metadata.get("effective_judge_model"),
        "primary_judge_provider": metadata.get("primary_judge_provider"),
        "primary_judge_model": metadata.get("primary_judge_model"),
        "fallback_judge_provider": metadata.get("fallback_judge_provider"),
        "fallback_judge_model": metadata.get("fallback_judge_model"),
        "local_judge_model": metadata.get("local_judge_model"),
        "local_verifier_model": metadata.get("local_verifier_model"),
        "verifier_provider": metadata.get("verifier_provider"),
        "effective_verifier_provider": metadata.get("effective_verifier_provider"),
        "effective_verifier_model": metadata.get("effective_verifier_model"),
        "adjudicator_provider": metadata.get("adjudicator_provider"),
        "adjudicator_model": metadata.get("adjudicator_model"),
        "effective_adjudicator_provider": metadata.get("effective_adjudicator_provider"),
        "effective_adjudicator_model": metadata.get("effective_adjudicator_model"),
        "provider_route": metadata.get("provider_route", []),
        "cloud_usage": sanitize_for_artifact(metadata.get("cloud_usage", {})),
        "cloud_usage_for_decision": sanitize_for_artifact(metadata.get("cloud_usage_for_decision", metadata.get("cloud_usage", {}))),
        "local_fallback_used": bool(metadata.get("local_fallback_used", False)),
        "provider_failover_reason": metadata.get("provider_failover_reason"),
        "normalization_applied": bool(metadata.get("normalization_applied", False)),
        "normalization_reason": metadata.get("normalization_reason"),
        "normalization_steps": metadata.get("normalization_steps", []),
        "original_model_predicate": metadata.get("original_model_predicate"),
        "original_model_direction": metadata.get("original_model_direction"),
        "normalized_predicate": metadata.get("normalized_predicate"),
        "normalized_direction": metadata.get("normalized_direction"),
        "hierarchy_relation_detected": bool(metadata.get("hierarchy_relation_detected", False)),
        "hierarchy_parent_id": metadata.get("hierarchy_parent_id"),
        "hierarchy_child_id": metadata.get("hierarchy_child_id"),
        "final_guard_passed": bool(metadata.get("final_guard_passed", True)),
        "final_guard_checks": metadata.get("final_guard_checks", {}),
    }


def build_rejected_record(
    *,
    run_id: str,
    pair: CandidatePair,
    reason: str,
    judge_decision: RelationshipDecision | None,
    error: str | None,
    verifier_decision: VerificationDecision | None = None,
    council_metadata: dict[str, Any] | None = None,
    validation_error_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metadata = council_metadata or {}
    validation_record = validation_error_record or {}
    return {
        "schema_version": "aec-relationship-improvement-rejection/v1",
        "run_id": run_id,
        "node_pair_key": pair.node_pair_key,
        "node_a_id": pair.node_a_id,
        "node_b_id": pair.node_b_id,
        "similarity": pair.similarity,
        "reason": reason,
        "role": validation_record.get("role") or metadata.get("failed_role"),
        "provider": validation_record.get("provider") or metadata.get("judge_provider"),
        "model": validation_record.get("model") or metadata.get("judge_model"),
        "judge_decision": judge_decision.model_dump() if judge_decision else None,
        "verifier_decision": verifier_decision.model_dump() if verifier_decision else None,
        "error": truncate_error_text(error or "") if error else None,
        "validation_error_detail": validation_record.get("reason"),
        "failed_fields": validation_record.get("failed_fields", []),
        "raw_response_sha256": validation_record.get("raw_response_sha256"),
        "validation_error_record_id": validation_record.get("record_id"),
        "council_mode": metadata.get("council_mode", "local_only"),
        "judge_provider": metadata.get("judge_provider", "ollama"),
        "judge_model": metadata.get("judge_model"),
        "effective_judge_provider": metadata.get("effective_judge_provider"),
        "effective_judge_model": metadata.get("effective_judge_model"),
        "primary_judge_provider": metadata.get("primary_judge_provider"),
        "primary_judge_model": metadata.get("primary_judge_model"),
        "fallback_judge_provider": metadata.get("fallback_judge_provider"),
        "fallback_judge_model": metadata.get("fallback_judge_model"),
        "local_judge_model": metadata.get("local_judge_model"),
        "local_verifier_model": metadata.get("local_verifier_model"),
        "verifier_provider": metadata.get("verifier_provider"),
        "verifier_model": metadata.get("verifier_model"),
        "effective_verifier_provider": metadata.get("effective_verifier_provider"),
        "effective_verifier_model": metadata.get("effective_verifier_model"),
        "adjudicator_provider": metadata.get("adjudicator_provider"),
        "adjudicator_model": metadata.get("adjudicator_model"),
        "effective_adjudicator_provider": metadata.get("effective_adjudicator_provider"),
        "effective_adjudicator_model": metadata.get("effective_adjudicator_model"),
        "provider_route": metadata.get("provider_route", []),
        "cloud_usage": sanitize_for_artifact(metadata.get("cloud_usage", {})),
        "local_fallback_used": bool(metadata.get("local_fallback_used", False)),
        "provider_failover_reason": metadata.get("provider_failover_reason"),
        "normalization_applied": bool(metadata.get("normalization_applied", False)),
        "normalization_reason": metadata.get("normalization_reason"),
        "normalization_steps": metadata.get("normalization_steps", []),
        "created_at_utc": utc_now(),
    }


def build_needs_review_record(
    *,
    run_id: str,
    pair: CandidatePair,
    judge_decision: RelationshipDecision,
    verifier_decision: VerificationDecision | None,
    reason: str,
    council_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metadata = council_metadata or {}
    return {
        "schema_version": "aec-relationship-improvement-needs-review/v1",
        "run_id": run_id,
        "node_pair_key": pair.node_pair_key,
        "node_a_id": pair.node_a_id,
        "node_b_id": pair.node_b_id,
        "similarity": pair.similarity,
        "reason": reason,
        "review_reason": reason,
        "judge_decision": judge_decision.model_dump(),
        "verifier_decision": verifier_decision.model_dump() if verifier_decision else None,
        "council_mode": metadata.get("council_mode", "local_only"),
        "judge_provider": metadata.get("judge_provider", "ollama"),
        "judge_model": metadata.get("judge_model"),
        "effective_judge_provider": metadata.get("effective_judge_provider"),
        "effective_judge_model": metadata.get("effective_judge_model"),
        "primary_judge_provider": metadata.get("primary_judge_provider"),
        "primary_judge_model": metadata.get("primary_judge_model"),
        "fallback_judge_provider": metadata.get("fallback_judge_provider"),
        "fallback_judge_model": metadata.get("fallback_judge_model"),
        "local_judge_model": metadata.get("local_judge_model"),
        "local_verifier_model": metadata.get("local_verifier_model"),
        "verifier_provider": metadata.get("verifier_provider"),
        "verifier_model": metadata.get("verifier_model"),
        "effective_verifier_provider": metadata.get("effective_verifier_provider"),
        "effective_verifier_model": metadata.get("effective_verifier_model"),
        "adjudicator_provider": metadata.get("adjudicator_provider"),
        "adjudicator_model": metadata.get("adjudicator_model"),
        "effective_adjudicator_provider": metadata.get("effective_adjudicator_provider"),
        "effective_adjudicator_model": metadata.get("effective_adjudicator_model"),
        "provider_route": metadata.get("provider_route", []),
        "cloud_usage": sanitize_for_artifact(metadata.get("cloud_usage", {})),
        "local_fallback_used": bool(metadata.get("local_fallback_used", False)),
        "provider_failover_reason": metadata.get("provider_failover_reason"),
        "normalization_applied": bool(metadata.get("normalization_applied", False)),
        "normalization_reason": metadata.get("normalization_reason"),
        "normalization_steps": metadata.get("normalization_steps", []),
        "created_at_utc": utc_now(),
    }


def load_checkpoint(path: Path) -> Checkpoint | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return Checkpoint(
        run_id=_as_text(data.get("run_id")),
        status=_as_text(data.get("status")) or "in_progress",
        input_path=_as_text(data.get("input_path")),
        output_dir=_as_text(data.get("output_dir")),
        embedding_model=_as_text(data.get("embedding_model")),
        judge_model=_as_text(data.get("judge_model")),
        verifier_model=data.get("verifier_model"),
        council_mode=_as_text(data.get("council_mode")) or "local_only",
        local_judge_model=_as_text(data.get("local_judge_model")) or _as_text(data.get("judge_model")) or DEFAULT_JUDGE_MODEL,
        local_verifier_model=_as_text(data.get("local_verifier_model")) or _as_text(data.get("verifier_model")) or DEFAULT_VERIFIER_MODEL,
        primary_judge_provider=data.get("primary_judge_provider"),
        primary_judge_model=data.get("primary_judge_model"),
        fallback_judge_provider=data.get("fallback_judge_provider"),
        fallback_judge_model=data.get("fallback_judge_model"),
        primary_verifier_provider=data.get("primary_verifier_provider"),
        primary_verifier_model=data.get("primary_verifier_model"),
        fallback_verifier_provider=data.get("fallback_verifier_provider"),
        fallback_verifier_model=data.get("fallback_verifier_model"),
        primary_adjudicator_provider=data.get("primary_adjudicator_provider"),
        primary_adjudicator_model=data.get("primary_adjudicator_model"),
        fallback_adjudicator_provider=data.get("fallback_adjudicator_provider"),
        fallback_adjudicator_model=data.get("fallback_adjudicator_model"),
        effective_judge_provider=data.get("effective_judge_provider"),
        effective_judge_model=data.get("effective_judge_model"),
        effective_verifier_provider=data.get("effective_verifier_provider"),
        effective_verifier_model=data.get("effective_verifier_model"),
        effective_adjudicator_provider=data.get("effective_adjudicator_provider"),
        effective_adjudicator_model=data.get("effective_adjudicator_model"),
        processed_pair_keys=list(data.get("processed_pair_keys") or []),
        accepted_edge_keys=list(data.get("accepted_edge_keys") or []),
        rejected_pair_count=int(data.get("rejected_pair_count") or 0),
        error_count=int(data.get("error_count") or 0),
        cloud_usage=CloudUsage.from_record(data.get("cloud_usage")),
        provider_health=ProviderHealth.from_record(data.get("provider_health")),
        last_provider_used=data.get("last_provider_used"),
        deepseek_flash_max_calls=data.get("deepseek_flash_max_calls"),
        deepseek_pro_max_calls=data.get("deepseek_pro_max_calls"),
        hierarchy_normalization_count=int(data.get("hierarchy_normalization_count") or 0),
        taxonomy_part_of_conversion_count=int(data.get("taxonomy_part_of_conversion_count") or 0),
        validation_guard_downgrade_count=int(data.get("validation_guard_downgrade_count") or 0),
        phase=_as_text(data.get("phase")) or "loading",
        started_at_utc=_as_text(data.get("started_at_utc")) or utc_now(),
        elapsed_seconds=float(data.get("elapsed_seconds") or 0.0),
        nodes_loaded=int(data.get("nodes_loaded") or 0),
        nodes_selected=int(data.get("nodes_selected") or 0),
        embedding_total=int(data.get("embedding_total") or 0),
        embedding_processed=int(data.get("embedding_processed") or 0),
        embedding_cache_hits=int(data.get("embedding_cache_hits") or 0),
        embedding_cache_misses=int(data.get("embedding_cache_misses") or 0),
        embedding_dimensions=data.get("embedding_dimensions"),
        candidate_pairs_generated=int(data.get("candidate_pairs_generated") or 0),
        candidate_pairs_total_estimate=data.get("candidate_pairs_total_estimate"),
        max_pairs=int(data.get("max_pairs") or 0),
        processed_pair_count=int(data.get("processed_pair_count", len(data.get("processed_pair_keys") or [])) or 0),
        accepted_count=int(data.get("accepted_count", len(data.get("accepted_edge_keys") or [])) or 0),
        candidate_count=int(data.get("candidate_count") or 0),
        rejected_count=int(data.get("rejected_count", data.get("rejected_pair_count") or 0) or 0),
        current_pair_key=data.get("current_pair_key"),
        current_provider=data.get("current_provider"),
        current_model=data.get("current_model"),
        current_operation=data.get("current_operation"),
        avg_embedding_seconds=data.get("avg_embedding_seconds"),
        avg_judge_seconds=data.get("avg_judge_seconds"),
        avg_verifier_seconds=data.get("avg_verifier_seconds"),
        avg_adjudicator_seconds=data.get("avg_adjudicator_seconds"),
        pairs_per_minute=data.get("pairs_per_minute"),
        estimated_seconds_remaining=data.get("estimated_seconds_remaining"),
        recent_events=list(data.get("recent_events") or [])[-MAX_RECENT_EVENTS:],
        validation_error_count=int(data.get("validation_error_count") or 0),
        validation_errors_by_role=dict(data.get("validation_errors_by_role") or {}),
        validation_errors_by_provider=dict(data.get("validation_errors_by_provider") or {}),
        validation_errors_by_field=dict(data.get("validation_errors_by_field") or {}),
        progress_mode_effective=data.get("progress_mode_effective"),
        last_updated_at_utc=_as_text(data.get("last_updated_at_utc")) or utc_now(),
    )


def save_checkpoint(path: Path, checkpoint: Checkpoint) -> None:
    elapsed = seconds_since_utc(checkpoint.started_at_utc)
    if elapsed is not None:
        checkpoint.elapsed_seconds = round(elapsed, 3)
    checkpoint.last_updated_at_utc = utc_now()
    write_json(path, checkpoint.to_record())


def setup_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "relationship-improvement.log"
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def find_latest_in_progress_run(output_root: Path) -> str | None:
    if not output_root.exists():
        return None
    candidates = sorted((path for path in output_root.iterdir() if path.is_dir()), reverse=True)
    for candidate in candidates:
        checkpoint = load_checkpoint(candidate / "relationship-improvement-checkpoint.json")
        if checkpoint and checkpoint.status == "in_progress":
            return candidate.name
    return None


def _touch_output_files(output_dir: Path) -> dict[str, Path]:
    files = {
        "log": output_dir / "relationship-improvement.log",
        "report": output_dir / "relationship-improvement-report.json",
        "checkpoint": output_dir / "relationship-improvement-checkpoint.json",
        "candidate": output_dir / "candidate-relationships.jsonl",
        "accepted": output_dir / "accepted-relationships.jsonl",
        "rejected": output_dir / "rejected-relationships.jsonl",
        "errors": output_dir / "errors.jsonl",
        "validation_errors": output_dir / "validation-errors.jsonl",
        "run_embeddings": output_dir / "node-embeddings.jsonl",
        "similarity": output_dir / "similarity-candidates.jsonl",
        "audit": output_dir / "relationship-council-audit.jsonl",
        "events": output_dir / "relationship-improvement-events.jsonl",
        "summary_txt": output_dir / "relationship-improvement-summary.txt",
        "accepted_review_tsv": output_dir / "accepted-relationships-review.tsv",
        "rejected_review_tsv": output_dir / "rejected-relationships-review.tsv",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, path in files.items():
        if key != "checkpoint" and not path.exists():
            path.touch()
    return files


def _direct_relationships_between(
    relationships: list[dict[str, Any]],
    node_a_id: str,
    node_b_id: str,
) -> list[dict[str, Any]]:
    direct: list[dict[str, Any]] = []
    for relationship in relationships:
        from_id = _as_text(relationship.get("from_id"))
        to_id = _as_text(relationship.get("to_id"))
        if (from_id == node_a_id and to_id == node_b_id) or (from_id == node_b_id and to_id == node_a_id):
            direct.append(relationship)
    return direct


def _rejection(summary: RunSummary, reason: str) -> None:
    summary.rejected_count += 1
    summary.rejection_counts[reason] = summary.rejection_counts.get(reason, 0) + 1


def raw_response_sha256(raw: str | None) -> str:
    return sha256_text(raw or "")


def sanitize_raw_excerpt(raw: str | None, limit: int = MAX_RAW_RESPONSE_EXCERPT_CHARS) -> str:
    return truncate_error_text(redact_secret_text(_as_text(raw)), limit)


def build_validation_error_record(
    *,
    run_id: str,
    pair: CandidatePair,
    role: str,
    provider: str | None,
    model: str | None,
    error_type: str,
    reason: str,
    pydantic_errors: list[dict[str, Any]] | None = None,
    raw_response: str | None = None,
    finish_reason: str | None = None,
    usage: dict[str, Any] | None = None,
    prompt: str | None = None,
    repair_attempted: bool = False,
    repair_successful: bool = False,
    final_action: str = "rejected",
) -> dict[str, Any]:
    failed_fields = failed_fields_from_pydantic_errors(pydantic_errors or [])
    record = {
        "schema_version": "aec-relationship-validation-error/v1",
        "run_id": run_id,
        "record_id": f"{run_id}:{pair.node_pair_key}:{role}:{raw_response_sha256(raw_response)[:12]}",
        "created_at_utc": utc_now(),
        "pair_key": pair.node_pair_key,
        "node_a_id": pair.node_a_id,
        "node_b_id": pair.node_b_id,
        "role": role,
        "provider": provider,
        "model": model,
        "error_type": error_type,
        "reason": reason,
        "pydantic_errors": pydantic_errors or [],
        "failed_fields": failed_fields,
        "raw_response_excerpt": sanitize_raw_excerpt(raw_response),
        "raw_response_sha256": raw_response_sha256(raw_response),
        "finish_reason": finish_reason,
        "usage": sanitize_for_artifact(usage or {}),
        "prompt_hash": sha256_text(prompt or ""),
        "repair_attempted": repair_attempted,
        "repair_successful": repair_successful,
        "final_action": final_action,
    }
    return sanitize_for_artifact(record)


def record_validation_error(
    *,
    files: dict[str, Path],
    summary: RunSummary,
    checkpoint: Checkpoint,
    record: dict[str, Any],
) -> dict[str, Any]:
    append_jsonl(files["validation_errors"], record)
    summary.validation_error_count += 1
    role = _as_text(record.get("role")) or "unknown"
    provider = _as_text(record.get("provider")) or "unknown"
    summary.validation_errors_by_role[role] = summary.validation_errors_by_role.get(role, 0) + 1
    summary.validation_errors_by_provider[provider] = summary.validation_errors_by_provider.get(provider, 0) + 1
    for field in record.get("failed_fields") or []:
        field_text = _as_text(field) or "unknown"
        summary.validation_errors_by_field[field_text] = summary.validation_errors_by_field.get(field_text, 0) + 1
    checkpoint.validation_error_count = summary.validation_error_count
    checkpoint.validation_errors_by_role = dict(summary.validation_errors_by_role)
    checkpoint.validation_errors_by_provider = dict(summary.validation_errors_by_provider)
    checkpoint.validation_errors_by_field = dict(summary.validation_errors_by_field)
    return record


def record_council_response_rejections(
    *,
    files: dict[str, Path],
    summary: RunSummary,
    checkpoint: Checkpoint,
    council: "RelationshipCouncil",
    run_id: str,
    pair: CandidatePair,
) -> None:
    response_rejections = getattr(council, "response_rejections", [])
    while response_rejections:
        diagnostic = council.response_rejections.pop(0)
        record = {
            "schema_version": "aec-relationship-validation-error/v1",
            "run_id": run_id,
            "record_id": f"{run_id}:{pair.node_pair_key}:{diagnostic.get('role')}:{diagnostic.get('raw_response_sha256', '')[:12]}",
            "pair_key": pair.node_pair_key,
            "node_a_id": pair.node_a_id,
            "node_b_id": pair.node_b_id,
            "pydantic_errors": [],
            "failed_fields": [],
            **diagnostic,
        }
        record_validation_error(files=files, summary=summary, checkpoint=checkpoint, record=sanitize_for_artifact(record))


def envelope_for_role(
    role: str,
    judge: ProviderEnvelope | None,
    verifier: ProviderEnvelope | None,
    adjudicator: ProviderEnvelope | None,
) -> ProviderEnvelope | None:
    if role == "verifier":
        return verifier
    if role == "adjudicator":
        return adjudicator
    return judge


def role_from_operation(operation: str | None) -> str:
    if operation == "verifying":
        return "verifier"
    if operation == "adjudicating":
        return "adjudicator"
    return "judge"


def validation_error_record_from_exception(
    *,
    run_id: str,
    pair: CandidatePair,
    exc: Exception,
    role: str,
    envelope: ProviderEnvelope | None,
    prompt: str | None,
) -> dict[str, Any]:
    if isinstance(exc, RoleValidationError):
        raw = exc.raw_response or (envelope.raw_text if envelope else "")
        return build_validation_error_record(
            run_id=run_id,
            pair=pair,
            role=exc.role or role,
            provider=envelope.provider if envelope else None,
            model=envelope.model if envelope else None,
            error_type=exc.error_type,
            reason=exc.reason,
            pydantic_errors=exc.pydantic_errors,
            raw_response=raw,
            finish_reason=envelope.finish_reason if envelope else None,
            usage=(envelope.metadata or {}).get("usage") if envelope else None,
            prompt=prompt,
            repair_attempted=exc.repair_attempted,
            repair_successful=exc.repair_successful,
            final_action="rejected",
        )
    if isinstance(exc, CloudResponseRejectedError):
        if exc.reason == "deepseek_json_truncated":
            error_type = "finish_reason_length"
        elif exc.reason.startswith("empty_"):
            error_type = "empty_content"
        else:
            error_type = "semantic_validation_error"
        return build_validation_error_record(
            run_id=run_id,
            pair=pair,
            role=role,
            provider=exc.provider or (envelope.provider if envelope else None),
            model=exc.model or (envelope.model if envelope else None),
            error_type=error_type,
            reason=exc.reason,
            pydantic_errors=[],
            raw_response=exc.raw_response or (envelope.raw_text if envelope else ""),
            finish_reason=exc.finish_reason or (envelope.finish_reason if envelope else None),
            usage=exc.usage,
            prompt=prompt,
            final_action="rejected",
        )
    raw = envelope.raw_text if envelope else ""
    return build_validation_error_record(
        run_id=run_id,
        pair=pair,
        role=role,
        provider=envelope.provider if envelope else None,
        model=envelope.model if envelope else None,
        error_type="json_parse_error" if isinstance(exc, MalformedModelJSONError) else "semantic_validation_error",
        reason="malformed_json" if isinstance(exc, MalformedModelJSONError) else "validation_error",
        pydantic_errors=[],
        raw_response=raw,
        finish_reason=envelope.finish_reason if envelope else None,
        prompt=prompt,
        final_action="rejected",
    )


def build_council_metadata(
    *,
    config: RunConfig,
    usage: CloudUsage,
    judge: ProviderEnvelope | None,
    verifier: ProviderEnvelope | None = None,
    adjudicator: ProviderEnvelope | None = None,
) -> dict[str, Any]:
    route: list[dict[str, Any]] = []
    for envelope in (judge, verifier, adjudicator):
        if envelope:
            route.extend(envelope.to_metadata()["provider_route"])
    model_metadata = role_model_metadata(config)
    if judge:
        model_metadata["effective_judge_provider"] = judge.provider
        model_metadata["effective_judge_model"] = judge.model
    if verifier:
        model_metadata["effective_verifier_provider"] = verifier.provider
        model_metadata["effective_verifier_model"] = verifier.model
    if adjudicator:
        model_metadata["effective_adjudicator_provider"] = adjudicator.provider
        model_metadata["effective_adjudicator_model"] = adjudicator.model
    return {
        "council_mode": config.council_mode,
        "generation_method": generation_method_for_council_mode(config.council_mode),
        "judge_provider": judge.provider if judge else None,
        "judge_model": judge.model if judge else None,
        "verifier_provider": verifier.provider if verifier else None,
        "verifier_model": verifier.model if verifier else None,
        "adjudicator_provider": adjudicator.provider if adjudicator else None,
        "adjudicator_model": adjudicator.model if adjudicator else None,
        "provider_route": route,
        "cloud_usage": usage.to_record(),
        "local_fallback_used": any(
            envelope.local_fallback_used for envelope in (judge, verifier, adjudicator) if envelope
        ),
        "provider_failover_reason": next(
            (
                envelope.provider_failover_reason
                for envelope in (judge, verifier, adjudicator)
                if envelope and envelope.provider_failover_reason
            ),
            None,
        ),
        **model_metadata,
    }


def sync_checkpoint_progress(
    checkpoint: Checkpoint,
    *,
    config: RunConfig,
    summary: RunSummary | None = None,
    council: RelationshipCouncil | None = None,
) -> None:
    checkpoint.max_pairs = config.max_pairs
    checkpoint.deepseek_flash_max_calls = effective_deepseek_flash_max_calls(config)
    checkpoint.deepseek_pro_max_calls = effective_deepseek_pro_max_calls(config)
    checkpoint.progress_mode_effective = config.progress_mode_effective or checkpoint.progress_mode_effective
    for key, value in role_model_metadata(config).items():
        if getattr(checkpoint, key, None) in {None, ""} or key.startswith("primary_") or key.startswith("fallback_") or key.startswith("local_"):
            setattr(checkpoint, key, value)
    if summary is not None:
        checkpoint.nodes_selected = summary.nodes_loaded
        checkpoint.candidate_pairs_generated = summary.candidate_pair_count
        checkpoint.processed_pair_count = summary.processed_count
        checkpoint.accepted_count = summary.accepted_count
        checkpoint.candidate_count = summary.candidate_review_count
        checkpoint.rejected_count = summary.rejected_count
        checkpoint.rejected_pair_count = summary.rejected_count
        checkpoint.error_count = summary.error_count
        checkpoint.embedding_cache_hits = summary.embedding_cache_hits
        checkpoint.embedding_cache_misses = summary.embedding_cache_misses
        checkpoint.embedding_dimensions = summary.embedding_dimensions
        checkpoint.hierarchy_normalization_count = summary.hierarchy_normalization_count
        checkpoint.taxonomy_part_of_conversion_count = summary.taxonomy_part_of_conversion_count
        checkpoint.validation_guard_downgrade_count = summary.validation_guard_downgrade_count
        checkpoint.validation_error_count = summary.validation_error_count
        checkpoint.validation_errors_by_role = dict(summary.validation_errors_by_role)
        checkpoint.validation_errors_by_provider = dict(summary.validation_errors_by_provider)
        checkpoint.validation_errors_by_field = dict(summary.validation_errors_by_field)
        checkpoint.effective_judge_provider = summary.effective_judge_provider or checkpoint.effective_judge_provider
        checkpoint.effective_judge_model = summary.effective_judge_model or checkpoint.effective_judge_model
        checkpoint.effective_verifier_provider = summary.effective_verifier_provider or checkpoint.effective_verifier_provider
        checkpoint.effective_verifier_model = summary.effective_verifier_model or checkpoint.effective_verifier_model
        checkpoint.effective_adjudicator_provider = summary.effective_adjudicator_provider or checkpoint.effective_adjudicator_provider
        checkpoint.effective_adjudicator_model = summary.effective_adjudicator_model or checkpoint.effective_adjudicator_model
    if council is not None:
        checkpoint.cloud_usage = council.usage
        checkpoint.provider_health = council.health
    elapsed = seconds_since_utc(checkpoint.started_at_utc) or 0.0
    if summary and summary.processed_count > 0 and elapsed > 0:
        checkpoint.pairs_per_minute = round(summary.processed_count / elapsed * 60.0, 3)
        remaining = max(0, config.max_pairs - summary.processed_count)
        checkpoint.estimated_seconds_remaining = round(remaining / max(checkpoint.pairs_per_minute, 0.001) * 60.0, 3)


def is_high_impact_decision(decision: RelationshipDecision) -> bool:
    if decision.predicate in HIGH_IMPACT_PREDICATES:
        return True
    if decision.risk_flags:
        return True
    category = decision.relation_category.lower()
    if any(term in category for term in HIGH_IMPACT_TERMS):
        return True
    return any(any(term in nature.lower() for term in HIGH_IMPACT_TERMS) for nature in decision.relation_nature)


def should_verify_decision(config: RunConfig, decision: RelationshipDecision, pair: CandidatePair) -> bool:
    if config.verify_uncertain and config.verify_threshold <= decision.confidence < config.accept_threshold:
        return True
    if config.council_mode == "local_only":
        return False
    if config.verify_accepted_cloud and decision.edge_exists and decision.confidence >= config.accept_threshold:
        sample = max(0.0, min(1.0, config.verify_accepted_sample_rate))
        bucket = int(sha256_text(pair.node_pair_key)[:8], 16) / 0xFFFFFFFF
        if bucket <= sample:
            return True
    return decision.edge_exists and is_high_impact_decision(decision)


def should_adjudicate_decision(
    config: RunConfig,
    judge_decision: RelationshipDecision,
    verifier_decision: VerificationDecision | None,
) -> bool:
    if config.council_mode == "local_only":
        return False
    if config.adjudicator_provider == "none":
        return False
    if not config.adjudicate_disagreements and not config.high_impact_pro_adjudication:
        return False
    if config.high_impact_pro_adjudication and is_high_impact_decision(judge_decision):
        return True
    if verifier_decision is None:
        return False
    if verifier_decision.corrected_edge_exists != judge_decision.edge_exists:
        return bool(config.adjudicate_disagreements)
    if verifier_decision.corrected_predicate != judge_decision.predicate:
        return bool(config.adjudicate_disagreements)
    if verifier_decision.corrected_direction != judge_decision.direction:
        return bool(config.adjudicate_disagreements)
    return False


def build_next_run_recommendations(summary: RunSummary, config: RunConfig) -> list[str]:
    recommendations: list[str] = []
    processed = max(1, summary.processed_count)
    validation_rate = summary.validation_error_count / processed
    cost_budget = summary.cloud_usage.cloud_cost_budget_usd
    cost_ok = cost_budget is None or summary.cloud_usage.cloud_estimated_cost_usd < cost_budget * 0.25
    if (
        summary.error_count == 0
        and not summary.cloud_usage.provider_failover_events
        and validation_rate <= 0.10
        and cost_ok
    ):
        recommendations.append("Safe to scale to 250 nodes / 500 pairs if accepted candidates pass manual review.")
    if validation_rate > 0.10:
        recommendations.append(
            "Validation errors are elevated; rerun the same size with --deepseek-max-tokens 1000 --progress-mode plain and inspect validation-errors.jsonl."
        )
    if config.progress_mode_effective == "rich" and running_in_git_bash():
        recommendations.append("Use --progress-mode plain in Git Bash until Rich live rendering is stable.")
    pro_cap = effective_deepseek_pro_max_calls(config)
    if pro_cap is not None and summary.cloud_usage.deepseek_pro_call_count >= pro_cap:
        recommendations.append("DeepSeek Pro cap was reached; increase --deepseek-pro-max-calls modestly for high-impact adjudication.")
    if not recommendations:
        recommendations.append("Inspect accepted/rejected review TSV files before increasing run size.")
    return recommendations


def truncate_tsv_cell(value: Any, limit: int = 300) -> str:
    text = _as_text(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")
    text = redact_secret_text(text)
    return text[:limit] + ("..." if len(text) > limit else "")


def write_tsv(path: Path, headers: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({header: truncate_tsv_cell(row.get(header), 300) for header in headers})


def write_review_tsvs(files: dict[str, Path]) -> None:
    accepted, _ = read_jsonl_records_tolerant(files["accepted"])
    rejected, _ = read_jsonl_records_tolerant(files["rejected"])
    accepted_headers = [
        "edge_key",
        "from_id",
        "predicate",
        "to_id",
        "confidence_score",
        "raw_similarity",
        "judge_provider",
        "judge_model",
        "adjudicator_provider",
        "adjudicator_model",
        "normalization_applied",
        "normalization_reason",
        "rationale",
        "evidence",
    ]
    write_tsv(files["accepted_review_tsv"], accepted_headers, accepted)
    rejected_rows: list[dict[str, Any]] = []
    for record in rejected:
        decision = record.get("judge_decision") or {}
        rejected_rows.append(
            {
                "pair_key": record.get("node_pair_key"),
                "reason": record.get("reason"),
                "provider": record.get("provider") or record.get("judge_provider"),
                "model": record.get("model") or record.get("judge_model"),
                "confidence": decision.get("confidence") if isinstance(decision, dict) else None,
                "predicate": decision.get("predicate") if isinstance(decision, dict) else None,
                "direction": decision.get("direction") if isinstance(decision, dict) else None,
                "short_rationale": decision.get("rationale") if isinstance(decision, dict) else record.get("error"),
                "validation_error_fields": ",".join(_as_text(value) for value in (record.get("failed_fields") or [])),
                "raw_response_sha256": record.get("raw_response_sha256"),
            }
        )
    rejected_headers = [
        "pair_key",
        "reason",
        "provider",
        "model",
        "confidence",
        "predicate",
        "direction",
        "short_rationale",
        "validation_error_fields",
        "raw_response_sha256",
    ]
    write_tsv(files["rejected_review_tsv"], rejected_headers, rejected_rows)


def medium_run_command_template() -> str:
    return """export DEEPSEEK_API_KEY="$(powershell.exe -NoProfile -Command "[Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY','User')" | tr -d '\\r')"

PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \\
  --dry-run \\
  --council-mode deepseek_local \\
  --allow-cloud-ai \\
  --cloud-preflight \\
  --max-nodes 250 \\
  --max-pairs 500 \\
  --candidate-top-k 10 \\
  --min-similarity 0.35 \\
  --accept-threshold 0.85 \\
  --verify-threshold 0.65 \\
  --verify-uncertain \\
  --adjudicate-disagreements \\
  --high-impact-pro-adjudication \\
  --hierarchy-canonical-predicate broader_than \\
  --convert-taxonomy-part-of \\
  --embedding-model qwen3-embedding:0.6b \\
  --judge-provider auto \\
  --verifier-provider auto \\
  --adjudicator-provider auto \\
  --deepseek-base-url https://api.deepseek.com \\
  --deepseek-flash-model deepseek-v4-flash \\
  --deepseek-pro-model deepseek-v4-pro \\
  --deepseek-api-key-env DEEPSEEK_API_KEY \\
  --deepseek-flash-max-calls 750 \\
  --deepseek-pro-max-calls 20 \\
  --cloud-total-max-calls 800 \\
  --cloud-cost-budget-usd 2.00 \\
  --fallback-to-local-on-cloud-exhaustion \\
  --fallback-to-local-on-cloud-error \\
  --fallback-to-local-on-rate-limit \\
  --progress-mode plain \\
  --sleep-seconds 2 \\
  --deepseek-sleep-seconds 1"""


def write_summary_text(files: dict[str, Path], summary: RunSummary, config: RunConfig) -> None:
    accepted, _ = read_jsonl_records_tolerant(files["accepted"], limit=10)
    top_edges = [truncate_error_text(_as_text(record.get("edge_key")), 160) for record in accepted]
    lines = [
        "Vitruvius AEC Relationship Improvement Summary",
        "",
        f"Run ID: {summary.run_id}",
        f"Output path: {summary.output_dir}",
        f"Council mode: {config.council_mode}",
        "Safety: pending-only review artifacts; active graph files are not mutated.",
        "",
        f"Nodes loaded: {summary.nodes_loaded}",
        f"Candidate pairs generated: {summary.candidate_pair_count}",
        f"Processed pairs: {summary.processed_count}",
        f"Accepted: {summary.accepted_count}",
        f"Needs review: {summary.candidate_review_count}",
        f"Rejected: {summary.rejected_count}",
        f"Errors: {summary.error_count}",
        f"Validation errors: {summary.validation_error_count}",
        f"Validation errors by role: {json.dumps(summary.validation_errors_by_role, sort_keys=True)}",
        "",
        f"DeepSeek estimated cost: ${summary.cloud_usage.cloud_estimated_cost_usd:.6f}",
        f"Cloud budget: {summary.cloud_usage.cloud_cost_budget_usd}",
        f"Budget remaining: {cloud_budget_remaining_usd(summary.cloud_usage)}",
        "",
        "Top accepted edge keys:",
        *(f"- {edge}" for edge in top_edges),
        "",
        "Recommendations:",
        *(f"- {item}" for item in summary.recommendations),
        "",
        "Inspect artifacts:",
        f"- {files['accepted_review_tsv']}",
        f"- {files['rejected_review_tsv']}",
        f"- {files['validation_errors']}",
        "",
        "Next recommended command:",
        medium_run_command_template(),
    ]
    files["summary_txt"].write_text(redact_secret_text("\n".join(lines) + "\n"), encoding="utf-8")


@dataclass(frozen=True)
class HierarchyRelation:
    parent_is_a: bool


@dataclass(frozen=True)
class GuardResult:
    decision: RelationshipDecision
    metadata: dict[str, Any]
    downgrade_reason: str | None = None


def detect_path_hierarchy(node_a: BackboneNodeView, node_b: BackboneNodeView) -> HierarchyRelation | None:
    path_a = node_a.path_code.strip()
    path_b = node_b.path_code.strip()
    if not path_a or not path_b or path_a == path_b:
        return None
    if path_b.startswith(path_a + "."):
        return HierarchyRelation(parent_is_a=True)
    if path_a.startswith(path_b + "."):
        return HierarchyRelation(parent_is_a=False)
    return None


def direction_for_hierarchy(
    relation: HierarchyRelation,
    canonical_predicate: str,
) -> DIRECTION_LITERAL:
    if canonical_predicate == "broader_than":
        return "A_to_B" if relation.parent_is_a else "B_to_A"
    return "B_to_A" if relation.parent_is_a else "A_to_B"


def apply_deterministic_acceptance_guards(
    *,
    config: RunConfig,
    node_a: BackboneNodeView,
    node_b: BackboneNodeView,
    decision: RelationshipDecision,
) -> GuardResult:
    metadata: dict[str, Any] = {
        "normalization_applied": False,
        "normalization_reason": None,
        "normalization_steps": [],
        "original_model_predicate": None,
        "original_model_direction": None,
        "normalized_predicate": None,
        "normalized_direction": None,
        "hierarchy_relation_detected": False,
        "hierarchy_parent_id": None,
        "hierarchy_child_id": None,
    }
    if not decision.edge_exists:
        return GuardResult(decision=decision, metadata=metadata)

    relation = detect_path_hierarchy(node_a, node_b)
    if relation is None:
        return GuardResult(decision=decision, metadata=metadata)
    metadata.update(
        {
            "hierarchy_relation_detected": True,
            "hierarchy_parent_id": node_a.id if relation.parent_is_a else node_b.id,
            "hierarchy_child_id": node_b.id if relation.parent_is_a else node_a.id,
        }
    )

    if decision.predicate == "part_of" and not config.convert_taxonomy_part_of:
        metadata.update(
            {
                "normalization_reason": "taxonomy_part_of_path_code_only_downgraded",
                "normalization_steps": ["taxonomy_part_of_path_code_only_downgraded"],
                "original_model_predicate": decision.predicate,
                "original_model_direction": decision.direction,
            }
        )
        return GuardResult(decision=decision, metadata=metadata, downgrade_reason="taxonomy_part_of_needs_review")

    if decision.predicate not in {"broader_than", "narrower_than", "part_of"}:
        return GuardResult(decision=decision, metadata=metadata)

    normalized_predicate = config.hierarchy_canonical_predicate
    normalized_direction = direction_for_hierarchy(relation, normalized_predicate)
    if decision.predicate == normalized_predicate and decision.direction == normalized_direction:
        return GuardResult(decision=decision, metadata=metadata)

    normalized = decision.model_copy(
        update={
            "predicate": normalized_predicate,
            "direction": normalized_direction,
            "review_recommendation": "accept_candidate"
            if decision.review_recommendation == "accept_candidate"
            else decision.review_recommendation,
        }
    )
    metadata.update(
        {
            "normalization_applied": True,
            "normalization_reason": "path_code_hierarchy_direction"
            if decision.predicate != "part_of"
            else "taxonomy_part_of_converted_to_hierarchy",
            "normalization_steps": [
                "path_code_hierarchy_direction"
                if decision.predicate != "part_of"
                else "taxonomy_part_of_converted_to_hierarchy"
            ],
            "original_model_predicate": decision.predicate,
            "original_model_direction": decision.direction,
            "normalized_predicate": normalized.predicate,
            "normalized_direction": normalized.direction,
        }
    )
    return GuardResult(decision=normalized, metadata=metadata)


def _maybe_accept_or_record(
    *,
    config: RunConfig,
    files: dict[str, Path],
    summary: RunSummary,
    checkpoint: Checkpoint,
    pair: CandidatePair,
    node_a: BackboneNodeView,
    node_b: BackboneNodeView,
    decision: RelationshipDecision,
    existing_edge_keys: set[str],
    verifier_decision: VerificationDecision | None,
    final_decision: RelationshipDecision | None = None,
    council_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    decision_for_acceptance = final_decision or decision
    metadata = dict(council_metadata or {})
    try:
        validate_relationship_decision(decision_for_acceptance)
    except BlockedPredicateError as exc:
        append_jsonl(
            files["rejected"],
            build_rejected_record(
                run_id=summary.run_id,
                pair=pair,
                reason="blocked_predicate",
                judge_decision=decision,
                verifier_decision=verifier_decision,
                error=str(exc),
                council_metadata=council_metadata,
            ),
        )
        _rejection(summary, "blocked_predicate")
        return {"result_type": "rejected", "reason": "blocked_predicate"}
    except UnsafeDecisionError as exc:
        append_jsonl(
            files["rejected"],
            build_rejected_record(
                run_id=summary.run_id,
                pair=pair,
                reason="validation_error",
                judge_decision=decision,
                verifier_decision=verifier_decision,
                error=str(exc),
                council_metadata=council_metadata,
            ),
        )
        _rejection(summary, "validation_error")
        return {"result_type": "rejected", "reason": "validation_error"}

    if not decision_for_acceptance.edge_exists:
        append_jsonl(
            files["rejected"],
            build_rejected_record(
                run_id=summary.run_id,
                pair=pair,
                reason="no_edge",
                judge_decision=decision,
                verifier_decision=verifier_decision,
                error=None,
                council_metadata=council_metadata,
            ),
        )
        _rejection(summary, "no_edge")
        return {"result_type": "rejected", "reason": "no_edge"}

    guard = apply_deterministic_acceptance_guards(
        config=config,
        node_a=node_a,
        node_b=node_b,
        decision=decision_for_acceptance,
    )
    decision_for_acceptance = guard.decision
    metadata.update(guard.metadata)
    if guard.metadata.get("normalization_applied"):
        summary.hierarchy_normalization_count += 1
        checkpoint.hierarchy_normalization_count += 1
        if guard.metadata.get("normalization_reason") == "taxonomy_part_of_converted_to_hierarchy":
            summary.taxonomy_part_of_conversion_count += 1
            checkpoint.taxonomy_part_of_conversion_count += 1
    if guard.downgrade_reason:
        summary.validation_guard_downgrade_count += 1
        checkpoint.validation_guard_downgrade_count += 1
        metadata["final_guard_passed"] = False
        metadata["final_guard_checks"] = {
            "duplicate_edge": "unknown",
            "blocked_predicate": "pass",
            "confidence_threshold": "pass" if decision_for_acceptance.confidence >= config.accept_threshold else "fail",
            "evidence_present": "pass" if decision_for_acceptance.evidence.strip() else "fail",
            "rationale_present": "pass" if decision_for_acceptance.rationale.strip() else "fail",
            "hierarchy_consistency": "fail",
            "taxonomy_part_of_guard": "fail",
        }
        append_jsonl(
            files["candidate"],
            build_needs_review_record(
                run_id=summary.run_id,
                pair=pair,
                judge_decision=decision,
                verifier_decision=verifier_decision,
                reason=guard.downgrade_reason,
                council_metadata=metadata,
            ),
        )
        summary.candidate_review_count += 1
        return {
            "result_type": "needs_review",
            "reason": guard.downgrade_reason,
            "confidence": decision_for_acceptance.confidence,
        }

    metadata["final_guard_checks"] = {
        "duplicate_edge": "pass",
        "blocked_predicate": "pass" if decision_for_acceptance.predicate not in BLOCKED_PREDICATES else "fail",
        "confidence_threshold": "pass" if decision_for_acceptance.confidence >= config.accept_threshold else "fail",
        "evidence_present": "pass" if decision_for_acceptance.evidence.strip() else "fail",
        "rationale_present": "pass" if decision_for_acceptance.rationale.strip() else "fail",
        "hierarchy_consistency": "pass",
        "taxonomy_part_of_guard": "pass",
    }
    metadata["final_guard_passed"] = all(value == "pass" for value in metadata["final_guard_checks"].values())

    candidate_edge = decision_to_edge_record(
        run_id=summary.run_id,
        node_a=node_a,
        node_b=node_b,
        pair=pair,
        decision=decision_for_acceptance,
        embedding_model=config.embedding_model,
        judge_model=config.judge_model,
        verifier_model=config.verifier_model if verifier_decision else None,
        verifier_decision=verifier_decision,
        created_at_utc=utc_now(),
        council_metadata=metadata,
    )
    if is_duplicate_edge_record(candidate_edge, existing_edge_keys, checkpoint.accepted_edge_keys):
        metadata["final_guard_passed"] = False
        metadata["final_guard_checks"]["duplicate_edge"] = "fail"
        append_jsonl(
            files["rejected"],
            build_rejected_record(
                run_id=summary.run_id,
                pair=pair,
                reason="duplicate_edge",
                judge_decision=decision,
                verifier_decision=verifier_decision,
                error=None,
                council_metadata=metadata,
            ),
        )
        _rejection(summary, "duplicate_edge")
        return {"result_type": "rejected", "reason": "duplicate_edge"}

    accept = (
        decision_for_acceptance.edge_exists
        and decision_for_acceptance.predicate in ALLOWED_PREDICATES
        and decision_for_acceptance.confidence >= config.accept_threshold
        and decision_for_acceptance.direction != "none"
        and bool(decision_for_acceptance.rationale.strip())
        and bool(decision_for_acceptance.evidence.strip())
        and decision_for_acceptance.review_recommendation == "accept_candidate"
    )
    if accept:
        candidate_edge["final_guard_passed"] = True
        candidate_edge["final_guard_checks"] = metadata["final_guard_checks"]
        append_jsonl(files["accepted"], candidate_edge)
        checkpoint.accepted_edge_keys.append(candidate_edge["edge_key"])
        summary.accepted_count += 1
        logger.info("Accepted edge %s", candidate_edge["edge_key"])
        return {
            "result_type": "accepted",
            "edge_key": candidate_edge["edge_key"],
            "confidence": decision_for_acceptance.confidence,
        }

    metadata["final_guard_passed"] = False
    if not decision_for_acceptance.rationale.strip():
        reject_reason = "missing_rationale"
    elif not decision_for_acceptance.evidence.strip():
        reject_reason = "missing_evidence"
    elif decision_for_acceptance.confidence < config.verify_threshold and decision_for_acceptance.review_recommendation == "reject":
        reject_reason = "low_confidence"
    else:
        reject_reason = "low_confidence"

    if decision_for_acceptance.review_recommendation == "reject":
        append_jsonl(
            files["rejected"],
            build_rejected_record(
                run_id=summary.run_id,
                pair=pair,
                reason=reject_reason,
                judge_decision=decision,
                verifier_decision=verifier_decision,
                error=None,
                council_metadata=metadata,
            ),
        )
        _rejection(summary, reject_reason)
        return {"result_type": "rejected", "reason": reject_reason, "confidence": decision_for_acceptance.confidence}

    review_reason = "safe_schema_repair_needs_review" if decision_for_acceptance.review_recommendation == "needs_review" else "uncertain_confidence"
    if decision_for_acceptance.confidence < config.accept_threshold:
        review_reason = "uncertain_confidence"
    append_jsonl(
        files["candidate"],
        build_needs_review_record(
            run_id=summary.run_id,
            pair=pair,
            judge_decision=decision,
            verifier_decision=verifier_decision,
            reason=review_reason,
            council_metadata=metadata,
        ),
    )
    summary.candidate_review_count += 1
    return {"result_type": "needs_review", "reason": review_reason, "confidence": decision_for_acceptance.confidence}


def _verification_to_relationship_decision(
    original: RelationshipDecision,
    verification: VerificationDecision,
) -> RelationshipDecision:
    return RelationshipDecision(
        edge_exists=verification.corrected_edge_exists,
        predicate=verification.corrected_predicate,
        direction=verification.corrected_direction,
        confidence=verification.corrected_confidence,
        relation_type=original.relation_type,
        relation_category=original.relation_category,
        relation_nature=original.relation_nature,
        rationale=verification.rationale or original.rationale,
        evidence=original.evidence,
        risk_flags=original.risk_flags,
        review_recommendation="accept_candidate"
        if verification.corrected_confidence >= original.confidence
        else original.review_recommendation,
    )


class RelationshipCouncil:
    def __init__(
        self,
        config: RunConfig,
        *,
        generate_text: Callable[..., str],
        verifier_text: Callable[..., str] | None = None,
        cloud_post_json: Callable[..., dict[str, Any]] | None = None,
        usage: CloudUsage | None = None,
        health: ProviderHealth | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        self.generate_text = generate_text
        self.verifier_text = verifier_text or generate_text
        self.cloud_post_json = cloud_post_json
        self.usage = usage or CloudUsage()
        self.health = health or ProviderHealth()
        self.sleep = sleep
        self.usage.cloud_total_max_calls = effective_cloud_total_max_calls(config)
        self.usage.cloud_cost_budget_usd = effective_cloud_cost_budget(config)
        self.usage.kimi_max_calls = effective_kimi_max_calls(config)
        self.usage.kimi_disabled = not config.enable_kimi_experimental
        self.usage.kimi_disabled_reason = (
            "experimental_enabled"
            if config.enable_kimi_experimental
            else "disabled_for_relationship_workflow"
        )
        self.response_rejections: list[dict[str, Any]] = []

    def judge(self, prompt: str, schema: dict[str, Any]) -> ProviderEnvelope:
        return self._call_role("judge", prompt, schema)

    def verify(self, prompt: str, schema: dict[str, Any]) -> ProviderEnvelope:
        return self._call_role("verifier", prompt, schema)

    def adjudicate(self, prompt: str, schema: dict[str, Any]) -> ProviderEnvelope:
        return self._call_role("adjudicator", prompt, schema)

    def _call_role(self, role: str, prompt: str, schema: dict[str, Any]) -> ProviderEnvelope:
        route: list[ProviderRouteStep] = []
        failover_reason: str | None = None
        for provider, model in self._provider_priority(role):
            if provider == "none":
                continue
            health_key = self._provider_health_key(provider, model, role)
            allowed, reason = self._provider_allowed(provider, model, role=role)
            if not allowed:
                route.append(ProviderRouteStep(role, provider, model, "skipped", reason))
                failover_reason = failover_reason or reason
                continue
            try:
                if provider == "ollama":
                    if failover_reason:
                        self.usage.record_local_fallback(role, failover_reason)
                    local_generate = self.verifier_text if role in {"verifier", "adjudicator"} else self.generate_text
                    started_at = time.monotonic()
                    raw = local_generate(prompt=prompt, model=model, schema=schema)
                    latency = time.monotonic() - started_at
                    self.health.record_latency(provider, latency)
                    self.health.record_latency(health_key, latency)
                    self.health.mark_success(health_key)
                    route.append(ProviderRouteStep(role, provider, model, "success"))
                    return ProviderEnvelope(
                        raw_text=raw,
                        provider=provider,
                        model=model,
                        route=route,
                        local_fallback_used=bool(failover_reason),
                        provider_failover_reason=failover_reason,
                    )
                started_at = time.monotonic()
                response = self._call_cloud(provider, model, prompt, schema, role=role)
                latency = time.monotonic() - started_at
                self.health.record_latency(provider, latency)
                self.health.record_latency(health_key, latency)
                if provider == "kimi" and self.config.kimi_estimated_cost_per_call_usd:
                    response.usage["_estimated_cost_usd"] = self.config.kimi_estimated_cost_per_call_usd
                self.usage.record_cloud_usage(provider, model, response.usage)
                self.health.mark_success(provider)
                self.health.mark_success(health_key)
                route.append(ProviderRouteStep(role, provider, model, "success"))
                return ProviderEnvelope(
                    raw_text=response.content,
                    provider=provider,
                    model=model,
                    route=route,
                    finish_reason=response.finish_reason,
                    metadata={**response.metadata, "usage": response.usage},
                    provider_failover_reason=failover_reason,
                )
            except CloudResponseRejectedError as exc:
                route.append(ProviderRouteStep(role, provider, model, "rejected", exc.reason))
                raise
            except CloudProviderError as exc:
                status = self._health_status_for_error(exc)
                self.health.mark_failure(provider, status, self.config.cloud_circuit_breaker_failures)
                self.health.mark_failure(health_key, status, self.config.cloud_circuit_breaker_failures)
                event = {
                    "role": role,
                    "provider": provider,
                    "model": model,
                    "reason": exc.reason,
                    "status_code": exc.status_code,
                    "created_at_utc": utc_now(),
                }
                self.usage.provider_failover_events.append(event)
                route.append(ProviderRouteStep(role, provider, model, "failed", exc.reason))
                reason = exc.reason if exc.reason.startswith((provider, "cloud_")) else f"{provider}_{exc.reason}"
                failover_reason = failover_reason or reason
                if exc.reason == "disabled_auth_error" and self.config.stop_on_cloud_auth_error:
                    raise
                if not self._fallback_allowed(exc):
                    raise
                continue
        raise CloudProviderError("council", "no_provider_available", "No provider was available for council role.")

    def _call_cloud(
        self,
        provider: str,
        model: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        role: str | None = None,
    ) -> CloudChatResponse:
        attempts = max(1, self.config.cloud_max_retries + 1)
        last_error: CloudProviderError | None = None
        truncated_retry_attempted = False
        for attempt in range(attempts):
            allowed, reason = self._provider_allowed(provider, model, role=role)
            if not allowed:
                message = reason or "provider_not_allowed"
                raise CloudProviderError(provider, message, message, retryable=False)
            self.usage.record_cloud_attempt(provider, model, role=role, deepseek_tier=self._deepseek_tier(provider, model))
            try:
                if provider == "kimi":
                    response = call_kimi_chat_completion(
                        config=self.config,
                        prompt=prompt,
                        schema=schema,
                        post_json=self.cloud_post_json,
                    )
                    self.sleep(self.config.kimi_sleep_seconds)
                    return response
                response = call_deepseek_chat_completion(
                    config=self.config,
                    prompt=prompt,
                    schema=schema,
                    model=model,
                    post_json=self.cloud_post_json,
                )
                self.sleep(self.config.deepseek_sleep_seconds)
                return response
            except CloudResponseRejectedError as exc:
                if (
                    provider == "deepseek"
                    and exc.reason == "deepseek_json_truncated"
                    and self.config.deepseek_retry_truncated_json
                    and not truncated_retry_attempted
                    and attempt < attempts - 1
                ):
                    truncated_retry_attempted = True
                    old_tokens = int(self.config.deepseek_max_tokens)
                    self.config.deepseek_max_tokens = min(1500, max(old_tokens + 1, int(math.ceil(old_tokens * 1.5))))
                    self.usage.provider_failover_events.append(
                        {
                            "role": role,
                            "provider": provider,
                            "model": model,
                            "reason": "deepseek_json_truncated_retry",
                            "old_max_tokens": old_tokens,
                            "new_max_tokens": self.config.deepseek_max_tokens,
                            "raw_response_sha256": sha256_text(exc.raw_response or ""),
                            "created_at_utc": utc_now(),
                        }
                    )
                    self.response_rejections.append(
                        {
                            "role": role,
                            "provider": provider,
                            "model": model,
                            "error_type": "finish_reason_length",
                            "reason": exc.reason,
                            "raw_response_excerpt": sanitize_raw_excerpt(exc.raw_response),
                            "raw_response_sha256": raw_response_sha256(exc.raw_response),
                            "finish_reason": exc.finish_reason,
                            "usage": sanitize_for_artifact(exc.usage),
                            "prompt_hash": sha256_text(prompt),
                            "repair_attempted": True,
                            "repair_successful": True,
                            "final_action": "retried",
                            "created_at_utc": utc_now(),
                        }
                    )
                    self.sleep(self.config.cloud_backoff_seconds)
                    continue
                if provider == "deepseek" and exc.reason in {
                    "deepseek_content_filter",
                    "deepseek_insufficient_system_resource",
                }:
                    raise CloudProviderError(provider, exc.reason, str(exc), retryable=False) from exc
                raise
            except CloudProviderError as exc:
                last_error = exc
                if not exc.retryable or attempt >= attempts - 1:
                    raise
                self.sleep(self.config.cloud_backoff_seconds)
        assert last_error is not None
        raise last_error

    def _provider_priority(self, role: str) -> list[tuple[str, str]]:
        return provider_priority_for_role(self.config, role)

    def _model_for_provider_role(self, provider: str, role: str) -> str:
        if provider == "kimi":
            return self.config.kimi_model
        if provider == "deepseek":
            return self.config.deepseek_pro_model if role == "adjudicator" else self.config.deepseek_flash_model
        if role == "judge":
            return self.config.judge_model
        return self.config.verifier_model or DEFAULT_VERIFIER_MODEL

    def _provider_health_key(self, provider: str, model: str, role: str | None) -> str:
        if provider == "deepseek":
            return "deepseek_pro" if model == self.config.deepseek_pro_model else "deepseek_flash"
        if provider == "ollama":
            return "ollama_judge" if role == "judge" else "ollama_verifier"
        return provider

    def _deepseek_tier(self, provider: str, model: str) -> str | None:
        if provider != "deepseek":
            return None
        return "pro" if model == self.config.deepseek_pro_model else "flash"

    def _provider_allowed(self, provider: str, model: str, *, role: str | None = None) -> tuple[bool, str | None]:
        if provider == "ollama":
            if self.config.strict_cloud_only:
                return False, "strict_cloud_only"
            return True, None
        if provider == "kimi" and not self.config.enable_kimi_experimental:
            self.health.states["kimi"] = "disabled_for_relationship_workflow"
            return False, "kimi_disabled_for_relationship_workflow"
        if not self.config.allow_cloud_ai:
            return False, "cloud_not_enabled"
        health_key = self._provider_health_key(provider, model, role)
        if not self.health.is_available(provider):
            return False, self.health.status(provider)
        if not self.health.is_available(health_key):
            return False, self.health.status(health_key)
        if self.usage.cloud_total_max_calls is not None and self.usage.cloud_call_count >= self.usage.cloud_total_max_calls:
            self.health.states[provider] = "disabled_budget"
            return False, "cloud_total_max_calls_exhausted"
        if self.usage.cloud_cost_budget_usd is not None and self.usage.cloud_estimated_cost_usd >= self.usage.cloud_cost_budget_usd:
            self.health.states[provider] = "disabled_budget"
            return False, "cloud_cost_budget_exhausted"
        if provider == "kimi" and self.usage.kimi_max_calls is not None and self.usage.kimi_call_count >= self.usage.kimi_max_calls:
            self.health.states[provider] = "exhausted"
            return False, "kimi_max_calls_exhausted"
        if (
            provider == "kimi"
            and self.usage.cloud_cost_budget_usd is not None
            and self.config.kimi_estimated_cost_per_call_usd
            and self.usage.cloud_estimated_cost_usd + self.config.kimi_estimated_cost_per_call_usd
            > self.usage.cloud_cost_budget_usd
        ):
            self.health.states[provider] = "disabled_budget"
            return False, "cloud_cost_budget_exhausted"
        if provider == "deepseek":
            flash_cap = effective_deepseek_flash_max_calls(self.config)
            pro_cap = effective_deepseek_pro_max_calls(self.config)
            if model == self.config.deepseek_pro_model and pro_cap is not None and self.usage.deepseek_pro_call_count >= pro_cap:
                self.health.states["deepseek_pro"] = "exhausted"
                return False, "deepseek_pro_max_calls_exhausted"
            if model != self.config.deepseek_pro_model and flash_cap is not None and self.usage.deepseek_flash_call_count >= flash_cap:
                self.health.states["deepseek_flash"] = "exhausted"
                return False, "deepseek_flash_max_calls_exhausted"
        return True, None

    def _health_status_for_error(self, error: CloudProviderError) -> str:
        if error.reason in {"cloud_total_max_calls_exhausted", "cloud_cost_budget_exhausted"}:
            return "disabled_budget"
        if error.reason.endswith("_max_calls_exhausted"):
            return "exhausted"
        if error.reason in {"disabled_auth_error", "exhausted", "disabled_rate_limit", "disabled_timeout", "disabled_custom_base_url"}:
            return error.reason
        return "degraded"

    def _fallback_allowed(self, error: CloudProviderError) -> bool:
        if (
            error.reason in {"exhausted", "disabled_budget", "cloud_total_max_calls_exhausted", "cloud_cost_budget_exhausted"}
            or error.reason.endswith("_max_calls_exhausted")
        ):
            return self.config.fallback_to_local_on_cloud_exhaustion
        if error.reason == "disabled_rate_limit":
            return self.config.fallback_to_local_on_rate_limit
        return self.config.fallback_to_local_on_cloud_error


def _candidate_pair_from_artifact(record: dict[str, Any], *, run_id: str, embedding_model: str) -> CandidatePair:
    node_a_id = _as_text(record.get("node_a_id"))
    node_b_id = _as_text(record.get("node_b_id"))
    if not node_a_id or not node_b_id:
        raise ValueError("Audit artifact is missing node_a_id or node_b_id")
    node_pair_key = _as_text(record.get("node_pair_key")) or pair_key_for(node_a_id, node_b_id)
    similarity = record.get("similarity", record.get("raw_similarity", 0.0))
    return CandidatePair(
        run_id=run_id,
        node_pair_key=node_pair_key,
        node_a_id=node_a_id,
        node_b_id=node_b_id,
        similarity=float(similarity or 0.0),
        embedding_model=_as_text(record.get("embedding_model")) or embedding_model,
        created_at_utc=utc_now(),
    )


def _relationship_decision_from_artifact(record: dict[str, Any], pair: CandidatePair) -> RelationshipDecision:
    decision_data = record.get("judge_decision")
    if isinstance(decision_data, dict):
        decision = RelationshipDecision.model_validate(decision_data)
        validate_relationship_decision(decision)
        return decision

    from_id = _as_text(record.get("from_id"))
    to_id = _as_text(record.get("to_id"))
    predicate = _as_text(record.get("predicate")) or "none"
    if from_id == pair.node_a_id and to_id == pair.node_b_id:
        direction = "A_to_B"
    elif from_id == pair.node_b_id and to_id == pair.node_a_id:
        direction = "B_to_A"
    elif predicate == "conflicts_with" and from_id and to_id:
        direction = "undirected"
    else:
        direction = "none"

    relation_nature = record.get("relation_nature") or []
    if isinstance(relation_nature, str):
        relation_nature = [relation_nature]
    risk_flags = record.get("risk_flags") or []
    if isinstance(risk_flags, str):
        risk_flags = [risk_flags]
    confidence = float(record.get("confidence_score", record.get("weight", 0.0)) or 0.0)
    decision = RelationshipDecision(
        edge_exists=predicate != "none" and direction != "none",
        predicate=predicate,  # type: ignore[arg-type]
        direction=direction,  # type: ignore[arg-type]
        confidence=confidence,
        relation_type=_as_text(record.get("relation_type")) or "artifact_relationship",
        relation_category=_as_text(record.get("relation_category")) or "other",
        relation_nature=[_as_text(value) for value in relation_nature if _as_text(value)],
        rationale=_as_text(record.get("rationale")) or "Prior relationship-improvement artifact.",
        evidence=_as_text(record.get("evidence")) or _as_text(record.get("rationale")) or "Prior relationship-improvement artifact.",
        risk_flags=[_as_text(value) for value in risk_flags if _as_text(value)],
        review_recommendation="accept_candidate" if predicate != "none" else "reject",
    )
    validate_relationship_decision(decision)
    return decision


def _run_audit_only(
    *,
    config: RunConfig,
    run_id: str,
    files: dict[str, Path],
    checkpoint: Checkpoint,
    nodes_by_id: dict[str, BackboneNodeView],
    existing_relationships_loaded: int,
    council: RelationshipCouncil,
    reporter: ProgressReporter,
) -> RunSummary:
    logger.info("Audit-only mode: reading prior candidate/accepted artifacts; no new similarity candidates will be generated")
    reporter.set_phase("verifying", "audit_only")
    summary = RunSummary(
        run_id=run_id,
        output_dir=str(files["report"].parent),
        nodes_loaded=len(nodes_by_id),
        existing_relationships_loaded=existing_relationships_loaded,
        cloud_usage=council.usage,
        provider_health=council.health,
    )
    for key, value in role_model_metadata(config).items():
        if hasattr(summary, key):
            setattr(summary, key, value)
    summary.progress_mode_effective = config.progress_mode_effective
    processed_pair_keys = set(checkpoint.processed_pair_keys)
    verifier_schema = VerificationDecision.model_json_schema()
    relationship_schema = RelationshipDecision.model_json_schema()
    source_paths = (files["accepted"], files["candidate"])

    checkpoint.status = "in_progress"
    checkpoint.phase = "verifying"
    save_checkpoint(files["checkpoint"], checkpoint)

    for source_path in source_paths:
        for line_number, record in iter_jsonl_objects(source_path):
            if summary.processed_count >= config.max_pairs:
                break
            pair: CandidatePair | None = None
            council_metadata: dict[str, Any] | None = None
            audit_key = ""
            try:
                pair = _candidate_pair_from_artifact(record, run_id=run_id, embedding_model=config.embedding_model)
                audit_key = f"audit::{pair.node_pair_key}::{source_path.name}:{line_number}"
                if audit_key in processed_pair_keys:
                    summary.skipped_count += 1
                    continue
                node_a = nodes_by_id[pair.node_a_id]
                node_b = nodes_by_id[pair.node_b_id]
                decision = _relationship_decision_from_artifact(record, pair)
                verifier_prompt = build_verifier_prompt(
                    node_a=node_a,
                    node_b=node_b,
                    judge_decision=decision,
                    schema=verifier_schema,
                )
                verifier_envelope = council.verify(verifier_prompt, verifier_schema)
                verifier_decision = parse_verification_decision(verifier_envelope.raw_text)
                adjudicator_envelope: ProviderEnvelope | None = None
                adjudicator_decision: RelationshipDecision | None = None
                if should_adjudicate_decision(config, decision, verifier_decision):
                    adjudicator_prompt = build_adjudicator_prompt(
                        node_a=node_a,
                        node_b=node_b,
                        judge_decision=decision,
                        verifier_decision=verifier_decision,
                        schema=relationship_schema,
                    )
                    adjudicator_envelope = council.adjudicate(adjudicator_prompt, relationship_schema)
                    adjudicator_decision = parse_relationship_decision(
                        adjudicator_envelope.raw_text,
                        role="adjudicator",
                        config=config,
                    )
                council_metadata = build_council_metadata(
                    config=config,
                    usage=council.usage,
                    judge=None,
                    verifier=verifier_envelope,
                    adjudicator=adjudicator_envelope,
                )
                append_jsonl(
                    files["audit"],
                    {
                        "schema_version": "aec-relationship-council-audit/v1",
                        "run_id": run_id,
                        "source_file": source_path.name,
                        "source_line": line_number,
                        "node_pair_key": pair.node_pair_key,
                        "node_a_id": pair.node_a_id,
                        "node_b_id": pair.node_b_id,
                        "original_decision": decision.model_dump(),
                        "verification_decision": verifier_decision.model_dump(),
                        "adjudicator_decision": adjudicator_decision.model_dump() if adjudicator_decision else None,
                        **council_metadata,
                        "created_at_utc": utc_now(),
                    },
                )
                summary.processed_count += 1
                summary.candidate_review_count += 1
                reporter.update_pair_processed(pair.node_pair_key, "audited", verifier_envelope.to_metadata()["provider_route"])
                reporter.update_cloud_usage(council.usage)
                append_progress_event(
                    files,
                    checkpoint,
                    reporter,
                    build_progress_event(
                        run_id=run_id,
                        phase="verifying",
                        event_type="pair_completed",
                        message=f"Audited prior artifact {pair.node_pair_key}",
                        pair_key=pair.node_pair_key,
                    ),
                )
            except Exception as exc:
                summary.error_count += 1
                checkpoint.error_count += 1
                append_jsonl(
                    files["errors"],
                    {
                        "schema_version": "aec-relationship-improvement-error/v1",
                        "run_id": run_id,
                        "node_pair_key": pair.node_pair_key if pair else None,
                        "node_a_id": pair.node_a_id if pair else None,
                        "node_b_id": pair.node_b_id if pair else None,
                        "error": truncate_error_text(str(exc)),
                        "traceback": truncate_error_text(traceback.format_exc(), 1200),
                        "council_mode": config.council_mode,
                        "provider_route": (council_metadata or {}).get("provider_route", []),
                        "source_file": source_path.name,
                        "source_line": line_number,
                        "created_at_utc": utc_now(),
                    },
                )
                logger.exception("Error auditing artifact %s:%d", source_path, line_number)
                reporter.update_decision("error", reason=str(exc))
            finally:
                if audit_key:
                    processed_pair_keys.add(audit_key)
                    checkpoint.processed_pair_keys = sorted(processed_pair_keys)
                checkpoint.cloud_usage = council.usage
                checkpoint.provider_health = council.health
                checkpoint.last_provider_used = (council_metadata or {}).get("verifier_provider")
                checkpoint.phase = "verifying"
                sync_checkpoint_progress(checkpoint, config=config, summary=summary, council=council)
                checkpoint.error_count = summary.error_count
                save_checkpoint(files["checkpoint"], checkpoint)
        if summary.processed_count >= config.max_pairs:
            break

    checkpoint.status = "completed"
    checkpoint.phase = "completed"
    checkpoint.cloud_usage = council.usage
    checkpoint.provider_health = council.health
    checkpoint.error_count = summary.error_count
    sync_checkpoint_progress(checkpoint, config=config, summary=summary, council=council)
    summary.cloud_usage = council.usage
    summary.provider_health = council.health
    summary.elapsed_seconds = round(seconds_since_utc(checkpoint.started_at_utc) or checkpoint.elapsed_seconds, 3)
    summary.pairs_per_minute = checkpoint.pairs_per_minute
    summary.progress_mode_effective = config.progress_mode_effective
    summary.recommendations = build_next_run_recommendations(summary, config)
    write_review_tsvs(files)
    write_summary_text(files, summary, config)
    save_checkpoint(files["checkpoint"], checkpoint)
    write_json(files["report"], summary.to_record())
    reporter.finish(summary)
    reporter.close()
    logger.info(
        "Audit-only run completed: audited=%d skipped=%d errors=%d",
        summary.processed_count,
        summary.skipped_count,
        summary.error_count,
    )
    return summary


def run_relationship_improvement(
    config: RunConfig,
    *,
    embed_texts: Callable[[list[str]], list[list[float]]] | None = None,
    generate_text: Callable[..., str] | None = None,
    verifier_text: Callable[..., str] | None = None,
    cloud_post_json: Callable[..., dict[str, Any]] | None = None,
    progress_reporter: ProgressReporter | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> RunSummary:
    ensure_apply_mode_is_deferred(config.apply)
    ensure_local_ollama_base_url(config.ollama_base_url)
    validate_council_config(config)
    repo_root = get_repo_root()
    input_path = resolve_path(config.input_path, repo_root)
    output_root = resolve_path(config.output_root, repo_root)
    run_id = config.run_id
    if config.resume and not run_id:
        run_id = find_latest_in_progress_run(output_root)
        if run_id is None:
            run_id = default_run_id()
    run_id = run_id or default_run_id()
    output_dir = output_root / run_id
    files = _touch_output_files(output_dir)
    setup_logging(output_dir)
    reporter = progress_reporter or create_progress_reporter(config)
    reporter.start_run(config, run_id, output_dir)
    reporter.set_phase("loading")

    logger.info("Run started: %s", run_id)
    logger.info("CLI config: %s", json.dumps(sanitize_for_artifact(_config_for_logging(config)), sort_keys=True))
    logger.info("Input path: %s", input_path)
    logger.info("Output directory: %s", output_dir)
    logger.info("Models: embedding=%s judge=%s verifier=%s", config.embedding_model, config.judge_model, config.verifier_model)
    logger.info("Ollama base URL: %s", config.ollama_base_url)
    logger.info(
        "Council mode: %s cloud_enabled=%s judge_provider=%s verifier_provider=%s adjudicator_provider=%s",
        config.council_mode,
        config.allow_cloud_ai,
        config.judge_provider,
        config.verifier_provider,
        config.adjudicator_provider,
    )
    logger.info("Cloud API key env vars: deepseek=%s kimi=%s (kimi disabled by default)", config.deepseek_api_key_env, config.kimi_api_key_env)
    logger.info("Pending-only mode is enforced; active graph mutation is disabled.")

    checkpoint = load_checkpoint(files["checkpoint"]) if (config.resume or config.council_mode == "audit_only") else None
    if checkpoint is None:
        checkpoint = Checkpoint(
            run_id=run_id,
            status="in_progress",
            phase="loading",
            input_path=str(input_path),
            output_dir=str(output_dir),
            embedding_model=config.embedding_model,
            judge_model=config.judge_model,
            verifier_model=config.verifier_model,
            council_mode=config.council_mode,
            max_pairs=config.max_pairs,
            deepseek_flash_max_calls=effective_deepseek_flash_max_calls(config),
            deepseek_pro_max_calls=effective_deepseek_pro_max_calls(config),
            cloud_usage=CloudUsage(
                cloud_total_max_calls=effective_cloud_total_max_calls(config),
                cloud_cost_budget_usd=effective_cloud_cost_budget(config),
                kimi_max_calls=effective_kimi_max_calls(config),
                kimi_disabled=not config.enable_kimi_experimental,
                kimi_disabled_reason="experimental_enabled"
                if config.enable_kimi_experimental
                else "disabled_for_relationship_workflow",
            ),
        )
        append_progress_event(
            files,
            checkpoint,
            reporter,
            build_progress_event(
                run_id=run_id,
                phase="loading",
                event_type="phase_started",
                message="Run started",
                counts={"max_pairs": config.max_pairs, "max_nodes": config.max_nodes},
            ),
        )
        save_checkpoint(files["checkpoint"], checkpoint)
    else:
        if config.reset_cloud_budget_for_resume:
            checkpoint.cloud_usage = CloudUsage(
                cloud_total_max_calls=effective_cloud_total_max_calls(config),
                cloud_cost_budget_usd=effective_cloud_cost_budget(config),
                kimi_max_calls=effective_kimi_max_calls(config),
                kimi_disabled=not config.enable_kimi_experimental,
                kimi_disabled_reason="experimental_enabled"
                if config.enable_kimi_experimental
                else "disabled_for_relationship_workflow",
            )
        logger.info(
            "Resume state: processed=%d accepted=%d rejected=%d errors=%d",
            len(checkpoint.processed_pair_keys),
            len(checkpoint.accepted_edge_keys),
            checkpoint.rejected_pair_count,
            checkpoint.error_count,
        )
    checkpoint.council_mode = config.council_mode

    records, relationships = load_backbone_graph(input_path)
    nodes = [make_node_view(record) for record in records[: max(0, config.max_nodes)]]
    nodes_by_id = {node.id: node for node in nodes}
    existing_edge_keys = build_existing_edge_keys(relationships)
    existing_pair_index = build_existing_pair_index(relationships)
    logger.info("Loaded %d nodes and %d existing relationships", len(nodes), len(relationships))
    checkpoint.nodes_loaded = len(records)
    checkpoint.nodes_selected = len(nodes)
    checkpoint.embedding_total = len(nodes)
    checkpoint.max_pairs = config.max_pairs
    reporter.set_totals(nodes=len(nodes), pairs=config.max_pairs)
    save_checkpoint(files["checkpoint"], checkpoint)

    stable_cache_path = None
    if not config.no_stable_embedding_cache:
        stable_cache_path = config.stable_embedding_cache_path
        if stable_cache_path is None:
            stable_cache_path = (
                repo_root
                / "005_Operational-Intelligence-Layer"
                / "embeddings"
                / "aec-mepfs-backbone"
                / safe_model_name(config.embedding_model)
                / "node-embeddings.jsonl"
            )
        else:
            stable_cache_path = resolve_path(stable_cache_path, repo_root)

    embed_texts = embed_texts or make_ollama_embedder(config)
    generate_text = generate_text or make_ollama_generator(config)
    verifier_text = verifier_text or generate_text
    council = RelationshipCouncil(
        config,
        generate_text=generate_text,
        verifier_text=verifier_text,
        cloud_post_json=cloud_post_json,
        usage=checkpoint.cloud_usage,
        health=checkpoint.provider_health,
        sleep=sleep,
    )
    if should_run_deepseek_preflight(config):
        checkpoint.phase = "loading"
        checkpoint.current_operation = "deepseek_preflight"
        checkpoint.current_provider = "deepseek"
        checkpoint.current_model = config.deepseek_flash_model
        save_checkpoint(files["checkpoint"], checkpoint)
        preflight_ok = run_deepseek_preflight(config, council)
        checkpoint.cloud_usage = council.usage
        checkpoint.provider_health = council.health
        append_progress_event(
            files,
            checkpoint,
            reporter,
            build_progress_event(
                run_id=run_id,
                phase="loading",
                event_type="phase_completed" if preflight_ok else "provider_failover",
                message="DeepSeek preflight completed" if preflight_ok else "DeepSeek preflight failed; local fallback remains available",
                provider="deepseek",
                model=config.deepseek_flash_model,
                reason=None if preflight_ok else "deepseek_preflight_failed",
            ),
        )
        logger.info("DeepSeek preflight %s", "passed" if preflight_ok else "failed; local fallback remains available")
        if config.strict_cloud_only and not preflight_ok:
            raise CloudProviderError("deepseek", "deepseek_preflight_failed", "DeepSeek preflight failed in strict cloud mode.", retryable=False)
        save_checkpoint(files["checkpoint"], checkpoint)
    if config.council_mode == "audit_only":
        return _run_audit_only(
            config=config,
            run_id=run_id,
            files=files,
            checkpoint=checkpoint,
            nodes_by_id=nodes_by_id,
            existing_relationships_loaded=len(relationships),
            council=council,
            reporter=reporter,
        )

    checkpoint.phase = "embedding"
    checkpoint.current_operation = "embedding"
    reporter.set_phase("embedding")
    append_progress_event(
        files,
        checkpoint,
        reporter,
        build_progress_event(
            run_id=run_id,
            phase="embedding",
            event_type="phase_started",
            message="Embedding phase started",
            counts={"embedding_total": len(nodes)},
        ),
    )
    save_checkpoint(files["checkpoint"], checkpoint)
    embedding_latency_samples = 0

    def _embedding_progress(
        processed: int,
        hits: int,
        misses: int,
        dimensions: int | None,
        latency: float | None,
    ) -> None:
        nonlocal embedding_latency_samples
        checkpoint.phase = "embedding"
        checkpoint.embedding_processed = processed
        checkpoint.embedding_cache_hits = hits
        checkpoint.embedding_cache_misses = misses
        checkpoint.embedding_dimensions = dimensions
        if latency is not None:
            embedding_latency_samples += 1
            checkpoint.avg_embedding_seconds = update_rolling_average(
                checkpoint.avg_embedding_seconds,
                latency,
                embedding_latency_samples,
            )
        reporter.update_embeddings(processed=processed, hits=hits, misses=misses, dimensions=dimensions)
        save_checkpoint(files["checkpoint"], checkpoint)

    embeddings, embedding_stats = get_or_create_embeddings(
        nodes,
        config.embedding_model,
        stable_cache_path=stable_cache_path,
        run_cache_path=files["run_embeddings"],
        embed_texts=embed_texts,
        store_text=config.store_embedding_text,
        batch_size=config.embedding_batch_size,
        progress_callback=_embedding_progress,
    )
    logger.info(
        "Embedding cache hits=%d misses=%d dimensions=%s",
        embedding_stats["cache_hits"],
        embedding_stats["cache_misses"],
        embedding_stats["embedding_dimensions"],
    )
    append_progress_event(
        files,
        checkpoint,
        reporter,
        build_progress_event(
            run_id=run_id,
            phase="embedding",
            event_type="phase_completed",
            message="Embedding phase completed",
            counts={
                "embedding_processed": checkpoint.embedding_processed,
                "embedding_cache_hits": embedding_stats["cache_hits"],
                "embedding_cache_misses": embedding_stats["cache_misses"],
            },
        ),
    )

    summary = RunSummary(
        run_id=run_id,
        output_dir=str(output_dir),
        nodes_loaded=len(nodes),
        existing_relationships_loaded=len(relationships),
        embedding_cache_hits=int(embedding_stats["cache_hits"] or 0),
        embedding_cache_misses=int(embedding_stats["cache_misses"] or 0),
        embedding_dimensions=embedding_stats["embedding_dimensions"],
        cloud_usage=council.usage,
        provider_health=council.health,
    )
    for key, value in role_model_metadata(config).items():
        if hasattr(summary, key):
            setattr(summary, key, value)
    summary.progress_mode_effective = config.progress_mode_effective
    if config.resume:
        summary.accepted_count = len(checkpoint.accepted_edge_keys)
        summary.rejected_count = checkpoint.rejected_pair_count
        summary.error_count = checkpoint.error_count

    processed_pair_keys = set(checkpoint.processed_pair_keys)
    schema = RelationshipDecision.model_json_schema()
    verifier_schema = VerificationDecision.model_json_schema()
    checkpoint.phase = "candidate_generation"
    checkpoint.current_operation = "candidate_generation"
    sync_checkpoint_progress(checkpoint, config=config, summary=summary, council=council)
    reporter.set_phase("candidate_generation")
    save_checkpoint(files["checkpoint"], checkpoint)

    try:
        for pair in generate_candidate_pairs(
            nodes,
            embeddings,
            run_id=run_id,
            embedding_model=config.embedding_model,
            candidate_top_k=config.candidate_top_k,
            min_similarity=config.min_similarity,
            max_pairs=config.max_pairs,
            existing_pair_index=existing_pair_index,
            include_existing_pairs=config.include_existing_pairs,
        ):
            if pair.node_pair_key in processed_pair_keys:
                summary.skipped_count += 1
                continue
            summary.candidate_pair_count += 1
            append_jsonl(files["similarity"], pair.to_record())
            checkpoint.candidate_pairs_generated = summary.candidate_pair_count
            checkpoint.current_pair_key = pair.node_pair_key
            checkpoint.current_operation = "candidate_generation"
            reporter.update_candidates(generated=summary.candidate_pair_count)
            append_progress_event(
                files,
                checkpoint,
                reporter,
                build_progress_event(
                    run_id=run_id,
                    phase="candidate_generation",
                    event_type="candidate_generated",
                    message=f"Generated candidate pair {pair.node_pair_key}",
                    pair_key=pair.node_pair_key,
                    counts={"candidate_pairs_generated": summary.candidate_pair_count},
                ),
            )
            node_a = nodes_by_id[pair.node_a_id]
            node_b = nodes_by_id[pair.node_b_id]
            existing_direct_relationships = _direct_relationships_between(
                relationships,
                pair.node_a_id,
                pair.node_b_id,
            )
            prompt = build_judge_prompt(
                node_a=node_a,
                node_b=node_b,
                existing_direct_relationships=existing_direct_relationships,
                similarity=pair.similarity,
                schema=schema,
            )
            decision: RelationshipDecision | None = None
            verifier_decision: VerificationDecision | None = None
            judge_envelope: ProviderEnvelope | None = None
            verifier_envelope: ProviderEnvelope | None = None
            adjudicator_envelope: ProviderEnvelope | None = None
            council_metadata: dict[str, Any] | None = None
            decision_result: dict[str, Any] | None = None
            provider_failover_start = len(council.usage.provider_failover_events)
            pair_started_at = time.monotonic()
            current_prompt = prompt
            try:
                checkpoint.phase = "judging"
                checkpoint.current_operation = "judging"
                reporter.set_phase("judging", pair.node_pair_key)
                append_progress_event(
                    files,
                    checkpoint,
                    reporter,
                    build_progress_event(
                        run_id=run_id,
                        phase="judging",
                        event_type="pair_started",
                        message=f"Started pair {pair.node_pair_key}",
                        pair_key=pair.node_pair_key,
                    ),
                )
                save_checkpoint(files["checkpoint"], checkpoint)
                judge_started_at = time.monotonic()
                judge_envelope = council.judge(prompt, schema)
                checkpoint.avg_judge_seconds = update_rolling_average(
                    checkpoint.avg_judge_seconds,
                    time.monotonic() - judge_started_at,
                    summary.processed_count + 1,
                )
                checkpoint.current_provider = judge_envelope.provider
                checkpoint.current_model = judge_envelope.model
                record_council_response_rejections(
                    files=files,
                    summary=summary,
                    checkpoint=checkpoint,
                    council=council,
                    run_id=run_id,
                    pair=pair,
                )
                checkpoint.effective_judge_provider = judge_envelope.provider
                checkpoint.effective_judge_model = judge_envelope.model
                summary.effective_judge_provider = judge_envelope.provider
                summary.effective_judge_model = judge_envelope.model
                decision = parse_relationship_decision_for_role(judge_envelope.raw_text, "judge", config=config)

                if should_verify_decision(config, decision, pair):
                    checkpoint.phase = "verifying"
                    checkpoint.current_operation = "verifying"
                    reporter.set_phase("verifying", pair.node_pair_key)
                    verifier_prompt = build_verifier_prompt(
                        node_a=node_a,
                        node_b=node_b,
                        judge_decision=decision,
                        schema=verifier_schema,
                    )
                    current_prompt = verifier_prompt
                    verifier_started_at = time.monotonic()
                    verifier_envelope = council.verify(verifier_prompt, verifier_schema)
                    checkpoint.avg_verifier_seconds = update_rolling_average(
                        checkpoint.avg_verifier_seconds,
                        time.monotonic() - verifier_started_at,
                        summary.processed_count + 1,
                    )
                    checkpoint.current_provider = verifier_envelope.provider
                    checkpoint.current_model = verifier_envelope.model
                    record_council_response_rejections(
                        files=files,
                        summary=summary,
                        checkpoint=checkpoint,
                        council=council,
                        run_id=run_id,
                        pair=pair,
                    )
                    checkpoint.effective_verifier_provider = verifier_envelope.provider
                    checkpoint.effective_verifier_model = verifier_envelope.model
                    summary.effective_verifier_provider = verifier_envelope.provider
                    summary.effective_verifier_model = verifier_envelope.model
                    verifier_decision = parse_verification_decision_for_role(verifier_envelope.raw_text, "verifier")
                    if should_adjudicate_decision(config, decision, verifier_decision):
                        checkpoint.phase = "adjudicating"
                        checkpoint.current_operation = "adjudicating"
                        reporter.set_phase("adjudicating", pair.node_pair_key)
                        adjudicator_prompt = build_adjudicator_prompt(
                            node_a=node_a,
                            node_b=node_b,
                            judge_decision=decision,
                            verifier_decision=verifier_decision,
                            schema=schema,
                        )
                        current_prompt = adjudicator_prompt
                        adjudicator_started_at = time.monotonic()
                        adjudicator_envelope = council.adjudicate(adjudicator_prompt, schema)
                        checkpoint.avg_adjudicator_seconds = update_rolling_average(
                            checkpoint.avg_adjudicator_seconds,
                            time.monotonic() - adjudicator_started_at,
                            summary.processed_count + 1,
                        )
                        checkpoint.current_provider = adjudicator_envelope.provider
                        checkpoint.current_model = adjudicator_envelope.model
                        record_council_response_rejections(
                            files=files,
                            summary=summary,
                            checkpoint=checkpoint,
                            council=council,
                            run_id=run_id,
                            pair=pair,
                        )
                        checkpoint.effective_adjudicator_provider = adjudicator_envelope.provider
                        checkpoint.effective_adjudicator_model = adjudicator_envelope.model
                        summary.effective_adjudicator_provider = adjudicator_envelope.provider
                        summary.effective_adjudicator_model = adjudicator_envelope.model
                        decision = parse_relationship_decision_for_role(adjudicator_envelope.raw_text, "adjudicator", config=config)
                    if verifier_decision.agrees or verifier_decision.corrected_confidence >= config.accept_threshold:
                        final_decision = _verification_to_relationship_decision(decision, verifier_decision)
                    else:
                        council_metadata = build_council_metadata(
                            config=config,
                            usage=council.usage,
                            judge=judge_envelope,
                            verifier=verifier_envelope,
                            adjudicator=adjudicator_envelope,
                        )
                        append_jsonl(
                            files["rejected"],
                            build_rejected_record(
                                run_id=run_id,
                                pair=pair,
                                reason="verifier_disagreed",
                                judge_decision=decision,
                                verifier_decision=verifier_decision,
                                error=None,
                                council_metadata=council_metadata,
                            ),
                        )
                        _rejection(summary, "verifier_disagreed")
                        decision_result = {"result_type": "rejected", "reason": "verifier_disagreed"}
                        final_decision = None
                    if final_decision is not None:
                        council_metadata = build_council_metadata(
                            config=config,
                            usage=council.usage,
                            judge=judge_envelope,
                            verifier=verifier_envelope,
                            adjudicator=adjudicator_envelope,
                        )
                        decision_result = _maybe_accept_or_record(
                            config=config,
                            files=files,
                            summary=summary,
                            checkpoint=checkpoint,
                            pair=pair,
                            node_a=node_a,
                            node_b=node_b,
                            decision=decision,
                            existing_edge_keys=existing_edge_keys,
                            verifier_decision=verifier_decision,
                            final_decision=final_decision,
                            council_metadata=council_metadata,
                        )
                else:
                    council_metadata = build_council_metadata(
                        config=config,
                        usage=council.usage,
                        judge=judge_envelope,
                    )
                    decision_result = _maybe_accept_or_record(
                        config=config,
                        files=files,
                        summary=summary,
                        checkpoint=checkpoint,
                        pair=pair,
                        node_a=node_a,
                        node_b=node_b,
                        decision=decision,
                        existing_edge_keys=existing_edge_keys,
                        verifier_decision=None,
                        council_metadata=council_metadata,
                    )
                summary.processed_count += 1
            except CloudResponseRejectedError as exc:
                council_metadata = build_council_metadata(
                    config=config,
                    usage=council.usage,
                    judge=judge_envelope,
                    verifier=verifier_envelope,
                    adjudicator=adjudicator_envelope,
                )
                role = role_from_operation(checkpoint.current_operation)
                validation_record = record_validation_error(
                    files=files,
                    summary=summary,
                    checkpoint=checkpoint,
                    record=validation_error_record_from_exception(
                        run_id=run_id,
                        pair=pair,
                        exc=exc,
                        role=role,
                        envelope=envelope_for_role(role, judge_envelope, verifier_envelope, adjudicator_envelope),
                        prompt=current_prompt,
                    ),
                )
                append_jsonl(
                    files["rejected"],
                    build_rejected_record(
                        run_id=run_id,
                        pair=pair,
                        reason=exc.reason,
                        judge_decision=decision,
                        verifier_decision=verifier_decision,
                        error=str(exc),
                        council_metadata=council_metadata,
                        validation_error_record=validation_record,
                    ),
                )
                _rejection(summary, exc.reason)
                decision_result = {"result_type": "rejected", "reason": exc.reason}
                summary.processed_count += 1
            except BlockedPredicateError as exc:
                if council_metadata is None:
                    council_metadata = build_council_metadata(
                        config=config,
                        usage=council.usage,
                        judge=judge_envelope,
                        verifier=verifier_envelope,
                        adjudicator=adjudicator_envelope,
                    )
                append_jsonl(
                    files["rejected"],
                    build_rejected_record(
                        run_id=run_id,
                        pair=pair,
                        reason="blocked_predicate",
                        judge_decision=decision,
                        verifier_decision=verifier_decision,
                        error=str(exc),
                        council_metadata=council_metadata,
                    ),
                )
                _rejection(summary, "blocked_predicate")
                decision_result = {"result_type": "rejected", "reason": "blocked_predicate"}
                summary.processed_count += 1
            except MalformedModelJSONError as exc:
                if council_metadata is None:
                    council_metadata = build_council_metadata(
                        config=config,
                        usage=council.usage,
                        judge=judge_envelope,
                        verifier=verifier_envelope,
                        adjudicator=adjudicator_envelope,
                    )
                role = role_from_operation(checkpoint.current_operation)
                validation_record = record_validation_error(
                    files=files,
                    summary=summary,
                    checkpoint=checkpoint,
                    record=validation_error_record_from_exception(
                        run_id=run_id,
                        pair=pair,
                        exc=exc,
                        role=role,
                        envelope=envelope_for_role(role, judge_envelope, verifier_envelope, adjudicator_envelope),
                        prompt=current_prompt,
                    ),
                )
                append_jsonl(
                    files["rejected"],
                    build_rejected_record(
                        run_id=run_id,
                        pair=pair,
                        reason="malformed_json",
                        judge_decision=decision,
                        verifier_decision=verifier_decision,
                        error=str(exc),
                        council_metadata=council_metadata,
                        validation_error_record=validation_record,
                    ),
                )
                _rejection(summary, "malformed_json")
                decision_result = {"result_type": "rejected", "reason": "malformed_json"}
                summary.processed_count += 1
            except RoleValidationError as exc:
                if council_metadata is None:
                    council_metadata = build_council_metadata(
                        config=config,
                        usage=council.usage,
                        judge=judge_envelope,
                        verifier=verifier_envelope,
                        adjudicator=adjudicator_envelope,
                    )
                role = exc.role or role_from_operation(checkpoint.current_operation)
                validation_record = record_validation_error(
                    files=files,
                    summary=summary,
                    checkpoint=checkpoint,
                    record=validation_error_record_from_exception(
                        run_id=run_id,
                        pair=pair,
                        exc=exc,
                        role=role,
                        envelope=envelope_for_role(role, judge_envelope, verifier_envelope, adjudicator_envelope),
                        prompt=current_prompt,
                    ),
                )
                append_jsonl(
                    files["rejected"],
                    build_rejected_record(
                        run_id=run_id,
                        pair=pair,
                        reason=exc.reason,
                        judge_decision=decision,
                        verifier_decision=verifier_decision,
                        error=str(exc),
                        council_metadata=council_metadata,
                        validation_error_record=validation_record,
                    ),
                )
                _rejection(summary, exc.reason)
                decision_result = {"result_type": "rejected", "reason": exc.reason}
                summary.processed_count += 1
            except (UnsafeDecisionError, ValidationError) as exc:
                append_jsonl(
                    files["rejected"],
                    build_rejected_record(
                        run_id=run_id,
                        pair=pair,
                        reason="validation_error",
                        judge_decision=decision,
                        verifier_decision=verifier_decision,
                        error=str(exc),
                        council_metadata=council_metadata,
                    ),
                )
                _rejection(summary, "validation_error")
                decision_result = {"result_type": "rejected", "reason": "validation_error"}
                summary.processed_count += 1
            except Exception as exc:
                summary.error_count += 1
                checkpoint.error_count += 1
                append_jsonl(
                    files["errors"],
                    {
                        "schema_version": "aec-relationship-improvement-error/v1",
                        "run_id": run_id,
                        "node_pair_key": pair.node_pair_key,
                        "node_a_id": pair.node_a_id,
                        "node_b_id": pair.node_b_id,
                        "error": truncate_error_text(str(exc)),
                        "traceback": truncate_error_text(traceback.format_exc(), 1200),
                        "council_mode": config.council_mode,
                        "provider_route": (council_metadata or {}).get("provider_route", []),
                        "created_at_utc": utc_now(),
                    },
                )
                logger.exception("Error processing pair %s", pair.node_pair_key)
                decision_result = {"result_type": "error", "reason": str(exc)}
            finally:
                if decision_result:
                    reporter.update_decision(
                        _as_text(decision_result.get("result_type")),
                        edge_key=decision_result.get("edge_key"),
                        reason=decision_result.get("reason"),
                        confidence=decision_result.get("confidence"),
                    )
                    append_progress_event(
                        files,
                        checkpoint,
                        reporter,
                        build_progress_event(
                            run_id=run_id,
                            phase=checkpoint.phase,
                            event_type=_as_text(decision_result.get("result_type")) or "pair_completed",
                            message=f"{decision_result.get('result_type')} {pair.node_pair_key}",
                            pair_key=pair.node_pair_key,
                            edge_key=decision_result.get("edge_key"),
                            confidence=decision_result.get("confidence"),
                            reason=decision_result.get("reason"),
                            counts={
                                "accepted": summary.accepted_count,
                                "needs_review": summary.candidate_review_count,
                                "rejected": summary.rejected_count,
                                "errors": summary.error_count,
                            },
                        ),
                    )
                for failover_event in council.usage.provider_failover_events[provider_failover_start:]:
                    append_progress_event(
                        files,
                        checkpoint,
                        reporter,
                        build_progress_event(
                            run_id=run_id,
                            phase=checkpoint.phase,
                            event_type="provider_failover",
                            message=f"Provider failover: {failover_event.get('provider')} {failover_event.get('reason')}",
                            pair_key=pair.node_pair_key,
                            provider=failover_event.get("provider"),
                            model=failover_event.get("model"),
                            reason=failover_event.get("reason"),
                        ),
                    )
                reporter.update_cloud_usage(council.usage)
                reporter.update_provider_health(council.health)
                reporter.update_pair_processed(
                    pair.node_pair_key,
                    _as_text((decision_result or {}).get("result_type")) or "processed",
                    (council_metadata or {}).get("provider_route", []),
                )
                processed_pair_keys.add(pair.node_pair_key)
                checkpoint.processed_pair_keys = sorted(processed_pair_keys)
                checkpoint.rejected_pair_count = summary.rejected_count
                checkpoint.rejected_count = summary.rejected_count
                checkpoint.accepted_count = summary.accepted_count
                checkpoint.candidate_count = summary.candidate_review_count
                checkpoint.processed_pair_count = summary.processed_count
                checkpoint.cloud_usage = council.usage
                checkpoint.provider_health = council.health
                checkpoint.last_provider_used = (council_metadata or {}).get("judge_provider")
                checkpoint.current_operation = "sleep"
                pair_elapsed = time.monotonic() - pair_started_at
                if pair_elapsed > 0 and summary.processed_count > 0:
                    checkpoint.pairs_per_minute = round(summary.processed_count / max(0.001, seconds_since_utc(checkpoint.started_at_utc) or pair_elapsed) * 60, 3)
                sync_checkpoint_progress(checkpoint, config=config, summary=summary, council=council)
                save_checkpoint(files["checkpoint"], checkpoint)
    except KeyboardInterrupt:
        checkpoint.status = "interrupted"
        checkpoint.phase = "interrupted"
        sync_checkpoint_progress(checkpoint, config=config, summary=summary, council=council)
        save_checkpoint(files["checkpoint"], checkpoint)
        reporter.close()
        logger.warning("Interrupted; checkpoint marked interrupted")
        print(
            "\nInterrupted safely.\n"
            "Pending artifacts are preserved at:\n"
            f"{output_dir}\n\n"
            "Resume with:\n"
            f"PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships --resume --run-id {run_id}\n\n"
            "Watch with:\n"
            f"PYTHONPATH=scripts python scripts/pipeline_cli.py aec-watch-relationship-run --run-id {run_id}\n",
            file=sys.stderr,
        )
        raise

    checkpoint.status = "in_progress"
    checkpoint.phase = "writing_report"
    reporter.set_phase("writing_report")
    checkpoint.rejected_pair_count = summary.rejected_count
    checkpoint.error_count = summary.error_count
    checkpoint.cloud_usage = council.usage
    checkpoint.provider_health = council.health
    sync_checkpoint_progress(checkpoint, config=config, summary=summary, council=council)
    summary.cloud_usage = council.usage
    summary.provider_health = council.health
    summary.hierarchy_normalization_count = checkpoint.hierarchy_normalization_count
    summary.taxonomy_part_of_conversion_count = checkpoint.taxonomy_part_of_conversion_count
    summary.validation_guard_downgrade_count = checkpoint.validation_guard_downgrade_count
    summary.avg_judge_seconds = checkpoint.avg_judge_seconds
    summary.avg_verifier_seconds = checkpoint.avg_verifier_seconds
    summary.avg_adjudicator_seconds = checkpoint.avg_adjudicator_seconds
    summary.pairs_per_minute = checkpoint.pairs_per_minute
    summary.elapsed_seconds = round(seconds_since_utc(checkpoint.started_at_utc) or checkpoint.elapsed_seconds, 3)
    summary.progress_mode_effective = config.progress_mode_effective
    summary.recommendations = build_next_run_recommendations(summary, config)
    write_review_tsvs(files)
    write_summary_text(files, summary, config)
    save_checkpoint(files["checkpoint"], checkpoint)
    write_json(files["report"], summary.to_record())
    checkpoint.status = "completed"
    checkpoint.phase = "completed"
    save_checkpoint(files["checkpoint"], checkpoint)
    append_progress_event(
        files,
        checkpoint,
        reporter,
        build_progress_event(
            run_id=run_id,
            phase="completed",
            event_type="summary",
            message="Run completed",
            counts=summary.to_record(),
        ),
    )
    save_checkpoint(files["checkpoint"], checkpoint)
    reporter.set_phase("completed")
    reporter.finish(summary)
    reporter.close()
    logger.info("Candidate pairs generated: %d", summary.candidate_pair_count)
    logger.info("Rejection counts by reason: %s", summary.rejection_counts)
    logger.info(
        "Run completed: processed=%d skipped=%d accepted=%d candidates=%d rejected=%d errors=%d",
        summary.processed_count,
        summary.skipped_count,
        summary.accepted_count,
        summary.candidate_review_count,
        summary.rejected_count,
        summary.error_count,
    )
    return summary


def _config_for_logging(config: RunConfig) -> dict[str, Any]:
    data = config.__dict__.copy()
    for key, value in list(data.items()):
        if isinstance(value, Path):
            data[key] = str(value)
    return data


def default_stable_embedding_cache_path(embedding_model: str) -> Path:
    return (
        Path("005_Operational-Intelligence-Layer")
        / "embeddings"
        / "aec-mepfs-backbone"
        / safe_model_name(embedding_model)
        / "node-embeddings.jsonl"
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Propose pending AEC Backbone relationship improvements.")
    add_cli_arguments(parser)
    return parser


def add_cli_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-nodes", type=int, default=1000)
    parser.add_argument("--max-pairs", type=int, default=5000)
    parser.add_argument("--candidate-top-k", type=int, default=20)
    parser.add_argument("--min-similarity", type=float, default=0.35)
    parser.add_argument("--accept-threshold", type=float, default=0.85)
    parser.add_argument("--verify-threshold", type=float, default=0.65)
    parser.add_argument("--verify-uncertain", action="store_true")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--verifier-model", default=DEFAULT_VERIFIER_MODEL)
    parser.add_argument("--ollama-base-url", default=DEFAULT_OLLAMA_BASE_URL)
    parser.add_argument("--sleep-seconds", type=float, default=2.0)
    parser.add_argument("--verifier-sleep-seconds", type=float, default=3.0)
    parser.add_argument("--embedding-batch-size", type=int, default=1)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument("--num-predict", type=int, default=500)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--think", action="store_true")
    parser.add_argument("--include-existing-pairs", action="store_true")
    parser.add_argument("--store-embedding-text", action="store_true")
    parser.add_argument("--stable-embedding-cache", type=Path, default=None)
    parser.add_argument("--no-stable-embedding-cache", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-cloud-ai", action="store_true")
    parser.add_argument("--council-mode", choices=COUNCIL_MODES, default="local_only")
    parser.add_argument("--cloud-cost-budget-usd", type=float, default=None)
    parser.add_argument("--cloud-total-max-calls", type=int, default=None)
    parser.add_argument("--cloud-timeout-seconds", type=int, default=120)
    parser.add_argument("--cloud-max-retries", type=int, default=2)
    parser.add_argument("--cloud-backoff-seconds", type=float, default=10.0)
    parser.add_argument("--cloud-circuit-breaker-failures", type=int, default=3)
    parser.add_argument("--cloud-redact-fields", default="")
    parser.add_argument("--judge-provider", choices=PROVIDER_CHOICES, default="auto")
    parser.add_argument("--verifier-provider", choices=PROVIDER_CHOICES, default="auto")
    parser.add_argument("--adjudicator-provider", choices=ADJUDICATOR_PROVIDER_CHOICES, default="none")
    parser.add_argument("--kimi-base-url", default=DEFAULT_KIMI_BASE_URL)
    parser.add_argument("--kimi-model", default=DEFAULT_KIMI_MODEL)
    parser.add_argument("--kimi-api-key-env", default=DEFAULT_KIMI_API_KEY_ENV)
    parser.add_argument("--kimi-disable-thinking", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--kimi-max-tokens", type=int, default=700)
    parser.add_argument("--kimi-sleep-seconds", type=float, default=2.0)
    parser.add_argument("--kimi-max-calls", type=int, default=None)
    parser.add_argument("--kimi-estimated-cost-per-call-usd", type=float, default=0.0)
    parser.add_argument("--kimi-verify-accepted-sample-rate", type=float, default=0.25)
    parser.add_argument("--kimi-verify-uncertain", action="store_true", default=None)
    parser.add_argument("--allow-custom-kimi-base-url", action="store_true")
    parser.add_argument(
        "--enable-kimi-experimental",
        action="store_true",
        help="Deprecated/experimental. Kimi Code chat completion is not recommended for this workflow.",
    )
    parser.add_argument("--deepseek-base-url", default=DEFAULT_DEEPSEEK_BASE_URL)
    parser.add_argument("--deepseek-flash-model", default=DEFAULT_DEEPSEEK_FLASH_MODEL)
    parser.add_argument("--deepseek-pro-model", default=DEFAULT_DEEPSEEK_PRO_MODEL)
    parser.add_argument("--deepseek-api-key-env", default=DEFAULT_DEEPSEEK_API_KEY_ENV)
    parser.add_argument("--deepseek-disable-thinking", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--deepseek-reasoning-effort", choices=["high", "max"], default="high")
    parser.add_argument("--deepseek-max-tokens", type=int, default=700)
    parser.add_argument("--deepseek-sleep-seconds", type=float, default=1.0)
    parser.add_argument("--deepseek-flash-max-calls", type=int, default=None)
    parser.add_argument("--deepseek-pro-max-calls", type=int, default=None)
    parser.add_argument("--deepseek-flash-call-buffer", type=float, default=0.50)
    parser.add_argument("--allow-custom-deepseek-base-url", action="store_true")
    parser.add_argument("--cloud-preflight", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--deepseek-retry-truncated-json", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--hierarchy-canonical-predicate", choices=HIERARCHY_CANONICAL_PREDICATES, default="broader_than")
    parser.add_argument("--convert-taxonomy-part-of", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--enable-safe-schema-repair", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--schema-repair-acceptance-policy",
        choices=["needs_review_only", "allow_accept_after_final_guard"],
        default="needs_review_only",
    )
    parser.add_argument("--verify-accepted-cloud", action="store_true", default=None)
    parser.add_argument("--verify-accepted-sample-rate", type=float, default=0.25)
    parser.add_argument("--adjudicate-disagreements", action="store_true", default=None)
    parser.add_argument("--high-impact-pro-adjudication", action="store_true", default=True)
    parser.add_argument("--fallback-to-local-on-cloud-exhaustion", action="store_true", default=True)
    parser.add_argument("--fallback-to-local-on-cloud-error", action="store_true", default=True)
    parser.add_argument("--fallback-to-local-on-rate-limit", action="store_true", default=True)
    parser.add_argument("--stop-on-cloud-auth-error", action="store_true")
    parser.add_argument("--strict-cloud-only", action="store_true")
    parser.add_argument("--reset-cloud-budget-for-resume", action="store_true")
    parser.add_argument("--progress-mode", choices=PROGRESS_MODES, default="auto")
    parser.add_argument("--progress-refresh-per-second", type=float, default=2.0)
    parser.add_argument("--progress-log-every-seconds", type=float, default=30.0)
    parser.add_argument("--progress-show-recent", type=int, default=8)
    parser.add_argument("--progress-transient", action="store_true")
    parser.add_argument("--no-progress", dest="progress_mode", action="store_const", const="off")
    parser.add_argument("--force-rich-in-git-bash", action="store_true")
    parser.add_argument("--watch-run", default=None)


def config_from_args(args: argparse.Namespace) -> RunConfig:
    stable_cache = args.stable_embedding_cache
    if stable_cache is None and not args.no_stable_embedding_cache:
        stable_cache = default_stable_embedding_cache_path(args.embedding_model)
    return RunConfig(
        input_path=args.input_path,
        output_root=args.output_root,
        run_id=args.run_id,
        dry_run=args.dry_run,
        resume=args.resume,
        max_nodes=args.max_nodes,
        max_pairs=args.max_pairs,
        candidate_top_k=args.candidate_top_k,
        min_similarity=args.min_similarity,
        accept_threshold=args.accept_threshold,
        verify_threshold=args.verify_threshold,
        verify_uncertain=args.verify_uncertain,
        embedding_model=args.embedding_model,
        judge_model=args.judge_model,
        verifier_model=args.verifier_model,
        ollama_base_url=args.ollama_base_url,
        sleep_seconds=args.sleep_seconds,
        verifier_sleep_seconds=args.verifier_sleep_seconds,
        embedding_batch_size=args.embedding_batch_size,
        num_ctx=args.num_ctx,
        num_predict=args.num_predict,
        temperature=args.temperature,
        think=args.think,
        include_existing_pairs=args.include_existing_pairs,
        store_embedding_text=args.store_embedding_text,
        stable_embedding_cache_path=stable_cache,
        no_stable_embedding_cache=args.no_stable_embedding_cache,
        apply=args.apply,
        allow_cloud_ai=args.allow_cloud_ai,
        council_mode=args.council_mode,
        cloud_cost_budget_usd=args.cloud_cost_budget_usd,
        cloud_total_max_calls=args.cloud_total_max_calls,
        cloud_timeout_seconds=args.cloud_timeout_seconds,
        cloud_max_retries=args.cloud_max_retries,
        cloud_backoff_seconds=args.cloud_backoff_seconds,
        cloud_circuit_breaker_failures=args.cloud_circuit_breaker_failures,
        cloud_redact_fields=tuple(
            item.strip() for item in (args.cloud_redact_fields or "").split(",") if item.strip()
        ),
        judge_provider=args.judge_provider,
        verifier_provider=args.verifier_provider,
        adjudicator_provider=args.adjudicator_provider,
        kimi_base_url=args.kimi_base_url,
        kimi_model=args.kimi_model,
        kimi_api_key_env=args.kimi_api_key_env,
        kimi_disable_thinking=args.kimi_disable_thinking,
        kimi_max_tokens=args.kimi_max_tokens,
        kimi_sleep_seconds=args.kimi_sleep_seconds,
        kimi_max_calls=args.kimi_max_calls,
        kimi_estimated_cost_per_call_usd=args.kimi_estimated_cost_per_call_usd,
        kimi_verify_accepted_sample_rate=args.kimi_verify_accepted_sample_rate,
        kimi_verify_uncertain=args.kimi_verify_uncertain,
        allow_custom_kimi_base_url=args.allow_custom_kimi_base_url,
        enable_kimi_experimental=args.enable_kimi_experimental,
        deepseek_base_url=args.deepseek_base_url,
        deepseek_flash_model=args.deepseek_flash_model,
        deepseek_pro_model=args.deepseek_pro_model,
        deepseek_api_key_env=args.deepseek_api_key_env,
        deepseek_disable_thinking=args.deepseek_disable_thinking,
        deepseek_reasoning_effort=args.deepseek_reasoning_effort,
        deepseek_max_tokens=args.deepseek_max_tokens,
        deepseek_sleep_seconds=args.deepseek_sleep_seconds,
        deepseek_flash_max_calls=args.deepseek_flash_max_calls,
        deepseek_pro_max_calls=args.deepseek_pro_max_calls,
        deepseek_flash_call_buffer=args.deepseek_flash_call_buffer,
        allow_custom_deepseek_base_url=args.allow_custom_deepseek_base_url,
        cloud_preflight=args.cloud_preflight,
        deepseek_retry_truncated_json=args.deepseek_retry_truncated_json,
        hierarchy_canonical_predicate=args.hierarchy_canonical_predicate,
        convert_taxonomy_part_of=args.convert_taxonomy_part_of,
        enable_safe_schema_repair=args.enable_safe_schema_repair,
        schema_repair_acceptance_policy=args.schema_repair_acceptance_policy,
        verify_accepted_cloud=args.verify_accepted_cloud,
        verify_accepted_sample_rate=args.verify_accepted_sample_rate,
        adjudicate_disagreements=args.adjudicate_disagreements,
        high_impact_pro_adjudication=args.high_impact_pro_adjudication,
        fallback_to_local_on_cloud_exhaustion=args.fallback_to_local_on_cloud_exhaustion,
        fallback_to_local_on_cloud_error=args.fallback_to_local_on_cloud_error,
        fallback_to_local_on_rate_limit=args.fallback_to_local_on_rate_limit,
        stop_on_cloud_auth_error=args.stop_on_cloud_auth_error,
        strict_cloud_only=args.strict_cloud_only,
        reset_cloud_budget_for_resume=args.reset_cloud_budget_for_resume,
        progress_mode=args.progress_mode,
        progress_refresh_per_second=args.progress_refresh_per_second,
        progress_log_every_seconds=args.progress_log_every_seconds,
        progress_show_recent=args.progress_show_recent,
        progress_transient=args.progress_transient,
        force_rich_in_git_bash=args.force_rich_in_git_bash,
        watch_run=args.watch_run,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = config_from_args(args)
        ensure_apply_mode_is_deferred(config.apply)
        if config.watch_run:
            watch_target = Path(config.watch_run)
            watch_config = WatchRunConfig(
                run_id=None if watch_target.exists() or any(sep in config.watch_run for sep in ("/", "\\")) else config.watch_run,
                output_root=config.output_root,
                output_dir=watch_target if watch_target.exists() or any(sep in config.watch_run for sep in ("/", "\\")) else None,
                progress_mode=config.progress_mode,
                refresh_seconds=max(0.1, 1.0 / max(config.progress_refresh_per_second, 0.1)),
                show_recent=config.progress_show_recent,
                force_rich_in_git_bash=config.force_rich_in_git_bash,
            )
            return watch_relationship_run(watch_config)
        summary = run_relationship_improvement(config)
    except ApplyModeDeferredError as exc:
        parser.error(str(exc))
        return 2
    except RuntimeError as exc:
        parser.error(str(exc))
        return 2
    except KeyboardInterrupt:
        return 130
    print(json.dumps(summary.to_record(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
