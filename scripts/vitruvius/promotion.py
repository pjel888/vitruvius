from __future__ import annotations

import hashlib
import re

from .utils import utc_now_stamp


_SLUG_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    value = value.lower()
    value = _SLUG_NON_ALNUM.sub("-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def build_relationship_id(from_entity: str, predicate: str, to_entity: str) -> str:
    slug = slugify(f"{from_entity}-{predicate}-{to_entity}")
    return f"rel-{slug}"


def build_promotion_batch_id() -> str:
    stamp = utc_now_stamp()
    return f"{stamp}_{short_hash(stamp)}"
