# SherryAgent - Story-04: Research Miner + Security Auditor Spec

## Overview
- **Summary**: 长跑调研/分析 + 安全审计，强调来源可追溯与不确定性标注（docs-only 固化契约）。
- **Related Story Doc**: `docs/stories/story-04-research-miner-security-auditor.md`

## Goals
- 固化 sources/findings/confidence 的输出契约
- 明确“事实 vs 推断”的分离规则
- 明确扫描范围、预算与脱敏要求

## Acceptance Criteria
- 每条发现都有来源或证据缺口标注
- 每条结论都有置信度字段
- 高风险扫描必须确认并限定范围

