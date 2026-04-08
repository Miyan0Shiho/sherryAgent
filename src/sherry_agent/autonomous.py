from __future__ import annotations

from dataclasses import dataclass

from .cost import CostController
from .memory import MemoryStore
from .models import Evidence, MemoryRecord
from .planner import Planner, PlannerRequest
from .runtime import build_result_pack, finalize_cost_record, start_task_run
from .scheduler import TriggerScheduler
from .tooling import ToolRegistry


@dataclass(slots=True)
class AutonomousSafeRequest:
    source: str
    goal: str
    trigger_source: str = "cron"
    risk_level: str = "LOW"
    priority: int = 3
    real_run: bool = False
    request_id: str = "story02-default"


@dataclass(slots=True)
class BackgroundOpsRequest:
    source: str
    goal: str
    repo: str
    incident_id: str
    trigger_source: str = "event"
    risk_level: str = "MEDIUM"
    priority: int = 2
    apply_fix: bool = False
    simulate_destructive_fix: bool = False
    request_id: str = "story03-default"


def run_autonomous_safe(request: AutonomousSafeRequest):
    plan = Planner().plan(PlannerRequest(source=request.source, goal=request.goal, risk_level=request.risk_level, preferred_mode="autonomous-safe"))
    task, run = start_task_run(source=request.source, goal=request.goal, priority=request.priority, risk_level=request.risk_level, request_id=request.request_id, plan=plan)
    scheduler = TriggerScheduler()
    trigger = scheduler.schedule_event(source=request.trigger_source, payload={"goal": request.goal})
    registry = ToolRegistry()
    tool_call = registry.build_call(run_id=run.run_id, tool_name="scheduler.trigger", target=request.trigger_source, mode=plan.mode, risk_level=request.risk_level)
    decision = registry.evaluate_call(tool_call)
    evidence = [
        Evidence(run_id=run.run_id, source_type="request", source_ref=request.request_id, summary=f"Autonomous safe request received: {request.goal}", confidence="high"),
        Evidence(run_id=run.run_id, source_type="trigger", source_ref=request.trigger_source, summary="Background trigger captured for a safe autonomous run.", confidence="high"),
    ]
    with MemoryStore() as store:
        memory_record = store.put(
            MemoryRecord(
                task_id=task.task_id,
                run_id=run.run_id,
                scope="story02",
                kind="session",
                key="dry-run" if not request.real_run else "real-run",
                value=f"Autonomous safe workflow planned for {request.goal}",
                ttl_seconds=3600,
            )
        )
    if not request.real_run:
        evidence.append(Evidence(run_id=run.run_id, source_type="dry_run", source_ref="autonomous-safe", summary="Dry-run completed with confirmation required before real execution.", confidence="high"))
        task.transition("waiting_confirmation")
        run.finish(outcome="waiting_confirmation", status="waiting_confirmation")
        cost_record = finalize_cost_record(run, token_in=100, token_out=72, tool_calls=1, estimated_cost=0.0015)
        return build_result_pack(
            task=task,
            run=run,
            plan=plan,
            evidence=evidence,
            decisions=[decision],
            cost_record=cost_record,
            tool_calls=[tool_call],
            memory_records=[memory_record],
            trigger_events=[trigger],
            result_summary="Autonomous safe loop completed a dry-run and awaits confirmation.",
            output={"execution_mode": "dry-run", "requires_confirmation": True, "next_action": "confirm_real_run", "plan_steps": plan.steps},
        )
    evidence.append(Evidence(run_id=run.run_id, source_type="execution", source_ref="autonomous-safe:real-run", summary="Safe autonomous execution completed on the requested schedule.", confidence="high"))
    task.transition("completed")
    run.finish(outcome="completed", status="completed")
    cost_record = finalize_cost_record(run, token_in=150, token_out=96, tool_calls=1, estimated_cost=0.002)
    budget_decision = CostController(initial_profile=plan.budget_profile).record(cost_record)
    return build_result_pack(
        task=task,
        run=run,
        plan=plan,
        evidence=evidence,
        decisions=[decision],
        cost_record=cost_record,
        tool_calls=[tool_call],
        memory_records=[memory_record],
        trigger_events=[trigger],
        result_summary="Autonomous safe loop completed its real run.",
        output={"execution_mode": "real-run", "result": "Safe autonomous task completed.", "plan_steps": plan.steps, "budget_decision": budget_decision.to_dict()},
    )


def run_background_ops(request: BackgroundOpsRequest):
    plan = Planner().plan(PlannerRequest(source=request.source, goal=request.goal, risk_level=request.risk_level, preferred_mode="background-ops"))
    task, run = start_task_run(source=request.source, goal=request.goal, priority=request.priority, risk_level=request.risk_level, request_id=request.request_id, plan=plan)
    registry = ToolRegistry()
    scan_call = registry.build_call(run_id=run.run_id, tool_name="governance.scan", target=request.repo, mode=plan.mode, risk_level=request.risk_level)
    decisions = [registry.evaluate_call(scan_call)]
    evidence = [
        Evidence(run_id=run.run_id, source_type="incident", source_ref=request.incident_id, summary=f"Incident captured from {request.trigger_source} for repo {request.repo}.", confidence="high"),
        Evidence(run_id=run.run_id, source_type="repo", source_ref=request.repo, summary="Read-only repo context collected for diagnosis.", confidence="high"),
        Evidence(run_id=run.run_id, source_type="diagnosis", source_ref=request.incident_id, summary="Initial diagnosis produced from available evidence.", confidence="medium"),
    ]
    with MemoryStore() as store:
        memory_record = store.put(
            MemoryRecord(
                task_id=task.task_id,
                run_id=run.run_id,
                scope="story03",
                kind="session",
                key=request.incident_id,
                value=f"Incident evidence collected for repo {request.repo}",
                ttl_seconds=3600,
            )
        )
    output = {
        "incident_id": request.incident_id,
        "repo": request.repo,
        "diagnosis": "Evidence points to a contained issue requiring controlled remediation.",
        "rollback_plan": f"restore repo {request.repo} to the last known good state for {request.incident_id}",
        "runbook": "Capture evidence, confirm remediation, and keep human approval for any write action.",
        "plan_steps": plan.steps,
    }
    tool_calls = [scan_call]
    if request.apply_fix:
        write_call = registry.build_call(run_id=run.run_id, tool_name="repo.write", target=request.repo, mode=plan.mode, risk_level="CRITICAL" if request.simulate_destructive_fix else "HIGH")
        write_call.is_destructive = request.simulate_destructive_fix
        decisions.append(registry.evaluate_call(write_call))
        tool_calls.append(write_call)
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        output["blocked_reason"] = "policy_block"
        summary = "Background ops blocked because remediation was too risky."
    else:
        task.transition("completed")
        run.finish(outcome="completed", status="completed")
        summary = "Background ops completed evidence collection and diagnosis."
    cost_record = finalize_cost_record(run, token_in=180, token_out=120, tool_calls=len(tool_calls), estimated_cost=0.003)
    return build_result_pack(
        task=task,
        run=run,
        plan=plan,
        evidence=evidence,
        decisions=decisions,
        cost_record=cost_record,
        tool_calls=tool_calls,
        memory_records=[memory_record],
        result_summary=summary,
        output=output,
    )
