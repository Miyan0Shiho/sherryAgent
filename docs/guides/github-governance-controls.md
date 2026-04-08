---
title: "GitHub 并行治理与门禁配置"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "./git-workflow.md"
  - "./spec-authority.md"
  - "../plans/master-program.md"
---

# GitHub 并行治理与门禁配置

本文档把 SherryAgent 的“多对话并行开发防冲突”方案映射为可落地的 GitHub 控制面。

## 1. 基础模型

- 工作单元：`1 Issue + 1 Branch + 1 PR`
- 分支命名：`codex/multi-agent-test/<issue-id>-<topic>`
- PR 标题：`[axis/subdomain] short topic`
- 进入评审前必须打 `status:in_review`，并触发冲突检查
- 一个 Work Unit 在同一时刻只能有一个 `role_owner`

## 2. Issue 类型与必备标签

Issue 类型：
- `type:axis-task`
- `type:contract-change`
- `type:conflict-decision`

标签维度：
- 轴线：`axis:*`
- 风险：`risk:low | risk:medium | risk:high`
- 门禁目标：`gate:G1 | gate:G2 | gate:G3 | gate:G4`
- 状态：`status:proposed | status:claimed | status:in_progress | status:in_review | status:blocked | status:merged`

角色字段：
- `role_owner`：当前主责角色
- `next_role`：下一位接手角色
- `handoff_ready`：是否满足交接条件
- `story_anchor`：当前 Work Unit 绑定的 Story 样板
- `gate_target`：当前 Work Unit 服务的 gate
- `branch_name`：当前 Work Unit 使用的分支，必须匹配实验期前缀

## 3. 必备仓库资产

- `.github/ISSUE_TEMPLATE/work-unit.yml`
- `.github/ISSUE_TEMPLATE/contract-change.yml`
- `.github/ISSUE_TEMPLATE/conflict-decision.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/CODEOWNERS`
- `.github/workflows/pr-governance-gates.yml`
- `scripts/ci/pr_governance_checks.py`
- `docs/roles/program-conductor.md`
- `docs/standard/program-conductor-state.md`
- `docs/standard/story-rollout-record.md`

## 4. Branch Protection（main）

在 GitHub 仓库设置中为 `main` 启用：

- Require a pull request before merging
- Require approvals（至少 1；`contract-impacting` 由 CODEOWNERS 实现双审）
- Require status checks to pass before merging，并勾选：
  - `Spec-Docs Sync`
  - `Glossary Consistency`
  - `Gate Eligibility (G1-G4)`
  - `No Active Conflict Claim`
- Dismiss stale pull request approvals when new commits are pushed
- Require conversation resolution before merging

## 5. CODEOWNERS 约束

- `.trae/specs/*` 与 `docs/*` 必须由不同 authority 组维护。
- `type:contract-change` PR 必须同时请求 `spec authority` 与 `docs authority`。
- `.github/*` 与 `scripts/ci/*` 建议由 `release-program authority` 负责。
- 角色映射建议：
  - `Program Conductor` 对 `docs/guides/*`, `docs/standard/*` 中的编排控制面有维护责任
  - `Spec Owner` 对 `.trae/specs/*`
  - `Architect/Spec Owner` 对 `docs/architecture/*`, `docs/specs/*`
  - `Release Governor` 对 `.github/*`, `docs/plans/*`, `scripts/ci/*`

## 6. 冲突裁决流程

触发条件：
- 多个 PR 同时修改同一契约对象（Task/Run/Evidence/Decision/Cost Record）
- 状态机、术语、Gate 判定口径冲突
- 同一 `axis/subdomain` 同时存在多个 `status:in_review` PR

流程：
1. 创建 `type:conflict-decision` Issue。
2. 按 `docs/guides/spec-authority.md` 的 A/B 类规则裁决。
3. 在冲突 Issue 记录 `facts -> decision_basis -> required_sync_actions`。
4. 将裁决结果回写冲突 PR 并完成同步修订。

## 7. 与 docs-only 阶段的关系

- 当前阶段不恢复旧实现，不绕过文档权威直接推进代码。
- 任何非 trivial 变更必须保持 `.trae/specs/*` 与 `docs/*` 同步更新。
- 门禁脚本服务于治理一致性，不替代人工架构审查。
- 角色文档和 prompt 模板属于协作控制面，必须服从双权威与 gate 规则。
- `Program Conductor` 只能调度和阻断，不能绕过角色边界直接宣布 gate 通过。
- 第一批实现型 rollout 只允许以 `Story-01` 与 `Story-05` 作为锚点。
