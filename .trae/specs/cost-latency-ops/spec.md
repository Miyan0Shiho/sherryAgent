# SherryAgent - Cost Latency Ops Spec

## Overview
- **Summary**: 定义预算、缓存、限流、观测、告警、容量规划和 SRE 运行口径。
- **Purpose**: 让质量、延迟、成本和稳定性之间的取舍可见且可运营。
- **Primary Owners**: 性能容量、成本控制、观测平台与 SRE 负责人。

## Goals
- 固定 `strict / balanced / premium` 预算档位
- 固定缓存、模型路由、限流、降级顺序
- 固定 10x / 100x 观测与容量规划指标

## Non-Goals
- 不实现监控或缓存系统

## Inputs
- `docs/architecture/quality-vs-latency-vs-cost.md` 中的默认决策矩阵
- `docs/architecture/scaling-strategy.md` 中的 10x / 100x 规划
- `platform-foundation` 提供的预算、风险、审计与成本记录字段
- `runtime-orchestration` 与 `tooling-integration` 提供的关键延迟点、重试点和并发模型

## Outputs
- `strict / balanced / premium` 预算档位的可执行定义
- 缓存、模型路由、限流、降级和容量规划的统一规则
- 运行观测、告警、值班、事故管理和回放指标
- 供评测、发布和运维共用的性能与成本目标线
- `G3 Governance Gate` 的正式输入证明

## Dependencies
### Upstream
- `platform-foundation`：提供成本记录、预算、风险级别和配置分层
- `runtime-orchestration`：提供主链路延迟、队列和恢复语义
- `tooling-integration`：提供工具调用开销与失败模式
- `memory-knowledge`：提供检索与存储的成本、容量与冷热分层输入

### Downstream
- `quality-evaluation` 依赖本主线输出成本、延迟和容量 benchmark 指标
- `release-program` 依赖本主线定义上线门禁中的预算、稳定性和扩容要求

## Milestones
### M1: Budget Policy Freeze
- 固定三档预算的适用场景、默认上限和升级条件
- 明确模型路由、缓存优先级和成本异常时的人工介入规则

### M2: Performance Control Freeze
- 固定限流、并发控制、重试退避、超时和降级顺序
- 明确不同运行模式和不同风险等级的延迟目标

### M3: Observability & SRE Freeze
- 固定日志、metrics、trace、replay、告警和事故分级口径
- 明确值班、升级、降级、回滚和人工接管的触发条件

### M4: Scale Freeze
- 固定 10x / 100x 下的容量指标、扩容阈值和服务拆分原则
- 明确 `tasks_per_min`、`queue_lag`、`concurrent_runs`、`token_burn_per_hour` 等关键观察指标

## Implementation Notes
- 成本控制不能以牺牲安全与审计为代价
- 降级顺序必须可解释，且优先保护高风险、高价值任务的完成质量
- 观测口径必须为项目管理、SRE 和评测同时服务，而不是只面向工程排障

## Blocking Conditions
- 三档预算无法映射到四种运行模式和五个 Story
- 10x / 100x 规划仍依赖单机、单索引或无限预算假设
- 没有统一的指标来源，导致延迟、成本、容量数据不可比
- 发布门禁或回归评测不能直接复用本主线指标

## Exit Criteria
- 预算、延迟、容量、告警和事故管理文档可以直接指导未来实现
- 质量评测和发布门禁都能引用本主线指标
- 10x / 100x 扩展路径具备明确分层拆分和观察阈值

## Acceptance Criteria
- 预算和降级顺序没有歧义
- 扩容、告警、值班和事故管理都有明确口径
