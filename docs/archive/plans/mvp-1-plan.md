---
title: "MVP-1 核心Agent Loop 详细计划"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["mvp-roadmap.md"]
---

# MVP-1 核心Agent Loop 详细计划

## 目标

实现最小可用的Agent执行循环，能够在CLI中完成简单的文件操作任务，包括基础的LLM推理、工具执行和权限控制。

## 实现范围

- 基础Agent Loop：消息输入 → LLM推理 → 工具执行 → 结果反馈
- 流式输出：CLI实时显示LLM生成的文本和工具执行过程
- 3个基础工具：文件读写、Shell执行、HTTP请求
- 基础权限系统：第1层（工具声明）+ 第2层（全局安全规则）+ 第6层（沙箱）
- CLI交互模式：Textual TUI基础界面

## 任务列表

### Week 1

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T1.1 | 项目初始化与基础结构搭建 | P0 |
| T1.2 | 数据模型与事件系统实现 | P0 |
| T1.3 | Agent Loop核心实现 | P0 |

### Week 2

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T2.1 | 基础工具实现（文件、Shell、HTTP） | P0 |
| T2.2 | 基础权限系统实现 | P0 |
| T2.3 | CLI交互界面实现 | P1 |
| T2.4 | 集成测试与调试 | P1 |

## 技术要点

### Agent Loop 核心代码

```python
async def agent_loop(
    messages: list[dict[str, Any]],
    config: AgentConfig,
    tool_executor: ToolExecutor,
    cancellation_token: CancellationToken | None = None,
) -> AsyncIterator[AgentEvent]:
    """Agent核心执行循环"""
    token_tracker = TokenTracker(config.token_budget)

    for round_index in range(config.max_tool_rounds):
        if cancellation_token and cancellation_token.is_cancelled:
            yield AgentEvent(EventType.ERROR, "执行被用户中止")
            return

        # 调用LLM获取响应
        response = await call_llm(messages, config, token_tracker)

        # 处理文本输出
        if response.text_content:
            yield AgentEvent(
                EventType.TEXT,
                response.text_content,
                token_usage=token_tracker.current_usage,
            )

        # 处理工具调用
        if not response.tool_calls:
            break

        # 执行工具调用
        for call in response.tool_calls:
            result = await tool_executor.execute(call)
            yield AgentEvent(EventType.TOOL_RESULT, result.summary)
            messages.append(result.to_message())
```

### 工具定义示例

```python
@tool(
    name="read_file",
    description="读取文件内容",
    parameters={
        "path": {"type": "string", "description": "文件路径"}
    },
    permissions=[Permission.READ]
)
async def read_file(path: str) -> str:
    """读取指定路径的文件内容"""
    with open(path, 'r') as f:
        return f.read()
```

## 验收标准

| 编号 | 验收条件 | 验证方式 |
|------|---------|---------|
| 1.1 | CLI启动后能接收用户输入 | 手动测试 |
| 1.2 | LLM响应流式输出到终端 | 观察输出 |
| 1.3 | 能调用文件读写工具完成文件操作 | 端到端测试 |
| 1.4 | 能调用Shell工具执行命令 | 端到端测试 |
| 1.5 | 危险命令被权限系统拦截 | 单元测试 |
| 1.6 | 用户可中止正在执行的任务 | 手动测试 |

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| LLM API调用延迟 | 用户体验差 | 实现流式输出，提供实时反馈 |
| 权限系统过于严格 | 阻碍正常操作 | 提供用户可配置的权限规则 |
| CLI界面复杂度 | 开发周期延长 | 保持界面简洁，专注核心功能 |
