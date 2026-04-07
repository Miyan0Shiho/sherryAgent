# SherryAgent - Story-03: Ops Sentinel + Incident Responder Spec

## Overview
- **Summary**: 上线后巡检/告警/证据收集/排障 runbook + 高风险确认与回滚计划（docs-only 固化契约）。
- **Purpose**: 作为验收与演示套件，验证运维巡检与事故响应链路。
- **Related Story Doc**: `docs/stories/story-03-ops-sentinel-incident-responder.md`

## Goals
- 固化 Health Report 与 Incident Report 的输出契约
- 固化告警风暴限流/聚合与预算停止策略
- 固化高风险动作确认与回滚计划格式

## Acceptance Criteria
- Incident Report 包含 hypotheses+confidence、runbook、actions_requiring_confirmation、rollback_plan
- 风险分级明确且 CRITICAL 默认拒绝
