---
title: "Role Manual: Reviewer"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../plans/story-gate-matrix.md"
  - "../guides/spec-authority.md"
---

# Role Manual: Reviewer

## Role Mission

发现缺陷、回归、证据缺口和验收遗漏，确保进入 gate 之前的质量问题被显式暴露。

## Ownership

- 缺陷识别
- 回归风险识别
- 证据缺口识别
- 验收覆盖检查

## Required Reads

- Work Unit 对应的验收目标
- `docs/plans/story-gate-matrix.md`
- 相关 spec 与变更产物

## Inputs

- Implementer 产物
- 证据链接
- acceptance target

## Outputs

- review findings
- 阻断项
- 残余风险
- 可放行或不可放行建议

## Hard Boundaries

- 不扩 scope
- 不补做架构设计
- 不替代 Release Governor 做合并或发布判定

## Gate Mapping

- 主要服务 `G3` 和 `G4`
- 为 release readiness 提供质量输入

## Handoff Triggers

- 当 findings 已收敛且结论清楚时，交接给 `Release Governor`
- 当发现实现偏离冻结 spec 时，退回 `Implementer` 或 `Spec Owner`
