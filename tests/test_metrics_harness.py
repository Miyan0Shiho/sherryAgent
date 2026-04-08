from __future__ import annotations

from pathlib import Path

import pytest

from tests.support.metrics import build_metrics_summary, parse_coverage_pct, write_metrics_json

pytestmark = [pytest.mark.metrics]


def test_parse_coverage_pct_reads_line_rate(tmp_path: Path) -> None:
    coverage_xml = tmp_path / "coverage.xml"
    coverage_xml.write_text(
        """<?xml version="1.0" ?>
<coverage line-rate="0.875" branch-rate="0.0" version="7.4">
</coverage>
""",
        encoding="utf-8",
    )

    assert parse_coverage_pct(coverage_xml) == 87.5


def test_build_metrics_summary_aggregates_marker_counts(tmp_path: Path) -> None:
    coverage_xml = tmp_path / "coverage.xml"
    coverage_xml.write_text(
        """<?xml version="1.0" ?>
<coverage line-rate="0.9" branch-rate="0.0" version="7.4">
</coverage>
""",
        encoding="utf-8",
    )

    summary = build_metrics_summary(
        tests_collected=5,
        tests_passed=4,
        tests_failed=1,
        tests_skipped=0,
        duration_seconds=1.2345,
        marker_counts={
            "story01_passed": 2,
            "story05_passed": 1,
            "governance_passed": 3,
            "contract_passed": 4,
            "decision_replay_passed": 2,
        },
        coverage_xml_path=coverage_xml,
    )

    assert summary.tests_collected == 5
    assert summary.tests_passed == 4
    assert summary.story_cases_passed == 3
    assert summary.governance_checks_passed == 3
    assert summary.contract_checks_passed == 4
    assert summary.decision_replay_coverage == 50.0
    assert summary.coverage_pct == 90.0


def test_write_metrics_json_persists_summary(tmp_path: Path) -> None:
    summary = build_metrics_summary(
        tests_collected=1,
        tests_passed=1,
        tests_failed=0,
        tests_skipped=0,
        duration_seconds=0.25,
        marker_counts={"decision_replay_passed": 1},
        coverage_xml_path=None,
    )
    output = tmp_path / "metrics.json"
    write_metrics_json(output, summary)

    payload = output.read_text(encoding="utf-8")
    assert '"tests_passed": 1' in payload
    assert '"decision_replay_coverage": 100.0' in payload
