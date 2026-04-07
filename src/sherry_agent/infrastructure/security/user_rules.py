import os
import fnmatch
from .base import PermissionChecker, PermissionDecision, PermissionRequest, PermissionResult
from ...config.settings import settings
import toml
from typing import Dict, List, Optional


class UserConfigRules(PermissionChecker):
    """用户配置规则检查器
    
    从用户配置文件中读取权限规则，支持允许/拒绝列表
    """

    def __init__(self, config_path: Optional[str] = None):
        """初始化用户配置规则检查器

        Args:
            config_path: 配置文件路径，如果为 None，则使用默认路径
        """
        if config_path is None:
            self.config_path = os.path.expanduser("~/.agent/config.toml")
        else:
            self.config_path = config_path
        
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载用户配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return toml.load(f)
            except Exception:
                pass
        return {}

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查用户配置规则"""
        # 检查是否有用户配置
        permissions_config = self.config.get('permissions', {})
        
        # 检查拒绝列表
        deny_list = permissions_config.get('deny_list', {})
        if self._is_denied(request, deny_list):
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason="用户配置规则拒绝",
                layer="user_config_rules",
                audit_log_entry={
                    "tool": request.tool_name,
                    "operation": request.operation,
                    "target_path": request.target_path,
                    "reason": "用户配置规则拒绝",
                    "status": "denied"
                }
            )
        
        # 检查允许列表
        allow_list = permissions_config.get('allow_list', {})
        if self._is_allowed(request, allow_list):
            return PermissionResult(
                decision=PermissionDecision.ALLOW,
                reason="用户配置规则允许",
                layer="user_config_rules"
            )
        
        # 无匹配规则，继续下一层检查
        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="无用户配置规则匹配，继续检查",
            layer="user_config_rules"
        )

    def _is_denied(self, request: PermissionRequest, deny_list: Dict) -> bool:
        """检查是否在拒绝列表中"""
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
        
        return False

    def _is_allowed(self, request: PermissionRequest, allow_list: Dict) -> bool:
        """检查是否在允许列表中"""
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
        
        return False

    def _match_path(self, path: str, pattern: str) -> bool:
        """匹配路径模式"""
        # 规范化路径
        normalized_path = os.path.normpath(os.path.abspath(os.path.expanduser(path)))
        normalized_pattern = os.path.normpath(os.path.abspath(os.path.expanduser(pattern)))
        
        # 使用fnmatch进行模式匹配
        return fnmatch.fnmatch(normalized_path, normalized_pattern)
