---
title: "数据流契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/system-blueprint.md"
  - "../architecture/core-operational-loops.md"
  - "./core-data-contracts.md"
---

# 数据流契约

本文件定义平台级数据流，不再描述旧实现中的局部模块调用关系。

## 平台主数据流

```mermaid
sequenceDiagram
    participant SRC as Source
    participant GW as Gateway
    participant TS as Task Service
    participant PL as Planner
    participant EX as Execution Engine
    participant PG as Policy & Guardrail
    participant MR as Memory & Retrieval
    participant OE as Observability & Evaluation
    participant CC as Cost & Capacity Controller

    SRC->>GW: request / event / cron / webhook
    GW->>TS: create Task
    TS->>PL: plan request
    PL->>CC: allocate budget/mode
    PL->>MR: retrieve context
    PL->>EX: create Run + execution plan
    EX->>PG: tool / action request
    PG-->>EX: allow / deny / require_confirmation
    EX->>MR: read/write evidence & memory
    EX->>OE: emit events / metrics / replay data
    EX->>CC: report cost / latency
    EX-->>TS: outcome + status update
    TS-->>GW: final result / blocked state
```

## 核心对象流转

- `Gateway` 创建或标准化请求
- `Task Service` 维护 `Task`
- `Planner` 生成 `Run` 计划并路由模式
- `Execution Engine` 产出 `Evidence / Decision / Cost Record`
- `Observability & Evaluation` 消费运行事件并形成回放与指标

## 关键约束

- 任一链路都必须可追踪到 `Task -> Run -> Evidence -> Decision -> Cost Record`
- 数据流中不能出现“只在日志里存在、没有对象归属”的关键决策
- 后台与批量任务必须经过与交互任务相同的数据对象体系，只是模式和预算不同

