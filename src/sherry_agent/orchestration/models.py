"""编排模块的数据模型"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class SubTask:
    """子任务定义"""

    sub_task_id: str
    description: str
    parent_task_id: str
    assigned_agent_id: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None


@dataclass
class ForkConfig:
    """子Agent Fork配置"""

    inherit_system_prompt: bool = True
    inherit_tools: Optional[List[str]] = None  # None表示继承全部
    extra_tools: List[str] = field(default_factory=list)
    extra_permissions: List[str] = field(default_factory=list)
    restricted_paths: List[str] = field(default_factory=list)
    max_tokens: int = 4096


@dataclass
class LaneConfig:
    """Lane队列配置"""

    max_concurrent: int = 3
    session_serial: bool = True  # 同一会话内串行
    priority_queue: bool = True


__all__ = [
    "TaskStatus",
    "TaskPriority",
    "SubTask",
    "ForkConfig",
    "LaneConfig",
]