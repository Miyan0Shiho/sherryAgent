---
title: "权限系统模块设计"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["agent-loop.md", "runtime-modes.md"]
---

# 权限系统模块设计

权限系统为所有Agent操作提供安全保障，采用六层管道实现纵深防御。每一层都可以独立拦截危险操作，确保即使某一层被绕过，后续层仍能提供保护。

## 六层权限管道

```
工具调用请求
    │
    ▼
┌─────────────────────────────────────┐
│ 第1层：工具声明式权限                 │
│ 工具自身声明所需权限（读/写/执行/网络）│
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│ 第2层：全局安全规则                   │
│ 禁止列表：rm -rf /、DROP TABLE 等    │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│ 第3层：自动模式分类器                 │
│ LLM判断操作风险等级（低/中/高）       │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│ 第4层：用户配置规则                   │
│ .agent/config.toml 中的自定义规则    │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│ 第5层：企业策略（可选）               │
│ 组织级安全策略覆盖                    │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│ 第6层：沙箱隔离                      │
│ 文件系统路径限制 + 网络白名单         │
└──────────────┬──────────────────────┘
               ▼
          允许 / 拒绝
```

## 各层职责

| 层级 | 名称 | 检查内容 | 可配置性 |
|------|------|----------|----------|
| 第1层 | 工具声明式权限 | 输入校验、参数验证、路径安全 | 工具内置 |
| 第2层 | 全局安全规则 | 禁止危险操作（如 `rm -rf /`）、敏感信息过滤 | Anthropic 内置 |
| 第3层 | 自动模式分类器 | LLM 判断操作安全性，并行运行多个 Resolver | `--permission-mode auto` |
| 第4层 | 用户配置规则 | Glob 模式匹配的允许/拒绝规则 | 用户自定义 |
| 第5层 | 企业策略 | 组织级权限策略、合规审计 | 企业管理员配置 |
| 第6层 | 沙箱隔离 | 文件系统访问限制、网络访问白名单 | 运行时强制 |

## 核心数据结构

```python
from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PermissionDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_CONFIRM = "require_confirm"


@dataclass
class PermissionRequest:
    """权限请求"""

    tool_name: str
    operation: str
    target_path: str | None = None
    risk_level: RiskLevel = RiskLevel.LOW
    context: str = ""


@dataclass
class PermissionResult:
    """权限决策结果"""

    decision: PermissionDecision
    reason: str
    layer: str  # 哪一层做出的决策
    audit_log_entry: dict[str, Any] | None = None
```

## 后台模式策略

后台自主模式下，权限系统调整为"自动模式 + 审计日志 + 异常告警"：

| 风险等级 | 处理方式 |
|----------|----------|
| 低风险操作 | 自动放行，记录审计日志 |
| 中风险操作 | 自动放行，记录审计日志 + 推送通知 |
| 高风险操作 | 暂停执行，推送告警等待人工确认 |
| 严重风险操作 | 直接拒绝，推送紧急告警 |

## 危险命令列表

### 禁止执行的命令

```python
DENIED_COMMANDS = [
    "rm -rf /",
    "rm -rf /*",
    "rm -rf ~",
    "rm -rf ~/*",
    "DROP TABLE",
    "DELETE FROM",
    "TRUNCATE",
    ":(){ :|:& };:",  # Fork bomb
    "mkfs",
    "dd if=/dev/zero",
]
```

### 禁止访问的路径

```python
DENIED_PATHS = [
    "/etc/passwd",
    "/etc/shadow",
    "~/.ssh",
    "~/.aws",
    "~/.gnupg",
]
```

## 配置示例

```toml
# .agent/config.toml

[permissions]
auto_mode = false  # CLI模式默认关闭，后台模式默认开启
audit_log = true
alert_on_high_risk = true

[permissions.deny_list]
commands = ["rm -rf /", "DROP TABLE", "DELETE FROM"]
paths = ["/etc", "~/.ssh", "~/.aws"]

[permissions.allow_list]
paths = ["~/projects/*", "/tmp/*"]
commands = ["git", "npm", "python"]
```
