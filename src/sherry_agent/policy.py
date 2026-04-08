from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .models import Decision


@dataclass(slots=True)
class PolicyAction:
    run_id: str
    name: str
    mode: str
    risk_level: str
    target: str | None = None
    tool_name: str | None = None
    is_write: bool = False
    is_destructive: bool = False
    approved_by: str | None = None
    requires_confirmation: bool = False
    context: dict[str, Any] = field(default_factory=dict)


class PolicyGate:
    """Policy gate with explicit block and confirmation semantics."""

    def evaluate(self, action: PolicyAction) -> Decision:
        if action.is_destructive or action.risk_level == "CRITICAL":
            return Decision(
                run_id=action.run_id,
                decision_type="block",
                policy_basis="destructive_or_critical_action",
                requires_human=True,
                approved_by=action.approved_by,
                reason="Destructive or critical actions are blocked by default.",
                target=action.target or action.name,
            )

        if action.mode in {"background-ops", "autonomous-safe"} and action.is_write:
            return Decision(
                run_id=action.run_id,
                decision_type="block",
                policy_basis="background_write_blocked",
                requires_human=True,
                approved_by=action.approved_by,
                reason="Background write actions are blocked until a human takes over.",
                target=action.target or action.name,
            )

        if action.is_write or action.risk_level == "HIGH" or action.requires_confirmation:
            return Decision(
                run_id=action.run_id,
                decision_type="require_confirmation",
                policy_basis="write_or_high_risk_requires_confirmation",
                requires_human=True,
                approved_by=action.approved_by,
                reason="Write or high-risk actions require human confirmation.",
                target=action.target or action.name,
            )

        return Decision(
            run_id=action.run_id,
            decision_type="allow",
            policy_basis="read_only_low_risk",
            requires_human=False,
            approved_by=action.approved_by or "policy-gate",
            reason="Read-only low-risk action is allowed.",
            target=action.target or action.name,
        )
