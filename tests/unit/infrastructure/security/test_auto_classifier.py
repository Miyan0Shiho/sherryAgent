import asyncio
import time
import pytest
from src.sherry_agent.infrastructure.security.auto_classifier import AutoModeClassifier, CachedAutoModeClassifier
from src.sherry_agent.infrastructure.security.base import PermissionRequest, RiskLevel, PermissionDecision
from src.sherry_agent.llm.client import MockLLMClient


@pytest.fixture
async def mock_llm_client():
    """创建一个模拟的LLM客户端"""
    return MockLLMClient(responses=["low", "low", "low", "low"])


@pytest.fixture
async def auto_classifier(mock_llm_client):
    """创建一个自动模式分类器实例"""
    return AutoModeClassifier(llm_client=mock_llm_client)


@pytest.fixture
async def cached_auto_classifier(mock_llm_client):
    """创建一个带缓存的自动模式分类器实例"""
    return CachedAutoModeClassifier(llm_client=mock_llm_client)


async def test_auto_mode_classifier_risk_assessment():
    """测试自动模式分类器的风险评估功能"""
    # 创建一个返回不同风险等级的模拟LLM客户端
    mock_llm = MockLLMClient(responses=["low", "medium", "high", "critical"])
    auto_classifier = AutoModeClassifier(llm_client=mock_llm)
    
    # 测试低风险操作
    request = PermissionRequest(
        tool_name="file",
        operation="read",
        target_path="/tmp/test.txt"
    )
    result = await auto_classifier.async_check(request)
    assert result.decision == PermissionDecision.ALLOW
    
    # 测试中风险操作
    request = PermissionRequest(
        tool_name="file",
        operation="write",
        target_path="/tmp/test.txt"
    )
    result = await auto_classifier.async_check(request)
    assert result.decision == PermissionDecision.ALLOW
    
    # 测试高风险操作
    request = PermissionRequest(
        tool_name="shell",
        operation="execute",
        target_path="rm -rf /tmp"
    )
    result = await auto_classifier.async_check(request)
    assert result.decision == PermissionDecision.REQUIRE_CONFIRM
    
    # 测试严重风险操作
    request = PermissionRequest(
        tool_name="shell",
        operation="execute",
        target_path="rm -rf /"
    )
    result = await auto_classifier.async_check(request)
    assert result.decision == PermissionDecision.DENY


async def test_cached_auto_mode_classifier_performance(cached_auto_classifier):
    """测试带缓存的自动模式分类器的性能"""
    # 测试首次评估时间
    request = PermissionRequest(
        tool_name="file",
        operation="read",
        target_path="/tmp/test.txt"
    )
    
    start_time = time.time()
    result1 = await cached_auto_classifier.async_check(request)
    evaluation_time1 = time.time() - start_time
    print(f"首次评估时间: {evaluation_time1}秒")
    assert evaluation_time1 < 1.0  # 首次评估时间应小于1秒
    
    # 测试缓存评估时间
    start_time = time.time()
    result2 = await cached_auto_classifier.async_check(request)
    evaluation_time2 = time.time() - start_time
    print(f"缓存评估时间: {evaluation_time2}秒")
    assert evaluation_time2 < 0.1  # 缓存评估时间应小于0.1秒
    
    # 验证两次评估结果相同
    assert result1.decision == result2.decision


async def test_auto_mode_classifier_error_handling(auto_classifier):
    """测试自动模式分类器的错误处理能力"""
    # 模拟LLM客户端抛出异常
    class ErrorLLMClient:
        async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
            raise Exception("LLM API 错误")
    
    error_classifier = AutoModeClassifier(llm_client=ErrorLLMClient())
    
    # 测试错误处理
    request = PermissionRequest(
        tool_name="file",
        operation="read",
        target_path="/tmp/test.txt"
    )
    result = await error_classifier.async_check(request)
    # 当LLM调用失败时，应默认返回中风险
    assert result.decision == PermissionDecision.ALLOW


async def test_cached_auto_mode_classifier_cache_management(cached_auto_classifier):
    """测试带缓存的自动模式分类器的缓存管理功能"""
    # 创建多个不同的请求
    requests = [
        PermissionRequest(
            tool_name="file",
            operation="read",
            target_path="/tmp/test1.txt"
        ),
        PermissionRequest(
            tool_name="file",
            operation="read",
            target_path="/tmp/test2.txt"
        ),
        PermissionRequest(
            tool_name="file",
            operation="write",
            target_path="/tmp/test1.txt"
        )
    ]
    
    # 执行所有请求
    results = []
    for request in requests:
        result = await cached_auto_classifier.async_check(request)
        results.append(result)
    
    # 验证所有请求都通过
    for result in results:
        assert result.decision == PermissionDecision.ALLOW
    
    # 验证缓存大小
    assert len(cached_auto_classifier.cache) == 3


if __name__ == "__main__":
    asyncio.run(test_auto_mode_classifier_risk_assessment(auto_classifier))
    asyncio.run(test_cached_auto_mode_classifier_performance(cached_auto_classifier))
    asyncio.run(test_auto_mode_classifier_error_handling(auto_classifier))
    asyncio.run(test_cached_auto_mode_classifier_cache_management(cached_auto_classifier))
