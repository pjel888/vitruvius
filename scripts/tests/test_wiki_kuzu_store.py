"""Sprint WIKI Stream WIKI.3 — Kuzu hybrid store tests."""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("kuzu")

from vitruvius.wiki.kuzu_store import (
    KuzuWikiStore,
    WikiPageRow,
)


def test_initialize_creates_schema(tmp_path: Path) -> None:
    db_path = tmp_path / "wiki.kuzu"
    store = KuzuWikiStore(db_path=db_path)
    try:
        assert db_path.exists()
        assert store.count_pages() == 0
    finally:
        store.close()


def test_upsert_and_fetch_page(tmp_path: Path) -> None:
    db_path = tmp_path / "wiki.kuzu"
    store = KuzuWikiStore(db_path=db_path)
    try:
        row = WikiPageRow(
            page_id="concept-building-permit",
            title="Building Permit",
            source_id="law-pd-1096",
            tags=("governance", "permit"),
            linked_entities=("concept-building-official",),
        )
        store.upsert_page(row)
        fetched = store.get_page("concept-building-permit")
        assert fetched is not None
        assert fetched.title == "Building Permit"
        assert "permit" in fetched.tags
        assert "concept-building-official" in fetched.linked_entities
    finally:
        store.close()


def test_upsert_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "wiki.kuzu"
    store = KuzuWikiStore(db_path=db_path)
    try:
        row = WikiPageRow(
            page_id="concept-setbacks",
            title="Setbacks",
            source_id="law-pd-1096",
            tags=(),
            linked_entities=(),
        )
        store.upsert_page(row)
        store.upsert_page(row)
        store.upsert_page(row)
        assert store.count_pages() == 1
    finally:
        store.close()


def test_query_by_source(tmp_path: Path) -> None:
    db_path = tmp_path / "wiki.kuzu"
    store = KuzuWikiStore(db_path=db_path)
    try:
        store.upsert_page(WikiPageRow(
            page_id="concept-a", title="A",
            source_id="law-pd-1096", tags=(), linked_entities=(),
        ))
        store.upsert_page(WikiPageRow(
            page_id="concept-b", title="B",
            source_id="law-pd-1096", tags=(), linked_entities=(),
        ))
        store.upsert_page(WikiPageRow(
            page_id="concept-c", title="C",
            source_id="law-other", tags=(), linked_entities=(),
        ))
        pages = store.pages_by_source("law-pd-1096")
        assert len(pages) == 2
        assert {p.page_id for p in pages} == {"concept-a", "concept-b"}
    finally:
        store.close()
