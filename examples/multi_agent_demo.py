#!/usr/bin/env python3
"""
多Agent协作示例

展示如何使用SherryAgent框架创建多Agent协作场景
"""

import asyncio
import sys
from typing import List, Dict

# 添加项目根目录到Python路径
sys.path.insert(0, '/Users/liuminxuan/Desktop/sherryAgent')

from sherry_agent.llm.client import LLMClient
from sherry_agent.orchestration.orchestrator import Orchestrator
from sherry_agent.orchestration.lane import Lane
from sherry_agent.orchestration.models import SubTask


async def multi_agent_task():
    """多Agent协作任务示例"""
    print("=== SherryAgent 多Agent协作示例 ===")
    print()
    
    # 1. 初始化LLM客户端
    print("1. 初始化LLM客户端...")
    llm_client = LLMClient(api_key="YOUR_API_KEY")
    
    # 2. 创建任务编排器
    print("2. 创建任务编排器...")
    orchestrator = Orchestrator(llm_client)
    
    # 3. 创建Lane队列（用于任务调度）
    print("3. 创建任务执行队列...")
    lane = Lane(llm_client=llm_client, max_workers=3)
    
    # 4. 定义复杂任务
    complex_task = "开发一个简单的天气查询应用，包括：
- 前端界面设计
- 后端API开发
- 天气数据集成
- 测试和部署"
    
    print(f"4. 分解复杂任务：{complex_task}")
    
    # 5. 分解任务为子任务
    print("5. 分解任务为子任务...")
    sub_tasks = await orchestrator.decompose(complex_task, "main_task_1")
    
    print(f"   生成了 {len(sub_tasks)} 个子任务：")
    for i, task in enumerate(sub_tasks, 1):
        deps = "无" if not task.dependencies else ", ".join(task.dependencies)
        print(f"   {i}. {task.description} (优先级: {task.priority.name}, 依赖: {deps})")
    
    # 6. 执行子任务
    print("\n6. 执行子任务...")
    results = await orchestrator.execute_sub_tasks(sub_tasks, lane)
    
    # 7. 展示执行结果
    print("\n7. 执行结果：")
    for task_id, result in results.items():
        task = next((t for t in sub_tasks if t.sub_task_id == task_id), None)
        if task:
            print(f"   - {task.description}: {result[:100]}...")
    
    # 8. 清理资源
    print("\n8. 清理资源...")
    await lane.stop()
    
    print("\n=== 多Agent协作示例完成 ===")


async def simple_agent_demo():
    """简单Agent演示"""
    print("=== SherryAgent 简单Agent演示 ===")
    print()
    
    # 1. 初始化LLM客户端
    print("1. 初始化LLM客户端...")
    llm_client = LLMClient(api_key="YOUR_API_KEY")
    
    # 2. 创建Lane队列
    print("2. 创建任务执行队列...")
    lane = Lane(llm_client=llm_client, max_workers=1)
    
    # 3. 创建一个简单任务
    simple_task = SubTask(
        sub_task_id="demo_task_1",
        description="解释什么是人工智能Agent",
        parent_task_id="demo_parent",
        priority="NORMAL"
    )
    
    print(f"3. 执行任务：{simple_task.description}")
    
    # 4. 提交任务并等待结果
    ticket_id = await lane.submit(simple_task)
    completed_task = await lane.wait_for_result(ticket_id)
    
    print("\n4. 任务结果：")
    print(completed_task.result)
    
    # 5. 清理资源
    print("\n5. 清理资源...")
    await lane.stop()
    
    print("\n=== 简单Agent演示完成 ===")


if __name__ == "__main__":
    print("SherryAgent 框架演示")
    print("=" * 50)
    print("1. 简单Agent演示")
    print("2. 多Agent协作示例")
    print("=" * 50)
    
    choice = input("请选择演示类型 (1/2): ")
    
    if choice == "1":
        asyncio.run(simple_agent_demo())
    elif choice == "2":
        asyncio.run(multi_agent_task())
    else:
        print("无效选择，退出程序")
