from __future__ import annotations

from typing import Any, Optional

from ..execution.agent_loop import ToolExecutor as AbstractToolExecutor
from .mcp.client import MCPclient
from .security import ComprehensivePermissionChecker, PermissionRequest, RiskLevel
from .tools.base import (
    BaseTool,
    ToolDefinition,
    get_all_tools,
)
from .tools.file import ReadFileTool, WriteFileTool
from .tools.http import HttpTool
from .tools.shell import ShellTool


class ToolExecutor(AbstractToolExecutor):
    def __init__(self) -> None:
        self.permission_checker = ComprehensivePermissionChecker()
        self._tools: dict[str, BaseTool] = {}
        self._tool_definitions: dict[str, ToolDefinition] = {}
        self._mcp_clients: dict[str, MCPclient] = {}
        self._load_tools()
        self._load_registered_tools()

    def register_mcp_client(self, name: str, server_url: str) -> None:
        """注册MCP客户端"""
        self._mcp_clients[name] = MCPclient(server_url)

    def get_mcp_client(self, name: str) -> Optional[MCPclient]:
        """获取MCP客户端"""
        return self._mcp_clients.get(name)

    def _load_tools(self) -> None:
        # 加载所有工具实例
        self._tools = {
            "read_file": ReadFileTool(),
            "write_file": WriteFileTool(),
            "exec_command": ShellTool(),
            "http_request": HttpTool(),
        }

    def _load_registered_tools(self) -> None:
        # 加载通过装饰器注册的工具
        self._tool_definitions = get_all_tools()

    def register_tool(self, tool: BaseTool | ToolDefinition) -> None:
        if isinstance(tool, BaseTool):
            self._tools[tool.name] = tool
        else:
            self._tool_definitions[tool.name] = tool

    def get_available_tools(self) -> list[dict[str, Any]]:
        # 合并工具实例和装饰器注册的工具
        tool_schemas = [tool.to_schema() for tool in self._tools.values()]
        tool_schemas.extend([tool.to_schema() for tool in self._tool_definitions.values()])
        return tool_schemas

    async def execute_tool(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        call_id: str,
    ) -> tuple[str, dict[str, Any]]:
        # 检查是否为MCP远程工具调用格式: mcp://client_name/tool_name
        if tool_name.startswith("mcp://"):
            try:
                # 解析MCP工具路径
                parts = tool_name.split("/")
                if len(parts) < 3:
                    return (
                        f"Invalid MCP tool format: {tool_name}",
                        {"error": "invalid_mcp_format", "tool_name": tool_name},
                    )
                
                client_name = parts[2]
                remote_tool_name = "/".join(parts[3:])
                
                # 获取MCP客户端
                mcp_client = self.get_mcp_client(client_name)
                if not mcp_client:
                    return (
                        f"MCP client not found: {client_name}",
                        {"error": "mcp_client_not_found", "client_name": client_name},
                    )
                
                # 执行远程工具
                result = await mcp_client.execute_tool(remote_tool_name, tool_input)
                return result.content, {
                    "success": result.success,
                    "call_id": call_id,
                    **result.metadata,
                }
            except Exception as e:
                return (
                    f"Error executing MCP tool {tool_name}: {e}",
                    {"error": "mcp_execution_error", "tool_name": tool_name, "exception": str(e)},
                )
        # 先查找工具实例
        elif tool_name in self._tools:
            tool = self._tools[tool_name]

            # 构建权限请求
            permission_request = self._build_permission_request(tool_name, tool_input)

            # 检查权限
            permission_result = self.permission_checker.check(permission_request)
            if permission_result.decision.value != "allow":
                return (
                    f"Permission denied: {permission_result.reason}",
                    {"error": "permission_denied", "reason": permission_result.reason},
                )

            try:
                result = await tool.execute(**tool_input)
                return result.content, {
                    "success": result.success,
                    "call_id": call_id,
                    **result.metadata,
                }
            except Exception as e:
                return (
                    f"Error executing tool {tool_name}: {e}",
                    {"error": "execution_error", "tool_name": tool_name, "exception": str(e)},
                )
        # 再查找装饰器注册的工具
        elif tool_name in self._tool_definitions:
            tool_def = self._tool_definitions[tool_name]

            # 构建权限请求
            permission_request = self._build_permission_request(tool_name, tool_input)

            # 检查权限
            permission_result = self.permission_checker.check(permission_request)
            if permission_result.decision.value != "allow":
                return (
                    f"Permission denied: {permission_result.reason}",
                    {"error": "permission_denied", "reason": permission_result.reason},
                )

            try:
                result = await tool_def.func(**tool_input)
                return result.content, {
                    "success": result.success,
                    "call_id": call_id,
                    **result.metadata,
                }
            except Exception as e:
                return (
                    f"Error executing tool {tool_name}: {e}",
                    {"error": "execution_error", "tool_name": tool_name, "exception": str(e)},
                )
        # 工具未找到
        else:
            return (
                f"Tool not found: {tool_name}",
                {"error": "tool_not_found", "tool_name": tool_name},
            )

    def _build_permission_request(self, tool_name: str, tool_input: dict[str, Any]) -> PermissionRequest:
        """构建权限请求"""
        operation = tool_name
        target_path = None

        # 根据工具类型提取操作和路径
        if tool_name == "read_file" or tool_name == "write_file":
            target_path = tool_input.get("file_path")
        elif tool_name == "exec_command":
            operation = tool_input.get("command", "")
        elif tool_name == "http_request":
            operation = tool_input.get("method", "GET")
            target_path = tool_input.get("url")

        # 确定风险等级
        risk_level = RiskLevel.LOW
        if tool_name == "exec_command":
            risk_level = RiskLevel.MEDIUM

        return PermissionRequest(
            tool_name=tool_name,
            operation=operation,
            target_path=target_path,
            risk_level=risk_level,
            context=str(tool_input)
        )
