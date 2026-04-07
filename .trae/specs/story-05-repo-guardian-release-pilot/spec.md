# SherryAgent - Story-05: Repo Guardian + Release Pilot Spec

## Overview
- **Summary**: 仓库治理 + 发布编排闭环，强调门禁、计划、确认与回滚（docs-only 固化契约）。
- **Purpose**: 作为验收与演示套件，验证 repo 治理与发布门禁链路。
- **Related Story Doc**: `docs/stories/story-05-repo-guardian-release-pilot.md`

## Goals
- 固化 Repo Health Report 与 Release Plan 的输出契约
- 固化发布门禁（gates）与证据字段最低要求
- 固化发布动作的确认与回滚策略

## Acceptance Criteria
- Release Plan 必须包含 gates/steps/commands/rollback_plan/actions_requiring_confirmation
- 任何生产/部署类动作默认 CRITICAL（拒绝或强确认）
