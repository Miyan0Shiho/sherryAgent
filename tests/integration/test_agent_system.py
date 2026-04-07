#!/usr/bin/env python3
"""
测试完整的 Agent 系统功能
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


async def test_agent_system():
    """测试完整的 Agent 系统"""
    print("=== 测试完整 Agent 系统 ===")
    
    # 创建必要的组件
    llm_client = OllamaClient()
    tool_executor = ToolExecutor()
    config = AgentConfig(model="qwen3:0.6b")
    
    print("✅ 创建组件成功")
    
    # 测试任务：简单的对话
    test_messages = [
        {"role": "user", "content": "你好，请介绍一下自己"}
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
            elif event.event_type == EventType.TOOL_RESULT:
                print(f"✅ 工具结果: {event.content}")
            elif event.event_type == EventType.ERROR:
                print(f"❌ 错误: {event.content}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent_system())
