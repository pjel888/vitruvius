"""One-time backfill script for existing sources.

Creates DocumentVersion v1 records in PostgreSQL for all sources found in:
- 003_Canonical-Knowledge-Layer/shared/sources/  (canonical Markdown)
- 001_Raw-Source-Layer/                          (raw PDFs, Office files)

Usage::

    python scripts/vitruvius/kg/backfill_document_versions.py

The script is idempotent (ON CONFLICT UPDATE) and read-only on source layers.
"""

from __future__ import annotations

import hashlib
import logging
import sys
from pathlib import Path
from typing import Any

import yaml

from vitruvius.config import get_kg_postgres_conninfo
from vitruvius.kg.postgres_client import PostgresClient
from vitruvius.paths import get_repo_root

logger = logging.getLogger(__name__)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _slugify(name: str) -> str:
    import re

    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def _load_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        data = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _derive_document_id(source_path: Path) -> str:
    """Derive a stable doc- ID from a file path."""
    slug = _slugify(source_path.stem)[:64]
    return f"doc-{slug}"


def backfill_canonical_sources(
    postgres: PostgresClient,
    canonical_root: Path,
) -> int:
    """Backfill DocumentVersion records from canonical Markdown sources."""
    sources_dir = canonical_root / "sources"
    if not sources_dir.exists():
        logger.warning("Canonical sources directory not found: %s", sources_dir)
        return 0

    count = 0
    for md_path in sorted(sources_dir.rglob("*.md")):
        fm = _load_frontmatter(md_path)
        if not fm:
            logger.warning("No frontmatter: %s", md_path)
            continue

        entity_id = fm.get("id")
        if not entity_id:
            logger.warning("Missing id in frontmatter: %s", md_path)
            continue

        slug = _slugify(entity_id)
        docv_id = f"docv-{slug}-v1"
        doc_id = f"doc-{slug}"

        # SHA-256 from canonical file content
        sha = _sha256_file(md_path)

        record = {
            "id": docv_id,
            "document_id": doc_id,
            "title": fm.get("title", md_path.stem.replace("-", " ").title()),
            "source_uri": str(md_path.relative_to(canonical_root.parent.parent)),
            "mime_type": "text/markdown",
            "sha256": sha,
            "supersedes": None,
        }
        postgres.insert_document_version(record)
        count += 1

    logger.info("Backfilled %d canonical sources", count)
    return count


def backfill_raw_sources(
    postgres: PostgresClient,
    raw_root: Path,
) -> int:
    """Backfill DocumentVersion records from raw source files."""
    if not raw_root.exists():
        logger.warning("Raw source directory not found: %s", raw_root)
        return 0

    extensions = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"}
    count = 0

    for source_path in sorted(raw_root.rglob("*")):
        if not source_path.is_file():
            continue
        if source_path.suffix.lower() not in extensions:
            continue

        doc_id = _derive_document_id(source_path)
        docv_id = f"{doc_id.replace('doc-', 'docv-')}-v1"
        sha = _sha256_file(source_path)

        mime_map = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".ppt": "application/vnd.ms-powerpoint",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
        }

        record = {
            "id": docv_id,
            "document_id": doc_id,
            "title": source_path.stem,
            "source_uri": str(source_path.relative_to(raw_root.parent)),
            "mime_type": mime_map.get(source_path.suffix.lower(), "application/octet-stream"),
            "sha256": sha,
            "supersedes": None,
        }
        postgres.insert_document_version(record)
        count += 1

    logger.info("Backfilled %d raw sources", count)
    return count


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    repo_root = get_repo_root()
    canonical_root = repo_root / "003_Canonical-Knowledge-Layer" / "shared"
    raw_root = repo_root / "001_Raw-Source-Layer"

    postgres = PostgresClient(conninfo=get_kg_postgres_conninfo())
    if not postgres.verify_connectivity():
        logger.error("PostgreSQL is not reachable. Check config/vitruvius.yaml.")
        return 1

    canonical_count = backfill_canonical_sources(postgres, canonical_root)
    raw_count = backfill_raw_sources(postgres, raw_root)

    total = canonical_count + raw_count
    logger.info("Backfill complete: %d total document versions inserted/updated", total)

    postgres.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
