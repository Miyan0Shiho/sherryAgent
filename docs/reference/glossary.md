---
title: "术语表"
status: draft
created: 2026-04-07
updated: 2026-04-08
related:
  - "../architecture/system-blueprint.md"
  - "../specs/core-data-contracts.md"
---

# 术语表

## 当前有效术语

- **Hybrid Platform**：同时支持严谨开发协作和长期自主执行的平台定位。
- **Task**：统一任务对象，承载来源、目标、模式、风险、预算和状态。
- **Run**：某个 Task 的一次具体执行实例。
- **Evidence**：支撑结论、报告或决策的可定位证据。
- **Decision**：策略、权限、降级、升级、确认等关键裁决记录。
- **Cost Record**：单次 Run 的 token、延迟、工具调用和成本摘要。
- **Gateway**：CLI/API/Webhook/cron/event 统一入口。
- **Task Service**：任务状态机、幂等键、优先级、依赖和恢复边界。
- **Planner**：模式选择、任务拆解、模型路由、工具路由、预算分配。
- **Execution Engine**：执行循环、子任务执行、取消、超时、恢复。
- **Memory & Retrieval**：上下文装配、长期记忆、检索、压缩、冷热分层。
- **Policy & Guardrail**：风险分级、确认流、沙箱、审计、阻断与降级。
- **Scheduler & Trigger**：cron、事件、条件触发、节流和批处理调度。
- **Observability & Evaluation**：日志、指标、trace、run replay、benchmark、regression。
- **Cost & Capacity Controller**：预算、缓存、限流、并发控制、fallback、容量配额。
- **Release & Ops**：发布门禁、回滚、值班、事故管理、变更治理。
- **Runtime Mode**：`interactive-dev`、`autonomous-safe`、`background-ops`、`bulk-analysis` 四种运行模式。
- **Story**：验收与演示套件，不是顶层项目规划主轴。
- **Capability Benchmark**：能力基准评测，用于比较 baseline 和 current。
- **Regression Suite**：固定失败样本、事故样本和边界样本的回归集合。
- **G1 Foundation Gate**：`platform-foundation` 与 `runtime-orchestration` 的冻结门禁。
- **G2 Capability Gate**：`memory-knowledge` 与 `tooling-integration` 的能力层门禁。
- **G3 Governance Gate**：`quality-evaluation` 与 `cost-latency-ops` 的治理层门禁。
- **G4 Release Readiness Gate**：`release-program` 与 Story 验收汇总后的发布准备门禁。

## 历史术语

- **MVP-1..5**：已归档的旧阶段口径，不再作为执行主轴。
- **Phoenix / Egg / Chick**：已归档的比喻式路线图术语，不再作为当前计划口径。
- **Fork / Lane / Teammate**：历史实现和研究中出现的执行策略术语，当前不是一级模块边界。
