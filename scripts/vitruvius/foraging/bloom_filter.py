"""Sprint GT Stream GT.5.2 — stdlib-only Bloom filter.

Uses ``hashlib.blake2b`` with distinct salts to derive
``hash_count`` independent hash functions, and stores the
bit-vector in a ``bytearray`` (no third-party bitarray
dependency). Intended for dropping redundant ingestion records
before they hit the engine.
"""
from __future__ import annotations

import hashlib


class BloomFilter:
    def __init__(self, size: int, hash_count: int) -> None:
        if size <= 0:
            raise ValueError(f"size must be positive (got {size})")
        if hash_count <= 0:
            raise ValueError(f"hash_count must be positive (got {hash_count})")
        self._size = int(size)
        self._hash_count = int(hash_count)
        byte_len = (self._size + 7) // 8
        self._bits = bytearray(byte_len)

    def _positions(self, item: str) -> list[int]:
        data = item.encode("utf-8")
        positions: list[int] = []
        for k in range(self._hash_count):
            salt = k.to_bytes(4, "little")
            digest = hashlib.blake2b(data + salt, digest_size=8).digest()
            positions.append(int.from_bytes(digest, "little") % self._size)
        return positions

    def add(self, item: str) -> None:
        for pos in self._positions(item):
            self._bits[pos // 8] |= 1 << (pos % 8)

    def contains(self, item: str) -> bool:
        for pos in self._positions(item):
            if not (self._bits[pos // 8] & (1 << (pos % 8))):
                return False
        return True
