---
title: "规范驱动工作流"
status: approved
created: 2026-04-07
updated: 2026-04-07
related:
  - "./spec-authority.md"
  - "./openspec-guide.md"
  - "../plans/implementation-program.md"
---

# 规范驱动工作流

SherryAgent 当前采用的是 **planning-first 的规范驱动工作流**，不是“先写实现再补文档”。

## 当前工作流

1. 在 `.trae/specs/<主线>/` 中定义执行计划。
2. 在 `docs/vision/`, `docs/architecture/`, `docs/specs/` 中落系统契约。
3. 在 `docs/stories/` 中补验收与演示套件。
4. 用 `docs/INDEX.md` 暴露导航入口。
5. 进入未来实现阶段后，再补测试、评测、发布与运维细节。

## 当前规则

- `.trae/specs` 决定做什么。
- `docs/*` 决定系统是什么。
- `docs/stories/*` 决定如何验收和演示。
- OpenSpec 只提供写法参考，不提供权威约束。

## 当前不采用的旧流程

- 不再以 `openspec/changes/*` 作为执行入口。
- 不再把 proposal/design/tasks 当成独立于 `.trae/specs` 的平行体系。

