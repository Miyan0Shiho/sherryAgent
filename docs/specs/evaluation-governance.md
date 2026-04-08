---
title: "Evaluation Governance"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../plans/story-gate-matrix.md"
  - "../reference/technical-metrics.md"
  - "../reference/business-metrics.md"
---

# Evaluation Governance

## 六类评测层级

| 层级 | 目标 | 主要输入 | 主要输出 |
|------|------|----------|----------|
| `Capability Benchmark` | 比较能力变化 | golden tasks, 标准输入集 | 成功率、部分成功率、质量差异 |
| `Story Acceptance` | 验证业务闭环 | 5 个 Story 场景 | 是否达到 Story 最低通过线 |
| `Regression Suite` | 防止旧问题回归 | failure corpus, incident cases | 回归通过/失败 |
| `Load & Scale Test` | 验证规模与吞吐 | 批量任务、并发模型 | 吞吐、P95、容量压力 |
| `Safety Evaluation` | 验证误放行/误拦截 | policy regression cases | 危险操作拦截率、误拦截率 |
| `Cost / Latency Benchmark` | 比较成本与时延 | baseline/current 运行包 | 单位成本、P50/P95、人工介入率 |

## Baseline 规则

- 默认 `baseline` 是“当前冻结契约下的最保守可接受方案”，不是临时挑一个好看的历史版本。
- `current` 必须与 `baseline` 使用相同 Story、相同输入集、相同度量模板。
- 任何更换基线的行为都必须形成文档化 `Decision`，并说明为什么旧基线失效。

## 结果模板

每次正式评测至少输出：

- 质量结果：成功率、部分成功率、关键失败模式覆盖
- 风险结果：危险动作拦截率、误拦截率、确认流命中情况
- 成本结果：`cost_per_run`, `token_burn_per_hour`, `cache_hit_rate`
- 时延结果：`run_completion_latency_ms`, `retrieval_p95_ms`, `approval_wait_time_p95_ms`
- 治理结论：是否阻断 gate、是否需要人工复核

## Corpus 治理

- `golden tasks`：代表正常目标能力，需求变化时更新
- `failure corpus`：代表历史缺陷、事故、边界失败，修复后不得删除其防回归价值
- `policy regression cases`：代表越权、误放行、误拦截、高风险确认路径

每次计划或契约变更至少要回答：

- 是否新增或淘汰 golden task
- 是否新增 failure corpus
- 是否新增 policy regression case
- 是否改变 Story 最低通过线

## Gate 映射

- `G1`：主要消费 Story 对统一对象、状态机和主链路的验证
- `G2`：主要消费记忆、工具、权限治理的能力验证
- `G3`：主要消费 baseline/current、回归、成本与风险结果
- `G4`：主要消费前 3 个 gate 的汇总结论，以及 Story 正式通过记录

## Story 最低通过线

- `Story-01`：必须通过 `Story Acceptance`、`Safety Evaluation`、`Cost / Latency Benchmark`
- `Story-02`：必须通过 `Story Acceptance`、`Safety Evaluation`
- `Story-03`：必须通过 `Story Acceptance`、`Regression Suite`、`Safety Evaluation`
- `Story-04`：必须通过 `Story Acceptance`、`Load & Scale Test`
- `Story-05`：必须通过 `Story Acceptance`、`Regression Suite`、`Safety Evaluation`、`Cost / Latency Benchmark`

任一 Story 未达到最低通过线时，不得宣称对应 gate 已完整通过。
