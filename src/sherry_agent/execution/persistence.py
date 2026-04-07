from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import os
from typing import Any, Dict, List, Optional
import asyncio


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskState:
    """任务状态，序列化为 state.json"""

    task_id: str
    description: str
    status: TaskStatus
    parent_task_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    current_step: int = 0
    total_steps: int = 0
    progress: float = 0.0
    result_summary: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为可序列化的字典"""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "status": self.status.value,
            "parent_task_id": self.parent_task_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "progress": self.progress,
            "result_summary": self.result_summary,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskState":
        """从字典创建 TaskState"""
        return cls(
            task_id=data["task_id"],
            description=data["description"],
            status=TaskStatus(data["status"]),
            parent_task_id=data.get("parent_task_id"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            current_step=data.get("current_step", 0),
            total_steps=data.get("total_steps", 0),
            progress=data.get("progress", 0.0),
            result_summary=data.get("result_summary"),
            error_message=data.get("error_message"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class TranscriptEntry:
    """执行日志条目，追加写入 transcript.jsonl"""

    timestamp: datetime
    step_index: int
    event_type: str
    content: str
    token_usage: Optional[Dict[str, int]] = None
    duration_ms: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为可序列化的字典"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "step_index": self.step_index,
            "event_type": self.event_type,
            "content": self.content,
            "token_usage": self.token_usage,
            "duration_ms": self.duration_ms,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TranscriptEntry":
        """从字典创建 TranscriptEntry"""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            step_index=data["step_index"],
            event_type=data["event_type"],
            content=data["content"],
            token_usage=data.get("token_usage"),
            duration_ms=data.get("duration_ms"),
        )


@dataclass
class RecoveryContext:
    """任务恢复上下文"""

    task_state: TaskState
    messages: List[Dict[str, Any]]
    last_successful_step: int
    pending_steps: List[str]
    memory_snapshot: Optional[Dict[str, Any]] = None


class TaskPersistence:
    """任务持久化管理器"""

    def __init__(self, tasks_dir: str = "tasks"):
        """初始化持久化管理器

        Args:
            tasks_dir: 任务目录路径
        """
        self.tasks_dir = tasks_dir
        os.makedirs(self.tasks_dir, exist_ok=True)

    def get_task_dir(self, task_id: str) -> str:
        """获取任务目录路径

        Args:
            task_id: 任务ID

        Returns:
            任务目录路径
        """
        return os.path.join(self.tasks_dir, task_id)

    def get_state_file(self, task_id: str) -> str:
        """获取状态文件路径

        Args:
            task_id: 任务ID

        Returns:
            状态文件路径
        """
        return os.path.join(self.get_task_dir(task_id), "state.json")

    def get_transcript_file(self, task_id: str) -> str:
        """获取执行日志文件路径

        Args:
            task_id: 任务ID

        Returns:
            执行日志文件路径
        """
        return os.path.join(self.get_task_dir(task_id), "transcript.jsonl")

    def get_heartbeat_file(self, task_id: str) -> str:
        """获取心跳文件路径

        Args:
            task_id: 任务ID

        Returns:
            心跳文件路径
        """
        return os.path.join(self.get_task_dir(task_id), "heartbeat.md")

    def get_context_snapshot_dir(self, task_id: str) -> str:
        """获取上下文快照目录路径

        Args:
            task_id: 任务ID

        Returns:
            上下文快照目录路径
        """
        return os.path.join(self.get_task_dir(task_id), "context_snapshot")

    async def save_state(self, task_state: TaskState) -> None:
        """保存任务状态

        Args:
            task_state: 任务状态
        """
        task_dir = self.get_task_dir(task_state.task_id)
        os.makedirs(task_dir, exist_ok=True)

        state_file = self.get_state_file(task_state.task_id)
        temp_file = f"{state_file}.tmp"

        # 更新时间戳
        task_state.updated_at = datetime.now()

        # 先写入临时文件
        with open(temp_file, "w") as f:
            json.dump(task_state.to_dict(), f, indent=2, ensure_ascii=False)

        # 原子性重命名
        os.replace(temp_file, state_file)

    async def load_state(self, task_id: str) -> Optional[TaskState]:
        """加载任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态，如果文件不存在返回 None
        """
        state_file = self.get_state_file(task_id)

        if not os.path.exists(state_file):
            return None

        with open(state_file, "r") as f:
            data = json.load(f)

        return TaskState.from_dict(data)

    async def append_transcript(self, task_id: str, entry: TranscriptEntry) -> None:
        """追加执行日志

        Args:
            task_id: 任务ID
            entry: 日志条目
        """
        task_dir = self.get_task_dir(task_id)
        os.makedirs(task_dir, exist_ok=True)

        transcript_file = self.get_transcript_file(task_id)

        with open(transcript_file, "a") as f:
            json.dump(entry.to_dict(), f, ensure_ascii=False)
            f.write("\n")

    async def load_transcript(self, task_id: str) -> List[TranscriptEntry]:
        """加载执行日志

        Args:
            task_id: 任务ID

        Returns:
            日志条目列表
        """
        transcript_file = self.get_transcript_file(task_id)

        if not os.path.exists(transcript_file):
            return []

        entries = []
        with open(transcript_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    entries.append(TranscriptEntry.from_dict(data))

        return entries

    async def update_heartbeat(self, task_id: str, message: str) -> None:
        """更新心跳信息

        Args:
            task_id: 任务ID
            message: 心跳消息
        """
        task_dir = self.get_task_dir(task_id)
        os.makedirs(task_dir, exist_ok=True)

        heartbeat_file = self.get_heartbeat_file(task_id)

        with open(heartbeat_file, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")

    async def scan_interrupted_tasks(self) -> List[TaskState]:
        """扫描中断的任务

        Returns:
            中断的任务列表，按更新时间倒序排列
        """
        interrupted_tasks = []

        if not os.path.exists(self.tasks_dir):
            return interrupted_tasks

        for task_id in os.listdir(self.tasks_dir):
            task_dir = os.path.join(self.tasks_dir, task_id)
            if not os.path.isdir(task_dir):
                continue

            state = await self.load_state(task_id)
            if state and state.status in (TaskStatus.RUNNING, TaskStatus.SUSPENDED):
                interrupted_tasks.append(state)

        # 按更新时间倒序排列
        interrupted_tasks.sort(key=lambda x: x.updated_at, reverse=True)

        return interrupted_tasks

    async def recover_task(self, task_id: str) -> Optional[RecoveryContext]:
        """从断点恢复任务

        Args:
            task_id: 任务ID

        Returns:
            恢复上下文，如果任务不存在返回 None
        """
        # 读取任务状态
        task_state = await self.load_state(task_id)
        if not task_state:
            return None

        # 读取执行日志
        transcript = await self.load_transcript(task_id)

        # 构建消息列表
        messages = []
        last_successful_step = -1
        completed_steps = set()

        # 首先遍历所有日志，记录已完成的步骤
        for entry in transcript:
            if entry.event_type == "step_completed":
                last_successful_step = entry.step_index
                completed_steps.add(entry.step_index)

        # 再次遍历所有日志，构建消息列表和未完成的步骤
        pending_steps = []
        for entry in transcript:
            if entry.event_type == "user_input" or entry.event_type == "agent_output":
                messages.append({
                    "role": entry.event_type.replace("_input", "").replace("_output", ""),
                    "content": entry.content
                })
            elif entry.event_type == "step_started":
                # 只添加未完成的步骤
                if entry.step_index not in completed_steps:
                    pending_steps.append(entry.content)

        return RecoveryContext(
            task_state=task_state,
            messages=messages,
            last_successful_step=last_successful_step,
            pending_steps=pending_steps
        )

    async def create_task(self, task_id: str, description: str, parent_task_id: Optional[str] = None) -> TaskState:
        """创建新任务

        Args:
            task_id: 任务ID
            description: 任务描述
            parent_task_id: 父任务ID

        Returns:
            新创建的任务状态
        """
        task_state = TaskState(
            task_id=task_id,
            description=description,
            status=TaskStatus.PENDING,
            parent_task_id=parent_task_id
        )

        await self.save_state(task_state)
        await self.update_heartbeat(task_id, f"Task created: {description}")

        return task_state

    async def update_task_status(self, task_id: str, status: TaskStatus, error_message: Optional[str] = None) -> Optional[TaskState]:
        """更新任务状态

        Args:
            task_id: 任务ID
            status: 新状态
            error_message: 错误信息

        Returns:
            更新后的任务状态，如果任务不存在返回 None
        """
        task_state = await self.load_state(task_id)
        if not task_state:
            return None

        task_state.status = status
        task_state.error_message = error_message

        if status == TaskStatus.COMPLETED:
            task_state.completed_at = datetime.now()
            await self.update_heartbeat(task_id, "Task completed")
        elif status == TaskStatus.FAILED:
            await self.update_heartbeat(task_id, f"Task failed: {error_message}")
        elif status == TaskStatus.RUNNING:
            await self.update_heartbeat(task_id, "Task started")
        elif status == TaskStatus.SUSPENDED:
            await self.update_heartbeat(task_id, "Task suspended")

        await self.save_state(task_state)
        return task_state

    async def update_task_progress(self, task_id: str, current_step: int, total_steps: int, progress: float) -> Optional[TaskState]:
        """更新任务进度

        Args:
            task_id: 任务ID
            current_step: 当前步骤
            total_steps: 总步骤数
            progress: 进度百分比

        Returns:
            更新后的任务状态，如果任务不存在返回 None
        """
        task_state = await self.load_state(task_id)
        if not task_state:
            return None

        task_state.current_step = current_step
        task_state.total_steps = total_steps
        task_state.progress = progress

        await self.save_state(task_state)
        await self.update_heartbeat(task_id, f"Progress: {progress:.1f}% (Step {current_step}/{total_steps})")

        return task_state

    async def complete_task(self, task_id: str, result_summary: str) -> Optional[TaskState]:
        """完成任务

        Args:
            task_id: 任务ID
            result_summary: 结果摘要

        Returns:
            更新后的任务状态，如果任务不存在返回 None
        """
        task_state = await self.load_state(task_id)
        if not task_state:
            return None

        task_state.status = TaskStatus.COMPLETED
        task_state.result_summary = result_summary
        task_state.completed_at = datetime.now()
        task_state.progress = 100.0

        await self.save_state(task_state)
        await self.update_heartbeat(task_id, f"Task completed: {result_summary}")

        return task_state
