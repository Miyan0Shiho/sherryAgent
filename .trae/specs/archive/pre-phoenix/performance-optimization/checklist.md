# 性能优化 Checklist

## Phase 1: 连接池管理

- [ ] LongTermMemory 数据库连接复用实现正确
- [ ] LongTermMemory 所有数据库操作使用复用连接
- [ ] LongTermMemory.close() 方法正确关闭连接
- [ ] OllamaClient HTTP Session 复用实现正确
- [ ] OllamaClient 请求超时配置正确（连接 5s，读取 30s）
- [ ] OllamaClient.close() 方法正确关闭 session
- [ ] 连接池相关测试全部通过

## Phase 2: 并发控制与缓存

- [ ] ConcurrencyManager 信号量管理实现正确
- [ ] 并发限制基于 CPU 核心数自动设置
- [ ] agent_loop 中并发控制集成正确
- [ ] TTLCache 过期机制工作正常
- [ ] 权限检查缓存生效
- [ ] 记忆搜索缓存生效
- [ ] 并发控制和缓存相关测试全部通过

## Phase 3: Token 估算优化

- [ ] tiktoken 依赖已添加到 pyproject.toml
- [ ] TokenEstimator 支持多种编码器
- [ ] estimate_tokens() 使用 tiktoken 精确估算
- [ ] tiktoken 不可用时降级策略工作正常
- [ ] Token 估算相关测试全部通过

## Phase 4: 数据库搜索优化

- [ ] FTS5 虚拟表创建正确
- [ ] FTS5 触发器同步内容正常
- [ ] search_memory() 使用 FTS5 MATCH 查询
- [ ] hybrid_search() FTS5 支持正常
- [ ] add_memories_batch() 批量插入实现正确
- [ ] MemoryBridge 使用批量操作
- [ ] 数据库搜索相关测试全部通过

## Phase 5: HTTP 客户端优化

- [ ] 指数退避重试装饰器实现正确
- [ ] OllamaClient 重试机制工作正常
- [ ] 重试仅对可重试错误（网络错误、5xx）生效
- [ ] HTTP 重试相关测试全部通过

## Phase 6: 资源监控

- [ ] ResourceMonitor 内存监控工作正常
- [ ] ResourceMonitor CPU 监控工作正常
- [ ] 性能指标收集正确
- [ ] 心跳引擎监控集成正确
- [ ] 资源监控相关测试全部通过

## Phase 7: 性能基准测试

- [ ] 记忆系统性能测试通过
- [ ] LLM 客户端性能测试通过
- [ ] 并发性能测试通过
- [ ] 性能报告生成正确

## 整体验证

- [ ] 所有单元测试通过（`uv run pytest tests/unit/`）
- [ ] 所有集成测试通过（`uv run pytest tests/integration/`）
- [ ] 类型检查通过（`uv run mypy src/`）
- [ ] 代码检查通过（`uv run ruff check src/`）
- [ ] 性能基准测试显示明显改善（响应时间降低 > 20%）
