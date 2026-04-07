#!/usr/bin/env python3
"""
完整的端到端测试套件
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from sherry_agent.execution.agent_loop import agent_loop
from sherry_agent.infrastructure.tool_executor import ToolExecutor
from sherry_agent.llm import OllamaClient
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import EventType


@pytest.fixture
def llm_client():
    """提供 Ollama 客户端"""
    return OllamaClient()


@pytest.fixture
def tool_executor():
    """提供工具执行器"""
    return ToolExecutor()


@pytest.fixture
def agent_config():
    """提供 Agent 配置"""
    return AgentConfig(model="qwen3:0.6b")


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.asyncio
async def test_simple_conversation(llm_client, tool_executor, agent_config):
    """测试简单对话"""
    test_messages = [
        {"role": "user", "content": "你好，请简单介绍一下自己"}
    ]
    
    received_text = False
    
    async for event in agent_loop(
        messages=test_messages,
        config=agent_config,
        llm_client=llm_client,
        tool_executor=tool_executor
    ):
        if event.event_type == EventType.TEXT:
            received_text = True
            assert event.content is not None
    
    assert received_text, "应该收到文本回复"


@pytest.mark.e2e
@pytest.mark.tools
@pytest.mark.asyncio
async def test_read_file_tool(tool_executor):
    """测试读取文件工具"""
    result_content, result_metadata = await tool_executor.execute_tool(
        tool_name="read_file",
        tool_input={"path": "AGENTS.md"},
        call_id="test-read"
    )
    
    assert result_metadata.get("success") is True, "文件读取应该成功"
    assert len(result_content) > 0, "文件内容不应该为空"


@pytest.mark.e2e
@pytest.mark.tools
@pytest.mark.asyncio
async def test_exec_command_tool(tool_executor):
    """测试执行命令工具"""
    result_content, result_metadata = await tool_executor.execute_tool(
        tool_name="exec_command",
        tool_input={"command": "echo 'Hello from SherryAgent!'"},
        call_id="test-command"
    )
    
    assert result_metadata.get("success") is True, "命令执行应该成功"
    assert "Hello from SherryAgent!" in result_content, "应该包含预期的输出"


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.asyncio
async def test_math_conversation(llm_client, tool_executor, agent_config):
    """测试数学对话"""
    test_messages = [
        {"role": "user", "content": "请告诉我 1+1 等于几"}
    ]
    
    received_text = False
    
    async for event in agent_loop(
        messages=test_messages,
        config=agent_config,
        llm_client=llm_client,
        tool_executor=tool_executor
    ):
        if event.event_type == EventType.TEXT:
            received_text = True
            assert event.content is not None
    
    assert received_text, "应该收到文本回复"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
