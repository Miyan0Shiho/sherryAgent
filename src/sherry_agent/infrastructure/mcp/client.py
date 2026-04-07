from __future__ import annotations

import asyncio
import uuid
from typing import Any, Dict, List, Optional

import aiohttp

from ..tools.base import ToolResult
from .protocol import MCPprotocol, MCPRequest, MCPResponse


class MCPclient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def disconnect(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        await self.connect()
        
        request_id = str(uuid.uuid4())
        
        try:
            async with self.session.post(
                f"{self.server_url}/api/v1/execute",
                json={
                    "tool": tool_name,
                    "params": params,
                    "id": request_id
                }
            ) as response:
                if response.status != 200:
                    return ToolResult(
                        success=False,
                        content=f"HTTP Error: {response.status}",
                        metadata={"status": response.status}
                    )
                
                data = await response.json()
                
                return ToolResult(
                    success=data["success"],
                    content=data["content"],
                    metadata=data.get("metadata", {})
                )
        except Exception as e:
            return ToolResult(
                success=False,
                content=f"Error executing tool: {str(e)}",
                metadata={"error": str(e)}
            )

    async def list_tools(self) -> List[Dict[str, Any]]:
        await self.connect()
        
        try:
            async with self.session.get(f"{self.server_url}/api/v1/tools") as response:
                if response.status != 200:
                    return []
                return await response.json()
        except Exception:
            return []

    async def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        await self.connect()
        
        try:
            async with self.session.get(f"{self.server_url}/api/v1/tools/{tool_name}") as response:
                if response.status != 200:
                    return None
                return await response.json()
        except Exception:
            return None

    async def __aenter__(self) -> MCPclient:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()