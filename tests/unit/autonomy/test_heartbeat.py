import asyncio
import tempfile
import os
from datetime import datetime
import pytest

from sherry_agent.autonomy import HeartbeatEngine, HeartbeatStatusManager


async def test_heartbeat_engine_start_stop():
    """测试心跳引擎的启动和停止"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        engine = HeartbeatEngine(enable_websocket=False)
        
        # 重写 status_manager 使用临时文件
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        
        # 启动心跳引擎（非阻塞）
        task = asyncio.create_task(engine.start())
        
        # 等待一段时间，确保心跳循环运行
        await asyncio.sleep(0.3)
        
        # 停止心跳引擎
        await engine.stop()
        
        # 等待任务完成
        await task
        
        # 验证心跳至少执行了一次
        assert engine.status.cycle_count > 0
        assert engine.status.last_heartbeat_at is not None
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_heartbeat_cycle_execution():
    """测试心跳周期的执行"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        engine = HeartbeatEngine(enable_websocket=False)
        
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        
        engine.status.cycle_count = 0
        engine.status.current_mode = "normal"
        engine.status.consecutive_idle_cycles = 0
        
        await engine.heartbeat_cycle()
        
        assert engine.status.cycle_count == 1
        assert engine.status.last_heartbeat_at is not None
        assert engine.status.tasks_completed_this_cycle == 0
        assert engine.status.current_mode == "normal"
        assert engine.status.consecutive_idle_cycles == 1
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_low_power_mode():
    """测试低功耗模式"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        engine = HeartbeatEngine(enable_websocket=False)
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        engine.status.cycle_count = 0
        engine.status.current_mode = "normal"
        engine.status.consecutive_idle_cycles = 0
        
        for _ in range(6):
            await engine.heartbeat_cycle()
        
        assert engine.status.current_mode == "low_power"
        assert engine.status.consecutive_idle_cycles == 6
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_wake_from_low_power():
    """测试从低功耗模式唤醒"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        engine = HeartbeatEngine(enable_websocket=False)
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        engine.status.cycle_count = 0
        engine.status.current_mode = "normal"
        engine.status.consecutive_idle_cycles = 0
        
        for _ in range(6):
            await engine.heartbeat_cycle()
        assert engine.status.current_mode == "low_power"
        
        engine.status.tasks_completed_this_cycle = 1
        engine._check_idle_status()
        
        assert engine.status.current_mode == "normal"
        assert engine.status.consecutive_idle_cycles == 0
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_get_status():
    """测试获取状态"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        engine = HeartbeatEngine(enable_websocket=False)
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        engine.status.cycle_count = 0
        engine.status.current_mode = "normal"
        engine.status.consecutive_idle_cycles = 0
        
        await engine.heartbeat_cycle()
        
        status = engine.get_status()
        
        assert "cycle_count" in status
        assert "last_heartbeat_at" in status
        assert "current_mode" in status
        assert "consecutive_idle_cycles" in status
        assert "tasks_completed_this_cycle" in status
        
        assert status["cycle_count"] == 1
        assert status["current_mode"] == "normal"
        assert status["consecutive_idle_cycles"] == 1
        assert status["tasks_completed_this_cycle"] == 0
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
