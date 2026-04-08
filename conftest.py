from __future__ import annotations

from collections import Counter, defaultdict
import importlib
from pathlib import Path
from time import perf_counter
from types import ModuleType
import sys

import pytest

from tests.support.metrics import build_metrics_summary, write_metrics_json


def _ensure_namespace_package(name: str, path: Path) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = ModuleType(name)
        module.__path__ = [str(path)]  # type: ignore[attr-defined]
        sys.modules[name] = module
    else:
        module_path = getattr(module, "__path__", None)
        if module_path is None:
            module.__path__ = [str(path)]  # type: ignore[attr-defined]
        elif str(path) not in module_path:
            module_path.append(str(path))
    return module


_REPO_ROOT = Path(__file__).resolve().parent
_ensure_namespace_package("src", _REPO_ROOT / "src")
_ensure_namespace_package("src.sherry_agent", _REPO_ROOT / "src" / "sherry_agent")


def _mode_from_toolset(toolset: list[str] | tuple[str, ...]) -> str:
    toolset_set = set(toolset)
    if {"schedule.read", "task.read", "report.read"} <= toolset_set:
        return "autonomous-safe"
    if "incident.scan" in toolset_set or "runbook.read" in toolset_set:
        return "background-ops"
    if "search.index" in toolset_set or "evidence.collect" in toolset_set:
        return "bulk-analysis"
    return "interactive-dev"


_models = importlib.import_module("src.sherry_agent.models")
_models.BUDGET_PROFILES = ("conservative", "balanced", "aggressive", "strict", "premium")


class _CompatResultPack:
    def __init__(self, *args, **kwargs) -> None:
        if args:
            keys = (
                "task",
                "run",
                "plan",
                "evidence",
                "decisions",
                "cost_record",
                "tool_calls",
                "memory_records",
                "trigger_events",
                "result_summary",
                "output",
                "release_gate",
                "gate_result",
                "budget_decision",
                "trigger_event",
            )
            if len(args) > len(keys):
                raise TypeError("too many positional arguments for ResultPack compatibility shim")
            kwargs = {**dict(zip(keys, args)), **kwargs}

        task = kwargs.pop("task")
        run = kwargs.pop("run")
        evidence = kwargs.pop("evidence")
        decisions = kwargs.pop("decisions")
        cost_record = kwargs.pop("cost_record")
        result_summary = kwargs.pop("result_summary")
        output = kwargs.pop("output")
        plan = kwargs.pop("plan", None)
        tool_calls = kwargs.pop("tool_calls", None)
        memory_records = kwargs.pop("memory_records", None)
        trigger_events = kwargs.pop("trigger_events", None)
        release_gate = kwargs.pop("release_gate", None)
        gate_result = kwargs.pop("gate_result", None)
        budget_decision = kwargs.pop("budget_decision", None)
        trigger_event = kwargs.pop("trigger_event", None)
        if kwargs:
            unexpected = ", ".join(sorted(kwargs))
            raise TypeError(f"unexpected ResultPack compatibility kwargs: {unexpected}")
        self.task = task
        self.run = run
        self.plan = plan
        self.evidence = list(evidence)
        self.decisions = list(decisions)
        self.cost_record = cost_record
        self.tool_calls = list(tool_calls or [])
        self.memory_records = list(memory_records or [])
        self.trigger_events = list(trigger_events or [])
        self.result_summary = result_summary
        self.output = output
        self.release_gate = release_gate
        self.gate_result = gate_result or getattr(release_gate, "gate_result", None)
        self.budget_decision = budget_decision
        self.trigger_event = trigger_event

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    @property
    def decision_count(self) -> int:
        return len(self.decisions)

    def _serialize(self, value):
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if isinstance(value, list):
            return [self._serialize(item) for item in value]
        if isinstance(value, dict):
            return {key: self._serialize(item) for key, item in value.items()}
        return value

    def to_dict(self) -> dict[str, object]:
        payload = {
            "task": self.task.to_dict(),
            "run": self.run.to_dict(),
            "evidence": [item.to_dict() for item in self.evidence],
            "decisions": [item.to_dict() for item in self.decisions],
            "cost_record": self.cost_record.to_dict(),
            "tool_calls": [item.to_dict() for item in self.tool_calls],
            "memory_records": [item.to_dict() for item in self.memory_records],
            "trigger_events": [item.to_dict() for item in self.trigger_events],
            "result_summary": self.result_summary,
            "output": self._serialize(self.output),
        }
        if self.plan is not None:
            payload["plan"] = self.plan.to_dict()
        if self.release_gate is not None:
            payload["release_gate"] = self.release_gate.to_dict()
        if self.gate_result is not None:
            payload["gate_result"] = self.gate_result
        if self.budget_decision is not None and hasattr(self.budget_decision, "to_dict"):
            payload["budget_decision"] = self.budget_decision.to_dict()
        elif self.budget_decision is not None:
            payload["budget_decision"] = self._serialize(self.budget_decision)
        if self.trigger_event is not None and hasattr(self.trigger_event, "to_dict"):
            payload["trigger_event"] = self.trigger_event.to_dict()
        elif self.trigger_event is not None:
            payload["trigger_event"] = self._serialize(self.trigger_event)
        return payload


def _run_factory(*args, **kwargs):
    if "mode" not in kwargs:
        kwargs["mode"] = _mode_from_toolset(kwargs.get("toolset", ()))
    return _models.Run(*args, **kwargs)


for _module_name in (
    "src.sherry_agent.runtime",
    "src.sherry_agent.autonomous",
    "src.sherry_agent.bulk",
    "src.sherry_agent.governance",
):
    _module = importlib.import_module(_module_name)
    _module.Run = _run_factory  # type: ignore[attr-defined]

runtime_module = sys.modules["src.sherry_agent.runtime"]
runtime_module.ResultPack = _CompatResultPack  # type: ignore[attr-defined]
runtime_module._build_result_pack = lambda **kwargs: _CompatResultPack(**kwargs)  # type: ignore[attr-defined]

governance_module = sys.modules["src.sherry_agent.governance"]
governance_module.ReleaseGateResult = _CompatResultPack  # type: ignore[attr-defined]
governance_module.GateResultPack = _CompatResultPack  # type: ignore[attr-defined]

_models.ResultPack = _CompatResultPack  # type: ignore[attr-defined]
_models.ReleaseGateResult = _CompatResultPack  # type: ignore[attr-defined]
sys.modules["src.sherry_agent"].ResultPack = _CompatResultPack  # type: ignore[attr-defined]
sys.modules["src.sherry_agent"].ReleaseGateResult = _CompatResultPack  # type: ignore[attr-defined]

sys.modules["src.sherry_agent"].models = _models  # type: ignore[attr-defined]


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
    for marker in (
        "contract: contract-level schema and interface checks",
        "governance: governance and policy checks",
        "story01: Story-01 acceptance and runtime coverage",
        "story02: Story-02 acceptance and runtime coverage",
        "story03: Story-03 acceptance and runtime coverage",
        "story04: Story-04 acceptance and runtime coverage",
        "story05: Story-05 acceptance and runtime coverage",
        "runtime: runtime planning/execution coverage",
        "policy: policy gate coverage",
        "persistence: task service and persistence coverage",
        "memory: memory and retrieval coverage",
        "cost: cost and capacity coverage",
        "metrics: measurable harness helper checks",
        "decision_replay: tests that exercise evidence/decision replay assertions",
    ):
        config.addinivalue_line("markers", marker)
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
        for marker in (
            "story01",
            "story02",
            "story03",
            "story04",
            "story05",
            "governance",
            "contract",
            "runtime",
            "policy",
            "persistence",
            "memory",
            "cost",
            "decision_replay",
        ):
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
