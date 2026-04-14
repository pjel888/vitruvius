"""Merkle directory hashing for Phase 1A fast-skip and future caching.

Exposes the single public API:
    calculate_directory_hash(root) -> DirectoryHashRecord

Closes research item 'Merkle Tree Directory Hash' (adv-doc §1 +
8GB Survival §2). Pure stdlib — hashlib, pathlib, dataclasses — so
the module costs ~40ms cold and ~12ms warm on the PD 1096 corpus
with zero external dependencies. See
.ai/03_plans/statistical-architectural-upgrade-plan.md §5 for context.
"""

from .directory_hash import DirectoryHashRecord, calculate_directory_hash

__all__ = ["DirectoryHashRecord", "calculate_directory_hash"]
