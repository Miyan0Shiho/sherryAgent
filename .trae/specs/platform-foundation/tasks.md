# Platform Foundation Tasks

## Implementation Sync 2026-04-08

- [x] `src/sherry_agent/models.py` 已实现 `Task / Run / Evidence / Decision / CostRecord / Plan / ToolCall / MemoryRecord / TriggerEvent / ReleaseGateResult`
- [x] `src/sherry_agent/settings.py` 已实现分层配置加载入口
- [x] `src/sherry_agent/storage.py` 与 `src/sherry_agent/task_service.py` 已实现 sqlite 持久化与恢复编排
- [x] foundation 相关测试与全量回归已通过，量化结果写入 `build/test-metrics.json`

## Phase 0: Alignment

### Work Packages
- [ ] P0-W1: 对齐 `docs/specs/core-data-contracts.md`、`docs/reference/glossary.md` 与本主线术语
- [ ] P0-W2: 列出所有下游主线会消费的核心对象、状态和治理字段
- [ ] P0-W3: 标记当前仍存在“实现者自行决定”的空白点

### Deliverables
- [ ] D0-1: foundation 输入清单
- [ ] D0-2: 术语冲突清单

### Blockers
- [ ] B0-1: `docs/*` 与 `.trae/specs/*` 中存在多套对象命名

## Phase 1: Core Object Freeze

### Work Packages
- [ ] P1-W1: 固定 `Task / Run / Evidence / Decision / Cost Record` 字段、字段含义和最小约束
- [ ] P1-W2: 固定统一状态机 `created -> planned -> running -> waiting_confirmation -> completed|blocked|failed|cancelled`
- [ ] P1-W3: 定义 Task 与 Run 的一对多关系，以及 Evidence / Decision / Cost Record 的归属关系
- [ ] P1-W4: 明确幂等键、关联键、最小索引字段和审计追踪字段

### Deliverables
- [ ] D1-1: 核心对象字段表
- [ ] D1-2: 统一状态机表
- [ ] D1-3: 对象关系说明

### Dependencies
- [ ] DEP1-1: `system-blueprint` 与 `core-operational-loops` 已冻结模块边界和主链路名称

### Blockers
- [ ] B1-1: 任一 Story 仍需要私有对象或私有状态

## Phase 2: Governance Freeze

### Work Packages
- [ ] P2-W1: 固定 `LOW / MEDIUM / HIGH / CRITICAL` 风险等级语义
- [ ] P2-W2: 固定确认流、阻断流、降级流的最小审计字段
- [ ] P2-W3: 定义哪些系统动作必须形成 `Decision`
- [ ] P2-W4: 固定 `strict / balanced / premium` 预算档位在 foundation 层的最小语义

### Deliverables
- [ ] D2-1: 风险分级表
- [ ] D2-2: 审计字段最小集合
- [ ] D2-3: Decision 生成规则

### Dependencies
- [ ] DEP2-1: `permission-system.md` 与 `quality-vs-latency-vs-cost.md` 已给出高层约束

### Blockers
- [ ] B2-1: 风险、预算和审计字段不能被下游主线直接复用

## Phase 3: Configuration & Lifecycle Freeze

### Work Packages
- [ ] P3-W1: 定义 `local / team / prod` 配置分层
- [ ] P3-W2: 定义配置优先级、变更边界和敏感配置处理原则
- [ ] P3-W3: 定义不同环境下的默认模式、预算姿态和权限姿态
- [ ] P3-W4: 定义任务、证据、审计、成本记录的生命周期与冷热分层
- [ ] P3-W5: 定义恢复时必须存在的最小上下文集合

### Deliverables
- [ ] D3-1: 配置分层说明
- [ ] D3-2: 生命周期与归档表
- [ ] D3-3: 恢复最小上下文要求

### Dependencies
- [ ] DEP3-1: `memory-knowledge` 与 `cost-latency-ops` 的扩展和容量约束已可引用

### Blockers
- [ ] B3-1: 生命周期规则仍然无法支撑 10x / 100x 规划

## Phase 4: Cross-Axis Adoption

### Work Packages
- [ ] P4-W1: 将核心对象和状态机回写到 `docs/specs/core-data-contracts.md`
- [ ] P4-W2: 检查 5 个 Story 是否都使用统一对象与状态机
- [ ] P4-W3: 确认其余 6 条主线没有引入冲突字段或私有状态机
- [ ] P4-W4: 形成 foundation 完成证明，供 `release-program` 作为 `G1 Foundation Gate` 输入

### Deliverables
- [ ] D4-1: 下游采用矩阵
- [ ] D4-2: foundation gate 通过说明
- [ ] D4-3: `docs/plans/gate-readiness-evidence.md` 中的 `G1 / platform-foundation` 证据段
