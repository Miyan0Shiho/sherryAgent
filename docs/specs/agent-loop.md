---
title: "Agent Loop 契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "../architecture/core-operational-loops.md"
  - "./core-data-contracts.md"
---

# Agent Loop 契约

Agent Loop 不再被定义为“孤立的代码模块实现”，而被定义为 **Execution Engine** 的核心运行单元。

## 定位

- 所属模块：`Execution Engine`
- 上游输入：`Planner` 生成的执行计划、预算档位、模式、工具集合、策略上下文
- 下游输出：事件流、Evidence、Decision、Cost Record、结构化结果

## 职责边界

Agent Loop 负责：

- 驱动单次 Run 的推理与工具执行循环
- 管理轮次、预算、取消、超时和中断恢复
- 产出可回放的事件流
- 把关键结论沉淀为 Evidence，把关键裁决沉淀为 Decision

Agent Loop 不负责：

- 决定系统总目标
- 直接维护任务生命周期主状态
- 越过 Policy & Guardrail 独立执行高风险动作

## 最小输入契约

- `task_id`
- `run_id`
- `mode`
- `budget_profile`
- `model_profile`
- `toolset`
- `policy_context`
- `execution_plan`

## 最小输出契约

- `outcome`
- `events`
- `evidence[]`
- `decisions[]`
- `cost_record`
- `blocked_reason`（如有）

## 运行约束

- 任何工具调用都必须先经过 `Policy & Guardrail`
- 任何模式切换都必须记录到 `Decision`
- 任何预算触顶都必须停止继续扩张执行深度
- 任何不可恢复失败都必须保留可复盘事件和证据

## 与主链路的关系

- `Interactive Dev Loop`：强调结构化输出与高质量 review
- `Autonomous Background Loop`：强调预算硬边界与审计
- `Bulk Research / Analysis Loop`：强调分片执行与异步聚合
- `Repo / Release Governance Loop`：强调证据先行与门禁一致性

