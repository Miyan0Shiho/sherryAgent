---
title: "编码标准"
status: approved
created: 2026-04-03
updated: 2026-04-03
---

# 编码标准

## 代码结构

### 函数设计

- 单个函数不超过 30 行
- 参数不超过 4 个，超出时使用对象封装
- 嵌套深度不超过 3 层，超出时使用提前返回
- 禁止布尔参数（使用枚举或配置对象替代）

### 文件组织

- 单个文件不超过 300 行
- 按职责拆分：一个文件一个导出类/模块
- 导入顺序：标准库 → 第三方库 → 项目内部模块
- 禁止循环依赖

## 类型安全

### 使用类型注解

```python
from dataclasses import dataclass
from typing import Any
from collections.abc import AsyncIterator

@dataclass
class AgentEvent:
    event_type: EventType
    content: str
    metadata: dict[str, Any]

async def agent_loop(
    messages: list[dict[str, Any]],
    config: AgentConfig,
) -> AsyncIterator[AgentEvent]:
    ...
```

### 禁止事项

- 禁止使用 `any` / `unknown` 类型绕过类型检查
- 禁止使用 `# type: ignore` 压制类型错误
- 禁止使用 `@ts-ignore` / `@ts-nocheck`

## 错误处理

### 分层异常策略

| 层级 | 处理方式 |
|------|----------|
| 入口层 | 捕获所有异常，转换为统一错误响应 |
| 服务层 | 抛出业务异常，携带错误码和上下文信息 |
| 基础设施层 | 抛出技术异常，携带原始错误信息 |

### 禁止事项

- 禁止捕获 `Exception` / `Throwable` / `Error` 等宽泛类型
- 禁止在 catch 块中仅打印堆栈不做处理
- 禁止使用异常控制程序流程

## 注释规范

### 好注释 vs 坏注释

- ✅ 解释"为什么"（设计决策、业务规则、历史原因）
- ❌ 解释"做什么"（代码本身应该清楚表达）
- ✅ 标注 TODO 时附带 issue 编号和预期时间
- ❌ 注释掉的代码（直接删除，Git 会记住）

### 文档字符串

所有公开 API 必须包含文档字符串，格式如下：

```python
async def compact(
    self, messages: list[dict[str, Any]], level: str = "auto"
) -> list[dict[str, Any]]:
    """
    对消息列表执行压缩，返回压缩后的消息列表。

    Args:
        messages: 当前对话消息列表
        level: 压缩级别 (micro/auto/session/reactive)

    Returns:
        压缩后的消息列表

    Raises:
        CompactionError: 压缩过程中遇到错误
    """
    ...
```
