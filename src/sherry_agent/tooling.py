from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .models import ToolCall
from .policy import PolicyAction, PolicyGate


def _risk_rank(level: str) -> int:
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
    return order.get(level, 0)


@dataclass(slots=True)
class ToolMetadata:
    name: str
    capability: str
    risk_level: str
    is_write: bool = False
    sandbox_required: bool = True
    timeout_seconds: int = 30
    retryable: bool = False
    audit_required: bool = True
    requires_confirmation: bool = False
    description: str = ""

    def __post_init__(self) -> None:
        if self.is_write or self.risk_level in {"HIGH", "CRITICAL"}:
            self.requires_confirmation = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ToolRegistry:
    def __init__(self, tools: Iterable[ToolMetadata] | None = None) -> None:
        self._tools: dict[str, ToolMetadata] = {}
        for tool in tools or default_toolset():
            self.register(tool)

    def register(self, tool: ToolMetadata) -> None:
        self._tools[tool.name] = tool

    def require(self, name: str) -> ToolMetadata:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]

    def list(self) -> list[ToolMetadata]:
        return list(self._tools.values())

    def evaluate_call(self, call: ToolCall):
        metadata = self.require(call.tool_name)
        effective_risk = max(call.risk_level, metadata.risk_level, key=_risk_rank)
        gate = PolicyGate()
        return gate.evaluate(
            action=PolicyAction(
                run_id=call.run_id,
                name=call.tool_name,
                mode=call.mode,
                risk_level=effective_risk,
                target=call.target,
                tool_name=call.tool_name,
                is_write=call.is_write or metadata.is_write,
                is_destructive=call.is_destructive,
                approved_by=call.approved_by,
                requires_confirmation=metadata.requires_confirmation,
            )
        )

    def build_call(
        self,
        *,
        run_id: str,
        tool_name: str,
        target: str,
        mode: str,
        risk_level: str,
        arguments: dict[str, Any] | None = None,
        outcome: str = "completed",
    ) -> ToolCall:
        metadata = self.require(tool_name)
        return ToolCall(
            run_id=run_id,
            tool_name=tool_name,
            target=target,
            mode=mode,
            risk_level=max(risk_level, metadata.risk_level, key=_risk_rank),
            arguments=arguments or {},
            is_write=metadata.is_write,
            outcome=outcome,
            metadata=metadata.to_dict(),
        )


def default_toolset() -> list[ToolMetadata]:
    return [
        ToolMetadata("repo.read", "read repository context", "LOW", is_write=False, retryable=True),
        ToolMetadata("governance.scan", "scan repo governance", "LOW", is_write=False, retryable=True),
        ToolMetadata("memory.read", "retrieve memory", "LOW", is_write=False, sandbox_required=False),
        ToolMetadata("memory.write", "write memory", "MEDIUM", is_write=True, sandbox_required=False),
        ToolMetadata("scheduler.trigger", "create or inspect triggers", "MEDIUM", is_write=False, sandbox_required=False),
        ToolMetadata("repo.write", "write repository", "HIGH", is_write=True),
    ]
