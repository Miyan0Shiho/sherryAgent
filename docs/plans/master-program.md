---
title: "Master Program"
status: draft
created: 2026-04-07
updated: 2026-04-08
related:
  - "./implementation-program.md"
  - "./story-gate-matrix.md"
  - "../architecture/system-blueprint.md"
  - "../architecture/core-operational-loops.md"
---

# Master Program

## Program Objective

本文件是 SherryAgent 的总控计划文档，用于把 7 条主线汇总成一个可执行的项目程序。它回答 4 个问题：

1. 哪些主线必须先完成，哪些可以并行推进。
2. 每个阶段的出口条件是什么。
3. 什么时候允许从 planning-first 进入实现阶段。
4. 当质量、成本、延迟或安全发生冲突时，谁有权阻断推进。

## Program Scope

本 program 面向当前 docs-only 阶段和后续实现重建阶段，默认服务于：

- 小团队协作
- 多仓库、多任务并发
- 质量与安全优先
- 成本与延迟通过预算、模式和降级控制

不在本 program 内的内容：

- 具体发布日期
- 具体人力分配
- 具体代码实现方案

## Workstreams

| 主线 | 角色 | 核心产物 |
|------|------|----------|
| `platform-foundation` | 平台底座 | 核心对象、状态机、风险、预算、审计、配置 |
| `runtime-orchestration` | 执行骨架 | 4 条主链路、planner/executor/scheduler 边界 |
| `memory-knowledge` | 信息治理 | 检索、压缩、记忆、Evidence 生命周期、10x/100x 策略 |
| `tooling-integration` | 工具治理 | 工具协议、接入边界、幂等、隔离、失败治理 |
| `quality-evaluation` | 质量平台 | benchmark、回归、Story 验收、基线对比 |
| `cost-latency-ops` | 运营控制 | 预算、缓存、限流、观测、SRE、容量规划 |
| `release-program` | 总控治理 | 里程碑、门禁、风险台账、阶段切换、发布治理 |

## Dependency Map

### Hard Dependencies

| 下游主线 | 依赖上游 | 原因 |
|------|------|------|
| `runtime-orchestration` | `platform-foundation` | 没有统一对象与状态机，无法定义链路 |
| `memory-knowledge` | `platform-foundation`, `runtime-orchestration` | 没有 Evidence 语义与检索触发点，无法定义记忆边界 |
| `tooling-integration` | `platform-foundation`, `runtime-orchestration` | 没有风险/审计和运行触发模板，无法定义工具治理 |
| `quality-evaluation` | `runtime-orchestration`, `memory-knowledge`, `tooling-integration`, `cost-latency-ops` | 没有链路、检索、工具、成本口径，无法做比较 |
| `cost-latency-ops` | `platform-foundation`, `runtime-orchestration`, `tooling-integration`, `memory-knowledge` | 没有记录字段和关键延迟点，无法定义预算与观测 |
| `release-program` | 所有主线 | 没有完整输入，无法做阶段门禁和项目治理 |

### Soft Dependencies

| 主线 | 软依赖 | 说明 |
|------|------|------|
| `runtime-orchestration` | `cost-latency-ops` | 运行模式的延迟/预算目标需要后续回填 |
| `memory-knowledge` | `quality-evaluation` | 检索质量指标需要评测层正式冻结 |
| `tooling-integration` | `quality-evaluation` | 故障注入和越权回归会反向校正工具治理 |

## Phase Map

### Phase 0: Program Setup

目标：
- 固定主线、术语、文档入口和双权威规则。
- 清理旧 `phoenix / mvp-*` 叙事对当前计划的干扰。

必须完成：
- `docs/INDEX.md`、`implementation-program.md`、7 条主线 `spec/tasks/checklist` 建立统一口径。
- 5 个 Story 降级为正式验收套件，而非顶层计划轴。

出口条件：
- 所有文档入口不再引用旧主轴。
- 7 条主线具备基础 spec/tasks/checklist。

### Phase 1: Foundation Freeze

目标：
- 先冻结平台底座和运行骨架，避免后续主线各自发明对象和控制流。

主线：
- `platform-foundation`
- `runtime-orchestration`

并行窗口：
- 两条主线可并行推进，但 `runtime-orchestration` 的最终冻结依赖 `platform-foundation` 的对象与状态机冻结。

出口条件：
- 4 条主链路、5 个核心对象、统一状态机、预算档位、风险分级都已定稿。
- Story 与 4 条主链路映射一致。

### Phase 2: Capability Freeze

目标：
- 冻结可复用能力层，明确工具、记忆、信息治理和运行边界。

主线：
- `memory-knowledge`
- `tooling-integration`

并行窗口：
- 两条主线可并行推进。
- 如果 Evidence 生命周期、权限口径或工具风险分类未冻结，则不得进入本阶段出口。

出口条件：
- 记忆、检索、压缩、TTL、知识版本、工具协议、接入边界和失败治理全部定稿。
- 10x / 100x 策略具备可引用口径。

### Phase 3: Governance Freeze

目标：
- 把质量、成本、延迟、观测和 SRE 从“工程附属物”提升为正式平台能力。

主线：
- `quality-evaluation`
- `cost-latency-ops`

并行窗口：
- 两条主线可并行，但 `quality-evaluation` 依赖 `cost-latency-ops` 的成本与延迟指标，`cost-latency-ops` 依赖前面主线暴露关键事件点。

出口条件：
- 6 类评测层级、baseline 与回归资产规则已经冻结。
- 三档预算、缓存、限流、降级、容量规划和 SRE 口径已经冻结。

### Phase 4: Release Readiness

目标：
- 把 7 条主线汇总为统一交付程序，形成真正能指导实现和上线的治理体系。

主线：
- `release-program`

并行窗口：
- 可在 Phase 2 开始预研，但只有在 Phase 3 指标冻结后才能完成 gate 定稿。

出口条件：
- 7 条主线依赖图、阶段图、门禁矩阵和风险台账全部定稿。
- 允许进入“实现阶段”的条件已写死。

## Parallelization Windows

| 窗口 | 可并行项 | 共享前置条件 | 共同风险 |
|------|----------|--------------|----------|
| Window A | `platform-foundation` + `runtime-orchestration` | 术语、对象命名、状态机命名统一 | 对象未冻结导致链路返工 |
| Window B | `memory-knowledge` + `tooling-integration` | Evidence、Decision、权限口径已冻结 | 记忆与工具都单独扩展语义 |
| Window C | `quality-evaluation` + `cost-latency-ops` | 关键事件点、成本记录、运行模式定义完整 | 指标取数口径不一致 |
| Window D | `release-program` + Story 验收细化 | 其余主线至少完成阶段出口草案 | 发布门禁脱离真实主线产物 |

## Gate Matrix

| Gate | 必需输入 | 阻断条件 | 输出 |
|------|----------|----------|------|
| `G1 Foundation Gate` | `platform-foundation`, `runtime-orchestration` | 对象、状态机、主链路仍存在多套定义 | 允许进入能力层细化 |
| `G2 Capability Gate` | `memory-knowledge`, `tooling-integration` | 记忆边界、工具协议、权限风险仍需实现者自行决定 | 允许进入质量与运营治理 |
| `G3 Governance Gate` | `quality-evaluation`, `cost-latency-ops` | 无 baseline、无成本口径、无容量指标、无降级顺序 | 允许定义发布与实现切换条件 |
| `G4 Release Readiness Gate` | `release-program` + 5 个 Story | 风险台账缺失、门禁不引用正式指标、Story 无法证明闭环 | 允许进入实现阶段讨论 |

## Decision Rules

- 当质量与成本冲突时，默认以质量与安全优先，除非任务被标记为高频低风险批量任务。
- 当运行效率与审计完整性冲突时，默认保留审计完整性。
- 当某主线希望引入新对象、新状态或新指标时，必须先回写 `platform-foundation` 或对应上游主线。
- 当 Story 展示效果与正式门禁冲突时，以正式门禁为准。

## Readiness Definition For Rebuild

只有同时满足以下条件，才允许进入“恢复实现/重建代码”讨论：

- `G1` 到 `G4` 全部通过。
- 7 条主线的 `spec/tasks/checklist` 没有红色阻断项。
- 5 个 Story 都具备正式验收检查点。
- `quality-evaluation` 已定义 baseline、回归资产和结果模板。
- `cost-latency-ops` 已定义预算档位、降级顺序和 10x / 100x 容量指标。
- `release-program` 已产出阶段门禁与风险台账格式。

## Program Risks

| 风险 | 说明 | 预防策略 |
|------|------|----------|
| 计划漂移 | 各主线继续独立演化术语和对象 | 统一回写到 foundation 与 glossary |
| 展示优先 | Story 演示反向绑架平台设计 | Story 只作为验收套件，不作为顶层约束 |
| 成本盲区 | 质量设计完备，但成本与扩容后置 | Governance Freeze 前不允许进入发布准备 |
| 评测空转 | 写了 benchmark 名称，但没有 baseline 和语料治理 | 把评测资产更新写入主线 gate |

## Program Outputs

本 program 的最终产物不是代码，而是以下可直接指导未来实现的资产：

- 主线依赖图
- 阶段图与并行窗口
- 门禁矩阵
- Story 穿透 gate 的验收矩阵
- 风险台账格式
- 从 planning-first 进入实现阶段的切换标准
- GitHub 并行治理控制面（Issue/PR/CODEOWNERS/required checks）
