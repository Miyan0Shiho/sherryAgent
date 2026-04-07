#!/usr/bin/env python3
"""
测试小模型优化
1. 验证系统提示词对小模型的优化
2. 验证工具描述的优化
3. 验证工具调用能力
"""

import asyncio
from src.sherry_agent.llm.client import OllamaClient
from src.sherry_agent.config.system_prompts import get_system_prompt

async def test_read_file():
    """测试读取文件工具"""
    print("=== 测试读取文件工具 ===")
    client = OllamaClient()
    
    system_prompt = get_system_prompt("qwen3:0.6b")
    
    response = await client.chat(
        messages=[{"role": "user", "content": "请读取 README.md 文件"}],
        model="qwen3:0.6b",
        max_tokens=1000,
        tools=[{
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "文件路径，比如 'README.md' 或 'src/file.py'"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }],
        system_prompt=system_prompt
    )
    
    print(f"响应内容: {response.content}")
    print(f"工具调用: {response.tool_calls}")
    print()

async def test_write_file():
    """测试写入文件工具"""
    print("=== 测试写入文件工具 ===")
    client = OllamaClient()
    
    system_prompt = get_system_prompt("qwen3:0.6b")
    
    response = await client.chat(
        messages=[{"role": "user", "content": "请创建一个测试文件 test_small_model.txt，内容为 'Hello from qwen3:0.6b'"}],
        model="qwen3:0.6b",
        max_tokens=1000,
        tools=[{
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "写入文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "文件路径，比如 'README.md' 或 'src/file.py'"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的文件内容"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        }],
        system_prompt=system_prompt
    )
    
    print(f"响应内容: {response.content}")
    print(f"工具调用: {response.tool_calls}")
    print()

async def test_exec_command():
    """测试执行命令工具"""
    print("=== 测试执行命令工具 ===")
    client = OllamaClient()
    
    system_prompt = get_system_prompt("qwen3:0.6b")
    
    response = await client.chat(
        messages=[{"role": "user", "content": "请列出当前目录的文件"}],
        model="qwen3:0.6b",
        max_tokens=1000,
        tools=[{
            "type": "function",
            "function": {
                "name": "exec_command",
                "description": "执行 shell 命令",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "要执行的 shell 命令"
                        }
                    },
                    "required": ["command"]
                }
            }
        }],
        system_prompt=system_prompt
    )
    
    print(f"响应内容: {response.content}")
    print(f"工具调用: {response.tool_calls}")
    print()

if __name__ == "__main__":
    asyncio.run(test_read_file())
    asyncio.run(test_write_file())
    asyncio.run(test_exec_command())
