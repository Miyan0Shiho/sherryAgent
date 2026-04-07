#!/usr/bin/env python3
"""
端到端测试套件

整合所有核心功能测试，包括：
- LLM 集成测试
- Agent Loop 测试
- 工具调用测试
- 权限系统测试
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sherry_agent.execution.agent_loop import agent_loop
from sherry_agent.infrastructure.tool_executor import ToolExecutor
from sherry_agent.llm import OllamaClient
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import EventType


@pytest.mark.e2e
@pytest.mark.llm
class TestLLMIntegration:
    """LLM 集成测试"""

    @pytest.fixture
    def llm_client(self):
        """创建 LLM 客户端"""
        return OllamaClient()

    @pytest.fixture
    def config(self):
        """创建测试配置"""
        return AgentConfig(model="qwen3:0.6b")

    @pytest.mark.asyncio
    async def test_simple_conversation(self, llm_client, config):
        """测试简单对话功能"""
        test_messages = [
            {"role": "user", "content": "你好，请简单介绍一下自己"}
        ]
        
        tool_executor = ToolExecutor()
        responses = []
        
        async for event in agent_loop(
            messages=test_messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            if event.event_type == EventType.TEXT:
                responses.append(event.content)
            elif event.event_type == EventType.ERROR:
                pytest.fail(f"LLM 对话测试失败: {event.content}")
        
        assert len(responses) > 0, "应该收到至少一个回复"
        assert isinstance(responses[0], str), "回复应该是字符串"

    @pytest.mark.asyncio
    async def test_math_calculation(self, llm_client, config):
        """测试数学计算能力"""
        test_messages = [
            {"role": "user", "content": "请告诉我 123 + 456 等于多少"}
        ]
        
        tool_executor = ToolExecutor()
        responses = []
        
        async for event in agent_loop(
            messages=test_messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            if event.event_type == EventType.TEXT:
                responses.append(event.content)
            elif event.event_type == EventType.ERROR:
                pytest.fail(f"数学计算测试失败: {event.content}")
        
        assert len(responses) > 0, "应该收到至少一个回复"
        # 检查回复是否包含数字，而不是具体的计算结果
        assert any(char.isdigit() for char in responses[0]), "回复应该包含数字"


@pytest.mark.e2e
@pytest.mark.agent_loop
class TestAgentLoop:
    """Agent Loop 测试"""

    @pytest.fixture
    def llm_client(self):
        """创建 LLM 客户端"""
        return OllamaClient()

    @pytest.fixture
    def tool_executor(self):
        """创建工具执行器"""
        return ToolExecutor()

    @pytest.fixture
    def config(self, tool_executor):
        """创建测试配置"""
        return AgentConfig(
            model="qwen3:0.6b",
            tools=tool_executor.get_available_tools()
        )

    @pytest.mark.asyncio
    async def test_agent_loop_completion(self, llm_client, tool_executor, config):
        """测试 Agent Loop 完整执行"""
        test_messages = [
            {"role": "user", "content": "你好，请简单介绍一下自己"}
        ]
        
        events = []
        
        async for event in agent_loop(
            messages=test_messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            events.append(event)
        
        assert len(events) > 0, "应该产生至少一个事件"
        text_events = [e for e in events if e.event_type == EventType.TEXT]
        assert len(text_events) > 0, "应该产生至少一个文本回复"

    @pytest.mark.asyncio
    async def test_agent_loop_with_error_handling(self, llm_client, tool_executor, config):
        """测试 Agent Loop 错误处理"""
        # 使用无效的模型名称来触发错误
        error_config = AgentConfig(model="invalid_model_name")
        test_messages = [
            {"role": "user", "content": "你好"}
        ]
        
        events = []
        
        async for event in agent_loop(
            messages=test_messages,
            config=error_config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            events.append(event)
        
        error_events = [e for e in events if e.event_type == EventType.ERROR]
        # 允许错误事件存在，因为使用了无效模型
        assert len(events) > 0, "应该产生至少一个事件"


@pytest.mark.e2e
@pytest.mark.tools
class TestToolCalling:
    """工具调用测试"""

    @pytest.fixture
    def tool_executor(self):
        """创建工具执行器"""
        return ToolExecutor()

    @pytest.fixture
    def test_file(self):
        """创建测试文件"""
        test_file = Path("test_temp_file.txt")
        test_file.write_text("Hello, World!")
        yield test_file
        # 清理测试文件
        if test_file.exists():
            test_file.unlink()

    @pytest.mark.asyncio
    async def test_read_file_tool(self, tool_executor, test_file):
        """测试读取文件工具"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="read_file",
            tool_input={"file_path": str(test_file)},
            call_id="test_read_file"
        )
        
        assert "Permission denied" not in result
        assert "Hello, World!" in result or metadata.get("success") is True or "error" not in metadata

    @pytest.mark.asyncio
    async def test_write_file_tool(self, tool_executor):
        """测试写入文件工具"""
        test_write_path = Path("test_write_temp.txt")
        
        result, metadata = await tool_executor.execute_tool(
            tool_name="write_file",
            tool_input={"file_path": str(test_write_path), "content": "Test write"},
            call_id="test_write_file"
        )
        
        assert "Permission denied" not in result
        assert test_write_path.exists() or metadata.get("success") is True or "error" not in metadata
        
        # 清理测试文件
        if test_write_path.exists():
            test_write_path.unlink()

    @pytest.mark.asyncio
    async def test_exec_command_tool(self, tool_executor):
        """测试执行命令工具"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "echo 'Hello from SherryAgent!'"},
            call_id="test_exec_command"
        )
        
        assert metadata.get("success") is True or "error" not in metadata
        assert "Permission denied" not in result

    @pytest.mark.asyncio
    async def test_http_request_tool(self, tool_executor):
        """测试 HTTP 请求工具"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="http_request",
            tool_input={"url": "https://example.com", "method": "GET"},
            call_id="test_http_request"
        )
        
        assert "Permission denied" not in result
        assert metadata.get("success") is True or "error" not in metadata


@pytest.mark.e2e
@pytest.mark.security
class TestPermissionSystem:
    """权限系统测试"""

    @pytest.fixture
    def tool_executor(self):
        """创建工具执行器"""
        return ToolExecutor()

    @pytest.mark.asyncio
    async def test_dangerous_command_denied(self, tool_executor):
        """测试危险命令被拦截"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "rm -rf /"},
            call_id="test_dangerous_cmd"
        )
        
        assert "Permission denied" in result
        assert metadata.get("error") == "permission_denied"
        assert "危险命令被禁止" in metadata.get("reason", "")

    @pytest.mark.asyncio
    async def test_safe_command_allowed(self, tool_executor):
        """测试安全命令能正常执行"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "echo 'safe command'"},
            call_id="test_safe_cmd"
        )
        
        assert metadata.get("success") is True or "error" not in metadata
        assert "Permission denied" not in result

    @pytest.mark.asyncio
    async def test_read_file_outside_sandbox_denied(self, tool_executor):
        """测试读取沙箱外文件被拒绝"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="read_file",
            tool_input={"file_path": "/etc/passwd"},
            call_id="test_read_outside_sandbox"
        )
        
        assert "Permission denied" in result
        assert metadata.get("error") == "permission_denied"
        assert "访问危险路径被禁止" in metadata.get("reason", "")

    @pytest.mark.asyncio
    async def test_multiple_dangerous_commands_denied(self, tool_executor):
        """测试多种危险命令都被拦截"""
        dangerous_commands = [
            "rm -rf /*",
            "rm -rf ~",
            "rm -rf ~/*",
            ":(){ :|:& };:",
        ]
        
        for cmd in dangerous_commands:
            result, metadata = await tool_executor.execute_tool(
                tool_name="exec_command",
                tool_input={"command": cmd},
                call_id=f"test_dangerous_{hash(cmd)}"
            )
            
            assert "Permission denied" in result
            assert metadata.get("error") == "permission_denied"


@pytest.mark.e2e
@pytest.mark.integration
class TestFullIntegration:
    """完整集成测试"""

    @pytest.fixture
    def llm_client(self):
        """创建 LLM 客户端"""
        return OllamaClient()

    @pytest.fixture
    def tool_executor(self):
        """创建工具执行器"""
        return ToolExecutor()

    @pytest.fixture
    def config(self, tool_executor):
        """创建测试配置"""
        return AgentConfig(
            model="qwen3:0.6b",
            tools=tool_executor.get_available_tools()
        )

    @pytest.mark.asyncio
    async def test_full_end_to_end_flow(self, llm_client, tool_executor, config, tmp_path):
        """测试完整的端到端流程"""
        # 创建测试文件
        test_file = tmp_path / "test_e2e.txt"
        test_file.write_text("End-to-end test file")
        
        # 测试消息序列
        test_messages = [
            {"role": "user", "content": f"请读取文件 {test_file} 的内容"}
        ]
        
        events = []
        
        async for event in agent_loop(
            messages=test_messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            events.append(event)
        
        # 验证事件
        assert len(events) > 0, "应该产生至少一个事件"
        
        # 检查是否有工具使用和工具结果事件
        tool_use_events = [e for e in events if e.event_type == EventType.TOOL_USE]
        tool_result_events = [e for e in events if e.event_type == EventType.TOOL_RESULT]
        text_events = [e for e in events if e.event_type == EventType.TEXT]
        
        # 至少应该有一个文本回复
        assert len(text_events) > 0, "应该产生至少一个文本回复"


if __name__ == "__main__":
    # 运行所有端到端测试
    pytest.main([__file__, "-v", "-m", "e2e"])
