#!/usr/bin/env python3
"""
测试 SherryAgent 执行中等难度任务的能力
"""

import asyncio
import json
from src.sherry_agent.llm.client import OllamaClient
from src.sherry_agent.infrastructure.tools.file_tools import read_file, write_file
from src.sherry_agent.infrastructure.tools.shell_tools import exec_shell

class TestToolExecutor:
    """测试工具执行器"""
    async def execute_tool(self, tool_name, tool_input, call_id):
        """执行工具"""
        if tool_name == "read_file":
            result = await read_file(tool_input["path"])
            return result.content, result.metadata
        elif tool_name == "write_file":
            result = await write_file(
                tool_input["path"], 
                tool_input["content"]
            )
            return result.content, result.metadata
        elif tool_name == "list_directory":
            # 使用 shell 命令列出目录
            result = await exec_shell(f"ls -la {tool_input['directory']}")
            return result.content, result.metadata
        else:
            return f"工具 {tool_name} 不存在", {}

async def test_file_operations():
    """测试文件操作"""
    print("测试文件操作能力...\n")
    
    # 创建工具执行器
    tool_executor = TestToolExecutor()
    
    # 测试读取文件
    print("测试 1: 读取 README.md 文件")
    try:
        content, metadata = await tool_executor.execute_tool(
            "read_file",
            {"path": "README.md"},
            "test-1"
        )
        print("✅ 文件读取成功！")
        print(f"文件内容前 200 字符: {content[:200]}...")
        print("-" * 50)
    except Exception as e:
        print(f"❌ 文件读取失败: {str(e)}")
        print("-" * 50)
    
    # 测试写入文件
    print("测试 2: 创建并写入测试文件")
    test_content = "这是一个测试文件，用于测试 SherryAgent 的文件写入能力。"
    try:
        result, metadata = await tool_executor.execute_tool(
            "write_file",
            {"path": "test_output.txt", "content": test_content},
            "test-2"
        )
        print("✅ 文件写入成功！")
        print(f"结果: {result}")
        print("-" * 50)
    except Exception as e:
        print(f"❌ 文件写入失败: {str(e)}")
        print("-" * 50)
    
    # 测试列出目录
    print("测试 3: 列出 src 目录内容")
    try:
        content, metadata = await tool_executor.execute_tool(
            "list_directory",
            {"directory": "src"},
            "test-3"
        )
        print("✅ 目录列出成功！")
        print(f"目录内容: {content}")
        print("-" * 50)
    except Exception as e:
        print(f"❌ 目录列出失败: {str(e)}")
        print("-" * 50)

async def test_llm_with_tools():
    """测试 LLM 与工具的集成"""
    print("测试 LLM 与工具的集成...\n")
    
    # 创建 Ollama 客户端
    client = OllamaClient()
    
    # 定义工具
    tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "文件路径"
                        }
                    },
                    "required": ["path"]
                }
            }
        }
    ]
    
    # 测试任务
    messages = [
        {
            "role": "user", 
            "content": "请读取 README.md 文件并告诉我它的主要内容"
        }
    ]
    
    try:
        response = await client.chat(
            messages=messages,
            model="qwen3:0.6b",
            max_tokens=300,
            tools=tools,
            system_prompt="你是一个 helpful 的 AI 助手，能够使用工具完成任务"
        )
        
        print("✅ LLM 响应成功！")
        print("响应:")
        print(response.content)
        print("工具调用:")
        print(f"调用数量: {len(response.tool_calls)}")
        if response.tool_calls:
            for tool_call in response.tool_calls:
                print(f"工具: {tool_call.tool_name}")
                print(f"输入: {tool_call.tool_input}")
        print("-" * 50)
    except Exception as e:
        print(f"❌ LLM 测试失败: {str(e)}")
        print("-" * 50)

async def main():
    """主函数"""
    await test_file_operations()
    await test_llm_with_tools()
    print("中等难度任务测试完成！")

if __name__ == "__main__":
    asyncio.run(main())