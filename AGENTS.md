# SherryAgent

> 基于 Claude Code 与 OpenClaw 两大 AI Agent 框架优势融合的 Python 多 Agent 框架，用于学习 Agent 开发、毕业项目和简历项目。

## Build & Development

```bash
# 安装依赖
uv sync

# 运行 CLI
uv run sherry-agent

# 运行测试
uv run pytest

# 类型检查
uv run mypy src/

# 代码检查
uv run ruff check src/
```

## Stack

| 类别 | 技术选型 |
|------|----------|
| 语言 | Python 3.12+ |
| 异步框架 | asyncio |
| CLI | Textual + click |
| LLM | anthropic / openai SDK |
| 数据库 | aiosqlite + sqlite-vec |
| 调度 | APScheduler |
| 配置 | pydantic-settings + TOML |
| 日志 | structlog |
| 插件 | pluggy |
| 测试 | pytest + pytest-asyncio |

## Architecture

SherryAgent 采用六层融合架构：

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

详见 [ARCHITECTURE.md](ARCHITECTURE.md) 和 [docs/specs/six-layer-architecture.md](docs/specs/six-layer-architecture.md)。

## Conventions

- 命名规范：[docs/standard/naming-conventions.md](docs/standard/naming-conventions.md)
- 编码标准：[docs/standard/coding-standards.md](docs/standard/coding-standards.md)
- 设计原则：[docs/standard/design-principles.md](docs/standard/design-principles.md)

## Working Rules

### MVP 开发顺序

1. **MVP-1**: 核心Agent Loop（2周）
2. **MVP-2**: 记忆与持久化（3周）
3. **MVP-3**: 自主运行（2周）
4. **MVP-4**: 多Agent编排（3周）
5. **MVP-5**: Skill插件与生态（2周）

详见 [docs/plans/mvp-roadmap.md](docs/plans/mvp-roadmap.md)。

### 安全红线

- 禁止执行 `rm -rf /`、`DROP TABLE` 等破坏性命令
- 禁止硬编码密钥、密码、Token
- 禁止在日志中输出敏感信息
- 所有工具调用必须经过权限检查

## Known Pitfalls

- **asyncio 陷阱**：避免在异步函数中使用阻塞操作，使用 `asyncio.to_thread()` 包装同步调用
- **Token 消耗失控**：OpenClaw 的心跳循环可能导致 Token 消耗"滚雪球"式增长，需要设置预算上限
- **权限过于严格**：六层权限管道可能影响自动化效率，需要根据场景调整权限模式
- **记忆检索冗余**：全量检索可能注入冗余信息，需要结合压缩策略控制上下文

## 文档索引

完整文档索引见 [docs/INDEX.md](docs/INDEX.md)。

| 目录 | 内容 |
|------|------|
| [docs/standard/](docs/standard/) | 核心原则与标准 |
| [docs/specs/](docs/specs/) | 技术规范 |
| [docs/reference/](docs/reference/) | API 与配置参考 |
| [docs/plans/](docs/plans/) | 实施计划 |
| [docs/research/](docs/research/) | 研究分析 |
