---
title: "需求评审流程"
status: approved
created: 2026-04-07
updated: 2026-04-07
related:
  - "./spec-authority.md"
  - "../plans/implementation-program.md"
---

# 需求评审流程

本文档定义 SherryAgent 当前的需求评审流程，目标是保证任何新增能力都能落入现有平台蓝图，而不是重新长出一套平行叙事。

## 评审必须回答的 6 个问题

1. 这个需求属于哪条一级主线？
2. 它影响哪一条核心链路？
3. 它新增或修改了哪些核心数据对象？
4. 它对质量、延迟、成本三者的取舍是什么？
5. 它对 10x / 100x 扩展是否有影响？
6. 它的验收方式是哪个 Story、哪个 benchmark、哪个 regression case？

## 必查项

- Goals 和 Non-Goals 明确
- 归属主线明确（7 条主线之一）
- 数据契约影响明确
- 风险等级和确认流明确
- 评测与回归影响明确
- 成本与延迟影响明确

## 产出要求

需求评审完成后，至少要更新：

- `.trae/specs/<主线>/spec.md` 或 `tasks.md`
- 相关 `docs/architecture/*` 或 `docs/specs/*`
- 必要时更新 `docs/stories/*`

## 不允许的情况

- 只写 Story，不写主线计划
- 只讲功能，不讲成本/风险/评测
- 只讲当前能做什么，不讲扩容和运维影响

