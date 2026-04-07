---
title: "MVP-3 自主运行 详细计划"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["mvp-roadmap.md", "mvp-2-plan.md"]
---

# MVP-3 自主运行 详细计划

## 目标

实现后台自主运行能力，支持心跳驱动和定时调度。

## 实现范围

- 心跳引擎：while-True循环 + 可配置周期
- Cron调度：集成APScheduler，支持Cron表达式
- 后台模式：CLI可切换到后台运行
- WebSocket状态推送：实时推送任务执行状态
- 空闲检测与低功耗模式

## 任务列表

### Week 1

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T1.1 | 心跳引擎基础结构 | P0 |
| T1.2 | 心跳循环实现 | P0 |
| T1.3 | Cron调度集成 | P0 |

### Week 2

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T2.1 | 后台模式实现 | P0 |
| T2.2 | WebSocket服务 | P0 |
| T2.3 | 空闲检测与低功耗模式 | P1 |
| T2.4 | 断电恢复 | P0 |
| T2.5 | 集成测试 | P1 |

## 技术要点

### 心跳引擎核心

```python
class HeartbeatEngine:
    async def start(self) -> None:
        """启动心跳循环"""
        while not self._stopped:
            await self.heartbeat_cycle()
            interval = self._get_interval()
            await asyncio.sleep(interval)

    async def heartbeat_cycle(self) -> None:
        """执行一次心跳周期"""
        # 1. 读取 HEARTBEAT.md 获取待办
        # 2. 检查 Cron 任务到期
        # 3. 检查挂起任务需恢复
        # 4. 执行到期任务
        # 5. 更新状态文件
        ...
```

### Cron调度配置

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# Cron表达式
scheduler.add_job(task, 'cron', hour=8, minute=0)

# 固定间隔
scheduler.add_job(task, 'interval', hours=2)

# 一次性
scheduler.add_job(task, 'date', run_date='2026-04-04 08:00:00')
```

## 验收标准

| 编号 | 验收条件 | 验证方式 |
|------|---------|---------|
| 3.1 | 心跳引擎持续运行24小时无崩溃 | 长时间运行测试 |
| 3.2 | Cron任务按预期时间触发 | 定时任务测试 |
| 3.3 | CLI可切换到后台，WebSocket推送状态 | 手动测试 |
| 3.4 | 断电重启后心跳引擎自动恢复 | 崩溃恢复测试 |
| 3.5 | 空闲时自动进入低功耗模式 | 资源监控 |

## 依赖

- MVP-1 的 Agent Loop
- MVP-2 的持久化
- APScheduler >= 3.10
- websockets >= 13.0
- fastapi >= 0.115
