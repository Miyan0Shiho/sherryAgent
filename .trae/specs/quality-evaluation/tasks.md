# Quality Evaluation Tasks

## Phase 1: 评测层级定稿

- [ ] Task 1.1: 固定 `Capability Benchmark` 的目标、输入和输出
- [ ] Task 1.2: 固定 `Story Acceptance` 的验收方式，并与 5 个 Story 一一映射
- [ ] Task 1.3: 固定 `Regression Suite` 的样本类型与维护规则
- [ ] Task 1.4: 固定 `Load & Scale Test` 的规模维度与观察指标
- [ ] Task 1.5: 固定 `Safety Evaluation` 的误放行、误拦截、越权处理口径
- [ ] Task 1.6: 固定 `Cost / Latency Benchmark` 的比较方式

## Phase 2: 结果指标与输出模板

- [ ] Task 2.1: 定义成功率、部分成功率、误判率、危险操作拦截率
- [ ] Task 2.2: 定义单位成本、P50/P95 延迟、人工介入率
- [ ] Task 2.3: 定义 baseline vs current 的统一结果模板

## Phase 3: 回归资产治理

- [ ] Task 3.1: 定义 `golden tasks` 的来源、更新规则、失效规则
- [ ] Task 3.2: 定义 `failure corpus` 的纳入标准与归档规则
- [ ] Task 3.3: 定义 `policy regression cases` 的维护边界

## Phase 4: Story 套件正式接入

- [ ] Task 4.1: 为 5 个 Story 分别指定主验收层与辅助评测层
- [ ] Task 4.2: 为每个 Story 指定必须覆盖的失败模式样本
- [ ] Task 4.3: 为每个 Story 指定最低可接受质量、成本和风险表现

## Phase 5: 交付门禁

- [ ] Task 5.1: 定义“能力提升”何时可视为真实提升而非成本堆叠
- [ ] Task 5.2: 定义哪些改动必须更新 benchmark / regression case
- [ ] Task 5.3: 定义评测失败时的阻断规则

