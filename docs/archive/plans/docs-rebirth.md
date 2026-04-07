---
title: "Docs Rebirth：从 Demo 到文档驱动重生的蒸馏计划"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../guides/spec-authority.md"
  - "../INDEX.md"
---

# Docs Rebirth：从 Demo 到文档驱动重生的蒸馏计划

本计划的目标不是“把代码修到完美”，而是把 SherryAgent 迭代为 **文档即产品、文档即规范** 的项目形态，并为后续“凤凰重生（可选 docs-only）”设定可验收 Gate。

## Distill-1：现状蒸馏（Docs 可独立解释系统）

**输出**：
- 六层能力的“行为说明”：每层做什么、不做什么、关键接口与边界
- 已知问题与设计债务清单（含优先级与影响）
- 文档与实现的偏差记录（不是立刻修代码，而是先把偏差写出来）

**验收（文档验收）**：
- 新人不看代码，仅靠 docs 能解释：系统怎么跑、怎么约束风险、5 个 Story 分别如何演示

## Distill-2：文档即规范（5 个 Story 全部可演示闭环）

**输出**：
- 5 个 Story 全部补齐：演示脚本、输出契约、权限策略、失败降级、六层映射
- `.trae/specs` 的任务拆分与验收标准能直接驱动实现
- `AGENTS.md` 明确：权威矩阵、冲突裁决、DoD

**验收（文档验收）**：
- 任意新增能力必须先更新 `.trae/specs` 与 docs；否则视为“未完成变更”

## Distill-3：docs-only Gate（是否删除代码的决策点）

**Gate 条件（必须同时满足）**：
- docs 覆盖：北极星 + 5 Story + 术语表 + 权威矩阵 + 核心安全原则
- 每个 Story 都有可观察输出契约与审计要求
- 明确“失败边界”与“升级模型/转人工”的条件

**结果**：
- 通过 Gate：允许进入“docs-only”收敛决策（删除范围与保留骨架另行决议）
- 未通过 Gate：禁止进行删除代码的动作，继续完善 docs 与 `.trae/specs`

