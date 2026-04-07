#!/usr/bin/env python3
"""
测试 Ollama API 的工具调用支持
"""

import asyncio
import aiohttp

async def test_ollama_tools():
    url = "http://localhost:11434/api/chat"
    
    # 测试请求体
    request_data = {
        "model": "qwen3:0.6b",
        "messages": [
            {
                "role": "user",
                "content": "请计算 123 + 456"
            }
        ],
        "tools": [
            {
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
            }
        ],
        "stream": False
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=request_data) as response:
                print(f"状态码: {response.status}")
                content = await response.text()
                print(f"响应: {content}")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama_tools())
