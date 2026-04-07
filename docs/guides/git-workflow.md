---
title: "Git 工作流规范"
status: approved
created: 2026-04-07
updated: 2026-04-07
related:
  - "../plans/implementation-program.md"
  - "./spec-authority.md"
---

# Git 工作流规范

本文档定义当前 planning-first 阶段和未来恢复实现阶段都适用的 Git 规则。

## 分支策略

- `main`：稳定主线，只接收经过审查的文档或实现变更。
- `codex/*` 或 `feat/*`：功能分支、计划分支、文档重构分支。
- `release/*`：仅在未来恢复实现并进入发布流程后使用。
- `hotfix/*`：仅在未来出现生产级紧急修复时使用。

## 当前阶段要求

- 所有结构性变更都走独立分支。
- 文档体系重构和历史资料归档不要混在同一个提交里。
- 提交信息必须说明“变更了什么口径”，而不是只写文件名。

## 提交粒度

- 一个提交只解决一个清晰问题。
- “入口改造”“规格对齐”“归档历史路线图”应分开提交。
- 任何会改变系统口径的提交，都要同步更新 `docs/INDEX.md`。

## 与文档权威的关系

- 分支上实现的内容若改变计划或契约，必须先改 `.trae/specs` 或 `docs/`。
- Git 流程服从 `docs/guides/spec-authority.md` 的双权威规则。

