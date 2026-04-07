import os
import pytest

from src.sherry_agent.infrastructure.security import ComprehensivePermissionChecker, PermissionRequest, RiskLevel


def test_comprehensive_checker_allow_safe_operation():
    """测试综合权限检查器允许安全操作"""
    current_dir = os.getcwd()
    checker = ComprehensivePermissionChecker(allowed_paths=[current_dir])
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path=os.path.join(current_dir, "test.txt"),
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == "allow"
    assert "所有权限检查通过" in result.reason


def test_comprehensive_checker_deny_dangerous_command():
    """测试综合权限检查器拒绝危险命令"""
    checker = ComprehensivePermissionChecker()
    request = PermissionRequest(
        tool_name="exec_command",
        operation="rm -rf /",
        risk_level=RiskLevel.CRITICAL
    )
    result = checker.check(request)
    assert result.decision.value == "deny"
    assert "执行危险命令被禁止" in result.reason


def test_comprehensive_checker_deny_external_path():
    """测试综合权限检查器拒绝超出沙箱范围的路径"""
    current_dir = os.getcwd()
    checker = ComprehensivePermissionChecker(allowed_paths=[current_dir])
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path="/etc/passwd",
        risk_level=RiskLevel.MEDIUM
    )
    result = checker.check(request)
    assert result.decision.value == "deny"
    assert "访问危险路径被禁止" in result.reason


@pytest.mark.asyncio
async def test_async_check_caching():
    """测试异步权限检查的缓存功能"""
    current_dir = os.getcwd()
    checker = ComprehensivePermissionChecker(allowed_paths=[current_dir])
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path=os.path.join(current_dir, "test.txt"),
        risk_level=RiskLevel.LOW
    )
    
    result1 = await checker.async_check(request)
    assert result1.decision.value == "allow"
    
    stats = checker.get_cache_stats()
    assert stats['size'] == 1
    
    result2 = await checker.async_check(request)
    assert result2.decision.value == "allow"
    
    stats = checker.get_cache_stats()
    assert stats['hits'] == 1


@pytest.mark.asyncio
async def test_async_check_cache_different_requests():
    """测试不同请求的缓存隔离"""
    current_dir = os.getcwd()
    checker = ComprehensivePermissionChecker(allowed_paths=[current_dir])
    
    request1 = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path=os.path.join(current_dir, "test1.txt"),
        risk_level=RiskLevel.LOW
    )
    
    request2 = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path=os.path.join(current_dir, "test2.txt"),
        risk_level=RiskLevel.LOW
    )
    
    await checker.async_check(request1)
    await checker.async_check(request2)
    
    stats = checker.get_cache_stats()
    assert stats['size'] == 2


@pytest.mark.asyncio
async def test_clear_cache():
    """测试清空缓存"""
    current_dir = os.getcwd()
    checker = ComprehensivePermissionChecker(allowed_paths=[current_dir])
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path=os.path.join(current_dir, "test.txt"),
        risk_level=RiskLevel.LOW
    )
    
    await checker.async_check(request)
    
    stats = checker.get_cache_stats()
    assert stats['size'] == 1
    
    await checker.clear_cache()
    
    stats = checker.get_cache_stats()
    assert stats['size'] == 0