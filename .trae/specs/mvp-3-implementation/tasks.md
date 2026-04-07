# MVP-3 自主运行 - 实施计划

## [x] Task 1: 心跳引擎基础结构
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建心跳引擎核心类 `HeartbeatEngine`
  - 实现配置管理和状态跟踪
  - 定义心跳循环的基础架构
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-1.1: 心跳引擎能够正常启动和停止
  - `programmatic` TR-1.2: 心跳周期配置能够正确加载
- **Notes**: 参考 docs/specs/heartbeat-engine.md 中的设计

## [x] Task 2: 心跳循环实现
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 实现 `heartbeat_cycle` 方法
  - 集成 HEARTBEAT.md 状态管理
  - 实现任务检查和执行逻辑
- **Acceptance Criteria Addressed**: AC-1, AC-6
- **Test Requirements**:
  - `programmatic` TR-2.1: 心跳循环能够定期执行
  - `programmatic` TR-2.2: 能够正确读取和更新 HEARTBEAT.md
- **Notes**: 确保心跳循环的稳定性和可靠性

## [x] Task 3: Cron 调度集成
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 集成 APScheduler
  - 实现 Cron 任务配置和管理
  - 支持 Cron 表达式、固定间隔和一次性任务
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: Cron 任务能够按预期时间触发
  - `programmatic` TR-3.2: 不同类型的调度方式都能正常工作
- **Notes**: 确保调度器与心跳引擎的协同工作

## [x] Task 4: 后台模式实现
- **Priority**: P0
- **Depends On**: Task 1, Task 2
- **Description**:
  - 扩展 CLI 支持后台模式
  - 实现进程守护和后台运行
  - 提供前台/后台切换命令
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `human-judgment` TR-4.1: CLI 能够成功切换到后台运行
  - `programmatic` TR-4.2: 后台进程能够持续运行
- **Notes**: 考虑不同操作系统的后台运行机制

## [x] Task 5: WebSocket 服务
- **Priority**: P0
- **Depends On**: Task 1, Task 2
- **Description**:
  - 集成 fastapi 和 websockets
  - 实现 WebSocket 连接管理
  - 实现任务状态实时推送
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-5.1: WebSocket 服务能够正常启动
  - `programmatic` TR-5.2: 状态变更时能够实时推送
- **Notes**: 确保 WebSocket 服务的稳定性和性能

## [x] Task 6: 空闲检测与低功耗模式
- **Priority**: P1
- **Depends On**: Task 1, Task 2
- **Description**:
  - 实现空闲检测逻辑
  - 实现低功耗模式切换
  - 优化资源使用
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `programmatic` TR-6.1: 连续空闲时能够进入低功耗模式
  - `programmatic` TR-6.2: 有任务时能够自动唤醒
- **Notes**: 确保低功耗模式的正确切换

## [x] Task 7: 断电恢复
- **Priority**: P0
- **Depends On**: Task 2, Task 3
- **Description**:
  - 实现任务状态持久化
  - 实现重启后的任务恢复逻辑
  - 确保任务不会因系统重启而丢失
- **Acceptance Criteria Addressed**: AC-6
- **Test Requirements**:
  - `programmatic` TR-7.1: 系统重启后能够恢复未完成的任务
  - `programmatic` TR-7.2: 恢复过程无错误
- **Notes**: 确保持久化机制的可靠性

## [x] Task 8: 集成测试
- **Priority**: P1
- **Depends On**: All previous tasks
- **Description**:
  - 编写集成测试用例
  - 测试心跳引擎的稳定性
  - 测试各模块的协同工作
- **Acceptance Criteria Addressed**: All
- **Test Requirements**:
  - `programmatic` TR-8.1: 所有集成测试通过
  - `programmatic` TR-8.2: 心跳引擎持续运行 24 小时无崩溃
- **Notes**: 确保系统的整体稳定性