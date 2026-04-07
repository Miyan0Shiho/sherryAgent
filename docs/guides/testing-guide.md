---
title: "测试运行指南（Legacy）"
status: archived
created: 2026-04-03
updated: 2026-04-07
related:
  - "../INDEX.md"
  - "../plans/phoenix-roadmap.md"
---

# 测试运行指南（Legacy）

> 说明：本仓库当前处于 **docs-only（Egg）**，已不包含可运行实现与测试目录。本文档保留为 pre-phoenix 的工程实践参考，供未来进入 Chick 阶段后重建测试体系时复用。

## 概述

本指南介绍如何运行和管理 SherryAgent 项目的测试套件，确保代码质量和功能可靠性。

## 测试环境设置

### 1. 安装依赖

```bash
# 安装开发依赖
uv sync --extra dev
```

### 2. 配置环境

- **Ollama 本地服务**（可选，用于集成测试）：
  - 安装 Ollama：https://ollama.com/download
  - 下载 qwen3:0.6b 模型：`ollama pull qwen3:0.6b`
  - 启动 Ollama 服务

- **API 密钥**（可选，用于云端 LLM 测试）：
  - 在 `.env` 文件中配置 API 密钥
  - 参考 `.env.example` 文件

## 运行测试

### 1. 运行所有测试

```bash
# 运行所有测试
uv run pytest

# 运行所有测试并生成覆盖率报告
uv run pytest --cov=src --cov-report=html --cov-report=term
```

### 2. 按类型运行测试

```bash
# 运行单元测试
uv run pytest tests/unit/

# 运行集成测试
uv run pytest tests/integration/

# 运行端到端测试
uv run pytest tests/e2e/
```

### 3. 按标记运行测试

```bash
# 运行 Ollama 相关测试
uv run pytest -m ollama

# 运行安全相关测试
uv run pytest -m security

# 运行端到端测试
uv run pytest -m e2e

# 运行集成测试
uv run pytest -m integration
```

### 4. 运行特定测试文件

```bash
# 运行特定测试文件
uv run pytest tests/unit/execution/test_agent_loop.py

# 运行特定测试函数
uv run pytest tests/unit/execution/test_agent_loop.py::test_agent_loop_basic
```

## 测试覆盖率分析

### 1. 生成覆盖率报告

```bash
# 生成 HTML 覆盖率报告
uv run pytest --cov=src --cov-report=html

# 查看报告
open htmlcov/index.html
```

### 2. 覆盖率指标

- **核心逻辑覆盖率**：目标 > 80%
- **工具模块覆盖率**：目标 > 90%
- **安全模块覆盖率**：目标 100%

## 测试最佳实践

### 1. 测试编写原则

- **原子性**：每个测试只测试一个功能点
- **独立性**：测试之间不应相互依赖
- **可重复性**：测试结果应该是可重复的
- **清晰性**：测试代码应该易于理解
- **完整性**：覆盖正常和异常场景

### 2. 测试文件结构

```
tests/
├── unit/         # 单元测试
├── integration/  # 集成测试
└── e2e/         # 端到端测试
```

### 3. 测试命名规范

- **文件命名**：`test_<module_name>.py`
- **类命名**：`Test<ModuleName>`
- **方法命名**：`test_<functionality>_<scenario>`

### 4. 模拟和桩

- 对外部依赖使用模拟（Mock）
- 对网络请求使用桩（Stub）
- 对文件系统操作使用临时文件

### 5. 测试标记

使用以下标记对测试进行分类：
- `@pytest.mark.unit` - 单元测试
- `@pytest.mark.integration` - 集成测试
- `@pytest.mark.e2e` - 端到端测试
- `@pytest.mark.ollama` - Ollama 相关测试
- `@pytest.mark.security` - 安全相关测试
- `@pytest.mark.slow` - 慢速测试

## 常见问题排查

### 1. 测试失败

- 检查环境配置
- 检查依赖版本
- 检查 Ollama 服务是否运行
- 检查 API 密钥是否正确

### 2. 覆盖率低

- 分析覆盖率报告，识别未覆盖的代码
- 为未覆盖的代码添加测试
- 关注核心逻辑和关键路径

### 3. 测试运行缓慢

- 识别并标记慢速测试
- 并行运行测试：`uv run pytest -n auto`
- 优化测试设置和清理

## CI/CD 集成

在 CI/CD 流程中，建议运行以下测试：

```bash
# 运行所有测试并检查覆盖率
uv run pytest --cov=src --cov-fail-under=80

# 运行静态分析
uv run mypy src/
uv run ruff check src/
```

## 总结

通过遵循本指南，您可以：
- 确保代码质量和功能可靠性
- 快速定位和修复问题
- 建立良好的测试习惯
- 为项目的持续集成提供保障
