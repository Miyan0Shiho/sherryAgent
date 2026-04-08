---
title: "Story Rollout Record 模板"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../plans/story-gate-matrix.md"
  - "../roles/program-conductor.md"
---

# Story Rollout Record 模板

`Story Rollout Record` 用于记录某个 Story 在 program 中承担的证明责任，以及其当前 gate 穿透状态。

## Required Fields

- `story_id`
- `issue_ref`
- `branch_name`
- `pr_ref`
- `required_workstreams`
- `gate_status`
- `blockers`
- `evidence_links`
- `release_governor_decision`

## Field Notes

- `story_id`：Story 标识，例如 `Story-01`
- `issue_ref`：对应的 Issue 编号或链接
- `branch_name`：对应的实验期分支名，必须匹配 `codex/multi-agent-test/<issue-id>-<topic>`
- `pr_ref`：对应的 PR 编号或链接
- `required_workstreams`：该 Story 当前依赖的主线
- `gate_status`：对 `G1-G4` 的通过、阻断或待补充状态
- `blockers`：当前阻断项
- `evidence_links`：支撑 gate 判断的文档、Issue、PR 或报告链接
- `release_governor_decision`：`pass | block | hold`

## Batch Rules

- 第一批 rollout 只允许 `Story-01` 与 `Story-05`
- 第二批优先加入 `Story-03`
- `Story-02` 与 `Story-04` 只在基础调度、记忆和治理边界稳定后进入 rollout

## Minimal Example

```md
story_id: Story-05
issue_ref: "#1234"
branch_name: codex/multi-agent-test/1234-release-gate-simulation
pr_ref: "#1250"
required_workstreams:
  - platform-foundation
  - runtime-orchestration
  - memory-knowledge
  - tooling-integration
  - quality-evaluation
  - cost-latency-ops
  - release-program
gate_status:
  G1: pass
  G2: pass
  G3: hold
  G4: blocked
blockers:
  - rollback_plan evidence missing
evidence_links:
  - docs/stories/story-05-repo-guardian-release-pilot.md
  - docs/plans/story-gate-matrix.md
release_governor_decision: hold
```
