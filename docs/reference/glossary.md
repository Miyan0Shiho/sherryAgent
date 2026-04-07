---
title: "术语表"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../specs/six-layer-architecture.md"
  - "../vision/north-star.md"
---

# 术语表

本术语表用于统一 SherryAgent 的叙事口径与系统契约。所有 Story 与 `.trae/specs` 中的关键概念应优先使用这里的术语。

## 核心概念

- **Story（场景包/面试故事）**：一个可演示的闭环能力包，必须包含演示脚本、输出契约、权限策略、失败降级与六层映射。
- **六层架构**：交互层、编排层、执行层、自主运行层、记忆层、基础设施层。
- **Agent Loop**：单 agent 的“推理-工具-观察”循环，以事件流方式输出过程可观察信息。
- **Orchestrator（编排器）**：把任务分解成子任务，管理依赖与执行策略（并行/串行/重试/汇总）。
- **Lane（并发通道）**：并发控制单元（session 串行 + global 并发），避免工具执行竞态与资源爆炸。
- **Fork（子 Agent 派生）**：从父 agent 派生子 agent，继承部分上下文与约束，执行子任务并回传结果。

## 自主运行与触发

- **Heartbeat（心跳引擎）**：后台 while-true 驱动循环，负责检查待办、触发任务、更新状态与资源监控。
- **Cron（定时调度）**：基于 APScheduler 的定时任务触发机制（cron/interval/date）。
- **条件触发（Condition Trigger）**：满足某条件（阈值、事件、状态变化）后启动任务的机制。

## 安全与合规

- **权限管道（6-Layer Permission Pipeline）**：工具声明式权限 -> 全局规则 -> 自动模式分类 -> 用户配置 -> 企业策略 -> 沙箱隔离。
- **审计日志（Audit Log）**：记录工具调用、权限决策、人工确认与关键状态变化，用于回放与追责。
- **风险等级（Risk Level）**：LOW / MEDIUM / HIGH / CRITICAL，用于决定自动放行、确认或拒绝策略。

## 记忆

- **短期记忆（STM）**：会话上下文管理与压缩策略（micro/auto/session/reactive）。
- **长期记忆（LTM）**：跨会话知识存储与检索（SQLite + FTS + 向量/混合检索）。
- **记忆桥接（Bridge）**：把会话洞察从 STM 提炼写入 LTM，并在新任务中检索注入。

## 工具与扩展

- **Tool（工具）**：可被 agent 调用的外部操作（文件、shell、http 等），必须走权限检查。
- **Skill（技能）**：以文档/插件形式封装的能力包（通常包含工具、提示与门控规则）。
- **MCP（Model Context Protocol）**：连接外部工具服务器的协议与客户端能力。

