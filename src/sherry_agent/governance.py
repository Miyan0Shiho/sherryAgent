from __future__ import annotations

from dataclasses import dataclass

from .cost import BudgetDecision, CostController
from .memory import MemoryStore
from .models import Evidence, MemoryRecord, ReleaseGateResult as ReleaseSummary, ResultPack, TriggerEvent
from .planner import Planner, PlannerRequest
from .runtime import finalize_cost_record, start_task_run
from .scheduler import TriggerScheduler
from .tooling import ToolRegistry


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
    budget_profile: str | None = None
    quant_summary: dict[str, object] | None = None


GateResultPack = ResultPack


@dataclass(slots=True)
class GateResultPack(ResultPack):
    gate_result: str | None = None
    budget_decision: BudgetDecision | None = None
    trigger_event: TriggerEvent | None = None

    def to_dict(self) -> dict[str, object]:
        payload = super().to_dict()
        if self.gate_result is not None:
            payload["gate_result"] = self.gate_result
        if self.budget_decision is not None:
            payload["budget_decision"] = self.budget_decision.to_dict()
        if self.trigger_event is not None:
            payload["trigger_event"] = self.trigger_event.to_dict()
        return payload


def run_release_gate(request: GateRequest, *, memory_store: MemoryStore | None = None):
    plan = Planner().plan(PlannerRequest(source=request.source, goal=request.goal, risk_level="HIGH" if request.simulate_high_risk else request.risk_level, preferred_mode="background-ops"))
    if request.budget_profile:
        plan.budget_profile = request.budget_profile
    task, run = start_task_run(source=request.source, goal=request.goal, priority=2, risk_level="HIGH" if request.simulate_high_risk else request.risk_level, request_id=request.request_id, plan=plan)
    scheduler = TriggerScheduler()
    trigger_event = scheduler.schedule_event(source=request.source, payload={"repo": request.repo, "goal": request.goal})
    registry = ToolRegistry()
    tool_call = registry.build_call(run_id=run.run_id, tool_name="governance.scan", target=request.repo, mode=plan.mode, risk_level=task.risk_level)
    if request.simulate_high_risk:
        tool_call.is_destructive = True
    decision = registry.evaluate_call(tool_call)
    evidence = [
        Evidence(run_id=run.run_id, source_type="repo", source_ref=request.repo, summary=f"Governance scan requested for repository {request.repo}.", confidence="high"),
        Evidence(run_id=run.run_id, source_type="required_checks", source_ref=",".join(request.required_checks), summary="Required checks captured for gate evaluation.", confidence="high"),
    ]
    gate_result = "pass"
    summary = "Release governance scan passed."
    output = {
        "required_checks": request.required_checks,
        "rollback_plan": request.rollback_plan,
        "evidence_links": [item.source_ref for item in evidence],
        "quant_summary": request.quant_summary or {},
        "trigger_event": trigger_event.to_dict(),
    }
    cost_record = finalize_cost_record(run, token_in=140, token_out=110, tool_calls=1, estimated_cost=0.003)
    budget_controller = CostController(initial_profile=plan.budget_profile)
    budget_decision: BudgetDecision = budget_controller.record(cost_record)
    output["budget_decision"] = budget_decision.to_dict()
    memory_records: list[MemoryRecord] = []
    if request.rollback_plan is None:
        gate_result = "block"
        summary = "Release governance scan blocked because rollback plan is missing."
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        output["blocked_reason"] = "missing_rollback_plan"
    elif budget_decision.status == "block":
        gate_result = "block"
        summary = "Release governance scan blocked by budget controller."
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        output["blocked_reason"] = "budget_block"
    elif decision.decision_type == "block":
        gate_result = "block"
        summary = "Release governance scan blocked by policy gate."
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        output["blocked_reason"] = "policy_block"
    elif decision.decision_type == "require_confirmation":
        gate_result = "hold"
        summary = "Release governance scan is waiting on human confirmation."
        task.transition("waiting_confirmation")
        run.finish(outcome="waiting_confirmation", status="waiting_confirmation")
        output["blocked_reason"] = "waiting_confirmation"
    else:
        task.transition("completed")
        run.finish(outcome="completed", status="completed")
        output["gate_result"] = "pass"
    active_memory_store = memory_store or MemoryStore()
    try:
        for item in evidence:
            memory_records.append(
                active_memory_store.put(
                    MemoryRecord(
                        task_id=task.task_id,
                        run_id=run.run_id,
                        scope=f"release:{request.repo}",
                        kind="session",
                        key=item.source_type,
                        value=item.summary,
                        ttl_seconds=3600,
                    )
                )
            )
        output["memory_summary"] = active_memory_store.compress(scope=f"release:{request.repo}", ttl_seconds=7200).to_dict()
    finally:
        if memory_store is None:
            active_memory_store.close()
    release_gate = ReleaseSummary(
        gate_result=gate_result,
        required_checks=request.required_checks,
        evidence_links=output["evidence_links"],
        rollback_plan=request.rollback_plan,
        runbook=[
            "Collect evidence and gate metrics.",
            "Require human confirmation for any write path.",
            "Prepare rollback before release execution.",
        ],
    )
    output["gate_result"] = gate_result
    return GateResultPack(
        task=task,
        run=run,
        plan=plan,
        evidence=evidence,
        decisions=[decision],
        cost_record=cost_record,
        tool_calls=[tool_call],
        memory_records=memory_records,
        trigger_events=[trigger_event],
        result_summary=summary,
        output=output,
        release_gate=release_gate,
        gate_result=gate_result,
        budget_decision=budget_decision,
        trigger_event=trigger_event,
    )
