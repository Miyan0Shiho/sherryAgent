from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


TASK_STATUSES = (
    "created",
    "planned",
    "running",
    "waiting_confirmation",
    "blocked",
    "completed",
    "failed",
    "cancelled",
)
TERMINAL_TASK_STATUSES = {"blocked", "completed", "failed", "cancelled"}
TASK_TRANSITIONS = {
    "created": {"planned", "cancelled"},
    "planned": {"running", "blocked", "cancelled"},
    "running": {"waiting_confirmation", "blocked", "completed", "failed", "cancelled"},
    "waiting_confirmation": {"running", "blocked", "cancelled"},
    "blocked": {"running", "cancelled"},
    "completed": set(),
    "failed": set(),
    "cancelled": set(),
}
RUN_STATUSES = TASK_STATUSES
RISK_LEVELS = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
BUDGET_PROFILES = ("strict", "balanced", "premium")
RUN_MODES = (
    "interactive-dev",
    "autonomous-safe",
    "background-ops",
    "bulk-analysis",
)
EVIDENCE_CONFIDENCE = ("high", "medium", "low")
DECISION_TYPES = ("allow", "block", "require_confirmation")
MEMORY_KINDS = ("session", "summary", "knowledge", "inference")
TRIGGER_KINDS = ("manual", "scheduled", "event", "incident")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _ensure_member(value: str, allowed: tuple[str, ...] | set[str], label: str) -> None:
    if value not in allowed:
        raise ValueError(f"invalid {label}: {value}")


def _ensure_mode(value: str) -> None:
    _ensure_member(value, RUN_MODES, "mode")


def _serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    return value


def _deserialize_mapping(data: Mapping[str, Any], *, datetime_fields: set[str] | tuple[str, ...] = ()) -> dict[str, Any]:
    payload = dict(data)
    for key in datetime_fields:
        value = payload.get(key)
        if isinstance(value, str):
            payload[key] = datetime.fromisoformat(value)
    return payload


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
    owner: str = "system"
    task_id: str = field(default_factory=lambda: generate_id("task"))
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        _ensure_member(self.status, TASK_STATUSES, "task status")
        _ensure_member(self.risk_level, RISK_LEVELS, "risk level")
        _ensure_member(self.budget_profile, BUDGET_PROFILES, "budget profile")
        _ensure_mode(self.mode)

    def transition(self, status: str) -> None:
        _ensure_member(status, TASK_STATUSES, "task status")
        allowed = TASK_TRANSITIONS[self.status]
        if status != self.status and status not in allowed:
            raise ValueError(f"illegal task transition: {self.status} -> {status}")
        self.status = status
        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MemoryRecord":
        return cls(**_deserialize_mapping(data, datetime_fields={"created_at", "expires_at"}))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Evidence":
        return cls(**_deserialize_mapping(data, datetime_fields={"captured_at"}))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Task":
        return cls(**_deserialize_mapping(data, datetime_fields={"created_at", "updated_at"}))


@dataclass(slots=True)
class Plan:
    mode: str
    budget_profile: str
    toolset: list[str]
    steps: list[str]
    model_profile: str
    approval_requirements: list[str] = field(default_factory=list)
    plan_version: str = "v2"
    max_parallelism: int = 1

    def __post_init__(self) -> None:
        _ensure_mode(self.mode)
        _ensure_member(self.budget_profile, BUDGET_PROFILES, "budget profile")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TriggerEvent":
        return cls(**_deserialize_mapping(data, datetime_fields={"scheduled_for", "created_at", "dispatched_at", "completed_at"}))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Decision":
        return cls(**_deserialize_mapping(data, datetime_fields={"created_at"}))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Plan":
        return cls(**_deserialize_mapping(data))


@dataclass(slots=True)
class Run:
    task_id: str
    plan_version: str
    model_profile: str
    toolset: list[str]
    outcome: str
    status: str
    mode: str = "interactive-dev"
    run_id: str = field(default_factory=lambda: generate_id("run"))
    started_at: datetime = field(default_factory=utc_now)
    ended_at: datetime | None = None

    def __post_init__(self) -> None:
        _ensure_member(self.status, RUN_STATUSES, "run status")
        _ensure_mode(self.mode)

    def transition(self, status: str, outcome: str | None = None) -> None:
        _ensure_member(status, RUN_STATUSES, "run status")
        allowed = TASK_TRANSITIONS[self.status]
        if status != self.status and status not in allowed:
            raise ValueError(f"illegal run transition: {self.status} -> {status}")
        if status in TERMINAL_TASK_STATUSES:
            self.ended_at = utc_now()
        self.status = status
        if outcome is not None:
            self.outcome = outcome

    def finish(self, outcome: str, status: str) -> None:
        self.transition(status=status, outcome=outcome)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ReleaseGateResult":
        return cls(**_deserialize_mapping(data))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ToolCall":
        return cls(**_deserialize_mapping(data, datetime_fields={"created_at"}))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Run":
        return cls(**_deserialize_mapping(data, datetime_fields={"started_at", "ended_at"}))


@dataclass(slots=True)
class Evidence:
    run_id: str
    source_type: str
    source_ref: str
    summary: str
    confidence: str
    content: str | None = None
    is_inference: bool = False
    evidence_id: str = field(default_factory=lambda: generate_id("evidence"))
    captured_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        _ensure_member(self.confidence, EVIDENCE_CONFIDENCE, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CostRecord":
        return cls(**_deserialize_mapping(data, datetime_fields={"recorded_at"}))


@dataclass(slots=True)
class Decision:
    run_id: str
    decision_type: str
    policy_basis: str
    requires_human: bool
    approved_by: str | None
    reason: str
    target: str = ""
    decision_id: str = field(default_factory=lambda: generate_id("decision"))
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        _ensure_member(self.decision_type, DECISION_TYPES, "decision type")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class ToolCall:
    run_id: str
    tool_name: str
    target: str
    mode: str
    risk_level: str
    arguments: dict[str, Any] = field(default_factory=dict)
    is_write: bool = False
    is_destructive: bool = False
    approved_by: str | None = None
    outcome: str = "pending"
    metadata: dict[str, Any] = field(default_factory=dict)
    tool_call_id: str = field(default_factory=lambda: generate_id("toolcall"))
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
    degraded_mode: str | None = None
    retries: int = 0
    recorded_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class MemoryRecord:
    scope: str
    task_id: str = ""
    run_id: str = ""
    kind: str = "session"
    key: str = ""
    value: str = ""
    content: str | None = None
    story: str | None = None
    relevance: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    source_evidence_id: str | None = None
    ttl_seconds: int | None = None
    version: str = "v1"
    memory_id: str = field(default_factory=lambda: generate_id("memory"))
    created_at: datetime = field(default_factory=utc_now)
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        _ensure_member(self.kind, MEMORY_KINDS, "memory kind")
        if self.content and not self.value:
            self.value = self.content
        if not self.key:
            self.key = self.scope
        if not 0.0 <= self.relevance <= 1.0:
            raise ValueError("relevance must be between 0.0 and 1.0")

    def is_expired(self, now: datetime | None = None) -> bool:
        if self.expires_at is None:
            return False
        current = now or utc_now()
        return self.expires_at <= current

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class TriggerEvent:
    trigger_kind: str
    trigger_ref: str
    payload: dict[str, Any]
    task_id: str = ""
    run_id: str = ""
    status: str = "queued"
    scheduled_for: datetime = field(default_factory=utc_now)
    trigger_id: str = field(default_factory=lambda: generate_id("trigger"))
    created_at: datetime = field(default_factory=utc_now)
    dispatched_at: datetime | None = None
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        _ensure_member(self.trigger_kind, TRIGGER_KINDS, "trigger kind")

    def mark_dispatched(self) -> None:
        self.status = "dispatched"
        self.dispatched_at = utc_now()

    def mark_completed(self, status: str = "completed") -> None:
        self.status = status
        self.completed_at = utc_now()

    def is_due(self, now: datetime | None = None) -> bool:
        probe = now or utc_now()
        return self.status == "queued" and self.scheduled_for <= probe

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class ReleaseGateResult:
    gate_result: str
    required_checks: list[str]
    evidence_links: list[str]
    rollback_plan: str | None
    runbook: list[str]
    gate_id: str = field(default_factory=lambda: generate_id("gate"))

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass(slots=True)
class ResultPack:
    task: Task
    run: Run
    plan: Plan
    evidence: list[Evidence]
    decisions: list[Decision]
    cost_record: CostRecord
    tool_calls: list[ToolCall]
    memory_records: list[MemoryRecord]
    trigger_events: list[TriggerEvent]
    result_summary: str
    output: dict[str, Any]
    release_gate: ReleaseGateResult | None = None

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    @property
    def decision_count(self) -> int:
        return len(self.decisions)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "task": self.task.to_dict(),
            "run": self.run.to_dict(),
            "plan": self.plan.to_dict(),
            "evidence": [item.to_dict() for item in self.evidence],
            "decisions": [item.to_dict() for item in self.decisions],
            "cost_record": self.cost_record.to_dict(),
            "tool_calls": [item.to_dict() for item in self.tool_calls],
            "memory_records": [item.to_dict() for item in self.memory_records],
            "trigger_events": [item.to_dict() for item in self.trigger_events],
            "result_summary": self.result_summary,
            "output": _serialize(self.output),
        }
        if self.release_gate is not None:
            payload["release_gate"] = self.release_gate.to_dict()
            payload["gate_result"] = self.release_gate.gate_result
        return payload


def _from_mapping(cls: type[Any], data: Mapping[str, Any], datetime_fields: set[str]) -> Any:
    payload = dict(data)
    for key in datetime_fields:
        value = payload.get(key)
        if isinstance(value, str):
            payload[key] = datetime.fromisoformat(value)
    return cls(**payload)


Task.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"created_at", "updated_at"}))  # type: ignore[attr-defined]
Plan.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, set()))  # type: ignore[attr-defined]
Run.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"started_at", "ended_at"}))  # type: ignore[attr-defined]
Evidence.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"captured_at"}))  # type: ignore[attr-defined]
Decision.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"created_at"}))  # type: ignore[attr-defined]
ToolCall.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"created_at"}))  # type: ignore[attr-defined]
CostRecord.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"recorded_at"}))  # type: ignore[attr-defined]
MemoryRecord.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"created_at", "expires_at"}))  # type: ignore[attr-defined]
TriggerEvent.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, {"scheduled_for", "created_at", "dispatched_at", "completed_at"}))  # type: ignore[attr-defined]
ReleaseGateResult.from_dict = classmethod(lambda cls, data: _from_mapping(cls, data, set()))  # type: ignore[attr-defined]
ResultPack.from_dict = classmethod(
    lambda cls, data: cls(
        task=Task.from_dict(data["task"]),
        run=Run.from_dict(data["run"]),
        plan=Plan.from_dict(data["plan"]),
        evidence=[Evidence.from_dict(item) for item in data.get("evidence", [])],
        decisions=[Decision.from_dict(item) for item in data.get("decisions", [])],
        cost_record=CostRecord.from_dict(data["cost_record"]),
        tool_calls=[ToolCall.from_dict(item) for item in data.get("tool_calls", [])],
        memory_records=[MemoryRecord.from_dict(item) for item in data.get("memory_records", [])],
        trigger_events=[TriggerEvent.from_dict(item) for item in data.get("trigger_events", [])],
        result_summary=data["result_summary"],
        output=data.get("output", {}),
        release_gate=ReleaseGateResult.from_dict(data["release_gate"]) if data.get("release_gate") else None,
    )
)  # type: ignore[attr-defined]
