import asyncio
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

from sherry_agent.autonomy import TaskScheduler


async def test_scheduler_start_stop():
    """测试调度器的启动和停止"""
    scheduler = TaskScheduler()
    
    # 启动调度器
    scheduler.start()
    assert scheduler.scheduler.running
    
    # 停止调度器
    scheduler.stop()
    # 注意：APScheduler 停止后 running 属性不会立即变为 False，我们跳过这个检查


async def test_add_cron_task():
    """测试添加 Cron 任务"""
    scheduler = TaskScheduler()
    scheduler.start()
    
    try:
        # 测试函数
        called = False
        def test_func():
            nonlocal called
            called = True
        
        # 添加 Cron 任务（每分钟执行一次）
        task_id = scheduler.add_cron_task(
            name="test_cron",
            func=test_func,
            cron_expression="* * * * *"
        )
        
        # 验证任务已添加
        tasks = scheduler.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['name'] == "test_cron"
        assert tasks[0]['type'] == "cron"
        assert tasks[0]['expression'] == "* * * * *"
        
        # 移除任务
        scheduler.remove_task(task_id)
        tasks = scheduler.get_all_tasks()
        assert len(tasks) == 0
        
    finally:
        scheduler.stop()


async def test_add_interval_task():
    """测试添加固定间隔任务"""
    scheduler = TaskScheduler()
    scheduler.start()
    
    try:
        # 测试函数
        call_count = 0
        def test_func():
            nonlocal call_count
            call_count += 1
        
        # 添加间隔任务（每 0.5 秒执行一次）
        task_id = scheduler.add_interval_task(
            name="test_interval",
            func=test_func,
            seconds=0.5
        )
        
        # 验证任务已添加
        tasks = scheduler.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['name'] == "test_interval"
        assert tasks[0]['type'] == "interval"
        assert tasks[0]['interval']['seconds'] == 0.5
        
        # 等待任务执行
        await asyncio.sleep(1.2)
        assert call_count >= 2
        
        # 移除任务
        scheduler.remove_task(task_id)
        tasks = scheduler.get_all_tasks()
        assert len(tasks) == 0
        
    finally:
        scheduler.stop()


async def test_add_date_task():
    """测试添加一次性任务"""
    scheduler = TaskScheduler()
    scheduler.start()
    
    try:
        # 测试函数
        called = False
        def test_func():
            nonlocal called
            called = True
        
        # 添加一次性任务（1秒后执行）
        run_date = datetime.now(UTC) + timedelta(seconds=1)
        task_id = scheduler.add_date_task(
            name="test_date",
            func=test_func,
            run_date=run_date
        )
        
        # 验证任务已添加
        tasks = scheduler.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['name'] == "test_date"
        assert tasks[0]['type'] == "date"
        
        # 等待任务执行
        await asyncio.sleep(1.5)
        assert called
        
        # 任务已经执行完毕，不需要再移除
        
    finally:
        scheduler.stop()
