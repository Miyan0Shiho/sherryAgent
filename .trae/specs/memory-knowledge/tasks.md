# Memory Knowledge Tasks

## Implementation Sync 2026-04-08

- [x] `src/sherry_agent/memory.py` 已实现基于 sqlite 的写入、检索、压缩、TTL 清理
- [x] `MemoryRecord` 已支持 scope、version、TTL、summary 压缩与 evidence 回链字段
- [x] `Story-02/03/04/05` 已接入 session memory 或 release memory 写入

## Phase 0: Knowledge Scope Alignment

### Work Packages
- [ ] P0-W1: 对齐 `memory-system.md`、`core-data-contracts.md`、`scaling-strategy.md` 与本主线术语
- [ ] P0-W2: 列出 4 条主链路的记忆读取、写入、压缩和归档需求
- [ ] P0-W3: 列出当前最容易被误当作长期知识的高风险信息类型

### Deliverables
- [ ] D0-1: 记忆范围说明
- [ ] D0-2: 高风险知识类型清单

## Phase 1: Memory Boundary Freeze

### Work Packages
- [ ] P1-W1: 定义短期上下文、工作记忆、长期记忆、冷归档四层职责
- [ ] P1-W2: 定义 Evidence 与记忆的关系，避免把未验证文本直接当长期知识
- [ ] P1-W3: 定义记忆写入与检索的最小审计要求
- [ ] P1-W4: 明确哪些信息只允许短暂缓存，哪些可以进入长期保留

### Deliverables
- [ ] D1-1: 四层记忆边界表
- [ ] D1-2: Evidence 到记忆的准入规则

### Dependencies
- [ ] DEP1-1: `platform-foundation` 已冻结 Evidence 生命周期和审计字段

## Phase 2: Retrieval & Compression Freeze

### Work Packages
- [ ] P2-W1: 定义混合检索原则（关键词、结构过滤、向量召回）
- [ ] P2-W2: 定义压缩、去重、TTL、上下文裁剪的触发条件
- [ ] P2-W3: 定义检索结果进入上下文前的预算裁剪规则
- [ ] P2-W4: 定义引用格式、置信度和过时信息剔除策略

### Deliverables
- [ ] D2-1: 检索与压缩规则表
- [ ] D2-2: 引用与置信度说明

### Blockers
- [ ] B2-1: 检索和压缩规则无法解释上下文爆炸与证据可追溯性的冲突

## Phase 3: Lifecycle & Scale Freeze

### Work Packages
- [ ] P3-W1: 定义 10x 规模下的独立索引层和热点缓存口径
- [ ] P3-W2: 定义 100x 规模下的分片、冷热分层和异步归档口径
- [ ] P3-W3: 定义知识版本化、过期、替换和回溯原则
- [ ] P3-W4: 定义多租户、多仓库、多数据集场景下的隔离边界

### Deliverables
- [ ] D3-1: 10x / 100x 扩展矩阵
- [ ] D3-2: 知识演化与回溯规则

### Dependencies
- [ ] DEP3-1: `cost-latency-ops` 已给出容量观察指标

## Phase 4: Evaluation Adoption

### Work Packages
- [ ] P4-W1: 确认 Story-01/03/04/05 的 Evidence 需求可以由该主线支撑
- [ ] P4-W2: 确认检索质量指标能进入 `quality-evaluation` 主线
- [ ] P4-W3: 确认扩容指标与 `scaling-strategy` 一致
- [ ] P4-W4: 形成记忆主线完成证明，供 `G2 Capability Gate` 使用

### Deliverables
- [ ] D4-1: Story-Memory 映射矩阵
- [ ] D4-2: capability gate 输入说明
- [ ] D4-3: `docs/plans/gate-readiness-evidence.md` 中的 `G2 / memory-knowledge` 证据段
