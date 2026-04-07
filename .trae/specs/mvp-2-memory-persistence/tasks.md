# Fusion Agent - MVP-2 记忆与持久化 实现计划

## [ ] Task 1: 短期记忆基础结构
- **Priority**: P0
- **Depends On**: MVP-1
- **Description**:
  - 实现TokenTracker用于token预算管理
  - 实现ShortTermMemory类
  - 实现token估算函数
- **Acceptance Criteria Addressed**: FR-1
- **Test Requirements**:
  - `programmatic` TR-1.1: TokenTracker能正确追踪token消耗
  - `programmatic` TR-1.2: token估算函数误差 < 10%

## [ ] Task 2: Micro-Compact 实现
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 实现单条消息截断逻辑
  - 保留首尾关键内容
  - 处理工具调用结果摘要
- **Acceptance Criteria Addressed**: FR-1, AC-1
- **Test Requirements**:
  - `programmatic` TR-2.1: 长消息被正确截断
  - `programmatic` TR-2.2: 截断后保留关键信息

## [ ] Task 3: Auto-Compact 实现
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 实现LLM摘要压缩逻辑
  - 提取关键决策和当前任务状态
  - 压缩早期对话
- **Acceptance Criteria Addressed**: FR-1, AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: 上下文接近阈值时触发压缩
  - `regression-test` TR-3.2: 压缩后关键信息可检索

## [ ] Task 4: 长期记忆存储
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 设计SQLite数据库schema
  - 实现FTS5全文索引
  - 集成sqlite-vec向量索引
  - 实现MemoryEntry数据模型
- **Acceptance Criteria Addressed**: FR-2
- **Test Requirements**:
  - `programmatic` TR-4.1: 记忆条目能正确存储
  - `programmatic` TR-4.2: FTS5索引能正确检索
  - `programmatic` TR-4.3: 向量索引能正确检索

## [ ] Task 5: 混合检索实现
- **Priority**: P0
- **Depends On**: Task 4
- **Description**:
  - 实现BM25 + 向量 + 重要性 + 时效性混合评分
  - 实现MemoryQuery查询接口
  - 实现Top-K结果返回
- **Acceptance Criteria Addressed**: FR-2, AC-5
- **Test Requirements**:
  - `programmatic` TR-5.1: 混合检索返回相关结果
  - `integration-test` TR-5.2: 跨会话记忆可检索

## [ ] Task 6: 任务持久化
- **Priority**: P0
- **Depends On**: MVP-1
- **Description**:
  - 设计tasks/目录结构
  - 实现state.json读写
  - 实现transcript.jsonl追加写入
  - 实现heartbeat.md人类可读看板
- **Acceptance Criteria Addressed**: FR-3, AC-3
- **Test Requirements**:
  - `programmatic` TR-6.1: 任务状态正确持久化
  - `programmatic` TR-6.2: 执行日志正确追加

## [ ] Task 7: 断点续传
- **Priority**: P0
- **Depends On**: Task 6
- **Description**:
  - 实现TaskRecovery恢复管理器
  - 实现scan_interrupted_tasks扫描逻辑
  - 实现recover_task恢复逻辑
  - 实现RecoveryContext上下文重建
- **Acceptance Criteria Addressed**: FR-4, AC-4
- **Test Requirements**:
  - `crash-recovery-test` TR-7.1: 崩溃后任务可恢复
  - `programmatic` TR-7.2: 恢复后上下文正确

## [ ] Task 8: 记忆桥接
- **Priority**: P1
- **Depends On**: Task 3, Task 4
- **Description**:
  - 实现MemoryBridge类
  - 实现关键信息提取逻辑
  - 实现重要性评分算法
  - 实现会话结束时自动写入
- **Acceptance Criteria Addressed**: FR-5
- **Test Requirements**:
  - `programmatic` TR-8.1: 关键信息被正确提取
  - `programmatic` TR-8.2: 记忆被正确写入长期存储

## [ ] Task 9: 集成测试
- **Priority**: P1
- **Depends On**: All Tasks
- **Description**:
  - 编写端到端记忆系统测试
  - 编写断点续传测试
  - 性能测试和优化
- **Acceptance Criteria Addressed**: All ACs
- **Test Requirements**:
  - `programmatic` TR-9.1: 所有测试通过
  - `programmatic` TR-9.2: 性能满足要求

## Task Dependencies
- Task 2, 3 depend on Task 1
- Task 5 depends on Task 4
- Task 7 depends on Task 6
- Task 8 depends on Task 3, Task 4
- Task 9 depends on all other tasks
