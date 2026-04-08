---
title: "Program Conductor 状态对象"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../roles/program-conductor.md"
  - "../guides/multi-conversation-development.md"
---

# Program Conductor 状态对象

`Program Conductor State` 是总控 Agent 在任意时刻都必须维护的最小状态表。

## Required Fields

- `phase`
- `active_work_units`
- `branch_allocations`
- `current_role`
- `next_role`
- `gate_target`
- `story_anchor`
- `handoff_status`
- `blocked_reason`
- `blocking_risks`

## Field Notes

- `phase`：当前 program 所处阶段，只能为 `A/G1`, `B/G2`, `C/G3`, `D/G4`
- `active_work_units`：当前被调度的 Work Unit 列表
- `branch_allocations`：当前 phase 下每个 Work Unit 对应的分支名映射
- `current_role`：当前 Work Unit 的主责角色
- `next_role`：下一位必须接手的角色
- `gate_target`：该 Work Unit 当前服务的 gate
- `branch_allocations` 中的分支名必须匹配 `codex/multi-agent-test/<issue-id>-<topic>`
- `story_anchor`：该 Work Unit 对应的 Story 样板；首批只允许 `Story-01` 或 `Story-05`
- `handoff_status`：`not_ready | ready | blocked | completed`
- `blocked_reason`：当前阻断原因
- `blocking_risks`：当前必须显式暴露的风险

## Minimal Example

```md
phase: A/G1
active_work_units:
  - platform-foundation/task-object/freeze-required-fields
branch_allocations:
  platform-foundation/task-object/freeze-required-fields: codex/multi-agent-test/1234-task-object-freeze
current_role: Spec Owner
next_role: Reviewer
gate_target: G1
story_anchor: Story-01
handoff_status: ready
blocked_reason:
blocking_risks:
  - Runtime orchestration wording may drift if not synced this round
```
