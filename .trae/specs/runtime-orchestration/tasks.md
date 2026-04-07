# Runtime Orchestration Tasks

## Phase 1: 四条主链路定稿

- [ ] Task 1.1: 固定 `Interactive Dev Loop` 的输入、输出、状态与降级
- [ ] Task 1.2: 固定 `Autonomous Background Loop` 的输入、输出、状态与降级
- [ ] Task 1.3: 固定 `Bulk Research / Analysis Loop` 的输入、输出、状态与降级
- [ ] Task 1.4: 固定 `Repo / Release Governance Loop` 的输入、输出、状态与降级

## Phase 2: Planner / Execution / Scheduler 边界

- [ ] Task 2.1: 固定 Planner 的输入、输出、模式选择、预算分配和路由责任
- [ ] Task 2.2: 固定 Execution Engine 的执行、取消、超时、恢复和结果聚合责任
- [ ] Task 2.3: 固定 Scheduler & Trigger 的触发、节流、去重、批处理责任

## Phase 3: 运行时控制流

- [ ] Task 3.1: 定义 `waiting_confirmation`、`blocked`、`failed` 的差异与迁移条件
- [ ] Task 3.2: 定义工具失败、预算耗尽、上游数据缺失时的统一降级策略
- [ ] Task 3.3: 定义模式切换、模型升级、计划重试何时允许发生

## Phase 4: Story 对齐

- [ ] Task 4.1: 确认 5 个 Story 与 4 条主链路映射一致
- [ ] Task 4.2: 确认 Story 的输出契约能回映到 Runtime 对象和状态机
- [ ] Task 4.3: 确认没有 Story 自定义一套私有控制流

