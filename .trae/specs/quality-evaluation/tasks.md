# Quality Evaluation Tasks

## Phase 0: Evaluation Scope Alignment

### Work Packages
- [ ] P0-W1: 对齐 `technical-metrics`、`business-metrics`、Story 文档与本主线术语
- [ ] P0-W2: 汇总当前所有主线需要被验证的能力点、风险点和成本点
- [ ] P0-W3: 明确默认 baseline 是“裸奔模式”，并写死不可漂移

### Deliverables
- [ ] D0-1: 评测范围清单
- [ ] D0-2: baseline 说明

## Phase 1: Evaluation Taxonomy Freeze

### Work Packages
- [ ] P1-W1: 固定 `Capability Benchmark` 的目标、输入和输出
- [ ] P1-W2: 固定 `Story Acceptance` 的验收方式，并与 5 个 Story 一一映射
- [ ] P1-W3: 固定 `Regression Suite` 的样本类型与维护规则
- [ ] P1-W4: 固定 `Load & Scale Test` 的规模维度与观察指标
- [ ] P1-W5: 固定 `Safety Evaluation` 的误放行、误拦截、越权处理口径
- [ ] P1-W6: 固定 `Cost / Latency Benchmark` 的比较方式

### Deliverables
- [ ] D1-1: 六类评测层级表
- [ ] D1-2: Story-评测映射矩阵

### Dependencies
- [ ] DEP1-1: `runtime-orchestration`、`cost-latency-ops`、`tooling-integration` 已冻结核心输入口径

## Phase 2: Metrics & Reporting Freeze

### Work Packages
- [ ] P2-W1: 定义成功率、部分成功率、误判率、危险操作拦截率
- [ ] P2-W2: 定义单位成本、P50/P95 延迟、人工介入率
- [ ] P2-W3: 定义 baseline vs current 的统一结果模板
- [ ] P2-W4: 定义评测结果如何映射到项目 gate 与发布门禁

### Deliverables
- [ ] D2-1: 结果模板
- [ ] D2-2: 质量阻断规则

### Blockers
- [ ] B2-1: 结果模板无法同时解释质量、成本和风险取舍

## Phase 3: Corpus Governance Freeze

### Work Packages
- [ ] P3-W1: 定义 `golden tasks` 的来源、更新规则、失效规则
- [ ] P3-W2: 定义 `failure corpus` 的纳入标准与归档规则
- [ ] P3-W3: 定义 `policy regression cases` 的维护边界
- [ ] P3-W4: 定义每次计划或实现变更必须更新哪类评测资产

### Deliverables
- [ ] D3-1: 回归资产治理规则
- [ ] D3-2: 变更到评测资产更新矩阵

## Phase 4: Story Adoption

### Work Packages
- [ ] P4-W1: 为 5 个 Story 分别指定主验收层与辅助评测层
- [ ] P4-W2: 为每个 Story 指定必须覆盖的失败模式样本
- [ ] P4-W3: 为每个 Story 指定最低可接受质量、成本和风险表现
- [ ] P4-W4: 形成质量主线完成证明，供 `G3 Governance Gate` 使用

### Deliverables
- [ ] D4-1: Story 质量门槛矩阵
- [ ] D4-2: governance gate 输入说明
- [ ] D4-3: `docs/plans/gate-readiness-evidence.md` 中的 `G3 / quality-evaluation` 证据段
