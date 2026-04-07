"""Unit tests for ShortTermMemory class."""

import pytest
from src.sherry_agent.memory.short_term import ShortTermMemory


class TestShortTermMemory:
    """Test cases for ShortTermMemory class."""

    def test_initialization(self):
        """Test that ShortTermMemory initializes correctly."""
        memory = ShortTermMemory(max_tokens=1000)
        assert memory.max_tokens == 1000
        assert memory.get_memory() == []
        assert memory.get_total_tokens() == 0

    def test_initialization_with_custom_encoding(self):
        """Test initialization with custom encoding name."""
        memory = ShortTermMemory(max_tokens=1000, encoding_name="p50k_base")
        assert memory.max_tokens == 1000
        assert memory._token_estimator.encoding_name == "p50k_base"

    def test_estimate_tokens(self):
        """Test token estimation functionality."""
        memory = ShortTermMemory()
        assert memory.estimate_tokens("Hello world") > 0
        assert memory.estimate_tokens("Hello, world!") > 0
        assert memory.estimate_tokens("") == 0
        long_text = "This is a longer sentence with multiple words."
        assert memory.estimate_tokens(long_text) > 5

    def test_estimate_tokens_chinese(self):
        """Test token estimation for Chinese text."""
        memory = ShortTermMemory()
        text = "这是一个中文测试句子"
        tokens = memory.estimate_tokens(text)
        assert tokens > 0

    def test_estimate_tokens_mixed_language(self):
        """Test token estimation for mixed language text."""
        memory = ShortTermMemory()
        text = "Hello world 你好世界 Mixed text 混合文本"
        tokens = memory.estimate_tokens(text)
        assert tokens > 5

    def test_add_item(self):
        """Test adding items to memory."""
        memory = ShortTermMemory()
        item1 = {"content": "Hello world"}
        item2 = {"content": "How are you?"}
        
        memory.add_item(item1)
        assert len(memory.get_memory()) == 1
        assert memory.get_total_tokens() > 0
        
        memory.add_item(item2)
        assert len(memory.get_memory()) == 2

    def test_get_total_tokens(self):
        """Test getting total tokens in memory."""
        memory = ShortTermMemory()
        assert memory.get_total_tokens() == 0
        
        memory.add_item({"content": "Hello world"})
        total1 = memory.get_total_tokens()
        assert total1 > 0
        
        memory.add_item({"content": "How are you?"})
        total2 = memory.get_total_tokens()
        assert total2 > total1

    def test_micro_compact(self):
        """Test micro-compact strategy."""
        memory = ShortTermMemory()
        item = {
            "content": "This is a test sentence. In conclusion, I think this is basically a really long sentence that needs to be compressed. Actually, you know, it's very much too long."
        }
        
        original_content = item["content"]
        memory._micro_compact(item)
        
        assert "content" in item
        assert item["content"] != original_content
        assert item.get("compressed") is True
        # Should be shorter than original
        assert len(item["content"]) < len(original_content)

    def test_compact(self):
        """Test memory compaction."""
        # Create memory with small token limit
        memory = ShortTermMemory(max_tokens=10)
        
        # Add items that exceed the limit
        memory.add_item({"content": "This is a long sentence that will exceed the token limit"})
        memory.add_item({"content": "Another long sentence to test compaction"})
        
        # Should have compacted or removed items
        memory_items = memory.get_memory()
        assert len(memory_items) <= 2
        assert memory.get_total_tokens() <= 10

    def test_clear(self):
        """Test clearing memory."""
        memory = ShortTermMemory()
        memory.add_item({"content": "Hello world"})
        assert len(memory.get_memory()) == 1
        
        memory.clear()
        assert len(memory.get_memory()) == 0
        assert memory.get_total_tokens() == 0

    def test_compact_single_item(self):
        """Test compacting when only one item is present."""
        # Create memory with small token limit
        memory = ShortTermMemory(max_tokens=20)
        
        # Add a single item that exceeds the limit but can be compressed
        memory.add_item({"content": "This is a test sentence. In conclusion, I think this is basically a really long sentence that needs to be compressed."})
        
        # Should have compacted the item
        memory_items = memory.get_memory()
        assert len(memory_items) == 1
        assert memory_items[0].get("compressed") is True

    def test_auto_compact(self):
        """Test auto-compact strategy."""
        memory = ShortTermMemory()
        
        # Add multiple items
        memory.add_item({"content": "First item content"})
        memory.add_item({"content": "Second item content"})
        memory.add_item({"content": "Third item content"})
        
        # Apply auto-compact
        memory._auto_compact()
        
        # Should have one summary item
        memory_items = memory.get_memory()
        assert len(memory_items) == 1
        assert memory_items[0].get("compressed") is True
        assert memory_items[0].get("strategy") == "auto-compact"
        assert "Summary of recent interactions" in memory_items[0].get("content", "")

    def test_session_compact(self):
        """Test session-compact strategy."""
        memory = ShortTermMemory()
        
        # Add items with key points
        memory.add_item({"content": "This is important information about the project."})
        memory.add_item({"content": "The main goal is to improve performance."})
        memory.add_item({"content": "Regular text without key points."})
        
        # Apply session-compact
        memory._session_compact()
        
        # Should have structured items
        memory_items = memory.get_memory()
        assert len(memory_items) > 0
        for item in memory_items:
            assert item.get("compressed") is True
            assert item.get("strategy") == "session-compact"

    def test_reactive_compact(self):
        """Test reactive-compact strategy."""
        memory = ShortTermMemory()
        
        # Add multiple items
        memory.add_item({"content": "First item with long content that should be aggressively compressed"})
        memory.add_item({"content": "Second item that should be kept"})
        
        # Apply reactive-compact
        memory._reactive_compact()
        
        # Should have only one aggressively compressed item
        memory_items = memory.get_memory()
        assert len(memory_items) == 1
        assert memory_items[0].get("compressed") is True
        assert memory_items[0].get("strategy") == "reactive-compact"
        assert len(memory_items[0].get("content", "")) <= 103  # 100 chars + "..."

    def test_compact_with_different_levels(self):
        """Test compact method with different compression levels."""
        # Test auto level
        memory_auto = ShortTermMemory(max_tokens=10)
        memory_auto.add_item({"content": "This is a long sentence that will exceed the token limit"})
        memory_auto.compact(level="auto")
        assert len(memory_auto.get_memory()) <= 1
        
        # Test session level
        memory_session = ShortTermMemory(max_tokens=10)
        memory_session.add_item({"content": "This is important information"})
        memory_session.compact(level="session")
        assert len(memory_session.get_memory()) <= 1
        
        # Test reactive level
        memory_reactive = ShortTermMemory(max_tokens=10)
        memory_reactive.add_item({"content": "This is a long sentence that will exceed the token limit"})
        memory_reactive.compact(level="reactive")
        assert len(memory_reactive.get_memory()) <= 1
        
        # Test micro level
        memory_micro = ShortTermMemory(max_tokens=10)
        memory_micro.add_item({"content": "This is a long sentence that will exceed the token limit"})
        memory_micro.compact(level="micro")
        assert len(memory_micro.get_memory()) <= 1
