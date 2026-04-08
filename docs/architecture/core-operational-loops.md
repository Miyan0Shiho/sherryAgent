---
title: "Core Operational Loops"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "./runtime-modes.md"
  - "../specs/core-data-contracts.md"
---

# Core Operational Loops

## 1. Interactive Dev Loop

- 入口：CLI / API
- 触发条件：显式开发请求、设计评审请求、代码变更请求
- 流程：`request normalize -> planner -> subtask plan -> execution -> tool/policy gate -> review -> result pack`
- 输出：结构化结果、变更建议、审计记录、成本摘要
- 可观察字段：`plan_version`, `model_profile`, `toolset`, `blocked_reason`, `review_outcome`
- 目标：质量最高，允许更高延迟和 token
- 失败降级：预算耗尽时输出 progress report；工具失败时转为只读诊断

## 2. Autonomous Background Loop

- 入口：cron / event / condition
- 触发条件：计划任务、条件命中、外部事件
- 流程：`trigger -> policy precheck -> budget allocation -> execution -> evidence collection -> report -> human escalation if needed`
- 输出：报告、行动项、风险分级、必要确认请求
- 可观察字段：`trigger_source`, `budget_profile`, `approval_wait_time`, `policy_block_rate`
- 目标：严格预算、强审计、默认只读/低风险
- 失败降级：触发限流、批处理聚合、超过预算时硬停止

## 3. Bulk Research / Analysis Loop

- 入口：批量任务、数据集、仓库集合
- 触发条件：批量输入到达、数据集更新、调研批次提交
- 流程：`batch ingestion -> queue -> shard execution -> aggregation -> confidence scoring -> report`
- 输出：可追溯证据报告、统计结论、低置信项
- 可观察字段：`batch_size`, `shard_count`, `aggregation_latency_ms`, `low_confidence_rate`
- 目标：成本可控、吞吐优先、支持异步聚合
- 失败降级：采样、分段执行、低置信标记、延迟汇总

## 4. Repo / Release Governance Loop

- 入口：PR、push、release candidate、deployment event
- 触发条件：治理扫描请求、发布候选、合并前检查、部署前后事件
- 流程：`trigger -> policy gate -> scan -> evaluation -> decision -> rollout / block / rollback`
- 输出：门禁结论、失败原因、风险建议、回滚记录
- 可观察字段：`gate_result`, `required_checks`, `rollback_plan`, `release_risk_level`
- 目标：强一致、强可回放、宁慢勿错放
- 失败降级：门禁失败时只输出阻塞项，不自动推进

## 通用状态机

所有主链路都必须遵守统一运行阶段：

`created -> planned -> running -> waiting_confirmation -> completed | blocked | failed | cancelled`

每次状态变化都必须产生审计与可观察事件。

## 角色边界

- `Planner`：负责模式选择、任务拆解、预算分配、模型和工具路由；不直接执行工具。
- `Execution Engine`：负责执行计划、收集 Evidence、生成 Decision、形成结果包；不决定是否触发任务。
- `Scheduler & Trigger`：负责定时、事件、条件触发、去重和恢复；不替代 Planner 做复杂任务拆解。
- `Policy Gate`：负责权限、风险、确认、阻断与降级裁决。
- `Review`：负责对结果包进行质量校验、缺口暴露和最终可交付性判断。

## 失败与恢复规则

- `waiting_confirmation`：证据、计划和风险判断都已具备，但必须等待人工授权。
- `blocked`：缺少继续前提，或恢复不安全，或关键输入不可回放。
- `failed`：执行过程本身失败，当前 run 已终止。
- 工具失败优先降级到只读诊断；预算超限优先停止扩张而不是跳过审计。
- 模式切换、模型升级、计划重试都必须形成 `Decision`。
- 中断恢复必须基于最近可回放 `Run` 上下文；否则进入 `blocked`。
