"""TTL Cache implementation for SherryAgent.

This module provides a thread-safe, async-compatible TTL (Time-To-Live) cache
with automatic expiration and size limits.
"""

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

K = TypeVar('K')
V = TypeVar('V')


@dataclass
class CacheEntry(Generic[V]):
    """Cache entry with expiration metadata."""
    value: V
    expires_at: float
    created_at: float


class TTLCache(Generic[K, V]):
    """Thread-safe TTL cache with automatic expiration.

    This cache supports:
    - Time-to-live (TTL) for entries
    - Maximum size limit with LRU-like eviction
    - Async-safe operations using locks
    - Statistics tracking (hits/misses)
    - Automatic cleanup of expired entries
    """

    def __init__(self, default_ttl: float = 60.0, max_size: int = 1000):
        """Initialize the TTL cache.

        Args:
            default_ttl: Default time-to-live in seconds for cache entries.
            max_size: Maximum number of entries in the cache.
        """
        self._cache: dict[K, CacheEntry[V]] = {}
        self._default_ttl = default_ttl
        self._max_size = max_size
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0

    async def get(self, key: K) -> V | None:
        """Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Cached value if exists and not expired, None otherwise.
        """
        async with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self._misses += 1
                return None

            current_time = time.time()
            if current_time > entry.expires_at:
                del self._cache[key]
                self._misses += 1
                return None

            self._hits += 1
            return entry.value

    async def set(self, key: K, value: V, ttl: float | None = None) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to cache.
            ttl: Time-to-live in seconds. Uses default_ttl if None.
        """
        async with self._lock:
            if len(self._cache) >= self._max_size and key not in self._cache:
                await self._evict_oldest()

            current_time = time.time()
            actual_ttl = ttl if ttl is not None else self._default_ttl

            self._cache[key] = CacheEntry(
                value=value,
                expires_at=current_time + actual_ttl,
                created_at=current_time
            )

    async def delete(self, key: K) -> bool:
        """Delete a value from the cache.

        Args:
            key: Cache key.

        Returns:
            True if the key was deleted, False if it didn't exist.
        """
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def clear(self) -> None:
        """Clear all entries from the cache."""
        async with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    async def cleanup_expired(self) -> int:
        """Remove all expired entries from the cache.

        Returns:
            Number of entries removed.
        """
        async with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if current_time > entry.expires_at
            ]

            for key in expired_keys:
                del self._cache[key]

            return len(expired_keys)

    def get_stats(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with cache statistics including:
            - size: Current number of entries
            - max_size: Maximum allowed entries
            - hits: Number of cache hits
            - misses: Number of cache misses
            - hit_rate: Cache hit rate (0.0 to 1.0)
        """
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

        return {
            'size': len(self._cache),
            'max_size': self._max_size,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': hit_rate
        }

    async def _evict_oldest(self) -> None:
        """Evict the oldest entry from the cache.

        This is called internally when the cache reaches max size.
        """
        if not self._cache:
            return

        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k].created_at
        )
        del self._cache[oldest_key]

    async def exists(self, key: K) -> bool:
        """Check if a key exists in the cache and is not expired.

        Args:
            key: Cache key.

        Returns:
            True if the key exists and is not expired, False otherwise.
        """
        async with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return False

            if time.time() > entry.expires_at:
                del self._cache[key]
                return False

            return True

    async def get_or_set(
        self,
        key: K,
        factory: Callable[[], Awaitable[V]],
        ttl: float | None = None
    ) -> V:
        """Get a value from cache, or compute and cache it if missing.

        Args:
            key: Cache key.
            factory: Async function to compute the value if not cached.
            ttl: Time-to-live in seconds. Uses default_ttl if None.

        Returns:
            Cached or computed value.
        """
        value = await self.get(key)
        if value is not None:
            return value

        computed_value = await factory()
        await self.set(key, computed_value, ttl)
        return computed_value
