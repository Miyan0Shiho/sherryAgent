# Tooling Integration Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G2 Capability Gate`
- [ ] 本主线交付物已同步到 `docs/specs/permission-system.md`、`docs/specs/agent-loop.md` 与相关工具治理文档

## Entry Criteria

- [ ] `tooling-integration/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `tooling-integration/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] `platform-foundation` 与 `runtime-orchestration` 已冻结审计字段和失败恢复模板

## Pass Criteria

### Tool Contract Gate
- [ ] 工具最小契约已定稿
- [ ] 工具分类已定稿
- [ ] 工具元数据中的超时、幂等、重试和副作用声明已定稿

### Integration Boundary Gate
- [ ] 本地/MCP/API 接入边界已定稿
- [ ] 工具调用与业务决策的责任分离已定稿
- [ ] 鉴权、隔离、回放、模拟运行和凭证边界已定稿

### Reliability & Governance Gate
- [ ] 幂等、超时、重试、隔离策略已定稿
- [ ] 高风险工具默认确认条件已定稿
- [ ] 故障降级、回退和证据输出路径已定稿

### Acceptance Adoption Gate
- [ ] 高风险工具路径均受 Policy & Guardrail 约束
- [ ] 5 个 Story 中的工具动作可落入统一分类
- [ ] 该主线完成证明已准备好供 `quality-evaluation` 与 `release-program` 消费

## Blocking Conditions

- [ ] 任一接入方式仍把策略判断和执行混在一起
- [ ] 工具元数据不足以支撑权限审计、评测和成本核算
- [ ] Story 工具路径仍存在绕过审计或确认的情况

## Handoff

- [ ] `quality-evaluation` 已确认可基于本主线建立工具故障注入与越权回归
- [ ] `cost-latency-ops` 已确认可消费工具成本和失败模式输入
- [ ] 该主线可作为 `G2 Capability Gate` 正式输入
