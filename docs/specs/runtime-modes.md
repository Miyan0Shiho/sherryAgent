---
title: "运行模式契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/runtime-modes.md"
  - "./core-data-contracts.md"
---

# 运行模式契约

本文件是 `docs/architecture/runtime-modes.md` 的技术契约补充，定义模式在系统中的约束。

## 可用模式

- `interactive-dev`
- `autonomous-safe`
- `background-ops`
- `bulk-analysis`

## 契约要求

- 每个 Task 必须绑定一个 `mode`
- `Planner` 负责模式选择，不能由 Execution Engine 临时决定
- 模式切换必须通过 Decision 留痕
- 模式影响预算、权限、缓存、并发和输出契约严格度

## 约束映射

| Mode | 默认预算 | 默认权限姿态 | 默认并发姿态 |
|------|------|------|------|
| `interactive-dev` | `balanced` / `premium` | 可确认高风险动作 | 中等并发 |
| `autonomous-safe` | `strict` | 只读优先 | 低并发 |
| `background-ops` | `balanced` / `premium` | 修复动作需确认 | 中低并发 |
| `bulk-analysis` | `strict` / `balanced` | 范围受限 | 高并发、异步聚合 |

