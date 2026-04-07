# SherryAgent

> 基于 Claude Code 与 OpenClaw 两大 AI Agent 框架优势融合的 Python 多 Agent 框架，用于学习 Agent 开发、毕业项目和简历项目。

## Mode: docs-only (Egg)

本仓库当前处于 **docs-only** 阶段：实现代码已被“毁灭”以便重生。你不应尝试运行 CLI、测试、类型检查等命令。

## How To Work Here

### 1) 先读（入口）

1. `docs/INDEX.md`（Story Suite 入口）
2. `docs/vision/north-star.md`（北极星：成功指标与失败边界）
3. `docs/guides/spec-authority.md`（双权威与冲突裁决）

### 2) 再做（执行权威）

任何新增/修改都必须先落到 `.trae/specs/*`（spec/tasks/checklist），然后同步更新 `docs/*` 的契约与叙事口径。

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

### Spec Authority（必须遵守）

SherryAgent 采用 **`.trae/specs` + `docs/` 双权威**：

- **`.trae/specs/*`：开发执行权威**（做什么、验收是什么、任务如何拆分）
- **`docs/*`：系统契约与叙事权威**（长期结构、术语、安全原则、Story 口径）
- **OpenSpec：方法论参考**（文档写法/模板参考，不作为项目权威规范来源）

冲突裁决写在：[docs/guides/spec-authority.md](docs/guides/spec-authority.md)

### Definition of Done（文档版）

任何非 trivial 变更（新增 Story、修改系统契约、安全策略、流程）完成时，至少满足：

- `.trae/specs`：对应 spec/tasks/checklist 已更新
- `docs/`：相关 Story/契约文档已更新且术语一致
- `docs/INDEX.md`：能导航到新增/修改的入口

### Phoenix 开发顺序（Story 驱动）

以 5 个 Story 为计划主轴，统一由 `.trae/specs/story-*/` 驱动。

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

## 推荐阅读路径（先故事，后契约）

1. [docs/vision/north-star.md](docs/vision/north-star.md)
2. [docs/INDEX.md](docs/INDEX.md) 的 Story Suite（5 个故事）
3. [docs/reference/glossary.md](docs/reference/glossary.md)
4. [docs/specs/six-layer-architecture.md](docs/specs/six-layer-architecture.md)

| 目录 | 内容 |
|------|------|
| [docs/standard/](docs/standard/) | 核心原则与标准 |
| [docs/specs/](docs/specs/) | 技术规范 |
| [docs/reference/](docs/reference/) | API 与配置参考 |
| [docs/plans/](docs/plans/) | 实施计划 |
| [docs/research/](docs/research/) | 研究分析 |
