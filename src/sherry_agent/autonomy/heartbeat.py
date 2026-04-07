import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sherry_agent.config.settings import Settings
from sherry_agent.infrastructure.monitoring import ResourceMonitor, ResourceSnapshot

from .scheduler import TaskScheduler
from .status import HeartbeatStatusManager
from .websocket import WebSocketServer


@dataclass
class HeartbeatConfig:
    """心跳引擎配置"""

    base_interval_seconds: int = 60
    low_power_interval_seconds: int = 300
    idle_threshold_cycles: int = 5
    max_concurrent_tasks: int = 3


@dataclass
class HeartbeatStatus:
    """心跳状态记录"""

    cycle_count: int = 0
    last_heartbeat_at: datetime | None = None
    tasks_completed_this_cycle: int = 0
    current_mode: str = "normal"
    consecutive_idle_cycles: int = 0


class HeartbeatEngine:
    """心跳引擎，驱动后台自主运行"""

    def __init__(
        self, settings: Settings | None = None, enable_websocket: bool = True
    ):
        self.settings = settings or Settings()
        self.config = HeartbeatConfig(
            base_interval_seconds=self.settings.heartbeat.base_interval,
            low_power_interval_seconds=self.settings.heartbeat.low_power_interval,
            idle_threshold_cycles=self.settings.heartbeat.idle_threshold,
            max_concurrent_tasks=self.settings.heartbeat.max_concurrent_tasks,
        )
        self.status = HeartbeatStatus()
        self._stopped = False
        self._tasks: list[asyncio.Task[None]] = []
        self.status_manager = HeartbeatStatusManager()
        self.scheduler = TaskScheduler()
        self._scheduler_started = False
        self.enable_websocket = enable_websocket
        self.websocket_server: WebSocketServer | None = None
        if self.enable_websocket:
            self.websocket_server = WebSocketServer()

        self.resource_monitor = ResourceMonitor(
            memory_warning_threshold=80.0,
            memory_critical_threshold=90.0,
            history_size=100,
        )
        self.resource_monitor.add_alert_callback(self._handle_resource_alert)

        self._restore_state()

    async def start(self) -> None:
        """启动心跳循环，阻塞直到被中止"""
        self._stopped = False
        try:
            if not self._scheduler_started:
                self.scheduler.start()
                self._scheduler_started = True

            if self.enable_websocket and self.websocket_server:
                self.websocket_server.start_in_background()

            await self.resource_monitor.start_monitoring(interval=5.0)

            while not self._stopped:
                await self.heartbeat_cycle()
                interval = self._get_interval()
                await asyncio.sleep(interval)
        finally:
            await self._cleanup()

    async def stop(self) -> None:
        """优雅停止心跳引擎"""
        self._stopped = True
        await self._cleanup()

    async def heartbeat_cycle(self) -> None:
        """
        执行一次心跳周期。

        1. 读取 HEARTBEAT.md 获取待办
        2. 检查 Cron 任务到期
        3. 检查挂起任务需恢复
        4. 执行到期任务
        5. 更新状态文件
        """
        try:
            snapshot = await asyncio.to_thread(self.resource_monitor.get_current_snapshot)
            self.resource_monitor.record_metric(
                "heartbeat_cycle",
                1.0,
                {"cycle": str(self.status.cycle_count)},
            )

            self.status.cycle_count += 1
            self.status.last_heartbeat_at = datetime.now(UTC)
            self.status.tasks_completed_this_cycle = 0

            hb_status = self.status_manager.read_status()

            cron_tasks = self.scheduler.get_all_tasks()
            hb_status["cron_schedule"] = []
            for task in cron_tasks:
                hb_status["cron_schedule"].append(
                    {
                        "task": task["name"],
                        "schedule": self._format_schedule(task),
                        "next_run": task["next_run"],
                    }
                )

            pending_tasks = hb_status.get("pending_tasks", [])
            max_tasks = self._get_adjusted_max_concurrent(snapshot)
            for task in pending_tasks[:max_tasks]:
                await self._execute_task(task)
                self.status.tasks_completed_this_cycle += 1
                self.status_manager.remove_pending_task(task)
                self.status_manager.add_activity(f"Completed task: {task}")

            hb_status["mode"] = self.status.current_mode
            hb_status["last_heartbeat"] = self.status.last_heartbeat_at.isoformat()
            hb_status["cycle_count"] = self.status.cycle_count
            hb_status["resource_stats"] = self.resource_monitor.get_statistics()
            self.status_manager.write_status(hb_status)

            if self.enable_websocket and self.websocket_server:
                status_update = {
                    "heartbeat": self.get_status(),
                    "cron_tasks": self.get_all_tasks(),
                    "pending_tasks": hb_status.get("pending_tasks", []),
                    "recent_activity": hb_status.get("recent_activity", []),
                    "resource_stats": self.resource_monitor.get_statistics(),
                }
                self.websocket_server.send_status_update(status_update)

            self._check_idle_status()

        except Exception as e:
            print(f"Heartbeat cycle error: {e}")
            self.status_manager.add_activity(f"Error in heartbeat cycle: {e}")

    async def _execute_task(self, task: str) -> None:
        """执行任务"""
        print(f"Executing task: {task}")
        await asyncio.sleep(0.5)

    def _get_adjusted_max_concurrent(self, snapshot: ResourceSnapshot) -> int:
        """根据资源使用情况动态调整并发限制"""
        base_max = self.config.max_concurrent_tasks

        if snapshot.memory_percent >= 90:
            return max(1, base_max - 2)
        elif snapshot.memory_percent >= 80:
            return max(1, base_max - 1)
        elif snapshot.cpu_percent >= 90:
            return max(1, base_max - 1)

        return base_max

    def _handle_resource_alert(self, alert_type: str, data: dict[str, Any]) -> None:
        """处理资源告警"""
        if alert_type == "memory_critical":
            print(
                f"CRITICAL: Memory usage {data['memory_percent']:.1f}% exceeds threshold {data['threshold']}%"
            )
            self.status_manager.add_activity(
                f"Memory critical: {data['memory_percent']:.1f}%"
            )
        elif alert_type == "memory_warning":
            print(
                f"WARNING: Memory usage {data['memory_percent']:.1f}% exceeds threshold {data['threshold']}%"
            )
            self.status_manager.add_activity(
                f"Memory warning: {data['memory_percent']:.1f}%"
            )

    async def _cleanup(self) -> None:
        """清理资源"""
        await self.resource_monitor.stop_monitoring()
        for task in self._tasks:
            if not task.done():
                task.cancel()
        self._tasks.clear()
        self.scheduler.stop()
        if self.enable_websocket and self.websocket_server:
            await self.websocket_server.stop()

    def _get_interval(self) -> int:
        """获取当前心跳间隔"""
        if self.status.current_mode == "low_power":
            return self.config.low_power_interval_seconds
        return self.config.base_interval_seconds

    def _check_idle_status(self) -> None:
        """检查空闲状态并切换模式"""
        if self.status.tasks_completed_this_cycle == 0:
            self.status.consecutive_idle_cycles += 1
        else:
            self.status.consecutive_idle_cycles = 0
            if self.status.current_mode == "low_power":
                self.status.current_mode = "normal"

        if self.status.consecutive_idle_cycles >= self.config.idle_threshold_cycles:
            self.status.current_mode = "low_power"

    def get_status(self) -> dict[str, Any]:
        """获取当前状态"""
        return {
            "cycle_count": self.status.cycle_count,
            "last_heartbeat_at": (
                self.status.last_heartbeat_at.isoformat()
                if self.status.last_heartbeat_at
                else None
            ),
            "current_mode": self.status.current_mode,
            "consecutive_idle_cycles": self.status.consecutive_idle_cycles,
            "tasks_completed_this_cycle": self.status.tasks_completed_this_cycle,
        }

    def _format_schedule(self, task: dict[str, Any]) -> str:
        """格式化任务调度信息"""
        task_type = task.get("type")
        if task_type == "cron":
            return task.get("expression", "")
        elif task_type == "interval":
            interval = task.get("interval", {})
            parts = []
            if interval.get("days", 0) > 0:
                parts.append(f"{interval['days']}d")
            if interval.get("hours", 0) > 0:
                parts.append(f"{interval['hours']}h")
            if interval.get("minutes", 0) > 0:
                parts.append(f"{interval['minutes']}m")
            if interval.get("seconds", 0) > 0:
                parts.append(f"{interval['seconds']}s")
            return " ".join(parts) if parts else "0s"
        elif task_type == "date":
            return f"at {task.get('run_date', '')}"
        return ""

    def add_cron_task(
        self,
        name: str,
        func: Callable[..., Any],
        cron_expression: str,
        args: tuple[Any, ...] = (),
        kwargs: dict[str, Any] | None = None,
    ) -> str:
        """添加 Cron 任务"""
        if not self._scheduler_started:
            self.scheduler.start()
            self._scheduler_started = True
        return self.scheduler.add_cron_task(name, func, cron_expression, args, kwargs)

    def add_interval_task(
        self,
        name: str,
        func: Callable[..., Any],
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        args: tuple[Any, ...] = (),
        kwargs: dict[str, Any] | None = None,
    ) -> str:
        """添加固定间隔任务"""
        if not self._scheduler_started:
            self.scheduler.start()
            self._scheduler_started = True
        return self.scheduler.add_interval_task(
            name, func, seconds, minutes, hours, days, args, kwargs
        )

    def add_date_task(
        self,
        name: str,
        func: Callable[..., Any],
        run_date: datetime,
        args: tuple[Any, ...] = (),
        kwargs: dict[str, Any] | None = None,
    ) -> str:
        """添加一次性任务"""
        if not self._scheduler_started:
            self.scheduler.start()
            self._scheduler_started = True
        return self.scheduler.add_date_task(name, func, run_date, args, kwargs)

    def remove_task(self, task_id: str) -> None:
        """移除任务"""
        self.scheduler.remove_task(task_id)

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """获取所有任务"""
        return self.scheduler.get_all_tasks()

    def _restore_state(self) -> None:
        """从 HEARTBEAT.md 恢复状态"""
        try:
            hb_status = self.status_manager.read_status()

            if "cycle_count" in hb_status:
                self.status.cycle_count = hb_status["cycle_count"]
            if "mode" in hb_status:
                self.status.current_mode = hb_status["mode"]
            if "last_heartbeat" in hb_status:
                try:
                    self.status.last_heartbeat_at = datetime.fromisoformat(
                        hb_status["last_heartbeat"]
                    )
                except (ValueError, TypeError):
                    pass

            print(
                f"State restored from HEARTBEAT.md: cycle_count={self.status.cycle_count}, mode={self.status.current_mode}"
            )
        except Exception as e:
            print(f"Error restoring state: {e}")
