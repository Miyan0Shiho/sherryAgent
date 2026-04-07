# SherryAgent - Platform Foundation Spec

## Overview
- **Summary**: 定义平台底座，包括任务模型、事件模型、状态机、权限、审计、配置和存储基础。
- **Purpose**: 为后续所有运行链路提供统一对象、统一边界和统一治理口径。
- **Primary Owners**: 平台架构、治理与运行时基础能力负责人。

## Goals
- 固定 Task / Run / Evidence / Decision / Cost Record 数据对象
- 固定统一状态机、风险分级、预算档位
- 固定配置分层与权限审计口径

## Non-Goals
- 本阶段不恢复任何运行时代码
- 不深入某条具体业务链路的实现细节

## Inputs
- `docs/specs/core-data-contracts.md` 中定义的核心对象与字段口径
- `docs/architecture/module-map.md` 中的平台模块边界
- `docs/architecture/core-operational-loops.md` 中四条主链路的共性约束
- `docs/guides/spec-authority.md` 中的双权威与冲突裁决规则

## Outputs
- 平台统一对象与状态机规范
- 风险分级、预算档位、审计字段和幂等语义
- 配置分层、环境边界与存储生命周期原则
- 供其余 6 条主线直接复用的基础契约清单

## Dependencies
### Upstream
- `docs/vision/product-charter.md`：定义平台面向的小团队、多仓库、多任务并发目标
- `docs/architecture/system-blueprint.md`：定义平台整体边界和模块职责

### Downstream
- `runtime-orchestration` 依赖本主线提供统一对象、状态机和任务元数据
- `memory-knowledge` 依赖本主线提供 Evidence 生命周期和版本语义
- `tooling-integration` 依赖本主线提供权限、审计和幂等口径
- `quality-evaluation`、`cost-latency-ops`、`release-program` 依赖本主线提供统一指标和状态来源

## Milestones
### M1: Core Object Freeze
- 固定 `Task / Run / Evidence / Decision / Cost Record` 的必填字段、状态流转和最小索引语义
- 明确幂等键、关联关系、审计追踪字段

### M2: Governance Freeze
- 固定风险等级、预算档位、权限审批口径和审计保留要求
- 明确人工确认与自动决策的边界

### M3: Configuration & Storage Freeze
- 固定 `local / team / prod` 配置分层
- 固定任务、证据、审计、成本记录的生命周期和归档原则

### M4: Cross-Axis Adoption Gate
- 其余 6 条主线在自身 spec/tasks/checklist 中引用并继承本主线产物
- 不再允许各主线单独发明对象字段或状态机

## Implementation Notes
- 平台底座优先保证术语稳定性，避免为局部场景优化破坏全局契约
- 任何新增对象都必须先证明无法由五个核心对象组合表达
- 审计字段必须优先服务回放、归责和成本核算，而不是只服务日志展示

## Blocking Conditions
- 核心对象字段在 `docs/*` 与 `.trae/specs/*` 中出现多套定义
- 状态机无法覆盖四条主链路的暂停、失败、重试、人工接管场景
- 权限、预算和审计口径不能支撑 `quality-evaluation` 与 `cost-latency-ops` 的指标需求
- 配置分层仍然混用“个人实验”与“团队运行”假设

## Exit Criteria
- 其余 6 条主线都能直接引用本主线对象与治理口径，无需补充“实现者自行决定”
- Story 套件中的 5 个场景都能映射到统一对象和状态机
- 评测、回归、观测、成本与发布文档都能从本主线对象直接取数

## Acceptance Criteria
- 文档中不存在“实现者自行决定”的核心对象字段
- 状态机、幂等、审计、配置分层都有明确文字约束
