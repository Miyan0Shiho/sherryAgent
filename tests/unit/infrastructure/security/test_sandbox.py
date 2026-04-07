import os
import pytest

from src.sherry_agent.infrastructure.security import SandboxIsolation, PermissionRequest, RiskLevel


def test_sandbox_isolation_allow_allowed_path():
    """测试沙箱隔离允许在允许路径内的操作"""
    current_dir = os.getcwd()
    checker = SandboxIsolation(allowed_paths=[current_dir])
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path=os.path.join(current_dir, "test.txt"),
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == "allow"
    assert "路径在允许范围内" in result.reason


def test_sandbox_isolation_deny_external_path():
    """测试沙箱隔离拒绝超出范围的路径"""
    current_dir = os.getcwd()
    checker = SandboxIsolation(allowed_paths=[current_dir])
    request = PermissionRequest(
        tool_name="read_file",
        operation="read_file",
        target_path="/etc/passwd",
        risk_level=RiskLevel.MEDIUM
    )
    result = checker.check(request)
    assert result.decision.value == "deny"
    assert "路径超出沙箱范围" in result.reason


def test_sandbox_isolation_allow_no_path():
    """测试沙箱隔离允许无目标路径的操作"""
    checker = SandboxIsolation()
    request = PermissionRequest(
        tool_name="exec_command",
        operation="ls -la",
        risk_level=RiskLevel.LOW
    )
    result = checker.check(request)
    assert result.decision.value == "allow"
    assert "无目标路径" in result.reason