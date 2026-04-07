# SherryAgent - Release Program Spec

## Overview
- **Summary**: 定义里程碑、依赖关系、验收门禁、风险台账和上线策略。
- **Purpose**: 把研发、测试、评测、运维整合成可执行的项目交付程序。
- **Primary Owners**: 项目管理、交付治理、质量门禁与发布运营负责人。

## Goals
- 固定阶段顺序与跨主线依赖
- 固定文档交付门禁
- 固定上线前必须满足的质量、成本、安全和回滚要求

## Non-Goals
- 不生成具体发布日期

## Inputs
- 7 条主线的 spec/tasks/checklist
- 5 个 Story 作为正式验收套件的映射结果
- `docs/plans/implementation-program.md` 中的整体实施计划
- `quality-evaluation`、`cost-latency-ops`、`platform-foundation` 提供的门禁指标与共用契约

## Outputs
- 跨主线依赖图、阶段顺序、里程碑和交付门禁
- 风险台账、阻断升级机制和阶段性决策规则
- Story 验收、质量回归、成本稳定性和运维准备的综合出口条件
- 供未来真正排期与项目例会使用的项目程序定义

## Dependencies
### Upstream
- `platform-foundation`：提供统一对象、审计和配置基线
- `runtime-orchestration`：提供核心能力范围和链路成熟度
- `memory-knowledge`、`tooling-integration`：提供平台关键能力成熟度
- `quality-evaluation`、`cost-latency-ops`：提供门禁指标与风险判断依据

### Downstream
- 后续任何“实现阶段排期”“重建代码讨论”“上线准备”都必须依赖本主线产出的阶段门禁

## Milestones
### M1: Program Structure Freeze
- 固定 7 条主线的依赖关系、阶段顺序和并行窗口
- 明确哪些工作可以并行，哪些必须先冻结前置契约

### M2: Gate Policy Freeze
- 固定文档门禁、评测门禁、成本门禁、安全门禁和运维门禁
- 明确每个阶段需要哪些 evidence 才允许推进

### M3: Risk Ledger Freeze
- 固定风险登记、分级、责任人、缓解动作和升级路径
- 明确范围变更、架构变更、成本异常和安全争议的裁决机制

### M4: Story & Release Integration Gate
- 5 个 Story 统一纳入阶段验收
- 发布准备不再依赖旧 `mvp-*` 或 `phoenix` 叙事

## Implementation Notes
- 本主线的工作重点不是“写更多计划”，而是防止各主线独立推进后失去统一交付节奏
- 任何阶段推进都必须有明确出口条件，不能以“文档已经很多了”替代完成定义
- Risk ledger 必须是活文档，而不是一次性罗列问题

## Blocking Conditions
- 7 条主线之间仍然存在隐性依赖，无法形成清晰的交付顺序
- 门禁标准没有引用正式评测、成本或安全指标
- Story 验收与主线里程碑脱节，导致展示与实际交付不一致
- 仍然需要引用旧路线图或历史计划才能解释当前排期

## Exit Criteria
- 7 条主线具备清晰依赖、阶段顺序和阶段门禁
- Story、评测、成本、安全、运维要求都被纳入统一交付程序
- 后续可以直接在本主线基础上扩展 master program、里程碑图和周度执行节奏

## Acceptance Criteria
- 阶段、依赖、门禁和风险管理都可直接指导后续实施
- 不再依赖 Story 或旧路线图做顶层排期
