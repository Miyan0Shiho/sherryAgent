"""Unit tests for LongTermMemory class."""

import os
import tempfile
import pytest
from sherry_agent.memory.long_term import LongTermMemory


def run_async(coro):
    """Run an async coroutine synchronously."""
    import asyncio
    return asyncio.run(coro)


class TestLongTermMemory:
    """Test cases for LongTermMemory class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary file for the database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            self.db_path = temp_file.name

        self.memory = LongTermMemory(db_path=self.db_path)
        run_async(self.memory.initialize())

    def teardown_method(self):
        """Clean up test fixtures."""
        # Close the connection
        run_async(self.memory.close())
        
        # Clean up the temporary file
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_add_memory(self):
        """Test adding a memory item."""
        content = "This is a test memory"
        metadata = {"category": "test", "priority": "high"}

        memory_id = run_async(self.memory.add_memory(content, metadata))

        assert memory_id > 0
        assert run_async(self.memory.get_memory_count()) == 1

    def test_get_memory_by_id(self):
        """Test retrieving a memory item by ID."""
        content = "Test memory for retrieval"
        metadata = {"test": "value"}

        memory_id = run_async(self.memory.add_memory(content, metadata))
        retrieved_memory = run_async(self.memory.get_memory_by_id(memory_id))

        assert retrieved_memory is not None
        assert retrieved_memory["id"] == memory_id
        assert retrieved_memory["content"] == content
        assert retrieved_memory["metadata"] == metadata

    def test_get_memory_by_id_nonexistent(self):
        """Test retrieving a nonexistent memory item."""
        retrieved_memory = run_async(self.memory.get_memory_by_id(999))
        assert retrieved_memory is None

    def test_search_memory(self):
        """Test searching memory items using FTS5."""
        run_async(self.memory.add_memory("This is a test about Python programming"))
        run_async(self.memory.add_memory("This is a test about JavaScript"))
        run_async(self.memory.add_memory("This is a test about SQL databases"))

        results = run_async(self.memory.search_memory("Python"))
        assert len(results) == 1
        assert "Python" in results[0]["content"]

        results = run_async(self.memory.search_memory("test"))
        assert len(results) == 3

    def test_fts5_phrase_search(self):
        """Test FTS5 phrase search functionality."""
        run_async(self.memory.add_memory("Machine learning is fascinating"))
        run_async(self.memory.add_memory("Deep learning is a subset of machine learning"))
        run_async(self.memory.add_memory("Natural language processing"))

        results = run_async(self.memory.search_memory("machine learning"))
        assert len(results) >= 1
        for result in results:
            assert "machine" in result["content"].lower() or "learning" in result["content"].lower()

    def test_fts5_special_characters(self):
        """Test FTS5 query with special characters."""
        run_async(self.memory.add_memory('Content with "quotes" inside'))
        run_async(self.memory.add_memory("Normal content"))

        results = run_async(self.memory.search_memory("quotes"))
        assert len(results) == 1
        assert "quotes" in results[0]["content"]

    def test_fts5_sync_on_update(self):
        """Test that FTS5 index is synced when memory is updated."""
        memory_id = run_async(self.memory.add_memory("Original content about Python"))

        results = run_async(self.memory.search_memory("JavaScript"))
        assert len(results) == 0

        run_async(self.memory.update_memory(memory_id, content="Updated content about JavaScript"))

        results = run_async(self.memory.search_memory("JavaScript"))
        assert len(results) == 1
        assert "JavaScript" in results[0]["content"]

        results = run_async(self.memory.search_memory("Python"))
        assert len(results) == 0

    def test_fts5_sync_on_delete(self):
        """Test that FTS5 index is synced when memory is deleted."""
        memory_id = run_async(self.memory.add_memory("Unique keyword XYZ123"))

        results = run_async(self.memory.search_memory("XYZ123"))
        assert len(results) == 1

        run_async(self.memory.delete_memory(memory_id))

        results = run_async(self.memory.search_memory("XYZ123"))
        assert len(results) == 0

    def test_get_recent_memories(self):
        """Test retrieving recent memory items."""
        # Add test memories
        for i in range(5):
            run_async(self.memory.add_memory(f"Memory {i}"))

        recent_memories = run_async(self.memory.get_recent_memories(3))
        assert len(recent_memories) == 3
        assert recent_memories[0]["content"] == "Memory 4"  # Most recent
        assert recent_memories[1]["content"] == "Memory 3"
        assert recent_memories[2]["content"] == "Memory 2"

    def test_update_memory(self):
        """Test updating a memory item."""
        original_content = "Original content"
        memory_id = run_async(self.memory.add_memory(original_content))

        # Update content
        new_content = "Updated content"
        updated = run_async(self.memory.update_memory(memory_id, content=new_content))
        assert updated is True

        retrieved_memory = run_async(self.memory.get_memory_by_id(memory_id))
        assert retrieved_memory["content"] == new_content

        # Update metadata
        new_metadata = {"updated": True}
        updated = run_async(self.memory.update_memory(memory_id, metadata=new_metadata))
        assert updated is True

        retrieved_memory = run_async(self.memory.get_memory_by_id(memory_id))
        assert retrieved_memory["metadata"] == new_metadata

        # Update both content and metadata
        new_content_2 = "Updated content 2"
        new_metadata_2 = {"updated": True, "version": 2}
        updated = run_async(self.memory.update_memory(memory_id, content=new_content_2, metadata=new_metadata_2))
        assert updated is True

        retrieved_memory = run_async(self.memory.get_memory_by_id(memory_id))
        assert retrieved_memory["content"] == new_content_2
        assert retrieved_memory["metadata"] == new_metadata_2

    def test_update_memory_nonexistent(self):
        """Test updating a nonexistent memory item."""
        updated = run_async(self.memory.update_memory(999, content="Updated content"))
        assert updated is False

    def test_delete_memory(self):
        """Test deleting a memory item."""
        content = "Memory to be deleted"
        memory_id = run_async(self.memory.add_memory(content))

        deleted = run_async(self.memory.delete_memory(memory_id))
        assert deleted is True
        assert run_async(self.memory.get_memory_count()) == 0

        # Verify the memory is gone
        retrieved_memory = run_async(self.memory.get_memory_by_id(memory_id))
        assert retrieved_memory is None

    def test_delete_memory_nonexistent(self):
        """Test deleting a nonexistent memory item."""
        deleted = run_async(self.memory.delete_memory(999))
        assert deleted is False

    def test_clear_memory(self):
        """Test clearing all memory."""
        # Add some test memories
        for i in range(3):
            run_async(self.memory.add_memory(f"Memory {i}"))

        assert run_async(self.memory.get_memory_count()) == 3

        run_async(self.memory.clear_memory())

        assert run_async(self.memory.get_memory_count()) == 0
        assert len(run_async(self.memory.get_recent_memories())) == 0

    def test_get_memory_count(self):
        """Test getting the memory count."""
        assert run_async(self.memory.get_memory_count()) == 0

        # Add some memories
        for i in range(5):
            run_async(self.memory.add_memory(f"Memory {i}"))

        assert run_async(self.memory.get_memory_count()) == 5

        # Delete one memory
        memory_id = run_async(self.memory.add_memory("Memory to delete"))
        assert run_async(self.memory.get_memory_count()) == 6

        run_async(self.memory.delete_memory(memory_id))
        assert run_async(self.memory.get_memory_count()) == 5

    def test_hybrid_search_without_vector(self):
        """Test hybrid search without vector using FTS5."""
        run_async(self.memory.add_memory("This is a test about Python programming"))
        run_async(self.memory.add_memory("This is a test about JavaScript"))
        run_async(self.memory.add_memory("This is a test about SQL databases"))

        results = run_async(self.memory.hybrid_search("Python"))
        assert len(results) == 1
        assert "Python" in results[0]["content"]

        results = run_async(self.memory.hybrid_search("test"))
        assert len(results) == 3

    def test_hybrid_search_with_vector(self):
        """Test hybrid search with vector using FTS5."""
        run_async(self.memory.add_memory("This is a test about Python programming"))
        run_async(self.memory.add_memory("This is a test about JavaScript"))
        run_async(self.memory.add_memory("This is a test about SQL databases"))

        query_vector = [0.1, 0.2, 0.3, 0.4, 0.5]

        results = run_async(self.memory.hybrid_search("Python", query_vector=query_vector))
        assert len(results) > 0
        for result in results:
            assert "hybrid_score" in result

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [1.0, 2.0, 3.0]
        # Identical vectors should have similarity 1.0
        assert self.memory._cosine_similarity(vec1, vec2) == 1.0

        vec3 = [1.0, 0.0, 0.0]
        vec4 = [0.0, 1.0, 0.0]
        # Orthogonal vectors should have similarity 0.0
        assert self.memory._cosine_similarity(vec3, vec4) == 0.0

    def test_search_memory_caching(self):
        """Test that search_memory uses caching."""
        run_async(self.memory.add_memory("This is a test about Python programming"))
        
        results1 = run_async(self.memory.search_memory("Python"))
        assert len(results1) == 1
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 1
        assert stats['hits'] == 0
        
        results2 = run_async(self.memory.search_memory("Python"))
        assert len(results2) == 1
        
        stats = self.memory.get_cache_stats()
        assert stats['hits'] == 1

    def test_cache_invalidation_on_add(self):
        """Test that cache is invalidated when adding new memory."""
        run_async(self.memory.add_memory("This is a test about Python"))
        
        run_async(self.memory.search_memory("Python"))
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 1
        
        run_async(self.memory.add_memory("This is another test about Python"))
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 0

    def test_cache_invalidation_on_update(self):
        """Test that cache is invalidated when updating memory."""
        memory_id = run_async(self.memory.add_memory("Original content"))
        
        run_async(self.memory.search_memory("Original"))
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 1
        
        run_async(self.memory.update_memory(memory_id, content="Updated content"))
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 0

    def test_cache_invalidation_on_delete(self):
        """Test that cache is invalidated when deleting memory."""
        memory_id = run_async(self.memory.add_memory("Test memory"))
        
        run_async(self.memory.search_memory("Test"))
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 1
        
        run_async(self.memory.delete_memory(memory_id))
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 0

    def test_cache_invalidation_on_clear(self):
        """Test that cache is invalidated when clearing memory."""
        run_async(self.memory.add_memory("Test memory"))
        
        run_async(self.memory.search_memory("Test"))
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 1
        
        run_async(self.memory.clear_memory())
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 0

    def test_cache_different_queries(self):
        """Test that different queries have separate cache entries."""
        run_async(self.memory.add_memory("Python programming"))
        run_async(self.memory.add_memory("JavaScript development"))
        
        run_async(self.memory.search_memory("Python"))
        run_async(self.memory.search_memory("JavaScript"))
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 2

    def test_add_memories_batch_empty(self):
        """Test batch adding empty list."""
        ids = run_async(self.memory.add_memories_batch([]))
        assert ids == []
        assert run_async(self.memory.get_memory_count()) == 0

    def test_add_memories_batch_single_item(self):
        """Test batch adding single item."""
        items = [
            {"content": "Single item", "metadata": {"test": "value"}}
        ]
        ids = run_async(self.memory.add_memories_batch(items))
        
        assert len(ids) == 1
        assert ids[0] > 0
        assert run_async(self.memory.get_memory_count()) == 1
        
        retrieved = run_async(self.memory.get_memory_by_id(ids[0]))
        assert retrieved["content"] == "Single item"
        assert retrieved["metadata"] == {"test": "value"}

    def test_add_memories_batch_multiple_items(self):
        """Test batch adding multiple items."""
        items = [
            {"content": "Item 1", "metadata": {"index": 1}},
            {"content": "Item 2", "metadata": {"index": 2}},
            {"content": "Item 3", "metadata": {"index": 3}},
        ]
        ids = run_async(self.memory.add_memories_batch(items))
        
        assert len(ids) == 3
        assert run_async(self.memory.get_memory_count()) == 3
        
        for i, memory_id in enumerate(ids):
            assert memory_id > 0
            retrieved = run_async(self.memory.get_memory_by_id(memory_id))
            assert retrieved["content"] == f"Item {i + 1}"
            assert retrieved["metadata"]["index"] == i + 1

    def test_add_memories_batch_without_metadata(self):
        """Test batch adding items without metadata."""
        items = [
            {"content": "Item without metadata"},
            {"content": "Another item"},
        ]
        ids = run_async(self.memory.add_memories_batch(items))
        
        assert len(ids) == 2
        
        for memory_id in ids:
            retrieved = run_async(self.memory.get_memory_by_id(memory_id))
            assert retrieved["metadata"] == {}

    def test_add_memories_batch_with_existing_data(self):
        """Test batch adding items when database already has data."""
        existing_id = run_async(self.memory.add_memory("Existing item"))
        
        items = [
            {"content": "Batch item 1"},
            {"content": "Batch item 2"},
        ]
        batch_ids = run_async(self.memory.add_memories_batch(items))
        
        assert run_async(self.memory.get_memory_count()) == 3
        assert all(id_ > existing_id for id_ in batch_ids)

    def test_add_memories_batch_cache_invalidation(self):
        """Test that cache is invalidated when batch adding items."""
        run_async(self.memory.add_memory("Initial item"))
        run_async(self.memory.search_memory("Initial"))
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 1
        
        items = [{"content": "Batch item 1"}, {"content": "Batch item 2"}]
        run_async(self.memory.add_memories_batch(items))
        
        stats = self.memory.get_cache_stats()
        assert stats['size'] == 0

    def test_add_memories_batch_performance(self):
        """Test batch insert is more efficient than individual inserts."""
        import time
        
        items = [{"content": f"Item {i}"} for i in range(100)]
        
        start_batch = time.time()
        batch_ids = run_async(self.memory.add_memories_batch(items))
        batch_time = time.time() - start_batch
        
        assert len(batch_ids) == 100
        assert run_async(self.memory.get_memory_count()) == 100
        
        run_async(self.memory.clear_memory())
        
        start_individual = time.time()
        for item in items:
            run_async(self.memory.add_memory(item["content"]))
        individual_time = time.time() - start_individual
        
        assert batch_time < individual_time