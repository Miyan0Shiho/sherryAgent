
from .base import PermissionChecker, PermissionDecision, PermissionRequest, PermissionResult


class GlobalSecurityRules(PermissionChecker):
    """全局安全规则检查器"""

    # 禁止执行的危险命令
    DENIED_COMMANDS: list[str] = [
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

    # 禁止访问的路径
    DENIED_PATHS: list[str] = [
        "/etc/passwd",
        "/etc/shadow",
        "~/.ssh",
        "~/.aws",
        "~/.gnupg",
    ]

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查全局安全规则"""
        # 检查危险命令
        if self._is_dangerous_command(request.operation):
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason=f"执行危险命令被禁止: {request.operation}",
                layer="global_security_rules",
                audit_log_entry={
                    "tool": request.tool_name,
                    "operation": request.operation,
                    "reason": "危险命令拦截",
                    "status": "denied"
                }
            )

        # 检查危险路径
        if request.target_path and self._is_dangerous_path(request.target_path):
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason=f"访问危险路径被禁止: {request.target_path}",
                layer="global_security_rules",
                audit_log_entry={
                    "tool": request.tool_name,
                    "operation": request.operation,
                    "target_path": request.target_path,
                    "reason": "危险路径拦截",
                    "status": "denied"
                }
            )

        # 规则通过
        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="全局安全规则检查通过",
            layer="global_security_rules"
        )

    def _is_dangerous_command(self, operation: str) -> bool:
        """检查是否为危险命令"""
        operation_lower = operation.lower()
        for denied_cmd in self.DENIED_COMMANDS:
            if denied_cmd.lower() in operation_lower:
                return True
        return False

    def _is_dangerous_path(self, path: str) -> bool:
        """检查是否为危险路径"""
        for denied_path in self.DENIED_PATHS:
            if denied_path in path:
                return True
        return False
