"""Sprint LSH-1 Task 5 — LSH fuzzy dedup micro-benchmark.

Measures wall-time of the exact-endpoint path vs the LSH +
exact-endpoint layered path on synthetic candidate corpora at
N in {100, 1000, 10000}. Also measures fuzzy-match hit rate
(LSH-dedup count vs exact-dedup count) and false-positive count
(disjoint-triple collapse detection).

Per AD-037 the existing dedupe_by_endpoints is already
O(n log n) dict-grouped exact dedup, so this bench does NOT
document a scaling fix. The point is to:

1. Verify the LSH layer's tax on corpora WITHOUT fuzzy duplicates
   is cheap enough to leave on by default (Task 5 flag-flip gate).
2. Verify the LSH layer's fuzzy-match hit rate on corpora WITH
   injected fuzzy duplicates (AD-037 hit-rate gate >=10%).
3. Verify the zero-false-positive guard on fully-disjoint corpora
   (AD-037 false-positive gate = 0).

Writes .ai/10_state/bench_lsh_dedup_2026-04-15.json with the
measured numbers.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from vitruvius.relationships.lsh_dedup import dedupe_by_endpoints_lsh
from vitruvius.relationships_sections import dedupe_by_endpoints


REPO_ROOT = Path(__file__).resolve().parents[3]


def _cand(from_id: str, type_: str, to: str, occurrences: int = 1) -> dict:
    return {
        "from": from_id,
        "type": type_,
        "to": to,
        "occurrences": occurrences,
        "sections": [],
        "examples": [],
    }


def generate_disjoint_corpus(n: int, *, rng: random.Random) -> list[dict]:
    """Generate a maximally-disjoint corpus for scaling bench.

    At scaling-bench sizes (n up to 10000) we cannot hand-pick slugs
    that are both meaningful English AND provably non-overlapping in
    the feature-bag sense. Instead we deterministically generate
    slugs from a SHA-256-based suffix so that each slug's 4-gram
    shingles are effectively random bytes with no cross-pair
    overlap. This matches the semantics of a real corpus where
    every relationship's slug is a distinct real-world concept.

    The ``concept-`` prefix is stripped for the first segment so
    the shingle overlap at the start of each slug doesn't
    artificially dominate the feature set.
    """
    import hashlib as _h
    predicates = ["governs", "requires", "limits", "affects", "depends_on"]

    def deterministic_slug(prefix: str, i: int) -> str:
        raw = _h.sha256(f"{prefix}:{i}".encode()).hexdigest()[:12]
        return f"c{raw}"

    candidates = []
    for i in range(n):
        s = deterministic_slug("subject", i)
        o = deterministic_slug("object", i)
        p = predicates[i % len(predicates)]
        candidates.append(_cand(s, p, o))
    return candidates


def inject_fuzzy_variants(
    corpus: list[dict],
    *,
    fraction: float,
    rng: random.Random,
) -> list[dict]:
    """Inject ``fraction`` * ``len(corpus)`` fuzzy near-duplicate
    variants into the corpus.

    For each original candidate selected, emit a second copy whose
    ``from`` slug has ``min-`` prepended AND its last character
    changed — mimicking the real PD 1096 pattern of slug drift like
    "lot area >= 100 sqm" vs "minimum lot area of 100 square meters"
    or "light governs corridor" vs "lighting governs corridors". The
    variant is guaranteed NOT byte-equal to the original so the
    exact-endpoint dedup cannot catch it, but shares enough 4-gram
    shingles that the LSH layer should collapse it.
    """
    num_inject = int(len(corpus) * fraction)
    if num_inject == 0:
        return list(corpus)
    victims = rng.sample(range(len(corpus)), num_inject)
    augmented = list(corpus)
    for idx in victims:
        original = corpus[idx]
        variant = dict(original)
        variant["from"] = f"min-{original['from']}x"
        augmented.append(variant)
    return augmented


def measure_wall_ms(fn, *args, **kwargs) -> float:
    """Return median of 3 runs in milliseconds."""
    samples = []
    for _ in range(3):
        t0 = time.perf_counter()
        fn(*args, **kwargs)
        samples.append((time.perf_counter() - t0) * 1000)
    samples.sort()
    return samples[1]


def measure_hit_rate(candidates: list[dict]) -> dict:
    """Run both paths and return counts + LSH hit rate."""
    exact = dedupe_by_endpoints(candidates)
    lsh = dedupe_by_endpoints_lsh(candidates)

    collapsed = len(exact) - len(lsh)
    hit_rate = collapsed / max(1, len(exact))
    return {
        "input_count": len(candidates),
        "exact_count": len(exact),
        "lsh_count": len(lsh),
        "collapsed_by_lsh": collapsed,
        "hit_rate": round(hit_rate, 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / ".ai" / "10_state" / "bench_lsh_dedup_2026-04-15.json"),
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)

    results: dict = {
        "generated_at": "2026-04-15",
        "sprint": "Sprint LSH-1",
        "ad": "AD-037, AD-042",
        "notes": (
            "Per AD-037 the existing dedupe_by_endpoints is O(n log n) "
            "dict-grouped exact dedup. This bench does NOT document a "
            "scaling fix — it documents (1) LSH layer tax on disjoint "
            "corpora, (2) fuzzy-match hit rate on corpora with injected "
            "near-duplicates, and (3) zero-false-positive guard on "
            "disjoint corpora."
        ),
        "scaling": [],
        "fuzzy_hit_rate": [],
        "false_positive_audit": None,
    }

    # 1. Scaling sanity — disjoint corpora at N in {100, 1000, 10000}.
    for n in (100, 1000, 10000):
        corpus = generate_disjoint_corpus(n, rng=rng)
        exact_ms = measure_wall_ms(dedupe_by_endpoints, corpus)
        lsh_ms = measure_wall_ms(dedupe_by_endpoints_lsh, corpus)
        exact_out = dedupe_by_endpoints(corpus)
        lsh_out = dedupe_by_endpoints_lsh(corpus)
        results["scaling"].append({
            "n": n,
            "exact_wall_ms": round(exact_ms, 3),
            "lsh_wall_ms": round(lsh_ms, 3),
            "lsh_tax_ratio": round(lsh_ms / max(0.001, exact_ms), 2),
            "exact_out_count": len(exact_out),
            "lsh_out_count": len(lsh_out),
            "equivalence": len(exact_out) == len(lsh_out),
        })

    # 2. Fuzzy hit rate — inject fuzzy variants into 100-candidate
    # corpora at 10%, 20%, 30% injection rates.
    for fraction in (0.10, 0.20, 0.30):
        base = generate_disjoint_corpus(100, rng=rng)
        with_variants = inject_fuzzy_variants(base, fraction=fraction, rng=rng)
        metrics = measure_hit_rate(with_variants)
        metrics["injection_fraction"] = fraction
        results["fuzzy_hit_rate"].append(metrics)

    # 3. Zero-false-positive audit — fully-disjoint corpus, LSH
    # must NOT collapse anything.
    disjoint = generate_disjoint_corpus(200, rng=rng)
    exact_out = dedupe_by_endpoints(disjoint)
    lsh_out = dedupe_by_endpoints_lsh(disjoint)
    fp_count = max(0, len(exact_out) - len(lsh_out))
    results["false_positive_audit"] = {
        "n": 200,
        "exact_count": len(exact_out),
        "lsh_count": len(lsh_out),
        "false_positive_collapses": fp_count,
        "target": 0,
        "passed": fp_count == 0,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    print(f"bench_lsh_dedup: wrote {out_path}")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
