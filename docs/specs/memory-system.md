---
title: "Memory & Retrieval 契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "../architecture/scaling-strategy.md"
  - "./core-data-contracts.md"
---

# Memory & Retrieval 契约

本文件定义平台级 `Memory & Retrieval` 模块，不再沿用“单个记忆系统实现”的叙事。

## 职责边界

负责：

- 当前 Run 的上下文装配
- 长期记忆与证据检索
- 压缩、去重、TTL、冷热分层
- 为 Planner 和 Execution Engine 提供检索结果

不负责：

- 决定任务目标
- 直接操作外部工具
- 代替 Observability 存储全部运行日志

## 设计原则

- 优先保留 Evidence，而不是保留未经验证的自由文本记忆
- 记忆与证据要能区分“事实”“推断”“习惯性规则”
- 检索必须兼容 10x / 100x 扩容，不依赖单索引无限增长

## 存储分层

- 短期上下文：服务单个 Run
- 工作记忆：服务单个 Task 的多轮 Run
- 长期记忆：服务跨 Task、跨仓库复用
- 冷归档：服务历史追溯与低频查询

## 检索策略

- 混合检索：关键词 + 结构化过滤 + 向量召回
- 重排依据：相关性、时效性、重要性、租户/仓库边界
- 预算约束：检索结果进入上下文前必须过预算裁剪

## 扩容要求

- 10x：独立索引层 + 热点缓存
- 100x：按仓库/团队/租户分片，冷热分层和异步归档

