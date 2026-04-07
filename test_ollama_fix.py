#!/usr/bin/env python3
"""
测试 Ollama 客户端修复
1. 验证 token 统计功能
2. 验证工具调用功能
"""

import asyncio
from src.sherry_agent.llm.client import OllamaClient

async def test_token_usage():
    """测试 token 使用统计"""
    print("=== 测试 Token 使用统计 ===")
    client = OllamaClient()
    
    response = await client.chat(
        messages=[{"role": "user", "content": "你好，请介绍一下自己"}],
        model="qwen3:0.6b",
        max_tokens=100
    )
    
    print(f"响应内容: {response.content}")
    print(f"Token 使用: {response.token_usage}")
    print(f"输入 Token: {response.token_usage.input_tokens}")
    print(f"输出 Token: {response.token_usage.output_tokens}")
    print()

async def test_tool_calls():
    """测试工具调用功能"""
    print("=== 测试工具调用功能 ===")
    client = OllamaClient()
    
    # 定义工具
    tools = [{
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    }]
    
    response = await client.chat(
        messages=[{"role": "user", "content": "请计算 123 + 456"}],
        model="qwen3:0.6b",
        max_tokens=100,
        tools=tools
    )
    
    print(f"响应内容: {response.content}")
    print(f"工具调用: {response.tool_calls}")
    print()

if __name__ == "__main__":
    asyncio.run(test_token_usage())
    asyncio.run(test_tool_calls())
