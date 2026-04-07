---
title: "MVP-2 记忆与持久化 详细计划"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["mvp-roadmap.md", "mvp-1-plan.md"]
---

# MVP-2 记忆与持久化 详细计划

## 目标

实现上下文压缩和任务持久化，支持会话中断后断点续传和跨会话记忆检索。

## 实现范围

- 短期记忆：token预算管理 + micro-compact + auto-compact
- 长期记忆：SQLite + FTS5 + 基础BM25检索
- 任务持久化：state.json + transcript.jsonl + heartbeat.md
- 断点续传：启动时扫描未完成任务，从最后成功步骤恢复
- 记忆桥接：会话结束时提取关键信息写入长期记忆

## 任务列表

### Week 1-2

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T1.1 | 短期记忆基础结构 | P0 |
| T1.2 | Micro-Compact 实现 | P0 |
| T1.3 | Auto-Compact 实现 | P0 |
| T1.4 | 长期记忆存储 | P0 |

### Week 3

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T2.1 | 混合检索实现 | P0 |
| T2.2 | 任务持久化 | P0 |
| T2.3 | 断点续传 | P0 |
| T2.4 | 记忆桥接 | P1 |
| T2.5 | 集成测试 | P1 |

## 技术要点

### 四层压缩策略

```python
class ShortTermMemory:
    async def compact(
        self, messages: list[dict], level: str = "auto"
    ) -> list[dict]:
        """
        压缩级别：
        - micro: 单条消息截断，保留首尾
        - auto: LLM摘要压缩早期对话
        - session: 提取结构化知识到session memory
        - reactive: 激进压缩，仅保留最近N轮
        """
        if level == "micro":
            return self._micro_compact(messages)
        elif level == "auto":
            return await self._auto_compact(messages)
        elif level == "session":
            return await self._session_compact(messages)
        else:
            return self._reactive_compact(messages)
```

### 混合检索评分

```python
def calculate_score(
    entry: MemoryEntry,
    query_embedding: list[float],
    bm25_score: float,
) -> float:
    """混合检索评分公式"""
    relevance = cosine_similarity(query_embedding, entry.embedding)
    recency = calculate_recency(entry.accessed_at)
    importance = entry.importance

    return (
        0.3 * bm25_score +
        0.5 * relevance +
        0.2 * importance +
        0.3 * recency
    )
```

## 验收标准

| 编号 | 验收条件 | 验证方式 |
|------|---------|---------|
| 2.1 | 长对话自动触发上下文压缩 | 压力测试 |
| 2.2 | 压缩后保留关键信息 | 回归测试 |
| 2.3 | 任务执行过程写入transcript.jsonl | 文件检查 |
| 2.4 | 进程崩溃后重启可恢复未完成任务 | 崩溃恢复测试 |
| 2.5 | 跨会话可检索到历史记忆 | 集成测试 |

## 依赖

- MVP-1 的 Agent Loop
- aiosqlite >= 0.20
- sqlite-vec >= 0.1
- sentence-transformers >= 3.0
