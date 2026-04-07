from __future__ import annotations

import asyncio
from unittest.mock import Mock, patch

import pytest

from src.sherry_agent.infrastructure.mcp.client import MCPclient
from src.sherry_agent.infrastructure.mcp.server import MCPserver


@pytest.mark.asyncio
async def test_mcp_client_execute_tool():
    """测试MCP客户端执行工具"""
    # 模拟响应
    mock_response = {
        "success": True,
        "content": "Test result",
        "metadata": {"test": "data"},
        "id": "test-id"
    }
    
    async def mock_json():
        return mock_response
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json = mock_json
        
        client = MCPclient("http://localhost:8000")
        result = await client.execute_tool("test_tool", {"param": "value"})
        
        assert result.success is True
        assert result.content == "Test result"
        assert result.metadata == {"test": "data"}
        await client.disconnect()


@pytest.mark.asyncio
async def test_mcp_client_list_tools():
    """测试MCP客户端列出工具"""
    mock_tools = [
        {"name": "tool1", "description": "Test tool 1"},
        {"name": "tool2", "description": "Test tool 2"}
    ]
    
    async def mock_json():
        return mock_tools
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = mock_json
        
        client = MCPclient("http://localhost:8000")
        tools = await client.list_tools()
        
        assert len(tools) == 2
        assert tools[0]["name"] == "tool1"
        await client.disconnect()


@pytest.mark.asyncio
async def test_mcp_client_get_tool_schema():
    """测试MCP客户端获取工具 schema"""
    mock_schema = {
        "name": "test_tool",
        "description": "Test tool",
        "parameters": {"param": {"type": "string"}}
    }
    
    async def mock_json():
        return mock_schema
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = mock_json
        
        client = MCPclient("http://localhost:8000")
        schema = await client.get_tool_schema("test_tool")
        
        assert schema["name"] == "test_tool"
        await client.disconnect()


@pytest.mark.asyncio
async def test_mcp_server_register_tool():
    """测试MCP服务器注册工具"""
    from src.sherry_agent.infrastructure.tools.base import BaseTool, Permission
    
    class TestTool(BaseTool):
        @property
        def name(self) -> str:
            return "test_tool"
        
        @property
        def description(self) -> str:
            return "Test tool"
        
        @property
        def parameters(self) -> dict:
            return {"param": {"type": "string"}}
        
        @property
        def permissions(self) -> list[Permission]:
            return []
        
        async def execute(self, **kwargs):
            from src.sherry_agent.infrastructure.tools.base import ToolResult
            return ToolResult(success=True, content="Test result")
    
    server = MCPserver()
    test_tool = TestTool()
    server.register_tool(test_tool)
    
    assert "test_tool" in server.registered_tools
    assert server.registered_tools["test_tool"].name == "test_tool"


@pytest.mark.asyncio
async def test_mcp_server_register_all_tools():
    """测试MCP服务器注册所有工具"""
    from src.sherry_agent.infrastructure.tools.base import tool, Permission
    
    # 注册一个测试工具
    @tool(
        name="test_registered_tool",
        description="Test registered tool",
        parameters={"param": {"type": "string"}},
        permissions=[Permission.READ]
    )
    async def test_registered_tool(param):
        from src.sherry_agent.infrastructure.tools.base import ToolResult
        return ToolResult(success=True, content=f"Test {param}")
    
    server = MCPserver()
    server.register_all_tools()
    
    assert "test_registered_tool" in server.registered_tools


@pytest.mark.asyncio
async def test_mcp_client_context_manager():
    """测试MCP客户端上下文管理器"""
    mock_response = {
        "success": True,
        "content": "Test result",
        "metadata": {},
        "id": "test-id"
    }
    
    async def mock_json():
        return mock_response
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json = mock_json
        
        async with MCPclient("http://localhost:8000") as client:
            result = await client.execute_tool("test_tool", {"param": "value"})
            assert result.success is True
        
        # 上下文退出后，session应该被关闭
        assert client.session is None