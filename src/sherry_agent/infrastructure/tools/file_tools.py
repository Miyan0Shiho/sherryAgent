from pathlib import Path

from .base import Permission, ToolResult, tool


class SandboxError(Exception):
    pass


def _resolve_path(path: str | Path, sandbox_root: Path) -> Path:
    sandbox_root = sandbox_root.resolve()
    target_path = (sandbox_root / path).resolve()

    if not target_path.is_relative_to(sandbox_root):
        raise SandboxError(f"Path '{path}' is outside the sandbox root '{sandbox_root}'")

    return target_path


def _get_sandbox_root() -> Path:
    return Path.cwd()


@tool(
    name="read_file",
    description="读取文件内容",
    parameters={
        "path": {
            "type": "string",
            "description": "文件相对路径，从项目根目录开始",
        }
    },
    permissions=[Permission.READ],
)
async def read_file(path: str) -> ToolResult:
    try:
        sandbox_root = _get_sandbox_root()
        target_path = _resolve_path(path, sandbox_root)

        if not target_path.exists():
            return ToolResult(
                success=False,
                content=f"File not found: {path}",
            )

        if not target_path.is_file():
            return ToolResult(
                success=False,
                content=f"Path is not a file: {path}",
            )

        content = await _read_file_async(target_path)
        return ToolResult(
            success=True,
            content=content,
            metadata={"path": str(target_path), "size": len(content)},
        )
    except SandboxError as e:
        return ToolResult(success=False, content=f"Security error: {e}")
    except Exception as e:
        return ToolResult(success=False, content=f"Error reading file: {e}")


async def _read_file_async(path: Path) -> str:
    import asyncio
    return await asyncio.to_thread(path.read_text)


@tool(
    name="write_file",
    description="写入文件内容",
    parameters={
        "path": {
            "type": "string",
            "description": "文件相对路径，从项目根目录开始",
        },
        "content": {
            "type": "string",
            "description": "要写入的文件内容",
        },
    },
    permissions=[Permission.WRITE],
)
async def write_file(path: str, content: str) -> ToolResult:
    try:
        sandbox_root = _get_sandbox_root()
        target_path = _resolve_path(path, sandbox_root)

        target_path.parent.mkdir(parents=True, exist_ok=True)

        await _write_file_async(target_path, content)

        return ToolResult(
            success=True,
            content=f"Successfully wrote {len(content)} characters to {path}",
            metadata={"path": str(target_path), "size": len(content)},
        )
    except SandboxError as e:
        return ToolResult(success=False, content=f"Security error: {e}")
    except Exception as e:
        return ToolResult(success=False, content=f"Error writing file: {e}")


async def _write_file_async(path: Path, content: str) -> None:
    import asyncio
    await asyncio.to_thread(path.write_text, content)
