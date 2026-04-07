---
title: "设计目标与原则"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["../specs/six-layer-architecture.md"]
---

# 设计目标与原则

## 融合目标

本方案旨在将 Claude Code 与 OpenClaw 两个优秀 AI Agent 框架的核心优势进行深度融合，构建一个兼具交互深度与自主运行能力的 Python 多 Agent 框架。

### 取自 Claude Code 的核心能力

| 能力 | 说明 |
|------|------|
| 编排器-子Agent架构 | 主Agent负责任务分解与调度，子Agent独立执行子任务，形成层次化的任务处理体系 |
| 四层上下文压缩策略 | micro-compact、auto-compact、session memory compact、reactive compact 四级渐进压缩，最大化上下文窗口利用率 |
| 六层权限管道 | 从工具声明到沙箱隔离的六层纵深防御，覆盖所有执行路径 |
| Fork优化 | 子Agent继承父Agent系统提示前缀，复用 prompt cache，降低冷启动成本 |
| MCP集成 | 通过 Model Context Protocol 连接外部工具服务器，扩展工具生态 |
| Agent Teams点对点通信 | Team Lead 协调 Teammate，共享任务列表与消息邮箱，支持并行协作 |

### 取自 OpenClaw 的核心能力

| 能力 | 说明 |
|------|------|
| 心跳机制（While-True循环） | 持续运行的自主循环，定期检查待办、调度任务、更新状态 |
| 任务持久化与断点续传 | 任务状态、执行日志、进度看板全部落盘，崩溃后可从断点恢复 |
| 三层记忆系统 | 身份层（我是谁）、操作层（我会什么）、记忆层（我知道什么），结构化长期记忆 |
| Cron调度系统 | 基于时间表达式的周期性任务调度，支持定时检查、定期汇报等场景 |
| Lane队列并发控制 | 双层排队机制（session串行 + global并发），精确控制并发度 |
| Skill插件热加载 | 运行时动态加载/卸载技能插件，无需重启即可扩展Agent能力 |

## 设计原则

### 模块化（Modularity）

每个核心能力封装为独立模块，通过明确定义的接口交互。模块可独立替换、升级或禁用，不影响系统整体运行。例如，记忆系统可从 SQLite 切换到 PostgreSQL，权限系统可从六层简化为三层。

### 渐进式（Progressive）

采用 MVP（Minimum Viable Product）策略，先实现核心路径（Agent Loop + 基础工具），再逐步扩展记忆、持久化、多Agent编排等高级能力。每个阶段都有明确的验收标准。

### Python原生（Pythonic）

充分利用 Python 3.12+ 的异步生态（asyncio、async for、TaskGroup），使用类型注解（typing）、数据类（dataclass）、Pydantic 模型确保类型安全，遵循 PEP 规范。

### 安全优先（Security First）

权限系统贯穿所有执行路径，从工具声明到沙箱隔离形成纵深防御。后台自主模式下启用审计日志和异常告警，确保无人值守时的安全性。

### 本地优先（Local First）

所有数据（任务状态、记忆、配置）存储在本地文件系统，用户完全掌控。不依赖外部云服务即可完整运行，可选接入云端LLM和工具服务。
