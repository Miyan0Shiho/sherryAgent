# SherryAgent MVP-2 - 记忆与持久化系统 - 产品需求文档

## Overview
- **Summary**: 实现 SherryAgent 的记忆与持久化系统，包括短期记忆压缩、长期记忆存储、任务持久化和断点续传功能，支持会话中断后恢复和跨会话记忆检索。
- **Purpose**: 解决 Agent 系统在长对话中上下文管理和跨会话知识持久化的问题，提升 Agent 的持续学习能力和可靠性。
- **Target Users**: 开发人员、AI Agent 研究者、使用 SherryAgent 进行任务自动化的用户。

## Goals
- 实现短期记忆的四层压缩策略，有效管理上下文窗口
- 建立长期记忆存储系统，支持跨会话知识检索
- 实现任务持久化，确保系统崩溃后可恢复
- 建立记忆桥接机制，实现短期到长期记忆的自动转化
- 提供混合检索能力，结合 BM25 和向量相似度

## Non-Goals (Out of Scope)
- 复杂的知识图谱构建
- 多模态记忆支持（图像、音频等）
- 高级语义理解和推理
- 分布式存储支持

## Background & Context
- MVP-1 已完成核心 Agent Loop 的实现
- 需要解决长对话中 token 消耗失控的问题
- 需要支持跨会话的知识积累和检索
- 技术栈：Python 3.12+, aiosqlite, sqlite-vec, sentence-transformers

## Functional Requirements
- **FR-1**: 短期记忆管理 - 实现四层压缩策略（micro-compact、auto-compact、session memory compact、reactive compact）
- **FR-2**: 长期记忆存储 - 基于 SQLite + FTS5 + 向量索引的混合存储方案
- **FR-3**: 任务持久化 - 将任务状态、对话历史和心跳信息持久化到磁盘
- **FR-4**: 断点续传 - 系统重启后自动恢复未完成的任务
- **FR-5**: 记忆桥接 - 会话结束时自动提取关键信息到长期记忆
- **FR-6**: 混合检索 - 结合 BM25 和向量相似度的多维度检索

## Non-Functional Requirements
- **NFR-1**: 性能 - 压缩和检索操作应在 100ms 内完成
- **NFR-2**: 可靠性 - 系统崩溃后数据不丢失，可恢复到最近状态
- **NFR-3**: 可扩展性 - 支持未来增加新的记忆类型和压缩策略
- **NFR-4**: 安全性 - 记忆存储应加密敏感信息，防止未授权访问

## Constraints
- **Technical**: 依赖 aiosqlite >= 0.20, sqlite-vec >= 0.1, sentence-transformers >= 3.0
- **Business**: 3 周开发时间
- **Dependencies**: 基于 MVP-1 的 Agent Loop 实现

## Assumptions
- 系统运行环境有足够的磁盘空间存储记忆数据
- 网络连接稳定，可访问必要的模型和依赖
- 用户会按照设计的 API 接口使用记忆系统

## Acceptance Criteria

### AC-1: 短期记忆压缩
- **Given**: 对话消息超过 token 预算
- **When**: 系统触发压缩机制
- **Then**: 消息被压缩，保留关键信息，token 消耗在预算内
- **Verification**: `programmatic`
- **Notes**: 需验证各压缩级别的效果

### AC-2: 长期记忆存储
- **Given**: 会话结束或关键信息产生
- **When**: 记忆桥接机制启动
- **Then**: 关键信息被提取并存储到长期记忆
- **Verification**: `programmatic`
- **Notes**: 验证存储格式和索引创建

### AC-3: 任务持久化
- **Given**: 任务执行过程中
- **When**: 系统定期保存状态
- **Then**: 任务状态、对话历史被写入磁盘
- **Verification**: `programmatic`
- **Notes**: 检查 state.json、transcript.jsonl、heartbeat.md 文件

### AC-4: 断点续传
- **Given**: 系统崩溃或手动重启
- **When**: 系统重新启动
- **Then**: 未完成的任务从上次成功步骤恢复
- **Verification**: `programmatic`
- **Notes**: 模拟崩溃场景测试

### AC-5: 混合检索
- **Given**: 用户查询历史记忆
- **When**: 系统执行检索
- **Then**: 返回按相关性排序的记忆结果
- **Verification**: `programmatic`
- **Notes**: 验证检索准确性和响应时间

## Open Questions
- [ ] 具体的 token 预算阈值如何设置？
- [ ] 长期记忆的存储容量上限如何管理？
- [ ] 向量模型的选择和部署方式？
- [ ] 记忆过期和清理策略？