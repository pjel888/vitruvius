"""Sprint CLEANUP-1 Stream C2.1 — phrase-density definition extractor.

For concepts whose definitions are not anchor-style (e.g. "shall mean")
and are not captured by section-title matching, this extractor scans
for paragraphs where the slug or an alias occurs above a density
threshold (mentions per 500 chars) and returns them as candidates.

The current 4 targets in PD 1096: exit-width, parking-and-loading-spaces,
setbacks, yards. All four are discussed across multiple paragraphs that
describe the concept without explicitly defining it — density is the
only signal we have.

Gated behind `p3_density_extractor` in config/vitruvius.yaml.

Perf call: pure string scan, above the Rust Line (AD-036). Python is
the correct choice; this is called at most a few dozen times per
enrichment run.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DensityCandidate:
    slug: str
    definition: str
    density: float  # mentions per window_chars
    start_offset: int


_PARAGRAPH_SPLIT = re.compile(r"\n\s*\n")


def extract_definitions_by_density(
    *,
    text: str,
    slug: str,
    aliases: List[str],
    min_density: float = 2.0,
    window_chars: int = 500,
) -> List[DensityCandidate]:
    """Return DensityCandidate objects for paragraphs where
    `slug` or any of `aliases` occurs with density >= min_density
    per `window_chars` characters.

    Sorted by density (highest first).
    """
    search_terms = [slug.replace("-", " ").lower()] + [a.lower() for a in aliases]
    patterns = [re.compile(r"\b" + re.escape(term) + r"s?\b", re.IGNORECASE) for term in search_terms]

    candidates: List[DensityCandidate] = []
    offset = 0
    for para in _PARAGRAPH_SPLIT.split(text):
        length = len(para)
        if length == 0:
            offset += 2  # approximate paragraph separator
            continue
        mentions = sum(len(p.findall(para)) for p in patterns)
        if mentions == 0:
            offset += length + 2
            continue
        # Use max(length, window_chars) so very short paragraphs cannot
        # extrapolate a false-high density. A paragraph shorter than one
        # window is measured as mentions-per-window directly.
        density = mentions * window_chars / max(length, window_chars)
        if density >= min_density:
            candidates.append(
                DensityCandidate(
                    slug=slug,
                    definition=para.strip(),
                    density=density,
                    start_offset=offset,
                )
            )
        offset += length + 2

    candidates.sort(key=lambda c: c.density, reverse=True)
    return candidates
