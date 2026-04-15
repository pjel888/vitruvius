"""Sprint WIKI Stream WIKI.3 — Kuzu-backed hybrid wiki page store.

Maps wiki-page YAML frontmatter into a relational graph schema that
lives inside a single :class:`kuzu.Database`. Callers feed upserts
through :meth:`KuzuWikiStore.upsert_page` and query via
:meth:`pages_by_source` / :meth:`get_page`. Tags and linked
entities land as comma-joined strings in the node table because
Kuzu 0.11 does not accept list literals in bind parameters from the
Python driver — the reader side splits them back into tuples.

Lazy-imported: ``import vitruvius.wiki.kuzu_store`` does not load the
``kuzu`` library. Only :class:`KuzuWikiStore.__init__` does.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class WikiPageRow:
    page_id: str
    title: str
    source_id: str
    tags: tuple[str, ...]
    linked_entities: tuple[str, ...]


def _join(values: Iterable[str]) -> str:
    return ",".join(values)


def _split(joined: str) -> tuple[str, ...]:
    if not joined:
        return ()
    return tuple(piece for piece in joined.split(",") if piece)


class KuzuWikiStore:
    """Thin facade around a Kuzu database storing wiki pages.

    The store is designed to be opened once per operator session and
    explicitly closed via :meth:`close`. Tests use tmp_path so each
    test gets a fresh database.
    """

    _SCHEMA = (
        "CREATE NODE TABLE IF NOT EXISTS WikiPage("
        "page_id STRING, "
        "title STRING, "
        "source_id STRING, "
        "tags_joined STRING, "
        "linked_joined STRING, "
        "PRIMARY KEY (page_id)"
        ")"
    )

    def __init__(self, *, db_path: Path) -> None:
        import kuzu

        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db = kuzu.Database(str(self._db_path))
        self._conn = kuzu.Connection(self._db)
        self._conn.execute(self._SCHEMA)

    def upsert_page(self, row: WikiPageRow) -> None:
        """Insert or replace a :class:`WikiPageRow` keyed by page_id."""
        self._conn.execute(
            "MERGE (p:WikiPage {page_id: $pid}) "
            "SET p.title = $title, "
            "p.source_id = $source, "
            "p.tags_joined = $tags, "
            "p.linked_joined = $linked",
            {
                "pid": row.page_id,
                "title": row.title,
                "source": row.source_id,
                "tags": _join(row.tags),
                "linked": _join(row.linked_entities),
            },
        )

    def get_page(self, page_id: str) -> Optional[WikiPageRow]:
        result = self._conn.execute(
            "MATCH (p:WikiPage) WHERE p.page_id = $pid "
            "RETURN p.page_id, p.title, p.source_id, p.tags_joined, p.linked_joined",
            {"pid": page_id},
        )
        if not result.has_next():
            return None
        row = result.get_next()
        return WikiPageRow(
            page_id=row[0],
            title=row[1],
            source_id=row[2],
            tags=_split(row[3]),
            linked_entities=_split(row[4]),
        )

    def pages_by_source(self, source_id: str) -> list[WikiPageRow]:
        result = self._conn.execute(
            "MATCH (p:WikiPage) WHERE p.source_id = $source "
            "RETURN p.page_id, p.title, p.source_id, p.tags_joined, p.linked_joined "
            "ORDER BY p.page_id",
            {"source": source_id},
        )
        rows: list[WikiPageRow] = []
        while result.has_next():
            r = result.get_next()
            rows.append(
                WikiPageRow(
                    page_id=r[0],
                    title=r[1],
                    source_id=r[2],
                    tags=_split(r[3]),
                    linked_entities=_split(r[4]),
                )
            )
        return rows

    def count_pages(self) -> int:
        result = self._conn.execute("MATCH (p:WikiPage) RETURN count(p)")
        if not result.has_next():
            return 0
        return int(result.get_next()[0])

    def close(self) -> None:
        # Kuzu releases resources when the Python objects are garbage
        # collected; set explicit None to drop references.
        self._conn = None  # type: ignore[assignment]
        self._db = None  # type: ignore[assignment]
