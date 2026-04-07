# 项目最小骨架搭建 Spec

## Why
项目文档体系已完整，但缺少实际的代码框架。需要创建最小骨架让项目可以运行起来，为后续 MVP-1 开发做准备。

## What Changes
- 创建 `pyproject.toml` 项目配置文件
- 创建 `src/sherry_agent/` 目录结构
- 创建各模块的 `__init__.py` 文件
- 创建基础配置文件（.env.example, .gitignore）
- 创建 tests/ 目录结构

## Impact
- Affected specs: 无
- Affected code: 新建所有代码文件

## ADDED Requirements

### Requirement: 项目配置
系统 SHALL 提供 pyproject.toml 配置文件，定义项目元数据和依赖。

#### Scenario: 依赖安装
- **WHEN** 用户执行 `uv sync`
- **THEN** 所有依赖被正确安装

### Requirement: 目录结构
系统 SHALL 提供完整的源码目录结构。

#### Scenario: 目录创建
- **WHEN** 搭建完成
- **THEN** 存在以下目录：
  - src/sherry_agent/cli/
  - src/sherry_agent/orchestration/
  - src/sherry_agent/execution/
  - src/sherry_agent/autonomy/
  - src/sherry_agent/memory/
  - src/sherry_agent/infrastructure/
  - src/sherry_agent/models/
  - src/sherry_agent/llm/
  - src/sherry_agent/config/
  - tests/unit/
  - tests/integration/
  - tests/e2e/
