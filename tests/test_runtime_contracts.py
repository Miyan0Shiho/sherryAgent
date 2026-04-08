from __future__ import annotations

from dataclasses import is_dataclass

import pytest

from src.sherry_agent.governance import GateRequest, GateResultPack, run_release_gate
from src.sherry_agent.planner import Plan, Planner, PlannerRequest
from src.sherry_agent.policy import PolicyAction, PolicyGate
from src.sherry_agent.runtime import InteractiveDevRequest, run_interactive_dev

pytestmark = [pytest.mark.contract, pytest.mark.runtime, pytest.mark.policy]


def _interactive_request() -> dict[str, object]:
    return {
        "source": "cli",
        "goal": "create a small command",
        "risk_level": "LOW",
    }


def _release_request() -> dict[str, object]:
    return {
        "source": "cli",
        "repo": "sherryAgent",
        "goal": "run release governance scan",
        "risk_level": "LOW",
        "rollback_plan": "restore prior state",
        "required_checks": ["Spec-Docs Sync", "Gate Eligibility (G1-G4)"],
    }


def test_planner_returns_public_plan_object() -> None:
    planner = Planner()
    plan = planner.plan(
        PlannerRequest(
            source="cli",
            goal="create a small command",
            risk_level="LOW",
            preferred_mode="interactive-dev",
        )
    )

    assert isinstance(plan, Plan)
    assert plan.mode == "interactive-dev"
    assert plan.budget_profile == "balanced"
    assert plan.toolset == ["repo.read"]
    assert plan.steps[-1] == "review_output"


def test_planner_routes_release_governance_requests_to_background_ops() -> None:
    planner = Planner()
    plan = planner.plan(
        PlannerRequest(
            source="cli",
            goal="run release governance scan",
            risk_level="LOW",
        )
    )

    assert plan.mode == "background-ops"
    assert plan.budget_profile == "strict"
    assert plan.steps[-1] == "produce_gate_result"


@pytest.mark.decision_replay
def test_policy_gate_requires_confirmation_for_high_risk_writes() -> None:
    gate = PolicyGate()
    decision = gate.evaluate(
        PolicyAction(
            run_id="run-1",
            name="write_file",
            mode="interactive-dev",
            risk_level="HIGH",
            is_write=True,
        )
    )

    assert is_dataclass(decision)
    assert getattr(decision, "requires_human") is True
    assert decision.decision_type == "require_confirmation"
    assert decision.policy_basis == "write_or_high_risk_requires_confirmation"
    assert decision.reason


def test_policy_gate_blocks_destructive_actions() -> None:
    gate = PolicyGate()
    decision = gate.evaluate(
        PolicyAction(
            run_id="run-2",
            name="delete_file",
            mode="background-ops",
            risk_level="LOW",
            is_write=True,
            is_destructive=True,
        )
    )

    assert decision.decision_type == "block"
    assert decision.requires_human is True
    assert decision.policy_basis == "destructive_or_critical_action"


def test_policy_gate_blocks_background_writes() -> None:
    pytest.xfail("Background write block ordering is not wired in the current runtime yet.")
    gate = PolicyGate()
    decision = gate.evaluate(
        PolicyAction(
            run_id="run-3",
            name="write_file",
            mode="background-ops",
            risk_level="LOW",
            is_write=True,
        )
    )

    assert decision.decision_type == "block"
    assert decision.requires_human is True
    assert decision.policy_basis == "background_write_blocked"


@pytest.mark.story01
@pytest.mark.decision_replay
def test_run_interactive_dev_returns_core_result_pack() -> None:
    result = run_interactive_dev(
        InteractiveDevRequest(
            source="cli",
            goal="create a small command",
            risk_level="LOW",
            request_id="req-1",
        )
    )

    assert result.task.status == "completed"
    assert result.run.status == "completed"
    assert result.evidence_count == 2
    assert result.decision_count == 1
    assert result.output["result"] == "Minimal interactive dev execution completed."
    assert result.cost_record.run_id == result.run.run_id


@pytest.mark.story01
@pytest.mark.decision_replay
def test_run_interactive_dev_budget_exhaustion_blocks_execution() -> None:
    result = run_interactive_dev(
        InteractiveDevRequest(
            source="cli",
            goal="create a small command",
            risk_level="LOW",
            simulate_budget_exhausted=True,
            request_id="req-2",
        )
    )

    assert result.task.status == "blocked"
    assert result.run.status == "blocked"
    assert result.output["blocked_reason"] == "budget_exhausted"
    assert result.evidence_count == 2


@pytest.mark.story05
@pytest.mark.governance
@pytest.mark.decision_replay
def test_run_release_gate_returns_gate_result_pack() -> None:
    result = run_release_gate(
        GateRequest(
            source="cli",
            goal="run release governance scan",
            repo="sherryAgent",
            required_checks=["Spec-Docs Sync", "Gate Eligibility (G1-G4)"],
            rollback_plan="restore prior state",
            risk_level="LOW",
            request_id="req-5",
        )
    )

    assert isinstance(result, GateResultPack)
    assert result.gate_result == "pass"
    assert result.task.status == "completed"
    assert result.output["rollback_plan"] == "restore prior state"
    assert len(result.evidence) == 2


@pytest.mark.story05
@pytest.mark.governance
@pytest.mark.decision_replay
def test_run_release_gate_missing_rollback_plan_blocks() -> None:
    result = run_release_gate(
        GateRequest(
            source="cli",
            goal="run release governance scan",
            repo="sherryAgent",
            required_checks=["Spec-Docs Sync", "Gate Eligibility (G1-G4)"],
            rollback_plan=None,
            risk_level="LOW",
            request_id="req-6",
        )
    )

    assert result.gate_result == "block"
    assert result.task.status == "blocked"
    assert result.output["blocked_reason"] == "missing_rollback_plan"
