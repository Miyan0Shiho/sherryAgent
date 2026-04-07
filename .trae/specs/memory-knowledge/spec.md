# SherryAgent - Memory Knowledge Spec

## Overview
- **Summary**: 定义短期上下文、长期记忆、检索、压缩、TTL、知识版本化和冷热分层。
- **Purpose**: 保证复杂任务、多轮运行和批量场景下的信息一致性与成本可控。

## Goals
- 固定短期与长期记忆边界
- 固定检索与证据引用的基本规则
- 固定 10x / 100x 下的索引与冷热策略

## Non-Goals
- 不在本阶段挑选具体数据库或向量引擎实现

## Acceptance Criteria
- 上下文压缩、长期记忆、证据引用之间的关系清晰
- 扩容时的分层与归档策略明确

