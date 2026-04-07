# Platform Foundation Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G1 Foundation Gate`
- [ ] 本主线交付物已同步到 `docs/specs/core-data-contracts.md` 与相关上游文档

## Entry Criteria

- [ ] `platform-foundation/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `platform-foundation/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] `docs/reference/glossary.md` 与 foundation 术语一致

## Pass Criteria

### Core Object Gate
- [ ] `Task / Run / Evidence / Decision / Cost Record` 已具备统一字段定义
- [ ] 对象关系、幂等键、关联键、最小索引字段已定稿

### State & Governance Gate
- [ ] 平台状态机已统一，未出现平行状态机口径
- [ ] 风险等级、确认流、阻断流、降级流已有明确文字约束
- [ ] `Decision` 生成条件与审计字段已定稿
- [ ] `strict / balanced / premium` 的 foundation 层语义已定稿

### Configuration & Lifecycle Gate
- [ ] `local / team / prod` 配置分层已定稿
- [ ] 生命周期与冷热分层口径已定稿
- [ ] 恢复时必须存在的最小上下文集合已定稿

### Cross-Axis Adoption Gate
- [ ] 5 个 Story 与其余 6 条主线均引用同一套基础对象
- [ ] 下游主线未引入私有字段或私有状态机
- [ ] foundation 完成证明已准备好供 `release-program` 消费

## Blocking Conditions

- [ ] `docs/*` 与 `.trae/specs/*` 中仍存在多套对象命名
- [ ] 任一 Story 仍依赖私有对象或私有状态
- [ ] 风险、预算、审计字段不能被下游主线直接复用
- [ ] 生命周期规则无法支撑 10x / 100x 规划

## Handoff

- [ ] `runtime-orchestration` 已确认可直接消费 foundation 对象与状态机
- [ ] `memory-knowledge`、`tooling-integration`、`cost-latency-ops` 已确认可直接消费 foundation 治理字段
- [ ] 该主线可作为 `G1 Foundation Gate` 正式输入
