# Fusion Agent - MVP-2 记忆与持久化 产品需求文档

## Overview
- **Summary**: 实现上下文压缩和任务持久化，支持会话中断后断点续传和跨会话记忆检索。
- **Purpose**: 构建Fusion Agent框架的记忆系统，实现短期记忆压缩和长期记忆持久化。
- **Target Users**: 开发者和AI Agent研究者，需要长时间运行任务和跨会话知识积累。

## Goals
- 实现短期记忆的token预算管理和四层压缩策略
- 实现长期记忆的SQLite + FTS5 + 向量检索
- 实现任务持久化，包括state.json、transcript.jsonl、heartbeat.md
- 实现断点续传，支持崩溃后恢复未完成任务
- 实现记忆桥接，会话结束时提取关键信息写入长期记忆

## Non-Goals (Out of Scope)
- 后台自主运行和Cron调度
- 多Agent编排和子Agent Fork
- Skill插件和MCP集成
- WebSocket状态推送

## Background & Context
- MVP-2是框架的第二个里程碑，专注于记忆系统和任务持久化
- 融合Claude Code的四层压缩策略和OpenClaw的三层记忆模型
- 采用SQLite + FTS5 + sqlite-vec作为存储引擎

## Functional Requirements
- **FR-1**: 短期记忆管理，支持token预算管理和micro-compact、auto-compact压缩
- **FR-2**: 长期记忆存储，支持SQLite + FTS5 + 向量检索
- **FR-3**: 任务持久化，支持state.json、transcript.jsonl、heartbeat.md格式
- **FR-4**: 断点续传，支持启动时扫描未完成任务并恢复
- **FR-5**: 记忆桥接，支持会话结束时提取关键信息写入长期记忆

## Non-Functional Requirements
- **NFR-1**: 压缩效率，压缩后保留关键信息（可通过提问验证）
- **NFR-2**: 持久化安全，任务执行过程写入transcript.jsonl
- **NFR-3**: 恢复可靠，进程崩溃后重启可恢复未完成任务
- **NFR-4**: 检索准确，跨会话可检索到历史记忆
- **NFR-5**: 性能，长对话自动触发上下文压缩

## Constraints
- **Technical**: Python 3.12+，依赖aiosqlite、sqlite-vec、sentence-transformers
- **Business**: 3周开发周期
- **Dependencies**: 需要MVP-1完成

## Assumptions
- MVP-1的Agent Loop已实现
- 用户有足够的磁盘空间存储记忆数据库

## Acceptance Criteria

### AC-1: 长对话自动触发上下文压缩
- **Given**: 用户进行长对话
- **When**: 上下文接近预算80%
- **Then**: 自动触发auto-compact压缩
- **Verification**: `programmatic`

### AC-2: 压缩后保留关键信息
- **Given**: 上下文被压缩
- **When**: 用户询问压缩前的关键信息
- **Then**: Agent能正确回答
- **Verification**: `regression-test`

### AC-3: 任务执行过程持久化
- **Given**: Agent正在执行任务
- **When**: 任务执行过程中
- **Then**: 执行日志追加写入transcript.jsonl
- **Verification**: `programmatic`

### AC-4: 进程崩溃后恢复
- **Given**: Agent进程崩溃
- **When**: 重启Agent
- **Then**: 自动恢复未完成的任务
- **Verification**: `crash-recovery-test`

### AC-5: 跨会话记忆检索
- **Given**: 用户在之前的会话中存储了信息
- **When**: 用户在新会话中查询相关信息
- **Then**: Agent能检索到历史记忆
- **Verification**: `integration-test`

## Open Questions
- [ ] 向量检索使用哪个embedding模型？
- [ ] 长期记忆的重要性评分算法如何设计？
- [ ] 记忆桥接的信息提取策略如何实现？
