# SherryAgent - MVP-1 核心Agent Loop 实现计划

## [x] Task 1: 项目初始化与基础结构搭建
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建项目目录结构
  - 配置pyproject.toml
  - 安装必要依赖
  - 初始化git仓库
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-1.1: 项目能正常安装依赖
  - `programmatic` TR-1.2: 目录结构符合设计规范
- **Notes**: 采用uv作为依赖管理工具，速度更快

## [x] Task 2: 数据模型与事件系统
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 实现AgentEvent、EventType、ToolCall等核心数据结构
  - 定义TokenUsage和AgentConfig模型
  - 实现CancellationToken用于任务中止
- **Acceptance Criteria Addressed**: FR-1
- **Test Requirements**:
  - `programmatic` TR-2.1: 数据模型能正确序列化/反序列化
  - `programmatic` TR-2.2: CancellationToken能正确中止任务
- **Notes**: 使用dataclasses和enum确保类型安全

## [x] Task 3: Agent Loop核心实现
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 实现agent_loop异步生成器
  - 集成LLM调用（anthropic/openai）
  - 处理工具调用和结果
  - 支持流式输出
- **Acceptance Criteria Addressed**: FR-1, FR-2
- **Test Requirements**:
  - `programmatic` TR-3.1: Agent Loop能正常执行完整流程
  - `human-judgment` TR-3.2: LLM响应能流式输出到终端
- **Notes**: 使用asyncio.Queue处理并发工具调用

## [x] Task 4: 基础工具实现
- **Priority**: P0
- **Depends On**: Task 3
- **Description**:
  - 实现文件读写工具（read/write）
  - 实现Shell执行工具（exec）
  - 实现HTTP请求工具（fetch）
  - 工具执行器ToolExecutor
- **Acceptance Criteria Addressed**: FR-3, FR-4, FR-5
- **Test Requirements**:
  - `programmatic` TR-4.1: 文件工具能正确读写文件
  - `programmatic` TR-4.2: Shell工具能执行命令并返回结果
  - `programmatic` TR-4.3: HTTP工具能发送请求并返回响应
- **Notes**: 工具执行需要权限检查

## [x] Task 5: 基础权限系统
- **Priority**: P0
- **Depends On**: Task 4
- **Description**:
  - 实现第1层：工具声明式权限
  - 实现第2层：全局安全规则（危险命令拦截）
  - 实现第6层：沙箱隔离（文件系统路径限制）
  - 权限检查流程
- **Acceptance Criteria Addressed**: FR-6, AC-6
- **Test Requirements**:
  - `programmatic` TR-5.1: 危险命令被正确拦截
  - `programmatic` TR-5.2: 权限检查流程正常工作
- **Notes**: 危险命令列表包括rm -rf /、DROP TABLE等

## [x] Task 6: CLI交互界面
- **Priority**: P1
- **Depends On**: Task 3, Task 4
- **Description**:
  - 基于Textual实现TUI界面
  - 支持用户输入和命令执行
  - 显示流式输出和工具执行结果
  - 支持任务中止
- **Acceptance Criteria Addressed**: FR-7, AC-1, AC-7
- **Test Requirements**:
  - `human-judgment` TR-6.1: CLI界面能正常启动和响应输入
  - `human-judgment` TR-6.2: 用户能通过快捷键中止任务
- **Notes**: 保持界面简洁，专注核心功能

## [x] Task 7: 集成测试与调试
- **Priority**: P1
- **Depends On**: Task 3, Task 4, Task 5, Task 6
- **Description**:
  - 编写端到端测试
  - 测试完整执行流程
  - 调试和修复问题
  - 性能优化
- **Acceptance Criteria Addressed**: All ACs
- **Test Requirements**:
  - `programmatic` TR-7.1: 所有端到端测试通过
  - `programmatic` TR-7.2: 单次验证循环 < 30秒
- **Notes**: 使用pytest和pytest-asyncio进行测试