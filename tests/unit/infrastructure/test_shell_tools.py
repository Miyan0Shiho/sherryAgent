import sys

import pytest
from src.sherry_agent.infrastructure.tools.shell_tools import exec_shell


@pytest.mark.asyncio
async def test_exec_shell_echo():
    result = await exec_shell("echo hello world")
    assert result.success is True
    assert "hello world" in result.content


@pytest.mark.asyncio
async def test_exec_shell_failure():
    result = await exec_shell("false")
    assert result.success is False
    assert result.metadata["returncode"] != 0


@pytest.mark.asyncio
async def test_exec_shell_with_args():
    test_string = "test with spaces"
    result = await exec_shell(f'echo "{test_string}"')
    assert result.success is True
    assert test_string in result.content


@pytest.mark.asyncio
async def test_exec_shell_metadata():
    result = await exec_shell("echo test")
    assert "returncode" in result.metadata
    assert "stdout" in result.metadata
    assert "stderr" in result.metadata
    assert "command" in result.metadata


@pytest.mark.asyncio
@pytest.mark.skipif(sys.platform == "win32", reason="Timeout test not reliable on Windows")
async def test_exec_shell_timeout():
    result = await exec_shell("sleep 10", timeout=0.1)
    assert result.success is False
    assert "Command timed out" in result.content
