---
title: "Git 工作流规范"
status: approved
created: 2026-04-07
updated: 2026-04-08
related:
  - "../plans/implementation-program.md"
  - "./spec-authority.md"
  - "./github-governance-controls.md"
---

# Git 工作流规范

本文档定义当前 planning-first 阶段和未来恢复实现阶段都适用的 Git 规则。

## 并行开发基本规则

- 并行工作单元采用 `1 Issue + 1 Branch + 1 PR`。
- 一个分支只能服务一个 Issue，禁止跨 Issue 混合提交。
- 非 trivial 工作先认领 Issue，再开分支推进。

## 分支策略

- `main`：稳定主线，只接收经过审查的文档或实现变更。
- `codex/multi-agent-test/<issue-id>-<topic>`：实验期多子 Agent 的强制分支前缀，首批实现 Work Unit 必须使用。
- `release/*`：仅在未来恢复实现并进入发布流程后使用。
- `hotfix/*`：仅在未来出现生产级紧急修复时使用。

## 当前阶段要求

- 所有结构性变更都走独立分支。
- 文档体系重构和历史资料归档不要混在同一个提交里。
- 提交信息必须说明“变更了什么口径”，而不是只写文件名。
- 分支命名必须满足：`codex/multi-agent-test/<issue-id>-<topic>`。
- PR 标题推荐：`[axis/subdomain] short topic`。

## 提交粒度

- 一个提交只解决一个清晰问题。
- “入口改造”“规格对齐”“归档历史路线图”应分开提交。
- 任何会改变系统口径的提交，都要同步更新 `docs/INDEX.md`。

## PR 强制门禁

- 所有变更通过 PR 合并，禁止直推 `main`。
- PR 模板中的治理字段必须完整填写：
  - `linked_issue`
  - `contract_impact`
  - `spec_update`
  - `docs_update`
  - `gate_impact`
  - `evidence`
  - `rollback_plan`
- 仓库必须启用并保护以下检查：
  - `Spec-Docs Sync`
  - `Glossary Consistency`
  - `Gate Eligibility (G1-G4)`
  - `No Active Conflict Claim`

## 与文档权威的关系

- 分支上实现的内容若改变计划或契约，必须先改 `.trae/specs` 或 `docs/`。
- Git 流程服从 `docs/guides/spec-authority.md` 的双权威规则。

## 参考

- 具体 GitHub 设置步骤见 `docs/guides/github-governance-controls.md`。
