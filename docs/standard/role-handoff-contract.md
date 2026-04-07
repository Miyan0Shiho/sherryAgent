---
title: "角色交接契约"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../guides/spec-authority.md"
---

# 角色交接契约

本文档定义多对话角色协作时统一的交接对象与有效性规则。

## Handoff Object

每次交接都必须至少包含以下字段：

- `handoff_id`
- `from_role`
- `to_role`
- `work_unit`
- `goal`
- `decisions_locked`
- `open_questions`
- `required_inputs`
- `artifacts`
- `blocking_risks`
- `acceptance_target`

## 字段说明

- `handoff_id`：唯一交接编号，建议与 Issue 或 PR 关联。
- `from_role`：当前交接发起角色。
- `to_role`：下一位主责角色。
- `work_unit`：对应的 Work Unit 标识，必须能映射到 Issue。
- `goal`：交接后的唯一目标。
- `decisions_locked`：已经冻结、不能让接收方再次决定的事项。
- `open_questions`：仍未解决但允许接收方处理的问题。
- `required_inputs`：接收方继续推进所需的最小输入。
- `artifacts`：当前阶段已产出的文档、PR、Issue、报告或证据。
- `blocking_risks`：当前仍存在的阻断风险。
- `acceptance_target`：下一阶段的验收目标或 gate 目标。

## 交接有效性规则

- 未写 `decisions_locked` 的交接无效。
- `Implementer` 不接收“仍需自己决定契约”的任务。
- `Reviewer` 不接收“没有 acceptance target”的任务。
- `Release Governor` 不接收“没有 evidence links 或 rollback 信息”的任务。
- 如果 `open_questions` 实际上是契约争议，必须退回 `Spec Owner` 或 `Architect`。

## 标准模板

```md
handoff_id: HANDOFF-2026-04-08-001
from_role: Architect
to_role: Spec Owner
work_unit: runtime-orchestration/planner/budget-routing
goal: Freeze the planner budget-routing contract in dual-authority docs
decisions_locked:
  - Planner owns budget allocation before execution starts
  - Execution Engine cannot silently upgrade budget profile
open_questions:
  - Whether low-risk dry-run paths need a separate note in story docs
required_inputs:
  - Current planner notes
  - Related Story-01 acceptance mapping
artifacts:
  - docs/architecture/system-blueprint.md
  - docs/plans/story-gate-matrix.md
blocking_risks:
  - Cost profile terms may drift from cost-latency-ops if not synced
acceptance_target:
  - G1 contract wording frozen and referenced from `.trae/specs`
```
