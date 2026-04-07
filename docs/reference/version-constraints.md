---
title: "版本约束"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "./tech-stack.md"
---

# 版本约束

本文档记录未来恢复实现时的目标版本约束，不代表当前仓库已经具备这些依赖。

## 核心依赖

| 依赖 | 目标版本 | 用途 |
|------|------|------|
| Python | >= 3.12 | 异步并发、类型能力、TaskGroup |
| anthropic | >= 0.40 | 主模型 SDK |
| openai | >= 1.50 | 主模型 SDK |
| textual | >= 3.0 | CLI 交互入口 |
| aiosqlite | >= 0.20 | 轻量状态存储 |
| sqlite-vec | >= 0.1 | 早期向量索引 |
| APScheduler | >= 3.10 | 调度与触发 |
| pydantic | >= 2.10 | 数据模型与校验 |
| pydantic-settings | >= 2.6 | 分层配置 |
| structlog | >= 24.0 | 结构化日志与审计 |
| fastapi | >= 0.115 | API / Webhook |
| websockets | >= 13.0 | 状态推送 |
| click | >= 8.1 | 命令行参数层 |

## 开发与验证依赖

| 依赖 | 目标版本 | 用途 |
|------|------|------|
| pytest | >= 8.0 | 测试框架 |
| pytest-asyncio | >= 0.24 | 异步测试 |
| pytest-cov | >= 5.0 | 覆盖率 |
| ruff | >= 0.6 | 静态检查 |
| mypy | >= 1.11 | 类型检查 |

## 说明

- 版本约束服务当前蓝图，不再附带旧实现期的完整 `pyproject` 样例。
- 一旦进入恢复实现阶段，实际版本应由 `.trae/specs/platform-foundation/` 与 `.trae/specs/release-program/` 共同约束。

