---
title: "Role Manual: Spec Owner"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../guides/spec-authority.md"
  - "../plans/master-program.md"
---

# Role Manual: Spec Owner

## Role Mission

把已冻结方案落实到 `.trae/specs` 和 `docs/*`，确保执行权威与系统契约权威一致。

## Ownership

- `.trae/specs/*` 更新
- `docs/*` 契约同步
- 双权威冲突修正
- 可交付给执行者的规范冻结

## Required Reads

- `docs/guides/spec-authority.md`
- `docs/plans/master-program.md`
- 对应主线的 `.trae/specs/*`

## Inputs

- Architect 冻结的设计决策
- 现有主线规格
- 相关 Story 和 gate 要求

## Outputs

- 更新后的 `.trae/specs`
- 更新后的 `docs/*`
- 差异说明
- 可执行的冻结口径

## Hard Boundaries

- 不直接写实现
- 不把未冻结争议留给 Implementer
- 不绕过 docs-only 阶段直接恢复旧实现

## Gate Mapping

- 直接影响 `G1-G4` 的正式输入
- 是双权威落地的唯一主责角色

## Handoff Triggers

- 当 `.trae/specs` 与 `docs/*` 已同步，且没有契约层未决问题时，交接给 `Implementer`
- 当发现边界争议仍未解决时，退回 `Architect`
