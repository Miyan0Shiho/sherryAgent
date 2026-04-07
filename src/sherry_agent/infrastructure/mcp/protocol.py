from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MCPRequest:
    tool: str
    params: Dict[str, Any]
    id: str

    def to_json(self) -> str:
        return json.dumps({
            "tool": self.tool,
            "params": self.params,
            "id": self.id
        })

    @classmethod
    def from_json(cls, json_str: str) -> MCPRequest:
        data = json.loads(json_str)
        return cls(
            tool=data["tool"],
            params=data.get("params", {}),
            id=data["id"]
        )


@dataclass
class MCPResponse:
    success: bool
    content: str
    metadata: Dict[str, Any]
    id: str

    def to_json(self) -> str:
        return json.dumps({
            "success": self.success,
            "content": self.content,
            "metadata": self.metadata,
            "id": self.id
        })

    @classmethod
    def from_json(cls, json_str: str) -> MCPResponse:
        data = json.loads(json_str)
        return cls(
            success=data["success"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            id=data["id"]
        )


@dataclass
class MCPToolSchema:
    name: str
    description: str
    parameters: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        })

    @classmethod
    def from_json(cls, json_str: str) -> MCPToolSchema:
        data = json.loads(json_str)
        return cls(
            name=data["name"],
            description=data["description"],
            parameters=data["parameters"]
        )


class MCPprotocol:
    @staticmethod
    def create_request(tool: str, params: Dict[str, Any], request_id: str) -> MCPRequest:
        return MCPRequest(tool=tool, params=params, id=request_id)

    @staticmethod
    def create_response(success: bool, content: str, metadata: Dict[str, Any], request_id: str) -> MCPResponse:
        return MCPResponse(
            success=success,
            content=content,
            metadata=metadata,
            id=request_id
        )

    @staticmethod
    def create_tool_schema(name: str, description: str, parameters: Dict[str, Any]) -> MCPToolSchema:
        return MCPToolSchema(
            name=name,
            description=description,
            parameters=parameters
        )