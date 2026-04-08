from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _read_doc(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _assert_terms(text: str, terms: tuple[str, ...]) -> None:
    missing = [term for term in terms if term not in text]
    assert not missing, f"missing terms: {', '.join(missing)}"


@pytest.mark.contract
@pytest.mark.runtime
@pytest.mark.persistence
def test_core_data_contract_document_locks_state_machine_and_relationships() -> None:
    text = _read_doc("docs/specs/core-data-contracts.md")
    _assert_terms(
        text,
        (
            "Task -> Run -> Evidence -> Decision -> Cost Record",
            "created",
            "planned",
            "running",
            "waiting_confirmation",
            "blocked",
            "failed",
            "cancelled",
            "task_id",
            "run_id",
            "evidence_id",
            "decision_id",
            "estimated_cost",
        ),
    )


@pytest.mark.contract
@pytest.mark.persistence
def test_task_persistence_contract_document_requires_recovery_consistency() -> None:
    text = _read_doc("docs/specs/task-persistence.md")
    _assert_terms(
        text,
        (
            "Task Service",
            "恢复",
            "waiting_confirmation",
            "Decision",
            "审计",
            "blocked",
            "只读诊断报告",
        ),
    )


@pytest.mark.contract
@pytest.mark.memory
def test_memory_contract_document_prioritizes_evidence_and_ttl_rules() -> None:
    text = _read_doc("docs/specs/memory-system.md")
    _assert_terms(
        text,
        (
            "Evidence",
            "TTL",
            "high | medium | low",
            "evidence_id",
            "source_ref",
            "事实",
            "推断",
            "版本化",
            "冷热分层",
        ),
    )


@pytest.mark.contract
@pytest.mark.cost
def test_cost_contract_document_defines_budget_and_degradation_rules() -> None:
    text = _read_doc("docs/specs/cost-ops-governance.md")
    _assert_terms(
        text,
        (
            "strict",
            "balanced",
            "premium",
            "降级",
            "缓存",
            "限流",
            "queue_lag",
            "token_burn_per_hour",
            "concurrent_runs",
            "policy_block_rate",
        ),
    )
