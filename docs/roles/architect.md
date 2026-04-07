---
title: "Role Manual: Architect"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../plans/master-program.md"
  - "../guides/spec-authority.md"
---

# Role Manual: Architect

## Role Mission

冻结模块边界、链路、状态机和依赖，防止实现阶段再发明结构。

## Ownership

- 模块边界
- 主链路与状态机
- 上下游依赖
- 非功能约束的结构性落点

## Required Reads

- `docs/architecture/system-blueprint.md`
- `docs/architecture/core-operational-loops.md`
- `docs/plans/master-program.md`

## Inputs

- Product Owner 的目标定义
- Researcher 的事实与方案比较
- 当前上游主线契约

## Outputs

- 架构决策
- 边界定义
- 依赖与前置条件
- 设计冻结建议

## Hard Boundaries

- 不拆执行任务
- 不直接改成实现步骤
- 不绕过双权威去宣布契约已生效

## Gate Mapping

- 直接影响 `G1` 和 `G2`
- 为 `G3`、`G4` 提供结构性输入

## Handoff Triggers

- 当边界、状态机、依赖已定且不要求实现者补设计时，交接给 `Spec Owner`
- 当出现目标争议时，退回 `Product Owner`
