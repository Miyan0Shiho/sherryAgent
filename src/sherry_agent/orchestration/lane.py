"""Lane并发控制队列"""

import asyncio
import uuid
from typing import Dict, Optional

from .models import SubTask, LaneConfig, TaskStatus


class LaneQueue:
    """Lane并发控制队列"""

    def __init__(self, config: LaneConfig):
        """
        初始化Lane队列

        Args:
            config: Lane队列配置
        """
        self.config = config
        self._global_queue = asyncio.Queue()
        self._session_queues: Dict[str, asyncio.Queue] = {}
        self._result_map: Dict[str, SubTask] = {}
        self._active_tasks = 0
        self._task_semaphore = asyncio.Semaphore(config.max_concurrent)
        self._running = True

        # 启动队列处理器
        self._processor_task = asyncio.create_task(self._process_queue())

    async def submit(self, sub_task: SubTask) -> str:
        """
        提交子任务到队列，返回票据ID

        Args:
            sub_task: 子任务

        Returns:
            票据ID
        """
        ticket_id = str(uuid.uuid4())
        sub_task.status = TaskStatus.RUNNING

        # 存储任务，以便后续查询结果
        self._result_map[ticket_id] = sub_task

        # Session级串行
        if self.config.session_serial and hasattr(sub_task, 'session_id') and sub_task.session_id:
            session_id = sub_task.session_id
            if session_id not in self._session_queues:
                self._session_queues[session_id] = asyncio.Queue()
            await self._session_queues[session_id].put((ticket_id, sub_task))
        else:
            # Global级并发控制
            await self._global_queue.put((ticket_id, sub_task))

        return ticket_id

    async def wait_for_result(self, ticket_id: str) -> SubTask:
        """
        等待指定票据对应的子任务完成

        Args:
            ticket_id: 票据ID

        Returns:
            完成的子任务
        """
        while ticket_id in self._result_map:
            task = self._result_map[ticket_id]
            if task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                return task
            await asyncio.sleep(0.1)

        # 如果票据ID不存在，返回失败的任务
        task = SubTask(
            sub_task_id="unknown",
            description="未知任务",
            parent_task_id="unknown"
        )
        task.status = TaskStatus.FAILED
        task.result = "任务不存在"
        return task

    async def _process_queue(self):
        """处理队列中的任务"""
        while self._running:
            try:
                # 处理session队列
                for session_id, session_queue in list(self._session_queues.items()):
                    if not session_queue.empty():
                        ticket_id, task = await session_queue.get()
                        await self._execute_task(ticket_id, task)
                        session_queue.task_done()

                # 处理全局队列
                if not self._global_queue.empty():
                    ticket_id, task = await self._global_queue.get()
                    await self._execute_task(ticket_id, task)
                    self._global_queue.task_done()

                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"处理队列时出错: {e}")

    async def _execute_task(self, ticket_id: str, task: SubTask):
        """
        执行任务

        Args:
            ticket_id: 票据ID
            task: 子任务
        """
        async with self._task_semaphore:
            try:
                # 模拟任务执行
                await asyncio.sleep(1)  # 模拟执行时间
                task.status = TaskStatus.COMPLETED
                task.result = f"任务 '{task.description}' 执行成功"
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.result = f"任务执行失败: {str(e)}"
            finally:
                # 更新结果
                self._result_map[ticket_id] = task

    async def shutdown(self):
        """
        关闭队列
        """
        self._running = False
        if self._processor_task:
            await self._processor_task


__all__ = ["LaneQueue"]