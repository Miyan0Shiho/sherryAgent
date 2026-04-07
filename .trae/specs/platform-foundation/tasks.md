# Platform Foundation Tasks

## Phase 1: 核心对象与状态机

- [ ] Task 1.1: 固定 `Task / Run / Evidence / Decision / Cost Record` 的字段、字段含义和最小约束
- [ ] Task 1.2: 固定统一状态机 `created -> planned -> running -> waiting_confirmation -> completed|blocked|failed|cancelled`
- [ ] Task 1.3: 定义 Task 与 Run 的一对多关系，以及 Evidence / Decision / Cost Record 的归属关系

## Phase 2: 风险、权限、审计基础

- [ ] Task 2.1: 固定 `LOW / MEDIUM / HIGH / CRITICAL` 风险等级的语义
- [ ] Task 2.2: 固定确认流、阻断流、降级流的最小审计字段
- [ ] Task 2.3: 定义哪些系统动作必须形成 `Decision`

## Phase 3: 配置与环境分层

- [ ] Task 3.1: 定义 `local / team / prod` 配置分层
- [ ] Task 3.2: 定义配置优先级、变更边界和敏感配置处理原则
- [ ] Task 3.3: 定义不同环境下的默认模式、预算姿态和权限姿态

## Phase 4: 存储与生命周期

- [ ] Task 4.1: 定义任务、证据、审计、成本记录的生命周期
- [ ] Task 4.2: 定义热数据、温数据、冷归档的分层口径
- [ ] Task 4.3: 定义恢复时必须存在的最小上下文集合

## Phase 5: 验收整合

- [ ] Task 5.1: 将核心对象和状态机回写到 `docs/specs/core-data-contracts.md`
- [ ] Task 5.2: 检查 5 个 Story 是否都使用统一对象与状态机
- [ ] Task 5.3: 确认其余 6 条主线没有引入冲突字段或私有状态机

