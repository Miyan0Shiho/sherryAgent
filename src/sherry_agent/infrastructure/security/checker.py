
import asyncio
import hashlib

from ..cache import TTLCache
from .auto_classifier import CachedAutoModeClassifier
from .base import PermissionChecker, PermissionDecision, PermissionRequest, PermissionResult
from .enterprise_policy import EnterprisePolicy
from .rules import GlobalSecurityRules
from .sandbox import SandboxIsolation
from .user_rules import UserConfigRules


class ComprehensivePermissionChecker(PermissionChecker):
    """综合权限检查器，整合所有权限检查逻辑"""

    def __init__(self, allowed_paths: list[str] | None = None, llm_client=None):
        """初始化综合权限检查器

        Args:
            allowed_paths: 沙箱允许访问的路径列表
            llm_client: LLM客户端实例，用于自动模式分类器
        """
        if llm_client is None:
            from ...llm.client import MockLLMClient
            llm_client = MockLLMClient(responses=["low"])

        self.checkers = [
            GlobalSecurityRules(),
            CachedAutoModeClassifier(llm_client=llm_client),
            UserConfigRules(),
            EnterprisePolicy(),
            SandboxIsolation(allowed_paths=allowed_paths)
        ]

        self._permission_cache = TTLCache[tuple, PermissionResult](default_ttl=60.0, max_size=1000)

    def _make_cache_key(self, request: PermissionRequest) -> tuple:
        """生成缓存键

        Args:
            request: 权限请求

        Returns:
            缓存键元组
        """
        key_str = f"{request.tool_name}:{request.operation}:{request.target_path or ''}"
        return (hashlib.md5(key_str.encode()).hexdigest(),)

    def check(self, request: PermissionRequest) -> PermissionResult:
        """执行完整的权限检查流程

        检查流程：
        1. 全局安全规则检查
        2. 自动模式分类器检查
        3. 沙箱隔离检查

        Args:
            request: 权限请求

        Returns:
            权限决策结果
        """
        for checker in self.checkers:
            result = checker.check(request)
            if result.decision != PermissionDecision.ALLOW:
                return result

        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="所有权限检查通过",
            layer="comprehensive_checker"
        )

    async def async_check(self, request: PermissionRequest) -> PermissionResult:
        """执行异步权限检查流程

        检查流程：
        1. 检查缓存
        2. 全局安全规则检查
        3. 自动模式分类器检查（异步）
        4. 用户配置规则检查
        5. 企业策略检查
        6. 沙箱隔离检查
        7. 缓存结果

        Args:
            request: 权限请求

        Returns:
            权限决策结果
        """
        cache_key = self._make_cache_key(request)

        cached_result = await self._permission_cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        global_rules = GlobalSecurityRules()
        result = global_rules.check(request)
        if result.decision != PermissionDecision.ALLOW:
            await self._permission_cache.set(cache_key, result)
            return result

        for checker in self.checkers:
            if hasattr(checker, 'async_check') and asyncio.iscoroutinefunction(checker.async_check):
                result = await checker.async_check(request)
                if result.decision != PermissionDecision.ALLOW:
                    await self._permission_cache.set(cache_key, result)
                    return result
            elif hasattr(checker, 'check'):
                result = checker.check(request)
                if result.decision != PermissionDecision.ALLOW:
                    await self._permission_cache.set(cache_key, result)
                    return result

        result = PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="所有权限检查通过",
            layer="comprehensive_checker"
        )
        await self._permission_cache.set(cache_key, result)
        return result

    async def clear_cache(self) -> None:
        """清空权限检查缓存"""
        await self._permission_cache.clear()

    def get_cache_stats(self) -> dict:
        """获取缓存统计信息"""
        return self._permission_cache.get_stats()
