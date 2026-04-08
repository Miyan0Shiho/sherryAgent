from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass
from datetime import datetime, timezone

import pytest

from src.sherry_agent import models

pytestmark = [pytest.mark.contract, pytest.mark.persistence]


EXPECTED_TASK_FIELDS = {
    "task_id",
    "idempotency_key",
    "source",
    "goal",
    "priority",
    "risk_level",
    "budget_profile",
    "mode",
    "status",
    "created_at",
    "updated_at",
}

EXPECTED_RUN_FIELDS = {
    "run_id",
    "task_id",
    "plan_version",
    "model_profile",
    "toolset",
    "started_at",
    "ended_at",
    "outcome",
    "status",
    "mode",
}

EXPECTED_EVIDENCE_FIELDS = {
    "evidence_id",
    "run_id",
    "source_type",
    "source_ref",
    "summary",
    "confidence",
    "captured_at",
}

EXPECTED_DECISION_FIELDS = {
    "decision_id",
    "run_id",
    "decision_type",
    "policy_basis",
    "requires_human",
    "approved_by",
    "reason",
    "created_at",
}

EXPECTED_COST_RECORD_FIELDS = {
    "run_id",
    "token_in",
    "token_out",
    "tool_calls",
    "latency_ms",
    "cache_hit",
    "estimated_cost",
    "recorded_at",
}

EXPECTED_STATUS_VALUES = {
    "created",
    "planned",
    "running",
    "waiting_confirmation",
    "completed",
    "blocked",
    "failed",
    "cancelled",
}


def _public_string_constants(module) -> set[str]:
    values: set[str] = set()
    for name, value in vars(module).items():
        if not name.isupper():
            continue
        if isinstance(value, str):
            values.add(value)
        elif isinstance(value, (tuple, list, set, frozenset)):
            values.update(item for item in value if isinstance(item, str))
    return values


def _build_sample_time() -> datetime:
    return datetime(2026, 4, 8, tzinfo=timezone.utc)


def test_models_are_dataclasses_and_expose_required_fields() -> None:
    for model_name, expected_fields in (
        ("Task", EXPECTED_TASK_FIELDS),
        ("Run", EXPECTED_RUN_FIELDS),
        ("Evidence", EXPECTED_EVIDENCE_FIELDS),
        ("Decision", EXPECTED_DECISION_FIELDS),
        ("CostRecord", EXPECTED_COST_RECORD_FIELDS),
    ):
        model = getattr(models, model_name)
        assert is_dataclass(model), model_name
        assert expected_fields <= {field.name for field in fields(model)}, model_name


def test_status_constants_cover_the_expected_state_machine() -> None:
    values = _public_string_constants(models)
    assert EXPECTED_STATUS_VALUES <= values


def test_task_and_run_reject_invalid_state_values() -> None:
    task = models.Task(
        source="cli",
        goal="run Story-01",
        priority=1,
        risk_level="LOW",
        budget_profile="balanced",
        mode="interactive-dev",
        status="created",
        idempotency_key="idem-3",
    )
    with pytest.raises(ValueError):
        task.transition("not-a-state")

    run = models.Run(
        task_id=task.task_id,
        plan_version="plan-1",
        model_profile="baseline-fast",
        toolset=["repo.read"],
        outcome="planned",
        status="running",
        mode="interactive-dev",
    )
    with pytest.raises(ValueError):
        run.finish(outcome="completed", status="not-a-state")


def test_core_objects_round_trip_relationships() -> None:
    task = models.Task(
        task_id="task-1",
        idempotency_key="idem-1",
        source="cli",
        goal="run Story-01",
        priority=1,
        risk_level="LOW",
        budget_profile="balanced",
        mode="interactive-dev",
        status="created",
        created_at=_build_sample_time(),
        updated_at=_build_sample_time(),
    )
    run = models.Run(
        run_id="run-1",
        task_id=task.task_id,
        plan_version="plan-1",
        model_profile="gpt-5",
        toolset=["read_file"],
        started_at=_build_sample_time(),
        ended_at=_build_sample_time(),
        outcome="ok",
        status="completed",
        mode="interactive-dev",
    )
    evidence = models.Evidence(
        evidence_id="ev-1",
        run_id=run.run_id,
        source_type="file",
        source_ref="docs/specs/core-data-contracts.md",
        summary="core contract proof",
        confidence="high",
        captured_at=_build_sample_time(),
    )
    decision = models.Decision(
        decision_id="dec-1",
        run_id=run.run_id,
        decision_type="allow",
        policy_basis="LOW risk read-only action",
        requires_human=False,
        approved_by="policy-gate",
        reason="Allowed because the action is read-only and low risk.",
        created_at=_build_sample_time(),
    )
    cost = models.CostRecord(
        run_id=run.run_id,
        token_in=10,
        token_out=20,
        tool_calls=1,
        latency_ms=15,
        cache_hit=True,
        estimated_cost=0.01,
        recorded_at=_build_sample_time(),
    )

    assert task.task_id == run.task_id
    assert evidence.run_id == run.run_id
    assert decision.run_id == run.run_id
    assert cost.run_id == run.run_id
    assert asdict(task)["mode"] == "interactive-dev"


@pytest.mark.decision_replay
def test_state_transition_helpers_update_status_and_timestamps() -> None:
    task = models.Task(
        source="cli",
        goal="run Story-01",
        priority=1,
        risk_level="LOW",
        budget_profile="balanced",
        mode="interactive-dev",
        status="created",
        idempotency_key="idem-2",
    )
    original_updated_at = task.updated_at
    task.transition("planned")

    assert task.status == "planned"
    assert task.updated_at >= original_updated_at

    run = models.Run(
        task_id=task.task_id,
        plan_version="plan-1",
        model_profile="baseline-fast",
        toolset=["repo.read"],
        outcome="planned",
        status="running",
        mode="interactive-dev",
    )
    assert run.ended_at is None
    run.finish(outcome="completed", status="completed")

    assert run.outcome == "completed"
    assert run.status == "completed"
    assert run.ended_at is not None
