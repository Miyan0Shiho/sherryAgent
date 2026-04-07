from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger


class TaskScheduler:
    """任务调度器，基于 APScheduler"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def start(self) -> None:
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()

    def stop(self) -> None:
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()

    def add_cron_task(self, 
                     name: str, 
                     func: Callable, 
                     cron_expression: str, 
                     args: tuple = (), 
                     kwargs: Dict[str, Any] = None) -> str:
        """
        添加 Cron 任务
        
        Args:
            name: 任务名称
            func: 任务函数
            cron_expression: Cron 表达式 (例如: "0 8 * * *")
            args: 函数参数
            kwargs: 函数关键字参数
            
        Returns:
            任务 ID
        """
        if kwargs is None:
            kwargs = {}
        
        # 解析 Cron 表达式
        parts = cron_expression.split()
        if len(parts) != 5:
            raise ValueError("Invalid cron expression format")
        
        minute, hour, day, month, day_of_week = parts
        trigger = CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week
        )
        
        job_id = self.scheduler.add_job(
            func=func,
            trigger=trigger,
            args=args,
            kwargs=kwargs,
            id=name,
            replace_existing=True
        ).id
        
        self.tasks[job_id] = {
            "name": name,
            "type": "cron",
            "expression": cron_expression,
            "next_run": self._get_next_run_time(job_id)
        }
        
        return job_id

    def add_interval_task(self, 
                         name: str, 
                         func: Callable, 
                         seconds: int = 0, 
                         minutes: int = 0, 
                         hours: int = 0, 
                         days: int = 0, 
                         args: tuple = (), 
                         kwargs: Dict[str, Any] = None) -> str:
        """
        添加固定间隔任务
        
        Args:
            name: 任务名称
            func: 任务函数
            seconds: 秒数
            minutes: 分钟数
            hours: 小时数
            days: 天数
            args: 函数参数
            kwargs: 函数关键字参数
            
        Returns:
            任务 ID
        """
        if kwargs is None:
            kwargs = {}
        
        trigger = IntervalTrigger(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days
        )
        
        job_id = self.scheduler.add_job(
            func=func,
            trigger=trigger,
            args=args,
            kwargs=kwargs,
            id=name,
            replace_existing=True
        ).id
        
        self.tasks[job_id] = {
            "name": name,
            "type": "interval",
            "interval": {
                "seconds": seconds,
                "minutes": minutes,
                "hours": hours,
                "days": days
            },
            "next_run": self._get_next_run_time(job_id)
        }
        
        return job_id

    def add_date_task(self, 
                     name: str, 
                     func: Callable, 
                     run_date: datetime, 
                     args: tuple = (), 
                     kwargs: Dict[str, Any] = None) -> str:
        """
        添加一次性任务
        
        Args:
            name: 任务名称
            func: 任务函数
            run_date: 运行时间
            args: 函数参数
            kwargs: 函数关键字参数
            
        Returns:
            任务 ID
        """
        if kwargs is None:
            kwargs = {}
        
        trigger = DateTrigger(run_date=run_date)
        
        job_id = self.scheduler.add_job(
            func=func,
            trigger=trigger,
            args=args,
            kwargs=kwargs,
            id=name,
            replace_existing=True
        ).id
        
        self.tasks[job_id] = {
            "name": name,
            "type": "date",
            "run_date": run_date.isoformat(),
            "next_run": run_date.isoformat()
        }
        
        return job_id

    def remove_task(self, task_id: str) -> None:
        """
        移除任务
        
        Args:
            task_id: 任务 ID
        """
        if task_id in self.tasks:
            self.scheduler.remove_job(task_id)
            del self.tasks[task_id]

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        获取所有任务
        
        Returns:
            任务列表
        """
        # 更新任务的下次运行时间
        for task_id in self.tasks:
            self.tasks[task_id]["next_run"] = self._get_next_run_time(task_id)
        
        return list(self.tasks.values())

    def _get_next_run_time(self, task_id: str) -> Optional[str]:
        """
        获取任务的下次运行时间
        
        Args:
            task_id: 任务 ID
            
        Returns:
            下次运行时间（ISO 格式）
        """
        job = self.scheduler.get_job(task_id)
        if job:
            next_run = job.next_run_time
            if next_run:
                return next_run.isoformat()
        return None
