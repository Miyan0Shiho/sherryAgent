# Runtime Orchestration Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G1 Foundation Gate`
- [ ] 本主线交付物已同步到 `docs/architecture/core-operational-loops.md`、`docs/specs/agent-loop.md` 与相关运行时文档

## Entry Criteria

- [ ] `runtime-orchestration/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `runtime-orchestration/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] `platform-foundation` 已冻结核心对象与状态机

## Pass Criteria

### Loop Contract Gate
- [ ] 四条主链路都具备输入、输出、状态与降级定义
- [ ] 每条主链路都具备触发条件、产出包和可观察字段

### Role Boundary Gate
- [ ] Planner / Execution / Scheduler 边界无重叠歧义
- [ ] Policy Gate 与 Review 在运行链路中的位置已定稿

### Failure & Recovery Gate
- [ ] `waiting_confirmation` / `blocked` / `failed` 差异已定稿
- [ ] 模式切换、模型升级、预算中断有统一口径
- [ ] 中断恢复、人工接管和重放边界已定稿

### Acceptance Adoption Gate
- [ ] 5 个 Story 的主链路映射与 Runtime 口径一致
- [ ] Story 输出契约能回映到 Runtime 对象和状态机
- [ ] runtime 完成证明已准备好供 `quality-evaluation` 与 `release-program` 消费
- [ ] `gate-readiness-evidence.md` 已给出 `runtime-orchestration` 对 `G1` 的正式证据

## Blocking Conditions

- [ ] 任一链路仍依赖隐式实现假设
- [ ] Planner、Execution、Scheduler 仍会对同一类问题做重复裁决
- [ ] 运行模式与链路模板冲突
- [ ] Story 仍定义私有控制流

## Handoff

- [ ] `quality-evaluation` 已确认可基于本主线建立 benchmark 与 Story 验收
- [ ] `cost-latency-ops` 已确认可基于本主线提取关键延迟点和降级点
- [ ] 该主线可作为 `G1 Foundation Gate` 正式输入
