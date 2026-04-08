from __future__ import annotations

import json

import click

from .governance import GateRequest, run_release_gate
from .runtime import InteractiveDevRequest, run_interactive_dev


@click.group()
def main() -> None:
    """Minimal CLI for the first SherryAgent implementation experiment."""


@main.command("story01")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--risk-level", default="LOW", show_default=True)
@click.option("--simulate-budget-exhausted", is_flag=True, default=False)
def story01(source: str, goal: str, risk_level: str, simulate_budget_exhausted: bool) -> None:
    result = run_interactive_dev(
        InteractiveDevRequest(
            source=source,
            goal=goal,
            risk_level=risk_level,
            simulate_budget_exhausted=simulate_budget_exhausted,
            request_id=f"{source}:{goal}",
        )
    )
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@main.command("story05")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--repo", required=True)
@click.option("--required-check", "required_checks", multiple=True)
@click.option("--rollback-plan", default=None)
@click.option("--risk-level", default="LOW", show_default=True)
@click.option("--simulate-high-risk", is_flag=True, default=False)
def story05(
    source: str,
    goal: str,
    repo: str,
    required_checks: tuple[str, ...],
    rollback_plan: str | None,
    risk_level: str,
    simulate_high_risk: bool,
) -> None:
    checks = list(required_checks) or ["Spec-Docs Sync", "Gate Eligibility (G1-G4)"]
    result = run_release_gate(
        GateRequest(
            source=source,
            goal=goal,
            repo=repo,
            required_checks=checks,
            rollback_plan=rollback_plan,
            risk_level=risk_level,
            request_id=f"{source}:{repo}:{goal}",
            simulate_high_risk=simulate_high_risk,
        )
    )
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
