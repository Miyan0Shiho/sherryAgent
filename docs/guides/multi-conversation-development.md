---
title: "多对话角色化开发指南"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "./spec-authority.md"
  - "./github-governance-controls.md"
  - "../plans/master-program.md"
  - "../plans/story-gate-matrix.md"
  - "../standard/role-handoff-contract.md"
---

# 多对话角色化开发指南

本文档定义 SherryAgent 在 docs-first 阶段使用多个对话并行推进时的角色化协作模型。

## 为什么需要角色化协作

- 单一对话容易同时承担澄清、设计、执行、评审和治理，导致边界漂移。
- 多个对话并行时，如果没有角色边界，很容易在同一 Work Unit 上重复决策或互相覆盖。
- 角色化的目标不是增加流程，而是把“谁负责决定什么”写死，减少二次判断。

## 7 角色全景图

| 角色 | 主职责 | 主要输出 |
|------|--------|----------|
| `Product Owner` | 澄清目标、成功标准、范围边界 | 目标定义、验收目标、范围裁剪 |
| `Researcher` | 补事实、补备选方案、补风险事实 | 调研摘要、事实证据、方案选项 |
| `Architect` | 定模块边界、链路、状态机、依赖 | 架构决策、边界说明、设计冻结建议 |
| `Spec Owner` | 落双权威文档并冻结执行口径 | `.trae/specs`、`docs/*` 同步更新方案 |
| `Implementer` | 按冻结 spec 执行实现或文档任务 | 变更产物、执行记录、实现说明 |
| `Reviewer` | 找缺陷、回归、证据缺口 | 审查结论、阻断项、残余风险 |
| `Release Governor` | 判断 gate readiness 与合并/发布资格 | gate 结论、阻断决定、发布建议 |

## 启动顺序

默认顺序：

1. `Product Owner`
2. `Researcher`
3. `Architect`
4. `Spec Owner`
5. `Implementer`
6. `Reviewer`
7. `Release Governor`

允许跳过的情况：

- 明确是已有 spec 的小型执行任务，可从 `Implementer` 开始。
- 明确是已完成变更的质量检查，可从 `Reviewer` 开始。
- 明确是 gate 判断任务，可直接由 `Release Governor` 接入。

## Work Unit 绑定规则

- 一个 Work Unit 采用 `1 Issue + 1 Branch + 1 PR`。
- 一个 Work Unit 在同一时刻只能有一个主责角色。
- 非主责角色只能以 `research`, `review`, `support` 身份介入，不能改写主责角色已冻结的决定。
- 当 Work Unit 涉及契约层改动时，`Spec Owner` 必须成为主责角色后才能进入实现。

## 交接时机

- `Product Owner -> Researcher`：目标、成功标准、范围边界已经明确，但事实仍不足。
- `Researcher -> Architect`：事实证据和备选方案已齐全，可以开始冻结结构决策。
- `Architect -> Spec Owner`：边界、链路、状态机、依赖已定，不再要求实现者补设计。
- `Spec Owner -> Implementer`：`.trae/specs` 与 `docs/*` 已同步，执行口径可直接消费。
- `Implementer -> Reviewer`：产物、证据、验收目标已齐备，可以做缺陷审查。
- `Reviewer -> Release Governor`：审查结论已出，剩余问题和风险分级清晰。

## 阻断条件

- 同一 Work Unit 出现两个主责角色。
- `Implementer` 收到仍需决定契约的任务。
- `Reviewer` 收到没有验收目标或证据链接的任务。
- `Release Governor` 收到缺少 gate 输入、rollback 信息或阻断解释的任务。

## 升级路径

- 目标/范围争议：升级给 `Product Owner`
- 事实不足或方案证据不足：升级给 `Researcher`
- 边界/状态机/依赖争议：升级给 `Architect`
- 双权威冲突：升级给 `Spec Owner`
- 实现偏离冻结 spec：退回 `Implementer`
- 缺陷或回归争议：升级给 `Reviewer`
- 合并、门禁、发布资格争议：升级给 `Release Governor`

## 与 GitHub 治理的关系

- Issue 记录 `role_owner`, `next_role`, `handoff_ready`
- PR 记录 `origin_role`, `review_role`, `gate_owner`
- 冲突 Issue 记录 `role_conflict`
- `CODEOWNERS` 不直接定义角色，但角色分工必须能映射到 owner 组

## 与主线和 Story 的关系

- `Product Owner` 与 `Researcher` 主要服务 Story 目标澄清和事实补完。
- `Architect` 与 `Spec Owner` 主要服务 7 条主线和契约冻结。
- `Implementer` 与 `Reviewer` 主要服务执行与质量闭环。
- `Release Governor` 直接使用 `story-gate-matrix` 和 `release-program` 做判断。
