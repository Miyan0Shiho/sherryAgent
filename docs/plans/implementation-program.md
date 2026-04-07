---
title: "Implementation Program"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/product-charter.md"
  - "../architecture/system-blueprint.md"
---

# Implementation Program

## 计划主轴

SherryAgent 的实现计划按 7 条主线推进：

1. `platform-foundation`
2. `runtime-orchestration`
3. `memory-knowledge`
4. `tooling-integration`
5. `quality-evaluation`
6. `cost-latency-ops`
7. `release-program`

## 分阶段推进

### Phase 1: 平台基础定稿

- 固定 Task / Run / Evidence / Decision / Cost Record 数据对象
- 固定统一状态机、模式、预算档位、风险分级
- 固定入口、执行、策略、审计、成本之间的边界

### Phase 2: 四条主链路定稿

- Interactive Dev Loop
- Autonomous Background Loop
- Bulk Research / Analysis Loop
- Repo / Release Governance Loop

每条链路都必须具备：
- 输入/输出契约
- 状态机
- 失败降级
- 可观察字段

### Phase 3: 评测与回归体系定稿

- Capability Benchmark
- Story Acceptance
- Regression Suite
- Load & Scale Test
- Safety Evaluation
- Cost / Latency Benchmark

### Phase 4: 成本、性能、扩展与运营策略定稿

- 预算、缓存、限流、fallback
- 10x / 100x 扩容
- 配置、值班、回滚、事故管理

## 交付门禁

- 顶层文档不再以 `phoenix` 或 `mvp-*` 为主轴
- 7 条一级计划轴都具备 `spec/tasks/checklist`
- 4 条主链路、5 类以上评测、3 档预算策略、10x/100x 扩容口径均已定稿
- Story 明确标记为验收与演示套件

