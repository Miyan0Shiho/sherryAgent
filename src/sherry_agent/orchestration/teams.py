"""Agent Teams功能"""

import asyncio
from typing import Dict, List

from .models import SubTask
from .orchestrator import Orchestrator
from .lane import LaneQueue


class TeamLead:
    """Team Lead角色"""

    def __init__(self, orchestrator: Orchestrator, lane: LaneQueue):
        """
        初始化Team Lead

        Args:
            orchestrator: 编排器实例
            lane: Lane队列实例
        """
        self.orchestrator = orchestrator
        self.lane = lane
        self.teammates: Dict[str, Teammate] = {}
        self.task_list: List[SubTask] = []

    async def assign_task(self, task_description: str, teammate_id: str) -> str:
        """
        分配任务给Teammate

        Args:
            task_description: 任务描述
            teammate_id: Teammate ID

        Returns:
            任务ID
        """
        # 分解任务
        subtasks = await self.orchestrator.decompose(task_description, f"team_task_{id(self)}")
        self.task_list.extend(subtasks)

        # 分配给Teammate
        if teammate_id in self.teammates:
            teammate = self.teammates[teammate_id]
            for task in subtasks:
                task.assigned_agent_id = teammate_id
                ticket_id = await self.lane.submit(task)
                teammate.add_task(ticket_id, task)
            return f"任务已分配给Teammate {teammate_id}"
        else:
            return f"Teammate {teammate_id} 不存在"

    async def monitor_progress(self) -> Dict[str, str]:
        """
        监控任务进度

        Returns:
            任务ID到状态的映射
        """
        progress = {}
        for task in self.task_list:
            if task.assigned_agent_id and task.assigned_agent_id in self.teammates:
                teammate = self.teammates[task.assigned_agent_id]
                status = teammate.get_task_status(task.sub_task_id)
                progress[task.sub_task_id] = status
        return progress

    def add_teammate(self, teammate_id: str, teammate):
        """
        添加Teammate

        Args:
            teammate_id: Teammate ID
            teammate: Teammate实例
        """
        self.teammates[teammate_id] = teammate


class Teammate:
    """Teammate角色"""

    def __init__(self, agent_id: str):
        """
        初始化Teammate

        Args:
            agent_id: Agent ID
        """
        self.agent_id = agent_id
        self.tasks: Dict[str, SubTask] = {}
        self.ticket_map: Dict[str, str] = {}  # ticket_id -> task_id

    def add_task(self, ticket_id: str, task: SubTask):
        """
        添加任务

        Args:
            ticket_id: 票据ID
            task: 子任务
        """
        self.tasks[task.sub_task_id] = task
        self.ticket_map[ticket_id] = task.sub_task_id

    def get_task_status(self, task_id: str) -> str:
        """
        获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            return f"{task.status.value}: {task.result or '进行中'}"
        return "任务不存在"

    async def complete_task(self, task_id: str, result: str):
        """
        完成任务

        Args:
            task_id: 任务ID
            result: 任务结果
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.result = result


__all__ = ["TeamLead", "Teammate"]