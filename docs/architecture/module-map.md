---
title: "Module Map"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "./system-blueprint.md"
  - "../specs/core-data-contracts.md"
---

# Module Map

## 强边界模块

### Gateway

- 输入：CLI、API、Webhook、cron、event
- 责任：请求标准化、鉴权、请求 ID、入口日志
- 不负责：任务拆解、预算决策、工具调用

### Task Service

- 输入：标准化请求与调度触发
- 责任：任务状态机、幂等键、优先级、依赖、run 建立
- 不负责：LLM 规划或工具执行

### Planner

- 输入：Task、上下文、策略、预算档位
- 责任：选择运行模式、任务拆解、模型路由、工具路由、预算分配
- 不负责：直接执行副作用动作

### Execution Engine

- 输入：已规划的子任务与执行上下文
- 责任：agent loop、超时、取消、重试、中断恢复、结果聚合
- 不负责：最终权限裁决

### Memory & Retrieval

- 输入：Task 上下文、运行历史、知识文档、证据
- 责任：短期上下文、长期记忆、检索、压缩、TTL、冷热分层
- 不负责：外部工具调用

### Policy & Guardrail

- 输入：工具调用请求、风险信息、用户/团队策略
- 责任：风险分级、确认流、审计策略、沙箱要求、拒绝原因
- 不负责：业务规划

### Scheduler & Trigger

- 输入：计划任务、事件源、规则、健康检查
- 责任：触发、去重、节流、批处理调度
- 不负责：直接操作任务业务逻辑

### Observability & Evaluation

- 输入：run 事件、指标、日志、trace、回放数据、benchmark 结果
- 责任：run replay、评测、回归、异常定位、质量看板
- 不负责：改写执行路径

### Cost & Capacity Controller

- 输入：成本统计、队列深度、缓存命中、配额、SLA
- 责任：预算、限流、并发控制、缓存、降级、fallback
- 不负责：决定任务业务目标

### Release & Ops

- 输入：构建结果、门禁结果、事故信息、配置变更
- 责任：发布、回滚、值班、变更审计、runbook 维护
- 不负责：模型推理本身

## 初期实现建议

- Phase 1 可以单进程，但模块边界、数据对象、日志字段必须按未来可拆分的方式定义。
- 最早需要拆开的模块是：Task Service、Execution Engine、Memory & Retrieval、Observability & Evaluation。

