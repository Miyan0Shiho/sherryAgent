# SherryAgent

> 基于 Claude Code 与 OpenClaw 两大 AI Agent 框架优势融合的 Python 多 Agent 框架

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## 快速开始

### 环境要求

- Python 3.12+
- uv（推荐）或 pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/sherry-agent.git
cd sherry-agent

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加 ANTHROPIC_API_KEY 或 OPENAI_API_KEY
```

### 运行

```bash
# 启动 CLI
uv run sherry-agent

# 运行测试
uv run pytest

# 类型检查
uv run mypy src/
```

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

## MVP 开发路线

| 阶段 | 目标 | 状态 |
|------|------|------|
| MVP-1 | 核心 Agent Loop | 📝 规划中 |
| MVP-2 | 记忆与持久化 | 📝 规划中 |
| MVP-3 | 自主运行 | 📝 规划中 |
| MVP-4 | 多 Agent 编排 | 📝 规划中 |
| MVP-5 | Skill 插件与生态 | 📝 规划中 |

详见 [docs/plans/mvp-roadmap.md](docs/plans/mvp-roadmap.md)。

## 文档

| 文档 | 说明 |
|------|------|
| [AGENTS.md](AGENTS.md) | AI Agent 入口指南 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 系统架构概述 |
| [docs/INDEX.md](docs/INDEX.md) | 完整文档索引 |

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
