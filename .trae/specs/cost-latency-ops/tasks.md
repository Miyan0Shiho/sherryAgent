# Cost Latency Ops Tasks

## Phase 0: Operating Model Alignment

### Work Packages
- [ ] P0-W1: 对齐 `quality-vs-latency-vs-cost`、`scaling-strategy` 与本主线术语
- [ ] P0-W2: 识别四种运行模式与五个 Story 的默认成本姿态
- [ ] P0-W3: 列出最关键的成本失控、延迟失控和容量失控场景

### Deliverables
- [ ] D0-1: 运行模式成本地图
- [ ] D0-2: 失控场景清单

## Phase 1: Budget Policy Freeze

### Work Packages
- [ ] P1-W1: 固定 `strict / balanced / premium` 三档预算
- [ ] P1-W2: 固定模型路由、小模型优先与升级触发条件
- [ ] P1-W3: 固定 token、工具、缓存和长任务的成本记录方式
- [ ] P1-W4: 定义预算超限时的降级、暂停与人工介入规则

### Deliverables
- [ ] D1-1: 预算档位表
- [ ] D1-2: 成本记录模型

### Dependencies
- [ ] DEP1-1: `platform-foundation` 已冻结 `Cost Record` 与预算字段

## Phase 2: Performance Control Freeze

### Work Packages
- [ ] P2-W1: 定义 prompt / evidence / retrieval / decision cache 的命中条件
- [ ] P2-W2: 定义并发控制、队列限流和热点任务治理
- [ ] P2-W3: 定义延迟目标、P95 目标和异常阈值
- [ ] P2-W4: 定义先降并发、再降模型、再降深度、最后人工介入的降级顺序

### Deliverables
- [ ] D2-1: 缓存与限流规则
- [ ] D2-2: 延迟与降级矩阵

### Blockers
- [ ] B2-1: 降级顺序无法同时保护高风险任务质量与批量任务吞吐

## Phase 3: Scale & SRE Freeze

### Work Packages
- [ ] P3-W1: 定义 10x 下的单机多 worker 与持久化队列口径
- [ ] P3-W2: 定义 100x 下的独立伸缩、分片和冷热分层口径
- [ ] P3-W3: 固定 `tasks_per_min`、`queue_lag`、`token_burn_per_hour` 等容量指标
- [ ] P3-W4: 定义告警、值班、Sev 分级与升级路径
- [ ] P3-W5: 定义 run replay、cost dashboard、人工接管和回滚要求
- [ ] P3-W6: 定义异常成本上涨、缓存失效、队列堆积时的响应动作

### Deliverables
- [ ] D3-1: 10x / 100x 容量规划表
- [ ] D3-2: SRE 与事故响应规则

### Dependencies
- [ ] DEP3-1: `memory-knowledge`、`runtime-orchestration`、`tooling-integration` 已暴露关键事件点

## Phase 4: Evaluation Adoption

### Work Packages
- [ ] P4-W1: 为每个 Story 指定默认预算档位
- [ ] P4-W2: 为每个 Story 指定最关键的成本或延迟指标
- [ ] P4-W3: 确认 `quality-evaluation` 的结果指标可以直接消费该主线输出
- [ ] P4-W4: 形成运营主线完成证明，供 `G3 Governance Gate` 使用

### Deliverables
- [ ] D4-1: Story 成本与延迟矩阵
- [ ] D4-2: governance gate 输入说明
