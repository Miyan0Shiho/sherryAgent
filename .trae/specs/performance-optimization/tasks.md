# Tasks

## Phase 1: 连接池管理（高优先级）

- [x] Task 1: 实现 LongTermMemory 数据库连接池
  - [x] SubTask 1.1: 添加 `_connection` 属性和 `_get_connection()` 方法
  - [x] SubTask 1.2: 修改所有数据库操作使用复用连接
  - [x] SubTask 1.3: 添加 `close()` 方法正确关闭连接
  - [x] SubTask 1.4: 更新测试用例

- [x] Task 2: 实现 OllamaClient HTTP Session 复用
  - [x] SubTask 2.1: 添加 `_session` 属性和 `_get_session()` 方法
  - [x] SubTask 2.2: 修改 `chat()` 和 `chat_stream()` 使用复用 session
  - [x] SubTask 2.3: 添加 `close()` 方法正确关闭 session
  - [x] SubTask 2.4: 添加超时配置（连接超时 5s，读取超时 30s）
  - [x] SubTask 2.5: 更新测试用例

## Phase 2: 并发控制与缓存（高优先级）

- [x] Task 3: 实现异步并发控制
  - [x] SubTask 3.1: 创建 `src/sherry_agent/infrastructure/concurrency.py` 模块
  - [x] SubTask 3.2: 实现 `ConcurrencyManager` 类，包含信号量管理
  - [x] SubTask 3.3: 添加基于系统资源的动态调整逻辑
  - [x] SubTask 3.4: 在 `agent_loop.py` 中集成并发控制
  - [x] SubTask 3.5: 编写单元测试

- [x] Task 4: 实现缓存机制
  - [x] SubTask 4.1: 创建 `src/sherry_agent/infrastructure/cache.py` 模块
  - [x] SubTask 4.2: 实现 `TTLCache` 类，支持过期时间
  - [x] SubTask 4.3: 在权限检查器中添加缓存
  - [x] SubTask 4.4: 在记忆搜索中添加缓存
  - [x] SubTask 4.5: 编写单元测试

## Phase 3: Token 估算优化（中优先级）

- [x] Task 5: 优化 ShortTermMemory Token 估算
  - [x] SubTask 5.1: 添加 tiktoken 依赖到 pyproject.toml
  - [x] SubTask 5.2: 实现 `TokenEstimator` 类，支持多种编码器
  - [x] SubTask 5.3: 修改 `estimate_tokens()` 使用 tiktoken
  - [x] SubTask 5.4: 添加降级策略（tiktoken 不可用时）
  - [x] SubTask 5.5: 更新测试用例

## Phase 4: 数据库搜索优化（中优先级）

- [x] Task 6: 实现 FTS5 全文搜索
  - [x] SubTask 6.1: 修改 `LongTermMemory.initialize()` 创建 FTS5 虚拟表
  - [x] SubTask 6.2: 添加触发器同步内容到 FTS5 表
  - [x] SubTask 6.3: 修改 `search_memory()` 使用 FTS5 MATCH 查询
  - [x] SubTask 6.4: 添加 `hybrid_search()` 的 FTS5 支持
  - [x] SubTask 6.5: 更新测试用例

- [x] Task 7: 实现批量操作
  - [x] SubTask 7.1: 添加 `add_memories_batch()` 方法
  - [x] SubTask 7.2: 使用 `executemany()` 批量插入
  - [x] SubTask 7.3: 在 MemoryBridge 中使用批量操作
  - [x] SubTask 7.4: 更新测试用例

## Phase 5: HTTP 客户端优化（中优先级）

- [x] Task 8: 实现 HTTP 重试机制
  - [x] SubTask 8.1: 创建 `src/sherry_agent/infrastructure/retry.py` 模块
  - [x] SubTask 8.2: 实现指数退避重试装饰器
  - [x] SubTask 8.3: 在 OllamaClient 中应用重试机制
  - [x] SubTask 8.4: 编写单元测试

## Phase 6: 资源监控（低优先级）

- [x] Task 9: 实现资源监控
  - [x] SubTask 9.1: 创建 `src/sherry_agent/infrastructure/monitoring.py` 模块
  - [x] SubTask 9.2: 实现 `ResourceMonitor` 类，监控内存和 CPU
  - [x] SubTask 9.3: 添加性能指标收集
  - [x] SubTask 9.4: 在心跳引擎中集成监控
  - [x] SubTask 9.5: 编写单元测试

## Phase 7: 性能基准测试

- [x] Task 10: 建立性能基准测试
  - [x] SubTask 10.1: 创建 `tests/benchmark/performance_benchmark.py`
  - [x] SubTask 10.2: 添加记忆系统性能测试
  - [x] SubTask 10.3: 添加 LLM 客户端性能测试
  - [x] SubTask 10.4: 添加并发性能测试
  - [x] SubTask 10.5: 生成性能报告

# Task Dependencies

- [Task 3] depends on [Task 1, Task 2] - 并发控制需要在连接池完成后
- [Task 4] depends on [Task 3] - 缓存依赖并发控制
- [Task 6] depends on [Task 1] - FTS5 依赖数据库连接池
- [Task 7] depends on [Task 1] - 批量操作依赖数据库连接池
- [Task 8] depends on [Task 2] - 重试机制依赖 Session 复用
- [Task 9] depends on [Task 3, Task 4] - 监控依赖并发控制和缓存
- [Task 10] depends on [Task 1-9] - 基准测试在所有优化完成后

# 并行执行建议

以下任务可以并行执行：
- Phase 1: Task 1 和 Task 2 可并行
- Phase 2: Task 3 和 Task 4 可并行（但 Task 4 依赖 Task 3 完成）
- Phase 3 和 Phase 4: Task 5、Task 6、Task 7 可并行
- Phase 5 和 Phase 6: Task 8、Task 9 可并行
