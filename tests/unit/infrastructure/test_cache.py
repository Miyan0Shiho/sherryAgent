"""Unit tests for TTLCache class."""

import asyncio
import time
import pytest

from sherry_agent.infrastructure.cache import TTLCache, CacheEntry


class TestTTLCache:
    """Test cases for TTLCache class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cache = TTLCache[str, int](default_ttl=1.0, max_size=10)

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        """Test basic set and get operations."""
        await self.cache.set("key1", 100)
        value = await self.cache.get("key1")
        assert value == 100

    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self):
        """Test getting a nonexistent key."""
        value = await self.cache.get("nonexistent")
        assert value is None

    @pytest.mark.asyncio
    async def test_get_expired_key(self):
        """Test getting an expired key."""
        await self.cache.set("key1", 100, ttl=0.1)
        
        await asyncio.sleep(0.15)
        
        value = await self.cache.get("key1")
        assert value is None

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test deleting a key."""
        await self.cache.set("key1", 100)
        
        deleted = await self.cache.delete("key1")
        assert deleted is True
        
        value = await self.cache.get("key1")
        assert value is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_key(self):
        """Test deleting a nonexistent key."""
        deleted = await self.cache.delete("nonexistent")
        assert deleted is False

    @pytest.mark.asyncio
    async def test_clear(self):
        """Test clearing the cache."""
        await self.cache.set("key1", 100)
        await self.cache.set("key2", 200)
        
        await self.cache.clear()
        
        stats = self.cache.get_stats()
        assert stats['size'] == 0
        assert stats['hits'] == 0
        assert stats['misses'] == 0
        
        assert await self.cache.get("key1") is None
        assert await self.cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_cleanup_expired(self):
        """Test cleaning up expired entries."""
        await self.cache.set("key1", 100, ttl=0.1)
        await self.cache.set("key2", 200, ttl=0.1)
        await self.cache.set("key3", 300, ttl=10.0)
        
        await asyncio.sleep(0.15)
        
        removed = await self.cache.cleanup_expired()
        assert removed == 2
        
        stats = self.cache.get_stats()
        assert stats['size'] == 1

    @pytest.mark.asyncio
    async def test_get_stats(self):
        """Test getting cache statistics."""
        await self.cache.set("key1", 100)
        
        await self.cache.get("key1")
        await self.cache.get("key1")
        await self.cache.get("nonexistent")
        
        stats = self.cache.get_stats()
        assert stats['size'] == 1
        assert stats['max_size'] == 10
        assert stats['hits'] == 2
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 2 / 3

    @pytest.mark.asyncio
    async def test_max_size_eviction(self):
        """Test that cache evicts oldest entries when max size is reached."""
        small_cache = TTLCache[str, int](default_ttl=10.0, max_size=3)
        
        await small_cache.set("key1", 100)
        await asyncio.sleep(0.01)
        await small_cache.set("key2", 200)
        await asyncio.sleep(0.01)
        await small_cache.set("key3", 300)
        await asyncio.sleep(0.01)
        await small_cache.set("key4", 400)
        
        stats = small_cache.get_stats()
        assert stats['size'] == 3
        
        assert await small_cache.get("key1") is None
        assert await small_cache.get("key2") is not None
        assert await small_cache.get("key3") is not None
        assert await small_cache.get("key4") is not None

    @pytest.mark.asyncio
    async def test_exists(self):
        """Test checking if a key exists."""
        await self.cache.set("key1", 100)
        
        assert await self.cache.exists("key1") is True
        assert await self.cache.exists("nonexistent") is False

    @pytest.mark.asyncio
    async def test_exists_expired(self):
        """Test checking if an expired key exists."""
        await self.cache.set("key1", 100, ttl=0.1)
        
        await asyncio.sleep(0.15)
        
        assert await self.cache.exists("key1") is False

    @pytest.mark.asyncio
    async def test_get_or_set(self):
        """Test get_or_set method."""
        call_count = 0
        
        async def factory():
            nonlocal call_count
            call_count += 1
            return 100
        
        value1 = await self.cache.get_or_set("key1", factory)
        assert value1 == 100
        assert call_count == 1
        
        value2 = await self.cache.get_or_set("key1", factory)
        assert value2 == 100
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_get_or_set_with_ttl(self):
        """Test get_or_set method with custom TTL."""
        call_count = 0
        
        async def factory():
            nonlocal call_count
            call_count += 1
            return 100
        
        value1 = await self.cache.get_or_set("key1", factory, ttl=0.1)
        assert value1 == 100
        assert call_count == 1
        
        await asyncio.sleep(0.15)
        
        value2 = await self.cache.get_or_set("key1", factory)
        assert value2 == 100
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_update_existing_key(self):
        """Test updating an existing key."""
        await self.cache.set("key1", 100)
        await self.cache.set("key1", 200)
        
        value = await self.cache.get("key1")
        assert value == 200
        
        stats = self.cache.get_stats()
        assert stats['size'] == 1

    @pytest.mark.asyncio
    async def test_default_ttl(self):
        """Test that default TTL is used when not specified."""
        cache = TTLCache[str, int](default_ttl=0.2, max_size=10)
        
        await cache.set("key1", 100)
        
        await asyncio.sleep(0.1)
        value = await cache.get("key1")
        assert value == 100
        
        await asyncio.sleep(0.15)
        value = await cache.get("key1")
        assert value is None

    @pytest.mark.asyncio
    async def test_concurrent_access(self):
        """Test concurrent access to the cache."""
        async def set_value(key: str, value: int):
            await self.cache.set(key, value)
        
        async def get_value(key: str) -> int | None:
            return await self.cache.get(key)
        
        tasks = []
        for i in range(10):
            tasks.append(set_value(f"key{i}", i))
        
        await asyncio.gather(*tasks)
        
        stats = self.cache.get_stats()
        assert stats['size'] == 10
        
        for i in range(10):
            value = await get_value(f"key{i}")
            assert value == i


class TestCacheEntry:
    """Test cases for CacheEntry dataclass."""

    def test_cache_entry_creation(self):
        """Test creating a cache entry."""
        current_time = time.time()
        entry = CacheEntry(
            value="test_value",
            expires_at=current_time + 60.0,
            created_at=current_time
        )
        
        assert entry.value == "test_value"
        assert entry.expires_at == current_time + 60.0
        assert entry.created_at == current_time
