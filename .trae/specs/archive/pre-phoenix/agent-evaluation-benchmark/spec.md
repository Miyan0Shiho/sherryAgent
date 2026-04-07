
# SherryAgent 能力评估与框架反省 - 产品需求文档

## Overview
- **Summary**: 使用开源 Agent 评估数据集（如 AgentBench、GAIA 等）对 SherryAgent 进行全面能力测试，使用本地 qwen3:0.6b 模型，观察任务解决过程，识别框架缺陷并提出改进方案。
- **Purpose**: 验证 SherryAgent 在实际任务上的表现，通过小模型成功解决复杂任务来证明框架设计的有效性，同时进行深度框架反省。
- **Target Users**: SherryAgent 开发团队、项目评审者、潜在用户。

## Goals
- 选择并集成 1-2 个有认可度的开源 Agent 评估数据集
- 在数据集上进行抽样测试，使用 qwen3:0.6b 模型
- 详细观察 SherryAgent 解决下游任务的完整过程
- 系统性识别框架存在的问题和瓶颈
- 生成框架反省报告和改进路线图
- 如果小模型能成功解决复杂任务，证明框架设计成功

## Non-Goals (Out of Scope)
- 不使用大模型（如 GPT-4、Claude 3）进行测试对比
- 不进行大规模性能基准测试
- 不立即修复所有发现的问题（仅识别和规划）
- 不修改用户规则和安全约束

## Background &amp; Context
- SherryAgent MVP-1 到 MVP-5 已全部完成
- 初步 qwen3:0.6b 测试显示基本功能正常，但工具调用能力不足
- 需要在标准评估数据集上验证框架的实际能力
- qwen3:0.6b 是 2025 年 7 月发布的轻量级模型，具有基础工具调用能力
- 如果小模型都能成功解决复杂任务，说明框架设计是成功的

## Functional Requirements
- **FR-1**: 能够下载/加载标准 Agent 评估数据集（如 AgentBench、GAIA、ToolBench 等）
- **FR-2**: 能够从数据集中抽取代表性测试用例
- **FR-3**: 能够使用 qwen3:0.6b 模型在 SherryAgent 上运行这些测试用例
- **FR-4**: 能够记录完整的任务执行过程（思考链、工具调用、中间结果）
- **FR-5**: 能够评估任务完成质量（成功率、正确性、效率）
- **FR-6**: 能够生成框架反省报告（问题分析、改进建议）

## Non-Functional Requirements
- **NFR-1**: 测试过程应可复现
- **NFR-2**: 执行日志应详细且可分析
- **NFR-3**: 评估标准应客观且可量化
- **NFR-4**: 测试应在合理时间内完成（每个任务 &lt; 10 分钟）

## Constraints
- **Technical**: 必须使用本地 qwen3:0.6b 模型，不使用云服务大模型
- **Business**: 测试覆盖简单、中等、困难三个难度级别
- **Dependencies**: 需要 Ollama 服务运行 qwen3:0.6b 模型

## Assumptions
- Ollama 服务已安装并运行
- qwen3:0.6b 模型已下载到本地
- SherryAgent 代码库处于可运行状态
- 选定的评估数据集有公开可访问的版本

## Acceptance Criteria

### AC-1: 数据集集成成功
- **Given**: 已选定 1-2 个标准 Agent 评估数据集
- **When**: 完成数据集加载器的实现
- **Then**: 能够成功从数据集中获取测试用例（包含任务描述、预期结果、评估标准）
- **Verification**: `programmatic`

### AC-2: 抽样测试执行
- **Given**: 数据集已加载，Ollama 服务运行正常
- **When**: 在每个难度级别（简单/中等/困难）各抽取 3-5 个测试用例执行
- **Then**: 所有测试用例都能在 SherryAgent + qwen3:0.6b 上完整运行
- **Verification**: `programmatic`

### AC-3: 执行过程记录完整
- **Given**: 测试用例正在执行
- **When**: 观察任务执行过程
- **Then**: 完整记录以下信息：思考链、工具调用序列、参数、返回值、中间结果、总耗时、Token 使用
- **Verification**: `human-judgment`

### AC-4: 任务质量评估
- **Given**: 测试用例执行完成
- **When**: 评估任务完成质量
- **Then**: 每个任务都有明确的评估结果（成功/部分成功/失败）及原因分析
- **Verification**: `human-judgment`

### AC-5: 框架问题识别
- **Given**: 所有测试用例执行完成
- **When**: 分析执行日志和结果
- **Then**: 识别出至少 5 个框架层面的问题（不限于：工具调用、记忆系统、编排、提示工程等）
- **Verification**: `human-judgment`

### AC-6: 反省报告生成
- **Given**: 问题识别完成
- **When**: 编写框架反省报告
- **Then**: 报告包含：测试概览、结果分析、问题清单、根本原因分析、改进建议、优先级排序、路线图
- **Verification**: `human-judgment`

### AC-7: 小模型验证成功（关键目标）
- **Given**: 完成所有测试
- **When**: 评估整体结果
- **Then**: 如果 qwen3:0.6b 能成功解决至少 1 个困难任务或 3 个中等任务，证明框架设计成功
- **Verification**: `human-judgment`

## Open Questions
- [ ] 选择哪个/哪些评估数据集？（候选：AgentBench、GAIA、ToolBench、WebArena）
- [ ] 数据集的许可证是否允许使用？
- [ ] 如何定义任务"成功"的标准？
- [ ] 如果 qwen3:0.6b 能力确实不足，是否考虑使用稍大一点的 qwen3 变体作为补充验证？

