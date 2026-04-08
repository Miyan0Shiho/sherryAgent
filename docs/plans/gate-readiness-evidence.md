---
title: "Gate Readiness Evidence"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "./development-readiness-gate-decision.md"
  - "./master-program.md"
  - "../specs/tool-governance.md"
  - "../specs/evaluation-governance.md"
  - "../specs/cost-ops-governance.md"
---

# Gate Readiness Evidence

## 使用规则

本文档是 `G1-G4` 的正式证据汇总入口。每个 gate 只有在这里能明确看到：

- 必需输入
- 引用源
- 通过理由
- 结论

才算具备正式判定基础。

## G1 Foundation Gate

### `platform-foundation`

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| 核心对象字段统一 | `core-data-contracts.md` | 已写死 `Task / Run / Evidence / Decision / Cost Record` 必填字段、关系和最小索引 |
| 状态机统一 | `core-data-contracts.md`, `core-operational-loops.md` | 已统一 `created -> planned -> running -> waiting_confirmation -> completed|blocked|failed|cancelled` |
| 风险、确认、降级、Decision 规则 | `permission-system.md`, `quality-vs-latency-vs-cost.md`, `core-data-contracts.md` | 已固定风险等级、Decision 生成和降级留痕规则 |
| 配置分层、生命周期、恢复最小上下文 | `core-data-contracts.md` | 已固定 `local / team / prod`、冷热分层和恢复前提 |

结论：`platform-foundation` 可作为 `G1` 正式输入。

### `runtime-orchestration`

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| 四条主链路契约 | `core-operational-loops.md` | 已逐条固定入口、触发条件、输出和降级 |
| 角色边界 | `core-operational-loops.md`, `multi-agent-orchestration.md`, `heartbeat-engine.md` | 已固定 Planner / Execution / Scheduler / Policy / Review 边界 |
| 失败与恢复 | `core-operational-loops.md`, `task-persistence.md`, `agent-loop.md` | 已固定 `waiting_confirmation` / `blocked` / `failed` 差异和恢复约束 |
| Story 映射 | `story-gate-matrix.md`, 各 Story 文档 | Story 输出均回映到统一对象和主链路 |

结论：`runtime-orchestration` 可作为 `G1` 正式输入。

### G1 总结

`G1 Foundation Gate`：`PASS`

## G2 Capability Gate

### `memory-knowledge`

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| 四层记忆边界 | `memory-system.md` | 已固定短期上下文、工作记忆、长期记忆、冷归档 |
| Evidence 与记忆关系 | `memory-system.md` | 已固定长期记忆优先绑定 Evidence，禁止未验证文本直接沉淀 |
| 检索、压缩、TTL、引用、置信度 | `memory-system.md` | 已固定混合检索、预算裁剪、TTL、时效处理和引用格式 |
| 10x / 100x、版本化、隔离 | `memory-system.md`, `scaling-strategy.md` | 已固定扩容、版本化和跨边界隔离规则 |

结论：`memory-knowledge` 可作为 `G2` 正式输入。

### `tooling-integration`

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| 工具最小契约 | `tool-governance.md` | 已固定最小字段、元数据和 replay 声明 |
| 工具分类 | `tool-governance.md` | 已固定 `READ_ONLY / WRITE / HIGH_RISK / DESTRUCTIVE` |
| CLI / MCP / HTTP/API 边界 | `tool-governance.md` | 已固定三类接入边界和鉴权原则 |
| 幂等、超时、重试、确认、降级 | `tool-governance.md`, `permission-system.md` | 已固定治理规则和高风险默认确认策略 |

结论：`tooling-integration` 可作为 `G2` 正式输入。

### G2 总结

`G2 Capability Gate`：`PASS`

## G3 Governance Gate

### `quality-evaluation`

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| 六类评测层级 | `evaluation-governance.md` | 已固定目标、输入和输出 |
| baseline vs current | `evaluation-governance.md` | 已固定基线定义和不可漂移规则 |
| 结果模板与 gate 映射 | `evaluation-governance.md` | 已固定质量、风险、成本、时延模板和 gate 消费关系 |
| corpus 治理 | `evaluation-governance.md` | 已固定 `golden tasks`、`failure corpus`、`policy regression cases` |

结论：`quality-evaluation` 可作为 `G3` 正式输入。

### `cost-latency-ops`

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| 三档预算 | `quality-vs-latency-vs-cost.md`, `cost-ops-governance.md` | 已固定 `strict / balanced / premium` 的适用场景和升级条件 |
| 降级顺序 | `quality-vs-latency-vs-cost.md`, `cost-ops-governance.md` | 已固定统一降级顺序 |
| 缓存、限流、延迟、容量指标 | `cost-ops-governance.md`, `technical-metrics.md`, `scaling-strategy.md` | 已固定关键策略和容量指标 |
| replay、dashboard、告警、回滚 | `cost-ops-governance.md`, `observability-system.md` | 已固定治理层必需运维资产 |

结论：`cost-latency-ops` 可作为 `G3` 正式输入。

### G3 总结

`G3 Governance Gate`：`PASS`

## G4 Release Readiness Gate

| 检查项 | 证据来源 | 结论 |
|------|----------|------|
| `G1-G4` 输入、阻断条件、输出 | `master-program.md`, `development-readiness-gate-decision.md`, 本文档 | 已形成正式闭环 |
| Story 穿透 gate | `story-gate-matrix.md` | 5 个 Story 已被正式纳入 gate 程序 |
| 质量、成本、运维输入 | `evaluation-governance.md`, `cost-ops-governance.md` | 已形成治理层输入 |
| 多对话治理与 release program | `multi-conversation-development.md`, `github-governance-controls.md`, `release-program` specs | 已具备项目程序与控制面说明 |

结论：`release-program` 可据此做 `G4` 汇总判断。

### G4 总结

`G4 Release Readiness Gate`：`PASS`
