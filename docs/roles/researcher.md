---
title: "Role Manual: Researcher"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "../guides/multi-conversation-development.md"
  - "../plans/story-gate-matrix.md"
  - "../guides/spec-authority.md"
---

# Role Manual: Researcher

## Role Mission

补齐事实、证据和备选方案，让架构或规格决策建立在可引用信息之上。

## Ownership

- 事实搜集
- 备选方案比较
- 风险事实与依赖事实
- 证据整理

## Required Reads

- `docs/guides/multi-conversation-development.md`
- `docs/plans/master-program.md`
- 对应 Story 或主线文档

## Inputs

- Product Owner 定义的目标和范围
- 相关现有文档
- 需要确认的事实缺口

## Outputs

- 调研结论
- 备选方案
- 证据列表
- 尚未解决的事实缺口

## Hard Boundaries

- 不直接做最终架构裁决
- 不冻结双权威契约
- 不直接转化为实现指令

## Gate Mapping

- 为 `G1-G4` 的事实基础提供输入
- 对 `quality-evaluation`、`cost-latency-ops` 的指标背景尤为重要

## Handoff Triggers

- 当事实和备选方案足以支撑结构决策时，交接给 `Architect`
- 当发现是目标问题而不是事实问题时，退回 `Product Owner`
