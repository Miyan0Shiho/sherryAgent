# SherryAgent

> 基于 Claude Code 与 OpenClaw 两大 AI Agent 框架优势融合的 Python 多 Agent 框架

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 状态：**docs-only（Egg）**。本仓库当前不提供可运行实现代码，目标是先把系统蒸馏为可落地的规范与故事套件，再进入下一阶段重生。

## 项目简介

SherryAgent 是一个用于学习 Agent 开发的 Python 多 Agent 框架，融合了 Claude Code 的**编排精度**和 OpenClaw 的**自主运行能力**。

### 核心特性

- 🔄 **Agent Loop** - 流式执行循环，支持工具调用和上下文压缩
- 🧠 **记忆系统** - 四层压缩策略 + 三层长期记忆
- 💾 **任务持久化** - 断点续传，崩溃恢复
- ⚡ **自主运行** - 心跳引擎 + Cron 调度
- 🤝 **多Agent编排** - 任务分解 + 并行执行
- 🔐 **权限系统** - 六层纵深防御
- 🔌 **插件生态** - Skill 热加载 + MCP 协议

## 从哪里开始读（面试/叙事优先）

1. [docs/INDEX.md](docs/INDEX.md) 的 “Story Suite”（5 个官方场景包）
2. [docs/vision/north-star.md](docs/vision/north-star.md)（融合愿景、成功指标、失败边界）
3. [docs/guides/spec-authority.md](docs/guides/spec-authority.md)（`.trae + docs` 双权威与冲突裁决）
4. [AGENTS.md](AGENTS.md)（后续 Agent 的工作规则）

## 开发入口（执行权威）

开发执行以 `.trae/specs` 为权威来源：它定义“做什么、验收是什么、任务如何拆分”。

推荐从 `.trae/specs/phoenix-roadmap/` 与 `.trae/specs/story-01..05/` 开始。

## 架构概览

```
交互层 (CLI/WebSocket/HTTP)
    ↓
编排层 (Orchestrator/Agent Teams)
    ↓
执行层 (Agent Loop/Fork/Lane Queue)
    ↓
自主运行层 (Heartbeat/Cron/Recovery)
    ↓
记忆层 (Short-term/Long-term/Bridge)
    ↓
基础设施层 (Permissions/Sandbox/MCP/Skills)
```

详见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## Phoenix Roadmap

docs-only 重生路线（Egg -> Chick -> Phoenix）见：
- [docs/plans/phoenix-roadmap.md](docs/plans/phoenix-roadmap.md)

## 文档

| 文档 | 说明 |
|------|------|
| [AGENTS.md](AGENTS.md) | AI Agent 入口指南 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 系统架构概述 |
| [docs/INDEX.md](docs/INDEX.md) | 完整文档索引 |

**面试与演示入口**：从 [docs/INDEX.md](docs/INDEX.md) 的 “Story Suite” 开始（5 个官方场景包）。

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.12+ |
| 异步框架 | asyncio |
| CLI | Textual + click |
| LLM | anthropic / openai SDK |
| 数据库 | aiosqlite + sqlite-vec |
| 调度 | APScheduler |
| 配置 | pydantic-settings |
| 日志 | structlog |
| 插件 | pluggy |
| 测试 | pytest + pytest-asyncio |

## 贡献指南

本项目主要用于学习 Agent 开发，欢迎提交 Issue 和 Pull Request。

## 许可证

[MIT License](LICENSE)

## 致谢

本项目设计参考了以下优秀框架：

- [Claude Code](https://www.anthropic.com/claude-code) - Anthropic 的终端原生 AI 编程助手
- [OpenClaw](https://github.com/openclaw/openclaw) - 开源本地优先的 AI Agent 框架
