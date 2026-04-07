---
title: "Story-02: Personal Clerk（个人助理：安全受控的重复劳动）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../standard/story-template.md"
  - "../specs/permission-system.md"
  - "../specs/heartbeat-engine.md"
---

# Story-02: Personal Clerk（个人助理：安全受控的重复劳动）

> 角色说明：本文档是 **验收与演示套件**，用于验证重复事务与条件触发链路，不承担顶层项目规划职责。

## Goal

让 Agent 能做“重复但有条件”的事务（整理、提醒、批处理、定期汇总），同时在无人值守时仍满足：
- 强权限与审计
- 可回放
- 高风险永不自动执行

## Non-Goals

- 不做“无边界的电脑接管”
- 不允许绕过权限管道的自动化
- 不承诺在信息不全时自动做决定（必须输出不确定性与置信度）

## 演示脚本

### 手动交互（CLI/TUI）

1. 用户给出一个重复任务（例如：每天把某目录的新增文件汇总成清单、每周生成一次学习周报）。
2. Agent 输出一个可执行的“任务定义”（触发条件、输入、输出、预算、风险分级）。
3. Agent 运行一次“dry-run”（只读）展示将产生什么输出。

### 条件触发/后台（Heartbeat/Cron）

1. 配置 Cron（或 heartbeat 待办）触发该任务。
2. 后台执行：只读/低风险动作自动放行，产生报告并写入审计日志。
3. 遇到高风险动作：暂停并推送“需要确认的最小动作集”。

## Output Contract

产出一个 “Clerk Report”，至少包含：
- `schedule`（何时触发）
- `inputs`（数据来源/路径/规则）
- `actions_planned`（计划动作列表，带风险等级）
- `actions_executed`（实际执行动作列表）
- `audit`（权限决策与确认记录引用）
- `results`（输出摘要）

## 核心链路映射

- **主链路**：`Autonomous Background Loop`
- **次链路**：`Interactive Dev Loop`（用于手工定义任务和 dry-run 审阅）
- **不作为主验收链路**：`Repo / Release Governance Loop`

## 核心数据对象映射

- **Task**：必须包含 `source=cron|event|cli`、`goal`、`risk_level`、`budget_profile`、`mode=autonomous-safe`
- **Run**：必须体现 dry-run 与真实执行的差异
- **Evidence**：必须能指向输入数据来源、触发条件命中与实际输出依据
- **Decision**：必须记录调度、确认等待、风险拒绝和预算停止
- **Cost Record**：必须反映周期性任务的单位运行成本与缓存命中情况

## 评测层级映射

- **Story Acceptance**：主验收层，验证重复事务与条件触发是否闭环
- **Regression Suite**：纳入高频触发、信息缺口、重复执行等历史失败样本
- **Safety Evaluation**：验证高风险动作不会在无人值守下自动执行
- **Cost / Latency Benchmark**：验证周期任务在 `strict` 档位下的成本稳定性
- **Load & Scale Test**：验证高频触发任务的聚合与限流

## 正式验收检查点

- 任务定义必须显式写出触发条件、输入、输出、预算与风险等级
- dry-run 与真实执行必须产生可区分的 Run 和审计记录
- 高频触发时必须能限流、聚合或硬停止，不能无限增殖执行
- 高风险动作必须停在 `waiting_confirmation`

## 风险分级与权限策略（写死）

- **LOW**：读文件、列目录、解析文本。自动放行 + 审计。
- **MEDIUM**：写报告文件、追加日志。默认放行 + 审计。
- **HIGH**：对外网络请求、执行命令、写入敏感路径。必须确认或降级为只读。
- **CRITICAL**：任何破坏性操作、疑似凭据操作。直接拒绝。

## 失败模式与降级

- 信息不全：生成“需要补充的信息清单”，不擅自假设继续执行。
- 触发频率过高导致预算风险：触发限流 + 聚合执行（批处理）+ 预算硬停止。
- 外部依赖失败：输出可复现的失败报告（错误码/重试建议/替代路径）。

## 六层映射

- 交互层：用 CLI/TUI 定义与审阅任务定义、查看报告。
- 编排层：把重复任务拆成采集/处理/输出/归档的流水线。
- 执行层：工具调用严格按风险分级执行（写串行）。
- 自主运行层：Heartbeat/Cron 驱动条件触发。
- 记忆层：沉淀“用户偏好与规则”，但敏感信息永不写入日志。
- 基础设施层：权限管道 + 审计日志是核心价值，不是附加项。
