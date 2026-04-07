---
title: "Story-01: Rigorous Dev Copilot（严谨开发助手）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../standard/story-template.md"
  - "../specs/agent-loop.md"
  - "../specs/permission-system.md"
  - "../../.trae/specs/mvp-1-core-agent-loop/spec.md"
---

# Story-01: Rigorous Dev Copilot（严谨开发助手）

## Goal

在 CLI/TUI 中完成“需求澄清 -> 设计 -> 实施 -> Review”的严谨工程闭环，并且做到：
- 输出结构化、可追溯、可复盘
- 工具调用全链路权限控制
- 所有变更必须有规范来源（`.trae/specs`）

## Non-Goals

- 不追求“全自动写完一个大型项目”
- 不允许绕过权限系统直接执行高风险操作
- 不把“能跑”当作唯一目标，必须满足 Output Contract

## 演示脚本

### 手动交互（CLI/TUI）

1. 用户输入一个明确任务（例如：新增一个命令、修正文档结构、重写某流程）。
2. Agent 输出 `Plan`（结构化）：需求澄清、范围、接口/文件影响、风险、验收点（引用 `.trae/specs`）。
3. Agent 执行（如果允许）：工具调用必须可观察（Tool Use/Tool Result 事件），并记录审计信息。
4. Agent 输出 `Review`：对变更的风险点、边界条件、残留债务给出清单。

### 条件触发/后台（可选）

- 条件：当 repo 发生变更或到达指定时间窗口，自动生成“工程健康摘要”（只读模式）。
- 规则：只读工具自动放行；任何写操作进入确认流程。

## Output Contract（必须满足）

产出一个 “Dev Session Report”（Markdown 或 JSON 均可），至少包含：

- `task_id`
- `inputs`（用户输入与关键上下文）
- `assumptions`（假设与缺口）
- `decisions`（关键决策与理由）
- `actions`（执行过的工具调用摘要）
- `artifacts`（生成/修改的文档或文件路径列表）
- `risks`（风险分级与处理）
- `acceptance`（对应 `.trae/specs` 的验收点引用）
- `next_steps`（下一步最小任务）

## 风险分级与权限策略（写死）

- **LOW**：只读分析、搜索、读取文件。自动放行 + 审计。
- **MEDIUM**：写文档、修改非关键配置。默认自动放行 + 审计（可配置为确认）。
- **HIGH**：执行 shell 命令、批量改动、改动权限/沙箱策略。必须人工确认。
- **CRITICAL**：破坏性命令、删除关键目录、任何疑似泄露密钥行为。直接拒绝 + 告警。

## 失败模式与降级

- 模型能力不足：拆分成更小子任务；输出更强约束模板；必要时升级模型。
- 工具失败：切换只读策略，先产出定位报告与最小修复建议。
- 预算耗尽：先输出当前阶段报告（progress + blocked_reason），停止继续行动。
- 权限拒绝：给出“需要人类确认的最小操作列表”，等待确认后继续。

## 六层映射（关键落点）

- 交互层：CLI/TUI 作为强约束输入/输出面板。
- 编排层：把工程任务分解为“澄清/设计/实现/校验/总结”子任务并汇总。
- 执行层：Agent Loop 事件流输出可观察过程；工具调用并发策略明确（读并发、写串行）。
- 自主运行层：可选的定期工程健康报告。
- 记忆层：沉淀“工程决策/常见错误/最佳实践”到长期记忆，减少返工率。
- 基础设施层：权限管道、审计、沙箱是硬门禁。

