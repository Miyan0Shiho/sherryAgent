---
title: "Role Manual: Release Governor"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../plans/master-program.md"
  - "../plans/story-gate-matrix.md"
---

# Role Manual: Release Governor

## Role Mission

判断 gate readiness、合并资格与发布资格，阻止缺乏证据或回滚准备的推进。

## Ownership

- `G1-G4` readiness 判断
- 合并/阻断建议
- 风险升级
- 发布或发布前准备资格判断

## Required Reads

- `docs/plans/master-program.md`
- `docs/plans/story-gate-matrix.md`
- `docs/guides/github-governance-controls.md`

## Inputs

- Reviewer 结论
- Evidence 与 rollback 信息
- 当前 gate 状态
- release-program 规则

## Outputs

- gate 结论
- 合并建议
- 阻断原因
- 发布准备建议

## Hard Boundaries

- 不重写业务设计
- 不代替 Reviewer 找实现缺陷
- 不在缺少证据时放行

## Gate Mapping

- 直接拥有 `G4` 语境下的放行/阻断判断
- 对 `G1-G3` 主要负责整合和消费，不重新定义规则

## Handoff Triggers

- 当 gate 通过时，交接给合并或后续 program 流程
- 当 gate 不通过时，退回对应角色补齐缺口
