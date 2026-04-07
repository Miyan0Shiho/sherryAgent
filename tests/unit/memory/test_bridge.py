"""Unit tests for MemoryBridge class."""

import pytest
import asyncio
from src.sherry_agent.memory.bridge import MemoryBridge
from src.sherry_agent.memory.short_term import ShortTermMemory
from src.sherry_agent.memory.long_term import LongTermMemory


class TestMemoryBridge:
    """Test cases for MemoryBridge class."""

    def test_initialization(self):
        """Test that MemoryBridge initializes correctly."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        assert memory_bridge.short_term_memory is not None
        assert memory_bridge.long_term_memory is not None

    def test_extract_key_information(self):
        """Test key information extraction."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        content = "Important meeting on 2026-04-01 at 10:30 AM with John Doe. We need to discuss the critical project deadline of 2 weeks."
        key_info = memory_bridge.extract_key_information(content)
        
        # Check that key information is extracted
        assert len(key_info) > 0
        assert "2026-04-01" in key_info
        assert "10:30" in key_info
        assert "John Doe" in key_info
        assert "2" in key_info

    def test_calculate_importance_score(self):
        """Test importance score calculation."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        # Test low importance item
        low_importance_item = {"content": "Hello world"}
        low_score = memory_bridge.calculate_importance_score(low_importance_item)
        assert 0.0 <= low_score < 0.5
        
        # Test high importance item
        high_importance_item = {"content": "Important meeting on 2026-04-01 at 10:30 AM with John Doe. We need to discuss the critical project deadline of 2 weeks. This is essential information."}
        high_score = memory_bridge.calculate_importance_score(high_importance_item)
        assert high_score >= 0.5
        assert high_score <= 1.0
        
        # Test item with timestamp
        timestamp_item = {"content": "Important meeting", "timestamp": "2026-04-01T10:30:00"}
        timestamp_score = memory_bridge.calculate_importance_score(timestamp_item)
        assert timestamp_score > 0.0

    def test_calculate_importance_score_no_content(self):
        """Test importance score calculation for item without content."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        item = {}
        score = memory_bridge.calculate_importance_score(item)
        assert score == 0.0

    async def test_transfer_to_long_term(self):
        """Test transferring items from short-term to long-term memory."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        # Initialize long-term memory
        await long_term.initialize()
        await long_term.clear_memory()
        
        # Add items to short-term memory
        memory_bridge.short_term_memory.add_item({"content": "Low importance item"})
        memory_bridge.short_term_memory.add_item({"content": "Important meeting on 2026-04-01 at 10:30 AM with John Doe. We need to discuss the critical project deadline."})
        
        # Transfer to long-term memory
        transferred_count = await memory_bridge.transfer_to_long_term()
        
        # Check that at least one item was transferred
        assert transferred_count >= 1
        
        # Check that items are in long-term memory
        long_term_count = await memory_bridge.long_term_memory.get_memory_count()
        assert long_term_count >= transferred_count

    async def test_process_memory_cycle(self):
        """Test complete memory cycle processing."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        # Initialize long-term memory
        await long_term.initialize()
        await long_term.clear_memory()
        
        # Add items to short-term memory
        memory_bridge.short_term_memory.add_item({"content": "Low importance item"})
        memory_bridge.short_term_memory.add_item({"content": "Important meeting on 2026-04-01 at 10:30 AM with John Doe. We need to discuss the critical project deadline."})
        
        # Process memory cycle
        result = await memory_bridge.process_memory_cycle(clear_short_term=True)
        
        # Check results
        assert "transferred_count" in result
        assert "short_term_count" in result
        assert "long_term_count" in result
        assert "importance_threshold" in result
        
        # Check that short-term memory was cleared
        assert result["short_term_count"] == 0
        
        # Check that items were transferred
        assert result["transferred_count"] >= 1
        assert result["long_term_count"] >= result["transferred_count"]

    async def test_process_memory_cycle_no_clear(self):
        """Test memory cycle processing without clearing short-term memory."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        # Initialize long-term memory
        await long_term.initialize()
        await long_term.clear_memory()
        
        # Add items to short-term memory
        memory_bridge.short_term_memory.add_item({"content": "Important meeting"})
        
        # Process memory cycle without clearing
        result = await memory_bridge.process_memory_cycle(clear_short_term=False)
        
        # Check that short-term memory was not cleared
        assert result["short_term_count"] > 0

    async def test_transfer_with_custom_threshold(self):
        """Test transferring items with custom importance threshold."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        # Initialize long-term memory
        await long_term.initialize()
        await long_term.clear_memory()
        
        # Add an item with medium importance
        memory_bridge.short_term_memory.add_item({"content": "Medium importance item"})
        
        # Transfer with low threshold (should transfer)
        transferred_low = await memory_bridge.transfer_to_long_term(importance_threshold=0.1)
        assert transferred_low >= 1
        
        # Clear long-term memory
        await memory_bridge.long_term_memory.clear_memory()
        
        # Transfer with high threshold (should not transfer)
        transferred_high = await memory_bridge.transfer_to_long_term(importance_threshold=0.9)
        assert transferred_high == 0

    async def test_transfer_to_long_term_batch_operation(self):
        """Test that transfer uses batch operation for efficiency."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        await long_term.initialize()
        await long_term.clear_memory()
        
        for i in range(10):
            memory_bridge.short_term_memory.add_item({
                "content": f"Important item {i} with critical information"
            })
        
        transferred_count = await memory_bridge.transfer_to_long_term(importance_threshold=0.3)
        
        assert transferred_count > 0
        long_term_count = await long_term.get_memory_count()
        assert long_term_count == transferred_count

    async def test_transfer_empty_short_term(self):
        """Test transferring when short-term memory is empty."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        await long_term.initialize()
        await long_term.clear_memory()
        
        transferred_count = await memory_bridge.transfer_to_long_term()
        
        assert transferred_count == 0
        assert await long_term.get_memory_count() == 0

    async def test_transfer_preserves_metadata(self):
        """Test that metadata is preserved during batch transfer."""
        short_term = ShortTermMemory()
        long_term = LongTermMemory("./test_memory_bridge.db")
        memory_bridge = MemoryBridge(short_term, long_term)
        
        await long_term.initialize()
        await long_term.clear_memory()
        
        memory_bridge.short_term_memory.add_item({
            "content": "Important meeting",
            "metadata": {"custom_field": "custom_value"}
        })
        
        await memory_bridge.transfer_to_long_term(importance_threshold=0.1)
        
        memories = await long_term.get_recent_memories(limit=1)
        assert len(memories) == 1
        assert "custom_field" in memories[0]["metadata"]
        assert memories[0]["metadata"]["custom_field"] == "custom_value"
        assert "importance_score" in memories[0]["metadata"]
        assert "source" in memories[0]["metadata"]
