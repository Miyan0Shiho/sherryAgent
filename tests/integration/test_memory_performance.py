import pytest
import asyncio
import time
from sherry_agent.memory.short_term import ShortTermMemory
from sherry_agent.memory.long_term import LongTermMemory
from sherry_agent.memory.bridge import MemoryBridge


@pytest.mark.asyncio
async def test_short_term_memory_performance():
    """测试短期记忆的性能"""
    # 创建短期记忆
    short_term_memory = ShortTermMemory(max_tokens=10000)
    
    # 测试添加项目的性能
    start_time = time.time()
    for i in range(1000):
        short_term_memory.add_item({
            "role": "user",
            "content": f"This is test message {i} with some content to test performance",
            "timestamp": "current"
        })
    end_time = time.time()
    
    # 验证添加时间
    add_time = end_time - start_time
    print(f"添加 1000 个项目到短期记忆耗时: {add_time:.4f} 秒")
    assert add_time < 1.0  # 应该在 1 秒内完成
    
    # 测试获取记忆的性能
    start_time = time.time()
    memory_items = short_term_memory.get_memory()
    end_time = time.time()
    
    # 验证获取时间
    get_time = end_time - start_time
    print(f"获取短期记忆耗时: {get_time:.4f} 秒")
    assert get_time < 0.1  # 应该在 0.1 秒内完成
    
    # 验证记忆项数量
    assert len(memory_items) > 0


@pytest.mark.asyncio
async def test_long_term_memory_performance():
    """测试长期记忆的性能"""
    # 创建长期记忆
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 测试添加记忆的性能
        start_time = time.time()
        for i in range(100):
            await long_term_memory.add_memory(
                f"This is test memory {i} with some content to test performance",
                {"category": "test", "index": i}
            )
        end_time = time.time()
        
        # 验证添加时间
        add_time = end_time - start_time
        print(f"添加 100 个项目到长期记忆耗时: {add_time:.4f} 秒")
        assert add_time < 2.0  # 应该在 2 秒内完成
        
        # 测试搜索记忆的性能
        start_time = time.time()
        results = await long_term_memory.search_memory("test", limit=10)
        end_time = time.time()
        
        # 验证搜索时间
        search_time = end_time - start_time
        print(f"搜索长期记忆耗时: {search_time:.4f} 秒")
        assert search_time < 0.5  # 应该在 0.5 秒内完成
        
        # 验证搜索结果
        assert len(results) > 0
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.mark.asyncio
async def test_memory_bridge_performance():
    """测试记忆桥接的性能"""
    # 创建记忆系统组件
    short_term_memory = ShortTermMemory(max_tokens=10000)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        memory_bridge = MemoryBridge(short_term_memory, long_term_memory)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 添加测试项目到短期记忆
        for i in range(100):
            short_term_memory.add_item({
                "role": "user",
                "content": f"This is important message {i} with key information to test memory bridge performance",
                "timestamp": "current"
            })
        
        # 测试记忆转移的性能
        start_time = time.time()
        result = await memory_bridge.process_memory_cycle(importance_threshold=0.5)
        end_time = time.time()
        
        # 验证转移时间
        transfer_time = end_time - start_time
        print(f"记忆转移耗时: {transfer_time:.4f} 秒")
        print(f"转移项目数量: {result['transferred_count']}")
        assert transfer_time < 2.0  # 应该在 2 秒内完成
        
        # 验证转移结果
        assert result["transferred_count"] > 0
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.mark.asyncio
async def test_memory_stress_test():
    """测试记忆系统的压力"""
    # 创建记忆系统组件
    short_term_memory = ShortTermMemory(max_tokens=5000)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        memory_bridge = MemoryBridge(short_term_memory, long_term_memory)
        
        # 初始化长期记忆
        await long_term_memory.initialize()
        
        # 模拟大量对话
        start_time = time.time()
        for i in range(500):
            # 添加用户消息到短期记忆
            short_term_memory.add_item({
                "role": "user",
                "content": f"User message {i}: How are you doing today?",
                "timestamp": "current"
            })
            
            # 添加助手响应到短期记忆
            short_term_memory.add_item({
                "role": "assistant",
                "content": f"Assistant response {i}: I'm doing well, thank you for asking!",
                "timestamp": "current"
            })
            
            # 每 100 轮执行一次记忆转移
            if i % 100 == 0 and i > 0:
                await memory_bridge.process_memory_cycle(importance_threshold=0.5)
        
        # 最后执行一次记忆转移
        await memory_bridge.process_memory_cycle(importance_threshold=0.5)
        end_time = time.time()
        
        # 验证总耗时
        total_time = end_time - start_time
        print(f"压力测试总耗时: {total_time:.4f} 秒")
        assert total_time < 10.0  # 应该在 10 秒内完成
        
        # 验证长期记忆中的项目数量
        long_term_count = await long_term_memory.get_memory_count()
        print(f"长期记忆项目数量: {long_term_count}")
        assert long_term_count > 0
        
        # 验证短期记忆中的项目数量
        short_term_count = len(short_term_memory.get_memory())
        print(f"短期记忆项目数量: {short_term_count}")
    finally:
        # 清理临时文件
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.mark.asyncio
async def test_memory_compaction_performance():
    """测试记忆压缩的性能"""
    # 创建短期记忆，设置较小的令牌限制
    short_term_memory = ShortTermMemory(max_tokens=100)
    
    # 添加大量项目，触发压缩
    start_time = time.time()
    for i in range(100):
        short_term_memory.add_item({
            "role": "user",
            "content": f"This is a long message {i} that will cause compaction to happen. " * 5,
            "timestamp": "current"
        })
    end_time = time.time()
    
    # 验证压缩时间
    compaction_time = end_time - start_time
    print(f"记忆压缩耗时: {compaction_time:.4f} 秒")
    assert compaction_time < 1.0  # 应该在 1 秒内完成
    
    # 验证压缩结果
    memory_items = short_term_memory.get_memory()
    print(f"压缩后记忆项目数量: {len(memory_items)}")
    assert len(memory_items) > 0
    
    # 验证压缩策略被应用
    compacted_items = [item for item in memory_items if item.get("compressed")]
    assert len(compacted_items) > 0
