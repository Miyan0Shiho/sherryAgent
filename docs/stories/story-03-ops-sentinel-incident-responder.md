---
title: "Story-03: Ops Sentinel + Incident Responder（运维哨兵 + 故障响应）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../standard/story-template.md"
  - "../specs/heartbeat-engine.md"
  - "../specs/permission-system.md"
  - "../specs/observability-system.md"
---

# Story-03: Ops Sentinel + Incident Responder（运维哨兵 + 故障响应）

> 角色说明：本文档是 **验收与演示套件**，用于验证巡检、告警、证据收集与事故响应链路，不承担顶层项目规划职责。

## Goal

在上线后场景中，Agent 能长期自主运行：
- 定时巡检、阈值告警、生成报告
- 发生告警时自动收集证据、生成 runbook 级的排障路径
- 需要高风险动作时进入人机协作确认（不自动“修机器”）

## Non-Goals

- 不做“无人值守的自动修复一切”
- 不在缺少可观察证据时给出确定性结论
- 不允许任何 CRITICAL 风险动作自动执行

## 演示脚本

### 手动交互（CLI/TUI）

1. 用户输入：定义一个巡检项（例如 CPU/内存阈值、服务端口存活、日志关键字）。
2. Agent 输出：巡检定义 + 阈值 + 触发策略 + 输出契约。
3. 用户模拟一次告警（或输入“触发告警”指令）：Agent 输出证据收集计划。

### 条件触发/后台（Heartbeat/Cron）

1. Cron 每 5 分钟执行巡检。
2. 发现异常：生成 Incident Report，并推送状态（WebSocket/日志）。
3. 如果需要执行修复动作（例如重启服务）：列出最小高风险动作集，等待确认后执行或降级为只读建议。

## Output Contract

产出两个报告：

1. **Ops Health Report**
   - `checks`（巡检项列表）
   - `status`（OK/WARN/ALERT）
   - `evidence`（采集到的证据摘要）
   - `trend`（最近 N 次变化）

2. **Incident Report**
   - `incident_id`
   - `symptoms`（症状）
   - `evidence`（命令输出/日志片段摘要/指标快照）
   - `hypotheses`（假设 + 置信度）
   - `runbook`（排障步骤：只读优先）
   - `actions_requiring_confirmation`（需要确认的高风险动作）
   - `rollback_plan`

## 核心链路映射

- **主链路**：`Autonomous Background Loop`
- **次链路**：`Repo / Release Governance Loop`（当事件来自发布、部署、配置变更）
- **辅助链路**：`Interactive Dev Loop`（人工查看报告与确认高风险动作）

## 核心数据对象映射

- **Task**：必须包含 `source=cron|event|webhook`、`risk_level`、`mode=background-ops`
- **Run**：必须能区分巡检 Run 与事故响应 Run
- **Evidence**：必须覆盖指标、日志、命令输出、配置快照中的至少一种
- **Decision**：必须记录告警聚合、权限阻断、确认请求、回滚建议
- **Cost Record**：必须可观察巡检频率对成本和延迟的影响

## 评测层级映射

- **Story Acceptance**：主验收层，验证巡检与事故响应是否闭环
- **Capability Benchmark**：验证证据收集、归因、runbook 生成
- **Safety Evaluation**：验证修复动作不会自动越权执行
- **Load & Scale Test**：验证告警风暴场景下的去重、合并与节流
- **Regression Suite**：纳入误报、证据不足、权限过严等历史事故样本

## 正式验收检查点

- `Ops Health Report` 与 `Incident Report` 必须都有 Evidence 支撑
- 不能在证据不足时输出确定性结论
- 修复动作必须与回滚计划成对出现
- 告警风暴必须表现为聚合与限流，而不是生成海量独立任务

## 风险分级与权限策略（写死）

- **LOW**：读指标、读日志、读配置。自动放行 + 审计。
- **MEDIUM**：写报告、发通知。自动放行 + 审计。
- **HIGH**：执行诊断命令（可能暴露敏感信息）、触网拉取依赖。必须确认或进行脱敏。
- **CRITICAL**：重启服务、修改系统配置、删除文件。默认拒绝，除非明确人工确认并带回滚计划。

## 失败模式与降级

- 无法收集证据：输出“证据缺口清单”，停止下结论。
- 告警风暴：聚合告警（去重/合并）+ 限流 + 预算硬停止。
- 权限过严导致无法执行：输出“最小放行建议”（策略变更建议），但不直接自改策略。

## 六层映射

- 交互层：查看健康报告与事故报告、进行确认操作。
- 编排层：将响应拆成证据收集/归因/建议/确认动作/回滚计划。
- 执行层：诊断并发、修复串行；所有动作产生可观察事件流。
- 自主运行层：Heartbeat/Cron 是主驱动。
- 记忆层：沉淀“历史事故与处理经验”（去敏），用于降低 MTTR。
- 基础设施层：权限管道 + 审计 + 通知是这条故事线的核心。
