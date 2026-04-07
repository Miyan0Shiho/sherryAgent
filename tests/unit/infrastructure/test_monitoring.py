"""
资源监控模块单元测试
"""

import asyncio
import time
from unittest.mock import MagicMock, patch

import pytest

from sherry_agent.infrastructure.monitoring import (
    PerformanceMetric,
    ResourceMonitor,
    ResourceSnapshot,
)


class TestResourceSnapshot:
    """测试 ResourceSnapshot 数据类"""

    def test_create_snapshot(self):
        """测试创建资源快照"""
        snapshot = ResourceSnapshot(
            timestamp=time.time(),
            memory_percent=50.0,
            cpu_percent=30.0,
            memory_mb=256.0,
        )

        assert snapshot.memory_percent == 50.0
        assert snapshot.cpu_percent == 30.0
        assert snapshot.memory_mb == 256.0
        assert snapshot.timestamp > 0


class TestPerformanceMetric:
    """测试 PerformanceMetric 数据类"""

    def test_create_metric(self):
        """测试创建性能指标"""
        metric = PerformanceMetric(
            name="test_metric",
            value=100.0,
            timestamp=time.time(),
        )

        assert metric.name == "test_metric"
        assert metric.value == 100.0
        assert metric.tags == {}

    def test_create_metric_with_tags(self):
        """测试创建带标签的性能指标"""
        metric = PerformanceMetric(
            name="test_metric",
            value=100.0,
            timestamp=time.time(),
            tags={"env": "test", "region": "us"},
        )

        assert metric.tags == {"env": "test", "region": "us"}


class TestResourceMonitor:
    """测试 ResourceMonitor 类"""

    def test_init_default_values(self):
        """测试默认初始化值"""
        monitor = ResourceMonitor()

        assert monitor._memory_warning_threshold == 80.0
        assert monitor._memory_critical_threshold == 90.0
        assert len(monitor._history) == 0
        assert len(monitor._metrics) == 0
        assert len(monitor._callbacks) == 0
        assert monitor._running is False

    def test_init_custom_values(self):
        """测试自定义初始化值"""
        monitor = ResourceMonitor(
            memory_warning_threshold=70.0,
            memory_critical_threshold=85.0,
            history_size=50,
        )

        assert monitor._memory_warning_threshold == 70.0
        assert monitor._memory_critical_threshold == 85.0

    def test_get_current_snapshot(self):
        """测试获取当前资源快照"""
        monitor = ResourceMonitor()

        snapshot = monitor.get_current_snapshot()

        assert isinstance(snapshot, ResourceSnapshot)
        assert snapshot.timestamp > 0
        assert snapshot.memory_percent >= 0
        assert snapshot.cpu_percent >= 0
        assert snapshot.memory_mb > 0
        assert len(monitor._history) == 1

    def test_get_current_snapshot_adds_to_history(self):
        """测试快照添加到历史记录"""
        monitor = ResourceMonitor(history_size=5)

        for _ in range(3):
            monitor.get_current_snapshot()

        assert len(monitor._history) == 3

    def test_history_size_limit(self):
        """测试历史记录大小限制"""
        monitor = ResourceMonitor(history_size=3)

        for _ in range(5):
            monitor.get_current_snapshot()

        assert len(monitor._history) == 3

    def test_record_metric(self):
        """测试记录性能指标"""
        monitor = ResourceMonitor()

        monitor.record_metric("test_metric", 100.0)
        monitor.record_metric("test_metric", 200.0)

        metrics = monitor.get_metrics("test_metric")
        assert len(metrics) == 2
        assert metrics[0].value == 100.0
        assert metrics[1].value == 200.0

    def test_record_metric_with_tags(self):
        """测试记录带标签的性能指标"""
        monitor = ResourceMonitor()

        monitor.record_metric("test_metric", 100.0, tags={"env": "test"})

        metrics = monitor.get_metrics("test_metric")
        assert len(metrics) == 1
        assert metrics[0].tags == {"env": "test"}

    def test_get_metrics_empty(self):
        """测试获取不存在的指标"""
        monitor = ResourceMonitor()

        metrics = monitor.get_metrics("nonexistent")

        assert metrics == []

    def test_get_statistics_empty(self):
        """测试空历史记录的统计"""
        monitor = ResourceMonitor()

        stats = monitor.get_statistics()

        assert stats["sample_count"] == 0
        assert stats["memory_avg_percent"] == 0.0
        assert stats["cpu_avg_percent"] == 0.0

    def test_get_statistics_with_data(self):
        """测试有数据时的统计"""
        monitor = ResourceMonitor()

        for _ in range(3):
            monitor.get_current_snapshot()

        stats = monitor.get_statistics()

        assert stats["sample_count"] == 3
        assert stats["memory_avg_percent"] > 0
        assert stats["memory_max_percent"] > 0
        assert stats["cpu_avg_percent"] >= 0
        assert stats["cpu_max_percent"] >= 0

    def test_add_alert_callback(self):
        """测试添加告警回调"""
        monitor = ResourceMonitor()
        callback = MagicMock()

        monitor.add_alert_callback(callback)

        assert callback in monitor._callbacks

    def test_remove_alert_callback(self):
        """测试移除告警回调"""
        monitor = ResourceMonitor()
        callback = MagicMock()

        monitor.add_alert_callback(callback)
        monitor.remove_alert_callback(callback)

        assert callback not in monitor._callbacks

    def test_memory_warning_alert(self):
        """测试内存警告告警"""
        monitor = ResourceMonitor(
            memory_warning_threshold=50.0,
            memory_critical_threshold=90.0,
        )
        callback = MagicMock()
        monitor.add_alert_callback(callback)

        with patch.object(
            monitor._process,
            "memory_percent",
            return_value=60.0
        ):
            with patch.object(
                monitor._process,
                "memory_info"
            ) as mock_mem_info:
                mock_mem_info.return_value = MagicMock(rss=100 * 1024 * 1024)
                with patch.object(
                    monitor._process,
                    "cpu_percent",
                    return_value=10.0
                ):
                    monitor.get_current_snapshot()

        callback.assert_called_once()
        call_args = callback.call_args
        assert call_args[0][0] == "memory_warning"
        assert "memory_percent" in call_args[0][1]

    def test_memory_critical_alert(self):
        """测试内存严重告警"""
        monitor = ResourceMonitor(
            memory_warning_threshold=50.0,
            memory_critical_threshold=80.0,
        )
        callback = MagicMock()
        monitor.add_alert_callback(callback)

        with patch.object(
            monitor._process,
            "memory_percent",
            return_value=90.0
        ):
            with patch.object(
                monitor._process,
                "memory_info"
            ) as mock_mem_info:
                mock_mem_info.return_value = MagicMock(rss=100 * 1024 * 1024)
                with patch.object(
                    monitor._process,
                    "cpu_percent",
                    return_value=10.0
                ):
                    monitor.get_current_snapshot()

        callback.assert_called_once()
        call_args = callback.call_args
        assert call_args[0][0] == "memory_critical"

    def test_get_history(self):
        """测试获取历史记录"""
        monitor = ResourceMonitor()

        for _ in range(3):
            monitor.get_current_snapshot()

        history = monitor.get_history()

        assert len(history) == 3
        assert all(isinstance(s, ResourceSnapshot) for s in history)

    def test_clear_history(self):
        """测试清空历史记录"""
        monitor = ResourceMonitor()

        monitor.get_current_snapshot()
        assert len(monitor._history) == 1

        monitor.clear_history()
        assert len(monitor._history) == 0

    def test_clear_metrics(self):
        """测试清空指标"""
        monitor = ResourceMonitor()
        monitor.record_metric("metric1", 100.0)
        monitor.record_metric("metric2", 200.0)

        monitor.clear_metrics("metric1")

        assert len(monitor.get_metrics("metric1")) == 0
        assert len(monitor.get_metrics("metric2")) == 1

    def test_clear_all_metrics(self):
        """测试清空所有指标"""
        monitor = ResourceMonitor()
        monitor.record_metric("metric1", 100.0)
        monitor.record_metric("metric2", 200.0)

        monitor.clear_metrics()

        assert len(monitor._metrics) == 0

    def test_is_running_property(self):
        """测试 is_running 属性"""
        monitor = ResourceMonitor()

        assert monitor.is_running is False

    def test_get_current_memory_mb(self):
        """测试获取当前内存使用量"""
        monitor = ResourceMonitor()

        memory_mb = monitor.get_current_memory_mb()

        assert memory_mb > 0

    def test_get_current_memory_percent(self):
        """测试获取当前内存使用百分比"""
        monitor = ResourceMonitor()

        memory_percent = monitor.get_current_memory_percent()

        assert memory_percent >= 0

    def test_get_current_cpu_percent(self):
        """测试获取当前 CPU 使用百分比"""
        monitor = ResourceMonitor()

        cpu_percent = monitor.get_current_cpu_percent()

        assert cpu_percent >= 0


class TestResourceMonitorAsync:
    """测试 ResourceMonitor 异步功能"""

    async def test_start_stop_monitoring(self):
        """测试启动和停止监控"""
        monitor = ResourceMonitor()

        await monitor.start_monitoring(interval=0.1)
        assert monitor.is_running is True

        await asyncio.sleep(0.3)

        await monitor.stop_monitoring()
        assert monitor.is_running is False

    async def test_monitoring_collects_snapshots(self):
        """测试监控收集快照"""
        monitor = ResourceMonitor()

        await monitor.start_monitoring(interval=0.1)
        await asyncio.sleep(0.35)
        await monitor.stop_monitoring()

        assert len(monitor._history) >= 2

    async def test_double_start(self):
        """测试重复启动"""
        monitor = ResourceMonitor()

        await monitor.start_monitoring(interval=0.1)
        await monitor.start_monitoring(interval=0.1)

        assert monitor.is_running is True

        await monitor.stop_monitoring()

    async def test_stop_without_start(self):
        """测试未启动时停止"""
        monitor = ResourceMonitor()

        await monitor.stop_monitoring()

        assert monitor.is_running is False

    async def test_callback_exception_handling(self):
        """测试回调异常处理"""
        monitor = ResourceMonitor(
            memory_warning_threshold=10.0,
            memory_critical_threshold=20.0,
        )

        def bad_callback(alert_type: str, data: dict):
            raise ValueError("Test error")

        monitor.add_alert_callback(bad_callback)

        snapshot = monitor.get_current_snapshot()

        assert isinstance(snapshot, ResourceSnapshot)
