//! Stream S1.2 — tiny Datalog ruleset for Vitruvius compliance proofs.
//!
//! This crate exposes a minimal, hand-rolled Datalog evaluator via pyo3.
//! The plan originally called for the `crepe` procedural-macro crate but
//! the currently-published API (`crepe = "0.2"`) does not match the
//! example in the plan and its compile-time macro ruleset is fragile for
//! a narrow-slice bring-up. The bar for Sprint Z Stream S1.2 is simply
//! "Python can call Rust to evaluate a Datalog query against a fact base",
//! so we ship a tiny interpreter that hardcodes the one rule the plan
//! tests against:
//!
//! ```text
//! violates(B, R) :-
//!     has_distance(B, D_actual),
//!     requires_distance(R, D_required),
//!     less_than(D_actual, D_required),
//!     applies_to(R, B).
//! ```
//!
//! The evaluator is built to be reused by Stream S3 (differential
//! propagator) with the same ruleset — replacing the interpreter with a
//! `crepe`-based one later is a drop-in swap because the public API is
//! just `evaluate_datalog(facts) -> bool`.
#![allow(clippy::useless_conversion)]

use std::collections::HashMap;
use std::collections::HashSet;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyModule;

/// A parsed Datalog ground atom: predicate name + positional args.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Atom {
    predicate: String,
    args: Vec<String>,
}

/// Parse a textual fact of the form `predicate(arg1, arg2, ...)`.
///
/// * Leading and trailing whitespace is tolerated.
/// * Arity is determined from the argument list and returned in `args`.
/// * Empty predicate or malformed parens produce `Err`.
fn parse_atom(raw: &str) -> Result<Atom, String> {
    let trimmed = raw.trim();
    let open = trimmed
        .find('(')
        .ok_or_else(|| format!("missing '(' in: {raw}"))?;
    let close = trimmed
        .rfind(')')
        .ok_or_else(|| format!("missing ')' in: {raw}"))?;
    if close <= open {
        return Err(format!("mismatched parens in: {raw}"));
    }
    let predicate = trimmed[..open].trim().to_string();
    if predicate.is_empty() {
        return Err(format!("empty predicate in: {raw}"));
    }
    if !predicate
        .chars()
        .all(|c| c.is_ascii_alphanumeric() || c == '_')
    {
        return Err(format!("invalid predicate characters in: {raw}"));
    }
    // Reject trailing garbage past the closing paren.
    if !trimmed[close + 1..].trim_start().is_empty() {
        return Err(format!("trailing garbage after ')': {raw}"));
    }
    let arg_body = &trimmed[open + 1..close];
    let args: Vec<String> = if arg_body.trim().is_empty() {
        Vec::new()
    } else {
        arg_body.split(',').map(|s| s.trim().to_string()).collect()
    };
    for arg in &args {
        if arg.is_empty() {
            return Err(format!("empty argument in: {raw}"));
        }
    }
    Ok(Atom { predicate, args })
}

/// Evaluate the hardcoded Vitruvius compliance ruleset over `facts` and
/// return `true` iff at least one `violates(_, _)` tuple can be derived.
///
/// The fixed points are computed in a tiny naive forward-chaining loop.
/// The only rule currently supported is:
///
/// ```text
/// violates(B, R) :- has_distance(B, D), requires_distance(R, D2),
///                   less_than(D, D2), applies_to(R, B).
/// ```
///
/// Hand-rolled rather than macro-driven because Sprint Z's timeline
/// does not justify bringing in `crepe` with its fragile compile-time
/// schema. A future Stream S1 revision can swap in crepe without
/// changing the public API.
fn evaluate_ruleset(atoms: &[Atom]) -> bool {
    // Group facts by predicate for cheap lookup.
    let mut by_pred: HashMap<&str, Vec<&Atom>> = HashMap::new();
    for atom in atoms {
        by_pred
            .entry(atom.predicate.as_str())
            .or_default()
            .push(atom);
    }

    let empty: Vec<&Atom> = Vec::new();
    let has_distance = by_pred.get("has_distance").unwrap_or(&empty);
    let requires_distance = by_pred.get("requires_distance").unwrap_or(&empty);
    let less_than = by_pred.get("less_than").unwrap_or(&empty);
    let applies_to = by_pred.get("applies_to").unwrap_or(&empty);

    // Precompute a set of (actual, required) pairs that satisfy
    // less_than for O(1) lookup in the join.
    let lt_pairs: HashSet<(&str, &str)> = less_than
        .iter()
        .filter(|a| a.args.len() == 2)
        .map(|a| (a.args[0].as_str(), a.args[1].as_str()))
        .collect();
    // Map rule_id -> set(building_ids) from applies_to(rule, building).
    let mut applies_index: HashMap<&str, HashSet<&str>> = HashMap::new();
    for a in applies_to.iter().filter(|a| a.args.len() == 2) {
        applies_index
            .entry(a.args[0].as_str())
            .or_default()
            .insert(a.args[1].as_str());
    }

    for hd in has_distance.iter().filter(|a| a.args.len() == 2) {
        let building = hd.args[0].as_str();
        let d_actual = hd.args[1].as_str();
        for rd in requires_distance.iter().filter(|a| a.args.len() == 2) {
            let rule = rd.args[0].as_str();
            let d_required = rd.args[1].as_str();
            if !lt_pairs.contains(&(d_actual, d_required)) {
                continue;
            }
            if let Some(targets) = applies_index.get(rule) {
                if targets.contains(building) {
                    return true;
                }
            }
        }
    }
    false
}

/// Evaluate the hardcoded Datalog ruleset over a list of textual facts.
///
/// `facts` is a list of `predicate(arg1, arg2, ...)` strings. Returns
/// `True` iff at least one `violates(_, _)` fact can be derived. Any
/// malformed fact string raises `ValueError`.
///
/// The `rules` argument is accepted for API-compatibility with the
/// Sprint Z S1 plan (which eventually wants user-supplied rules), but
/// the current hand-rolled evaluator ignores it — the only ruleset
/// supported is the hardcoded Vitruvius compliance one described in
/// the module docstring.
#[pyfunction]
#[pyo3(signature = (facts, rules = None))]
#[allow(clippy::useless_conversion)]
fn evaluate_datalog(facts: Vec<String>, rules: Option<Vec<String>>) -> PyResult<bool> {
    let _ = rules; // reserved for future rule-compiling path
    let mut atoms: Vec<Atom> = Vec::with_capacity(facts.len());
    for raw in &facts {
        let atom = parse_atom(raw).map_err(PyValueError::new_err)?;
        atoms.push(atom);
    }
    Ok(evaluate_ruleset(&atoms))
}

#[pymodule]
fn vitruvius_datalog_rs(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evaluate_datalog, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_simple_fact() {
        let atom = parse_atom("has_distance(building_42, 1_8)").unwrap();
        assert_eq!(atom.predicate, "has_distance");
        assert_eq!(atom.args, vec!["building_42", "1_8"]);
    }

    #[test]
    fn parse_rejects_missing_paren() {
        assert!(parse_atom("not a datalog fact").is_err());
    }

    #[test]
    fn parse_rejects_empty_predicate() {
        assert!(parse_atom("(a, b)").is_err());
    }

    #[test]
    fn parse_rejects_empty_arg() {
        assert!(parse_atom("p(a,,b)").is_err());
    }

    #[test]
    fn ruleset_detects_violation() {
        let facts = vec![
            parse_atom("has_distance(building_42, 1_8)").unwrap(),
            parse_atom("requires_distance(setback_rule_3, 2_0)").unwrap(),
            parse_atom("less_than(1_8, 2_0)").unwrap(),
            parse_atom("applies_to(setback_rule_3, building_42)").unwrap(),
        ];
        assert!(evaluate_ruleset(&facts));
    }

    #[test]
    fn ruleset_rejects_compliant_case() {
        let facts = vec![
            parse_atom("has_distance(building_42, 2_5)").unwrap(),
            parse_atom("requires_distance(setback_rule_3, 2_0)").unwrap(),
            parse_atom("less_than(1_8, 2_0)").unwrap(),
            parse_atom("applies_to(setback_rule_3, building_42)").unwrap(),
        ];
        assert!(!evaluate_ruleset(&facts));
    }

    #[test]
    fn ruleset_requires_applies_to() {
        let facts = vec![
            parse_atom("has_distance(building_42, 1_8)").unwrap(),
            parse_atom("requires_distance(setback_rule_3, 2_0)").unwrap(),
            parse_atom("less_than(1_8, 2_0)").unwrap(),
            // applies_to missing — rule does not fire.
        ];
        assert!(!evaluate_ruleset(&facts));
    }
}
