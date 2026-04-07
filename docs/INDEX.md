---
title: "SherryAgent 文档索引"
status: approved
created: 2026-04-03
updated: 2026-04-07
---

# SherryAgent 文档索引

## 面试故事（Story Suite）

> 面试与演示优先从这里开始。每个 Story 都是一个可演示闭环，并明确输出契约、权限策略与失败降级。

| Story | 描述 |
|------|------|
| [story-01-rigorous-dev-copilot.md](stories/story-01-rigorous-dev-copilot.md) | 严谨开发助手：需求澄清 -> 设计 -> 实施 -> Review |
| [story-02-personal-clerk.md](stories/story-02-personal-clerk.md) | 个人助理：安全受控的重复劳动与条件触发 |
| [story-03-ops-sentinel-incident-responder.md](stories/story-03-ops-sentinel-incident-responder.md) | 运维哨兵 + 故障响应：证据收集、runbook、确认与回滚 |
| [story-04-research-miner-security-auditor.md](stories/story-04-research-miner-security-auditor.md) | 调研流水线 + 安全审计：可追溯来源与置信度 |
| [story-05-repo-guardian-release-pilot.md](stories/story-05-repo-guardian-release-pilot.md) | 仓库治理 + 发布编排：门禁、计划、确认与回滚 |

## 北极星与统一口径

| 文档 | 描述 |
|------|------|
| [north-star.md](vision/north-star.md) | 融合愿景与成功定义（唯一北极星） |
| [glossary.md](reference/glossary.md) | 术语表（统一口径） |
| [spec-authority.md](guides/spec-authority.md) | `.trae + docs` 双权威与冲突裁决（硬规则） |
| [story-template.md](standard/story-template.md) | Story 文档模板（后续新增必须遵守） |

## Legacy（蒸馏承接层）

> docs-only 后，历史研究文档不再引用源码路径。所有“曾经实现过的能力快照”统一沉淀在 legacy 中。

| 文档 | 描述 |
|------|------|
| [implementation-snapshot.md](legacy/implementation-snapshot.md) | 已删除代码的能力快照（六层维度） |
| [source-map.md](legacy/source-map.md) | 研究文档引用映射（从源码路径映射到能力锚点） |

## 标准与规范

| 文档 | 描述 |
|------|------|
| [design-principles.md](standard/design-principles.md) | 设计目标与原则 |
| [naming-conventions.md](standard/naming-conventions.md) | 命名规范 |
| [coding-standards.md](standard/coding-standards.md) | 编码标准 |
| [research-template.md](standard/research-template.md) | 技术调研报告模板 |
| [retrospective-template.md](standard/retrospective-template.md) | 复盘报告模板 |

## 技术规范

| 文档 | 描述 |
|------|------|
| [six-layer-architecture.md](specs/six-layer-architecture.md) | 六层融合架构 |
| [runtime-modes.md](specs/runtime-modes.md) | 运行模式设计 |
| [data-flow.md](specs/data-flow.md) | 数据流设计 |
| [agent-loop.md](specs/agent-loop.md) | Agent Loop 模块设计 |
| [memory-system.md](specs/memory-system.md) | 记忆系统模块设计 |
| [task-persistence.md](specs/task-persistence.md) | 任务持久化与断点续传 |
| [heartbeat-engine.md](specs/heartbeat-engine.md) | 心跳引擎模块 |
| [multi-agent-orchestration.md](specs/multi-agent-orchestration.md) | 多Agent编排模块 |
| [permission-system.md](specs/permission-system.md) | 权限系统模块 |
| [observability-system.md](specs/observability-system.md) | 可观测性体系设计 |

## 参考文档

| 文档 | 描述 |
|------|------|
| [tech-stack.md](reference/tech-stack.md) | 技术栈总览 |
| [version-constraints.md](reference/version-constraints.md) | 版本约束 |
| [project-structure.md](reference/project-structure.md) | 项目结构 |
| [technical-metrics.md](reference/technical-metrics.md) | 系统技术指标 |
| [business-metrics.md](reference/business-metrics.md) | 业务指标定义 |

## 实施计划

| 文档 | 描述 |
|------|------|
| [phoenix-roadmap.md](plans/phoenix-roadmap.md) | Egg -> Chick -> Phoenix 重生路线图 |

### 历史计划（Archive）

> 以下文档为 pre-phoenix 历史计划，保留作参考，不再作为执行入口。

| 文档 | 描述 |
|------|------|
| [mvp-roadmap.md](archive/plans/mvp-roadmap.md) | 历史：MVP 实现路线图 |
| [mvp-1-plan.md](archive/plans/mvp-1-plan.md) | 历史：MVP-1 详细计划 |
| [mvp-2-plan.md](archive/plans/mvp-2-plan.md) | 历史：MVP-2 详细计划 |
| [mvp-3-plan.md](archive/plans/mvp-3-plan.md) | 历史：MVP-3 详细计划 |
| [mvp-4-plan.md](archive/plans/mvp-4-plan.md) | 历史：MVP-4 详细计划 |
| [mvp-5-plan.md](archive/plans/mvp-5-plan.md) | 历史：MVP-5 详细计划 |
| [2026-04-07-sherryagent-evolution-plan.md](archive/plans/2026-04-07-sherryagent-evolution-plan.md) | 历史：进化实现计划 |
| [docs-rebirth.md](archive/plans/docs-rebirth.md) | 历史：Docs Rebirth 蒸馏计划 |
| [version-control-migration.md](archive/plans/version-control-migration.md) | 历史：版本控制迁移计划 |

## 研究分析

| 文档 | 描述 |
|------|------|
| [claude-code-analysis.md](research/claude-code-analysis.md) | Claude Code 架构分析 |
| [openclaw-analysis.md](research/openclaw-analysis.md) | OpenClaw 架构分析 |
| [comparison.md](research/comparison.md) | 对比分析 |
| [community-feedback.md](research/community-feedback.md) | 社区评价汇总 |
| [mvp-1-retrospective.md](research/mvp-1-retrospective.md) | MVP-1 开发复盘 |
| [implementation-gap-analysis.md](research/implementation-gap-analysis.md) | 架构实现差距分析 |
| [claude-code-feature-gap.md](research/claude-code-feature-gap.md) | Claude Code 特性差距分析 |
| [openclaw-feature-gap.md](research/openclaw-feature-gap.md) | OpenClaw 特性差距分析 |
| [research-depth-analysis.md](research/research-depth-analysis.md) | 调研深度不足分析 |
| [cli-completeness-evaluation.md](research/cli-completeness-evaluation.md) | CLI 功能完整性评估 |
| [cli-ux-testing.md](research/cli-ux-testing.md) | CLI 用户体验测试报告 |
| [cli-comparison.md](research/cli-comparison.md) | CLI 与 Claude Code 对比 |
| [deep-retrospective.md](research/deep-retrospective.md) | 项目深度反思报告 |

## 操作指南

| 文档 | 描述 |
|------|------|
| （说明） | 该部分多为 pre-phoenix 运行指南与工程实践参考；docs-only（Egg）阶段不承诺可直接运行 |
| [testing-guide.md](guides/testing-guide.md) | 测试运行指南 |
| [plugin-development.md](guides/plugin-development.md) | 插件开发指南 |
| [plugin-best-practices.md](guides/plugin-best-practices.md) | 插件开发最佳实践 |
| [git-workflow.md](guides/git-workflow.md) | Git 工作流规范 |
| [requirement-review.md](guides/requirement-review.md) | 需求评审流程与模板 |
| [technical-research.md](guides/technical-research.md) | 技术预研流程与模板 |
| [testing-strategy.md](guides/testing-strategy.md) | 测试策略改进方案 |
| [sdd-workflow.md](guides/sdd-workflow.md) | 规范驱动开发 (SDD) 工作流指南 |
| [openspec-guide.md](guides/openspec-guide.md) | OpenSpec 方法论参考（非项目权威） |
| [spec-authority.md](guides/spec-authority.md) | 规范权威与冲突裁决 |
