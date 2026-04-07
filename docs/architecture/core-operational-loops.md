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
- 流程：`request normalize -> planner -> subtask plan -> execution -> tool/policy gate -> review -> result pack`
- 输出：结构化结果、变更建议、审计记录、成本摘要
- 目标：质量最高，允许更高延迟和 token
- 失败降级：预算耗尽时输出 progress report；工具失败时转为只读诊断

## 2. Autonomous Background Loop

- 入口：cron / event / condition
- 流程：`trigger -> policy precheck -> budget allocation -> execution -> evidence collection -> report -> human escalation if needed`
- 输出：报告、行动项、风险分级、必要确认请求
- 目标：严格预算、强审计、默认只读/低风险
- 失败降级：触发限流、批处理聚合、超过预算时硬停止

## 3. Bulk Research / Analysis Loop

- 入口：批量任务、数据集、仓库集合
- 流程：`batch ingestion -> queue -> shard execution -> aggregation -> confidence scoring -> report`
- 输出：可追溯证据报告、统计结论、低置信项
- 目标：成本可控、吞吐优先、支持异步聚合
- 失败降级：采样、分段执行、低置信标记、延迟汇总

## 4. Repo / Release Governance Loop

- 入口：PR、push、release candidate、deployment event
- 流程：`trigger -> policy gate -> scan -> evaluation -> decision -> rollout / block / rollback`
- 输出：门禁结论、失败原因、风险建议、回滚记录
- 目标：强一致、强可回放、宁慢勿错放
- 失败降级：门禁失败时只输出阻塞项，不自动推进

## 通用状态机

所有主链路都必须遵守统一运行阶段：

`created -> planned -> running -> waiting_confirmation -> completed | blocked | failed | cancelled`

每次状态变化都必须产生审计与可观察事件。

