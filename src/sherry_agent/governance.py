from __future__ import annotations

from dataclasses import dataclass

from .models import CostRecord, Evidence, ResultPack, Run, Task, utc_now
from .planner import Planner, PlannerRequest
from .policy import PolicyAction, PolicyGate


@dataclass(slots=True)
class GateRequest:
    source: str
    goal: str
    repo: str
    required_checks: list[str]
    rollback_plan: str | None
    risk_level: str = "LOW"
    request_id: str = "story05-default"
    simulate_high_risk: bool = False


@dataclass(slots=True)
class GateResultPack(ResultPack):
    gate_result: str = "hold"

    def to_dict(self) -> dict[str, object]:
        payload = ResultPack.to_dict(self)
        payload["gate_result"] = self.gate_result
        return payload


def run_release_gate(request: GateRequest) -> GateResultPack:
    planner = Planner()
    plan = planner.plan(
        PlannerRequest(
            source=request.source,
            goal=request.goal,
            risk_level="HIGH" if request.simulate_high_risk else request.risk_level,
            preferred_mode="background-ops",
        )
    )
    task = Task(
        source=request.source,
        goal=request.goal,
        priority=2,
        risk_level="HIGH" if request.simulate_high_risk else request.risk_level,
        budget_profile=plan.budget_profile,
        mode=plan.mode,
        status="created",
        idempotency_key=request.request_id,
    )
    task.transition("planned")
    run = Run(
        task_id=task.task_id,
        plan_version=plan.plan_version,
        model_profile=plan.model_profile,
        toolset=plan.toolset,
        outcome="planned",
        status="running",
    )
    task.transition("running")

    evidence = [
        Evidence(
            run_id=run.run_id,
            source_type="repo",
            source_ref=request.repo,
            summary=f"Governance scan requested for repository {request.repo}.",
            confidence="high",
        ),
        Evidence(
            run_id=run.run_id,
            source_type="required_checks",
            source_ref=",".join(request.required_checks),
            summary="Required checks captured for gate evaluation.",
            confidence="high",
        ),
    ]

    policy_gate = PolicyGate()
    decision = policy_gate.evaluate(
        PolicyAction(
            run_id=run.run_id,
            name="governance.scan",
            mode=plan.mode,
            risk_level=task.risk_level,
            is_write=False,
            is_destructive=request.simulate_high_risk,
        )
    )
    decisions = [decision]

    gate_result = "pass"
    summary = "Release governance scan passed."
    output = {
        "required_checks": request.required_checks,
        "rollback_plan": request.rollback_plan,
        "evidence_links": [item.source_ref for item in evidence],
    }

    if request.rollback_plan is None:
        gate_result = "block"
        summary = "Release governance scan blocked because rollback plan is missing."
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        decisions.append(
            policy_gate.evaluate(
                PolicyAction(
                    run_id=run.run_id,
                    name="missing.rollback_plan",
                    mode=plan.mode,
                    risk_level="HIGH",
                    is_write=True,
                )
            )
        )
        output["blocked_reason"] = "missing_rollback_plan"
    elif decision.decision_type == "block":
        gate_result = "block"
        summary = "Release governance scan blocked by policy gate."
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        output["blocked_reason"] = "policy_block"
    else:
        task.transition("completed")
        run.finish(outcome="completed", status="completed")
        output["gate_result"] = "pass"

    cost_record = CostRecord(
        run_id=run.run_id,
        token_in=140,
        token_out=110,
        tool_calls=1,
        latency_ms=max(int((utc_now() - run.started_at).total_seconds() * 1000), 1),
        cache_hit=False,
        estimated_cost=0.003,
    )
    return GateResultPack(
        task=task,
        run=run,
        evidence=evidence,
        decisions=decisions,
        cost_record=cost_record,
        result_summary=summary,
        output=output,
        gate_result=gate_result,
    )
