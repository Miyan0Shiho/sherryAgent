# Cost Latency Ops Tasks

## Phase 1: 成本与预算

- [ ] Task 1.1: 固定 `strict / balanced / premium` 三档预算
- [ ] Task 1.2: 固定模型路由、小模型优先与升级触发条件
- [ ] Task 1.3: 固定 token、工具、缓存和长任务的成本记录方式

## Phase 2: 性能与缓存

- [ ] Task 2.1: 定义 prompt / evidence / retrieval / decision cache 的命中条件
- [ ] Task 2.2: 定义并发控制、队列限流和热点任务治理
- [ ] Task 2.3: 定义延迟目标、P95 目标和异常阈值

## Phase 3: 扩容与容量规划

- [ ] Task 3.1: 定义 10x 下的单机多 worker 与持久化队列口径
- [ ] Task 3.2: 定义 100x 下的独立伸缩、分片和冷热分层口径
- [ ] Task 3.3: 固定 `tasks_per_min`、`queue_lag`、`token_burn_per_hour` 等容量指标

## Phase 4: 运行与 SRE

- [ ] Task 4.1: 定义告警、值班、Sev 分级与升级路径
- [ ] Task 4.2: 定义 run replay、cost dashboard、人工接管和回滚要求
- [ ] Task 4.3: 定义异常成本上涨、缓存失效、队列堆积时的响应动作

## Phase 5: Story / Evaluation 对齐

- [ ] Task 5.1: 为每个 Story 指定默认预算档位
- [ ] Task 5.2: 为每个 Story 指定最关键的成本或延迟指标
- [ ] Task 5.3: 确认 Quality Evaluation 的结果指标可以直接消费该主线输出

