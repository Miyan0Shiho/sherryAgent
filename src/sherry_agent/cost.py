from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from .models import CostRecord


@dataclass(slots=True)
class BudgetProfile:
    name: str
    max_token_units: int
    max_tool_calls: int
    max_latency_ms: int
    degrade_to: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BudgetDecision:
    profile_name: str
    status: str
    reason: str
    token_units_used: int
    tool_calls_used: int
    latency_ms_used: int
    next_profile: str | None = None
    profile_snapshot: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_budget_profiles() -> dict[str, BudgetProfile]:
    return {
        "strict": BudgetProfile("strict", max_token_units=256, max_tool_calls=1, max_latency_ms=200),
        "balanced": BudgetProfile("balanced", max_token_units=700, max_tool_calls=3, max_latency_ms=500, degrade_to="strict"),
        "premium": BudgetProfile("premium", max_token_units=1400, max_tool_calls=6, max_latency_ms=1200, degrade_to="balanced"),
    }


class CostController:
    def __init__(self, *, profiles: Mapping[str, BudgetProfile] | None = None, initial_profile: str = "balanced") -> None:
        self.profiles = dict(profiles or default_budget_profiles())
        self.current_profile = initial_profile
        self.token_units_used = 0
        self.tool_calls_used = 0
        self.latency_ms_used = 0

    def snapshot(self) -> dict[str, Any]:
        return {
            "profile": self.profiles[self.current_profile].to_dict(),
            "token_units_used": self.token_units_used,
            "tool_calls_used": self.tool_calls_used,
            "latency_ms_used": self.latency_ms_used,
        }

    def evaluate(self, record: CostRecord) -> BudgetDecision:
        profile = self.profiles[self.current_profile]
        token_units = self.token_units_used + record.token_in + record.token_out
        tool_calls = self.tool_calls_used + record.tool_calls
        latency_ms = self.latency_ms_used + record.latency_ms
        return self._decide(profile, token_units, tool_calls, latency_ms)

    def record(self, record: CostRecord) -> BudgetDecision:
        decision = self.evaluate(record)
        self.token_units_used += record.token_in + record.token_out
        self.tool_calls_used += record.tool_calls
        self.latency_ms_used += record.latency_ms
        if decision.status == "degrade" and decision.next_profile is not None:
            self.current_profile = decision.next_profile
        return decision

    def _decide(self, profile: BudgetProfile, token_units: int, tool_calls: int, latency_ms: int) -> BudgetDecision:
        reasons = []
        if token_units > profile.max_token_units:
            reasons.append("token_budget_exceeded")
        if tool_calls > profile.max_tool_calls:
            reasons.append("tool_call_budget_exceeded")
        if latency_ms > profile.max_latency_ms:
            reasons.append("latency_budget_exceeded")
        if not reasons:
            return BudgetDecision(profile.name, "continue", "within_budget", token_units, tool_calls, latency_ms, profile_snapshot=profile.to_dict())
        status = "degrade" if profile.degrade_to else "block"
        return BudgetDecision(
            profile.name,
            status,
            ",".join(reasons),
            token_units,
            tool_calls,
            latency_ms,
            next_profile=profile.degrade_to,
            profile_snapshot=profile.to_dict(),
        )
