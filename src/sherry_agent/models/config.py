from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentConfig:
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8192
    token_budget: int = 200_000
    max_tool_rounds: int = 20
    system_prompt: str = ""
    tools: list[dict[str, Any]] = field(default_factory=list)
