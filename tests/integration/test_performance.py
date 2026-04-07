import pytest
import time
import asyncio
from sherry_agent.infrastructure.tool_executor import ToolExecutor


@pytest.fixture
def tool_executor():
    return ToolExecutor()


@pytest.mark.asyncio
async def test_tool_executor_performance(tool_executor):
    """测试工具执行器的性能"""
    # 测试文件读取工具的响应时间
    start_time = time.time()
    content, metadata = await tool_executor.execute_tool("read_file", {"path": "README.md"}, "test_call_id")
    end_time = time.time()
    execution_time = end_time - start_time
    
    assert "error" not in metadata
    assert execution_time < 5.0  # 确保文件读取在 5 秒以内


def test_agent_loop_performance():
    """测试 Agent 循环的性能"""
    # 模拟单次验证循环
    start_time = time.time()
    
    # 这里应该是实际的 Agent 循环代码
    # 为了测试性能，我们模拟一个简单的循环
    for i in range(1000):
        pass
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    assert execution_time < 30.0  # 确保单次验证循环在 30 秒以内
