---
title: "Scaling Strategy"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "./system-blueprint.md"
  - "./quality-vs-latency-vs-cost.md"
---

# Scaling Strategy

## 10x 规模

目标：支持更多团队、仓库和后台任务，但仍以单机多 worker 为主。

### 架构变化

- 任务队列从内存态迁移为持久化队列。
- evidence 与记忆拆出独立索引层。
- 增加热点缓存与批量触发聚合。
- 交互任务与后台任务至少在 worker 层隔离。

### 重点风险

- `queue_lag` 增长
- retrieval 延迟抖动
- token burn rate 失控
- 背景任务挤占交互式任务

## 100x 规模

目标：支持模块独立伸缩与跨仓库大规模分析。

### 架构变化

- Gateway、Planner、Execution Engine、Scheduler、Retrieval 独立伸缩。
- evidence 和长期记忆做冷热分层与异步归档。
- 检索索引按仓库、团队或租户维度分片。
- 优先级队列与资源配额成为必须能力。
- 审计、策略、成本统计独立出来，避免阻塞执行路径。

### 重点风险

- 单一索引写放大与查询退化
- 观测系统拖累执行路径
- 批量分析流量占满预算
- 多团队共享环境下策略漂移

## 必须观测的容量指标

- `tasks_per_min`
- `queue_lag`
- `concurrent_runs`
- `evidence_growth_rate`
- `retrieval_p95_ms`
- `token_burn_per_hour`
- `approval_wait_time`
- `policy_block_rate`

