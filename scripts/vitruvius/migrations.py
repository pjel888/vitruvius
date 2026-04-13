from __future__ import annotations

import re
import yaml
from pathlib import Path
from typing import Dict, List

from .paths import get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


# --------------------------------------------------
# LOAD MIGRATION MAP
# --------------------------------------------------

def load_migration_map() -> Dict[str, str]:
    repo_root = get_repo_root()
    path = repo_root / "006_System-Manifests" / "migrations" / "id_migration_map.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Migration map not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("mappings", {})


# --------------------------------------------------
# FILE DISCOVERY
# --------------------------------------------------

def get_canonical_files() -> List[Path]:
    repo_root = get_repo_root()
    base = repo_root / "003_Canonical-Knowledge-Layer"
    return list(base.rglob("*.md"))


# --------------------------------------------------
# FIND REFERENCES (PLAN)
# --------------------------------------------------

def find_id_references(text: str, migration_map: Dict[str, str]) -> Dict[str, int]:
    counts = {}

    for old_id in migration_map.keys():
        matches = re.findall(rf"\b{re.escape(old_id)}\b", text)
        if matches:
            counts[old_id] = len(matches)

    return counts


def build_migration_plan():
    migration_map = load_migration_map()
    files = get_canonical_files()

    plan = {
        "generated_at": utc_now_stamp(),
        "total_files_scanned": len(files),
        "files_with_changes": [],
        "summary": {
            "total_replacements": 0,
            "unique_ids_affected": set(),
        }
    }

    for file_path in files:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        matches = find_id_references(content, migration_map)

        if not matches:
            continue

        file_entry = {
            "file": str(file_path),
            "matches": [],
        }

        for old_id, count in matches.items():
            new_id = migration_map[old_id]

            file_entry["matches"].append({
                "old_id": old_id,
                "new_id": new_id,
                "count": count,
            })

            plan["summary"]["total_replacements"] += count
            plan["summary"]["unique_ids_affected"].add(old_id)

        plan["files_with_changes"].append(file_entry)

    plan["summary"]["unique_ids_affected"] = list(plan["summary"]["unique_ids_affected"])

    return plan


def run_migrate_ids_plan() -> int:
    repo_root = get_repo_root()
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    plan = build_migration_plan()

    json_path = runs_dir / "latest_migrate_ids_plan.json"
    txt_path = runs_dir / "latest_migrate_ids_plan.txt"

    write_json(json_path, plan)

    lines = []
    lines.append("Vitruvius ID Migration Plan (Dry Run)\n")
    lines.append(f"Files scanned: {plan['total_files_scanned']}")
    lines.append(f"Files affected: {len(plan['files_with_changes'])}")
    lines.append(f"Total replacements: {plan['summary']['total_replacements']}\n")

    for file in plan["files_with_changes"]:
        lines.append(f"FILE: {file['file']}")
        for match in file["matches"]:
            lines.append(
                f"  {match['old_id']} -> {match['new_id']} (x{match['count']})"
            )
        lines.append("")

    write_text(txt_path, "\n".join(lines))

    print("migrate-ids-plan complete.")
    print(f"Report JSON: {json_path}")
    print(f"Report TXT: {txt_path}")

    return 0


# --------------------------------------------------
# APPLY
# --------------------------------------------------

def replace_ids(text: str, migration_map: Dict[str, str]) -> tuple[str, int]:
    total = 0

    for old_id, new_id in migration_map.items():
        pattern = rf"\b{re.escape(old_id)}\b"
        matches = re.findall(pattern, text)

        if matches:
            count = len(matches)
            text = re.sub(pattern, new_id, text)
            total += count

    return text, total


def apply_migration():
    migration_map = load_migration_map()
    files = get_canonical_files()

    report = {
        "generated_at": utc_now_stamp(),
        "files_updated": [],
        "total_replacements": 0,
    }

    for file_path in files:
        original = file_path.read_text(encoding="utf-8", errors="ignore")

        updated, count = replace_ids(original, migration_map)

        if count == 0:
            continue

        file_path.write_text(updated, encoding="utf-8")

        report["files_updated"].append({
            "file": str(file_path),
            "replacements": count,
        })

        report["total_replacements"] += count

    return report


def run_migrate_ids_apply() -> int:
    repo_root = get_repo_root()
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    report = apply_migration()

    json_path = runs_dir / "latest_migrate_ids_apply.json"
    txt_path = runs_dir / "latest_migrate_ids_apply.txt"

    write_json(json_path, report)

    lines = []
    lines.append("Vitruvius ID Migration Apply\n")
    lines.append(f"Files updated: {len(report['files_updated'])}")
    lines.append(f"Total replacements: {report['total_replacements']}\n")

    for item in report["files_updated"]:
        lines.append(f"{item['file']} (replacements: {item['replacements']})")

    write_text(txt_path, "\n".join(lines))

    print("migrate-ids-apply complete.")
    print(f"Report JSON: {json_path}")
    print(f"Report TXT: {txt_path}")

    return 0