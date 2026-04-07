---
title: "项目结构"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["tech-stack.md", "../specs/six-layer-architecture.md"]
---

# 项目结构

```
sherry-agent/
├── pyproject.toml              # 项目配置与依赖
├── README.md                   # 项目说明
├── AGENTS.md                   # AI Agent 入口指南
├── ARCHITECTURE.md             # 架构概述
├── src/
│   └── sherry_agent/
│       ├── __init__.py
│       ├── cli/                    # 交互层 Interface Layer
│       │   ├── __init__.py
│       │   ├── app.py              # Textual TUI应用
│       │   ├── commands.py         # click命令定义
│       │   └── widgets/            # TUI组件
│       │       ├── __init__.py
│       │       ├── chat.py         # 聊天面板
│       │       ├── status.py       # 状态栏
│       │       └── task_list.py    # 任务列表
│       ├── orchestration/          # 编排层 Orchestration Layer
│       │   ├── __init__.py
│       │   ├── orchestrator.py     # 任务编排器
│       │   ├── teams.py            # Agent Teams
│       │   ├── lane.py             # Lane队列
│       │   └── decomposer.py       # 任务分解器
│       ├── execution/              # 执行层 Execution Layer
│       │   ├── __init__.py
│       │   ├── loop.py             # Agent Loop
│       │   ├── fork.py             # 子Agent Fork
│       │   ├── tools.py            # 工具执行器
│       │   └── tools/              # 内置工具
│       │       ├── __init__.py
│       │       ├── file_ops.py     # 文件操作
│       │       ├── shell.py        # Shell执行
│       │       └── http.py         # HTTP请求
│       ├── autonomy/               # 自主运行层 Autonomy Layer
│       │   ├── __init__.py
│       │   ├── heartbeat.py        # 心跳引擎
│       │   ├── scheduler.py        # Cron调度
│       │   └── recovery.py         # 断点续传
│       ├── memory/                 # 记忆层 Memory Layer
│       │   ├── __init__.py
│       │   ├── short_term.py       # 短期记忆（压缩）
│       │   ├── long_term.py        # 长期记忆（SQLite+向量）
│       │   ├── bridge.py           # 记忆桥接
│       │   └── embedding.py        # 向量化
│       ├── infrastructure/         # 基础设施层 Infrastructure Layer
│       │   ├── __init__.py
│       │   ├── permissions.py      # 权限系统
│       │   ├── sandbox.py          # 工具沙箱
│       │   ├── mcp_client.py       # MCP客户端
│       │   └── plugins.py          # Skill插件系统
│       ├── models/                 # 数据模型
│       │   ├── __init__.py
│       │   ├── events.py           # 事件类型
│       │   ├── tasks.py            # 任务模型
│       │   ├── memory.py           # 记忆模型
│       │   └── config.py           # 配置模型
│       ├── llm/                    # LLM调用
│       │   ├── __init__.py
│       │   ├── anthropic.py        # Anthropic SDK封装
│       │   ├── openai.py           # OpenAI SDK封装
│       │   └── base.py             # 抽象基类
│       └── config/                 # 配置
│           ├── __init__.py
│           ├── settings.py         # Pydantic Settings
│           └── defaults.toml       # 默认配置
├── tests/                          # 测试
│   ├── __init__.py
│   ├── conftest.py                 # pytest配置
│   ├── unit/                       # 单元测试
│   │   ├── __init__.py
│   │   ├── test_loop.py
│   │   ├── test_memory.py
│   │   └── test_permissions.py
│   ├── integration/                # 集成测试
│   │   ├── __init__.py
│   │   ├── test_agent_flow.py
│   │   └── test_persistence.py
│   └── e2e/                        # 端到端测试
│       ├── __init__.py
│       └── test_cli.py
├── docs/                           # 文档
│   ├── INDEX.md                    # 文档索引
│   ├── standard/                   # 标准与规范
│   ├── guides/                     # 操作指南
│   ├── reference/                  # 参考文档
│   ├── specs/                      # 技术规范
│   ├── plans/                      # 实施计划
│   └── research/                   # 研究分析
├── .trae/                          # Trae配置
│   └── specs/                      # MVP规范
│       ├── mvp-1-core-agent-loop/
│       ├── mvp-2-memory-persistence/
│       ├── mvp-3-autonomy/
│       ├── mvp-4-orchestration/
│       └── mvp-5-plugin-ecosystem/
└── skills/                         # Skill插件目录
    └── example-skill/
        └── SKILL.md
```

## 目录职责说明

| 目录 | 职责 |
|------|------|
| `cli/` | 用户交互入口，TUI界面，命令解析 |
| `orchestration/` | 任务分解，子Agent调度，团队协调 |
| `execution/` | Agent执行循环，工具调用，Fork管理 |
| `autonomy/` | 心跳驱动，定时调度，崩溃恢复 |
| `memory/` | 上下文压缩，长期记忆，知识检索 |
| `infrastructure/` | 权限控制，沙箱隔离，插件加载 |
| `models/` | 数据结构定义，类型注解 |
| `llm/` | LLM API封装，流式调用 |
| `config/` | 配置加载，环境变量 |
