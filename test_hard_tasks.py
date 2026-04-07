#!/usr/bin/env python3
"""
测试 SherryAgent 执行困难任务的能力
"""

import asyncio
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
        elif tool_name == "exec_shell":
            result = await exec_shell(tool_input["command"])
            return result.content, result.metadata
        else:
            return f"工具 {tool_name} 不存在", {}

async def test_multi_step_task():
    """测试多步骤任务"""
    print("测试多步骤问题解决能力...\n")
    
    # 创建 Ollama 客户端
    client = OllamaClient()
    
    # 定义工具
    tools = [
        {
            "type": "function",
            "function": {
                "name": "exec_shell",
                "description": "执行 Shell 命令",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "要执行的 Shell 命令"
                        }
                    },
                    "required": ["command"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "写入文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的文件内容"
                        }
                    },
                    "required": ["path", "content"]
                }
            }
        }
    ]
    
    # 测试任务：分析项目结构并生成报告
    messages = [
        {
            "role": "user", 
            "content": "请分析 SherryAgent 项目的结构，统计各个目录的文件数量，然后将分析结果写入到 project_analysis.md 文件中"
        }
    ]
    
    try:
        response = await client.chat(
            messages=messages,
            model="qwen3:0.6b",
            max_tokens=500,
            tools=tools,
            system_prompt="你是一个 helpful 的 AI 助手，能够使用工具完成多步骤任务"
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
        print(f"❌ 测试失败: {str(e)}")
        print("-" * 50)

async def test_complex_reasoning():
    """测试复杂推理能力"""
    print("测试复杂推理能力...\n")
    
    # 创建 Ollama 客户端
    client = OllamaClient()
    
    # 测试任务：解决复杂问题
    messages = [
        {
            "role": "user", 
            "content": "假设有一个数列：1, 3, 6, 10, 15, ... 请找出第 100 项的值，并解释你的思考过程"
        }
    ]
    
    try:
        response = await client.chat(
            messages=messages,
            model="qwen3:0.6b",
            max_tokens=300,
            system_prompt="你是一个 helpful 的 AI 助手，能够解决复杂的数学问题"
        )
        
        print("✅ LLM 响应成功！")
        print("响应:")
        print(response.content)
        print("-" * 50)
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print("-" * 50)

async def test_tool_chain():
    """测试工具调用链"""
    print("测试工具调用链...\n")
    
    # 创建工具执行器
    tool_executor = TestToolExecutor()
    
    try:
        # 步骤 1: 列出 src 目录
        print("步骤 1: 列出 src 目录")
        content, metadata = await tool_executor.execute_tool(
            "exec_shell",
            {"command": "ls -la src"},
            "step-1"
        )
        print("✅ 完成！")
        
        # 步骤 2: 统计文件数量
        print("步骤 2: 统计项目文件数量")
        content, metadata = await tool_executor.execute_tool(
            "exec_shell",
            {"command": "find . -type f -name '*.py' | wc -l"},
            "step-2"
        )
        print("✅ 完成！")
        
        # 步骤 3: 写入分析报告
        print("步骤 3: 写入分析报告")
        report_content = f"# 项目分析报告\n\n## 文件统计\nPython 文件数量: {content.strip()}\n\n## 目录结构\n{metadata.get('stdout', '')}"
        content, metadata = await tool_executor.execute_tool(
            "write_file",
            {"path": "project_report.md", "content": report_content},
            "step-3"
        )
        print("✅ 完成！")
        print(f"结果: {content}")
        print("-" * 50)
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print("-" * 50)

async def main():
    """主函数"""
    await test_multi_step_task()
    await test_complex_reasoning()
    await test_tool_chain()
    print("困难任务测试完成！")

if __name__ == "__main__":
    asyncio.run(main())