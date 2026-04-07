---
title: "命名规范"
status: approved
created: 2026-04-03
updated: 2026-04-03
---

# 命名规范

## 通用原则

- 使用有意义的、描述性的名称，禁止单字母变量（循环计数器除外）
- 名称长度与作用域成正比：短作用域用短名称，长作用域用完整名称
- 禁止使用缩写（除非是行业通用缩写如 URL、HTTP、API）

## Python 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类/结构体 | PascalCase | `AgentLoop`, `MemoryManager` |
| 函数/方法 | snake_case | `execute_task`, `compact_messages` |
| 变量/参数 | snake_case | `task_id`, `message_list` |
| 常量 | UPPER_SNAKE | `MAX_TOKENS`, `DEFAULT_TIMEOUT` |
| 私有成员 | _prefix | `_internal_state`, `_cache` |
| 模块/包 | snake_case | `agent_loop.py`, `memory_system/` |

## 文件命名规范

- 使用小写 + 短横线：`getting-started.md`、`api-reference.md`
- ADR 使用编号前缀：`adr-001-database-choice.md`
- 设计文档使用日期前缀：`2026-04-01-auth-redesign.md`
- 禁止使用中文文件名（确保跨平台兼容）

## 配置文件命名

| 文件 | 用途 |
|------|------|
| `pyproject.toml` | 项目配置和依赖 |
| `config.toml` | 运行时配置 |
| `.env.example` | 环境变量模板 |
| `AGENT.md` | Agent身份定义 |
| `SKILL.md` | Skill能力声明 |
