---
title: "Phoenix Roadmap（Egg -> Chick -> Phoenix）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../stories/story-01-rigorous-dev-copilot.md"
  - "../guides/spec-authority.md"
---

# Phoenix Roadmap（Egg -> Chick -> Phoenix）

本路线图用于将 SherryAgent 从 **docs-only（Egg）** 推进到可运行的“重生实现”（Chick）并最终演化为 Phoenix。

## 当前阶段：Egg（docs-only）

定义：
- 仓库不保留可运行实现代码
- `docs/` 是唯一产品与系统契约
- `.trae/specs/` 是唯一开发执行权威

Gate（进入 Chick 之前必须满足）：
- 5 个 Story 的演示脚本、输出契约、权限策略、失败降级齐全
- 研究文档不引用任何 `file:///...`、`src/`、`tests/` 路径
- `AGENTS.md` 与 `docs/guides/spec-authority.md` 写死权威矩阵与冲突裁决

## 下一阶段：Chick（最小可实现骨架）

目标：
- 只实现“让 Story 可跑起来所需的最小骨架”，避免回到大而全 demo
- 以 Story 为入口做实现，而不是以模块堆叠为入口

最小骨架原则：
- 每个 Story 只实现其最小闭环路径
- 默认只读 + 审计；高风险必须确认；CRITICAL 默认拒绝
- 先可观察性（状态/审计/回放），后能力扩展

## 未来阶段：Phoenix（可落地系统）

Phoenix 只作为愿景阶段描述，不与当前实现承诺绑定：
- 多模型适配与“能力放大”评测体系完善（qwen3:0.6b 裸奔 vs 加持）
- 更完整的自主运行、编排、记忆与权限生态
- 可持续迭代的 Story Suite 扩展机制

