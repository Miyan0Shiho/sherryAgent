# 性能优化 Spec

## Why

SherryAgent 在本地机器上运行时存在多个性能瓶颈，影响响应速度和资源利用效率。主要问题包括：
1. 数据库连接未复用，每次操作都创建新连接
2. HTTP 客户端每次请求都创建新 session
3. 记忆检索效率低下
4. 缺乏并发控制和资源限制
5. 缺乏性能监控和基准测试

## What Changes

### 核心优化
- **连接池管理**：为 aiosqlite 和 aiohttp 实现连接池复用
- **异步并发控制**：添加信号量限制并发操作数量
- **缓存机制**：为频繁访问的数据添加缓存层
- **批量操作**：优化数据库批量写入性能

### 记忆系统优化
- **Token 估算优化**：使用更精确的 tokenizer 替代简单正则
- **搜索优化**：使用 FTS5 全文搜索替代 LIKE 查询
- **连接复用**：LongTermMemory 复用数据库连接

### LLM 客户端优化
- **Session 复用**：OllamaClient 复用 aiohttp session
- **超时配置**：添加合理的请求超时设置
- **重试机制**：实现指数退避重试策略

### 资源管理
- **内存监控**：添加内存使用监控和告警
- **并发限制**：基于本地机器资源动态调整并发数
- **背压控制**：在高负载时自动降级

## Impact

- Affected specs: MVP-2 记忆系统、MVP-3 自主运行、MVP-4 多 Agent 编排
- Affected code:
  - `src/sherry_agent/llm/client.py` - LLM 客户端
  - `src/sherry_agent/memory/long_term.py` - 长期记忆
  - `src/sherry_agent/memory/short_term.py` - 短期记忆
  - `src/sherry_agent/execution/agent_loop.py` - Agent 循环
  - `src/sherry_agent/autonomy/heartbeat.py` - 心跳引擎
  - `src/sherry_agent/infrastructure/tool_executor.py` - 工具执行器

## ADDED Requirements

### Requirement: 连接池管理

系统 SHALL 提供连接池管理机制，复用数据库和 HTTP 连接。

#### Scenario: 数据库连接复用
- **WHEN** LongTermMemory 执行多次数据库操作
- **THEN** 应复用同一个数据库连接，而非每次创建新连接

#### Scenario: HTTP Session 复用
- **WHEN** OllamaClient 发送多次请求
- **THEN** 应复用同一个 aiohttp session

### Requirement: 异步并发控制

系统 SHALL 提供异步并发控制机制，防止资源耗尽。

#### Scenario: 并发限制
- **WHEN** 系统执行多个并发任务
- **THEN** 应通过信号量限制最大并发数，默认为 CPU 核心数 * 2

#### Scenario: 动态调整
- **WHEN** 系统资源紧张（内存使用 > 80%）
- **THEN** 应自动降低并发限制

### Requirement: 缓存机制

系统 SHALL 为频繁访问的数据提供缓存层。

#### Scenario: 权限检查缓存
- **WHEN** 对同一操作进行权限检查
- **THEN** 应缓存检查结果，有效期 60 秒

#### Scenario: 记忆搜索缓存
- **WHEN** 对相同查询进行记忆搜索
- **THEN** 应缓存搜索结果，有效期 30 秒

### Requirement: Token 估算优化

系统 SHALL 使用精确的 tokenizer 进行 token 估算。

#### Scenario: Tiktoken 集成
- **WHEN** 估算文本的 token 数量
- **THEN** 应使用 tiktoken 库进行精确估算，而非简单正则

#### Scenario: 降级策略
- **WHEN** tiktoken 不可用时
- **THEN** 应使用改进的启发式算法，误差 < 20%

### Requirement: 数据库搜索优化

系统 SHALL 使用 FTS5 全文搜索优化记忆检索。

#### Scenario: FTS5 索引创建
- **WHEN** LongTermMemory 初始化时
- **THEN** 应创建 FTS5 虚拟表用于全文搜索

#### Scenario: 全文搜索
- **WHEN** 搜索记忆内容
- **THEN** 应使用 FTS5 MATCH 查询，而非 LIKE

### Requirement: HTTP 客户端优化

系统 SHALL 为 HTTP 客户端添加超时和重试机制。

#### Scenario: 请求超时
- **WHEN** 发送 HTTP 请求
- **THEN** 应设置合理的连接超时（5s）和读取超时（30s）

#### Scenario: 重试机制
- **WHEN** HTTP 请求失败（网络错误或 5xx 错误）
- **THEN** 应使用指数退避重试，最多 3 次

### Requirement: 资源监控

系统 SHALL 提供资源使用监控功能。

#### Scenario: 内存监控
- **WHEN** 系统运行时
- **THEN** 应定期监控内存使用情况，超过阈值时发出警告

#### Scenario: 性能指标
- **WHEN** 执行关键操作
- **THEN** 应记录执行时间和资源消耗

### Requirement: 批量操作优化

系统 SHALL 支持数据库批量操作。

#### Scenario: 批量写入
- **WHEN** 需要写入多条记忆记录
- **THEN** 应使用批量插入，而非逐条插入

## MODIFIED Requirements

### Requirement: LongTermMemory 数据库管理

LongTermMemory SHALL 使用连接池管理数据库连接，并支持 FTS5 全文搜索。

**变更内容**：
- 添加 `_connection_pool` 属性管理连接
- 添加 `_ensure_connection()` 方法复用连接
- 添加 FTS5 虚拟表创建逻辑
- 修改 `search_memory()` 使用 FTS5 查询

### Requirement: OllamaClient HTTP 管理

OllamaClient SHALL 复用 HTTP session 并支持超时和重试。

**变更内容**：
- 添加 `_session` 属性管理 session
- 添加 `_get_session()` 方法延迟创建 session
- 添加超时配置
- 添加重试装饰器

### Requirement: ShortTermMemory Token 估算

ShortTermMemory SHALL 使用精确的 tokenizer 进行 token 估算。

**变更内容**：
- 添加 `_tokenizer` 属性
- 修改 `estimate_tokens()` 使用 tiktoken
- 添加降级策略

## REMOVED Requirements

无移除的需求。
