# SherryAgent

> 基于 Claude Code 与 OpenClaw 两类 Agent 优势融合的 Hybrid Platform 项目蓝图。

## Mode: docs-only / planning-first

本仓库当前处于 **docs-only** 阶段。你不应尝试恢复旧实现，也不应把历史 `mvp-*`、`phoenix-roadmap` 作为当前执行入口。

## How To Work Here

### 1) 先读

1. `docs/vision/product-charter.md`
2. `docs/architecture/system-blueprint.md`
3. `docs/architecture/core-operational-loops.md`
4. `docs/specs/core-data-contracts.md`
5. `docs/plans/implementation-program.md`
6. `docs/guides/spec-authority.md`

### 2) 再做

任何非 trivial 变更都必须先落到 `.trae/specs/*`，再同步更新 `docs/*` 的系统契约与产品口径。

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

SherryAgent 保留六层能力视角，但实现计划按公司级模块边界组织：

```
Gateway
  -> Task Service
  -> Planner
  -> Execution Engine
  -> Memory & Retrieval
  -> Policy & Guardrail
  -> Scheduler & Trigger
  -> Observability & Evaluation
  -> Cost & Capacity Controller
  -> Release & Ops
```

详见 `docs/architecture/system-blueprint.md` 与 `docs/architecture/module-map.md`。

## Working Rules

### Spec Authority

SherryAgent 采用 **`.trae/specs` + `docs/` 双权威**：

- `.trae/specs/*`：开发执行权威
- `docs/*`：系统契约与产品/运营口径权威
- `docs/stories/*`：验收与演示套件，不是顶层规划主轴
- OpenSpec：仅方法论参考

冲突裁决见：`docs/guides/spec-authority.md`

### Current Planning Axes

当前执行主线固定为 7 条：

- `platform-foundation`
- `runtime-orchestration`
- `memory-knowledge`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`
- `release-program`

### Definition of Done

任何非 trivial 计划或契约变更至少满足：

- `.trae/specs` 的相关 `spec/tasks/checklist` 已更新
- `docs/` 的相关蓝图、契约、索引已更新
- 关键数据对象、指标口径、链路状态机没有留给实现者二次决定

### Safety Red Lines

- 禁止把高风险动作默认自动化
- 禁止绕过权限、审计、确认、沙箱讨论实现
- 禁止用“先跑通再补治理”掩盖系统边界缺失
- 禁止把 Story 文档当作架构主计划替代物

## Recommended Reading Path

1. `docs/vision/product-charter.md`
2. `docs/architecture/module-map.md`
3. `docs/architecture/quality-vs-latency-vs-cost.md`
4. `docs/plans/implementation-program.md`
5. `docs/stories/`（仅用于验收视角）

