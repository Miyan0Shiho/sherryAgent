---
title: "技术栈总览"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "./version-constraints.md"
  - "./project-structure.md"
  - "../architecture/module-map.md"
---

# 技术栈总览

本文档描述的是 **未来实现阶段的目标技术栈口径**，服务当前公司级蓝图，而不是对已存在实现的描述。

## 平台核心技术

| 能力域 | 推荐方案 | 说明 |
|------|------|------|
| 语言运行时 | Python 3.12+ | 统一异步模型与类型能力 |
| 并发模型 | asyncio | 适合 I/O 密集和流式任务 |
| CLI 入口 | Textual + click | 交互入口之一 |
| HTTP / Webhook | FastAPI | API 与事件入口 |
| 实时通信 | websockets | 状态推送和异步反馈 |
| LLM 接入 | anthropic / openai SDK | 主模型接入层 |
| 本地模型 | Ollama 或同类本地 provider | 小模型、成本控制、对比实验 |
| 关系与轻量状态存储 | SQLite / aiosqlite | 早期单机阶段 |
| 检索与索引 | SQLite FTS + 向量索引 | 早期混合检索形态 |
| 调度 | APScheduler | cron / interval / date 触发 |
| 配置 | pydantic-settings + TOML | 分层配置与校验 |
| 结构化日志 | structlog | 日志、上下文、审计字段统一 |

## 模块对应关系

| 模块 | 主要技术依赖 |
|------|------|
| Gateway | Textual, click, FastAPI, websockets |
| Task Service | SQLite, pydantic, structlog |
| Planner | LLM SDK, pydantic, retrieval API |
| Execution Engine | asyncio, LLM SDK, tool runtime |
| Memory & Retrieval | SQLite, FTS, vector index |
| Policy & Guardrail | 配置规则、审计日志、沙箱策略 |
| Scheduler & Trigger | APScheduler, event adapters |
| Observability & Evaluation | structlog, metrics, benchmark artifacts |
| Cost & Capacity Controller | cost accounting, cache, rate limiting |
| Release & Ops | 配置管理、告警、回滚 runbook |

## 技术选型原则

- 早期优先单机、同进程、低运维复杂度。
- 边界按未来拆分服务设计，但不在一开始引入过多分布式复杂度。
- 模型能力不足优先通过流程、检索、缓存、评测和策略补齐，不默认通过换更大模型解决。

