import asyncio
import subprocess
from typing import Any

from .base import BaseTool, Permission, ToolResult


class ShellTool(BaseTool):
    @property
    def name(self) -> str:
        return "exec_command"

    @property
    def description(self) -> str:
        return "执行 shell 命令"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "command": {
                "type": "string",
                "description": "要执行的 shell 命令",
            },
            "timeout": {
                "type": "integer",
                "description": "命令执行超时时间（秒）",
                "default": 60,
            }
        }

    @property
    def permissions(self) -> list[Permission]:
        return [Permission.EXECUTE]

    async def execute(self, **kwargs: Any) -> ToolResult:
        try:
            # 获取参数
            command = kwargs.get("command", "")
            timeout = kwargs.get("timeout", 60)

            # 执行命令
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # 等待命令执行完成
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )

            # 解码输出
            stdout_str = stdout.decode('utf-8') if stdout else ''
            stderr_str = stderr.decode('utf-8') if stderr else ''

            # 构建结果
            success = process.returncode == 0
            content = stdout_str if success else stderr_str

            metadata: dict[str, Any] = {
                "returncode": process.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "command": command,
                "timeout": timeout,
            }

            return ToolResult(
                success=success,
                content=content,
                metadata=metadata,
            )
        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                content=f"Command timed out after {timeout} seconds",
                metadata={"command": command, "timeout": timeout},
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=f"Error executing command: {e}",
                metadata={"command": command, "timeout": timeout},
            )
