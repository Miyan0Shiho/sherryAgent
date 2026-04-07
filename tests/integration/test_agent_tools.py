#!/usr/bin/env python3
"""
测试 Agent 工具使用功能
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sherry_agent.execution.agent_loop import agent_loop
from sherry_agent.infrastructure.tool_executor import ToolExecutor
from sherry_agent.llm import OllamaClient
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import EventType


async def test_agent_tools():
    """测试 Agent 工具使用功能"""
    print("=== 测试 Agent 工具使用功能 ===")
    
    # 创建必要的组件
    llm_client = OllamaClient()
    tool_executor = ToolExecutor()
    
    # 配置工具
    config = AgentConfig(
        model="qwen3:0.6b",
        tools=tool_executor.get_available_tools()
    )
    
    print("✅ 创建组件成功")
    print(f"✅ 可用工具: {[tool['name'] for tool in config.tools]}")
    
    # 测试任务：读取文件
    test_messages = [
        {"role": "user", "content": "请读取 AGENTS.md 文件的内容"}
    ]
    
    print("🔄 运行 Agent 循环...")
    
    try:
        async for event in agent_loop(
            messages=test_messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor
        ):
            if event.event_type == EventType.TEXT:
                print("📝 模型回复:")
                print(event.content)
            elif event.event_type == EventType.TOOL_USE:
                print(f"🔧 调用工具: {event.content}")
                if hasattr(event, 'metadata') and event.metadata:
                    print(f"   工具输入: {event.metadata.get('tool_input', {})}")
            elif event.event_type == EventType.TOOL_RESULT:
                print(f"✅ 工具结果:")
                print(event.content)
            elif event.event_type == EventType.ERROR:
                print(f"❌ 错误: {event.content}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent_tools())
