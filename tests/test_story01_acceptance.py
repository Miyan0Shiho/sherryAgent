from __future__ import annotations

import json
from click.testing import CliRunner

import pytest

from src.sherry_agent.cli import main as cli_main

pytestmark = [pytest.mark.story01]


def test_story01_cli_entrypoint_produces_result_pack() -> None:
    runner = CliRunner()
    result = runner.invoke(cli_main, ["story01", "--goal", "Create a command"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["task"]["mode"] == "interactive-dev"
    assert payload["run"]["status"] == "completed"
    assert payload["evidence"]
    assert payload["decisions"]
    assert payload["cost_record"]["run_id"] == payload["run"]["run_id"]


def test_story01_cli_budget_exhaustion_blocks_and_reports() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        ["story01", "--goal", "Create a command", "--simulate-budget-exhausted"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["run"]["status"] == "blocked"
    assert payload["output"]["blocked_reason"] == "budget_exhausted"
