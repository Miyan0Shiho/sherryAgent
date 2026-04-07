import pytest
import asyncio
from unittest.mock import Mock, patch
from sherry_agent.execution.agent_loop import agent_loop
from sherry_agent.llm.client import LLMClient, MockLLMClient
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import EventType, ToolCall, TokenUsage
from sherry_agent.memory.short_term import ShortTermMemory
from sherry_agent.memory.long_term import LongTermMemory
from sherry_agent.memory.bridge import MemoryBridge





class MockToolExecutor:
    async def execute_tool(self, tool_name, tool_input, call_id):
        return f"Tool {tool_name} executed", {"status": "success"}


@pytest.mark.asyncio
async def test_agent_loop_with_memory():
    """测试 Agent Loop 与记忆系统的集成"""
    # 创建测试配置
    config = AgentConfig(
        model="test-model",
        max_tokens=1000,
        max_tool_rounds=3,
        token_budget=1000,
        system_prompt="You are a test agent"
    )
    
    # 创建 LLM 客户端和工具执行器
    llm_client = MockLLMClient(responses=["This is a test response"])
    
    tool_executor = MockToolExecutor()
    
    # 创建记忆系统组件
    short_term_memory = ShortTermMemory(max_tokens=1000)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        memory_bridge = MemoryBridge(short_term_memory, long_term_memory)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 添加一些测试记忆到长期记忆
        await long_term_memory.add_memory("Test memory 1", {"type": "test"})
        await long_term_memory.add_memory("Test memory 2", {"type": "test"})
        
        # 创建测试消息
        messages = [
            {"role": "user", "content": "Hello, how are you?"}
        ]
        
        # 运行 Agent Loop
        events = []
        async for event in agent_loop(
            messages=messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor,
            short_term_memory=short_term_memory,
            long_term_memory=long_term_memory,
            memory_bridge=memory_bridge
        ):
            events.append(event)
        
        # 验证事件
        assert len(events) > 0
        
        # 验证是否有文本响应事件
        text_events = [e for e in events if e.event_type == EventType.TEXT]
        assert len(text_events) > 0
        
        # 验证是否有记忆转移事件
        memory_events = [e for e in events if e.event_type == EventType.MEMORY_TRANSFER]
        assert len(memory_events) > 0
        
        # 验证短期记忆是否被填充
        short_term_items = short_term_memory.get_memory()
        assert len(short_term_items) > 0
        
        # 验证长期记忆是否有内容
        long_term_count = await long_term_memory.get_memory_count()
        assert long_term_count >= 2  # 至少有我们添加的两个测试记忆
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.mark.asyncio
async def test_memory_bridge_transfer():
    """测试记忆桥接功能"""
    # 创建记忆系统组件
    short_term_memory = ShortTermMemory(max_tokens=1000)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        memory_bridge = MemoryBridge(short_term_memory, long_term_memory)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 添加一些测试项目到短期记忆
        short_term_memory.add_item({
            "role": "user",
            "content": "This is an important message with key information",
            "timestamp": "current"
        })
        short_term_memory.add_item({
            "role": "assistant",
            "content": "This is a response to the important message",
            "timestamp": "current"
        })
        
        # 执行记忆转移
        result = await memory_bridge.process_memory_cycle(importance_threshold=0.5)
        
        # 验证转移结果
        assert result["transferred_count"] > 0
        
        # 验证长期记忆是否有内容
        long_term_count = await long_term_memory.get_memory_count()
        assert long_term_count > 0
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.mark.asyncio
async def test_short_term_memory_compaction():
    """测试短期记忆压缩功能"""
    # 创建短期记忆，设置较小的令牌限制
    short_term_memory = ShortTermMemory(max_tokens=50)
    
    # 添加多个项目
    for i in range(10):
        short_term_memory.add_item({
            "role": "user",
            "content": f"This is a test message {i} with some content to test compaction",
            "timestamp": "current"
        })
    
    # 验证记忆已被压缩
    memory_items = short_term_memory.get_memory()
    assert len(memory_items) <= 10
    
    # 验证压缩策略被应用
    compacted_items = [item for item in memory_items if item.get("compressed")]
    assert len(compacted_items) > 0


@pytest.mark.asyncio
async def test_long_term_memory_search():
    """测试长期记忆搜索功能"""
    # 创建长期记忆
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 添加测试记忆
        await long_term_memory.add_memory("Python is a programming language", {"category": "programming"})
        await long_term_memory.add_memory("JavaScript is a programming language", {"category": "programming"})
        await long_term_memory.add_memory("C++ is a programming language", {"category": "programming"})
        
        # 搜索记忆
        results = await long_term_memory.search_memory("Python", limit=5)
        
        # 验证搜索结果
        assert len(results) > 0
        assert any("Python" in result["content"] for result in results)
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.mark.asyncio
async def test_memory_integration_end_to_end():
    """测试记忆系统的端到端集成"""
    # 创建测试配置
    config = AgentConfig(
        model="test-model",
        max_tokens=1000,
        max_tool_rounds=1,
        token_budget=1000,
        system_prompt="You are a test agent"
    )
    
    # 创建 LLM 客户端和工具执行器
    llm_client = MockLLMClient(responses=["This is a test response"])
    
    tool_executor = MockToolExecutor()
    
    # 创建记忆系统组件
    short_term_memory = ShortTermMemory(max_tokens=1000)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        memory_bridge = MemoryBridge(short_term_memory, long_term_memory)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 测试多轮对话
        for i in range(3):
            messages = [
                {"role": "user", "content": f"Hello, this is test {i}"}
            ]
            
            events = []
            async for event in agent_loop(
                messages=messages,
                config=config,
                llm_client=llm_client,
                tool_executor=tool_executor,
                short_term_memory=short_term_memory,
                long_term_memory=long_term_memory,
                memory_bridge=memory_bridge
            ):
                events.append(event)
            
            # 验证每轮都有响应
            assert len(events) > 0
        
        # 验证长期记忆中存储了多轮对话的信息
        long_term_count = await long_term_memory.get_memory_count()
        assert long_term_count > 0
        
        # 验证可以搜索到之前的对话
        results = await long_term_memory.search_memory("test", limit=5)
        assert len(results) > 0
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)
