from __future__ import annotations

from dataclasses import dataclass

from .models import CostRecord, Evidence, ResultPack, Run, Task, utc_now
from .planner import Planner, PlannerRequest
from .policy import PolicyAction, PolicyGate


@dataclass(slots=True)
class InteractiveDevRequest:
    source: str
    goal: str
    risk_level: str = "LOW"
    priority: int = 3
    simulate_budget_exhausted: bool = False
    request_id: str = "story01-default"


def run_interactive_dev(request: InteractiveDevRequest) -> ResultPack:
    planner = Planner()
    plan = planner.plan(
        PlannerRequest(
            source=request.source,
            goal=request.goal,
            risk_level=request.risk_level,
            preferred_mode="interactive-dev",
        )
    )
    task = Task(
        source=request.source,
        goal=request.goal,
        priority=request.priority,
        risk_level=request.risk_level,
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
            source_type="request",
            source_ref=request.request_id,
            summary=f"Interactive dev request received: {request.goal}",
            confidence="high",
        )
    ]

    policy_gate = PolicyGate()
    policy_decision = policy_gate.evaluate(
        PolicyAction(
            run_id=run.run_id,
            name="repo.read",
            mode=plan.mode,
            risk_level=request.risk_level,
            is_write=False,
        )
    )
    decisions = [policy_decision]

    if request.simulate_budget_exhausted:
        progress_report = {
            "progress": "Planner and policy evaluation completed before budget exhausted.",
            "blocked_reason": "budget_exhausted",
        }
        evidence.append(
            Evidence(
                run_id=run.run_id,
                source_type="progress_report",
                source_ref="budget_exhausted",
                summary="Budget exhausted before execution completed.",
                confidence="high",
            )
        )
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        cost_record = CostRecord(
            run_id=run.run_id,
            token_in=120,
            token_out=80,
            tool_calls=0,
            latency_ms=15,
            cache_hit=False,
            estimated_cost=0.002,
        )
        return ResultPack(
            task=task,
            run=run,
            evidence=evidence,
            decisions=decisions,
            cost_record=cost_record,
            result_summary="Interactive dev loop blocked due to budget exhaustion.",
            output=progress_report,
        )

    evidence.append(
        Evidence(
            run_id=run.run_id,
            source_type="tool_result",
            source_ref="repo.read:design-snapshot",
            summary="Read-only development context collected for the requested task.",
            confidence="high",
        )
    )
    task.transition("completed")
    run.finish(outcome="completed", status="completed")
    cost_record = CostRecord(
        run_id=run.run_id,
        token_in=220,
        token_out=140,
        tool_calls=1,
        latency_ms=max(int((utc_now() - run.started_at).total_seconds() * 1000), 1),
        cache_hit=False,
        estimated_cost=0.004,
    )
    return ResultPack(
        task=task,
        run=run,
        evidence=evidence,
        decisions=decisions,
        cost_record=cost_record,
        result_summary="Interactive dev loop completed a minimal read-only execution.",
        output={
            "plan_steps": plan.steps,
            "result": "Minimal interactive dev execution completed.",
            "blocked_reason": None,
        },
    )
