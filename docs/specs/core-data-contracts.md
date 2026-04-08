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
- `idempotency_key`
- `source`
- `goal`
- `priority`
- `risk_level`
- `budget_profile`
- `mode`
- `status`
- `created_at`
- `updated_at`

说明：
- `source` 表示入口来源，例如 `cli`, `api`, `cron`, `event`, `webhook`
- `mode` 只能取运行模式定义中的值
- `idempotency_key` 用于去重同一入口触发的重复任务
- 最小索引：`task_id`, `idempotency_key`, `status`, `priority`, `created_at`

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
- `status`

说明：
- 一个 Task 可以有多个 Run
- `plan_version` 必须能追溯到使用的规格文档版本
- `status` 必须复用统一状态机，不允许定义私有 run 状态
- 最小索引：`run_id`, `task_id`, `status`, `started_at`

## Evidence

必填字段：

- `evidence_id`
- `run_id`
- `source_type`
- `source_ref`
- `summary`
- `confidence`
- `captured_at`

说明：
- `source_ref` 必须可定位到日志、文件、API 响应、命令结果或外部引用
- 任何关键结论都必须至少关联一条 Evidence
- `confidence` 必须使用 `high | medium | low` 离散值或等价映射，避免自由发挥
- 最小索引：`evidence_id`, `run_id`, `source_type`, `captured_at`

## Decision

必填字段：

- `decision_id`
- `run_id`
- `decision_type`
- `policy_basis`
- `requires_human`
- `approved_by`
- `created_at`

说明：
- 所有权限拦截、自动放行、降级、模型升级、预算调整都必须形成 Decision
- 任何导致状态变化、预算变化、模型切换、权限结论的动作都不得省略 Decision
- 最小索引：`decision_id`, `run_id`, `decision_type`, `created_at`

## Cost Record

必填字段：

- `run_id`
- `token_in`
- `token_out`
- `tool_calls`
- `latency_ms`
- `cache_hit`
- `estimated_cost`
- `recorded_at`

说明：
- 成本记录必须支持汇总到任务、仓库、团队、运行模式四个维度
- 最小索引：`run_id`, `recorded_at`

## 对象关系

- 一个 `Task` 可以拥有多个 `Run`
- 一个 `Run` 可以拥有多条 `Evidence`
- 一个 `Run` 可以拥有多条 `Decision`
- 一个 `Run` 至少要有一条终态 `Cost Record`
- 任何正式输出都必须可回链到 `Task -> Run -> Evidence -> Decision -> Cost Record`

## 统一状态机

- `created`：任务已建立，但尚未完成计划
- `planned`：已形成可执行计划和运行路由
- `running`：正在执行
- `waiting_confirmation`：等待人工确认，禁止自动越过
- `completed`：成功完成
- `blocked`：由于缺证据、缺权限、缺前置条件或恢复不安全而停止
- `failed`：执行本身失败且当前 run 不能继续
- `cancelled`：被显式取消

## 恢复最小上下文

要恢复一个 `Run`，至少必须存在：

- `Task` 基本字段和当前状态
- 最近一次 `Run` 的 `plan_version`
- 尚未消费完的 `Decision`
- 已采集 `Evidence` 的可定位引用
- 最近一条 `Cost Record`

缺失任一项时，恢复过程必须进入 `blocked`，而不是假定可继续执行。

## 配置分层

- `local`：单人环境，默认最保守的外部写入边界，强调可恢复性和显式确认
- `team`：团队共享环境，要求统一审计、配额和仓库边界
- `prod`：生产或高风险环境，要求强审计、强确认、强回滚与更严格的默认阻断

不同配置层只能收紧默认权限和预算，不能绕过统一状态机或审计字段。

## 生命周期与冷热分层

- `Task` / `Run`：热数据，服务当前执行和近期恢复
- `Evidence`：先热后冷；热层服务当前检索，冷层服务回放和审计
- `Decision`：默认长期保留，优先服务归责和策略复盘
- `Cost Record`：热层服务预算控制，冷层服务趋势分析和容量规划
