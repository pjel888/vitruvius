"""Stream W3.1 — one-shot migration adding `stringency_vector` to every concept.

Usage:
  PYTHONPATH=scripts python -m vitruvius.migrations.add_stringency_vector

The migration is idempotent: running it twice is a no-op.
"""
from __future__ import annotations

from pathlib import Path

_SEMANTICS = {
    # Stricter means a larger number — maximize
    "setbacks": "maximize",
    "exit-width": "maximize",
    "fire-resistive-construction": "maximize",
    "light-and-ventilation": "maximize",
    "means-of-egress": "maximize",
    "doors-and-exits": "maximize",
    # Stricter means a smaller number — minimize
    "lot-occupancy": "minimize",
    "floor-area": "minimize",
    "building-height": "minimize",
    # Everything else: qualitative (no single numeric axis)
}


def _default_vector(slug: str) -> str:
    return _SEMANTICS.get(slug, "qualitative")


def _migrate_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    head = text[3:end]
    if "stringency_vector" in head:
        return False  # idempotent
    vector = _default_vector(path.stem)
    new_head = head.rstrip() + f"\nstringency_vector: {vector}\n"
    new_text = "---" + new_head + "---" + text[end + 4:]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    concepts_dir = (
        repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    )
    updated = 0
    for path in sorted(concepts_dir.glob("*.md")):
        if _migrate_file(path):
            updated += 1
    print(f"updated {updated} concept files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
