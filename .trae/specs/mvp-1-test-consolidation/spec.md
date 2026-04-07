# SherryAgent - MVP-1 测试整合与覆盖分析 产品需求文档

## Overview
- **Summary**: 整合现有测试脚本，分析 MVP-1 测试覆盖情况，识别测试缺口并规划迭代改进方案
- **Purpose**: 确保 MVP-1 核心功能得到充分测试，提高代码质量和系统可靠性
- **Target Users**: 开发团队和测试工程师

## Goals
- 整合根目录的临时测试脚本到标准测试目录
- 分析 MVP-1 功能测试覆盖情况
- 识别测试缺口并补充缺失的测试
- 实现完全自动化的端到端测试
- 建立持续测试最佳实践

## Non-Goals (Out of Scope)
- MVP-2 及后续功能的测试
- 性能优化和压力测试
- 第三方服务的深度集成测试

## Background & Context
- MVP-1 核心功能已基本实现
- 根目录存在多个临时测试脚本需要整合
- 现有的单元测试和集成测试框架已建立
- 需要验证真实 LLM 模型（包括本地 Ollama）的集成

## Functional Requirements
- **FR-1**: 整合临时测试脚本到 `tests/` 目录
- **FR-2**: 创建完全自动化的端到端测试套件
- **FR-3**: 测试真实 LLM 模型（Ollama 本地模型）集成
- **FR-4**: 测试流式输出功能
- **FR-5**: 测试工具调用的完整流程
- **FR-6**: 测试权限系统拦截危险操作
- **FR-7**: 测试用户中止任务功能

## Non-Functional Requirements
- **NFR-1**: 自动化测试执行时间 < 5 分钟
- **NFR-2**: 所有测试必须可在无人工干预的情况下运行
- **NFR-3**: 测试覆盖率目标：核心逻辑 > 80%
- **NFR-4**: 测试输出必须清晰、结构化

## Constraints
- **Technical**: 使用 pytest 作为主要测试框架
- **Business**: 在 1-2 天内完成测试整合
- **Dependencies**: 需要 Ollama 本地服务运行用于集成测试

## Assumptions
- Ollama 服务已在本地运行
- qwen3:0.6b 模型已下载
- 网络连接正常（如需测试云端 LLM）

## Acceptance Criteria

### AC-1: 测试脚本整合
- **Given**: 根目录存在临时测试脚本
- **When**: 执行整合任务
- **Then**: 所有有用的测试脚本移动到 `tests/` 目录的适当位置
- **Verification**: `programmatic`

### AC-2: 完全自动化的端到端测试
- **Given**: 测试环境已配置
- **When**: 运行完整测试套件
- **Then**: 所有测试自动执行，无需用户输入
- **Verification**: `programmatic`

### AC-3: 真实 LLM 集成测试
- **Given**: Ollama 服务运行且 qwen3:0.6b 模型可用
- **When**: 运行 LLM 集成测试
- **Then**: 测试成功与真实模型交互
- **Verification**: `programmatic`

### AC-4: 流式输出测试
- **Given**: Agent 正在生成响应
- **When**: 响应流式输出
- **Then**: 输出按预期分块显示
- **Verification**: `programmatic`

### AC-5: 工具调用完整流程测试
- **Given**: 用户请求需要工具的任务
- **When**: Agent 执行任务
- **Then**: 工具被正确调用，结果被正确返回
- **Verification**: `programmatic`

### AC-6: 权限系统测试
- **Given**: 用户请求危险操作
- **When**: 权限系统检查操作
- **Then**: 危险操作被拦截
- **Verification**: `programmatic`

### AC-7: 测试覆盖分析
- **Given**: 测试套件运行完成
- **When**: 生成测试覆盖率报告
- **Then**: 报告清晰显示测试覆盖情况
- **Verification**: `programmatic`

## Open Questions
- [ ] 是否需要云端 LLM（Anthropic/OpenAI）的集成测试？
- [ ] 流式输出测试的具体验证标准是什么？
- [ ] 性能测试的具体指标是什么？
