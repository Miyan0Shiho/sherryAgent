import pytest
from src.sherry_agent.infrastructure.tool_executor import ToolExecutor
from src.sherry_agent.infrastructure.tools.base import ToolResult, tool, Permission, clear_tools


@pytest.fixture(autouse=True)
def clear_registry():
    clear_tools()
    yield
    clear_tools()


@pytest.fixture
def test_tool():
    @tool(
        name="test_tool",
        description="A test tool",
        parameters={"input": {"type": "string", "description": "Test input"}},
        permissions=[Permission.READ],
    )
    async def test_tool_func(input: str) -> ToolResult:
        return ToolResult(success=True, content=f"Processed: {input}")

    return test_tool_func


@pytest.mark.asyncio
async def test_tool_executor_initialization():
    executor = ToolExecutor()
    assert executor is not None
    assert executor.permission_checker is not None


@pytest.mark.asyncio
async def test_tool_executor_execute_tool(test_tool):
    executor = ToolExecutor()

    content, metadata = await executor.execute_tool(
        tool_name="test_tool",
        tool_input={"input": "hello"},
        call_id="test-123",
    )

    assert content == "Processed: hello"
    assert metadata["success"] is True
    assert metadata["call_id"] == "test-123"


@pytest.mark.asyncio
async def test_tool_executor_tool_not_found():
    executor = ToolExecutor()

    content, metadata = await executor.execute_tool(
        tool_name="nonexistent_tool",
        tool_input={},
        call_id="test-456",
    )

    assert "Tool not found" in content
    assert metadata["error"] == "tool_not_found"


@pytest.mark.asyncio
async def test_get_available_tools(test_tool):
    executor = ToolExecutor()
    tools = executor.get_available_tools()

    # 至少包含测试工具和默认工具
    tool_names = [tool["name"] for tool in tools]
    assert "test_tool" in tool_names
    assert "read_file" in tool_names
    assert "write_file" in tool_names
    assert "exec_command" in tool_names
    assert "http_request" in tool_names
    for tool in tools:
        assert "description" in tool
        assert "input_schema" in tool
