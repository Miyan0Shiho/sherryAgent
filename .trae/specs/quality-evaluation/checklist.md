# Quality Evaluation Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G3 Governance Gate`
- [ ] 本主线交付物已同步到 Story 套件、技术指标和业务指标文档

## Entry Criteria

- [ ] `quality-evaluation/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `quality-evaluation/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] `runtime-orchestration`、`tooling-integration`、`memory-knowledge`、`cost-latency-ops` 已提供正式输入口径

## Pass Criteria

### Taxonomy Gate
- [ ] 六类评测都具备明确目标、输入与输出
- [ ] Story 与评测层级映射已定稿

### Baseline & Reporting Gate
- [ ] baseline vs current 的统一对比口径已定稿
- [ ] 结果模板能同时表达质量、成本和风险表现
- [ ] 评测结果到 gate / 发布门禁的映射已定稿

### Corpus Governance Gate
- [ ] `golden tasks` / `failure corpus` / `policy regression cases` 已有维护规则
- [ ] 每次计划或实现变更必须更新哪类评测资产已定稿

### Governance Adoption Gate
- [ ] 5 个 Story 与评测层级映射已定稿
- [ ] 每个 Story 的最低可接受质量、成本和风险表现已定稿
- [ ] 评测失败阻断规则已定稿
- [ ] 该主线完成证明已准备好供 `G3 Governance Gate` 使用
- [ ] `gate-readiness-evidence.md` 已给出 `quality-evaluation` 对 `G3` 的正式证据

## Blocking Conditions

- [ ] baseline 不清晰，导致优化前后不可比
- [ ] 结果模板无法解释质量、成本和风险之间的取舍
- [ ] 缺乏固定 failure corpus，事故经验无法沉淀
- [ ] 发布门禁无法直接消费质量结果

## Handoff

- [ ] `release-program` 已确认可直接消费质量门禁和阻断规则
- [ ] Story 套件已确认可直接消费本主线的最低通过门槛
- [ ] 该主线可作为 `G3 Governance Gate` 正式输入
