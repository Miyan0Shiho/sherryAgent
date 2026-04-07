# SherryAgent

> 基于 Claude Code 与 OpenClaw 两类 Agent 优势融合的 docs-only 项目蓝图，目标是把 SherryAgent 规划成一个可落地、可扩展、可运营的公司级 Hybrid Platform，而不是 demo。

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 状态：**docs-only / planning-first**。当前仓库不提供可运行实现，主目标是先把产品蓝图、系统契约、实现计划、质量与运营策略定稿。

## 项目定位

SherryAgent 的产品定位是 **Hybrid Platform**：

- 面向严谨开发协作：需求澄清、设计、实现、review、repo 治理、发布门禁。
- 面向长期自主执行：后台巡检、条件触发、批量研究、安全审计、报告生成。
- 面向小团队、多仓库、多任务并发：默认优先质量与安全，再通过模式切换控制延迟与成本。

## 阅读入口

如果你要理解项目全貌，先读这些：

1. [docs/vision/product-charter.md](docs/vision/product-charter.md)
2. [docs/architecture/system-blueprint.md](docs/architecture/system-blueprint.md)
3. [docs/architecture/core-operational-loops.md](docs/architecture/core-operational-loops.md)
4. [docs/specs/core-data-contracts.md](docs/specs/core-data-contracts.md)
5. [docs/plans/implementation-program.md](docs/plans/implementation-program.md)
6. [docs/guides/spec-authority.md](docs/guides/spec-authority.md)

## 执行入口

执行层面的计划以 `.trae/specs/` 为权威，主入口不再是 `mvp-*` 或 `phoenix`，而是 7 条主线：

- `platform-foundation`
- `runtime-orchestration`
- `memory-knowledge`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`
- `release-program`

5 个 Story 继续保留，但只作为 **验收与演示套件**，不再承担顶层规划职责。

## 架构主线

SherryAgent 仍保留六层能力口径，但在实现计划上按公司级模块边界组织：

- Gateway
- Task Service
- Planner
- Execution Engine
- Memory & Retrieval
- Policy & Guardrail
- Scheduler & Trigger
- Observability & Evaluation
- Cost & Capacity Controller
- Release & Ops

详见 [ARCHITECTURE.md](ARCHITECTURE.md) 以及 [docs/architecture/module-map.md](docs/architecture/module-map.md)。

## 文档总览

- [AGENTS.md](AGENTS.md)：后续 Agent 的工作规则
- [docs/INDEX.md](docs/INDEX.md)：完整文档索引
- [docs/stories/](docs/stories/)：5 个 Story 验收套件
- [docs/archive/](docs/archive/)：历史路线图与 pre-project 资料

## 技术栈口径

文档中的技术栈仍以未来实现为目标口径：

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

## 当前原则

- 当前只做文档与计划重构，不恢复实现代码。
- 所有新增能力必须同时落到 `docs/` 与 `.trae/specs/`。
- 质量与安全默认优先于延迟与成本。

