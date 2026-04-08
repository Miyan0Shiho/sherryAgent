from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping
from xml.etree import ElementTree as ET


@dataclass(slots=True)
class MetricsSummary:
    tests_collected: int
    tests_passed: int
    tests_failed: int
    tests_skipped: int
    story_cases_passed: int
    story01_cases_passed: int
    story02_cases_passed: int
    story03_cases_passed: int
    story04_cases_passed: int
    story05_cases_passed: int
    governance_checks_passed: int
    contract_checks_passed: int
    runtime_checks_passed: int
    policy_checks_passed: int
    persistence_checks_passed: int
    memory_checks_passed: int
    cost_checks_passed: int
    decision_replay_coverage: float
    coverage_pct: float | None
    duration_seconds: float


def parse_coverage_pct(coverage_xml_path: str | Path | None) -> float | None:
    if coverage_xml_path is None:
        return None

    path = Path(coverage_xml_path)
    if not path.exists():
        return None

    root = ET.parse(path).getroot()
    line_rate = root.attrib.get("line-rate")
    if line_rate is None:
        return None
    return round(float(line_rate) * 100.0, 2)


def build_metrics_summary(
    *,
    tests_collected: int,
    tests_passed: int,
    tests_failed: int,
    tests_skipped: int,
    duration_seconds: float,
    marker_counts: Mapping[str, int],
    coverage_xml_path: str | Path | None = None,
) -> MetricsSummary:
    story01_cases_passed = marker_counts.get("story01_passed", 0)
    story02_cases_passed = marker_counts.get("story02_passed", 0)
    story03_cases_passed = marker_counts.get("story03_passed", 0)
    story04_cases_passed = marker_counts.get("story04_passed", 0)
    story05_cases_passed = marker_counts.get("story05_passed", 0)
    story_cases_passed = (
        story01_cases_passed
        + story02_cases_passed
        + story03_cases_passed
        + story04_cases_passed
        + story05_cases_passed
    )
    governance_checks_passed = marker_counts.get("governance_passed", 0)
    contract_checks_passed = marker_counts.get("contract_passed", 0)
    runtime_checks_passed = marker_counts.get("runtime_passed", 0)
    policy_checks_passed = marker_counts.get("policy_passed", 0)
    persistence_checks_passed = marker_counts.get("persistence_passed", 0)
    memory_checks_passed = marker_counts.get("memory_passed", 0)
    cost_checks_passed = marker_counts.get("cost_passed", 0)
    decision_replay_passed = marker_counts.get("decision_replay_passed", 0)
    decision_replay_coverage = round(
        (decision_replay_passed / tests_passed) * 100.0,
        2,
    ) if tests_passed else 0.0

    return MetricsSummary(
        tests_collected=tests_collected,
        tests_passed=tests_passed,
        tests_failed=tests_failed,
        tests_skipped=tests_skipped,
        story_cases_passed=story_cases_passed,
        story01_cases_passed=story01_cases_passed,
        story02_cases_passed=story02_cases_passed,
        story03_cases_passed=story03_cases_passed,
        story04_cases_passed=story04_cases_passed,
        story05_cases_passed=story05_cases_passed,
        governance_checks_passed=governance_checks_passed,
        contract_checks_passed=contract_checks_passed,
        runtime_checks_passed=runtime_checks_passed,
        policy_checks_passed=policy_checks_passed,
        persistence_checks_passed=persistence_checks_passed,
        memory_checks_passed=memory_checks_passed,
        cost_checks_passed=cost_checks_passed,
        decision_replay_coverage=decision_replay_coverage,
        coverage_pct=parse_coverage_pct(coverage_xml_path),
        duration_seconds=round(duration_seconds, 4),
    )


def write_metrics_json(path: Path, summary: MetricsSummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n", encoding="utf-8")
