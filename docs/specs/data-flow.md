---
title: "数据流设计"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["six-layer-architecture.md"]
---

# 数据流设计

以下序列图展示了从用户输入到最终状态更新的完整数据流，涵盖编排、执行、记忆、持久化各环节的交互。

## 完整数据流

```mermaid
sequenceDiagram
    participant U as 用户
    participant IF as 交互层
    participant ORC as 编排器
    participant LANE as Lane队列
    participant AGT as 子Agent
    participant MEM as 记忆系统
    participant PERS as 持久化

    U->>IF: 输入任务指令
    IF->>ORC: 解析并提交任务
    ORC->>ORC: 任务分解为子任务
    ORC->>LANE: 提交子任务到队列
    LANE->>AGT: 调度子Agent执行
    AGT->>AGT: Agent Loop 执行
    AGT->>MEM: 查询/更新记忆
    MEM-->>AGT: 返回相关上下文
    AGT->>PERS: 追加执行日志
    PERS-->>AGT: 确认持久化
    AGT-->>LANE: 返回执行结果
    LANE-->>ORC: 汇总子任务结果
    ORC->>MEM: 持久化长期记忆
    ORC->>PERS: 更新任务状态
    ORC-->>IF: 推送最终结果
    IF-->>U: 展示结果/状态更新
```

## 任务状态机

```mermaid
stateDiagram-v2
    [*] --> Pending: 创建任务
    Pending --> Running: 开始执行
    Running --> Suspended: 中断/崩溃
    Running --> Completed: 执行成功
    Running --> Failed: 执行失败（不可恢复）
    Suspended --> Running: 断点续传
    Suspended --> Failed: 恢复失败
    Completed --> [*]
    Failed --> [*]

    state Running {
        [*] --> StepExec
        StepExec --> ToolCall: 需要工具
        ToolCall --> StepExec: 工具返回
        StepExec --> StepDone: 步骤完成
        StepDone --> StepExec: 下一步
        StepDone --> [*]: 所有步骤完成
    }
```

## 持久化格式

```
tasks/
└── {task-id}/
    ├── state.json          # 任务元数据与状态
    ├── transcript.jsonl    # 执行日志（追加写入）
    ├── heartbeat.md        # 人类可读进度看板
    └── context_snapshot/   # 上下文快照（可选）
        └── latest.msgpack
```
