# SherryAgent - MVP-1 核心Agent Loop 产品需求文档

## Overview
- **Summary**: 实现最小可用的Agent执行循环，能够在CLI中完成简单的文件操作任务，包括基础的LLM推理、工具执行和权限控制。
- **Purpose**: 构建SherryAgent框架的核心执行引擎，为后续功能（记忆、持久化、自主运行、多Agent编排）提供基础。
- **Target Users**: 开发者和AI Agent研究者，通过CLI交互与Agent进行操作。

## Goals
- 实现基础Agent Loop，支持消息输入 → LLM推理 → 工具执行 → 结果反馈的完整流程
- 支持CLI实时流式输出LLM生成的文本和工具执行过程
- 集成3个基础工具：文件读写、Shell执行、HTTP请求
- 实现基础权限系统，确保操作安全性
- 提供CLI交互模式的基础界面

## Non-Goals (Out of Scope)
- 记忆系统和上下文压缩
- 任务持久化和断点续传
- 后台自主运行和Cron调度
- 多Agent编排和子Agent Fork
- Skill插件和MCP集成
- 复杂的TUI界面和WebSocket支持

## Background & Context
- SherryAgent是基于Claude Code与OpenClaw两大AI Agent框架优势融合的Python多Agent框架
- MVP-1是框架的第一个里程碑，专注于实现核心执行逻辑
- 采用Python 3.12+的异步生态，充分利用asyncio、TaskGroup等特性
- 安全优先原则，权限系统贯穿所有执行路径

## Functional Requirements
- **FR-1**: Agent执行循环，支持消息输入、LLM推理、工具执行和结果反馈的完整流程
- **FR-2**: 流式输出，CLI实时显示LLM生成的文本和工具执行过程
- **FR-3**: 文件操作工具，支持读取和写入文件
- **FR-4**: Shell执行工具，支持执行系统命令
- **FR-5**: HTTP请求工具，支持发送HTTP请求
- **FR-6**: 基础权限系统，包括工具声明式权限、全局安全规则和沙箱隔离
- **FR-7**: CLI交互模式，提供基础的Textual TUI界面

## Non-Functional Requirements
- **NFR-1**: 性能，单次验证循环 < 30秒
- **NFR-2**: 安全，危险操作必须被权限系统拦截
- **NFR-3**: 可用性，用户可随时中止正在执行的任务
- **NFR-4**: 可维护性，代码结构清晰，遵循Pythonic风格
- **NFR-5**: 兼容性，支持Python 3.12+

## Constraints
- **Technical**: Python 3.12+，依赖asyncio、Textual、anthropic/openai SDK等
- **Business**: 2周开发周期，专注核心功能
- **Dependencies**: 需要配置LLM API密钥（anthropic或openai）

## Assumptions
- 用户已配置有效的LLM API密钥
- 开发环境为macOS或Linux
- 网络连接正常，能够访问LLM API

## Acceptance Criteria

### AC-1: CLI启动与用户输入
- **Given**: 用户在终端启动SherryAgent
- **When**: 用户输入任务指令
- **Then**: Agent接收并解析用户输入，准备执行
- **Verification**: `programmatic`

### AC-2: LLM响应流式输出
- **Given**: Agent执行LLM推理
- **When**: LLM生成响应
- **Then**: 响应内容实时流式输出到终端
- **Verification**: `human-judgment`

### AC-3: 文件操作工具
- **Given**: 用户请求读取或写入文件
- **When**: Agent调用文件操作工具
- **Then**: 文件被正确读取或写入，操作结果反馈给用户
- **Verification**: `programmatic`

### AC-4: Shell执行工具
- **Given**: 用户请求执行系统命令
- **When**: Agent调用Shell执行工具
- **Then**: 命令被执行，输出结果反馈给用户
- **Verification**: `programmatic`

### AC-5: HTTP请求工具
- **Given**: 用户请求发送HTTP请求
- **When**: Agent调用HTTP请求工具
- **Then**: 请求被发送，响应结果反馈给用户
- **Verification**: `programmatic`

### AC-6: 权限系统拦截危险操作
- **Given**: 用户请求执行危险命令（如`rm -rf /`）
- **When**: Agent调用Shell执行工具
- **Then**: 权限系统拦截操作，拒绝执行并提示用户
- **Verification**: `programmatic`

### AC-7: 用户中止任务
- **Given**: Agent正在执行任务
- **When**: 用户按下中止快捷键
- **Then**: Agent停止执行，返回中止信息
- **Verification**: `human-judgment`

## Open Questions
- [ ] 具体使用哪个LLM模型作为默认配置？
- [ ] 权限系统的具体危险操作列表需要哪些？
- [ ] CLI界面的具体布局和交互方式如何设计？