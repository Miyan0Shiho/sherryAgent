# SherryAgent - Tooling Integration Spec

## Overview
- **Summary**: 定义工具协议、MCP/CLI/API 接入、隔离、重试、幂等和外部依赖治理。
- **Purpose**: 保证工具使用既可扩展又可审计，不因集成复杂度破坏平台稳定性。
- **Primary Owners**: 工具平台、外部集成、执行治理与安全接入负责人。

## Goals
- 固定工具调用最小契约
- 固定本地工具、远程工具、外部 API 的接入边界
- 固定幂等、超时、重试、隔离的治理要求

## Non-Goals
- 不编写具体工具实现

## Inputs
- `platform-foundation` 提供的权限、审计、幂等、风险等级和预算约束
- `runtime-orchestration` 提供的工具调用时机与失败恢复模板
- `docs/specs/permission-system.md`、`docs/specs/agent-loop.md` 中的工具执行原则
- `docs/architecture/module-map.md` 中 `Policy & Guardrail` 与 `Execution Engine` 的职责边界

## Outputs
- 工具最小接入契约与元数据要求
- 本地 CLI、MCP、HTTP/API 三类工具的接入边界与隔离口径
- 超时、重试、幂等、回放、模拟运行和错误分类规范
- 供安全、评测、成本和发布主线复用的工具治理基线
- `G2 Capability Gate` 的正式输入证明

## Dependencies
### Upstream
- `platform-foundation`：提供权限、预算、审计和对象关联语义
- `runtime-orchestration`：定义工具在各主链路中的触发与恢复点

### Downstream
- `quality-evaluation` 依赖本主线定义工具使用 benchmark、故障注入和越权回归
- `cost-latency-ops` 依赖本主线计算工具调用开销、缓存命中与限流策略
- `release-program` 依赖本主线判断哪些外部依赖属于上线门禁

## Milestones
### M1: Tool Contract Freeze
- 固定工具描述字段、输入输出边界、风险标签和审计字段
- 明确工具必须声明的超时、幂等、可重试性和副作用等级

### M2: Integration Boundary Freeze
- 固定 CLI、MCP、HTTP/API 三类接入模型
- 明确每类工具的鉴权、隔离、回放和失败分类规则

### M3: Governance Freeze
- 固定重试、熔断、模拟运行、人工确认和降级策略
- 明确高风险工具和低风险工具的审批差异

### M4: Evaluation & Release Gate
- 工具接入规范被 Story 套件、评测层级和发布门禁共同复用
- 不再允许用“临时脚本/临时接口”绕过统一治理

## Implementation Notes
- 工具协议必须优先解决“能否安全调用”和“能否稳定回放”，其次才是接入速度
- 任何外部依赖都必须被视为潜在不稳定源，不能把成功调用当成默认前提
- 同一类工具的风险与预算口径必须可比较，避免不同接入方式各自定义语义

## Blocking Conditions
- 工具元数据不足以支持权限审计、评测和成本核算
- MCP/CLI/API 接入方式仍然与运行时、策略层强耦合
- 幂等、超时、重试和回放规则不能覆盖后台任务与发布治理场景
- Story 验收无法指出工具失败时的预期降级路径

## Exit Criteria
- 三类接入方式都具备统一治理口径
- 工具风险、成本、重试和审计可以直接映射到 4 条主链路
- 未来新增工具无需修改顶层架构，只需满足本主线契约

## Acceptance Criteria
- 工具接入和执行风险有统一口径
- MCP/CLI/API 接入方式不会把策略和执行混杂
