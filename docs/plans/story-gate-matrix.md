---
title: "Story Gate Matrix"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "./master-program.md"
  - "./implementation-program.md"
  - "../architecture/core-operational-loops.md"
  - "../specs/core-data-contracts.md"
---

# Story Gate Matrix

## Purpose

本文件回答一个项目治理问题：

> 5 个 Story 不是独立展示页，而是必须穿透 7 条主线 gate 的正式验收套件。

因此，本矩阵用于明确：

- 每个 Story 依赖哪些主线能力。
- 每个 Story 要穿过哪些 gate 才能被视为“正式可验收”。
- 每个 Story 在 `G1` 到 `G4` 各自检查什么。
- 哪些阻断条件会导致 Story 虽然“看起来能演示”，但仍然不允许进入实现或发布讨论。

## How To Read

- `主链路`：该 Story 的主验收运行链路。
- `主对象`：验收时必须落地的核心数据对象。
- `Gate 穿透`：该 Story 在 `G1`、`G2`、`G3`、`G4` 的最小通过要求。
- `关键阻断`：即使 Story 演示能跑，也会被正式门禁拒绝的情况。

## Story Summary

| Story | 主链路 | 核心模式 | 主对象 |
|------|--------|----------|--------|
| `Story-01 Rigorous Dev Copilot` | `Interactive Dev Loop` | `interactive-dev` | `Task`, `Run`, `Evidence`, `Decision`, `Cost Record` |
| `Story-02 Personal Clerk` | `Autonomous Background Loop` | `autonomous-safe` | `Task`, `Run`, `Evidence`, `Decision`, `Cost Record` |
| `Story-03 Ops Sentinel + Incident Responder` | `Autonomous Background Loop` | `background-ops` | `Task`, `Run`, `Evidence`, `Decision`, `Cost Record` |
| `Story-04 Research Miner + Security Auditor` | `Bulk Research / Analysis Loop` | `bulk-analysis` | `Task`, `Run`, `Evidence`, `Decision`, `Cost Record` |
| `Story-05 Repo Guardian + Release Pilot` | `Repo / Release Governance Loop` | `interactive-dev` + `background-ops` | `Task`, `Run`, `Evidence`, `Decision`, `Cost Record` |

## Gate Penetration Matrix

| Story | `G1 Foundation Gate` | `G2 Capability Gate` | `G3 Governance Gate` | `G4 Release Readiness Gate` |
|------|-----------------------|----------------------|----------------------|-----------------------------|
| `Story-01` | 统一对象、状态机、`Interactive Dev Loop`、Planner/Execution 边界已冻结 | 工具契约、权限审计、最小记忆与 Evidence 引用已冻结 | 具备 baseline、开发会话质量门槛、成本与延迟指标 | 可纳入总控 gate，且开发 Story 的通过条件被 release-program 正式引用 |
| `Story-02` | 后台任务对象、`waiting_confirmation`、调度与 dry-run/real-run 区分已冻结 | Trigger、审计、工具分类、周期任务记忆与输入证据已冻结 | 高频触发限流、严格预算、无人值守安全门槛已冻结 | 可作为后台自动化代表场景纳入总控 gate，不允许因展示效果绕过安全门槛 |
| `Story-03` | 巡检与事故响应对象、告警状态流、后台运行链路已冻结 | 证据采集、工具治理、诊断与回滚计划模板已冻结 | 告警风暴治理、SRE 指标、误报/漏报回归与安全门槛已冻结 | 可作为运维与事故治理代表场景纳入总控 gate，必须与 runbook/回滚要求绑定 |
| `Story-04` | 批量任务对象、分片执行、聚合输出链路已冻结 | 检索、压缩、引用、工具范围限制与长期记忆治理已冻结 | baseline、事实/推断分离、长跑成本和吞吐指标已冻结 | 可作为调研/审计代表场景纳入总控 gate，必须证明规模化与低置信处理可控 |
| `Story-05` | 发布门禁对象、治理扫描与发布计划链路已冻结 | 工具分类、证据引用、回滚模板与 repo 规则治理已冻结 | 门禁误判回归、发布 dry-run 成本、生产风险门槛已冻结 | 本身直接参与 `G4`，用于证明 release-program 不是空壳流程 |

## Story By Story Gate Requirements

### Story-01: Rigorous Dev Copilot

#### Required Workstreams
- `platform-foundation`
- `runtime-orchestration`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`

#### Gate Requirements
- `G1`: 必须证明开发会话使用统一对象与 `Interactive Dev Loop`，且 `waiting_confirmation`、`blocked`、`failed` 的差异清晰。
- `G2`: 必须证明工具调用不会绕过 `Policy & Guardrail`，关键结论可用 `Evidence` 和 `Decision` 回放。
- `G3`: 必须证明高质量开发模式的单位成本、延迟和安全门槛可被比较。
- `G4`: 必须证明该 Story 的通过标准已经被 `release-program` 作为正式验收输入，而不是展示口径。

#### Key Blockers
- 开发计划无法映射到统一状态机。
- 高风险写操作能绕过确认。
- 最终报告没有 `Evidence` 或 `Cost Record`。

### Story-02: Personal Clerk

#### Required Workstreams
- `platform-foundation`
- `runtime-orchestration`
- `memory-knowledge`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`

#### Gate Requirements
- `G1`: 必须证明后台触发任务与 dry-run/real-run 使用统一对象和状态流。
- `G2`: 必须证明 trigger、输入证据、周期任务记忆和工具分类都受统一治理。
- `G3`: 必须证明高频触发任务具备限流、聚合、预算硬停止和无人值守安全门槛。
- `G4`: 必须证明该 Story 不能因“自动化体验好”而绕过正式门禁。

#### Key Blockers
- 高频触发没有聚合或限流。
- 高风险动作不会停在 `waiting_confirmation`。
- 背景任务没有可回放审计记录。

### Story-03: Ops Sentinel + Incident Responder

#### Required Workstreams
- `platform-foundation`
- `runtime-orchestration`
- `memory-knowledge`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`
- `release-program`

#### Gate Requirements
- `G1`: 必须证明巡检 Run 与事故响应 Run 的状态流和数据对象可区分。
- `G2`: 必须证明证据采集、诊断工具、回滚计划模板和敏感信息处理已经冻结。
- `G3`: 必须证明告警风暴治理、误报回归、SRE 指标和高风险动作门槛已经冻结。
- `G4`: 必须证明该 Story 的 runbook、回滚与人工接管要求已被 release-program 吸收。

#### Key Blockers
- 事故报告缺少证据或回滚计划。
- 告警风暴会生成大量独立任务而不是聚合。
- 修复动作可自动越权执行。

### Story-04: Research Miner + Security Auditor

#### Required Workstreams
- `platform-foundation`
- `runtime-orchestration`
- `memory-knowledge`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`

#### Gate Requirements
- `G1`: 必须证明批量分析任务与聚合输出链路具备统一对象、状态和产物格式。
- `G2`: 必须证明来源引用、压缩策略、范围限制、敏感目录限制和长期记忆治理已经冻结。
- `G3`: 必须证明事实/推断分离、低置信标记、长跑成本和吞吐门槛可被稳定评测。
- `G4`: 必须证明该 Story 的规模化和风险控制要求已被 release-program 接受为正式门禁输入。

#### Key Blockers
- 关键发现没有 Evidence 或证据缺口说明。
- 大范围任务没有采样、分片或限流。
- 高风险扫描范围没有明确边界。

### Story-05: Repo Guardian + Release Pilot

#### Required Workstreams
- `platform-foundation`
- `runtime-orchestration`
- `memory-knowledge`
- `tooling-integration`
- `quality-evaluation`
- `cost-latency-ops`
- `release-program`

#### Gate Requirements
- `G1`: 必须证明治理扫描 Run 与发布门禁 Run 使用统一对象、状态和 `Repo / Release Governance Loop`。
- `G2`: 必须证明门禁证据、工具分类、回滚模板和 repo 规则治理已经冻结。
- `G3`: 必须证明误放行/误阻断回归、dry-run 成本、生产风险阈值和确认流已经冻结。
- `G4`: 必须证明该 Story 被 `release-program` 用作发布就绪的代表性验收，而不是附属展示。

#### Key Blockers
- `Release Plan` 没有 `rollback_plan`。
- 门禁结论没有 Evidence。
- 生产相关动作不会停在确认或拒绝。

## Cross-Story Coverage

| 主线 | 被哪些 Story 覆盖 | 覆盖重点 |
|------|-------------------|----------|
| `platform-foundation` | 01, 02, 03, 04, 05 | 统一对象、统一状态机、风险、预算、审计 |
| `runtime-orchestration` | 01, 02, 03, 04, 05 | 4 条主链路与模式化运行 |
| `memory-knowledge` | 02, 03, 04, 05 | Evidence、检索、压缩、长期记忆、规模化 |
| `tooling-integration` | 01, 02, 03, 04, 05 | 工具分类、接入边界、越权防护 |
| `quality-evaluation` | 01, 02, 03, 04, 05 | Story 验收、回归、benchmark、风险门槛 |
| `cost-latency-ops` | 01, 02, 03, 04, 05 | 预算、限流、成本、延迟、容量 |
| `release-program` | 03, 05，并统摄 01/02/04 | gate、风险台账、实现切换条件 |

## Decision Rules

- Story 的“展示成功”不等于 gate 通过；只有穿透对应 gate，Story 才能作为正式验收资产。
- 任一 Story 若引入新的对象、状态、风险等级或指标，必须先回写对应主线文档。
- Story 若无法说明自身在 `G1` 到 `G4` 的穿透路径，则该 Story 只能算草稿，不算正式验收套件。
- `Story-05` 与 `Story-03` 是最直接触达发布与运行风险的场景，因此在 `G4` 中权重最高。

## Exit Criteria

- 5 个 Story 都能映射到 `G1` 到 `G4` 的正式门禁。
- 每个 Story 都能指出自身依赖的主线、关键阻断和正式通过条件。
- `master-program.md`、各 Story 文档和 7 条主线 checklist 可以互相引用且无冲突。
