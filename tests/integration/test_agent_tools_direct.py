#!/usr/bin/env python3
"""
直接测试工具执行功能
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sherry_agent.infrastructure.tool_executor import ToolExecutor


async def test_tool_executor():
    """直接测试工具执行功能"""
    print("=== 直接测试工具执行功能 ===")
    
    # 创建工具执行器
    tool_executor = ToolExecutor()
    print("✅ 创建工具执行器成功")
    
    # 测试读取文件工具
    print("\n🔄 测试读取文件工具...")
    try:
        # 注意：ReadFileTool 期望的参数是 "path"，不是 "file_path"
        result_content, result_metadata = await tool_executor.execute_tool(
            tool_name="read_file",
            tool_input={"path": "AGENTS.md"},  # 使用正确的参数名
            call_id="test-1"
        )
        print("✅ 工具执行成功")
        print(f"结果元数据: {result_metadata}")
        print(f"文件内容预览: {result_content[:500]}...")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试执行命令工具
    print("\n🔄 测试执行命令工具...")
    try:
        result_content, result_metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "ls -la"},
            call_id="test-2"
        )
        print("✅ 工具执行成功")
        print(f"结果元数据: {result_metadata}")
        print(f"命令输出: {result_content}")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(test_tool_executor())
