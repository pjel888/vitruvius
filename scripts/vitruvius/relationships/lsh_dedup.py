"""Sprint LSH-1 Task 3 — LSH-based relationship fuzzy dedup.

Fuzzy near-duplicate layer on top of
:func:`vitruvius.relationships_sections.dedupe_by_endpoints` (the
existing O(n log n) dict-grouped exact-endpoint dedup per AD-037).

**Why a fuzzy layer?** The existing exact-endpoint dedup groups by
``(from_id, to_id)`` and keeps one winner per group. What it cannot
catch is *semantic* near-duplicates — two relationship candidates
that refer to the same real-world constraint but express it with
slightly different subject or object slugs:

    {from: "concept-lot-area",         type: "requires", to: "concept-100-sqm"}
    {from: "concept-minimum-lot-area", type: "requires", to: "concept-100-sqm"}

The endpoint keys differ, so the exact dedup keeps both. A human
reading the review queue sees two candidates that mean the same
thing, inflating review queue length without adding information.

**How the LSH layer works.**

1. For each candidate, extract a feature set (4-gram shingles of
   ``from + type + to`` + the raw triple tokens). Small numerical
   variants and slug prefix differences leave most shingles shared.
2. Compute an ``(num_perm,)`` MinHash signature per candidate.
3. Build a band-based LSH index; two candidates collide in the index
   iff they share at least one band's values (approximates Jaccard
   >= threshold per the band rule of thumb).
4. Walk the connected components of the collision graph: any two
   candidates that collide land in the same component. Pick the
   highest-occurrence candidate per component as the representative.
5. Run the final representative list through the exact-endpoint
   dedup (a byte-equivalent delegate for corpora where no fuzzy
   duplicates exist — the equivalence guarantee in Task 3's test
   suite).

**Language/runtime choice.** Per AD-037 this module stays in Python
(pure stdlib + numpy via the minhash/lsh_index primitives). Near-
duplicate dedup runs once per ingestion batch, not in a hot loop, so
the pyo3 FFI overhead + Rust maintenance cost is not justified. The
same measurement-first discipline that drove AD-036 and AD-038.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from vitruvius.relationships.lsh_index import LSHIndex
from vitruvius.relationships.minhash import compute_minhash_signature
from vitruvius.relationships_sections import dedupe_by_endpoints


def _candidate_features(candidate: dict) -> set[str]:
    """Extract a feature set from a relationship candidate.

    The feature set is what MinHash will compare. We include:

    - ``type:<pred>`` — explicit predicate token. This is critical
      for the disjoint false-positive guard: two relationships with
      different predicates must NOT share this anchor feature.
    - Word-level tokens split on ``-`` — ``tok:<word>`` for each
      non-empty component of ``from`` and ``to``. This boosts
      Jaccard for candidates that share individual word tokens
      (e.g. ``lot-area`` and ``minimum-lot-area`` share ``lot`` and
      ``area``) even when the slug-string shingle overlap is
      borderline.
    - 4-gram shingles of the concatenated text
      ``f"{from}|{type}|{to}"``. Slug prefix variants like
      ``lot-area`` vs ``minimum-lot-area`` share most of their 4-grams
      but differ just enough that shingles alone wouldn't collide
      them reliably.
    - 4-gram shingles of each section id (if any). Candidates quoting
      the same section tend to be near-duplicates regardless of
      exactly how the slug was canonicalized.

    Missing fields are tolerated — the resulting signature just has
    fewer distinctive features.
    """
    features: set[str] = set()

    from_id = str(candidate.get("from") or "")
    to_id = str(candidate.get("to") or "")
    pred = str(candidate.get("type") or "")

    if pred:
        features.add(f"type:{pred}")

    for raw in (from_id, to_id):
        for token in raw.lower().split("-"):
            if len(token) >= 2:
                features.add(f"tok:{token}")

    slug_text = f"{from_id}|{pred}|{to_id}".lower()
    for i in range(max(0, len(slug_text) - 3)):
        features.add(f"sg:{slug_text[i : i + 4]}")

    sections = candidate.get("sections") or ()
    if isinstance(sections, list):
        for section in sections:
            if not isinstance(section, str):
                continue
            for i in range(max(0, len(section) - 3)):
                features.add(f"sec:{section[i : i + 4]}")

    return features


def _connected_components(
    num_candidates: int,
    adjacency: dict[int, set[int]],
) -> list[list[int]]:
    """Return the connected components of the collision graph.

    Uses a union-find pass so that if A collides with B and B with C,
    all three land in the same component even if A and C don't share
    any band directly. This is the standard "transitive closure of
    fuzzy equivalence" mental model.
    """
    parent = list(range(num_candidates))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for i, neighbours in adjacency.items():
        for j in neighbours:
            union(i, j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(num_candidates):
        groups[find(i)].append(i)
    return list(groups.values())


def _pick_representative(
    candidates: list[dict],
    member_indices: list[int],
) -> dict:
    """Pick the representative candidate from a fuzzy-duplicate group.

    Tie-break rules (high -> low priority):
    1. Highest ``occurrences`` wins.
    2. On tie, longest section list wins (more evidence).
    3. On tie, earliest index in the input list wins (stable).
    """
    def sort_key(idx: int) -> tuple:
        c = candidates[idx]
        return (
            -int(c.get("occurrences", 0)),
            -len(c.get("sections", []) or []),
            idx,
        )

    winner_idx = min(member_indices, key=sort_key)
    return candidates[winner_idx]


def dedupe_by_endpoints_lsh(
    candidates: Iterable[dict],
    *,
    num_perm: int = 256,
    num_bands: int = 32,
    seed: int = 0,
) -> list[dict]:
    """Dedup relationship candidates via MinHash LSH fuzzy near-duplicate layer.

    Two-layer algorithm:

    1. **LSH fuzzy layer.** Build a MinHash LSH index over candidate
       feature sets, walk the connected components of the collision
       graph, and keep one representative per component (highest
       ``occurrences``, then longest section list, then stable index).
    2. **Exact-endpoint delegation.** Run the representative list
       through the existing :func:`dedupe_by_endpoints` for the final
       ``(from, to)`` group selection. On corpora where no fuzzy
       duplicates exist the LSH layer is a no-op and the return is
       byte-equivalent to :func:`dedupe_by_endpoints` on the same
       input (the equivalence test guards this).

    Args:
        candidates: Iterable of candidate dicts. Each must carry at
            least ``from``, ``type``, ``to`` keys; ``occurrences``,
            ``sections``, ``examples`` are used when present.
        num_perm: MinHash permutation count.
        num_bands: Number of LSH bands. ``num_perm / num_bands`` must
            be a positive integer.
        seed: Hash-family seed. Fixing the seed makes the output
            deterministic across runs.

    Returns:
        A new list of deduped candidate dicts with the same keys the
        exact-endpoint path emits.
    """
    candidates_list = list(candidates)
    if not candidates_list:
        return []
    if len(candidates_list) == 1:
        # Delegate to the exact path so the single-candidate return
        # has the ``alternate_predicates`` field the downstream
        # pipeline expects.
        return dedupe_by_endpoints(candidates_list)

    # Step 1: compute MinHash signatures per candidate.
    signatures = [
        compute_minhash_signature(
            _candidate_features(c), num_perm=num_perm, seed=seed
        )
        for c in candidates_list
    ]

    # Step 2: build LSH index + collision adjacency.
    index = LSHIndex(num_perm=num_perm, num_bands=num_bands)
    for i, sig in enumerate(signatures):
        index.add(original_index=i, signature=sig)

    adjacency: dict[int, set[int]] = defaultdict(set)
    for i, sig in enumerate(signatures):
        for j in index.query_candidates(sig):
            if j != i:
                adjacency[i].add(j)

    # Step 3: walk connected components + pick representatives.
    components = _connected_components(len(candidates_list), adjacency)
    representatives = [
        _pick_representative(candidates_list, comp) for comp in components
    ]

    # Step 4: delegate to the exact-endpoint path for the final
    # ``(from, to)`` dedup pass. This preserves the exact-endpoint
    # equivalence guarantee: on corpora where every candidate sits
    # alone in its own LSH component, this call returns the same
    # set of triples as running ``dedupe_by_endpoints`` directly on
    # the input.
    return dedupe_by_endpoints(representatives)
