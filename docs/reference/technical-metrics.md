---
title: "系统技术指标"
status: approved
created: 2026-04-07
updated: 2026-04-07
related:
  - "../architecture/scaling-strategy.md"
  - "../specs/observability-system.md"
  - "./business-metrics.md"
---

# 系统技术指标

本文档定义平台级技术指标，服务性能优化、容量规划、故障诊断和成本治理。

## 一级指标组

### 延迟

- `time_to_first_response_ms`
- `run_completion_latency_ms`
- `retrieval_p95_ms`
- `approval_wait_time_p95_ms`

### 吞吐

- `tasks_per_min`
- `runs_per_min`
- `evidence_ingest_rate`
- `reports_generated_per_hour`

### 可靠性

- `run_failure_rate`
- `recovery_success_rate`
- `policy_evaluation_error_rate`
- `scheduler_trigger_success_rate`

### 成本

- `token_burn_per_hour`
- `cost_per_run`
- `cache_hit_rate`
- `model_upgrade_rate`

### 资源与扩容

- `queue_lag`
- `concurrent_runs`
- `evidence_growth_rate`
- `storage_hotset_size`
- `index_query_p95_ms`

### 治理

- `policy_block_rate`
- `dangerous_action_allow_rate`
- `decision_replay_coverage`
- `run_replay_availability`

## 指标与模块映射

| 模块 | 关键指标 |
|------|------|
| Gateway | `time_to_first_response_ms`, `request_normalization_failures` |
| Task Service | `queue_lag`, `task_state_transition_errors` |
| Planner | `planning_latency_ms`, `model_upgrade_rate` |
| Execution Engine | `run_completion_latency_ms`, `run_failure_rate` |
| Memory & Retrieval | `retrieval_p95_ms`, `evidence_growth_rate`, `cache_hit_rate` |
| Policy & Guardrail | `policy_block_rate`, `approval_wait_time_p95_ms` |
| Scheduler & Trigger | `scheduler_trigger_success_rate`, `trigger_drop_rate` |
| Observability & Evaluation | `decision_replay_coverage`, `run_replay_availability` |
| Cost & Capacity Controller | `token_burn_per_hour`, `cost_per_run`, `queue_lag` |
| Release & Ops | `release_gate_pass_rate`, `rollback_invocation_rate` |

## 默认关注阈值

| 指标 | 默认关注线 |
|------|------|
| `queue_lag` | 持续上升即告警 |
| `retrieval_p95_ms` | 超过目标 SLA 即告警 |
| `token_burn_per_hour` | 超预算趋势即告警 |
| `policy_block_rate` | 异常升高需检查误拦截 |
| `run_failure_rate` | 持续升高需进入回归分析 |

## 与评测的关系

- 技术指标描述运行健康度。
- 评测指标描述能力变化与正确性。
- 两者必须联动看，不能只看吞吐和延迟就判断平台“更好”。

