# SherryAgent 架构概述

本文档提供 SherryAgent 系统架构的高层概览，帮助开发者快速理解系统设计。

## 六层融合架构

SherryAgent 采用六层分层架构，融合了 Claude Code 的编排精度和 OpenClaw 的自主运行能力。

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

## 各层职责

| 层级 | 核心职责 | 关键组件 |
|------|---------|---------|
| **交互层** | 用户输入/输出，多通道适配 | CLI（Textual TUI）、WebSocket、HTTP API |
| **编排层** | 任务分解、子Agent分配、团队协调 | Orchestrator、Agent Teams |
| **执行层** | Agent执行循环、子Agent派生、并发控制 | Agent Loop、Fork、Lane队列 |
| **自主运行层** | 持续运行、定时调度、崩溃恢复 | 心跳引擎、Cron调度、断点续传 |
| **记忆层** | 上下文管理、信息压缩、知识持久化 | 短期记忆、长期记忆、记忆桥接 |
| **基础设施层** | 安全管控、工具执行、插件扩展 | 权限系统、沙箱、MCP、Skill插件 |

## 运行模式

系统支持三种运行模式：

| 模式 | 特征 | 适用场景 |
|------|------|----------|
| **CLI 交互模式** | 同步阻塞、人工监督、实时流式输出 | 开发、调试 |
| **后台自主模式** | 异步非阻塞、心跳驱动、自动决策 | 监控、巡检、自动化运维 |
| **混合模式** | 模式热切换、WebSocket状态推送 | 编译、部署、批量处理 |

## 数据流

```mermaid
sequenceDiagram
    participant U as 用户
    participant IF as 交互层
    participant ORC as 编排器
    participant AGT as 子Agent
    participant MEM as 记忆系统
    participant PERS as 持久化

    U->>IF: 输入任务指令
    IF->>ORC: 解析并提交任务
    ORC->>ORC: 任务分解为子任务
    ORC->>AGT: 调度子Agent执行
    AGT->>AGT: Agent Loop 执行
    AGT->>MEM: 查询/更新记忆
    MEM-->>AGT: 返回相关上下文
    AGT->>PERS: 追加执行日志
    AGT-->>ORC: 返回执行结果
    ORC->>MEM: 持久化长期记忆
    ORC-->>IF: 推送最终结果
    IF-->>U: 展示结果/状态更新
```

## 模块依赖关系

```mermaid
graph TD
    CLI[cli] --> ORC[orchestration]
    ORC --> EXEC[execution]
    EXEC --> MEM[memory]
    EXEC --> INFRA[infrastructure]
    MEM --> MODELS[models]
    INFRA --> MODELS
    AUTO[autonomy] --> EXEC
    AUTO --> MEM
    ORC --> AUTO
```

## 详细文档

| 主题 | 文档 |
|------|------|
| 六层架构详解 | [docs/specs/six-layer-architecture.md](docs/specs/six-layer-architecture.md) |
| Agent Loop 设计 | [docs/specs/agent-loop.md](docs/specs/agent-loop.md) |
| 记忆系统设计 | [docs/specs/memory-system.md](docs/specs/memory-system.md) |
| 权限系统设计 | [docs/specs/permission-system.md](docs/specs/permission-system.md) |
| 多Agent编排设计 | [docs/specs/multi-agent-orchestration.md](docs/specs/multi-agent-orchestration.md) |
| 心跳引擎设计 | [docs/specs/heartbeat-engine.md](docs/specs/heartbeat-engine.md) |
| 项目结构 | [docs/reference/project-structure.md](docs/reference/project-structure.md) |
