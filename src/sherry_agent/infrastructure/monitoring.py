"""
资源监控模块

提供系统资源（CPU、内存）监控和性能指标收集功能。
"""

from __future__ import annotations

import asyncio
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class ResourceSnapshot:
    """资源快照"""

    timestamp: float
    memory_percent: float
    cpu_percent: float
    memory_mb: float


@dataclass
class PerformanceMetric:
    """性能指标"""

    name: str
    value: float
    timestamp: float
    tags: dict[str, str] = field(default_factory=dict)


class ResourceMonitor:
    """资源监控器，监控系统资源使用情况"""

    def __init__(
        self,
        memory_warning_threshold: float = 80.0,
        memory_critical_threshold: float = 90.0,
        history_size: int = 100,
    ) -> None:
        self._memory_warning_threshold = memory_warning_threshold
        self._memory_critical_threshold = memory_critical_threshold
        self._history: deque[ResourceSnapshot] = deque(maxlen=history_size)
        self._metrics: dict[str, list[PerformanceMetric]] = {}
        self._callbacks: list[Callable[[str, dict[str, Any]], None]] = []
        self._running = False
        self._monitor_task: asyncio.Task[None] | None = None
        self._process = psutil.Process() if PSUTIL_AVAILABLE else None

    def get_current_snapshot(self, cpu_interval: float = 0.0) -> ResourceSnapshot:
        """获取当前资源快照"""
        if not PSUTIL_AVAILABLE or self._process is None:
            return ResourceSnapshot(
                timestamp=time.time(),
                memory_percent=0.0,
                cpu_percent=0.0,
                memory_mb=0.0,
            )

        memory_info = self._process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)
        memory_percent = self._process.memory_percent() or 0.0
        cpu_percent = self._process.cpu_percent(interval=cpu_interval) or 0.0

        snapshot = ResourceSnapshot(
            timestamp=time.time(),
            memory_percent=memory_percent,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
        )

        self._history.append(snapshot)

        self._check_thresholds(snapshot)

        return snapshot

    def _check_thresholds(self, snapshot: ResourceSnapshot) -> None:
        """检查资源阈值并触发告警"""
        alert_type: str | None = None
        alert_data: dict[str, Any] = {}

        if snapshot.memory_percent >= self._memory_critical_threshold:
            alert_type = "memory_critical"
            alert_data = {
                "memory_percent": snapshot.memory_percent,
                "memory_mb": snapshot.memory_mb,
                "threshold": self._memory_critical_threshold,
            }
        elif snapshot.memory_percent >= self._memory_warning_threshold:
            alert_type = "memory_warning"
            alert_data = {
                "memory_percent": snapshot.memory_percent,
                "memory_mb": snapshot.memory_mb,
                "threshold": self._memory_warning_threshold,
            }

        if alert_type:
            self._trigger_alert(alert_type, alert_data)

    def _trigger_alert(self, alert_type: str, data: dict[str, Any]) -> None:
        """触发告警回调"""
        for callback in self._callbacks:
            try:
                callback(alert_type, data)
            except Exception:
                pass

    async def start_monitoring(self, interval: float = 5.0) -> None:
        """开始定期监控"""
        if self._running:
            return

        self._running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop(interval))

    async def _monitor_loop(self, interval: float) -> None:
        """监控循环"""
        while self._running:
            try:
                await asyncio.to_thread(self.get_current_snapshot)
            except Exception:
                pass
            await asyncio.sleep(interval)

    async def stop_monitoring(self) -> None:
        """停止监控"""
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None

    def record_metric(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """记录性能指标"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
        )

        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(metric)

    def get_metrics(self, name: str) -> list[PerformanceMetric]:
        """获取指定指标的历史记录"""
        return self._metrics.get(name, [])

    def get_statistics(self) -> dict[str, Any]:
        """获取资源使用统计"""
        if not self._history:
            return {
                "sample_count": 0,
                "memory_avg_percent": 0.0,
                "memory_max_percent": 0.0,
                "memory_avg_mb": 0.0,
                "memory_max_mb": 0.0,
                "cpu_avg_percent": 0.0,
                "cpu_max_percent": 0.0,
            }

        memory_percents = [s.memory_percent for s in self._history]
        memory_mbs = [s.memory_mb for s in self._history]
        cpu_percents = [s.cpu_percent for s in self._history]

        return {
            "sample_count": len(self._history),
            "memory_avg_percent": sum(memory_percents) / len(memory_percents),
            "memory_max_percent": max(memory_percents),
            "memory_avg_mb": sum(memory_mbs) / len(memory_mbs),
            "memory_max_mb": max(memory_mbs),
            "cpu_avg_percent": sum(cpu_percents) / len(cpu_percents),
            "cpu_max_percent": max(cpu_percents),
        }

    def add_alert_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ) -> None:
        """添加告警回调"""
        self._callbacks.append(callback)

    def remove_alert_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ) -> None:
        """移除告警回调"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def get_history(self) -> list[ResourceSnapshot]:
        """获取历史快照列表"""
        return list(self._history)

    def clear_history(self) -> None:
        """清空历史记录"""
        self._history.clear()

    def clear_metrics(self, name: str | None = None) -> None:
        """清空指标记录"""
        if name:
            self._metrics.pop(name, None)
        else:
            self._metrics.clear()

    @property
    def is_running(self) -> bool:
        """检查监控是否正在运行"""
        return self._running

    def get_current_memory_mb(self) -> float:
        """获取当前内存使用量（MB）"""
        if not PSUTIL_AVAILABLE or self._process is None:
            return 0.0
        memory_info = self._process.memory_info()
        return float(memory_info.rss / (1024 * 1024))

    def get_current_memory_percent(self) -> float:
        """获取当前内存使用百分比"""
        if not PSUTIL_AVAILABLE or self._process is None:
            return 0.0
        result = self._process.memory_percent()
        return float(result) if result is not None else 0.0

    def get_current_cpu_percent(self) -> float:
        """获取当前 CPU 使用百分比"""
        if not PSUTIL_AVAILABLE or self._process is None:
            return 0.0
        result = self._process.cpu_percent(interval=0.0)
        return float(result) if result is not None else 0.0
