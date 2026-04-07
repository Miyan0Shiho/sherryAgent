---
title: "Story-05: Repo Guardian + Release Pilot（仓库治理 + 发布编排）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../standard/story-template.md"
  - "../specs/multi-agent-orchestration.md"
  - "../specs/task-persistence.md"
  - "../specs/permission-system.md"
---

# Story-05: Repo Guardian + Release Pilot（仓库治理 + 发布编排）

> 角色说明：本文档是 **验收与演示套件**，用于验证 repo 治理与发布门禁链路，不承担顶层项目规划职责。

## Goal

把“仓库治理”和“交付发布”合成一个工程闭环：
- 定期扫描质量/债务/风险，产出可执行治理清单
- 当满足发布门禁条件时，编排构建/测试/部署/回滚流程
- 自动化必须被权限与审计约束，避免“自动化毁仓库/毁生产”

## Non-Goals

- 不承诺一次性把 repo 治理到完美
- 不允许无门禁自动发布
- 不把 CI/CD 平台替代掉，而是作为可编排的能力层

## 演示脚本

### 手动交互（CLI/TUI）

1. 用户输入：对当前 repo 做一次治理扫描（依赖、结构、命名、风险、文档漂移）。
2. Agent 输出：治理报告 + 任务分解（Orchestrator）+ 最小修复建议。
3. 用户输入：执行一次“发布 dry-run”（不真正发布，只验证门禁与脚本）。

### 条件触发/后台（Cron/事件）

1. 每天定期触发治理扫描，生成 `Repo Health Report`。
2. 当满足门禁（例如主分支 green、版本号符合、变更摘要齐备）时，触发 `Release Plan`：
   - 默认只生成计划与命令，不执行高风险动作
   - 执行发布必须确认，并附带回滚计划

## Output Contract

产出两个报告：

1. **Repo Health Report**
   - `quality_signals`（lint/type/doc drift 等）
   - `risks`（安全/权限/依赖）
   - `debt_backlog`（债务清单，带优先级）
   - `suggested_tasks`（可执行任务拆分）

2. **Release Plan**
   - `gates`（门禁条件与结果）
   - `steps`（发布步骤）
   - `commands`（建议命令，默认不自动执行）
   - `rollback_plan`
   - `actions_requiring_confirmation`

## 核心链路映射

- **主链路**：`Repo / Release Governance Loop`
- **次链路**：`Interactive Dev Loop`（用于手工审阅治理报告与发布 dry-run）
- **辅助链路**：`Autonomous Background Loop`（用于定期治理扫描）

## 核心数据对象映射

- **Task**：必须包含 `source=cli|event|cron|webhook`、`risk_level`、`mode=interactive-dev|background-ops`
- **Run**：必须区分治理扫描 Run 与发布门禁 Run
- **Evidence**：必须支撑每一条门禁结论、风险结论和回滚建议
- **Decision**：必须记录门禁通过/阻断、确认请求、回滚建议与高风险拒绝
- **Cost Record**：必须反映扫描、构建、门禁评估的单位成本和时延

## 评测层级映射

- **Story Acceptance**：主验收层，验证 repo 治理和发布门禁闭环
- **Capability Benchmark**：验证门禁判断、风险识别、任务拆解与报告质量
- **Safety Evaluation**：验证部署、回滚、凭据相关动作不会自动越权执行
- **Regression Suite**：纳入误放行、误阻断、回滚缺失等历史发布失败样本
- **Cost / Latency Benchmark**：验证日常治理扫描与发布 dry-run 的成本与时延

## 正式验收检查点

- `Repo Health Report` 和 `Release Plan` 都必须有 Evidence 支撑
- 门禁失败时必须输出最小阻塞项，而不是泛泛而谈
- 任何生产相关动作必须停在确认或拒绝
- `rollback_plan` 不能缺席，缺席则判定验收失败

## 风险分级与权限策略（写死）

- **LOW**：读取、分析、生成报告。自动放行 + 审计。
- **MEDIUM**：修改文档、生成变更摘要、更新非关键配置。默认放行 + 审计（可配置确认）。
- **HIGH**：执行构建/测试命令、生成发布产物、操作凭据相关配置。必须确认。
- **CRITICAL**：部署到生产、回滚、删除发布产物、修改权限策略。默认拒绝，除非明确人工确认。

## 失败模式与降级

- 门禁失败：输出最小阻塞项清单（只列“必须修复的 Gate”）。
- 构建/测试不稳定：转为“只读诊断 + 报告”，不继续推进发布。
- 模型能力不足导致误判：要求每条门禁结论有证据字段，否则判定输出不合格。

## 六层映射

- 交互层：查看治理/发布计划，执行确认。
- 编排层：Orchestrator 分解并行扫描任务，汇总为报告与任务清单。
- 执行层：工具调用事件化；写操作严格串行。
- 自主运行层：定期治理扫描，条件满足触发发布计划。
- 记忆层：沉淀治理规则与历史发布经验（去敏），减少重复事故。
- 基础设施层：权限与审计把自动化框进安全边界。
