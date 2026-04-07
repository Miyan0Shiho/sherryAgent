# SherryAgent - Docs Rebirth（文档驱动重生）产品需求文档

## Overview
- **Summary**: 将 SherryAgent 从“已有代码的 demo”重置为“文档即产品、文档即规范、可讲 5 个故事”的项目形态。
- **Purpose**: 建立 `.trae/specs` + `docs/` 双权威体系，完成 Distill-1/2/3 三阶段蒸馏，为后续重生（可选 docs-only）铺路。
- **Target Users**: 项目维护者、后续 Agent 开发者、面试官/读者。

## Goals
- 写清北极星文档（融合愿景、成功指标、失败边界）
- 固化 5 个官方 Story 套件（演示脚本 + 输出契约 + 权限策略 + 失败降级 + 六层映射）
- 写死双权威矩阵与冲突裁决（避免 `.trae`/`docs`/OpenSpec 互相打架）
- 建立 Distill-1/2/3 的可验收 Gate（不要求测试，只要求文档验收）
- 统一术语与命名（清除历史 “Fusion Agent” 残留）

## Non-Goals (Out of Scope)
- 不要求立刻重构/保留/删除代码（删除代码属于 Distill-3 Gate 后的单独决策）
- 不要求新增工程功能（本 spec 的交付物是 docs 与规范体系）

## Functional Requirements
- **FR-1**: 生成并维护 `docs/vision/north-star.md`
- **FR-2**: 生成并维护 `docs/stories/` 下 5 个 Story 文档（按统一模板）
- **FR-3**: 生成并维护 `docs/reference/glossary.md` 术语表
- **FR-4**: 在 `AGENTS.md` 写清 Spec Authority、冲突裁决、DoD 与推荐阅读路径
- **FR-5**: 更新 `docs/INDEX.md`：Story Suite 作为第一入口
- **FR-6**: 明确 OpenSpec 在 SherryAgent 的定位为“参考模板”，不作为权威规范来源
- **FR-7**: 定义 Distill-1/2/3 Gate（文档验收口径）并固化为计划文档

## Acceptance Criteria（文档验收）

### AC-1: 北极星可回指
- **Given**: 任意 Story 或关键规范文档
- **When**: 阅读该文档
- **Then**: 能回指到北极星中的融合命题、成功指标或失败边界
- **Verification**: `human-judgment`

### AC-2: Story 套件可演示
- **Given**: 5 个 Story 文档
- **When**: 逐个阅读演示脚本与输出契约
- **Then**: 每个 Story 都是可演示闭环，且权限策略与失败降级明确
- **Verification**: `human-judgment`

### AC-3: 双权威不打架
- **Given**: 新增/修改需求
- **When**: 查看 `AGENTS.md` 与 `docs/guides/spec-authority.md`
- **Then**: 明确 `.trae/specs` 与 `docs/` 的权威边界、冲突裁决与 DoD
- **Verification**: `human-judgment`

### AC-4: Distill Gate 明确
- **Given**: Distill 计划
- **When**: 阅读计划文档
- **Then**: Distill-1/2/3 的输出与 Gate 条件明确，可用于后续推进与决策
- **Verification**: `human-judgment`

