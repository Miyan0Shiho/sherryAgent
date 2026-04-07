import os
import fnmatch
from .base import PermissionChecker, PermissionDecision, PermissionRequest, PermissionResult
import toml
from typing import Dict, Optional


class EnterprisePolicy(PermissionChecker):
    """企业级策略检查器
    
    组织级权限策略，优先级高于用户配置
    """

    def __init__(self, policy_path: Optional[str] = None):
        """初始化企业策略检查器

        Args:
            policy_path: 企业策略文件路径，如果为 None，则使用默认路径
        """
        if policy_path is None:
            # 默认企业策略路径
            self.policy_path = os.path.expanduser("/etc/sherry_agent/enterprise_policy.toml")
        else:
            self.policy_path = policy_path
        
        self.policy = self._load_policy()

    def _load_policy(self) -> Dict:
        """加载企业策略文件"""
        if os.path.exists(self.policy_path):
            try:
                with open(self.policy_path, 'r', encoding='utf-8') as f:
                    return toml.load(f)
            except Exception:
                pass
        return {}

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查企业策略"""
        # 检查是否有企业策略
        policy_config = self.policy.get('enterprise_policy', {})
        
        # 检查全局策略
        global_policy = policy_config.get('global', {})
        if global_policy.get('enforce', False):
            # 检查拒绝列表
            deny_list = policy_config.get('deny_list', {})
            if self._is_denied(request, deny_list):
                return PermissionResult(
                    decision=PermissionDecision.DENY,
                    reason="企业策略拒绝",
                    layer="enterprise_policy",
                    audit_log_entry={
                        "tool": request.tool_name,
                        "operation": request.operation,
                        "target_path": request.target_path,
                        "reason": "企业策略拒绝",
                        "status": "denied"
                    }
                )
            
            # 检查允许列表
            allow_list = policy_config.get('allow_list', {})
            if self._is_allowed(request, allow_list):
                return PermissionResult(
                    decision=PermissionDecision.ALLOW,
                    reason="企业策略允许",
                    layer="enterprise_policy"
                )
        
        # 无企业策略或未启用，继续下一层检查
        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="无企业策略或未启用，继续检查",
            layer="enterprise_policy"
        )

    def _is_denied(self, request: PermissionRequest, deny_list: Dict) -> bool:
        """检查是否在企业策略拒绝列表中"""
        # 检查命令拒绝列表
        denied_commands = deny_list.get('commands', [])
        for cmd_pattern in denied_commands:
            if fnmatch.fnmatch(request.operation, cmd_pattern):
                return True
        
        # 检查路径拒绝列表
        if request.target_path:
            denied_paths = deny_list.get('paths', [])
            for path_pattern in denied_paths:
                if self._match_path(request.target_path, path_pattern):
                    return True
        
        # 检查危险操作类型
        denied_operations = deny_list.get('operations', [])
        if request.operation in denied_operations:
            return True
        
        return False

    def _is_allowed(self, request: PermissionRequest, allow_list: Dict) -> bool:
        """检查是否在企业策略允许列表中"""
        # 检查命令允许列表
        allowed_commands = allow_list.get('commands', [])
        for cmd_pattern in allowed_commands:
            if fnmatch.fnmatch(request.operation, cmd_pattern):
                return True
        
        # 检查路径允许列表
        if request.target_path:
            allowed_paths = allow_list.get('paths', [])
            for path_pattern in allowed_paths:
                if self._match_path(request.target_path, path_pattern):
                    return True
        
        # 检查允许的操作类型
        allowed_operations = allow_list.get('operations', [])
        if request.operation in allowed_operations:
            return True
        
        return False

    def _match_path(self, path: str, pattern: str) -> bool:
        """匹配路径模式"""
        # 规范化路径
        normalized_path = os.path.normpath(os.path.abspath(os.path.expanduser(path)))
        normalized_pattern = os.path.normpath(os.path.abspath(os.path.expanduser(pattern)))
        
        # 使用fnmatch进行模式匹配
        return fnmatch.fnmatch(normalized_path, normalized_pattern)
