from __future__ import annotations

from dataclasses import dataclass

from .cost import CostController
from .memory import MemoryStore
from .models import CostRecord, Evidence, MemoryRecord, Plan, ResultPack, Run, Task, ToolCall, TriggerEvent, utc_now
from .planner import Planner, PlannerRequest
from .tooling import ToolRegistry


@dataclass(slots=True)
class InteractiveDevRequest:
    source: str
    goal: str
    risk_level: str = "LOW"
    priority: int = 3
    simulate_budget_exhausted: bool = False
    request_id: str = "story01-default"


def build_result_pack(
    *,
    task: Task,
    run: Run,
    plan: Plan,
    evidence: list[Evidence],
    decisions: list,
    cost_record: CostRecord,
    tool_calls: list[ToolCall] | None = None,
    memory_records: list[MemoryRecord] | None = None,
    trigger_events: list[TriggerEvent] | None = None,
    result_summary: str,
    output: dict[str, object],
    release_gate=None,
) -> ResultPack:
    return ResultPack(
        task=task,
        run=run,
        plan=plan,
        evidence=evidence,
        decisions=decisions,
        cost_record=cost_record,
        tool_calls=tool_calls or [],
        memory_records=memory_records or [],
        trigger_events=trigger_events or [],
        result_summary=result_summary,
        output=output,
        release_gate=release_gate,
    )


def start_task_run(*, source: str, goal: str, priority: int, risk_level: str, request_id: str, plan: Plan) -> tuple[Task, Run]:
    task = Task(
        source=source,
        goal=goal,
        priority=priority,
        risk_level=risk_level,
        budget_profile=plan.budget_profile,
        mode=plan.mode,
        status="created",
        idempotency_key=request_id,
    )
    task.transition("planned")
    run = Run(
        task_id=task.task_id,
        plan_version=plan.plan_version,
        model_profile=plan.model_profile,
        toolset=plan.toolset,
        outcome="planned",
        status="running",
        mode=plan.mode,
    )
    task.transition("running")
    return task, run


def finalize_cost_record(run: Run, *, token_in: int, token_out: int, tool_calls: int, estimated_cost: float, degraded_mode: str | None = None) -> CostRecord:
    return CostRecord(
        run_id=run.run_id,
        token_in=token_in,
        token_out=token_out,
        tool_calls=tool_calls,
        latency_ms=max(int((utc_now() - run.started_at).total_seconds() * 1000), 1),
        cache_hit=False,
        estimated_cost=estimated_cost,
        degraded_mode=degraded_mode,
    )


def run_interactive_dev(request: InteractiveDevRequest) -> ResultPack:
    planner = Planner()
    plan = planner.plan(PlannerRequest(source=request.source, goal=request.goal, risk_level=request.risk_level, preferred_mode="interactive-dev"))
    task, run = start_task_run(
        source=request.source,
        goal=request.goal,
        priority=request.priority,
        risk_level=request.risk_level,
        request_id=request.request_id,
        plan=plan,
    )

    registry = ToolRegistry()
    tool_call = registry.build_call(run_id=run.run_id, tool_name="repo.read", target="workspace", mode=plan.mode, risk_level=request.risk_level)
    decision = registry.evaluate_call(tool_call)
    evidence = [
        Evidence(run_id=run.run_id, source_type="request", source_ref=request.request_id, summary=f"Interactive dev request received: {request.goal}", confidence="high"),
    ]
    memory_records: list[MemoryRecord] = []

    if request.simulate_budget_exhausted:
        evidence.append(Evidence(run_id=run.run_id, source_type="progress_report", source_ref="budget_exhausted", summary="Budget exhausted before execution completed.", confidence="high"))
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        cost_record = finalize_cost_record(run, token_in=120, token_out=80, tool_calls=0, estimated_cost=0.002, degraded_mode="blocked")
        return build_result_pack(
            task=task,
            run=run,
            plan=plan,
            evidence=evidence,
            decisions=[decision],
            cost_record=cost_record,
            tool_calls=[],
            memory_records=[],
            result_summary="Interactive dev loop blocked due to budget exhaustion.",
            output={"progress": "Planner and policy evaluation completed before budget exhausted.", "blocked_reason": "budget_exhausted"},
        )

    evidence.append(Evidence(run_id=run.run_id, source_type="tool_result", source_ref="repo.read:workspace", summary="Read-only development context collected for the requested task.", confidence="high"))
    with MemoryStore() as store:
        memory_records.append(
            store.put(
                MemoryRecord(
                    task_id=task.task_id,
                    run_id=run.run_id,
                    scope="story01",
                    kind="session",
                    key="interactive-dev-summary",
                    value=f"Prepared development context for goal: {request.goal}",
                    ttl_seconds=3600,
                )
            )
        )
    task.transition("completed")
    run.finish(outcome="completed", status="completed")
    cost_record = finalize_cost_record(run, token_in=220, token_out=140, tool_calls=1, estimated_cost=0.004)
    budget_decision = CostController(initial_profile=plan.budget_profile).record(cost_record)
    return build_result_pack(
        task=task,
        run=run,
        plan=plan,
        evidence=evidence,
        decisions=[decision],
        cost_record=cost_record,
        tool_calls=[tool_call],
        memory_records=memory_records,
        result_summary="Interactive dev loop completed a minimal read-only execution.",
        output={"plan_steps": plan.steps, "result": "Minimal interactive dev execution completed.", "blocked_reason": None, "budget_decision": budget_decision.to_dict()},
    )
