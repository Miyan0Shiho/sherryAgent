# Runtime Orchestration Tasks

## Implementation Sync 2026-04-08

- [x] `src/sherry_agent/runtime.py` 已实现 `Interactive Dev Loop`
- [x] `src/sherry_agent/autonomous.py` 已实现 `Autonomous Background Loop` 与 `background-ops` 事故路径
- [x] `src/sherry_agent/bulk.py` 已实现 `Bulk Research / Analysis Loop`
- [x] `src/sherry_agent/governance.py` 已实现 `Repo / Release Governance Loop`
- [x] `src/sherry_agent/cli.py` 已暴露 `story01` 到 `story05` 的正式 CLI 入口

## Phase 0: Runtime Scope Alignment

### Work Packages
- [ ] P0-W1: 对齐 `core-operational-loops`、`runtime-modes` 与本主线术语
- [ ] P0-W2: 标出 4 条主链路的共性步骤与差异点
- [ ] P0-W3: 标出 Planner / Execution / Scheduler 当前仍模糊的职责边界

### Deliverables
- [ ] D0-1: 运行时范围清单
- [ ] D0-2: 职责冲突清单

## Phase 1: Loop Contract Freeze

### Work Packages
- [ ] P1-W1: 固定 `Interactive Dev Loop` 的输入、输出、状态与降级
- [ ] P1-W2: 固定 `Autonomous Background Loop` 的输入、输出、状态与降级
- [ ] P1-W3: 固定 `Bulk Research / Analysis Loop` 的输入、输出、状态与降级
- [ ] P1-W4: 固定 `Repo / Release Governance Loop` 的输入、输出、状态与降级
- [ ] P1-W5: 为每条主链路补齐触发条件、产出包和可观察字段

### Deliverables
- [ ] D1-1: 四条主链路契约表
- [ ] D1-2: 链路级失败与降级说明

### Dependencies
- [ ] DEP1-1: `platform-foundation` 已冻结核心对象与状态机

### Blockers
- [ ] B1-1: 任一链路仍依赖隐式实现假设

## Phase 2: Role Boundary Freeze

### Work Packages
- [ ] P2-W1: 固定 Planner 的输入、输出、模式选择、预算分配和路由责任
- [ ] P2-W2: 固定 Execution Engine 的执行、取消、超时、恢复和结果聚合责任
- [ ] P2-W3: 固定 Scheduler & Trigger 的触发、节流、去重、批处理责任
- [ ] P2-W4: 定义 Policy Gate 和 Review 在运行链路中的位置，避免职责漂移

### Deliverables
- [ ] D2-1: 角色边界矩阵
- [ ] D2-2: 责任归属说明

### Blockers
- [ ] B2-1: Planner、Execution、Scheduler 仍然能对同一类问题做重复裁决

## Phase 3: Failure & Recovery Freeze

### Work Packages
- [ ] P3-W1: 定义 `waiting_confirmation`、`blocked`、`failed` 的差异与迁移条件
- [ ] P3-W2: 定义工具失败、预算耗尽、上游数据缺失时的统一降级策略
- [ ] P3-W3: 定义模式切换、模型升级、计划重试何时允许发生
- [ ] P3-W4: 定义中断恢复、人工接管和重放的边界

### Deliverables
- [ ] D3-1: 失败分类表
- [ ] D3-2: 恢复与人工接管说明

### Dependencies
- [ ] DEP3-1: `tooling-integration`、`cost-latency-ops` 已给出失败类型与预算档位

## Phase 4: Acceptance Adoption

### Work Packages
- [ ] P4-W1: 确认 5 个 Story 与 4 条主链路映射一致
- [ ] P4-W2: 确认 Story 的输出契约能回映到 Runtime 对象和状态机
- [ ] P4-W3: 确认没有 Story 自定义一套私有控制流
- [ ] P4-W4: 形成运行时完成证明，供 `quality-evaluation` 和 `release-program` 复用

### Deliverables
- [ ] D4-1: Story-Loop 映射矩阵
- [ ] D4-2: runtime gate 通过说明
- [ ] D4-3: `docs/plans/gate-readiness-evidence.md` 中的 `G1 / runtime-orchestration` 证据段
