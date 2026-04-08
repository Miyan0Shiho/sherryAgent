---
title: "Cost And Ops Governance"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../architecture/quality-vs-latency-vs-cost.md"
  - "../architecture/scaling-strategy.md"
  - "../reference/technical-metrics.md"
---

# Cost And Ops Governance

## 预算档位

| 档位 | 默认适用 | 预算姿态 | 升级条件 |
|------|----------|----------|----------|
| `strict` | 后台、批量、低风险周期任务 | 强预算、优先缓存、早停 | 只有在风险或质量不足以交付时才允许升级 |
| `balanced` | 常规交互与团队开发 | 平衡质量、延迟、成本 | 复杂任务或高风险审查可升级到 `premium` |
| `premium` | 高风险决策、事故响应、发布治理 | 质量和证据优先 | 只能由 Planner 或人工明确升级 |

## 降级顺序

统一顺序固定为：

1. 降并发
2. 降模型档位
3. 降规划深度、样本量或批次大小
4. 停止并请求人工介入

高风险任务禁止跳过前 3 步直接静默失败。

## 缓存与限流

- `prompt cache`：模板化重复任务优先命中
- `evidence cache`：相同来源、相同时效窗口内可复用
- `retrieval cache`：受租户、仓库、查询上下文共同约束
- `decision cache`：只缓存明确可复用的低风险裁决

限流至少按以下维度实施：

- 团队
- 仓库
- 任务类型
- 风险等级

## 延迟与容量目标

- 高风险交互任务：优先满足质量与可审计性，允许更高延迟
- 高频后台任务：优先保持预算稳定和队列可控
- 批量分析任务：优先维持吞吐和聚合稳定
- 发布治理任务：优先保证一致性和回滚可用

正式关注指标以 [technical-metrics.md](../reference/technical-metrics.md) 为准，至少包括：

- `queue_lag`
- `run_completion_latency_ms`
- `retrieval_p95_ms`
- `token_burn_per_hour`
- `concurrent_runs`
- `policy_block_rate`

## SRE 与人工接管

以下资产是治理层必需输入，不是可选附件：

- run replay 能力
- cost dashboard 口径
- 告警阈值和升级路径
- 人工接管要求
- rollback 触发条件

当出现以下任一情况时，必须进入人工接管或阻断：

- `queue_lag` 持续上升且影响交互任务
- `token_burn_per_hour` 出现超预算趋势
- `policy_block_rate` 异常飙升且怀疑误拦截
- 发布治理链路缺少 rollback 计划
