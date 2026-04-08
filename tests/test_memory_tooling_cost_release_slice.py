from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest

from src.sherry_agent.cost import CostController
from src.sherry_agent.governance import GateRequest, run_release_gate
from src.sherry_agent.memory import MemoryRecord, MemoryStore
from src.sherry_agent.scheduler import TriggerScheduler
from src.sherry_agent.tooling import ToolCall, ToolRegistry
from src.sherry_agent.models import CostRecord, utc_now

pytestmark = [pytest.mark.contract, pytest.mark.governance]


def test_tool_registry_enforces_tool_metadata_and_policy() -> None:
    registry = ToolRegistry()

    allow_decision = registry.evaluate_call(
        ToolCall(
            run_id="run-1",
            tool_name="governance.scan",
            target="repo",
            mode="background-ops",
            risk_level="LOW",
        )
    )
    block_decision = registry.evaluate_call(
        ToolCall(
            run_id="run-2",
            tool_name="repo.write",
            target="repo",
            mode="background-ops",
            risk_level="LOW",
            is_write=True,
        )
    )

    assert allow_decision.decision_type == "allow"
    assert block_decision.decision_type == "block"
    assert registry.require("repo.write").requires_confirmation is True


def test_memory_store_retrieves_compresses_and_purges(tmp_path: Path) -> None:
    db_path = tmp_path / "memory.sqlite"
    expired_at = utc_now() - timedelta(seconds=5)

    with MemoryStore(db_path) as store:
        first = store.put(
            MemoryRecord(
                scope="release:repo",
                content="Rollback plan documented for release gate.",
                story="Story-05",
                relevance=0.95,
                ttl_seconds=60,
            )
        )
        store.put(
            MemoryRecord(
                scope="release:repo",
                content="Evidence links collected from governance scan.",
                story="Story-05",
                relevance=0.85,
                ttl_seconds=60,
            )
        )
        store.put(
            MemoryRecord(
                scope="release:repo",
                content="expired note",
                story="Story-05",
                relevance=0.1,
                ttl_seconds=60,
                expires_at=expired_at,
            )
        )

        retrieved = store.retrieve("rollback", scope="release:repo")
        summary = store.compress(scope="release:repo", ttl_seconds=120)
        removed = store.purge_expired()

    assert first.memory_id
    assert retrieved and retrieved[0].content.startswith("Rollback plan")
    assert summary.kind == "summary"
    assert summary.metadata["compressed_from"]
    assert removed == 1


def test_cost_controller_degrades_then_tracks_budget() -> None:
    controller = CostController(initial_profile="balanced")
    costly_record = CostRecord(
        run_id="run-3",
        token_in=500,
        token_out=500,
        tool_calls=2,
        latency_ms=200,
        cache_hit=False,
        estimated_cost=0.25,
    )

    decision = controller.record(costly_record)

    assert decision.status == "degrade"
    assert decision.next_profile == "strict"
    assert controller.current_profile == "strict"


def test_scheduler_tracks_due_trigger_events() -> None:
    scheduler = TriggerScheduler()
    due_event = scheduler.schedule_event(
        source="ops",
        payload={"kind": "incident"},
        when=utc_now() - timedelta(seconds=1),
    )
    future_event = scheduler.schedule_periodic(
        source="ops",
        interval_seconds=60,
        payload={"kind": "periodic"},
    )

    due = scheduler.due_events()
    dispatched = scheduler.dispatch_due()
    completed = scheduler.complete(due_event.trigger_id)

    assert due == [due_event]
    assert dispatched[0].dispatched_at is not None
    assert completed.status == "completed"
    assert future_event.status == "queued"


def test_release_gate_produces_budget_and_trigger_evidence(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "release-memory.sqlite") as store:
        result = run_release_gate(
            GateRequest(
                source="cli",
                goal="Scan repo for release readiness",
                repo="sherryAgent",
                required_checks=["Spec-Docs Sync", "Gate Eligibility (G1-G4)"],
                rollback_plan="restore prior state",
                risk_level="LOW",
                request_id="req-release",
            ),
            memory_store=store,
        )

    assert result.gate_result == "pass"
    assert result.budget_decision is not None
    assert result.trigger_event is not None
    assert result.output["gate_result"] == "pass"
    assert result.output["memory_summary"]["kind"] == "summary"
    assert len(result.evidence) == 2


def test_release_gate_high_risk_waits_for_confirmation() -> None:
    result = run_release_gate(
        GateRequest(
            source="cli",
            goal="Scan repo for release readiness",
            repo="sherryAgent",
            required_checks=["Spec-Docs Sync", "Gate Eligibility (G1-G4)"],
            rollback_plan="restore prior state",
            risk_level="HIGH",
            request_id="req-release-high",
        )
    )

    assert result.gate_result == "hold"
    assert result.run.status == "waiting_confirmation"
    assert result.output["blocked_reason"] == "waiting_confirmation"
