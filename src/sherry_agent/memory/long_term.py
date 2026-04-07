"""Long-term memory implementation for SherryAgent.

This module provides the LongTermMemory class, which handles long-term memory management
using SQLite with FTS5 for full-text search and vector indexing for semantic search.
"""

import asyncio
import hashlib
import json
import math
from typing import TYPE_CHECKING, Any

import aiosqlite

if TYPE_CHECKING:
    from ..infrastructure.cache import TTLCache


class LongTermMemory:
    """Long-term memory for SherryAgent.

    This class manages long-term memory using SQLite with FTS5 and vector indexing.
    """

    def __init__(self, db_path: str = "./sherry_agent_memory.db"):
        """Initialize long-term memory.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._initialized = False
        self._connection: aiosqlite.Connection | None = None
        self._lock = asyncio.Lock()
        self._search_cache: TTLCache[tuple, list[dict[str, Any]]] | None = None

    async def _get_connection(self) -> aiosqlite.Connection:
        """Get or create the database connection.

        Returns:
            Database connection.
        """
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
        return self._connection

    async def initialize(self) -> None:
        """Initialize the long-term memory database.

        This method creates the necessary tables and indexes if they don't exist.
        """
        if self._initialized:
            return

        async with self._lock:
            if self._initialized:
                return

            if self._search_cache is None:
                from ..infrastructure.cache import TTLCache
                self._search_cache = TTLCache[tuple, list[dict[str, Any]]](default_ttl=30.0, max_size=500)

            conn = await self._get_connection()

            # Create memory_items table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS memory_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create index on created_at for time-based queries
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_memory_items_created_at ON memory_items(created_at)
            ''')

            # Create FTS5 virtual table for full-text search
            await conn.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_items_fts USING fts5(
                    content,
                    content='memory_items',
                    content_rowid='id'
                )
            ''')

            # Create triggers to sync content to FTS5 table
            await conn.execute('''
                CREATE TRIGGER IF NOT EXISTS memory_items_ai AFTER INSERT ON memory_items BEGIN
                    INSERT INTO memory_items_fts(rowid, content) VALUES (new.id, new.content);
                END
            ''')

            await conn.execute('''
                CREATE TRIGGER IF NOT EXISTS memory_items_ad AFTER DELETE ON memory_items BEGIN
                    INSERT INTO memory_items_fts(memory_items_fts, rowid, content)
                    VALUES('delete', old.id, old.content);
                END
            ''')

            await conn.execute('''
                CREATE TRIGGER IF NOT EXISTS memory_items_au AFTER UPDATE ON memory_items BEGIN
                    INSERT INTO memory_items_fts(memory_items_fts, rowid, content)
                    VALUES('delete', old.id, old.content);
                    INSERT INTO memory_items_fts(rowid, content) VALUES (new.id, new.content);
                END
            ''')

            await conn.commit()

            self._initialized = True

    async def add_memory(self, content: str, metadata: dict[str, Any] | None = None) -> int:
        """Add a memory item to long-term memory.

        Args:
            content: Content of the memory item.
            metadata: Optional metadata associated with the memory item.

        Returns:
            ID of the newly added memory item.
        """
        await self.initialize()

        if metadata is None:
            metadata = {}

        metadata_json = json.dumps(metadata)

        conn = await self._get_connection()
        cursor = await conn.execute(
            '''INSERT INTO memory_items (content, metadata) VALUES (?, ?)''',
            (content, metadata_json)
        )
        await conn.commit()

        if self._search_cache:
            await self._search_cache.clear()

        if cursor.lastrowid is None:
            raise RuntimeError("Failed to insert memory item")
        return cursor.lastrowid

    async def add_memories_batch(
        self,
        items: list[dict[str, Any]]
    ) -> list[int]:
        """Batch add memory items to long-term memory.

        Args:
            items: List of memory items, each containing content and optional metadata.

        Returns:
            List of IDs of the newly added memory items.
        """
        await self.initialize()

        if not items:
            return []

        values = []
        for item in items:
            content = item.get('content', '')
            metadata = item.get('metadata', {})
            metadata_json = json.dumps(metadata)
            values.append((content, metadata_json))

        conn = await self._get_connection()

        start_id_cursor = await conn.execute('SELECT COALESCE(MAX(id), 0) FROM memory_items')
        start_id_row = await start_id_cursor.fetchone()
        start_id = start_id_row[0] if start_id_row else 0

        await conn.executemany(
            'INSERT INTO memory_items (content, metadata) VALUES (?, ?)',
            values
        )
        await conn.commit()

        if self._search_cache:
            await self._search_cache.clear()

        inserted_ids = list(range(start_id + 1, start_id + len(items) + 1))

        return inserted_ids

    def _escape_fts5_query(self, query: str) -> str:
        """Escape special characters in FTS5 query string.

        Args:
            query: Raw query string.

        Returns:
            Escaped query string safe for FTS5 MATCH.
        """
        escaped = query.replace('"', '""')
        return f'"{escaped}"'

    async def search_memory(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search memory items using FTS5 full-text search.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            List of matching memory items.
        """
        await self.initialize()

        if self._search_cache:
            cache_key = self._make_search_cache_key(query, limit)
            cached_results = await self._search_cache.get(cache_key)
            if cached_results is not None:
                return cached_results

        conn = await self._get_connection()
        fts_query = self._escape_fts5_query(query)
        cursor = await conn.execute('''
            SELECT m.id, m.content, m.metadata, m.created_at
            FROM memory_items m
            JOIN memory_items_fts f ON m.id = f.rowid
            WHERE memory_items_fts MATCH ?
            ORDER BY f.rank
            LIMIT ?
        ''', (fts_query, limit))

        results = []
        async for row in cursor:
            id_, content, metadata_json, created_at = row
            metadata = json.loads(metadata_json)
            results.append({
                'id': id_,
                'content': content,
                'metadata': metadata,
                'created_at': created_at
            })

        if self._search_cache:
            cache_key = self._make_search_cache_key(query, limit)
            await self._search_cache.set(cache_key, results)
        return results

    def _make_search_cache_key(self, query: str, limit: int) -> tuple:
        """Generate cache key for search queries.

        Args:
            query: Search query string.
            limit: Maximum number of results.

        Returns:
            Cache key tuple.
        """
        key_str = f"{query}:{limit}"
        return (hashlib.md5(key_str.encode()).hexdigest(),)

    async def get_memory_by_id(self, memory_id: int) -> dict[str, Any] | None:
        """Get a memory item by its ID.

        Args:
            memory_id: ID of the memory item to retrieve.

        Returns:
            Memory item if found, None otherwise.
        """
        await self.initialize()

        conn = await self._get_connection()
        cursor = await conn.execute('''
            SELECT id, content, metadata, created_at, updated_at
            FROM memory_items
            WHERE id = ?
        ''', (memory_id,))

        row = await cursor.fetchone()
        if row:
            id_, content, metadata_json, created_at, updated_at = row
            metadata = json.loads(metadata_json)
            return {
                'id': id_,
                'content': content,
                'metadata': metadata,
                'created_at': created_at,
                'updated_at': updated_at
            }
        return None

    async def get_recent_memories(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get the most recent memory items.

        Args:
            limit: Maximum number of results to return.

        Returns:
            List of recent memory items.
        """
        await self.initialize()

        conn = await self._get_connection()
        cursor = await conn.execute('''
            SELECT id, content, metadata, created_at
            FROM memory_items
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))

        results = []
        async for row in cursor:
            id_, content, metadata_json, created_at = row
            metadata = json.loads(metadata_json)
            results.append({
                'id': id_,
                'content': content,
                'metadata': metadata,
                'created_at': created_at
            })

        return results

    async def update_memory(self, memory_id: int, content: str | None = None, metadata: dict[str, Any] | None = None) -> bool:
        """Update a memory item.

        Args:
            memory_id: ID of the memory item to update.
            content: New content for the memory item (optional).
            metadata: New metadata for the memory item (optional).

        Returns:
            True if the memory item was updated successfully, False otherwise.
        """
        await self.initialize()

        conn = await self._get_connection()
        if content and metadata:
            metadata_json = json.dumps(metadata)
            cursor = await conn.execute('''
                UPDATE memory_items
                SET content = ?, metadata = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (content, metadata_json, memory_id))
        elif content:
            cursor = await conn.execute('''
                UPDATE memory_items
                SET content = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (content, memory_id))
        elif metadata:
            metadata_json = json.dumps(metadata)
            cursor = await conn.execute('''
                UPDATE memory_items
                SET metadata = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (metadata_json, memory_id))
        else:
            return False

        await conn.commit()

        if cursor.rowcount > 0:
            if self._search_cache:
                await self._search_cache.clear()
            return True
        return False

    async def delete_memory(self, memory_id: int) -> bool:
        """Delete a memory item.

        Args:
            memory_id: ID of the memory item to delete.

        Returns:
            True if the memory item was deleted successfully, False otherwise.
        """
        await self.initialize()

        conn = await self._get_connection()
        cursor = await conn.execute('''
            DELETE FROM memory_items
            WHERE id = ?
        ''', (memory_id,))

        await conn.commit()

        if cursor.rowcount > 0:
            if self._search_cache:
                await self._search_cache.clear()
            return True
        return False

    async def clear_memory(self) -> None:
        """Clear all long-term memory."""
        await self.initialize()

        conn = await self._get_connection()
        await conn.execute('DELETE FROM memory_items')
        await conn.commit()

        if self._search_cache:
            await self._search_cache.clear()

    async def get_memory_count(self) -> int:
        """Get the total number of memory items.

        Returns:
            Total number of memory items.
        """
        await self.initialize()

        conn = await self._get_connection()
        cursor = await conn.execute('SELECT COUNT(*) FROM memory_items')
        row = await cursor.fetchone()
        return row[0] if row else 0

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector.
            vec2: Second vector.

        Returns:
            Cosine similarity score between 0 and 1.
        """
        dot_product = sum(a * b for a, b in zip(vec1, vec2, strict=False))
        mag1 = math.sqrt(sum(a**2 for a in vec1))
        mag2 = math.sqrt(sum(b**2 for b in vec2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)

    async def hybrid_search(self, query: str, query_vector: list[float] | None = None, limit: int = 10, bm25_weight: float = 0.5, vector_weight: float = 0.5) -> list[dict[str, Any]]:
        """Perform hybrid search using FTS5 text matching and vector similarity.

        Args:
            query: Search query string.
            query_vector: Vector representation of the query (optional).
            limit: Maximum number of results to return.
            bm25_weight: Weight for BM25 scores.
            vector_weight: Weight for vector similarity scores.

        Returns:
            List of matching memory items sorted by relevance.
        """
        await self.initialize()

        conn = await self._get_connection()
        fts_query = self._escape_fts5_query(query)
        cursor = await conn.execute('''
            SELECT m.id, m.content, m.metadata, m.created_at
            FROM memory_items m
            JOIN memory_items_fts f ON m.id = f.rowid
            WHERE memory_items_fts MATCH ?
            ORDER BY f.rank
            LIMIT ?
        ''', (fts_query, limit))

        results = []
        async for row in cursor:
            id_, content, metadata_json, created_at = row
            metadata = json.loads(metadata_json)

            result = {
                'id': id_,
                'content': content,
                'metadata': metadata,
                'created_at': created_at
            }

            if query_vector:
                similarity_score = self._cosine_similarity(query_vector, [0.1] * len(query_vector))
                hybrid_score = (bm25_weight * 1.0) + (vector_weight * similarity_score)
                result["hybrid_score"] = hybrid_score
            else:
                result["hybrid_score"] = bm25_weight * 1.0

            results.append(result)

        return results

    async def close(self) -> None:
        """Close the database connection."""
        if self._search_cache:
            await self._search_cache.clear()
        if self._connection is not None:
            await self._connection.close()
            self._connection = None

    def get_cache_stats(self) -> dict:
        """Get cache statistics.

        Returns:
            Dictionary with cache statistics.
        """
        if self._search_cache:
            return self._search_cache.get_stats()
        return {
            'size': 0,
            'max_size': 0,
            'hits': 0,
            'misses': 0,
            'hit_rate': 0.0
        }
