---
title: "Scheduler & Trigger 契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "../architecture/runtime-modes.md"
  - "./core-data-contracts.md"
---

# Scheduler & Trigger 契约

旧“心跳引擎”文档现统一收敛到 `Scheduler & Trigger` 模块，不再把 `while true` 循环视为唯一核心设计。

## 定位

- 所属模块：`Scheduler & Trigger`
- 负责：cron、事件触发、条件触发、节流、去重、批处理调度
- 服务对象：`Autonomous Background Loop`、`background-ops`、`bulk-analysis`

## 输入来源

- 固定时间计划
- 外部事件（仓库、部署、告警、Webhook）
- 条件触发（阈值、规则命中、待办积压）

## 输出

- 新建 `Task`
- 触发 `Run`
- 节流/合并/延迟决策
- 触发失败或等待确认状态

## 契约要求

- 调度必须支持去重，避免告警风暴和重复任务爆炸
- 调度必须支持按风险等级和任务类型限流
- 调度必须支持批量聚合，避免高频低价值任务挤占资源
- 调度决策必须产生日志与 Decision 记录

## 失败与降级

- 事件洪峰：聚合、节流、批处理
- 预算不足：延迟调度或停止新建任务
- 下游执行不可用：保留待执行状态并输出告警

