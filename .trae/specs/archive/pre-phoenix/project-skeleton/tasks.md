# 项目最小骨架搭建任务

## [x] Task 1: 创建 pyproject.toml
- **Description**: 创建项目配置文件，定义元数据、依赖和入口点
- **SubTasks**:
  - [x] 定义项目元数据（name, version, description）
  - [x] 定义 Python 版本要求（>=3.12）
  - [x] 定义核心依赖
  - [x] 定义开发依赖（pytest, mypy, ruff）
  - [x] 定义 CLI 入口点

## [x] Task 2: 创建源码目录结构
- **Description**: 创建 src/sherry_agent/ 下的所有模块目录
- **SubTasks**:
  - [x] 创建 cli/ 目录及 __init__.py
  - [x] 创建 orchestration/ 目录及 __init__.py
  - [x] 创建 execution/ 目录及 __init__.py
  - [x] 创建 autonomy/ 目录及 __init__.py
  - [x] 创建 memory/ 目录及 __init__.py
  - [x] 创建 infrastructure/ 目录及 __init__.py
  - [x] 创建 models/ 目录及 __init__.py
  - [x] 创建 llm/ 目录及 __init__.py
  - [x] 创建 config/ 目录及 __init__.py
  - [x] 创建顶层 __init__.py

## [x] Task 3: 创建测试目录结构
- **Description**: 创建 tests/ 下的所有测试目录
- **SubTasks**:
  - [x] 创建 tests/unit/ 目录及 __init__.py
  - [x] 创建 tests/integration/ 目录及 __init__.py
  - [x] 创建 tests/e2e/ 目录及 __init__.py
  - [x] 创建 tests/conftest.py

## [x] Task 4: 创建基础配置文件
- **Description**: 创建项目运行所需的配置文件
- **SubTasks**:
  - [x] 创建 .env.example
  - [x] 创建 .gitignore
  - [x] 创建 src/sherry_agent/config/defaults.toml

## Task Dependencies
- Task 2, 3, 4 可以并行执行
- Task 1 需要首先完成
