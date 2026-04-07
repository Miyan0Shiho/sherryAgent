import os

from .base import PermissionChecker, PermissionDecision, PermissionRequest, PermissionResult


class SandboxIsolation(PermissionChecker):
    """沙箱隔离检查器"""

    def __init__(self, allowed_paths: list[str] | None = None):
        """初始化沙箱隔离器

        Args:
            allowed_paths: 允许访问的路径列表，如果为 None，则默认允许当前工作目录
        """
        if allowed_paths is None:
            self.allowed_paths = [os.getcwd()]
        else:
            self.allowed_paths = allowed_paths

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查沙箱隔离规则"""
        # 如果没有目标路径，直接通过
        if not request.target_path:
            return PermissionResult(
                decision=PermissionDecision.ALLOW,
                reason="无目标路径，沙箱检查通过",
                layer="sandbox_isolation"
            )

        # 检查路径是否在允许的范围内
        if self._is_path_allowed(request.target_path):
            return PermissionResult(
                decision=PermissionDecision.ALLOW,
                reason="路径在允许范围内，沙箱检查通过",
                layer="sandbox_isolation"
            )
        else:
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason=f"路径超出沙箱范围: {request.target_path}",
                layer="sandbox_isolation",
                audit_log_entry={
                    "tool": request.tool_name,
                    "operation": request.operation,
                    "target_path": request.target_path,
                    "reason": "沙箱路径限制",
                    "status": "denied"
                }
            )

    def _is_path_allowed(self, path: str) -> bool:
        """检查路径是否在允许范围内"""
        # 规范化路径
        normalized_path = os.path.normpath(os.path.abspath(os.path.expanduser(path)))

        # 检查是否在允许的路径内
        for allowed_path in self.allowed_paths:
            normalized_allowed = os.path.normpath(os.path.abspath(os.path.expanduser(allowed_path)))
            if normalized_path.startswith(normalized_allowed + os.sep) or normalized_path == normalized_allowed:
                return True

        return False
