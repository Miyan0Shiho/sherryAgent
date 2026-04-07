import asyncio
import os
from pathlib import Path

import pytest

from sherry_agent.infrastructure.tools.file import ReadFileTool, WriteFileTool, SandboxError
from sherry_agent.infrastructure.tools.shell import ShellTool
from sherry_agent.infrastructure.tools.http import HttpTool
from sherry_agent.infrastructure.tools.base import ToolResult


class TestReadFileTool:
    @pytest.mark.asyncio
    async def test_read_existing_file(self, tmp_path):
        # 创建测试文件
        test_file = tmp_path / "test.txt"
        test_content = "Hello, world!"
        test_file.write_text(test_content)

        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = ReadFileTool()
            result = await tool.execute(path="test.txt")
            assert result.success
            assert result.content == test_content
            assert result.metadata["path"] == str(test_file)
            assert result.metadata["size"] == len(test_content)
        finally:
            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_read_nonexistent_file(self, tmp_path):
        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = ReadFileTool()
            result = await tool.execute(path="nonexistent.txt")
            assert not result.success
            assert "File not found" in result.content
        finally:
            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_read_directory(self, tmp_path):
        # 创建测试目录
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = ReadFileTool()
            result = await tool.execute(path="test_dir")
            assert not result.success
            assert "Path is not a file" in result.content
        finally:
            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_read_outside_sandbox(self, tmp_path):
        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = ReadFileTool()
            result = await tool.execute(path="../nonexistent.txt")
            assert not result.success
            assert "Security error" in result.content
        finally:
            os.chdir(original_cwd)


class TestWriteFileTool:
    @pytest.mark.asyncio
    async def test_write_file(self, tmp_path):
        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = WriteFileTool()
            test_content = "Hello, world!"
            result = await tool.execute(path="test.txt", content=test_content)
            assert result.success
            assert "File written successfully" in result.content

            # 验证文件内容
            test_file = tmp_path / "test.txt"
            assert test_file.exists()
            assert test_file.read_text() == test_content
        finally:
            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_write_file_with_subdirectory(self, tmp_path):
        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = WriteFileTool()
            test_content = "Hello, world!"
            result = await tool.execute(path="subdir/test.txt", content=test_content)
            assert result.success
            assert "File written successfully" in result.content

            # 验证文件内容
            test_file = tmp_path / "subdir" / "test.txt"
            assert test_file.exists()
            assert test_file.read_text() == test_content
        finally:
            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_write_outside_sandbox(self, tmp_path):
        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            tool = WriteFileTool()
            test_content = "Hello, world!"
            result = await tool.execute(path="../test.txt", content=test_content)
            assert not result.success
            assert "Security error" in result.content
        finally:
            os.chdir(original_cwd)


class TestShellTool:
    @pytest.mark.asyncio
    async def test_exec_successful_command(self):
        tool = ShellTool()
        result = await tool.execute(command="echo 'Hello, world!'")
        assert result.success
        assert "Hello, world!" in result.content
        assert result.metadata["returncode"] == 0

    @pytest.mark.asyncio
    async def test_exec_failed_command(self):
        tool = ShellTool()
        result = await tool.execute(command="nonexistent_command")
        assert not result.success
        assert result.metadata["returncode"] != 0

    @pytest.mark.asyncio
    async def test_exec_command_with_timeout(self):
        tool = ShellTool()
        result = await tool.execute(command="sleep 2", timeout=1)
        assert not result.success
        assert "Command timed out" in result.content


class TestHttpTool:
    @pytest.mark.asyncio
    async def test_http_get_request(self):
        tool = HttpTool()
        result = await tool.execute(url="http://example.com")
        assert result.success
        assert "Example Domain" in result.content
        assert 200 <= result.metadata["status"] < 300

    @pytest.mark.asyncio
    async def test_http_post_request(self):
        tool = HttpTool()
        result = await tool.execute(
            url="http://httpbin.org/post",
            method="POST",
            data={"test": "value"}
        )
        assert result.success
        assert "test" in result.content
        assert 200 <= result.metadata["status"] < 300

    @pytest.mark.asyncio
    async def test_http_request_with_timeout(self):
        tool = HttpTool()
        result = await tool.execute(
            url="http://example.com",
            timeout=0.1
        )
        # 可能成功也可能超时，取决于网络速度
        # 这里不做严格断言，只确保没有抛出异常
        assert isinstance(result, ToolResult)

    @pytest.mark.asyncio
    async def test_http_request_with_invalid_url(self):
        tool = HttpTool()
        result = await tool.execute(url="invalid-url")
        assert not result.success
        assert "Error sending HTTP request" in result.content or "HTTP client error" in result.content