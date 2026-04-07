---
title: "六层能力视角"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/system-blueprint.md"
  - "../architecture/module-map.md"
---

# 六层能力视角

六层架构现在作为 **能力视角** 保留，用于解释 SherryAgent 的技术来源与能力覆盖，不再直接等同于实现计划中的模块划分。

## 六层定义

| 层级 | 能力意义 | 对应当前模块 |
|------|---------|---------|
| 交互层 | 多入口接入与用户反馈 | Gateway |
| 编排层 | 任务拆解、模式选择、协同组织 | Planner |
| 执行层 | 单次 Run 的执行循环与工具调用 | Execution Engine |
| 自主运行层 | 调度、触发、批处理、恢复 | Scheduler & Trigger |
| 记忆层 | 上下文压缩、长期记忆、检索 | Memory & Retrieval |
| 基础设施层 | 权限、观测、成本、发布治理等底座 | Policy、Observability、Cost、Release |

## 当前定位

- 六层架构用于解释“能力从哪里来”
- 模块蓝图用于解释“系统怎么拆”
- 实现计划用于解释“项目怎么推进”

三者不能互相替代。

