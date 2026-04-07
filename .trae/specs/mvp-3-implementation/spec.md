# MVP-3 自主运行 - 产品需求文档

## Overview
- **Summary**: 实现 SherryAgent 的后台自主运行能力，包括心跳驱动、Cron 调度、后台模式、WebSocket 状态推送和低功耗模式。
- **Purpose**: 使 Agent 能够在无人监督的情况下持续运行，自动执行定时任务，恢复中断工作，并通过 WebSocket 实时推送状态。
- **Target Users**: 开发人员和系统管理员，需要 Agent 在后台持续运行并执行自动化任务。

## Goals
- 实现心跳引擎，支持持续的后台运行
- 集成 Cron 调度，支持定时任务触发
- 实现后台模式，允许 CLI 切换到后台运行
- 提供 WebSocket 服务，实时推送任务执行状态
- 实现空闲检测和低功耗模式，优化资源使用
- 支持断电恢复，确保任务不会因系统重启而丢失

## Non-Goals (Out of Scope)
- 不实现复杂的分布式架构
- 不支持多实例协调
- 不实现 GUI 界面（仅通过 CLI 和 WebSocket 管理）
- 不涉及外部监控系统集成（如 Prometheus）

## Background & Context
- 基于 MVP-1 的 Agent Loop 核心功能
- 基于 MVP-2 的持久化能力
- 需要集成 APScheduler 实现 Cron 调度
- 需要集成 websockets 和 fastapi 实现 WebSocket 服务

## Functional Requirements
- **FR-1**: 心跳引擎基础结构，支持可配置的心跳间隔
- **FR-2**: 心跳循环实现，执行检查-执行-更新流程
- **FR-3**: Cron 调度集成，支持 Cron 表达式和固定间隔任务
- **FR-4**: 后台模式实现，允许 CLI 切换到后台运行
- **FR-5**: WebSocket 服务，实时推送任务执行状态
- **FR-6**: 空闲检测与低功耗模式，优化资源使用
- **FR-7**: 断电恢复，确保任务在系统重启后自动恢复

## Non-Functional Requirements
- **NFR-1**: 心跳引擎稳定性，持续运行 24 小时无崩溃
- **NFR-2**: 资源使用优化，低功耗模式下减少 CPU 和内存消耗
- **NFR-3**: 响应速度，WebSocket 状态推送延迟 < 1 秒
- **NFR-4**: 可配置性，所有关键参数支持通过配置文件调整

## Constraints
- **Technical**: Python 3.12+, asyncio 异步框架
- **Dependencies**: APScheduler >= 3.10, websockets >= 13.0, fastapi >= 0.115
- **Performance**: 心跳引擎 CPU 使用率 < 5%（空闲状态）

## Assumptions
- MVP-1 和 MVP-2 的核心功能已经完成并稳定运行
- 系统环境支持异步操作和网络服务
- 用户具备基本的命令行操作能力

## Acceptance Criteria

### AC-1: 心跳引擎持续运行
- **Given**: 系统正常启动
- **When**: 启动心跳引擎
- **Then**: 心跳引擎持续运行 24 小时无崩溃，定期执行心跳周期
- **Verification**: `programmatic`

### AC-2: Cron 任务按预期触发
- **Given**: 配置了 Cron 任务
- **When**: 到达指定时间
- **Then**: Cron 任务自动执行
- **Verification**: `programmatic`

### AC-3: CLI 后台模式切换
- **Given**: CLI 运行中
- **When**: 切换到后台模式
- **Then**: CLI 进程在后台运行，释放终端
- **Verification**: `human-judgment`

### AC-4: WebSocket 状态推送
- **Given**: WebSocket 客户端连接
- **When**: 任务状态变更
- **Then**: WebSocket 客户端收到实时状态更新
- **Verification**: `programmatic`

### AC-5: 低功耗模式
- **Given**: 系统长时间空闲
- **When**: 连续空闲超过阈值
- **Then**: 自动进入低功耗模式，延长心跳间隔
- **Verification**: `programmatic`

### AC-6: 断电恢复
- **Given**: 系统意外重启
- **When**: 重启后启动 Agent
- **Then**: 心跳引擎自动恢复未完成的任务
- **Verification**: `programmatic`

## Open Questions
- [ ] 是否需要支持外部唤醒机制？
- [ ] WebSocket 服务的安全认证如何实现？
- [ ] 低功耗模式的具体阈值是否需要可配置？