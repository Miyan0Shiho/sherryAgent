# SherryAgent - Memory Knowledge Spec

## Overview
- **Summary**: 定义短期上下文、长期记忆、检索、压缩、TTL、知识版本化和冷热分层。
- **Purpose**: 保证复杂任务、多轮运行和批量场景下的信息一致性与成本可控。
- **Primary Owners**: 检索、记忆、知识治理与信息生命周期负责人。

## Goals
- 固定短期与长期记忆边界
- 固定检索与证据引用的基本规则
- 固定 10x / 100x 下的索引与冷热策略

## Non-Goals
- 不在本阶段挑选具体数据库或向量引擎实现

## Inputs
- `platform-foundation` 提供的 `Evidence / Run / Task` 对象和生命周期语义
- `docs/architecture/scaling-strategy.md` 中的 10x / 100x 扩展约束
- `docs/specs/memory-system.md` 中现有记忆与检索契约
- 4 条主链路对上下文压缩、证据引用、长期保留的差异化需求

## Outputs
- 短期上下文、长期记忆、证据库、知识版本的边界定义
- 检索、压缩、引用、归档、淘汰和冷热分层原则
- 面向交互任务、后台任务、批量分析和发布治理的差异化读取策略
- 供评测与成本控制复用的记忆命中与冗余控制口径

## Dependencies
### Upstream
- `platform-foundation`：提供 Evidence 标识、保留期限和审计要求
- `runtime-orchestration`：提供不同链路的检索触发点和上下文装载时机

### Downstream
- `quality-evaluation` 依赖本主线评估检索命中率、引用质量和长任务稳定性
- `cost-latency-ops` 依赖本主线定义缓存、索引、冷热分层和检索开销
- `release-program` 依赖本主线判断哪些里程碑需要规模化能力冻结

## Milestones
### M1: Memory Boundary Freeze
- 固定短期上下文、长期记忆、证据引用和知识版本的职责边界
- 明确每类数据的写入条件、读取条件和失效条件

### M2: Retrieval & Compression Freeze
- 固定检索触发规则、混合检索原则、压缩策略和引用格式
- 明确如何避免冗余注入、过时信息污染和上下文爆炸

### M3: Lifecycle & Scale Freeze
- 固定 TTL、冷热分层、归档和回收原则
- 给出 10x / 100x 下索引拆分、异步归档和租户隔离策略

### M4: Evaluation Integration Gate
- Story、benchmark、成本观测和扩容计划统一引用本主线指标
- 不再允许其它主线各自定义“临时记忆策略”

## Implementation Notes
- 记忆系统优先为“可追溯”和“可控成本”服务，而不是追求无限积累上下文
- 任何长期保留都必须有明确再利用场景与清理策略
- 引用必须优先绑定 Evidence，而不是直接绑定某次模型输出摘要

## Blocking Conditions
- 记忆边界不能支撑四条主链路的差异化需求
- 压缩策略无法解释信息损失、证据可追溯性或成本收益
- 10x / 100x 扩展仍依赖单一索引、单一租户或全量扫描假设
- Story 验收和回归无法从本主线提取检索与记忆指标

## Exit Criteria
- 所有链路都能说明何时读取、何时写入、何时压缩、何时丢弃记忆
- 评测与成本文档可以直接引用本主线指标定义
- 未来实现阶段能够在不改变契约的前提下替换具体存储或检索技术

## Acceptance Criteria
- 上下文压缩、长期记忆、证据引用之间的关系清晰
- 扩容时的分层与归档策略明确
