"""Sprint GT Stream GT.5.2 — Bloom filter for ingestion dedup."""
from __future__ import annotations

import random

import pytest

from vitruvius.foraging.bloom_filter import BloomFilter


def test_contains_returns_false_before_add() -> None:
    bf = BloomFilter(size=1024, hash_count=4)
    assert bf.contains("hello") is False


def test_add_then_contains_returns_true() -> None:
    bf = BloomFilter(size=1024, hash_count=4)
    bf.add("hello")
    assert bf.contains("hello") is True


def test_many_items_reproducible() -> None:
    bf = BloomFilter(size=10000, hash_count=5)
    for i in range(100):
        bf.add(f"item-{i}")
    for i in range(100):
        assert bf.contains(f"item-{i}") is True


def test_false_positive_rate_under_5_percent() -> None:
    random.seed(42)
    bf = BloomFilter(size=10000, hash_count=7)
    inserted = {f"inserted-{i}" for i in range(1000)}
    for item in inserted:
        bf.add(item)

    false_positives = 0
    trials = 2000
    for i in range(trials):
        probe = f"probe-{i}"
        if probe in inserted:
            continue
        if bf.contains(probe):
            false_positives += 1

    rate = false_positives / trials
    assert rate < 0.05, f"false positive rate {rate:.3%} exceeds 5% budget"


def test_invalid_size_raises() -> None:
    with pytest.raises(ValueError):
        BloomFilter(size=0, hash_count=4)
    with pytest.raises(ValueError):
        BloomFilter(size=1024, hash_count=0)
