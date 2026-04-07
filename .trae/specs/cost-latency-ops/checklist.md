# Cost Latency Ops Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G3 Governance Gate`
- [ ] 本主线交付物已同步到 `quality-vs-latency-vs-cost.md`、`scaling-strategy.md` 与相关运维口径文档

## Entry Criteria

- [ ] `cost-latency-ops/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `cost-latency-ops/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] `platform-foundation`、`runtime-orchestration`、`tooling-integration`、`memory-knowledge` 已提供成本与容量输入

## Pass Criteria

### Budget Gate
- [ ] 预算档位已定稿
- [ ] 成本记录模型已定稿
- [ ] 预算超限时的降级、暂停与人工介入规则已定稿

### Performance Control Gate
- [ ] 模型路由、缓存、限流、降级策略已定稿
- [ ] 延迟目标、P95 目标和异常阈值已定稿
- [ ] 降级顺序能够同时保护高风险任务质量与批量任务吞吐

### Scale & SRE Gate
- [ ] 10x / 100x 扩容口径已定稿
- [ ] 容量与告警指标已定稿
- [ ] run replay、cost dashboard、人工接管和回滚要求已定稿

### Governance Adoption Gate
- [ ] Story 默认预算和评测消费关系已定稿
- [ ] `quality-evaluation` 可直接消费本主线成本、延迟和容量指标
- [ ] 该主线完成证明已准备好供 `G3 Governance Gate` 使用

## Blocking Conditions

- [ ] 三档预算无法映射到四种运行模式和五个 Story
- [ ] 降级顺序无法解释质量优先与吞吐优先的切换
- [ ] 10x / 100x 仍依赖单机、单索引或无限预算假设
- [ ] 发布门禁无法直接消费本主线指标

## Handoff

- [ ] `quality-evaluation` 已确认可消费成本、延迟和容量 benchmark 指标
- [ ] `release-program` 已确认可消费 SRE、预算和扩容门禁
- [ ] 该主线可作为 `G3 Governance Gate` 正式输入
