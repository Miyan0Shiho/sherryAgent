# Memory Knowledge Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G2 Capability Gate`
- [ ] 本主线交付物已同步到 `docs/specs/memory-system.md` 与 `docs/architecture/scaling-strategy.md`

## Entry Criteria

- [ ] `memory-knowledge/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `memory-knowledge/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] `platform-foundation` 与 `runtime-orchestration` 已冻结 Evidence 生命周期和检索触发点

## Pass Criteria

### Memory Boundary Gate
- [ ] 记忆四层职责已定稿
- [ ] Evidence 与记忆关系已定稿
- [ ] 长期保留与短暂缓存边界已定稿

### Retrieval & Compression Gate
- [ ] 混合检索、压缩、TTL、裁剪策略已定稿
- [ ] 引用格式、置信度和过时信息剔除策略已定稿

### Scale Gate
- [ ] 10x / 100x 扩容口径已定稿
- [ ] 多租户、多仓库、多数据集隔离边界已定稿
- [ ] 知识版本化、过期、替换和回溯原则已定稿

### Evaluation Adoption Gate
- [ ] Story 与评测对记忆的要求可回映到该主线
- [ ] 检索质量指标可直接进入 `quality-evaluation`
- [ ] 该主线完成证明已准备好供 `G2 Capability Gate` 使用
- [ ] `gate-readiness-evidence.md` 已给出 `memory-knowledge` 对 `G2` 的正式证据

## Blocking Conditions

- [ ] 检索与压缩规则无法同时解释上下文爆炸和证据可追溯性
- [ ] 10x / 100x 仍依赖单一索引或全量扫描假设
- [ ] Story 或评测无法从本主线提取记忆指标

## Handoff

- [ ] `quality-evaluation` 已确认可消费检索与记忆指标
- [ ] `cost-latency-ops` 已确认可消费容量和缓存相关输入
- [ ] 该主线可作为 `G2 Capability Gate` 正式输入
