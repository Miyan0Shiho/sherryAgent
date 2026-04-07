# SherryAgent - Phoenix Roadmap（docs-only -> 重生实现）产品需求文档

## Overview
- **Summary**: 将仓库推进到 docs-only（Egg），并以 5 个 Story 为中心重建计划体系，为 Chick（最小可实现骨架）与 Phoenix（可落地系统）设定 Gate。
- **Purpose**: “毁掉代码获得新生”，用文档与执行规范先固化系统契约，禁止在 Distill-2 之前讨论/实施重建代码。
- **Target Users**: 后续开发 Agent、人类维护者、面试叙事读者。

## Goals
- 明确当前阶段为 docs-only（Egg），并在入口文档中移除“可运行实现”的误导
- 将 `.trae/specs` 的执行入口重生为 `phoenix-roadmap + story-01..05`
- 清理/归档旧 MVP 体系与 pre-phoenix 计划（避免误用）
- 让 docs/research 在删除代码后仍自洽（去掉 file:/// 与 src/tests 引用）

## Non-Goals
- 不实现任何运行时代码或工具（除非进入 Chick 阶段且通过 Gate）
- 不要求测试、CI、性能基准（docs-only 只做文档验收）

## Functional Requirements
- **FR-1**: `.trae/specs/story-01..05` 成为唯一执行入口（每个都有 spec/tasks/checklist）
- **FR-2**: `.trae/specs/archive/pre-phoenix` 包含全部旧计划（MVP 等），并标注不可执行
- **FR-3**: `docs/INDEX.md` 可导航到 Story Suite、北极星、双权威、legacy、research
- **FR-4**: `docs/legacy/*` 承接“曾经实现的能力快照”，供研究文档引用

## Gate（必须写死）

### Gate-0: docs-only 形态达成
- 工作区不存在 `src/`、`tests/` 等实现目录
- README/AGENTS 不包含任何 “uv run / pytest / mypy src/” 等可运行性承诺

### Gate-1: Distill-2（文档即规范）
- 5 个 Story 都具备：演示脚本 + 输出契约 + 权限策略 + 失败降级 + 六层映射
- research 文档不含 `file:///`，不引用已删除路径

> **强制规则**：未通过 Gate-1，禁止进入“重建实现代码”的讨论与任务分解。

## Acceptance Criteria（文档验收）

### AC-1: 入口正确
- **Given**: 新加入的维护者
- **When**: 从 README/AGENTS/docs/INDEX 开始阅读
- **Then**: 能明确项目处于 docs-only，并能找到 5 个 Story 与执行计划入口
- **Verification**: `human-judgment`

### AC-2: 旧计划不可误用
- **Given**: `.trae/specs` 下存在历史计划
- **When**: 浏览目录
- **Then**: 历史计划被放入 archive/pre-phoenix 或明确标注 archived
- **Verification**: `human-judgment`

