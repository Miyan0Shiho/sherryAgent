from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from time import perf_counter

import pytest

from tests.support.metrics import build_metrics_summary, write_metrics_json


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--metrics-json",
        action="store",
        default=None,
        help="Write a JSON metrics summary to this path after the test session.",
    )
    parser.addoption(
        "--coverage-xml",
        action="store",
        default=None,
        help="Optional coverage XML path used to populate metrics summary.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "contract: contract-level schema and interface checks")
    config.addinivalue_line("markers", "governance: governance and policy checks")
    config.addinivalue_line("markers", "story01: Story-01 acceptance and runtime coverage")
    config.addinivalue_line("markers", "story05: Story-05 acceptance and runtime coverage")
    config.addinivalue_line("markers", "metrics: measurable harness helper checks")
    config.addinivalue_line(
        "markers",
        "decision_replay: tests that exercise evidence/decision replay assertions",
    )
    config._sherry_started_at = perf_counter()  # type: ignore[attr-defined]
    config._sherry_marker_map = {}  # type: ignore[attr-defined]
    config._sherry_outcomes = defaultdict(float)  # type: ignore[attr-defined]
    config._sherry_marker_counts = Counter()  # type: ignore[attr-defined]


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    marker_map = {}
    for item in items:
        marker_map[item.nodeid] = {mark.name for mark in item.iter_markers()}
    config._sherry_marker_map = marker_map  # type: ignore[attr-defined]
    config._sherry_outcomes["collected"] = len(items)  # type: ignore[attr-defined,index]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    config = item.config
    config._sherry_outcomes[report.outcome] += 1  # type: ignore[attr-defined,index]
    config._sherry_outcomes["duration_seconds"] += report.duration  # type: ignore[attr-defined,index]

    markers = config._sherry_marker_map.get(item.nodeid, set())  # type: ignore[attr-defined]
    if report.outcome == "passed":
        for marker in ("story01", "story05", "governance", "contract", "decision_replay"):
            if marker in markers:
                config._sherry_marker_counts[f"{marker}_passed"] += 1  # type: ignore[attr-defined,index]


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    metrics_path = session.config.getoption("--metrics-json")
    if not metrics_path:
        return

    coverage_xml = session.config.getoption("--coverage-xml")
    if not coverage_xml:
        default_coverage = Path("build/coverage.xml")
        coverage_xml = str(default_coverage) if default_coverage.exists() else None
    summary = build_metrics_summary(
        tests_collected=int(session.config._sherry_outcomes.get("collected", 0)),  # type: ignore[attr-defined]
        tests_passed=int(session.config._sherry_outcomes.get("passed", 0)),  # type: ignore[attr-defined]
        tests_failed=int(session.config._sherry_outcomes.get("failed", 0)),  # type: ignore[attr-defined]
        tests_skipped=int(session.config._sherry_outcomes.get("skipped", 0)),  # type: ignore[attr-defined]
        duration_seconds=float(session.config._sherry_outcomes.get("duration_seconds", 0.0)),  # type: ignore[attr-defined]
        marker_counts=dict(session.config._sherry_marker_counts),  # type: ignore[attr-defined]
        coverage_xml_path=coverage_xml,
    )
    write_metrics_json(Path(metrics_path), summary)
