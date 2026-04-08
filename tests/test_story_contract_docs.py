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
@pytest.mark.story02
def test_story02_documented_clerk_contract_includes_runtime_safety_terms() -> None:
    text = _read_doc("docs/stories/story-02-personal-clerk.md")
    _assert_terms(
        text,
        (
            "schedule",
            "inputs",
            "actions_planned",
            "actions_executed",
            "audit",
            "results",
            "dry-run",
            "waiting_confirmation",
            "Cost Record",
        ),
    )


@pytest.mark.contract
@pytest.mark.story03
def test_story03_documented_incident_contract_includes_evidence_and_rollback_terms() -> None:
    text = _read_doc("docs/stories/story-03-ops-sentinel-incident-responder.md")
    _assert_terms(
        text,
        (
            "Ops Health Report",
            "Incident Report",
            "evidence",
            "hypotheses",
            "runbook",
            "actions_requiring_confirmation",
            "rollback_plan",
            "告警风暴",
            "Cost Record",
        ),
    )


@pytest.mark.contract
@pytest.mark.story04
def test_story04_documented_research_contract_includes_source_and_confidence_terms() -> None:
    text = _read_doc("docs/stories/story-04-research-miner-security-auditor.md")
    _assert_terms(
        text,
        (
            "Research+Security Report",
            "scope",
            "sources",
            "findings",
            "confidence",
            "risks",
            "actions",
            "Evidence",
            "事实/推断",
            "Cost Record",
        ),
    )
