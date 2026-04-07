---
title: "业务指标"
status: approved
created: 2026-04-07
updated: 2026-04-07
related:
  - "./technical-metrics.md"
  - "../vision/product-charter.md"
  - "../plans/implementation-program.md"
---

# 业务指标

本文档定义公司级 SherryAgent 平台的业务指标，用于衡量平台是否真正服务团队、多仓库和多工作负载，而不是只看单点功能是否“能跑”。

## 一级目标

### 1. 平台采用度

- `active_teams`
- `active_repos`
- `weekly_active_users`
- `story_acceptance_usage_rate`

意义：
- 衡量平台是否从单点试用变成团队日常工具。

### 2. 任务交付价值

- `task_completion_rate`
- `rework_rate`
- `first_pass_acceptance_rate`
- `human_intervention_rate`

意义：
- 衡量 SherryAgent 是否真正减少返工，而不是制造更多人工校正成本。

### 3. 风险治理效果

- `dangerous_action_block_rate`
- `false_block_rate`
- `approval_wait_time_p95`
- `policy_override_rate`

意义：
- 衡量平台是否在安全和效率之间取得合理平衡。

### 4. 运营效率

- `report_delivery_sla_rate`
- `incident_triage_time_p95`
- `release_gate_pass_rate`
- `backlog_burn_down_rate`

意义：
- 衡量后台任务、运维巡检和发布治理是否形成可持续流程。

### 5. 单位经济性

- `cost_per_successful_task`
- `token_cost_per_repo_per_week`
- `cost_per_story_acceptance_run`
- `manual_hours_saved_estimate`

意义：
- 衡量平台能力提升是否具备成本合理性。

## 指标分组与使用场景

| 指标组 | 核心问题 | 主要使用者 |
|------|------|------|
| 采用度 | 有多少团队和仓库在持续使用？ | 项目负责人、平台维护者 |
| 交付价值 | 平台有没有减少返工、提高一次通过率？ | 开发团队、项目经理 |
| 风险治理 | 安全策略是在保护平台还是拖慢平台？ | 安全负责人、平台维护者 |
| 运营效率 | 巡检、告警、发布治理是否形成闭环？ | 运维、SRE、发布负责人 |
| 单位经济性 | 能力提升是否值得当前成本？ | 项目负责人、平台维护者 |

## 默认阈值建议

| 指标 | 目标 |
|------|------|
| `task_completion_rate` | > 85% |
| `first_pass_acceptance_rate` | > 70% |
| `rework_rate` | < 20% |
| `dangerous_action_block_rate` | > 95% |
| `false_block_rate` | < 10% |
| `report_delivery_sla_rate` | > 95% |
| `cost_per_successful_task` | 持续下降或稳定可控 |

## 说明

- 业务指标必须和 `baseline vs current` 的评测结果一起看，不能孤立解释。
- 单独追求采用度而不控制返工率和误拦截率，会把平台推向“看起来很忙但并不可靠”。

