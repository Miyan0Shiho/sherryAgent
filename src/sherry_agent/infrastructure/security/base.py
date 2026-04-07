from dataclasses import dataclass
from enum import Enum
from typing import Any


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PermissionDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_CONFIRM = "require_confirm"


class PermissionType(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"


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


class PermissionChecker:
    """权限检查器基类"""

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查权限"""
        raise NotImplementedError
