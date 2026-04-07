import pytest

from src.sherry_agent.infrastructure.security import GlobalSecurityRules, PermissionRequest, RiskLevel


def test_global_security_rules_allow_safe_command():
    """测试全局安全规则允许安全命令"""
    checker = GlobalSecurityRules()
    request = PermissionRequest(
        tool_name="exec_command",
        operation="ls -la",
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == "allow"
    assert "全局安全规则检查通过" in result.reason


def test_global_security_rules_deny_dangerous_command():
    """测试全局安全规则拒绝危险命令"""
    checker = GlobalSecurityRules()
    request = PermissionRequest(
        tool_name="exec_command",
        operation="rm -rf /",
        risk_level=RiskLevel.CRITICAL
    )
    result = checker.check(request)
    assert result.decision.value == "deny"
    assert "执行危险命令被禁止" in result.reason


def test_global_security_rules_deny_dangerous_path():
    """测试全局安全规则拒绝危险路径"""
    checker = GlobalSecurityRules()
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path="/etc/passwd",
        risk_level=RiskLevel.MEDIUM
    )
    result = checker.check(request)
    assert result.decision.value == "deny"
    assert "访问危险路径被禁止" in result.reason


def test_global_security_rules_allow_safe_path():
    """测试全局安全规则允许安全路径"""
    checker = GlobalSecurityRules()
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path="./test.txt",
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == "allow"
    assert "全局安全规则检查通过" in result.reason