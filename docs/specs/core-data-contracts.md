---
title: "Core Data Contracts"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../architecture/core-operational-loops.md"
  - "../architecture/system-blueprint.md"
---

# Core Data Contracts

## Task

必填字段：

- `task_id`
- `source`
- `goal`
- `priority`
- `risk_level`
- `budget_profile`
- `mode`
- `status`

说明：
- `source` 表示入口来源，例如 `cli`, `api`, `cron`, `event`, `webhook`
- `mode` 只能取运行模式定义中的值

## Run

必填字段：

- `run_id`
- `task_id`
- `plan_version`
- `model_profile`
- `toolset`
- `started_at`
- `ended_at`
- `outcome`

说明：
- 一个 Task 可以有多个 Run
- `plan_version` 必须能追溯到使用的规格文档版本

## Evidence

必填字段：

- `evidence_id`
- `run_id`
- `source_type`
- `source_ref`
- `summary`
- `confidence`

说明：
- `source_ref` 必须可定位到日志、文件、API 响应、命令结果或外部引用
- 任何关键结论都必须至少关联一条 Evidence

## Decision

必填字段：

- `decision_id`
- `run_id`
- `decision_type`
- `policy_basis`
- `requires_human`
- `approved_by`

说明：
- 所有权限拦截、自动放行、降级、模型升级、预算调整都必须形成 Decision

## Cost Record

必填字段：

- `run_id`
- `token_in`
- `token_out`
- `tool_calls`
- `latency_ms`
- `cache_hit`
- `estimated_cost`

说明：
- 成本记录必须支持汇总到任务、仓库、团队、运行模式四个维度

