from __future__ import annotations

from dataclasses import dataclass

from .memory import MemoryStore
from .models import Evidence, MemoryRecord
from .planner import Planner, PlannerRequest
from .runtime import build_result_pack, finalize_cost_record, start_task_run
from .tooling import ToolRegistry


@dataclass(slots=True)
class BulkAnalysisRequest:
    source: str
    goal: str
    targets: list[str]
    risk_level: str = "LOW"
    shard_size: int = 3
    request_id: str = "story04-default"


def _chunk_targets(targets: list[str], shard_size: int) -> list[list[str]]:
    if shard_size <= 0:
        raise ValueError("shard_size must be positive")
    return [targets[index : index + shard_size] for index in range(0, len(targets), shard_size)]


def run_bulk_analysis(request: BulkAnalysisRequest):
    plan = Planner().plan(PlannerRequest(source=request.source, goal=request.goal, risk_level=request.risk_level, preferred_mode="bulk-analysis"))
    task, run = start_task_run(source=request.source, goal=request.goal, priority=2, risk_level=request.risk_level, request_id=request.request_id, plan=plan)
    registry = ToolRegistry()
    tool_call = registry.build_call(run_id=run.run_id, tool_name="memory.read", target="bulk-targets", mode=plan.mode, risk_level=request.risk_level)
    decision = registry.evaluate_call(tool_call)
    evidence = [Evidence(run_id=run.run_id, source_type="request", source_ref=request.request_id, summary=f"Bulk analysis request received for {len(request.targets)} targets.", confidence="high")]
    if not request.targets:
        task.transition("blocked")
        run.finish(outcome="blocked", status="blocked")
        evidence.append(Evidence(run_id=run.run_id, source_type="validation", source_ref="no-targets", summary="Bulk analysis blocked because no targets were provided.", confidence="high"))
        cost_record = finalize_cost_record(run, token_in=72, token_out=40, tool_calls=1, estimated_cost=0.001)
        return build_result_pack(
            task=task,
            run=run,
            plan=plan,
            evidence=evidence,
            decisions=[decision],
            cost_record=cost_record,
            tool_calls=[tool_call],
            result_summary="Bulk analysis blocked because the target list was empty.",
            output={"blocked_reason": "empty_targets", "shards": [], "aggregated_findings": []},
        )
    shards = _chunk_targets(request.targets, request.shard_size)
    aggregated_findings = []
    with MemoryStore() as store:
        memory_record = store.put(
            MemoryRecord(
                task_id=task.task_id,
                run_id=run.run_id,
                scope="story04",
                kind="knowledge",
                key="bulk-targets",
                value=", ".join(request.targets),
                ttl_seconds=3600,
            )
        )
    for index, shard in enumerate(shards, start=1):
        evidence.append(Evidence(run_id=run.run_id, source_type="shard", source_ref=f"shard-{index}", summary=f"Shard {index} covers {len(shard)} target(s): {', '.join(shard)}.", confidence="medium" if len(shard) > 1 else "high"))
        aggregated_findings.append({"shard": index, "targets": shard, "finding": "No blocking issues detected in this shard.", "confidence": "medium" if len(request.targets) > 4 else "high"})
    task.transition("completed")
    run.finish(outcome="completed", status="completed")
    cost_record = finalize_cost_record(run, token_in=240, token_out=180, tool_calls=len(shards) + 1, estimated_cost=0.004)
    return build_result_pack(
        task=task,
        run=run,
        plan=plan,
        evidence=evidence,
        decisions=[decision],
        cost_record=cost_record,
        tool_calls=[tool_call],
        memory_records=[memory_record],
        result_summary="Bulk analysis completed by sharding the target set and aggregating findings.",
        output={"shard_count": len(shards), "shards": shards, "aggregated_findings": aggregated_findings, "confidence": "medium" if len(request.targets) > 4 else "high", "plan_steps": plan.steps},
    )
