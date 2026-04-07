import os
import tempfile
from datetime import datetime

from sherry_agent.autonomy import HeartbeatStatusManager


def test_create_default_status():
    """测试创建默认状态"""
    manager = HeartbeatStatusManager()
    status = manager._create_default_status()
    
    assert status['mode'] == 'normal'
    assert 'last_heartbeat' in status
    assert status['cycle_count'] == 0
    assert status['pending_tasks'] == []
    assert status['cron_schedule'] == []
    assert status['recent_activity'] == []


def test_read_write_status():
    """测试读写状态文件"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = HeartbeatStatusManager(file_path=temp_file)
        
        # 写入初始状态
        initial_status = {
            "mode": "low_power",
            "last_heartbeat": "2026-04-04T00:00:00Z",
            "cycle_count": 42,
            "pending_tasks": ["Task 1", "Task 2"],
            "cron_schedule": [
                {"task": "Daily Report", "schedule": "0 8 * * *", "next_run": "2026-04-05T08:00:00Z"}
            ],
            "recent_activity": ["Completed Task 0"]
        }
        manager.write_status(initial_status)
        
        # 读取状态
        read_status = manager.read_status()
        
        assert read_status['mode'] == "low_power"
        assert read_status['cycle_count'] == 42
        assert "Task 1" in read_status['pending_tasks']
        assert "Task 2" in read_status['pending_tasks']
        assert len(read_status['cron_schedule']) == 1
        assert read_status['cron_schedule'][0]['task'] == "Daily Report"
        assert "Completed Task 0" in read_status['recent_activity']
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_add_remove_pending_task():
    """测试添加和移除待办任务"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = HeartbeatStatusManager(file_path=temp_file)
        
        # 添加任务
        manager.add_pending_task("Test Task")
        status = manager.read_status()
        assert "Test Task" in status['pending_tasks']
        
        # 移除任务
        manager.remove_pending_task("Test Task")
        status = manager.read_status()
        assert "Test Task" not in status['pending_tasks']
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_add_activity():
    """测试添加活动记录"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = HeartbeatStatusManager(file_path=temp_file)
        
        # 添加活动
        manager.add_activity("Test Activity")
        status = manager.read_status()
        assert len(status['recent_activity']) == 1
        assert "Test Activity" in status['recent_activity'][0]
        
        # 测试活动记录限制
        for i in range(15):
            manager.add_activity(f"Activity {i}")
        status = manager.read_status()
        assert len(status['recent_activity']) == 10  # 只保留最近 10 条
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
