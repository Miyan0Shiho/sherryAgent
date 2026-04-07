---
title: "项目结构"
status: approved
created: 2026-04-03
updated: 2026-04-07
related: ["tech-stack.md", "../architecture/system-blueprint.md"]
---

# 项目结构

> 本仓库当前处于 **docs-only / planning-first** 阶段。项目结构反映的是公司级计划体系与系统契约，不是旧实现目录。

```
sherry-agent/
├── README.md                        # 项目总入口
├── AGENTS.md                        # 后续 Agent 的工作规则
├── ARCHITECTURE.md                  # 六层能力的高层说明
├── pyproject.toml                   # 占位元数据
├── docs/
│   ├── INDEX.md                     # 文档总索引
│   ├── vision/                      # 产品章程、北极星
│   ├── architecture/                # 系统蓝图、运行模式、模块图、扩展策略
│   ├── specs/                       # 数据契约与技术规范
│   ├── plans/                       # 统一实现总计划
│   ├── stories/                     # 验收与演示套件
│   ├── guides/                      # 流程、治理、规范权威
│   ├── reference/                   # 术语、结构、指标等参考资料
│   ├── research/                    # 历史研究分析
│   ├── legacy/                      # 已删除实现的能力快照
│   └── archive/                     # 已归档的旧路线图与历史报告
└── .trae/
    └── specs/
        ├── platform-foundation/
        ├── runtime-orchestration/
        ├── memory-knowledge/
        ├── tooling-integration/
        ├── quality-evaluation/
        ├── cost-latency-ops/
        ├── release-program/
        ├── story-01-*/
        ├── story-02-*/
        ├── story-03-*/
        ├── story-04-*/
        ├── story-05-*/
        └── archive/
```

## 目录职责说明

| 目录 | 职责 |
|------|------|
| `docs/vision/` | 产品定位、目标用户、成功定义、长期命题 |
| `docs/architecture/` | 系统上下文、模块边界、运行模式、链路与扩展设计 |
| `docs/specs/` | 数据对象、技术契约、关键模块规范 |
| `docs/plans/` | 顶层实现计划与交付节奏 |
| `docs/stories/` | Story 验收与演示场景 |
| `docs/legacy/` | 历史实现的能力锚点与引用映射 |
| `.trae/specs/platform-foundation/` | 平台底座建设计划 |
| `.trae/specs/runtime-orchestration/` | 运行时、编排与执行计划 |
| `.trae/specs/memory-knowledge/` | 记忆与知识体系计划 |
| `.trae/specs/tooling-integration/` | 工具协议与外部集成计划 |
| `.trae/specs/quality-evaluation/` | 评测、回归、验证计划 |
| `.trae/specs/cost-latency-ops/` | 成本、性能、观测、SRE 计划 |
| `.trae/specs/release-program/` | 项目里程碑、门禁、上线治理计划 |

