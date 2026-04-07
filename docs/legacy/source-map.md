---
title: "Legacy Source Map（研究文档引用映射）"
status: draft
created: 2026-04-07
updated: 2026-04-07
related:
  - "./implementation-snapshot.md"
  - "../research/implementation-gap-analysis.md"
---

# Legacy Source Map（研究文档引用映射）

本表用于把历史研究文档中“指向源码文件/测试文件”的引用，映射为“指向文档化能力锚点”的引用，避免 docs-only 后出现断链。

## 规则

- 禁止：`file:///.../src/...`、`../../src/...`、`tests/...` 的路径引用
- 允许：指向 `docs/legacy/implementation-snapshot.md` 的能力锚点（例如 `EL-AgentLoop`）

## 映射（示例）

| 历史引用 | 新引用（docs-only） |
|---------|----------------------|
| `src/sherry_agent/execution/agent_loop.py` | `implementation-snapshot.md#el-agentloop` |
| `src/sherry_agent/llm/client.py` | `implementation-snapshot.md#el-llm-client` |
| `src/sherry_agent/autonomy/heartbeat.py` | `implementation-snapshot.md#aul-heartbeat` |
| `src/sherry_agent/cli/main.py` | `implementation-snapshot.md#il-cli-commandrouter` |
| `src/sherry_agent/cli/tui.py` | `implementation-snapshot.md#il-cli-tui` |
| `tests/benchmark/*` | “历史证据（代码已删除）”，必要时在研究文档内以表格摘要保留结论 |

> 后续在清理研究文档时，遇到新引用请补充到本表。
