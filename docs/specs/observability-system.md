---
title: "Observability & Evaluation 契约"
status: approved
created: 2026-04-07
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "../architecture/scaling-strategy.md"
  - "../reference/technical-metrics.md"
---

# Observability & Evaluation 契约

可观测性不再只被定义为日志和监控，而是平台级 `Observability & Evaluation` 模块。

## 覆盖范围

- 日志：结构化事件与审计记录
- Metrics：吞吐、延迟、成本、策略阻断、队列压力
- Trace：跨模块 run 链路追踪
- Replay：单次 Run 的可回放能力
- Evaluation：benchmark、regression、safety、load、cost 对比

## 必须回答的问题

- 当前 Task / Run 卡在哪个阶段
- 某次结果为何被允许、拒绝、降级或升级模型
- 当前成本为何上升，是否由缓存失效、模式切换或任务洪峰导致
- 新变更相对 baseline 是否真实提升能力，还是只增加成本

## 最小观测要求

- 每个 Run 都有事件流
- 每次策略裁决都有 Decision
- 每次成本变化都有 Cost Record
- 每条链路都能生成 replay 所需的最小数据

## 与评测的关系

- `Capability Benchmark`
- `Story Acceptance`
- `Regression Suite`
- `Load & Scale Test`
- `Safety Evaluation`
- `Cost / Latency Benchmark`

以上 6 类评测均属于本模块职责边界的一部分。

