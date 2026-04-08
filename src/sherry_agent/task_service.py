from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import (
    CostRecord,
    Decision,
    Evidence,
    MemoryRecord,
    Plan,
    ReleaseGateResult,
    ResultPack,
    Run,
    Task,
    TriggerEvent,
    ToolCall,
)
from .storage import SherryRepository


@dataclass(slots=True)
class TaskBundle:
    task: Task
    runs: list[Run]
    evidence: list[Evidence]
    decisions: list[Decision]
    cost_records: list[CostRecord]
    memory_records: list[MemoryRecord]
    trigger_events: list[TriggerEvent]


class TaskService:
    def __init__(self, repository: SherryRepository | None = None) -> None:
        self.repository = repository or SherryRepository()

    def persist(self, pack: ResultPack) -> ResultPack:
        self.repository.persist_result_pack(pack)
        return pack

    def create_task(self, task: Task) -> Task:
        existing = self.repository.get_task_by_idempotency_key(task.idempotency_key)
        if existing is not None:
            return existing
        return self.record_task(task)

    def transition_task(self, task_id: str, status: str) -> Task:
        task = self.require_task(task_id)
        task.transition(status)
        return self.record_task(task)

    def require_task(self, task_id: str) -> Task:
        task = self.repository.get_task(task_id)
        if task is None:
            raise KeyError(f"task not found: {task_id}")
        return task

    def record_task(self, task: Task) -> Task:
        self.repository.save_task(task)
        return task

    def record_run(self, run: Run) -> Run:
        self.repository.save_run(run)
        return run

    def start_run(self, task: Task, plan: Plan, *, outcome: str = "planned") -> Run:
        if task.status == "created":
            task.transition("planned")
        if task.status != "running":
            task.transition("running")
        run = Run(
            task_id=task.task_id,
            plan_version=plan.plan_version,
            model_profile=plan.model_profile,
            toolset=list(plan.toolset),
            outcome=outcome,
            status="running",
            mode=plan.mode,
        )
        self.record_task(task)
        self.record_run(run)
        return run

    def finish_run(self, run_id: str, outcome: str, status: str) -> Run:
        run = self.require_run(run_id)
        run.finish(outcome=outcome, status=status)
        return self.record_run(run)

    def require_run(self, run_id: str) -> Run:
        run = self.repository.get_run(run_id)
        if run is None:
            raise KeyError(f"run not found: {run_id}")
        return run

    def record_evidence(self, evidence: Evidence) -> Evidence:
        self.repository.save_evidence(evidence)
        return evidence

    def record_decision(self, decision: Decision) -> Decision:
        self.repository.save_decision(decision)
        return decision

    def record_cost(self, cost_record: CostRecord) -> CostRecord:
        self.repository.save_cost_record(cost_record)
        return cost_record

    def record_tool_call(self, tool_call: ToolCall) -> ToolCall:
        self.repository.save_tool_call(tool_call)
        return tool_call

    def record_memory(self, memory_record: MemoryRecord) -> MemoryRecord:
        self.repository.save_memory_record(memory_record)
        return memory_record

    def record_trigger(self, trigger_event: TriggerEvent) -> TriggerEvent:
        self.repository.save_trigger_event(trigger_event)
        return trigger_event

    def record_release_gate_result(self, result: ReleaseGateResult) -> ReleaseGateResult:
        self.repository.save_release_gate_result(result)
        return result

    def load_task_bundle(self, task_id: str) -> TaskBundle:
        task = self.require_task(task_id)
        runs = self.repository.list_runs(task_id)
        run_ids = [run.run_id for run in runs]
        evidence = [item for run_id in run_ids for item in self.repository.list_evidence(run_id)]
        decisions = [item for run_id in run_ids for item in self.repository.list_decisions(run_id)]
        cost_records = [item for run_id in run_ids for item in self.repository.list_cost_records(run_id)]
        memory_records = _dedupe_records(
            [*self.repository.list_memory_records(task_id=task_id), *[item for run_id in run_ids for item in self.repository.list_memory_records(run_id=run_id)]],
            "memory_id",
        )
        trigger_events = _dedupe_records(
            [*self.repository.list_trigger_events(task_id=task_id), *[item for run_id in run_ids for item in self.repository.list_trigger_events(run_id=run_id)]],
            "trigger_id",
        )
        return TaskBundle(
            task=task,
            runs=runs,
            evidence=evidence,
            decisions=decisions,
            cost_records=cost_records,
            memory_records=memory_records,
            trigger_events=trigger_events,
        )

    def snapshot(self, task_id: str) -> dict[str, Any]:
        bundle = self.load_task_bundle(task_id)
        return {
            "task": bundle.task.to_dict(),
            "runs": [run.to_dict() for run in bundle.runs],
            "evidence": [item.to_dict() for item in bundle.evidence],
            "decisions": [item.to_dict() for item in bundle.decisions],
            "cost_records": [item.to_dict() for item in bundle.cost_records],
            "memory_records": [item.to_dict() for item in bundle.memory_records],
            "trigger_events": [item.to_dict() for item in bundle.trigger_events],
        }


def _dedupe_records(items: list[Any], attr: str) -> list[Any]:
    seen: set[Any] = set()
    unique: list[Any] = []
    for item in items:
        marker = getattr(item, attr)
        if marker in seen:
            continue
        seen.add(marker)
        unique.append(item)
    return unique


__all__ = ["TaskBundle", "TaskService"]
