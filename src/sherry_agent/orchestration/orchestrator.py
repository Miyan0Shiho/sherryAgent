"""任务编排器"""

import asyncio
import json
from typing import List, Dict, Optional

from ..llm.client import LLMClient
from .models import SubTask, TaskPriority


class Orchestrator:
    """任务编排器"""

    def __init__(self, llm_client: LLMClient):
        """
        初始化编排器

        Args:
            llm_client: LLM客户端实例
        """
        self.llm_client = llm_client

    async def decompose(self, task_description: str, parent_task_id: str) -> List[SubTask]:
        """
        将顶层任务分解为子任务列表。

        Args:
            task_description: 顶层任务描述
            parent_task_id: 父任务ID

        Returns:
            子任务列表（含依赖关系）
        """
        prompt = f"""
        你是一个任务分解专家，将以下任务分解为独立的子任务，并标注依赖关系：

        任务：{task_description}

        要求：
        1. 分解为3-8个独立的子任务
        2. 每个子任务要有明确的职责边界
        3. 标注子任务之间的依赖关系
        4. 为每个子任务分配合理的优先级（CRITICAL、HIGH、NORMAL、LOW）

        输出格式（JSON）：
        {{"subtasks": [
            {{"sub_task_id": "唯一标识",
            "description": "子任务描述",
            "priority": "优先级",
            "dependencies": ["依赖的子任务ID列表"]
            }}
        ]}}
        """

        # 使用LLM生成子任务
        response = await self.llm_client.chat(
            messages=[{"role": "user", "content": prompt}],
            model="claude-3-opus-20240229",
            max_tokens=2048
        )

        # 解析LLM响应
        try:
            # 直接使用响应内容作为JSON
            data = json.loads(response.content)
            
            subtasks = []
            for task_data in data.get("subtasks", []):
                # 转换优先级
                priority_map = {
                    "CRITICAL": TaskPriority.CRITICAL,
                    "HIGH": TaskPriority.HIGH,
                    "NORMAL": TaskPriority.NORMAL,
                    "LOW": TaskPriority.LOW
                }
                priority = priority_map.get(task_data.get("priority", "NORMAL"), TaskPriority.NORMAL)

                subtask = SubTask(
                    sub_task_id=task_data.get("sub_task_id", f"sub_{len(subtasks)}"),
                    description=task_data.get("description", ""),
                    parent_task_id=parent_task_id,
                    priority=priority,
                    dependencies=task_data.get("dependencies", [])
                )
                subtasks.append(subtask)

            return subtasks
        except Exception as e:
            # 如果解析失败，返回默认的子任务
            return [
                SubTask(
                    sub_task_id="default_1",
                    description="分析任务需求",
                    parent_task_id=parent_task_id,
                    priority=TaskPriority.HIGH
                ),
                SubTask(
                    sub_task_id="default_2",
                    description="执行主要任务",
                    parent_task_id=parent_task_id,
                    priority=TaskPriority.CRITICAL,
                    dependencies=["default_1"]
                ),
                SubTask(
                    sub_task_id="default_3",
                    description="验证任务结果",
                    parent_task_id=parent_task_id,
                    priority=TaskPriority.NORMAL,
                    dependencies=["default_2"]
                )
            ]

    async def execute_sub_tasks(self, sub_tasks: List[SubTask], lane) -> Dict[str, str]:
        """
        通过Lane队列调度执行子任务。

        Args:
            sub_tasks: 子任务列表
            lane: Lane队列实例

        Returns:
            子任务ID到结果的映射
        """
        # 构建依赖DAG
        dependency_map = {task.sub_task_id: task.dependencies for task in sub_tasks}
        task_map = {task.sub_task_id: task for task in sub_tasks}

        # 拓扑排序
        def topological_sort(deps):
            visited = set()
            temp = set()
            order = []

            def visit(node):
                if node in temp:
                    raise ValueError("循环依赖检测到")
                if node not in visited:
                    temp.add(node)
                    for dep in deps.get(node, []):
                        visit(dep)
                    temp.remove(node)
                    visited.add(node)
                    order.append(node)

            for node in deps:
                if node not in visited:
                    visit(node)
            return order

        try:
            execution_order = topological_sort(dependency_map)
        except ValueError:
            # 如果有循环依赖，返回错误
            return {task.sub_task_id: "错误：存在循环依赖" for task in sub_tasks}

        # 提交任务到Lane队列
        results = {}
        ticket_map = {}

        # 按照拓扑排序顺序执行任务
        for task_id in execution_order:
            task = task_map[task_id]
            # 等待所有依赖完成
            for dep_id in task.dependencies:
                if dep_id not in results:
                    # 如果依赖未完成，等待它完成
                    if dep_id in ticket_map:
                        completed_task = await lane.wait_for_result(ticket_map[dep_id])
                        results[dep_id] = completed_task.result or "任务执行成功"

            # 提交当前任务
            ticket_id = await lane.submit(task)
            ticket_map[task_id] = ticket_id

        # 等待所有任务完成
        for task_id, ticket_id in ticket_map.items():
            if task_id not in results:
                completed_task = await lane.wait_for_result(ticket_id)
                results[task_id] = completed_task.result or "任务执行成功"

        return results


__all__ = ["Orchestrator"]