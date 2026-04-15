"""Stream S1.2 — pyo3 bridge to the Rust Datalog evaluator.

These tests pin the public API of ``vitruvius_datalog_rs.evaluate_datalog``
and exercise the hardcoded PD 1096 setback compliance ruleset:

    violates(B, R) :-
        has_distance(B, D_actual),
        requires_distance(R, D_required),
        less_than(D_actual, D_required),
        applies_to(R, B).

If the Rust wheel has not been built, ``pytest.importorskip`` skips
the module cleanly so the pure-Python test suite stays green on
machines without a Rust toolchain.
"""

from __future__ import annotations

import pytest

datalog_rs = pytest.importorskip(
    "vitruvius_datalog_rs",
    reason="vitruvius_datalog_rs Rust extension not built — "
    "run `maturin build --release` in scripts/vitruvius/datalog_rs/",
)


def test_module_exposes_evaluate_datalog() -> None:
    assert hasattr(datalog_rs, "evaluate_datalog")
    assert callable(datalog_rs.evaluate_datalog)


def test_module_exposes_version_string() -> None:
    assert isinstance(datalog_rs.__version__, str)
    assert datalog_rs.__version__.count(".") >= 1


def test_evaluate_datalog_accepts_violating_fact_set() -> None:
    facts = [
        "has_distance(building_42, 1_8)",
        "requires_distance(setback_rule_3, 2_0)",
        "less_than(1_8, 2_0)",
        "applies_to(setback_rule_3, building_42)",
    ]
    assert datalog_rs.evaluate_datalog(facts) is True


def test_evaluate_datalog_rejects_compliant_fact_set() -> None:
    facts = [
        "has_distance(building_42, 2_5)",
        "requires_distance(setback_rule_3, 2_0)",
        "less_than(1_8, 2_0)",
        "applies_to(setback_rule_3, building_42)",
    ]
    assert datalog_rs.evaluate_datalog(facts) is False


def test_evaluate_datalog_requires_applies_to_edge() -> None:
    """Without applies_to the rule body fails to join — no violation."""
    facts = [
        "has_distance(building_42, 1_8)",
        "requires_distance(setback_rule_3, 2_0)",
        "less_than(1_8, 2_0)",
        # applies_to deliberately missing
    ]
    assert datalog_rs.evaluate_datalog(facts) is False


def test_evaluate_datalog_rejects_malformed_fact() -> None:
    with pytest.raises(ValueError):
        datalog_rs.evaluate_datalog(["not a datalog fact"])


def test_evaluate_datalog_rejects_empty_predicate() -> None:
    with pytest.raises(ValueError):
        datalog_rs.evaluate_datalog(["(a, b)"])


def test_evaluate_datalog_empty_fact_set_is_false() -> None:
    """No facts → no derivable violations → False."""
    assert datalog_rs.evaluate_datalog([]) is False


def test_evaluate_datalog_accepts_optional_rules_arg() -> None:
    """The `rules` positional is reserved for the future crepe path.

    It is currently accepted (for forward-compat with the plan) but the
    hand-rolled evaluator ignores its contents. Verify callers can pass
    it without blowing up.
    """
    facts = [
        "has_distance(b, 1)",
        "requires_distance(r, 2)",
        "less_than(1, 2)",
        "applies_to(r, b)",
    ]
    assert datalog_rs.evaluate_datalog(facts, ["future_rule(X) :- _"]) is True
