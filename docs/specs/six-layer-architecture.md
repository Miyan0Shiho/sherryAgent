---
title: "六层融合架构"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["../standard/design-principles.md", "runtime-modes.md", "data-flow.md"]
---

# 六层融合架构

系统采用六层分层架构，自上而下分别为交互层、编排层、执行层、自主运行层、记忆层和基础设施层。各层职责清晰，通过明确定义的接口进行通信。

## 架构图

```mermaid
graph TB
    subgraph IL["交互层 Interface Layer"]
        CLI["CLI<br/>Textual TUI"]
        WS["WebSocket<br/>实时状态推送"]
        HTTP["HTTP API<br/>RESTful 接口"]
    end

    subgraph OL["编排层 Orchestration Layer"]
        ORC["编排器 Orchestrator<br/>任务分解 / 调度"]
        TM["Agent Teams<br/>Team Lead + Teammate"]
    end

    subgraph EL["执行层 Execution Layer"]
        AL["Agent Loop<br/>流式执行循环"]
        FORK["子 Agent Fork<br/>上下文继承"]
        LANE["Lane 队列<br/>并发控制"]
    end

    subgraph AUL["自主运行层 Autonomy Layer"]
        HB["心跳引擎<br/>While-True 循环"]
        CRON["Cron 调度<br/>APScheduler"]
        RES["断点续传<br/>状态恢复"]
    end

    subgraph ML["记忆层 Memory Layer"]
        STM["短期记忆<br/>四层压缩策略"]
        LTM["长期记忆<br/>SQLite + 向量"]
        BRIDGE["记忆桥接<br/>短期→长期转化"]
    end

    subgraph IFL["基础设施层 Infrastructure Layer"]
        PERM["权限系统<br/>六层管道"]
        SANDBOX["工具沙箱<br/>文件系统 + 网络"]
        MCP["MCP 客户端<br/>外部工具协议"]
        SKILL["Skill 插件<br/>热加载"]
    end

    CLI --> ORC
    WS --> ORC
    HTTP --> ORC
    ORC --> TM
    ORC --> AL
    TM --> AL
    AL --> FORK
    AL --> LANE
    FORK --> AL
    LANE --> AL
    HB --> CRON
    HB --> RES
    CRON --> ORC
    RES --> AL
    AL --> STM
    AL --> LTM
    STM --> BRIDGE
    BRIDGE --> LTM
    AL --> PERM
    AL --> SANDBOX
    AL --> MCP
    AL --> SKILL
    ORC --> LANE

    style IL fill:#e3f2fd,stroke:#1565c0
    style OL fill:#e8f5e9,stroke:#2e7d32
    style EL fill:#fff3e0,stroke:#e65100
    style AUL fill:#fce4ec,stroke:#c62828
    style ML fill:#f3e5f5,stroke:#6a1b9a
    style IFL fill:#eceff1,stroke:#37474f
```

## 各层职责说明

| 层级 | 核心职责 | 关键组件 |
|------|---------|---------|
| 交互层 | 用户输入/输出，多通道适配 | CLI（Textual TUI）、WebSocket、HTTP API |
| 编排层 | 任务分解、子Agent分配、团队协调 | Orchestrator、Agent Teams |
| 执行层 | Agent执行循环、子Agent派生、并发控制 | Agent Loop、Fork、Lane队列 |
| 自主运行层 | 持续运行、定时调度、崩溃恢复 | 心跳引擎、Cron调度、断点续传 |
| 记忆层 | 上下文管理、信息压缩、知识持久化 | 短期记忆、长期记忆、记忆桥接 |
| 基础设施层 | 安全管控、工具执行、插件扩展 | 权限系统、沙箱、MCP、Skill插件 |

## 与原框架的对应关系

| 本框架模块 | Claude Code 对应 | OpenClaw 对应 | 融合方式 |
|-----------|-----------------|--------------|---------|
| Agent Loop | Agent Loop | Agent执行 | 以Claude Code为基础，增加异步流式 |
| 短期记忆 | Context Window Management | - | 直接采用四层压缩策略 |
| 长期记忆 | - | 三层记忆系统 | 直接采用，增加向量检索 |
| 任务持久化 | - | Task Persistence | 直接采用JSONL格式 |
| 心跳引擎 | - | While-True Heartbeat | 直接采用，增加低功耗模式 |
| Cron调度 | - | Cron System | 集成APScheduler替代自研 |
| 编排器 | Orchestrator | - | 直接采用 |
| 子Agent Fork | Sub-Agent Fork | - | 直接采用，增加独立权限 |
| Agent Teams | Agent Teams | - | 直接采用 |
| Lane队列 | - | Lane Queue | 直接采用，增加优先级 |
| 权限系统 | Permission Pipeline | - | 直接采用六层管道 |
| MCP集成 | MCP Client | - | 直接采用 |
| Skill插件 | - | Skill System | 直接采用，增加pluggy框架 |
