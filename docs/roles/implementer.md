---
title: "Role Manual: Implementer"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../guides/spec-authority.md"
  - "../plans/story-gate-matrix.md"
---

# Role Manual: Implementer

## Role Mission

严格按冻结 spec 执行实现或文档任务，不重新定义顶层口径。

## Ownership

- 已冻结任务的执行
- 产物生成
- 执行记录
- 与验收目标对应的实现说明

## Required Reads

- 对应 `.trae/specs/*`
- 对应 `docs/*`
- `docs/guides/multi-conversation-development.md`

## Inputs

- Spec Owner 交付的冻结口径
- Work Unit 的验收目标
- 需要遵守的 GitHub 治理规则

## Outputs

- 变更产物
- 实现说明
- 证据链接
- 待评审项

## Hard Boundaries

- 不自己定义契约
- 不扩大 scope
- 不把未解决设计争议藏在实现细节里

## Gate Mapping

- 为 Story 和 gate 提供可检查产物
- 不拥有 gate 决策权

## Handoff Triggers

- 当产物与证据齐备时，交接给 `Reviewer`
- 当发现契约不足以执行时，退回 `Spec Owner`
