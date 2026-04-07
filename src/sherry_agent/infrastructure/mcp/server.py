from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from ..tools.base import BaseTool, ToolDefinition, get_all_tools
from .protocol import MCPToolSchema


class MCPserver:
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.registered_tools: Dict[str, ToolDefinition] = {}
        self.server_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn

        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.post("/api/v1/execute")
        async def execute_tool(tool: str, params: Dict[str, Any], id: str):
            if tool not in self.registered_tools:
                raise HTTPException(status_code=404, detail=f"Tool {tool} not found")
            
            tool_def = self.registered_tools[tool]
            result = await tool_def.func(**params)
            
            return {
                "success": result.success,
                "content": result.content,
                "metadata": result.metadata,
                "id": id
            }

        @app.get("/api/v1/tools")
        async def list_tools():
            return [tool.to_schema() for tool in self.registered_tools.values()]

        @app.get("/api/v1/tools/{tool_name}")
        async def get_tool(tool_name: str):
            if tool_name not in self.registered_tools:
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            return self.registered_tools[tool_name].to_schema()

        async def run_server():
            config = uvicorn.Config(app, host=self.host, port=self.port)
            server = uvicorn.Server(config)
            await server.serve()

        self.server_task = asyncio.create_task(run_server())

    async def stop(self) -> None:
        if self.server_task:
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass
            self.server_task = None

    def register_tool(self, tool: BaseTool | ToolDefinition) -> None:
        if isinstance(tool, BaseTool):
            tool_def = ToolDefinition(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters,
                permissions=tool.permissions,
                func=tool.execute
            )
            self.registered_tools[tool.name] = tool_def
        elif isinstance(tool, ToolDefinition):
            self.registered_tools[tool.name] = tool

    def register_all_tools(self) -> None:
        all_tools = get_all_tools()
        for tool_name, tool_def in all_tools.items():
            self.registered_tools[tool_name] = tool_def

    def unregister_tool(self, tool_name: str) -> None:
        if tool_name in self.registered_tools:
            del self.registered_tools[tool_name]

    def get_registered_tools(self) -> List[str]:
        return list(self.registered_tools.keys())

    async def __aenter__(self) -> MCPserver:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()