---
title: "实现蒸馏快照（Pre-Phoenix Implementation Snapshot）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "../vision/north-star.md"
  - "../reference/glossary.md"
  - "../specs/six-layer-architecture.md"
---

# 实现蒸馏快照（Pre-Phoenix Implementation Snapshot）

> 本文档用于承接“已删除的实现代码”所曾经覆盖的能力形态，供研究文档与后续实现计划引用。
>
> - 这是**文字版快照**：不包含源码，不保证可运行。
> - 任何研究文档不应再链接 `file:///.../src/...`，而应链接本文档的能力锚点。

## Interface Layer（交互层）

### IL-CLI-TUI

曾经具备：Textual TUI 的交互式界面，支持输入任务、流式输出文本与工具调用过程。

关键行为：
- 支持用户输入触发 agent loop
- 输出包含 text/tool_use/tool_result/error 等事件信息

### IL-CLI-CommandRouter

曾经具备：基于 Click 的 CLI 命令入口与参数解析雏形（`run/status/plugin` 等命令口径），并尝试支持“后台/daemon”运行模式。

关键行为：
- 命令层级与 help 输出（基本可用但示例不足）
- 参数优先级口径：命令行 > 环境变量（以 API Key 为主） > 默认值
- 后台模式（daemon）作为设计目标，但跨平台与进程管理能力不足（缺少 stop/restart/logs）

### IL-WebSocket

曾经具备：WebSocket 状态推送服务的雏形，用于将后台状态更新推送给客户端。

关键行为：
- 连接管理
- 状态广播（heartbeat/status/cron/pending_tasks 等概念）

### IL-HTTP-API

曾经具备：HTTP API 的雏形（基础端点/状态端点），完整的任务 CRUD 作为设计目标但未完全落地。

## Orchestration Layer（编排层）

### OL-Orchestrator

曾经具备：LLM 驱动的任务分解（JSON 子任务列表），支持依赖解析与拓扑排序执行。

关键行为：
- `decompose(task_description) -> subtasks[]`
- DAG 拓扑排序
- 通过 Lane 提交/等待结果并汇总

### OL-Teams

曾经具备：Team Lead / Teammate 的角色结构（能力展示层面）。

### OL-Lane

曾经具备：并发控制通道（session 串行 + global 并发）的雏形，用于限制工具调用与子任务并发。

## Execution Layer（执行层）

### EL-AgentLoop

曾经具备：异步生成器风格的 agent loop，输出事件流（TEXT/TOOL_USE/TOOL_RESULT/ERROR），具备 token budget 追踪与停止策略。

关键行为：
- 轮次上限（max_tool_rounds）
- token 预算上限（token_budget）
- 工具调用：单/多工具调用，读操作可并发，写操作倾向串行

### EL-LLM-Client

曾经具备：LLM 客户端封装雏形（Anthropic/OpenAI/Ollama 等口径），支持流式输出与事件化转换（作为 `EL-AgentLoop` 的上游依赖）。

关键行为：
- 流式响应转事件（text/tool_use/tool_result/error）
- 统一请求参数与模型选择口径
- token usage 统计作为目标，但在小模型/本地推理场景下统计不稳定（常见“全 0”问题）

### EL-ToolExecution

曾经具备：ToolExecutor 抽象与具体实现，支持：
- 内置工具（file/http/shell）
- MCP 远程工具调用格式（`mcp://...`）
- 权限检查（见 Infrastructure Layer）

### EL-Fork

曾经具备：子 Agent 派生（Fork）的雏形：继承部分上下文/提示，执行子任务并回传结果（作为多 agent 编排能力的一部分）。

## Autonomy Layer（自主运行层）

### AUL-Heartbeat

曾经具备：heartbeat while-true 循环，读取待办、按并发上限执行、写状态、推送 WebSocket 状态。

关键行为：
- 低功耗模式（idle 后延长间隔）
- 资源监控（CPU/内存阈值告警）

### AUL-Scheduler

曾经具备：APScheduler 集成（cron/interval/date）用于定时触发任务。

### AUL-Recovery

曾经具备：断点续传/恢复作为设计目标与部分实现雏形（状态快照与恢复策略未完全成熟）。

## Memory Layer（记忆层）

### ML-ShortTerm

曾经具备：短期记忆 token 估算 + 多级压缩策略（micro/auto/session/reactive 的简化实现形态）。

### ML-LongTerm

曾经具备：SQLite/检索接口的长期记忆雏形（含混合检索的设计口径）。

### ML-Bridge

曾经具备：短期到长期的桥接接口（以“提取/写入”为目标口径）。

## Infrastructure Layer（基础设施层）

### IFL-Permissions

曾经具备：多层权限管道的实现雏形（全局规则/自动分类/用户规则/企业策略/沙箱隔离的组合）。

关键行为：
- 对命令/路径进行拦截或要求确认
- 支持缓存（TTL）减少重复判定成本

### IFL-Monitoring

曾经具备：资源监控与阈值告警的实现雏形（CPU/内存），并在自主运行（heartbeat）场景中用于“自检与降级”。

关键行为：
- 采集基础资源指标（CPU/内存）
- 阈值触发告警事件（作为可观测性与运维 Story 的依赖能力）

### IFL-TokenEstimator

曾经具备：文本 token 数估算接口与简化实现，用于在没有 provider usage 的情况下做粗略预算与截断策略。

### IFL-TokenAccounting

曾经具备：token 预算与 token usage 统计的接口与数据结构雏形（作为“成本/性能可观测性”的基础）。

关键行为：
- 预算上限：超过预算必须停止或降级
- 统计口径：input/output/cache_read/cache_creation（设计口径）
- 已知缺陷：在某些 provider（尤其本地模型）上，usage 字段缺失或解析失败，导致统计为 0

### IFL-Sandbox

曾经具备：路径隔离与安全规则拦截（网络隔离为设计目标，未必完全落地）。

### IFL-MCP

曾经具备：MCP 客户端/协议模块雏形（服务端为可选）。

### IFL-Skills-Plugins

曾经具备：pluggy 插件/skill 解析与加载的雏形。

## Evaluation & Evidence（评测与证据，已删除实现）

### EV-BenchmarkHarness

曾经具备：基准评测与结果汇总脚本/runner 的雏形，用于对小模型（如 `qwen3:0.6b`）进行任务集跑分与日志汇总。

关键行为：
- 任务集分层（如简单/中等/困难的口径）
- 生成 summary JSON/Markdown（作为研究文档证据）
- docs-only 现状：相关实现与日志均已删除，仅保留研究结论与本文档的能力锚点引用
