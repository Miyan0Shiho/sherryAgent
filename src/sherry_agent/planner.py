from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PlannerRequest:
    source: str
    goal: str
    risk_level: str
    preferred_mode: str | None = None


@dataclass(slots=True)
class Plan:
    plan_version: str
    mode: str
    budget_profile: str
    toolset: list[str]
    steps: list[str]
    model_profile: str


class Planner:
    """A deliberately small planner for Story-01 and Story-05 flows."""

    def plan(self, request: PlannerRequest) -> Plan:
        mode = request.preferred_mode or self._select_mode(request)
        budget_profile = self._select_budget(mode, request.risk_level)
        toolset = ["repo.read"] if mode == "interactive-dev" else ["governance.scan"]
        steps = self._select_steps(mode)
        model_profile = "baseline-review" if request.risk_level in {"HIGH", "CRITICAL"} else "baseline-fast"
        return Plan(
            plan_version="v1",
            mode=mode,
            budget_profile=budget_profile,
            toolset=toolset,
            steps=steps,
            model_profile=model_profile,
        )

    def _select_mode(self, request: PlannerRequest) -> str:
        if "release" in request.goal.lower() or "governance" in request.goal.lower():
            return "background-ops"
        return "interactive-dev"

    def _select_budget(self, mode: str, risk_level: str) -> str:
        if risk_level in {"HIGH", "CRITICAL"}:
            return "premium"
        if mode == "background-ops":
            return "strict"
        return "balanced"

    def _select_steps(self, mode: str) -> list[str]:
        if mode == "background-ops":
            return ["normalize_request", "policy_precheck", "scan_repo", "produce_gate_result"]
        return ["normalize_request", "plan_work", "execute_read_only_action", "review_output"]
