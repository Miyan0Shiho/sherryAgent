# SherryAgent - Quality Evaluation Spec

## Overview
- **Summary**: 把评测、回归和安全验证定义为平台级能力。
- **Purpose**: 确保 SherryAgent 的能力提升可以被量化、可回归、可比较。
- **Primary Owners**: 质量平台、基准评测、回归治理与安全验证负责人。

## Goals
- 固定 6 类评测层次
- 固定 baseline vs current 的对比口径
- 固定 golden tasks、failure corpus、policy regression cases 的更新要求

## Non-Goals
- 不执行任何真实 benchmark

## Inputs
- 4 条主链路与 5 个 Story 的正式验收映射
- `platform-foundation` 提供的核心对象、状态和审计字段
- `cost-latency-ops` 提供的成本、延迟、容量与降级指标
- `docs/reference/technical-metrics.md` 与 `docs/reference/business-metrics.md` 中的平台指标口径

## Outputs
- 6 类评测层级的定义、输入资产和输出模板
- `baseline vs current` 对比规则与默认基线解释
- `golden tasks`、`failure corpus`、`policy regression cases` 的维护要求
- 与 Story 套件和发布门禁联动的质量阻断规则

## Dependencies
### Upstream
- `runtime-orchestration`：提供链路模板与失败类型
- `tooling-integration`：提供工具治理与故障注入边界
- `memory-knowledge`：提供检索命中、压缩、长任务稳定性评测维度
- `cost-latency-ops`：提供预算、延迟和容量指标

### Downstream
- `release-program` 依赖本主线定义里程碑门禁与上线阻断标准
- 各 Story 验收文档依赖本主线定义其所属评测层级和通过条件

## Milestones
### M1: Evaluation Taxonomy Freeze
- 固定 `Capability Benchmark`、`Story Acceptance`、`Regression Suite`、`Load & Scale Test`、`Safety Evaluation`、`Cost/Latency Benchmark`
- 明确每一层的目标、输入资产、输出指标和使用场景

### M2: Baseline & Corpus Freeze
- 固定 baseline 定义和对比方法
- 明确 golden tasks、failure corpus、policy regression cases 的来源、更新和归档规则

### M3: Reporting & Gating Freeze
- 固定成功率、部分成功率、误判率、危险操作拦截率、单位成本、P95 延迟、人工介入率等输出模板
- 明确哪些指标异常会阻断发布、阻断计划推进或触发人工审查

### M4: Story Integration Gate
- 5 个 Story 全部接入正式评测层级
- 各主线 checklist 都明确何时必须更新评测资产

## Implementation Notes
- 评测体系必须优先服务“能否比较”和“能否回归”，而不是只追求漂亮分数
- Story 不替代 benchmark；Story 用于验收闭环，benchmark 用于解释能力变化
- 任何性能或成本优化若没有回归对比，都不应被视为有效进展

## Blocking Conditions
- baseline 不清晰，导致优化前后无法比较
- Story 验收与 benchmark 指标脱节，无法解释“为什么通过/失败”
- 缺乏固定 failure corpus，导致事故经验无法沉淀
- 发布门禁无法直接引用质量评测结果

## Exit Criteria
- 所有主线和 Story 都能映射到至少一种正式评测层级
- 回归资产更新要求已经写进各主线任务与清单
- 未来实现阶段可以直接据此建设 benchmark harness 和质量门禁

## Acceptance Criteria
- 评测层级、输出指标、回归机制全部有明确口径
- Story 与 benchmark 的关系清晰
