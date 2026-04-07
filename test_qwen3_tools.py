#!/usr/bin/env python3
"""
测试 qwen3:0.6b 的工具调用能力
"""

import asyncio
import aiohttp
import json

async def test_qwen3_tools():
    url = "http://localhost:11434/api/chat"
    
    # 测试 1: 基本工具调用格式
    print("=== 测试 1: 基本工具调用格式 ===")
    request_data_1 = {
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
            async with session.post(url, json=request_data_1) as response:
                print(f"状态码: {response.status}")
                content = await response.text()
                data = json.loads(content)
                print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                print()
        except Exception as e:
            print(f"错误: {e}")
            print()
    
    # 测试 2: 添加明确的工具使用提示
    print("=== 测试 2: 添加明确的工具使用提示 ===")
    request_data_2 = {
        "model": "qwen3:0.6b",
        "messages": [
            {
                "role": "system",
                "content": "你是一个助手，当需要执行数学计算时，请使用 calculator 工具。"
            },
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
            async with session.post(url, json=request_data_2) as response:
                print(f"状态码: {response.status}")
                content = await response.text()
                data = json.loads(content)
                print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                print()
        except Exception as e:
            print(f"错误: {e}")
            print()
    
    # 测试 3: 更详细的工具描述
    print("=== 测试 3: 更详细的工具描述 ===")
    request_data_3 = {
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
                    "description": "使用 calculator 工具来执行数学计算，比如加法、减法、乘法、除法等",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "要计算的数学表达式，例如 '123 + 456' 或 '100 * 200'"
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
            async with session.post(url, json=request_data_3) as response:
                print(f"状态码: {response.status}")
                content = await response.text()
                data = json.loads(content)
                print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                print()
        except Exception as e:
            print(f"错误: {e}")
            print()

if __name__ == "__main__":
    asyncio.run(test_qwen3_tools())
