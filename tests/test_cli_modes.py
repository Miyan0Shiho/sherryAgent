from __future__ import annotations

import json

from click.testing import CliRunner

import pytest

from src.sherry_agent.cli import main as cli_main

pytestmark = [pytest.mark.metrics]


def test_story02_cli_outputs_autonomous_safe_payload() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        ["story02", "--goal", "generate a daily summary", "--trigger-source", "cron"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["task"]["mode"] == "autonomous-safe"
    assert payload["run"]["status"] == "waiting_confirmation"
    assert payload["output"]["execution_mode"] == "dry-run"


def test_story03_cli_outputs_background_ops_payload() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        [
            "story03",
            "--goal",
            "investigate and remediate an incident",
            "--repo",
            "sherryAgent",
            "--incident-id",
            "inc-002",
            "--apply-fix",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["task"]["mode"] == "background-ops"
    assert payload["run"]["status"] == "blocked"
    assert payload["output"]["blocked_reason"] == "policy_block"


def test_story04_cli_outputs_bulk_analysis_payload() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        [
            "story04",
            "--goal",
            "run a repository audit across many targets",
            "--target",
            "repo-a",
            "--target",
            "repo-b",
            "--target",
            "repo-c",
            "--target",
            "repo-d",
            "--shard-size",
            "2",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["task"]["mode"] == "bulk-analysis"
    assert payload["output"]["shard_count"] == 2
    assert len(payload["output"]["aggregated_findings"]) == 2
