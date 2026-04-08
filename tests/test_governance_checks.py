from __future__ import annotations

import pytest

from scripts.ci import pr_governance_checks as checks

pytestmark = [pytest.mark.governance]


def _context(
    *,
    labels: list[str],
    body: str,
    title: str = "[runtime-orchestration/planner] update",
    branch_name: str = "codex/multi-agent-test/123-runtime-orchestration",
) -> checks.PRContext:
    return checks.PRContext(
        number=1,
        title=title,
        body=body,
        branch_name=branch_name,
        labels=labels,
        changed_files=[".trae/specs/runtime-orchestration/spec.md", "docs/architecture/core-operational-loops.md"],
    )


def test_spec_docs_sync_passes_for_dual_authority_updates() -> None:
    checks.check_spec_docs_sync(_context(labels=["type:contract-change"], body=""))


def test_gate_eligibility_requires_governance_fields() -> None:
    ctx = _context(labels=["gate:G1"], body="linked_issue: #1")
    with pytest.raises(SystemExit):
        checks.check_gate_eligibility(ctx)


def test_gate_eligibility_passes_with_required_fields() -> None:
    ctx = _context(
        labels=["gate:G1"],
        body="""
linked_issue: #1
contract_impact: yes
spec_update: updated
docs_update: updated
gate_impact: gate:G1
evidence: tests
rollback_plan: revert commit
## Quantitative Summary
- tests_passed: 1
""",
    )
    checks.check_gate_eligibility(ctx)


def test_gate_eligibility_accepts_quant_summary_field() -> None:
    ctx = _context(
        labels=["gate:G1"],
        body="""
linked_issue: #1
contract_impact: yes
spec_update: updated
docs_update: updated
gate_impact: gate:G1
evidence: tests
rollback_plan: revert commit
quant_summary: tests_passed=1, coverage_pct=90.0
""",
    )
    checks.check_gate_eligibility(ctx)


def test_gate_eligibility_rejects_non_experimental_branch_name() -> None:
    ctx = _context(
        labels=["gate:G1"],
        body="""
linked_issue: #1
contract_impact: yes
spec_update: updated
docs_update: updated
gate_impact: gate:G1
evidence: tests
rollback_plan: revert commit
## Quantitative Summary
- tests_passed: 1
""",
        branch_name="feature/runtime-orchestration",
    )
    with pytest.raises(SystemExit):
        checks.check_gate_eligibility(ctx)


def test_no_active_conflict_claim_skips_when_not_in_review() -> None:
    ctx = _context(
        labels=["gate:G1", "axis:runtime-orchestration"],
        body="linked_issue: #1",
    )
    checks.check_no_active_conflict_claim(ctx)


def test_experimental_branch_prefix_matches_project_contract() -> None:
    valid_branch = "codex/multi-agent-test/123-story01"
    assert checks.BRANCH_PATTERN.fullmatch(valid_branch) is not None
