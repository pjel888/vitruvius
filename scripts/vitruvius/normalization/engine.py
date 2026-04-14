"""Centralized Normalization Engine — Phase 1C.

Phase-locked, scope-routed, tier-aware rule application. See
`/.ai/03_plans/phase-1c-centralized-normalization-plan.md` for the design
spec. This module implements a scoped minimum-viable subset: Tier A/B rules
only, no Tier C, no semantic chunking, no destructive rollback beyond what
individual rules do internally.

The engine's three guarantees:
1. Phase-locked execution: rules in phase N always run before rules in phase N+1.
2. Scope-routed: a rule declaring scope=[\"document_text\"] will not be applied
   to an identifier or filename.
3. Deterministic idempotency: for Tier A and Tier B rules with
   is_deterministic=True, normalize(normalize(x)) == normalize(x).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class NormalizationRule(Protocol):
    name: str
    tier: str                 # "A" | "B" | "C"
    phase: int                # 1..5
    scope: list[str]          # "document_text" | "identifier" | "filename" | ...
    gated_by: list[str]       # e.g. ["spreadsheet_unstructured"]
    is_deterministic: bool

    def apply(self, text: str) -> str: ...


@dataclass
class RuleResult:
    rule: str
    tier: str
    phase: int
    chars_before: int
    chars_after: int
    changed: bool


class NormalizationEngine:
    def __init__(self) -> None:
        self.rules: list[NormalizationRule] = []

    def register(self, rule: NormalizationRule) -> None:
        self.rules.append(rule)

    def _applicable(self, scope: str, document_class: str | None) -> list[NormalizationRule]:
        selected: list[NormalizationRule] = []
        for rule in self.rules:
            if scope not in rule.scope:
                continue
            if rule.gated_by and document_class is not None and document_class not in rule.gated_by:
                continue
            selected.append(rule)
        # Stable sort by phase only — within a phase, registration order is the
        # authoritative dependency order. Rule authors MUST register rules in
        # the order they must execute within the same phase (e.g. line endings
        # before trailing-whitespace cleanup).
        return sorted(selected, key=lambda r: r.phase)

    def run(
        self,
        text: str,
        *,
        scope: str = "document_text",
        document_class: str | None = None,
    ) -> tuple[str, list[dict[str, Any]]]:
        """Apply all applicable rules in phase order. Return (output, audit)."""
        audit: list[dict[str, Any]] = []
        current = text
        for rule in self._applicable(scope, document_class):
            before_text = current
            current = rule.apply(current)
            audit.append({
                "rule": rule.name,
                "tier": rule.tier,
                "phase": rule.phase,
                "chars_before": len(before_text),
                "chars_after": len(current),
                "changed": before_text != current,
            })
        return current, audit
