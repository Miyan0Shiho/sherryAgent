---
title: "项目结构"
status: approved
created: 2026-04-03
updated: 2026-04-07
related: ["tech-stack.md", "../specs/six-layer-architecture.md"]
---

# 项目结构

> 本仓库当前处于 **docs-only（Egg）**：不包含可运行实现代码。项目结构描述的是“文档即产品/契约”与“执行计划即权威”的形态。

```
sherry-agent/
├── README.md                   # 项目说明（docs-only 入口）
├── AGENTS.md                   # AI Agent 工作规则（docs-only）
├── ARCHITECTURE.md             # 架构概述（六层口径）
├── pyproject.toml              # 占位元数据（docs-only 阶段不承诺可运行）
├── docs/                       # 文档（唯一产品与系统契约）
│   ├── INDEX.md                # 文档索引（Story Suite 为第一入口）
│   ├── vision/                 # 北极星与愿景
│   ├── stories/                # 5 个官方 Story 套件
│   ├── legacy/                 # 实现蒸馏承接层（无源码）
│   ├── standard/               # 标准与规范
│   ├── guides/                 # 操作指南（含双权威规则）
│   ├── reference/              # 参考（术语表等）
│   ├── specs/                  # 技术规范（契约口径）
│   ├── plans/                  # Phoenix 重生计划
│   ├── research/               # 历史研究（去代码链接后保留结论）
│   └── archive/                # 历史资料归档
└── .trae/                      # 执行计划（唯一开发执行权威）
    └── specs/
        ├── phoenix-roadmap/    # Egg -> Chick -> Phoenix 汇总 Gate
        ├── story-01-*/         # 每个 Story 的 spec/tasks/checklist
        └── archive/            # 历史计划（pre-phoenix）
```

## 目录职责说明

| 目录 | 职责 |
|------|------|
| `docs/stories/` | 面试入口与场景闭环契约（5 个官方 Story） |
| `docs/vision/` | 北极星：融合命题、成功指标、失败边界 |
| `docs/specs/` | 技术契约：六层架构、权限、数据流、可观测性等 |
| `docs/standard/` | 文档与工程写作标准（模板、命名等） |
| `docs/guides/` | 操作与流程指南（含双权威与冲突裁决） |
| `docs/legacy/` | 已删除实现的“能力快照”承接层（只允许锚点引用，不含源码） |
| `docs/research/` | 历史研究与分析（已去除对 `src/`、`tests/` 等已删除路径的引用） |
| `docs/plans/` | Phoenix 重生计划（Egg -> Chick -> Phoenix） |
| `.trae/specs/` | 唯一开发执行权威（做什么、验收是什么、如何拆分） |

> 说明：六层架构中的“交互/编排/执行/自主/记忆/基础设施”在 docs-only 阶段以 **契约文档** 表达，不以代码目录结构表达。
