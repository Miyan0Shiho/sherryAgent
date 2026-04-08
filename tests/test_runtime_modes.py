from __future__ import annotations

import pytest

from src.sherry_agent.autonomous import (
    AutonomousSafeRequest,
    BackgroundOpsRequest,
    run_autonomous_safe,
    run_background_ops,
)
from src.sherry_agent.bulk import BulkAnalysisRequest, run_bulk_analysis
from src.sherry_agent.planner import Planner, PlannerRequest

pytestmark = [pytest.mark.contract]


@pytest.mark.parametrize(
    ("planner_request", "expected_mode", "expected_budget"),
    [
        (
            PlannerRequest(
                source="cli",
                goal="create a helper command",
                risk_level="LOW",
                preferred_mode="interactive-dev",
            ),
            "interactive-dev",
            "balanced",
        ),
        (
            PlannerRequest(
                source="cron",
                goal="run a daily report",
                risk_level="LOW",
            ),
            "autonomous-safe",
            "strict",
        ),
        (
            PlannerRequest(
                source="event",
                goal="respond to an incident alert",
                risk_level="MEDIUM",
            ),
            "background-ops",
            "strict",
        ),
        (
            PlannerRequest(
                source="cli",
                goal="run a bulk repository audit",
                risk_level="LOW",
            ),
            "bulk-analysis",
            "strict",
        ),
    ],
)
def test_planner_covers_the_four_runtime_modes(
    planner_request: PlannerRequest,
    expected_mode: str,
    expected_budget: str,
) -> None:
    plan = Planner().plan(planner_request)

    assert plan.mode == expected_mode
    assert plan.budget_profile == expected_budget
    assert plan.steps
    assert plan.toolset


@pytest.mark.story01
def test_autonomous_safe_dry_run_waits_for_confirmation() -> None:
    result = run_autonomous_safe(
        AutonomousSafeRequest(
            source="cron",
            goal="generate a daily account summary",
            trigger_source="cron",
            real_run=False,
            request_id="story02-dry-run",
        )
    )

    assert result.task.mode == "autonomous-safe"
    assert result.run.status == "waiting_confirmation"
    assert result.output["execution_mode"] == "dry-run"
    assert result.output["requires_confirmation"] is True
    assert result.evidence_count == 3


@pytest.mark.story05
@pytest.mark.governance
def test_background_ops_apply_fix_waits_for_confirmation() -> None:
    result = run_background_ops(
        BackgroundOpsRequest(
            source="event",
            goal="investigate and remediate an incident",
            repo="sherryAgent",
            incident_id="inc-001",
            apply_fix=True,
            request_id="story03-fix",
        )
    )

    assert result.task.mode == "background-ops"
    assert result.run.status == "blocked"
    assert result.output["rollback_plan"]
    assert result.output["blocked_reason"] == "policy_block"
    assert result.decision_count == 2


@pytest.mark.story05
def test_bulk_analysis_shards_targets_and_aggregates() -> None:
    result = run_bulk_analysis(
        BulkAnalysisRequest(
            source="cli",
            goal="run a repository audit across many targets",
            targets=["repo-a", "repo-b", "repo-c", "repo-d"],
            shard_size=2,
            request_id="story04-bulk",
        )
    )

    assert result.task.mode == "bulk-analysis"
    assert result.run.status == "completed"
    assert result.output["shard_count"] == 2
    assert len(result.output["aggregated_findings"]) == 2
    assert result.evidence_count == 3
