import asyncio
import os
from pathlib import Path

import pytest

from sherry_agent.infrastructure.tool_executor import ToolExecutor
from sherry_agent.infrastructure.tools.file import ReadFileTool


class TestToolExecutor:
    @pytest.mark.asyncio
    async def test_execute_existing_tool(self, tmp_path):
        # 创建测试文件
        test_file = tmp_path / "test.txt"
        test_content = "Hello, world!"
        test_file.write_text(test_content)

        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            executor = ToolExecutor()
            result_content, result_metadata = await executor.execute_tool(
                "read_file",
                {"path": "test.txt"},
                "test_call_id"
            )
            assert "Hello, world!" in result_content
            assert result_metadata["success"]
            assert result_metadata["call_id"] == "test_call_id"
        finally:
            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_execute_nonexistent_tool(self):
        executor = ToolExecutor()
        result_content, result_metadata = await executor.execute_tool(
            "nonexistent_tool",
            {},
            "test_call_id"
        )
        assert "Tool not found" in result_content
        assert result_metadata["error"] == "tool_not_found"
        assert result_metadata["tool_name"] == "nonexistent_tool"

    @pytest.mark.asyncio
    async def test_get_available_tools(self):
        executor = ToolExecutor()
        tools = executor.get_available_tools()
        assert len(tools) > 0
        tool_names = [tool["name"] for tool in tools]
        assert "read_file" in tool_names
        assert "write_file" in tool_names
        assert "exec_command" in tool_names
        assert "http_request" in tool_names

    @pytest.mark.asyncio
    async def test_register_tool(self):
        executor = ToolExecutor()
        custom_tool = ReadFileTool()
        executor.register_tool(custom_tool)
        tools = executor.get_available_tools()
        tool_names = [tool["name"] for tool in tools]
        assert "read_file" in tool_names