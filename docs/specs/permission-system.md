---
title: "Policy & Guardrail 契约"
status: approved
created: 2026-04-03
updated: 2026-04-07
related:
  - "../architecture/module-map.md"
  - "../architecture/runtime-modes.md"
  - "./core-data-contracts.md"
---

# Policy & Guardrail 契约

权限系统现在统一收敛为 `Policy & Guardrail` 模块。它不仅做“允许/拒绝”，还负责确认、降级、审计和策略解释。

## 职责

- 风险分级
- 策略匹配
- 确认流
- 沙箱要求
- 审计记录
- 降级或阻断决策

## 核心原则

- 高风险动作默认不自动化
- 后台模式与批量模式必须比交互模式更保守
- 策略不只是安全红线，还要解释“为什么阻断”
- 任何允许或拒绝都要能回放

## 风险等级

- `LOW`：只读分析、低风险收集
- `MEDIUM`：文档写入、低影响配置更新
- `HIGH`：执行命令、触网、批量写入、敏感路径操作
- `CRITICAL`：生产变更、服务重启、删除、凭据或权限策略修改

## 决策输出

每次策略裁决至少要输出：

- `decision_type`
- `policy_basis`
- `requires_human`
- `approved_by`
- `reason`

## 与运行模式的关系

- `interactive-dev`：允许更多人工确认
- `autonomous-safe`：默认只读，写入最小化
- `background-ops`：证据优先，修复必须确认
- `bulk-analysis`：范围限制、预算限制、数据最小化

