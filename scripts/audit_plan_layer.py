#!/usr/bin/env python3
"""
Plan-layer integrity scanner for .ai/03_plans/
Produces an audit report of frontmatter, status, and inventory issues.
"""
import os
import re
from pathlib import Path
from collections import defaultdict

PLANS_DIR = Path(".ai/03_plans")


def extract_frontmatter(text: str) -> dict:
    """Extract YAML-like frontmatter from markdown."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    result = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.startswith("#"):
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result


def scan_plans():
    files = sorted(PLANS_DIR.glob("*.md"))
    issues = []
    stats = defaultdict(int)
    statuses = defaultdict(list)
    phases = defaultdict(list)
    tasks = defaultdict(list)

    required_fields = {"task", "status"}
    recommended_fields = {"created", "phase"}

    for f in files:
        text = f.read_text()
        fm = extract_frontmatter(text)

        # Missing required fields
        missing = required_fields - set(fm.keys())
        if missing:
            issues.append((f.name, f"missing required fields: {missing}"))

        # Missing recommended fields
        missing_rec = recommended_fields - set(fm.keys())
        if missing_rec:
            issues.append((f.name, f"missing recommended fields: {missing_rec}"))

        status = fm.get("status", "UNKNOWN").lower()
        statuses[status].append(f.name)
        stats["total"] += 1

        phase = fm.get("phase", "UNKNOWN")
        phases[phase].append(f.name)

        task = fm.get("task", "UNKNOWN")
        tasks[task].append(f.name)

        # Check for stale placeholder text
        if "only two active plans" in text.lower():
            issues.append((f.name, "stale claim: 'only two active plans'"))

        # Check for empty plan body
        if text.startswith("---"):
            end_idx = text.find("---", 3)
            body = text[end_idx + 3:] if end_idx != -1 else text
        else:
            body = text
        if len(body.strip()) < 100:
            issues.append((f.name, "very short body — possible placeholder"))

        # Check heading integrity
        if "# " not in text:
            issues.append((f.name, "missing H1 heading"))

    # Duplicate task names
    for task, names in tasks.items():
        if len(names) > 1:
            issues.append((", ".join(names), f"duplicate task name: {task}"))

    # Check INDEX.md references exist
    index_path = PLANS_DIR / "INDEX.md"
    if index_path.exists():
        index_text = index_path.read_text()
        # Find backtick-quoted filenames
        for match in re.finditer(r'`([^`]+\.md)`', index_text):
            fname = match.group(1)
            if not (PLANS_DIR / fname).exists():
                issues.append(("INDEX.md", f"references missing file: {fname}"))

    # Check for files not in INDEX.md
    indexed = set()
    if index_path.exists():
        for match in re.finditer(r'`([^`]+\.md)`', index_text):
            indexed.add(match.group(1))
    for f in files:
        if f.name not in indexed and f.name != "INDEX.md":
            issues.append(("INDEX.md", f"missing from index: {f.name}"))

    return issues, statuses, phases, stats


def main():
    issues, statuses, phases, stats = scan_plans()

    print("# Plan Layer Integrity Audit Report")
    print(f"\nGenerated: {os.popen('date -u +%Y-%m-%dT%H:%M:%SZ').read().strip()}")
    print(f"\n## Summary")
    print(f"- Total plan files scanned: {stats['total']}")
    print(f"- Total issues found: {len(issues)}")

    print(f"\n## Status Distribution")
    for status in sorted(statuses.keys()):
        print(f"- `{status}`: {len(statuses[status])}")

    print(f"\n## Phase Distribution")
    for phase in sorted(phases.keys()):
        print(f"- Phase {phase}: {len(phases[phase])}")

    if issues:
        print(f"\n## Issues Found")
        current_file = None
        for fname, issue in sorted(issues):
            if fname != current_file:
                print(f"\n### {fname}")
                current_file = fname
            print(f"- {issue}")
    else:
        print(f"\n## Issues Found\nNone.")

    print(f"\n## Files by Status")
    for status in sorted(statuses.keys()):
        print(f"\n### {status}")
        for name in sorted(statuses[status]):
            print(f"- {name}")


if __name__ == "__main__":
    main()
