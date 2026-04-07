from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(Enum):
    TEXT = "text"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    THINKING = "thinking"
    MEMORY_TRANSFER = "memory_transfer"


@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0


@dataclass
class ToolCall:
    tool_name: str
    tool_input: dict[str, Any]
    call_id: str


@dataclass
class AgentEvent:
    event_type: EventType
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    token_usage: TokenUsage | None = None


class CancellationToken:
    def __init__(self) -> None:
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled
