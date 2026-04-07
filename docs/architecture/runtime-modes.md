---
title: "Runtime Modes"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "./quality-vs-latency-vs-cost.md"
  - "./core-operational-loops.md"
---

# Runtime Modes

## 1. `interactive-dev`

- 面向：交互式开发、设计、review、repo 操作
- 优先级：质量 > 安全 > 延迟 > 成本
- 默认策略：更多规划、更多审查、更多结构化输出
- 典型风险：高风险写操作、误改配置、发布前误判

## 2. `autonomous-safe`

- 面向：重复事务、定期报告、轻量后台任务
- 优先级：安全 > 成本 > 质量 > 延迟
- 默认策略：只读优先、写入最小化、预算严格、审计完整
- 典型风险：频繁触发导致成本滚雪球、条件判断漂移

## 3. `background-ops`

- 面向：巡检、告警响应、证据收集、事故分诊
- 优先级：安全 > 质量 > 成本 > 延迟
- 默认策略：证据先行、修复后置、高风险动作必须确认
- 典型风险：告警风暴、误触发修复、敏感信息泄露

## 4. `bulk-analysis`

- 面向：批量调研、仓库扫描、数据集分析、长跑任务
- 优先级：成本 > 吞吐 > 质量 > 实时性
- 默认策略：分片执行、异步聚合、缓存与采样、低置信标记
- 典型风险：批量任务挤占交互资源、证据膨胀、检索退化

## 模式切换规则

- 运行模式由 `Planner` 基于 `task.goal`, `risk_level`, `source`, `budget_profile` 决定。
- 模式切换必须记录在 `Run.model_profile` 和 `Decision.policy_basis` 中。
- 没有显式模式时，默认：
  - 交互任务 -> `interactive-dev`
  - cron/事件任务 -> `autonomous-safe`
  - 告警与事故 -> `background-ops`
  - 批量数据/仓库集合 -> `bulk-analysis`

