---
title: "技术栈总览"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["version-constraints.md", "project-structure.md"]
---

# 技术栈总览

## 技术选型

| 模块 | 推荐方案 | 备选方案 | 选择理由 |
|------|---------|---------|---------|
| 异步框架 | asyncio (stdlib) | - | Python原生，零依赖，与3.12+特性深度集成 |
| CLI框架 | Textual + click | Rich + Prompt Toolkit | Textual支持完整TUI（面板、布局、实时刷新），click处理命令行参数 |
| LLM调用 | anthropic + openai SDK | litellm | 原生SDK提供完整的类型注解和流式支持，避免抽象层带来的类型丢失 |
| 数据库 | aiosqlite + sqlite-vec | DuckDB | SQLite零配置、单文件部署，FTS5全文检索成熟，sqlite-vec支持向量索引 |
| Embedding | sentence-transformers | OpenAI API | 本地推理零成本，支持多语言，all-MiniLM-L6-v2模型体积小速度快 |
| 任务调度 | APScheduler | 自研 | 成熟稳定的调度库，支持Cron表达式、间隔调度、日期调度，异步友好 |
| 配置管理 | pydantic-settings + TOML | dynaconf | Pydantic提供类型安全的配置验证，TOML是Python生态标准配置格式 |
| 日志 | structlog | loguru | 结构化JSON日志，支持上下文绑定、处理器链，便于日志采集和分析 |
| 插件系统 | pluggy | stevedore | pytest同款插件框架，轻量、文档完善、hook规范清晰 |
| WebSocket | fastapi + websockets | aiohttp | FastAPI自动生成OpenAPI文档，websockets库性能优异，生态完善 |
| 测试 | pytest + pytest-asyncio | - | Python测试事实标准，pytest-asyncio提供完善的异步测试支持 |
| 依赖管理 | uv + pyproject.toml | poetry | uv比poetry快10-100倍，pyproject.toml是PEP标准格式 |

## 架构分层技术栈

| 层级 | 技术选型 |
|------|----------|
| 交互层 | Textual (TUI) + FastAPI (HTTP) + websockets (实时推送) |
| 编排层 | asyncio.TaskGroup + pluggy (插件hook) |
| 执行层 | asyncio (异步生成器) + anthropic/openai SDK |
| 自主运行层 | APScheduler + asyncio (心跳循环) |
| 记忆层 | aiosqlite + sqlite-vec + sentence-transformers |
| 基础设施层 | pydantic-settings + structlog + pluggy |

## 设计考量

### 为什么选择 asyncio 而非多线程？

- LLM API 调用是 I/O 密集型，asyncio 天然适合
- 避免多线程的 GIL 限制和锁复杂性
- Python 3.12+ 的 TaskGroup 提供了更优雅的并发控制
- 流式响应需要异步生成器支持

### 为什么选择 SQLite 而非 PostgreSQL？

- 零配置、单文件部署，降低用户使用门槛
- 本地优先原则，不依赖外部服务
- FTS5 全文检索成熟稳定
- sqlite-vec 扩展支持向量索引
- 可选支持迁移到 PostgreSQL

### 为什么选择 Textual 而非 Rich？

- Textual 支持完整的 TUI 应用（面板、布局、事件循环）
- Rich 仅支持富文本输出，无法构建交互式界面
- Textual 基于 Rich，继承其渲染能力
- 支持响应式布局和 CSS 样式
