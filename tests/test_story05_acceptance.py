from __future__ import annotations

import json

from click.testing import CliRunner
import pytest

from src.sherry_agent.cli import main as cli_main

pytestmark = [pytest.mark.story05, pytest.mark.governance]


def test_story05_cli_entrypoint_produces_gate_result() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        [
            "story05",
            "--goal",
            "Scan repo for release readiness",
            "--repo",
            "sherryAgent",
            "--rollback-plan",
            "restore prior state",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["gate_result"] == "pass"
    assert payload["output"]["rollback_plan"] == "restore prior state"
    assert payload["evidence"]
    assert payload["decisions"]


def test_story05_cli_missing_rollback_plan_blocks_gate() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        [
            "story05",
            "--goal",
            "Scan repo for release readiness",
            "--repo",
            "sherryAgent",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["gate_result"] == "block"
    assert payload["output"]["blocked_reason"] == "missing_rollback_plan"
