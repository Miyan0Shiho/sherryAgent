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
  - "../roles/program-conductor.md"
  - "../standard/program-conductor-state.md"
  - "../standard/story-rollout-record.md"
---

# 多对话角色化开发指南

本文档定义 SherryAgent 在 docs-first 阶段使用多个对话并行推进时的角色化协作模型。

## 为什么需要角色化协作

- 单一对话容易同时承担澄清、设计、执行、评审和治理，导致边界漂移。
- 多个对话并行时，如果没有角色边界，很容易在同一 Work Unit 上重复决策或互相覆盖。
- 角色化的目标不是增加流程，而是把“谁负责决定什么”写死，减少二次判断。

## Program Conductor

- `Program Conductor` 是唯一调度者，不是普通产物角色。
- 它负责读取总控文档、拆分 Work Unit、分配 `role_owner`、校验 handoff、控制 `G1 -> G4` 节奏。
- 它不能替代 7 个角色做设计、规格、实现或评审。

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

0. `Program Conductor`
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
- 一个 Work Unit 的分支必须遵守 `codex/multi-agent-test/<issue-id>-<topic>`。
- 一个 Work Unit 在同一时刻只能有一个主责角色。
- 非主责角色只能以 `research`, `review`, `support` 身份介入，不能改写主责角色已冻结的决定。
- 当 Work Unit 涉及契约层改动时，`Spec Owner` 必须成为主责角色后才能进入实现。
- `Program Conductor` 必须为每个 Work Unit 指定 `story_anchor` 和 `gate_target`。
- `Program Conductor` 还必须记录 `branch_name`，并确保其与 Issue 和 PR 保持一致。

## Phase Program

- Phase A: `G1 Foundation Gate`
  - 只推进 `platform-foundation` 与 `runtime-orchestration`
  - 输出：统一对象、统一状态机、4 条主链路冻结
- Phase B: `G2 Capability Gate`
  - 推进 `memory-knowledge` 与 `tooling-integration`
  - 输出：Evidence 生命周期、检索/压缩、工具协议、权限分类冻结
- Phase C: `G3 Governance Gate`
  - 推进 `quality-evaluation` 与 `cost-latency-ops`
  - 输出：baseline、回归资产、预算/限流/降级、容量指标冻结
- Phase D: `G4 Release Readiness Gate`
  - 推进 `release-program` 与 Story 穿透验证
  - 输出：门禁矩阵、风险台账、进入实现阶段条件

切换规则：

- `G1` 未冻结，禁止推进 `G2`
- `G4` 未通过，禁止进入恢复实现讨论

## 交接时机

- `Product Owner -> Researcher`：目标、成功标准、范围边界已经明确，但事实仍不足。
- `Researcher -> Architect`：事实证据和备选方案已齐全，可以开始冻结结构决策。
- `Architect -> Spec Owner`：边界、链路、状态机、依赖已定，不再要求实现者补设计。
- `Spec Owner -> Implementer`：`.trae/specs` 与 `docs/*` 已同步，`branch_name` 与 Issue/PR 已建立，执行口径可直接消费。
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
- 首批 rollout 固定为 `Story-01` 与 `Story-05`。
- 第二批补强从 `Story-03` 开始。
