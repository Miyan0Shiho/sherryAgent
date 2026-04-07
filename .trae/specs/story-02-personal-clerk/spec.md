# SherryAgent - Story-02: Personal Clerk（个人助理）Spec

## Overview
- **Summary**: 安全受控的重复劳动与条件触发个人助理（docs-only 阶段先固化契约与边界）。
- **Related Story Doc**: `docs/stories/story-02-personal-clerk.md`

## Goals
- 明确“允许的自动化边界”（默认只读 + 审计）
- 明确高风险动作永不自动执行（必须确认/拒绝）
- 定义可回放输出契约（计划动作 vs 实际动作）

## Non-Goals
- 不做无边界电脑接管
- 本阶段不实现代码

## Acceptance Criteria
- Story 文档具备可执行的条件触发演示脚本
- 输出契约包含 actions_planned/actions_executed/audit 字段

