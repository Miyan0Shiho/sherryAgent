from .base import PermissionChecker, PermissionDecision, PermissionRequest, PermissionResult, RiskLevel
from typing import Optional, Dict, Any
import asyncio
import time


class AutoModeClassifier(PermissionChecker):
    """自动模式分类器，使用LLM评估操作风险等级"""

    def __init__(self, llm_client, model="llama3:8b", max_tokens=100):
        """初始化自动模式分类器

        Args:
            llm_client: LLM客户端实例
            model: 使用的LLM模型
            max_tokens: 最大token数
        """
        self.llm_client = llm_client
        self.model = model
        self.max_tokens = max_tokens
        self.cache: Dict[str, RiskLevel] = {}
        self.cache_timeout = 3600  # 缓存1小时

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查权限，使用LLM评估风险等级（同步版本）

        Args:
            request: 权限请求

        Returns:
            权限决策结果
        """
        # 生成缓存键
        cache_key = f"{request.tool_name}:{request.operation}:{request.target_path or ''}"
        
        # 检查缓存
        if cache_key in self.cache:
            risk_level = self.cache[cache_key]
        else:
            # 评估风险等级
            start_time = time.time()
            # 检查是否有运行中的事件循环
            try:
                loop = asyncio.get_running_loop()
                # 如果有运行中的事件循环，返回默认风险等级
                # 避免在已运行的事件循环中调用 run_until_complete
                risk_level = RiskLevel.MEDIUM
            except RuntimeError:
                # 如果没有运行中的事件循环，使用 asyncio.run()
                risk_level = asyncio.run(self._assess_risk(request))
            evaluation_time = time.time() - start_time
            
            # 缓存结果
            self.cache[cache_key] = risk_level
        
        # 根据风险等级做出决策
        decision = self._make_decision(risk_level)
        
        return PermissionResult(
            decision=decision,
            reason=f"基于LLM评估的风险等级: {risk_level.value}",
            layer="auto_mode_classifier",
            audit_log_entry={
                "risk_level": risk_level.value,
                "tool_name": request.tool_name,
                "operation": request.operation,
                "target_path": request.target_path,
                "context": request.context
            }
        )

    async def async_check(self, request: PermissionRequest) -> PermissionResult:
        """检查权限，使用LLM评估风险等级（异步版本）

        Args:
            request: 权限请求

        Returns:
            权限决策结果
        """
        # 生成缓存键
        cache_key = f"{request.tool_name}:{request.operation}:{request.target_path or ''}"
        
        # 检查缓存
        if cache_key in self.cache:
            risk_level = self.cache[cache_key]
        else:
            # 评估风险等级
            start_time = time.time()
            risk_level = await self._assess_risk(request)
            evaluation_time = time.time() - start_time
            
            # 缓存结果
            self.cache[cache_key] = risk_level
        
        # 根据风险等级做出决策
        decision = self._make_decision(risk_level)
        
        return PermissionResult(
            decision=decision,
            reason=f"基于LLM评估的风险等级: {risk_level.value}",
            layer="auto_mode_classifier",
            audit_log_entry={
                "risk_level": risk_level.value,
                "tool_name": request.tool_name,
                "operation": request.operation,
                "target_path": request.target_path,
                "context": request.context
            }
        )

    async def _assess_risk(self, request: PermissionRequest) -> RiskLevel:
        """使用LLM评估操作的风险等级

        Args:
            request: 权限请求

        Returns:
            风险等级
        """
        # 构建系统提示
        system_prompt = "你是一个安全风险评估专家，负责评估AI Agent操作的风险等级。"
        
        # 构建用户提示
        user_prompt = f"请评估以下操作的风险等级：\n"\
                     f"工具名称: {request.tool_name}\n"\
                     f"操作: {request.operation}\n"\
                     f"目标路径: {request.target_path or '无'}\n"\
                     f"上下文: {request.context or '无'}\n"\
                     f"\n"\
                     f"请从以下选项中选择一个风险等级：\n"\
                     f"- low: 低风险，安全操作\n"\
                     f"- medium: 中风险，需要注意但可以自动执行\n"\
                     f"- high: 高风险，需要人工确认\n"\
                     f"- critical: 严重风险，应直接拒绝\n"\
                     f"\n"\
                     f"请仅返回风险等级的英文单词，不要添加任何其他内容。"
        
        # 发送请求到LLM
        messages = [{"role": "user", "content": user_prompt}]
        
        try:
            response = await self.llm_client.chat(
                messages=messages,
                model=self.model,
                max_tokens=self.max_tokens,
                system_prompt=system_prompt
            )
            
            # 解析响应
            content = response.content.strip().lower()
            
            # 映射到RiskLevel枚举
            if content == "low":
                return RiskLevel.LOW
            elif content == "medium":
                return RiskLevel.MEDIUM
            elif content == "high":
                return RiskLevel.HIGH
            elif content == "critical":
                return RiskLevel.CRITICAL
            else:
                # 如果解析失败，默认返回中风险
                return RiskLevel.MEDIUM
        except Exception as e:
            # 如果LLM调用失败，默认返回中风险
            return RiskLevel.MEDIUM

    def _make_decision(self, risk_level: RiskLevel) -> PermissionDecision:
        """根据风险等级做出权限决策

        Args:
            risk_level: 风险等级

        Returns:
            权限决策
        """
        if risk_level == RiskLevel.LOW:
            return PermissionDecision.ALLOW
        elif risk_level == RiskLevel.MEDIUM:
            return PermissionDecision.ALLOW
        elif risk_level == RiskLevel.HIGH:
            return PermissionDecision.REQUIRE_CONFIRM
        elif risk_level == RiskLevel.CRITICAL:
            return PermissionDecision.DENY
        else:
            return PermissionDecision.ALLOW


class CachedAutoModeClassifier(AutoModeClassifier):
    """带缓存的自动模式分类器，提高性能"""

    def __init__(self, llm_client, model="llama3:8b", max_tokens=100, cache_size=1000):
        """初始化带缓存的自动模式分类器

        Args:
            llm_client: LLM客户端实例
            model: 使用的LLM模型
            max_tokens: 最大token数
            cache_size: 缓存大小
        """
        super().__init__(llm_client, model, max_tokens)
        self.cache_size = cache_size
        self.cache_timestamps: Dict[str, float] = {}

    def check(self, request: PermissionRequest) -> PermissionResult:
        """检查权限，使用缓存提高性能（同步版本）

        Args:
            request: 权限请求

        Returns:
            权限决策结果
        """
        # 生成缓存键
        cache_key = f"{request.tool_name}:{request.operation}:{request.target_path or ''}"
        
        # 检查缓存是否过期
        current_time = time.time()
        if cache_key in self.cache_timestamps:
            if current_time - self.cache_timestamps[cache_key] > self.cache_timeout:
                del self.cache[cache_key]
                del self.cache_timestamps[cache_key]
        
        # 检查缓存大小
        if len(self.cache) > self.cache_size:
            # 删除最旧的缓存项
            oldest_key = min(self.cache_timestamps, key=self.cache_timestamps.get)
            del self.cache[oldest_key]
            del self.cache_timestamps[oldest_key]
        
        # 检查缓存
        if cache_key in self.cache:
            risk_level = self.cache[cache_key]
        else:
            # 评估风险等级
            start_time = time.time()
            # 检查是否有运行中的事件循环
            try:
                loop = asyncio.get_running_loop()
                # 如果有运行中的事件循环，返回默认风险等级
                # 避免在已运行的事件循环中调用 run_until_complete
                risk_level = RiskLevel.MEDIUM
            except RuntimeError:
                # 如果没有运行中的事件循环，使用 asyncio.run()
                risk_level = asyncio.run(self._assess_risk(request))
            evaluation_time = time.time() - start_time
            
            # 缓存结果
            self.cache[cache_key] = risk_level
            self.cache_timestamps[cache_key] = current_time
        
        # 根据风险等级做出决策
        decision = self._make_decision(risk_level)
        
        return PermissionResult(
            decision=decision,
            reason=f"基于LLM评估的风险等级: {risk_level.value}",
            layer="cached_auto_mode_classifier",
            audit_log_entry={
                "risk_level": risk_level.value,
                "tool_name": request.tool_name,
                "operation": request.operation,
                "target_path": request.target_path,
                "context": request.context
            }
        )

    async def async_check(self, request: PermissionRequest) -> PermissionResult:
        """检查权限，使用缓存提高性能（异步版本）

        Args:
            request: 权限请求

        Returns:
            权限决策结果
        """
        # 生成缓存键
        cache_key = f"{request.tool_name}:{request.operation}:{request.target_path or ''}"
        
        # 检查缓存是否过期
        current_time = time.time()
        if cache_key in self.cache_timestamps:
            if current_time - self.cache_timestamps[cache_key] > self.cache_timeout:
                del self.cache[cache_key]
                del self.cache_timestamps[cache_key]
        
        # 检查缓存大小
        if len(self.cache) > self.cache_size:
            # 删除最旧的缓存项
            oldest_key = min(self.cache_timestamps, key=self.cache_timestamps.get)
            del self.cache[oldest_key]
            del self.cache_timestamps[oldest_key]
        
        # 检查缓存
        if cache_key in self.cache:
            risk_level = self.cache[cache_key]
        else:
            # 评估风险等级
            start_time = time.time()
            risk_level = await self._assess_risk(request)
            evaluation_time = time.time() - start_time
            
            # 缓存结果
            self.cache[cache_key] = risk_level
            self.cache_timestamps[cache_key] = current_time
        
        # 根据风险等级做出决策
        decision = self._make_decision(risk_level)
        
        return PermissionResult(
            decision=decision,
            reason=f"基于LLM评估的风险等级: {risk_level.value}",
            layer="cached_auto_mode_classifier",
            audit_log_entry={
                "risk_level": risk_level.value,
                "tool_name": request.tool_name,
                "operation": request.operation,
                "target_path": request.target_path,
                "context": request.context
            }
        )
