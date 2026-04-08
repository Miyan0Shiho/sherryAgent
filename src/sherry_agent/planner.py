from __future__ import annotations

from dataclasses import dataclass

from .models import Plan


SUPPORTED_MODES = {
    "interactive-dev",
    "autonomous-safe",
    "background-ops",
    "bulk-analysis",
}


@dataclass(slots=True)
class PlannerRequest:
    source: str
    goal: str
    risk_level: str
    preferred_mode: str | None = None


class Planner:
    """Planner for the four primary SherryAgent runtime modes."""

    def plan(self, request: PlannerRequest) -> Plan:
        mode = request.preferred_mode or self._select_mode(request)
        if mode not in SUPPORTED_MODES:
            raise ValueError(f"unsupported runtime mode: {mode}")
        return Plan(
            mode=mode,
            budget_profile=self._select_budget(mode, request.risk_level),
            toolset=self._select_toolset(mode),
            steps=self._select_steps(mode),
            model_profile=self._select_model_profile(mode, request.risk_level),
            approval_requirements=self._select_approval_requirements(mode, request.risk_level),
            max_parallelism=4 if mode == "bulk-analysis" else 1,
        )

    def _select_mode(self, request: PlannerRequest) -> str:
        goal = request.goal.lower()
        source = request.source.lower()
        if any(word in goal for word in ("release", "governance", "incident", "alert", "ops", "rollback")):
            return "background-ops"
        if any(word in goal for word in ("bulk", "audit", "research", "security", "many", "shard")):
            return "bulk-analysis"
        if source in {"cron", "event"} or any(word in goal for word in ("daily", "routine", "schedule", "periodic")):
            return "autonomous-safe"
        return "interactive-dev"

    def _select_budget(self, mode: str, risk_level: str) -> str:
        if mode in {"autonomous-safe", "background-ops"}:
            return "strict"
        if risk_level in {"HIGH", "CRITICAL"}:
            return "premium"
        if mode == "bulk-analysis":
            return "strict"
        return "balanced"

    def _select_toolset(self, mode: str) -> list[str]:
        if mode == "interactive-dev":
            return ["repo.read"]
        if mode == "autonomous-safe":
            return ["scheduler.trigger", "repo.read"]
        if mode == "background-ops":
            return ["governance.scan", "repo.read"]
        return ["repo.read", "memory.read"]

    def _select_steps(self, mode: str) -> list[str]:
        if mode == "interactive-dev":
            return ["normalize_request", "plan_work", "execute_read_only_action", "review_output"]
        if mode == "autonomous-safe":
            return ["normalize_request", "schedule_trigger", "dry_run_plan", "await_confirmation"]
        if mode == "background-ops":
            return ["normalize_request", "policy_precheck", "scan_repo", "produce_gate_result"]
        return ["normalize_request", "shard_targets", "collect_evidence", "aggregate_findings"]

    def _select_model_profile(self, mode: str, risk_level: str) -> str:
        if mode == "background-ops":
            return "baseline-ops"
        if mode == "bulk-analysis":
            return "baseline-analysis"
        if mode == "autonomous-safe":
            return "baseline-safe"
        return "baseline-review" if risk_level in {"HIGH", "CRITICAL"} else "baseline-fast"

    def _select_approval_requirements(self, mode: str, risk_level: str) -> list[str]:
        if mode == "autonomous-safe":
            return ["real-run requires human confirmation"]
        if mode == "background-ops":
            return ["all write actions require human approval"]
        if risk_level in {"HIGH", "CRITICAL"}:
            return ["high-risk execution requires review"]
        return []
