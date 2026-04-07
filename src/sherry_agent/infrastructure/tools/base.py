from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class Permission(Enum):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    NETWORK = auto()


@dataclass
class ToolResult:
    success: bool
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_message(self) -> dict[str, Any]:
        return {
            "role": "tool_result",
            "content": self.content,
            "success": self.success,
            **self.metadata,
        }


class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        pass

    @property
    @abstractmethod
    def permissions(self) -> list[Permission]:
        pass

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        pass

    def to_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": list(self.parameters.keys()),
                },
            },
        }


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    permissions: list[Permission]
    func: Callable[..., Coroutine[Any, Any, ToolResult]]

    def to_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": list(self.parameters.keys()),
                },
            },
        }


_TOOL_REGISTRY: dict[str, ToolDefinition] = {}


def tool(
    name: str,
    description: str,
    parameters: dict[str, Any],
    permissions: list[Permission] | None = None,
) -> Callable[[Callable[P, Coroutine[Any, Any, ToolResult]]], Callable[P, Coroutine[Any, Any, ToolResult]]]:
    def decorator(func: Callable[P, Coroutine[Any, Any, ToolResult]]) -> Callable[P, Coroutine[Any, Any, ToolResult]]:
        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            permissions=permissions or [],
            func=func,
        )
        _TOOL_REGISTRY[name] = tool_def
        return func

    return decorator


def get_tool(name: str) -> ToolDefinition | None:
    return _TOOL_REGISTRY.get(name)


def get_all_tools() -> dict[str, ToolDefinition]:
    return _TOOL_REGISTRY.copy()


def clear_tools() -> None:
    _TOOL_REGISTRY.clear()
