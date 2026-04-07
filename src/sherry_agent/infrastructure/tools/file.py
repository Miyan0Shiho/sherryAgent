import asyncio
from pathlib import Path
from typing import Any

from .base import BaseTool, Permission, ToolResult


class SandboxError(Exception):
    pass


class ReadFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "读取文件内容"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "文件路径，比如 'README.md' 或 'src/file.py'",
            }
        }

    @property
    def permissions(self) -> list[Permission]:
        return [Permission.READ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        try:
            path = kwargs.get("file_path", "")
            sandbox_root = self._get_sandbox_root()
            target_path = self._resolve_path(path, sandbox_root)

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

            content = await self._read_file_async(target_path)
            return ToolResult(
                success=True,
                content=content,
                metadata={"path": str(target_path), "size": len(content)},
            )
        except SandboxError as e:
            return ToolResult(success=False, content=f"Security error: {e}")
        except Exception as e:
            return ToolResult(success=False, content=f"Error reading file: {e}")

    def _get_sandbox_root(self) -> Path:
        return Path.cwd()

    def _resolve_path(self, path: str, sandbox_root: Path) -> Path:
        sandbox_root = sandbox_root.resolve()
        target_path = (sandbox_root / path).resolve()

        if not target_path.is_relative_to(sandbox_root):
            raise SandboxError(f"Path '{path}' is outside the sandbox root '{sandbox_root}'")

        return target_path

    async def _read_file_async(self, path: Path) -> str:
        return await asyncio.to_thread(path.read_text)


class WriteFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "写入文件内容"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "文件路径，比如 'README.md' 或 'src/file.py'",
            },
            "content": {
                "type": "string",
                "description": "要写入的文件内容",
            }
        }

    @property
    def permissions(self) -> list[Permission]:
        return [Permission.WRITE]

    async def execute(self, **kwargs: Any) -> ToolResult:
        try:
            path = kwargs.get("file_path", "")
            content = kwargs.get("content", "")
            sandbox_root = self._get_sandbox_root()
            target_path = self._resolve_path(path, sandbox_root)

            # 确保目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)

            await self._write_file_async(target_path, content)
            return ToolResult(
                success=True,
                content=f"File written successfully: {path}",
                metadata={"path": str(target_path), "size": len(content)},
            )
        except SandboxError as e:
            return ToolResult(success=False, content=f"Security error: {e}")
        except Exception as e:
            return ToolResult(success=False, content=f"Error writing file: {e}")

    def _get_sandbox_root(self) -> Path:
        return Path.cwd()

    def _resolve_path(self, path: str, sandbox_root: Path) -> Path:
        sandbox_root = sandbox_root.resolve()
        target_path = (sandbox_root / path).resolve()

        if not target_path.is_relative_to(sandbox_root):
            raise SandboxError(f"Path '{path}' is outside the sandbox root '{sandbox_root}'")

        return target_path

    async def _write_file_async(self, path: Path, content: str) -> None:
        await asyncio.to_thread(path.write_text, content)
