"""PMI alias miner — deterministic pointwise-mutual-information candidate ranker."""

from __future__ import annotations

import json
from pathlib import Path

from vitruvius.features import Features
from vitruvius.concepts.pmi_alias_miner import (
    DEFAULT_MIN_JOINT_COUNT,
    DEFAULT_MIN_PMI,
    DEFAULT_WINDOW_SIZE,
    mine_aliases,
)


# Small hand-crafted corpus where "exit" and "egress" are perfectly collocated.
# Every occurrence of "exit" is accompanied by "egress" within a 5-word window.
COLLOCATED_CORPUS = (
    "Every exit shall serve as a means of egress for occupants. "
    "The minimum exit width equals the occupant load divided by the egress factor. "
    "Each exit route provides emergency egress during fire conditions. "
    "Required exit paths and means of egress must remain unobstructed. "
    "Fire exit signs guide occupants to the nearest egress point always. "
    "Exit capacity determines the maximum egress flow per minute safely. "
)


ISOLATED_CORPUS = (
    "The exit serves one hundred occupants. "
    "Building permits require payment of a fee. "
    "Fire safety means saving lives before anything else. "
    "Occupancy classification covers multiple building types. "
    # "banana" co-occurs with "exit" exactly once — should NOT clear min_joint_count
    "exit banana. "
)


def test_pmi_identifies_collocated_terms() -> None:
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=3,  # relax to pick up small corpus
    )
    # "egress" must appear in the candidate list for "exit"
    egresses = [c for c in report.candidates if c.candidate == "egress"]
    assert egresses, "expected 'egress' as a collocated alias for 'exit'"
    # It has a positive PMI score since both terms co-occur more often than chance
    assert egresses[0].pmi > 0


def test_pmi_ignores_isolated_cooccurrences() -> None:
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=ISOLATED_CORPUS,
        min_joint_count=DEFAULT_MIN_JOINT_COUNT,  # 5
    )
    # "banana" co-occurs with "exit" only once → excluded by min_joint_count
    bananas = [c for c in report.candidates if c.candidate == "banana"]
    assert bananas == []


def test_ranked_by_pmi_score_descending() -> None:
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
    )
    # Group by concept_slug, within a group PMI descending
    for slug in {c.concept_slug for c in report.candidates}:
        slug_group = [c for c in report.candidates if c.concept_slug == slug]
        scores = [c.pmi for c in slug_group]
        assert scores == sorted(scores, reverse=True), f"unsorted for {slug}"


def test_minimum_joint_count_filter() -> None:
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=100,  # absurdly high — nothing clears it
    )
    assert report.candidates == ()


def test_flag_off_is_noop(tmp_path: Path) -> None:
    features = Features(flags={})  # flag implicitly false
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        runs_dir=runs_dir,
    )
    assert report.candidates == ()
    out = runs_dir / "latest_pmi_alias_mining.json"
    assert not out.exists()


def test_writes_report_when_runs_dir_provided(tmp_path: Path) -> None:
    features = Features(flags={"d_pmi_aliases": True})
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
        runs_dir=runs_dir,
    )
    out = runs_dir / "latest_pmi_alias_mining.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert "window_size" in data
    assert "min_pmi" in data
    assert "candidates" in data


def test_multi_slug_report_is_deterministic(tmp_path: Path) -> None:
    features = Features(flags={"d_pmi_aliases": True})
    r1 = mine_aliases(
        features=features,
        concept_slugs=["exit", "width"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
    )
    r2 = mine_aliases(
        features=features,
        concept_slugs=["exit", "width"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
    )
    # Report is frozen; equality should hold
    assert r1 == r2


def test_stopwords_excluded_from_candidates() -> None:
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
    )
    stopwords = {"the", "a", "an", "of", "and", "for", "to", "is", "are", "be", "shall", "must"}
    cand_tokens = {c.candidate for c in report.candidates}
    assert cand_tokens.isdisjoint(stopwords)


def test_defaults_are_documented() -> None:
    # Sanity — defaults match the statistical-architectural-upgrade-plan §8.3
    assert DEFAULT_WINDOW_SIZE == 5
    assert DEFAULT_MIN_PMI == 3.0
    assert DEFAULT_MIN_JOINT_COUNT == 5


def test_slug_tokens_are_not_self_candidates() -> None:
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
    )
    # The slug token itself must never show up as its own alias candidate.
    assert all(c.candidate != "exit" for c in report.candidates if c.concept_slug == "exit")


def test_multi_token_slug_expands_on_hyphen() -> None:
    # "exit-width" → ["exit", "width"]; windows hitting either token should contribute
    features = Features(flags={"d_pmi_aliases": True})
    report = mine_aliases(
        features=features,
        concept_slugs=["exit-width"],
        corpus=COLLOCATED_CORPUS,
        min_joint_count=1,
    )
    # egress is heavily collocated with exit → should appear for the expanded slug
    egresses = [c for c in report.candidates if c.candidate == "egress"]
    assert egresses, "expected 'egress' under exit-width via slug-token expansion"
    # Neither slug component can be its own candidate
    assert all(c.candidate not in {"exit", "width"} for c in report.candidates)
