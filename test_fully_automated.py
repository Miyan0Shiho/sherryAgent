#!/usr/bin/env python3
"""
完全自动化的系统测试，无需用户输入
"""

import asyncio
import os
import sys

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sherry_agent.execution.agent_loop import agent_loop
from sherry_agent.infrastructure.tool_executor import ToolExecutor
from sherry_agent.llm import OllamaClient
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import EventType


async def test_full_system():
    """完整系统测试"""
    print("=" * 80)
    print("SherryAgent 完全自动化系统测试")
    print("=" * 80)
    
    # 创建所有组件
    print("\n[1/5] 创建组件...")
    llm_client = OllamaClient()
    tool_executor = ToolExecutor()
    config = AgentConfig(model="qwen3:0.6b")
    print("✅ 所有组件创建成功")
    
    # 测试 1: 简单对话
    print("\n[2/5] 测试简单对话...")
    test_messages_1 = [
        {"role": "user", "content": "你好，请简单介绍一下自己"}
    ]
    
    try:
        async for event in agent_loop(
            messages=test_messages_1,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            if event.event_type == EventType.TEXT:
                print("📝 模型回复:")
                print(event.content)
        print("✅ 简单对话测试通过")
    except Exception as e:
        print(f"❌ 简单对话测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 测试 2: 读取文件工具
    print("\n[3/5] 测试读取文件工具（直接调用）...")
    try:
        result_content, result_metadata = await tool_executor.execute_tool(
            tool_name="read_file",
            tool_input={"path": "AGENTS.md"},
            call_id="test-read"
        )
        if result_metadata.get("success"):
            print("✅ 文件读取成功")
            print(f"   文件大小: {result_metadata.get('size')} 字节")
            print(f"   内容预览: {result_content[:100]}...")
        else:
            print(f"❌ 文件读取失败: {result_content}")
    except Exception as e:
        print(f"❌ 文件读取测试失败: {str(e)}")
    
    # 测试 3: 执行命令工具
    print("\n[4/5] 测试执行命令工具（直接调用）...")
    try:
        result_content, result_metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "echo 'Hello from SherryAgent!'"},
            call_id="test-command"
        )
        if result_metadata.get("success"):
            print("✅ 命令执行成功")
            print(f"   返回码: {result_metadata.get('returncode')}")
            print(f"   输出: {result_content}")
        else:
            print(f"❌ 命令执行失败: {result_content}")
    except Exception as e:
        print(f"❌ 命令执行测试失败: {str(e)}")
    
    # 测试 4: 完整对话（不使用工具）
    print("\n[5/5] 测试完整对话流程...")
    test_messages_2 = [
        {"role": "user", "content": "请告诉我 1+1 等于几"}
    ]
    
    try:
        async for event in agent_loop(
            messages=test_messages_2,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            if event.event_type == EventType.TEXT:
                print("📝 模型回复:")
                print(event.content)
            elif event.event_type == EventType.ERROR:
                print(f"❌ 错误: {event.content}")
        print("✅ 完整对话测试通过")
    except Exception as e:
        print(f"❌ 完整对话测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_full_system())
