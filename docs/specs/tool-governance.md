---
title: "Tool Governance Contracts"
status: draft
created: 2026-04-08
updated: 2026-04-08
related:
  - "./permission-system.md"
  - "./agent-loop.md"
  - "../architecture/module-map.md"
---

# Tool Governance Contracts

## 最小工具契约

每个工具都必须声明：

- `tool_id`
- `tool_type`
- `risk_class`
- `input_schema`
- `output_schema`
- `timeout_ms`
- `idempotency_behavior`
- `retry_policy`
- `side_effect_level`
- `requires_confirmation`
- `credential_scope`
- `replay_mode`

## 工具分类

- `READ_ONLY`：只读查询、扫描、收集
- `WRITE`：可逆写入、文档或配置更新
- `HIGH_RISK`：命令执行、触网调用、批量写入、敏感目录访问
- `DESTRUCTIVE`：删除、覆盖、服务重启、生产变更、权限修改

默认策略：

- `READ_ONLY` 可在低风险模式下自动执行
- `WRITE` 必须受风险和预算共同约束
- `HIGH_RISK` 默认要求确认或强策略放行
- `DESTRUCTIVE` 默认阻断，除非明确人工批准

## 接入边界

- `CLI / local tool`：受本地路径、仓库边界、沙箱和命令策略约束
- `MCP tool`：受服务声明能力、会话上下文和凭证范围约束
- `HTTP / API tool`：受目标域、鉴权范围、重试与速率限制约束

工具接入只负责执行，不负责替代 `Policy & Guardrail` 做最终风险裁决。

## 回放与模拟运行

- `replay_mode` 必须声明 `full | partial | metadata_only | none`
- 高风险和破坏性工具必须至少支持元数据级回放
- 需要 dry-run 的工具必须声明模拟输出格式，避免用真实副作用试错

## 可靠性规则

- 幂等策略必须写明 `idempotent | conditionally_idempotent | non_idempotent`
- 重试必须受 `retry_policy` 限制，不能对 `DESTRUCTIVE` 工具默认盲重试
- 外部依赖失败时必须产生 `Evidence` 和 `Decision`，说明失败点、降级路径和是否需要人工接管

## 与核心对象的关系

- 每次工具调用都必须可回链到所属 `Run`
- 关键工具结果必须形成 `Evidence`
- 权限放行、阻断、确认、降级必须形成 `Decision`
- 工具开销必须进入 `Cost Record`
