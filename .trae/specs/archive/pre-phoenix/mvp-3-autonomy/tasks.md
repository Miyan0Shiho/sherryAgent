# SherryAgent - MVP-3 自主运行 实现计划

## [ ] Task 1: 心跳引擎基础结构
- **Priority**: P0
- **Depends On**: MVP-1, MVP-2
- **Description**:
  - 实现HeartbeatConfig配置类
  - 实现HeartbeatStatus状态记录
  - 实现HeartbeatEngine类基础框架
- **Acceptance Criteria Addressed**: FR-1
- **Test Requirements**:
  - `programmatic` TR-1.1: HeartbeatConfig正确解析配置
  - `programmatic` TR-1.2: HeartbeatStatus正确记录状态

## [ ] Task 2: 心跳循环实现
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 实现while-True心跳循环
  - 实现heartbeat_cycle单次周期逻辑
  - 实现HEARTBEAT.md读取和解析
  - 实现优雅启动和停止
- **Acceptance Criteria Addressed**: FR-1, AC-1
- **Test Requirements**:
  - `long-running-test` TR-2.1: 心跳引擎持续运行24小时无崩溃
  - `programmatic` TR-2.2: heartbeat_cycle正确执行

## [ ] Task 3: Cron调度集成
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 集成APScheduler
  - 实现Cron表达式解析
  - 实现固定间隔调度
  - 实现一次性任务调度
- **Acceptance Criteria Addressed**: FR-2, AC-2
- **Test Requirements**:
  - `scheduled-test` TR-3.1: Cron任务按时触发
  - `programmatic` TR-3.2: 三种调度模式都正确工作

## [ ] Task 4: 后台模式实现
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 实现CLI到后台的切换逻辑
  - 实现后台守护进程模式
  - 实现进程管理（启动、停止、重启）
- **Acceptance Criteria Addressed**: FR-3, AC-3
- **Test Requirements**:
  - `human-judgment` TR-4.1: CLI能切换到后台
  - `programmatic` TR-4.2: 后台进程正确管理

## [ ] Task 5: WebSocket服务
- **Priority**: P0
- **Depends On**: Task 4
- **Description**:
  - 集成FastAPI和websockets
  - 实现WebSocket连接管理
  - 实现状态推送逻辑
  - 实现心跳保活机制
- **Acceptance Criteria Addressed**: FR-4
- **Test Requirements**:
  - `programmatic` TR-5.1: WebSocket连接正常建立
  - `programmatic` TR-5.2: 状态推送延迟 < 1秒

## [ ] Task 6: 空闲检测与低功耗模式
- **Priority**: P1
- **Depends On**: Task 2
- **Description**:
  - 实现空闲检测逻辑
  - 实现低功耗模式切换
  - 实现唤醒条件检测
  - 实现资源监控
- **Acceptance Criteria Addressed**: FR-5, AC-5
- **Test Requirements**:
  - `resource-monitoring` TR-6.1: 空闲时自动进入低功耗模式
  - `programmatic` TR-6.2: 唤醒条件正确触发

## [ ] Task 7: 断电恢复
- **Priority**: P0
- **Depends On**: Task 2, MVP-2 Task 7
- **Description**:
  - 实现启动时自动恢复心跳引擎
  - 集成MVP-2的断点续传
  - 实现恢复后的状态同步
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `crash-recovery-test` TR-7.1: 断电重启后自动恢复
  - `programmatic` TR-7.2: 恢复后状态正确

## [ ] Task 8: 集成测试
- **Priority**: P1
- **Depends On**: All Tasks
- **Description**:
  - 编写长时间运行测试
  - 编写定时任务测试
  - 编写崩溃恢复测试
  - 性能测试和优化
- **Acceptance Criteria Addressed**: All ACs
- **Test Requirements**:
  - `programmatic` TR-8.1: 所有测试通过
  - `programmatic` TR-8.2: 性能满足要求

## Task Dependencies
- Task 2, 3 depend on Task 1
- Task 4 depends on Task 2
- Task 5 depends on Task 4
- Task 6 depends on Task 2
- Task 7 depends on Task 2
- Task 8 depends on all other tasks
