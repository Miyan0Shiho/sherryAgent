---
title: "Task Service 与恢复契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "./core-data-contracts.md"
  - "./data-flow.md"
---

# Task Service 与恢复契约

任务持久化现在统一纳入 `Task Service`，其核心不是“目录里存什么文件”，而是如何保证任务、运行和恢复的一致性。

## Task Service 的职责

- 创建与维护 Task
- 建立和关闭 Run
- 管理状态机
- 维护幂等键、依赖、优先级
- 记录恢复所需的最小上下文

## 恢复契约

- 恢复对象以 `Task` 和 `Run` 为单位，而不是以临时日志文件为单位
- 恢复必须优先保证一致性，而不是盲目续跑
- 已进入 `waiting_confirmation` 的任务不能自动越过确认继续执行
- 恢复过程本身必须形成新的 Decision 和审计记录

## 最小恢复信息

- 最后已确认的状态
- 最后可重放的事件位置
- 当前预算消耗
- 当前等待中的确认或阻塞原因
- 最近一次有效证据集

## 失败与降级

- 无法安全恢复：标记为 `blocked`
- 上下文丢失：退化为只读诊断报告
- 预算不足：停止恢复并请求人工决定是否继续

