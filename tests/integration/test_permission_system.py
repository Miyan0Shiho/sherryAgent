
"""
权限系统集成测试

测试权限系统的实际行为，包括：
- 危险命令拦截
- 安全命令执行
- 沙箱路径隔离
- 文件读写权限控制
"""

import os
import pytest
import tempfile
from pathlib import Path

from sherry_agent.infrastructure.tool_executor import ToolExecutor


@pytest.mark.integration
@pytest.mark.security
class TestPermissionSystemIntegration:
    """权限系统集成测试"""

    @pytest.fixture
    def tool_executor(self):
        """创建工具执行器实例"""
        return ToolExecutor()

    @pytest.fixture
    def temp_sandbox_dir(self):
        """创建临时沙箱目录"""
        project_dir = Path(__file__).parent.parent.parent
        temp_dir = project_dir / "test_temp"
        temp_dir.mkdir(exist_ok=True)
        yield temp_dir
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    @pytest.fixture
    def test_file(self, temp_sandbox_dir):
        """创建测试文件"""
        test_file_path = temp_sandbox_dir / "test.txt"
        test_file_path.write_text("Hello, World!")
        return test_file_path

    @pytest.mark.asyncio
    async def test_dangerous_command_denied(self, tool_executor):
        """测试危险命令被拦截"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "rm -rf /"},
            call_id="test_dangerous_cmd"
        )
        
        assert "Permission denied" in result
        assert metadata.get("error") == "permission_denied"
        assert "危险命令被禁止" in metadata.get("reason", "")

    @pytest.mark.asyncio
    async def test_safe_command_allowed(self, tool_executor):
        """测试安全命令能正常执行"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="exec_command",
            tool_input={"command": "echo 'safe command'"},
            call_id="test_safe_cmd"
        )
        
        assert metadata.get("success") is True or "error" not in metadata
        assert "Permission denied" not in result

    @pytest.mark.asyncio
    async def test_read_file_in_sandbox_allowed(self, tool_executor, test_file):
        """测试在沙箱路径内读取文件被允许"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="read_file",
            tool_input={"file_path": str(test_file)},
            call_id="test_read_in_sandbox"
        )
        
        assert "Permission denied" not in result
        assert "Hello, World!" in result or metadata.get("success") is True or "error" not in metadata

    @pytest.mark.asyncio
    async def test_read_file_outside_sandbox_denied(self, tool_executor):
        """测试读取沙箱外文件被拒绝"""
        result, metadata = await tool_executor.execute_tool(
            tool_name="read_file",
            tool_input={"file_path": "/etc/passwd"},
            call_id="test_read_outside_sandbox"
        )
        
        assert "Permission denied" in result
        assert metadata.get("error") == "permission_denied"
        assert "访问危险路径被禁止" in metadata.get("reason", "")

    @pytest.mark.asyncio
    async def test_write_file_in_sandbox_allowed(self, tool_executor, temp_sandbox_dir):
        """测试在沙箱路径内写入文件被允许"""
        test_write_path = temp_sandbox_dir / "write_test.txt"
        
        result, metadata = await tool_executor.execute_tool(
            tool_name="write_file",
            tool_input={"file_path": str(test_write_path), "content": "Test write"},
            call_id="test_write_in_sandbox"
        )
        
        assert "Permission denied" not in result
        assert test_write_path.exists() or metadata.get("success") is True or "error" not in metadata

    @pytest.mark.asyncio
    async def test_multiple_dangerous_commands_denied(self, tool_executor):
        """测试多种危险命令都被拦截"""
        dangerous_commands = [
            "rm -rf /*",
            "rm -rf ~",
            "rm -rf ~/*",
            "DROP TABLE users",
            "DELETE FROM orders",
            "TRUNCATE TABLE logs",
            ":(){ :|:& };:",
            "mkfs.ext4 /dev/sda",
            "dd if=/dev/zero of=/dev/sda"
        ]
        
        for cmd in dangerous_commands:
            result, metadata = await tool_executor.execute_tool(
                tool_name="exec_command",
                tool_input={"command": cmd},
                call_id=f"test_dangerous_{hash(cmd)}"
            )
            
            assert "Permission denied" in result
            assert metadata.get("error") == "permission_denied"

    @pytest.mark.asyncio
    async def test_sandbox_path_isolation(self, temp_sandbox_dir):
        """测试沙箱路径隔离功能"""
        from sherry_agent.infrastructure.security import SandboxIsolation, PermissionRequest, RiskLevel
        
        sandbox = SandboxIsolation(allowed_paths=[str(temp_sandbox_dir)])
        
        allowed_path = str(temp_sandbox_dir / "allowed.txt")
        allowed_request = PermissionRequest(
            tool_name="read_file",
            operation="read_file",
            target_path=allowed_path,
            risk_level=RiskLevel.LOW
        )
        allowed_result = sandbox.check(allowed_request)
        assert allowed_result.decision.value == "allow"
        
        denied_path = "/etc/denied.txt"
        denied_request = PermissionRequest(
            tool_name="read_file",
            operation="read_file",
            target_path=denied_path,
            risk_level=RiskLevel.LOW
        )
        denied_result = sandbox.check(denied_request)
        assert denied_result.decision.value == "deny"

    @pytest.mark.asyncio
    async def test_file_permission_denied_on_dangerous_path(self, tool_executor):
        """测试危险路径的文件操作被拒绝"""
        dangerous_paths = [
            "/etc/passwd",
            "/etc/shadow",
            os.path.expanduser("~/.ssh/id_rsa"),
            os.path.expanduser("~/.aws/credentials"),
            os.path.expanduser("~/.gnupg/secring.gpg")
        ]
        
        for path in dangerous_paths:
            result, metadata = await tool_executor.execute_tool(
                tool_name="read_file",
                tool_input={"file_path": path},
                call_id=f"test_dangerous_path_{hash(path)}"
            )
            
            assert "Permission denied" in result
            assert metadata.get("error") == "permission_denied"
