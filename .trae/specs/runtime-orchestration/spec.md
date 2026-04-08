# SherryAgent - Runtime Orchestration Spec

## Overview
- **Summary**: 定义 Planner、Execution Engine、Scheduler 与四条主链路的运行时组织方式。
- **Purpose**: 把交互式、后台、批量、发布治理四类工作负载统一到同一执行框架下。
- **Primary Owners**: 运行时架构、流程编排、交互与后台执行负责人。

## Goals
- 固定 4 条主链路的输入/输出契约
- 固定 mode、planner、executor、scheduler 的职责边界
- 固定超时、取消、重试、确认流的处理原则

## Non-Goals
- 不设计具体工具 API 细节

## Inputs
- `platform-foundation` 提供的对象模型、状态机、风险分级和预算档位
- `docs/architecture/runtime-modes.md` 中四种运行模式定义
- `docs/architecture/core-operational-loops.md` 中四条主链路草图
- `docs/specs/agent-loop.md`、`docs/specs/data-flow.md`、`docs/specs/runtime-modes.md` 中的系统契约

## Outputs
- 四条主链路的标准输入、输出、状态转换和失败降级规则
- Planner / Execution Engine / Scheduler 的责任边界
- 超时、取消、中断恢复、人工确认和重试的统一流程
- 支撑 Story 验收套件与质量评测的运行时模板
- `G1 Foundation Gate` 的正式输入证明

## Dependencies
### Upstream
- `platform-foundation`：提供任务对象、状态机、审计与预算语义
- `tooling-integration`：提供工具接入与执行约束
- `memory-knowledge`：提供检索、证据引用和上下文压缩能力边界

### Downstream
- `quality-evaluation` 依赖本主线固定链路模板以构建 benchmark 与回归
- `cost-latency-ops` 依赖本主线暴露关键延迟点、重试点和并发模型
- `release-program` 依赖本主线定义交付门禁中的运行链路能力范围

## Milestones
### M1: Loop Contract Freeze
- 固定 `Interactive Dev Loop`、`Autonomous Background Loop`、`Bulk Research / Analysis Loop`、`Repo/Release Governance Loop`
- 明确每条链路的入口、核心步骤、输出包和降级策略

### M2: Role Boundary Freeze
- 明确 Planner、Execution Engine、Scheduler、Policy Gate、Review 的边界
- 明确谁负责任务拆解、谁负责执行控制、谁负责触发与恢复

### M3: Failure & Recovery Freeze
- 固定超时、取消、重试、人工确认、中断恢复和任务恢复点的语义
- 明确哪些失败可以自动恢复，哪些必须升级到人工接管

### M4: Acceptance Integration Gate
- 5 个 Story 与 4 条主链路建立一一映射
- 质量评测和回归样本统一引用本主线链路模板

## Implementation Notes
- 运行时设计优先保证同一链路在不同模式下的可预测性，而不是追求“所有模式都复用完全相同的流程”
- Planner 只负责决策与拆解，不负责直接执行工具
- Scheduler 只负责触发与恢复，不负责替代 Planner 做复杂推理

## Blocking Conditions
- 任一主链路的输入、输出或降级策略仍需依赖隐含实现假设
- Planner / Execution / Scheduler 的职责重叠，导致归责和评测口径不清
- 运行模式与链路模板冲突，无法同时解释交互式和后台式任务
- Story 验收无法明确绑定某条主链路

## Exit Criteria
- 4 条主链路都具备完整的输入/输出、状态机和降级说明
- Story 套件、质量评测、成本观测都以本主线链路作为统一参照
- 后续实现阶段可以据此直接画出时序图和组件接口，不需要重写运行时口径

## Acceptance Criteria
- 4 条主链路都有明确流程、目标和降级策略
- Planner / Execution / Scheduler 边界没有重叠歧义
