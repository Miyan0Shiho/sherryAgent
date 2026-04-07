---
title: "Planner 与编排契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "../architecture/core-operational-loops.md"
  - "./core-data-contracts.md"
---

# Planner 与编排契约

多 Agent 编排现在被视为 `Planner + Execution Engine` 的联合能力，而不是孤立的“并行 demo 能力”。

## Planner 的核心职责

- 识别任务类型与运行模式
- 任务拆解与子任务编排
- 模型路由、工具路由、预算分配
- 决定何时并行、何时串行、何时等待确认

## 编排原则

- 默认优先保证正确性，而不是最大并发
- 读操作可并发，写操作与高风险动作需串行或确认
- 子任务拆解必须以输出契约为中心，而不是只按文件或模块机械拆分

## 适用场景

- Interactive Dev：按澄清、设计、实现、review 拆解
- Background Ops：按证据收集、归因、建议、确认动作拆解
- Bulk Analysis：按分片、聚合、抽样、置信度计算拆解
- Release Governance：按扫描、门禁、决策、回滚准备拆解

## 不再主推的旧口径

- Worktree / Fork / Teammate 不是当前主蓝图的一级模块
- 它们最多是未来 Execution Engine 的实现策略，而不是当前系统边界

