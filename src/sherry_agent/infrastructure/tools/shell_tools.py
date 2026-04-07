import asyncio
import shlex
from collections.abc import Sequence

from .base import Permission, ToolResult, tool

DEFAULT_TIMEOUT = 30.0


@tool(
    name="exec_shell",
    description="执行 Shell 命令",
    parameters={
        "command": {
            "type": "string",
            "description": "要执行的 Shell 命令",
        },
        "timeout": {
            "type": "number",
            "description": f"超时时间（秒），默认 {DEFAULT_TIMEOUT} 秒",
        },
    },
    permissions=[Permission.EXECUTE],
)
async def exec_shell(command: str, timeout: float = DEFAULT_TIMEOUT) -> ToolResult:
    try:
        args = shlex.split(command)
        result = await _run_command_async(args, timeout)

        return ToolResult(
            success=result.returncode == 0,
            content=result.stdout + result.stderr,
            metadata={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command,
            },
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
            metadata={"command": command},
        )


class _CommandResult:
    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


async def _run_command_async(args: Sequence[str], timeout: float) -> _CommandResult:
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout,
        )
    except TimeoutError:
        process.kill()
        await process.wait()
        raise

    stdout = stdout_bytes.decode("utf-8", errors="replace")
    stderr = stderr_bytes.decode("utf-8", errors="replace")

    return _CommandResult(
        returncode=process.returncode or 0,
        stdout=stdout,
        stderr=stderr,
    )
