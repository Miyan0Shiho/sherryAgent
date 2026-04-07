---
title: "版本约束"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["tech-stack.md"]
---

# 版本约束

## 核心依赖版本

| 依赖 | 最低版本 | 说明 |
|------|---------|------|
| Python | >= 3.12 | 需要TaskGroup、type alias、改进的错误信息 |
| anthropic | >= 0.40 | 流式响应、prompt cache、tool use |
| openai | >= 1.50 | 结构化输出、function calling |
| textual | >= 3.0 | TUI框架 |
| aiosqlite | >= 0.20 | 异步SQLite |
| sqlite-vec | >= 0.1 | SQLite向量扩展 |
| APScheduler | >= 3.10 | 异步调度器 |
| pydantic | >= 2.10 | 数据验证和序列化 |
| structlog | >= 24.0 | 结构化日志 |
| pluggy | >= 1.5 | 插件框架 |
| fastapi | >= 0.115 | HTTP API框架 |
| websockets | >= 13.0 | WebSocket支持 |
| pytest | >= 8.0 | 测试框架 |
| pytest-asyncio | >= 0.24 | 异步测试支持 |

## Python 3.12+ 特性依赖

### TaskGroup

```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(execute_tool(tool1))
    task2 = tg.create_task(execute_tool(tool2))
# 自动等待所有任务完成，异常自动传播
```

### Type Alias

```python
type Message = dict[str, Any]
type ToolResult = tuple[str, str]  # (call_id, result)
```

### 改进的错误信息

Python 3.12 提供更清晰的错误追踪，便于调试异步代码。

## pyproject.toml 示例

```toml
[project]
name = "sherry-agent"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "anthropic>=0.40",
    "openai>=1.50",
    "textual>=3.0",
    "aiosqlite>=0.20",
    "sqlite-vec>=0.1",
    "apscheduler>=3.10",
    "pydantic>=2.10",
    "pydantic-settings>=2.6",
    "structlog>=24.0",
    "pluggy>=1.5",
    "fastapi>=0.115",
    "websockets>=13.0",
    "click>=8.1",
    "sentence-transformers>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "ruff>=0.6",
    "mypy>=1.11",
]
