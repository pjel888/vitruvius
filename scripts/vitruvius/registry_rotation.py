from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .paths import get_repo_root
from .constants import MANIFESTS_NAME, REGISTRIES_NAME

_TIMESTAMP_RE = re.compile(r"^(?P<stamp>\d{8}T\d{6}Z)_(?P<family>.+\.csv)$")


@dataclass(kw_only=True, frozen=True)
class RotationPlan:
    family: str
    kept: tuple[Path, ...]
    pruned: tuple[Path, ...]


@dataclass(kw_only=True, frozen=True)
class RotationReport:
    plans: tuple[RotationPlan, ...]
    total_kept: int
    total_pruned: int
    dry_run: bool


def plan_rotation(
    registries_dir: Path,
    *,
    keep: int = 30,
) -> RotationReport:
    families: dict[str, list[tuple[str, Path]]] = {}
    for p in registries_dir.glob("*.csv"):
        m = _TIMESTAMP_RE.match(p.name)
        if not m:
            continue
        family = m.group("family")
        stamp = m.group("stamp")
        families.setdefault(family, []).append((stamp, p))

    plans: list[RotationPlan] = []
    for family in sorted(families):
        entries = sorted(families[family], key=lambda x: x[0], reverse=True)
        kept_paths = tuple(p for _, p in entries[:keep])
        pruned_paths = tuple(p for _, p in entries[keep:])
        plans.append(RotationPlan(family=family, kept=kept_paths, pruned=pruned_paths))

    total_kept = sum(len(pl.kept) for pl in plans)
    total_pruned = sum(len(pl.pruned) for pl in plans)
    return RotationReport(
        plans=tuple(plans),
        total_kept=total_kept,
        total_pruned=total_pruned,
        dry_run=True,
    )


def apply_rotation(report: RotationReport) -> RotationReport:
    for plan in report.plans:
        for p in plan.pruned:
            p.unlink()

    new_plans = tuple(
        RotationPlan(family=pl.family, kept=pl.kept, pruned=pl.pruned)
        for pl in report.plans
    )
    return RotationReport(
        plans=new_plans,
        total_kept=report.total_kept,
        total_pruned=report.total_pruned,
        dry_run=False,
    )


def run_rotate_registries(
    *,
    keep: int = 30,
    dry_run: bool = False,
    registries_dir: Path | None = None,
) -> int:
    if registries_dir is None:
        registries_dir = get_repo_root() / MANIFESTS_NAME / REGISTRIES_NAME

    report = plan_rotation(registries_dir, keep=keep)

    if not dry_run:
        report = apply_rotation(report)

    mode = "DRY RUN — " if dry_run else ""
    print(f"rotate-registries  {mode}keep={keep}")
    print(f"  total kept:   {report.total_kept}")
    print(f"  total pruned: {report.total_pruned}")
    for plan in report.plans:
        print(f"  {plan.family}: kept={len(plan.kept)}  pruned={len(plan.pruned)}")

    return 0
