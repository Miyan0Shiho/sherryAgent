# Fusion Agent - MVP-3 自主运行 产品需求文档

## Overview
- **Summary**: 实现后台自主运行能力，支持心跳驱动和定时调度。
- **Purpose**: 构建Fusion Agent框架的自主运行层，实现24/7在线能力。
- **Target Users**: 需要长时间运行监控、巡检、自动化运维的用户。

## Goals
- 实现心跳引擎，支持while-True循环和可配置周期
- 实现Cron调度，集成APScheduler支持Cron表达式
- 实现后台模式，支持CLI切换到后台运行
- 实现WebSocket状态推送，实时推送任务执行状态
- 实现空闲检测与低功耗模式

## Non-Goals (Out of Scope)
- 多Agent编排和子Agent Fork
- Skill插件和MCP集成
- 复杂的消息渠道集成

## Background & Context
- MVP-3是框架的第三个里程碑，专注于自主运行能力
- 融合OpenClaw的心跳机制和Cron调度系统
- 采用APScheduler作为调度引擎

## Functional Requirements
- **FR-1**: 心跳引擎，支持while-True循环和可配置周期
- **FR-2**: Cron调度，支持Cron表达式、固定间隔、一次性任务
- **FR-3**: 后台模式，支持CLI切换到后台运行
- **FR-4**: WebSocket状态推送，实时推送任务执行状态
- **FR-5**: 空闲检测与低功耗模式，降低资源消耗

## Non-Functional Requirements
- **NFR-1**: 稳定性，心跳引擎持续运行24小时无崩溃
- **NFR-2**: 准确性，Cron任务按预期时间触发
- **NFR-3**: 可恢复性，断电重启后心跳引擎自动恢复
- **NFR-4**: 效率，空闲时自动进入低功耗模式
- **NFR-5**: 实时性，WebSocket推送延迟 < 1秒

## Constraints
- **Technical**: Python 3.12+，依赖APScheduler、websockets、fastapi
- **Business**: 2周开发周期
- **Dependencies**: 需要MVP-1和MVP-2完成

## Assumptions
- MVP-1的Agent Loop和MVP-2的持久化已实现
- 用户有稳定的服务器环境运行后台模式

## Acceptance Criteria

### AC-1: 心跳引擎持续运行
- **Given**: 心跳引擎启动
- **When**: 持续运行24小时
- **Then**: 无崩溃，正常执行心跳周期
- **Verification**: `long-running-test`

### AC-2: Cron任务按时触发
- **Given**: 配置了Cron任务
- **When**: 到达预定时间
- **Then**: 任务被正确触发执行
- **Verification**: `scheduled-test`

### AC-3: CLI切换到后台
- **Given**: 用户在CLI模式下
- **When**: 执行切换到后台命令
- **Then**: Agent切换到后台运行，WebSocket开始推送状态
- **Verification**: `human-judgment`

### AC-4: 断电重启后恢复
- **Given**: Agent在后台运行时断电
- **When**: 重启系统
- **Then**: 心跳引擎自动恢复，继续执行未完成任务
- **Verification**: `crash-recovery-test`

### AC-5: 空闲时低功耗模式
- **Given**: Agent连续空闲超过阈值
- **When**: 检测到空闲
- **Then**: 自动进入低功耗模式，延长心跳周期
- **Verification**: `resource-monitoring`

## Open Questions
- [ ] 心跳周期的默认值如何设置？
- [ ] WebSocket的认证机制如何设计？
- [ ] 低功耗模式的唤醒条件有哪些？
