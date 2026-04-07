import asyncio
import tempfile
import os
from datetime import datetime, timedelta, timezone
import pytest

UTC = timezone.utc

from sherry_agent.autonomy import HeartbeatEngine, HeartbeatStatusManager


async def test_heartbeat_engine_integration():
    """测试心跳引擎集成"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        # 创建心跳引擎实例（禁用 WebSocket 以简化测试）
        engine = HeartbeatEngine(enable_websocket=False)
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        
        # 确保状态是干净的
        engine.status.cycle_count = 0
        
        try:
            # 启动心跳引擎
            task = asyncio.create_task(engine.start())
            
            # 等待心跳循环运行几次
            await asyncio.sleep(1.2)
            
            # 验证心跳状态
            assert engine.status.cycle_count > 0
            assert engine.status.last_heartbeat_at is not None
            
            # 停止心跳引擎
            await engine.stop()
            await task
            
        finally:
            # 确保资源被清理
            await engine._cleanup()
            
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_cron_task_integration():
    """测试 Cron 任务集成"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        # 创建心跳引擎实例（禁用 WebSocket 以简化测试）
        engine = HeartbeatEngine(enable_websocket=False)
        engine.status_manager = HeartbeatStatusManager(file_path=temp_file)
        engine.status.cycle_count = 0
        
        try:
            # 测试变量
            task_executed = False
            
            # 定义测试任务
            def test_task():
                nonlocal task_executed
                task_executed = True
            
            # 添加一个间隔任务（每 0.5 秒执行一次）
            engine.add_interval_task(
                name="test_interval",
                func=test_task,
                seconds=0.5
            )
            
            # 启动心跳引擎
            task = asyncio.create_task(engine.start())
            
            # 等待任务执行
            await asyncio.sleep(1.2)
            
            # 验证任务是否执行
            assert task_executed
            
            # 停止心跳引擎
            await engine.stop()
            await task
            
        finally:
            # 确保资源被清理
            await engine._cleanup()
            
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


async def test_status_persistence():
    """测试状态持久化"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name
    
    try:
        # 创建第一个心跳引擎实例（禁用 WebSocket）
        engine1 = HeartbeatEngine(enable_websocket=False)
        engine1.status_manager = HeartbeatStatusManager(file_path=temp_file)
        engine1.status.cycle_count = 0
        
        try:
            # 执行几次心跳循环
            for _ in range(3):
                await engine1.heartbeat_cycle()
            
            # 记录当前状态
            cycle_count1 = engine1.status.cycle_count
            mode1 = engine1.status.current_mode
            
            # 停止第一个引擎
            await engine1._cleanup()
            
            # 创建第二个心跳引擎实例，应该从 HEARTBEAT.md 恢复状态
            engine2 = HeartbeatEngine(enable_websocket=False)
            engine2.status_manager = HeartbeatStatusManager(file_path=temp_file)
            
            try:
                # 验证状态是否恢复
                assert engine2.status.cycle_count == cycle_count1
                assert engine2.status.current_mode == mode1
                
            finally:
                # 确保资源被清理
                await engine2._cleanup()
                
        finally:
            # 确保资源被清理
            await engine1._cleanup()
            
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
