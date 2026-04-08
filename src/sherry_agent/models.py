from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


TASK_STATUSES = {
    "created",
    "planned",
    "running",
    "waiting_confirmation",
    "completed",
    "blocked",
    "failed",
    "cancelled",
}
RISK_LEVELS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
BUDGET_PROFILES = {"strict", "balanced", "premium"}
EVIDENCE_CONFIDENCE = {"high", "medium", "low"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass(slots=True)
class Task:
    source: str
    goal: str
    priority: int
    risk_level: str
    budget_profile: str
    mode: str
    status: str
    idempotency_key: str
    task_id: str = field(default_factory=lambda: generate_id("task"))
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.status not in TASK_STATUSES:
            raise ValueError(f"invalid task status: {self.status}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"invalid risk level: {self.risk_level}")
        if self.budget_profile not in BUDGET_PROFILES:
            raise ValueError(f"invalid budget profile: {self.budget_profile}")

    def transition(self, status: str) -> None:
        if status not in TASK_STATUSES:
            raise ValueError(f"invalid task status: {status}")
        self.status = status
        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class Run:
    task_id: str
    plan_version: str
    model_profile: str
    toolset: list[str]
    outcome: str
    status: str
    run_id: str = field(default_factory=lambda: generate_id("run"))
    started_at: datetime = field(default_factory=utc_now)
    ended_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.status not in TASK_STATUSES:
            raise ValueError(f"invalid run status: {self.status}")

    def finish(self, outcome: str, status: str) -> None:
        if status not in TASK_STATUSES:
            raise ValueError(f"invalid run status: {status}")
        self.outcome = outcome
        self.status = status
        self.ended_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class Evidence:
    run_id: str
    source_type: str
    source_ref: str
    summary: str
    confidence: str
    evidence_id: str = field(default_factory=lambda: generate_id("evidence"))
    captured_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.confidence not in EVIDENCE_CONFIDENCE:
            raise ValueError(f"invalid confidence: {self.confidence}")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class Decision:
    run_id: str
    decision_type: str
    policy_basis: str
    requires_human: bool
    approved_by: str | None
    reason: str
    decision_id: str = field(default_factory=lambda: generate_id("decision"))
    created_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class CostRecord:
    run_id: str
    token_in: int
    token_out: int
    tool_calls: int
    latency_ms: int
    cache_hit: bool
    estimated_cost: float
    recorded_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class ResultPack:
    task: Task
    run: Run
    evidence: list[Evidence]
    decisions: list[Decision]
    cost_record: CostRecord
    result_summary: str
    output: dict[str, Any]

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    @property
    def decision_count(self) -> int:
        return len(self.decisions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task.to_dict(),
            "run": self.run.to_dict(),
            "evidence": [item.to_dict() for item in self.evidence],
            "decisions": [item.to_dict() for item in self.decisions],
            "cost_record": self.cost_record.to_dict(),
            "result_summary": self.result_summary,
            "output": _serialize(self.output),
        }


def _serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    return value
