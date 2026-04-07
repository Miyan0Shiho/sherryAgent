---
title: "SherryAgent 文档索引"
status: approved
created: 2026-04-03
updated: 2026-04-07
---

# SherryAgent 文档索引

## 产品蓝图

> 这是当前仓库的第一入口。阅读顺序应当是“产品 -> 架构 -> 契约 -> 计划 -> 验收”，而不是先看 Story。

| 文档 | 描述 |
|------|------|
| [product-charter.md](vision/product-charter.md) | 产品章程：定位、用户、目标工作负载、成功指标 |
| [north-star.md](vision/north-star.md) | 融合命题与长期成功定义 |
| [system-blueprint.md](architecture/system-blueprint.md) | 系统蓝图：服务边界、模块关系、数据流 |
| [module-map.md](architecture/module-map.md) | 公司级模块拆分与职责边界 |
| [runtime-modes.md](architecture/runtime-modes.md) | 4 种运行模式与各自 SLA/策略 |
| [core-operational-loops.md](architecture/core-operational-loops.md) | 4 条主链路、状态机与降级策略 |
| [core-data-contracts.md](specs/core-data-contracts.md) | Task/Run/Evidence/Decision/Cost Record 契约 |
| [quality-vs-latency-vs-cost.md](architecture/quality-vs-latency-vs-cost.md) | 质量/延迟/成本三角的默认决策矩阵 |
| [scaling-strategy.md](architecture/scaling-strategy.md) | 10x / 100x 扩容设计与容量指标 |

## 实现计划

| 文档 | 描述 |
|------|------|
| [implementation-program.md](plans/implementation-program.md) | 统一实现总计划：主线、阶段、门禁、交付节奏 |

### `.trae/specs` 主线计划

| 计划轴 | 描述 |
|------|------|
| `platform-foundation/` | 任务模型、状态机、权限、审计、配置、存储基础 |
| `runtime-orchestration/` | planner、agent loop、执行链路、workflow、调度 |
| `memory-knowledge/` | 上下文、长期记忆、索引、检索、压缩、知识版本化 |
| `tooling-integration/` | 工具协议、MCP/CLI/API、幂等、隔离、依赖治理 |
| `quality-evaluation/` | benchmark、回归、golden tasks、安全评测、负载评测 |
| `cost-latency-ops/` | 预算、缓存、限流、观测、SRE 手册、容量规划 |
| `release-program/` | 里程碑、依赖、验收门禁、上线/回滚策略 |

## 验收与演示套件

> Story 继续保留，但角色已经变成验收与对外演示入口，不再是顶层计划主轴。

| Story | 描述 |
|------|------|
| [story-01-rigorous-dev-copilot.md](stories/story-01-rigorous-dev-copilot.md) | 严谨开发协作验收场景 |
| [story-02-personal-clerk.md](stories/story-02-personal-clerk.md) | 重复事务与条件触发验收场景 |
| [story-03-ops-sentinel-incident-responder.md](stories/story-03-ops-sentinel-incident-responder.md) | 运维巡检与事故响应验收场景 |
| [story-04-research-miner-security-auditor.md](stories/story-04-research-miner-security-auditor.md) | 批量调研与安全审计验收场景 |
| [story-05-repo-guardian-release-pilot.md](stories/story-05-repo-guardian-release-pilot.md) | 仓库治理与发布门禁验收场景 |

## 标准与治理

| 文档 | 描述 |
|------|------|
| [spec-authority.md](guides/spec-authority.md) | `.trae + docs` 双权威与冲突裁决 |
| [design-principles.md](standard/design-principles.md) | 设计目标与原则 |
| [naming-conventions.md](standard/naming-conventions.md) | 命名规范 |
| [coding-standards.md](standard/coding-standards.md) | 编码标准 |
| [story-template.md](standard/story-template.md) | Story 模板 |
| [glossary.md](reference/glossary.md) | 术语表 |

## 技术规范与参考

| 文档 | 描述 |
|------|------|
| [core-data-contracts.md](specs/core-data-contracts.md) | 核心数据契约：Task/Run/Evidence/Decision/Cost Record |
| [six-layer-architecture.md](specs/six-layer-architecture.md) | 六层能力视角（能力来源，不等于模块蓝图） |
| [data-flow.md](specs/data-flow.md) | 平台级数据流契约 |
| [agent-loop.md](specs/agent-loop.md) | Execution Engine 中 Agent Loop 的运行契约 |
| [memory-system.md](specs/memory-system.md) | Memory & Retrieval 契约 |
| [task-persistence.md](specs/task-persistence.md) | Task Service 与恢复契约 |
| [multi-agent-orchestration.md](specs/multi-agent-orchestration.md) | Planner 与编排契约 |
| [permission-system.md](specs/permission-system.md) | Policy & Guardrail 契约 |
| [heartbeat-engine.md](specs/heartbeat-engine.md) | Scheduler & Trigger 契约 |
| [observability-system.md](specs/observability-system.md) | Observability & Evaluation 契约 |
| [tech-stack.md](reference/tech-stack.md) | 技术栈总览 |
| [project-structure.md](reference/project-structure.md) | 当前 docs-only 项目结构 |
| [technical-metrics.md](reference/technical-metrics.md) | 技术指标参考 |
| [business-metrics.md](reference/business-metrics.md) | 业务指标参考 |

## Legacy 与历史资料

| 文档 | 描述 |
|------|------|
| [implementation-snapshot.md](legacy/implementation-snapshot.md) | 已删除实现的能力快照 |
| [source-map.md](legacy/source-map.md) | 研究文档引用映射 |
| [phoenix-roadmap.md](archive/plans/phoenix-roadmap.md) | 已归档：旧比喻式路线图 |
| [mvp-roadmap.md](archive/plans/mvp-roadmap.md) | 已归档：旧 MVP 路线图 |
