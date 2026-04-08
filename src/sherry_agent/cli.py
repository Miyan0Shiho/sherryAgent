from __future__ import annotations

import json

import click

from .autonomous import AutonomousSafeRequest, BackgroundOpsRequest, run_autonomous_safe, run_background_ops
from .bulk import BulkAnalysisRequest, run_bulk_analysis
from .governance import GateRequest, run_release_gate
from .runtime import InteractiveDevRequest, run_interactive_dev


@click.group()
def main() -> None:
    """CLI for the SherryAgent multi-mode delivery program."""


@main.command("story01")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--risk-level", default="LOW", show_default=True)
@click.option("--simulate-budget-exhausted", is_flag=True, default=False)
def story01(source: str, goal: str, risk_level: str, simulate_budget_exhausted: bool) -> None:
    result = run_interactive_dev(InteractiveDevRequest(source=source, goal=goal, risk_level=risk_level, simulate_budget_exhausted=simulate_budget_exhausted, request_id=f"{source}:{goal}"))
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@main.command("story02")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--trigger-source", default="cron", show_default=True)
@click.option("--risk-level", default="LOW", show_default=True)
@click.option("--real-run", is_flag=True, default=False)
def story02(source: str, goal: str, trigger_source: str, risk_level: str, real_run: bool) -> None:
    result = run_autonomous_safe(AutonomousSafeRequest(source=source, goal=goal, trigger_source=trigger_source, risk_level=risk_level, real_run=real_run, request_id=f"{source}:{trigger_source}:{goal}"))
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@main.command("story03")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--repo", required=True)
@click.option("--incident-id", required=True)
@click.option("--trigger-source", default="event", show_default=True)
@click.option("--risk-level", default="MEDIUM", show_default=True)
@click.option("--apply-fix", is_flag=True, default=False)
@click.option("--simulate-destructive-fix", is_flag=True, default=False)
def story03(source: str, goal: str, repo: str, incident_id: str, trigger_source: str, risk_level: str, apply_fix: bool, simulate_destructive_fix: bool) -> None:
    result = run_background_ops(
        BackgroundOpsRequest(
            source=source,
            goal=goal,
            repo=repo,
            incident_id=incident_id,
            trigger_source=trigger_source,
            risk_level=risk_level,
            apply_fix=apply_fix,
            simulate_destructive_fix=simulate_destructive_fix,
            request_id=f"{source}:{incident_id}:{repo}",
        )
    )
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@main.command("story04")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--target", "targets", multiple=True, required=True)
@click.option("--risk-level", default="LOW", show_default=True)
@click.option("--shard-size", default=3, show_default=True, type=int)
def story04(source: str, goal: str, targets: tuple[str, ...], risk_level: str, shard_size: int) -> None:
    result = run_bulk_analysis(BulkAnalysisRequest(source=source, goal=goal, targets=list(targets), risk_level=risk_level, shard_size=shard_size, request_id=f"{source}:{goal}"))
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@main.command("story05")
@click.option("--source", default="cli", show_default=True)
@click.option("--goal", required=True)
@click.option("--repo", required=True)
@click.option("--required-check", "required_checks", multiple=True)
@click.option("--rollback-plan", default=None)
@click.option("--risk-level", default="LOW", show_default=True)
@click.option("--simulate-high-risk", is_flag=True, default=False)
def story05(source: str, goal: str, repo: str, required_checks: tuple[str, ...], rollback_plan: str | None, risk_level: str, simulate_high_risk: bool) -> None:
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
