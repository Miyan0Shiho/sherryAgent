# SherryAgent MVP-2 - 记忆与持久化系统 - 实现计划

## [x] Task 1: 短期记忆基础结构实现
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 实现 ShortTermMemory 类的基础结构
  - 实现 token 估算功能
  - 实现 micro-compact 压缩策略
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-1.1: 验证 token 估算准确性
  - `programmatic` TR-1.2: 验证 micro-compact 压缩效果
- **Notes**: 重点关注 token 估算的准确性，确保压缩触发时机正确

## [x] Task 2: 高级压缩策略实现
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 实现 auto-compact 压缩策略（LLM 摘要）
  - 实现 session memory compact 策略（结构化提取）
  - 实现 reactive compact 策略（激进压缩）
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-2.1: 验证各压缩级别的触发条件
  - `programmatic` TR-2.2: 验证压缩后关键信息保留情况
- **Notes**: 注意 LLM 摘要的质量和性能平衡

## [x] Task 3: 长期记忆存储系统
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 实现 LongTermMemory 类
  - 设计并创建 SQLite 数据库表结构
  - 实现 FTS5 和向量索引
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: 验证数据库表结构创建
  - `programmatic` TR-3.2: 验证记忆存储和检索功能
- **Notes**: 确保数据库操作的异步性能

## [x] Task 4: 混合检索实现
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 实现 BM25 检索
  - 实现向量相似度计算
  - 实现多维度评分和重排序
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `programmatic` TR-4.1: 验证检索准确性
  - `programmatic` TR-4.2: 验证检索响应时间
- **Notes**: 优化检索性能，确保在 100ms 内完成

## [x] Task 5: 任务持久化
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 实现任务状态持久化（state.json）
  - 实现对话历史持久化（transcript.jsonl）
  - 实现心跳信息持久化（heartbeat.md）
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-5.1: 验证状态文件正确生成
  - `programmatic` TR-5.2: 验证文件格式和内容
- **Notes**: 定期持久化，避免频繁 IO 操作

## [x] Task 6: 断点续传机制
- **Priority**: P0
- **Depends On**: Task 5
- **Description**: 
  - 实现启动时任务扫描
  - 实现从最近成功步骤恢复
  - 实现恢复状态验证
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-6.1: 验证崩溃后恢复功能
  - `programmatic` TR-6.2: 验证恢复状态的正确性
- **Notes**: 模拟各种崩溃场景进行测试

## [x] Task 7: 记忆桥接机制
- **Priority**: P1
- **Depends On**: Task 1, Task 3
- **Description**: 
  - 实现 MemoryBridge 类
  - 实现关键信息提取
  - 实现重要性评分
  - 实现短期到长期记忆的转化
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-7.1: 验证信息提取的准确性
  - `programmatic` TR-7.2: 验证长期记忆写入
- **Notes**: 重点关注信息提取的质量和效率

## [x] Task 8: 集成与测试
- **Priority**: P1
- **Depends On**: All previous tasks
- **Description**: 
  - 集成记忆系统到 Agent Loop
  - 编写单元测试和集成测试
  - 进行性能测试和压力测试
- **Acceptance Criteria Addressed**: All
- **Test Requirements**:
  - `programmatic` TR-8.1: 验证系统集成
  - `programmatic` TR-8.2: 验证性能指标
- **Notes**: 确保所有功能正常工作，性能达到要求