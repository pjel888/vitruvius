"""Sprint WIKI Stream WIKI.4.1 — SHA-256 delta tracking tests."""
from __future__ import annotations

from pathlib import Path

from vitruvius.wiki.delta_tracker import (
    DeltaTracker,
    PageDigest,
)


def test_first_pass_reports_all_pages_new(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "a.md").write_text("---\nid: a\n---\n# A", encoding="utf-8")
    (wiki / "b.md").write_text("---\nid: b\n---\n# B", encoding="utf-8")

    tracker = DeltaTracker(manifest_path=tmp_path / "manifest.json")
    delta = tracker.compute_delta(wiki)
    assert set(delta.new) == {"a.md", "b.md"}
    assert delta.changed == []
    assert delta.removed == []


def test_second_pass_detects_no_changes(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "a.md").write_text("hello", encoding="utf-8")

    tracker = DeltaTracker(manifest_path=tmp_path / "manifest.json")
    tracker.commit_snapshot(wiki)

    delta = tracker.compute_delta(wiki)
    assert delta.new == []
    assert delta.changed == []
    assert delta.removed == []


def test_mutation_detected_as_change(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "a.md").write_text("v1", encoding="utf-8")

    tracker = DeltaTracker(manifest_path=tmp_path / "manifest.json")
    tracker.commit_snapshot(wiki)

    (wiki / "a.md").write_text("v2", encoding="utf-8")
    delta = tracker.compute_delta(wiki)
    assert delta.changed == ["a.md"]
    assert delta.new == []
    assert delta.removed == []


def test_removal_detected(tmp_path: Path) -> None:
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "a.md").write_text("keep", encoding="utf-8")
    (wiki / "b.md").write_text("drop", encoding="utf-8")

    tracker = DeltaTracker(manifest_path=tmp_path / "manifest.json")
    tracker.commit_snapshot(wiki)

    (wiki / "b.md").unlink()
    delta = tracker.compute_delta(wiki)
    assert delta.removed == ["b.md"]


def test_page_digest_is_deterministic() -> None:
    a = PageDigest(relative_path="x.md", sha256="abc")
    b = PageDigest(relative_path="x.md", sha256="abc")
    assert a == b
    assert hash(a) == hash(b)
