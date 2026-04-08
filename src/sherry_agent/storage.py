from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .models import (
    CostRecord,
    Decision,
    Evidence,
    MemoryRecord,
    ReleaseGateResult,
    ResultPack,
    Run,
    Task,
    ToolCall,
    TriggerEvent,
)


def _json_default(value: Any) -> Any:
    from datetime import datetime

    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"unsupported value: {value!r}")


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=_json_default)


def _loads(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    payload = json.loads(value)
    return payload if isinstance(payload, dict) else {}


class SherryRepository:
    def __init__(self, database_path: str | Path = ":memory:") -> None:
        self.database_path = str(database_path)
        self._conn = sqlite3.connect(self.database_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self.init_db()

    def close(self) -> None:
        self._conn.close()

    def init_db(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                goal TEXT NOT NULL,
                priority INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                budget_profile TEXT NOT NULL,
                mode TEXT NOT NULL,
                status TEXT NOT NULL,
                idempotency_key TEXT NOT NULL UNIQUE,
                owner TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                plan_version TEXT NOT NULL,
                model_profile TEXT NOT NULL,
                toolset_json TEXT NOT NULL,
                outcome TEXT NOT NULL,
                status TEXT NOT NULL,
                mode TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                payload_json TEXT NOT NULL,
                FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_ref TEXT NOT NULL,
                summary TEXT NOT NULL,
                confidence TEXT NOT NULL,
                content TEXT,
                is_inference INTEGER NOT NULL,
                captured_at TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                FOREIGN KEY(run_id) REFERENCES runs(run_id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                policy_basis TEXT NOT NULL,
                requires_human INTEGER NOT NULL,
                approved_by TEXT,
                reason TEXT NOT NULL,
                target TEXT NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                FOREIGN KEY(run_id) REFERENCES runs(run_id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS cost_records (
                run_id TEXT PRIMARY KEY,
                token_in INTEGER NOT NULL,
                token_out INTEGER NOT NULL,
                tool_calls INTEGER NOT NULL,
                latency_ms INTEGER NOT NULL,
                cache_hit INTEGER NOT NULL,
                estimated_cost REAL NOT NULL,
                degraded_mode TEXT,
                retries INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                FOREIGN KEY(run_id) REFERENCES runs(run_id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS tool_calls (
                tool_call_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                target TEXT NOT NULL,
                mode TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                arguments_json TEXT NOT NULL,
                is_write INTEGER NOT NULL,
                is_destructive INTEGER NOT NULL,
                approved_by TEXT,
                outcome TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS memory_records (
                memory_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                run_id TEXT NOT NULL,
                scope TEXT NOT NULL,
                kind TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                source_evidence_id TEXT,
                ttl_seconds INTEGER,
                version TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS trigger_events (
                trigger_id TEXT PRIMARY KEY,
                trigger_kind TEXT NOT NULL,
                trigger_ref TEXT NOT NULL,
                task_id TEXT NOT NULL,
                run_id TEXT NOT NULL,
                status TEXT NOT NULL,
                scheduled_for TEXT NOT NULL,
                created_at TEXT NOT NULL,
                dispatched_at TEXT,
                completed_at TEXT,
                payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS release_gate_results (
                gate_id TEXT PRIMARY KEY,
                gate_result TEXT NOT NULL,
                required_checks_json TEXT NOT NULL,
                evidence_links_json TEXT NOT NULL,
                rollback_plan TEXT,
                runbook_json TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            """
        )
        self._conn.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
            CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
            CREATE INDEX IF NOT EXISTS idx_runs_task_id ON runs(task_id);
            CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
            CREATE INDEX IF NOT EXISTS idx_evidence_run_id ON evidence(run_id);
            CREATE INDEX IF NOT EXISTS idx_decisions_run_id ON decisions(run_id);
            CREATE INDEX IF NOT EXISTS idx_memory_task_id ON memory_records(task_id);
            CREATE INDEX IF NOT EXISTS idx_trigger_task_id ON trigger_events(task_id);
            """
        )
        self._conn.commit()

    def _upsert(self, table: str, key_column: str, primary_key: str, payload_json: str, **fields: Any) -> None:
        columns = [key_column, *fields.keys(), "payload_json"]
        values = [primary_key, *fields.values(), payload_json]
        placeholders = ", ".join("?" for _ in columns)
        assignments = ", ".join(f"{column}=excluded.{column}" for column in columns[1:])
        self._conn.execute(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) "
            f"ON CONFLICT({key_column}) DO UPDATE SET {assignments}",
            values,
        )
        self._conn.commit()

    def _load_record(self, table: str, key_column: str, key: str) -> dict[str, Any] | None:
        row = self._conn.execute(
            f"SELECT payload_json FROM {table} WHERE {key_column} = ?",
            (key,),
        ).fetchone()
        if row is None:
            return None
        return _loads(row["payload_json"])

    def _list_payloads(self, table: str, where_sql: str = "", params: tuple[Any, ...] = (), order_by: str | None = None) -> list[dict[str, Any]]:
        sql = f"SELECT payload_json FROM {table}"
        if where_sql:
            sql += f" WHERE {where_sql}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        rows = self._conn.execute(sql, params).fetchall()
        return [_loads(row["payload_json"]) for row in rows]

    def _dump_record(self, record: Any) -> str:
        return _dumps(record.to_dict())

    def save_task(self, task: Task) -> Task:
        self._upsert(
            "tasks",
            "task_id",
            task.task_id,
            self._dump_record(task),
            source=task.source,
            goal=task.goal,
            priority=task.priority,
            risk_level=task.risk_level,
            budget_profile=task.budget_profile,
            mode=task.mode,
            status=task.status,
            idempotency_key=task.idempotency_key,
            owner=task.owner,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
        )
        return task

    def get_task(self, task_id: str) -> Task | None:
        payload = self._load_record("tasks", "task_id", task_id)
        return Task.from_dict(payload) if payload else None

    def get_task_by_idempotency_key(self, idempotency_key: str) -> Task | None:
        row = self._conn.execute(
            "SELECT payload_json FROM tasks WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        if row is None:
            return None
        return Task.from_dict(_loads(row["payload_json"]))

    def list_tasks(self, status: str | None = None) -> list[Task]:
        where_sql = "status = ?" if status else ""
        params = (status,) if status else ()
        return [Task.from_dict(item) for item in self._list_payloads("tasks", where_sql, params, order_by="created_at ASC")]

    def save_run(self, run: Run) -> Run:
        self._upsert(
            "runs",
            "run_id",
            run.run_id,
            self._dump_record(run),
            task_id=run.task_id,
            plan_version=run.plan_version,
            model_profile=run.model_profile,
            toolset_json=_dumps(run.toolset),
            outcome=run.outcome,
            status=run.status,
            mode=run.mode,
            started_at=run.started_at.isoformat(),
            ended_at=run.ended_at.isoformat() if run.ended_at else None,
        )
        return run

    def get_run(self, run_id: str) -> Run | None:
        payload = self._load_record("runs", "run_id", run_id)
        return Run.from_dict(payload) if payload else None

    def list_runs(self, task_id: str | None = None) -> list[Run]:
        where_sql = "task_id = ?" if task_id else ""
        params = (task_id,) if task_id else ()
        return [Run.from_dict(item) for item in self._list_payloads("runs", where_sql, params, order_by="started_at ASC")]

    def save_evidence(self, evidence: Evidence) -> Evidence:
        self._upsert(
            "evidence",
            "evidence_id",
            evidence.evidence_id,
            self._dump_record(evidence),
            run_id=evidence.run_id,
            source_type=evidence.source_type,
            source_ref=evidence.source_ref,
            summary=evidence.summary,
            confidence=evidence.confidence,
            content=evidence.content,
            is_inference=int(evidence.is_inference),
            captured_at=evidence.captured_at.isoformat(),
        )
        return evidence

    def list_evidence(self, run_id: str | None = None) -> list[Evidence]:
        where_sql = "run_id = ?" if run_id else ""
        params = (run_id,) if run_id else ()
        return [Evidence.from_dict(item) for item in self._list_payloads("evidence", where_sql, params, order_by="captured_at ASC")]

    def save_decision(self, decision: Decision) -> Decision:
        self._upsert(
            "decisions",
            "decision_id",
            decision.decision_id,
            self._dump_record(decision),
            run_id=decision.run_id,
            decision_type=decision.decision_type,
            policy_basis=decision.policy_basis,
            requires_human=int(decision.requires_human),
            approved_by=decision.approved_by,
            reason=decision.reason,
            target=decision.target,
            created_at=decision.created_at.isoformat(),
        )
        return decision

    def list_decisions(self, run_id: str | None = None) -> list[Decision]:
        where_sql = "run_id = ?" if run_id else ""
        params = (run_id,) if run_id else ()
        return [Decision.from_dict(item) for item in self._list_payloads("decisions", where_sql, params, order_by="created_at ASC")]

    def save_cost_record(self, cost_record: CostRecord) -> CostRecord:
        self._upsert(
            "cost_records",
            "run_id",
            cost_record.run_id,
            self._dump_record(cost_record),
            token_in=cost_record.token_in,
            token_out=cost_record.token_out,
            tool_calls=cost_record.tool_calls,
            latency_ms=cost_record.latency_ms,
            cache_hit=int(cost_record.cache_hit),
            estimated_cost=cost_record.estimated_cost,
            degraded_mode=cost_record.degraded_mode,
            retries=cost_record.retries,
            recorded_at=cost_record.recorded_at.isoformat(),
        )
        return cost_record

    def list_cost_records(self, run_id: str | None = None) -> list[CostRecord]:
        where_sql = "run_id = ?" if run_id else ""
        params = (run_id,) if run_id else ()
        return [CostRecord.from_dict(item) for item in self._list_payloads("cost_records", where_sql, params, order_by="recorded_at ASC")]

    def save_tool_call(self, tool_call: ToolCall) -> ToolCall:
        self._upsert(
            "tool_calls",
            "tool_call_id",
            tool_call.tool_call_id,
            self._dump_record(tool_call),
            run_id=tool_call.run_id,
            tool_name=tool_call.tool_name,
            target=tool_call.target,
            mode=tool_call.mode,
            risk_level=tool_call.risk_level,
            arguments_json=_dumps(tool_call.arguments),
            is_write=int(tool_call.is_write),
            is_destructive=int(tool_call.is_destructive),
            approved_by=tool_call.approved_by,
            outcome=tool_call.outcome,
            metadata_json=_dumps(tool_call.metadata),
            created_at=tool_call.created_at.isoformat(),
        )
        return tool_call

    def save_memory_record(self, record: MemoryRecord) -> MemoryRecord:
        self._upsert(
            "memory_records",
            "memory_id",
            record.memory_id,
            self._dump_record(record),
            task_id=record.task_id,
            run_id=record.run_id,
            scope=record.scope,
            kind=record.kind,
            key=record.key,
            value=record.value,
            source_evidence_id=record.source_evidence_id,
            ttl_seconds=record.ttl_seconds,
            version=record.version,
            created_at=record.created_at.isoformat(),
            expires_at=record.expires_at.isoformat() if record.expires_at else None,
        )
        return record

    def list_memory_records(
        self,
        *,
        scope: str | None = None,
        task_id: str | None = None,
        run_id: str | None = None,
        key: str | None = None,
    ) -> list[MemoryRecord]:
        clauses: list[str] = []
        params: list[Any] = []
        for column, value in (("scope", scope), ("task_id", task_id), ("run_id", run_id), ("key", key)):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        where_sql = " AND ".join(clauses)
        return [MemoryRecord.from_dict(item) for item in self._list_payloads("memory_records", where_sql, tuple(params), order_by="created_at ASC")]

    def save_trigger_event(self, trigger: TriggerEvent) -> TriggerEvent:
        self._upsert(
            "trigger_events",
            "trigger_id",
            trigger.trigger_id,
            self._dump_record(trigger),
            trigger_kind=trigger.trigger_kind,
            trigger_ref=trigger.trigger_ref,
            task_id=trigger.task_id,
            run_id=trigger.run_id,
            status=trigger.status,
            scheduled_for=trigger.scheduled_for.isoformat(),
            created_at=trigger.created_at.isoformat(),
            dispatched_at=trigger.dispatched_at.isoformat() if trigger.dispatched_at else None,
            completed_at=trigger.completed_at.isoformat() if trigger.completed_at else None,
        )
        return trigger

    def list_trigger_events(
        self,
        *,
        task_id: str | None = None,
        run_id: str | None = None,
        status: str | None = None,
    ) -> list[TriggerEvent]:
        clauses: list[str] = []
        params: list[Any] = []
        for column, value in (("task_id", task_id), ("run_id", run_id), ("status", status)):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        where_sql = " AND ".join(clauses)
        return [TriggerEvent.from_dict(item) for item in self._list_payloads("trigger_events", where_sql, tuple(params), order_by="created_at ASC")]

    def save_release_gate_result(self, result: ReleaseGateResult) -> ReleaseGateResult:
        self._upsert(
            "release_gate_results",
            "gate_id",
            result.gate_id,
            self._dump_record(result),
            gate_result=result.gate_result,
            required_checks_json=_dumps(result.required_checks),
            evidence_links_json=_dumps(result.evidence_links),
            rollback_plan=result.rollback_plan,
            runbook_json=_dumps(result.runbook),
        )
        return result

    def persist_result_pack(self, pack: ResultPack) -> None:
        self.save_task(pack.task)
        self.save_run(pack.run)
        for evidence in pack.evidence:
            self.save_evidence(evidence)
        for decision in pack.decisions:
            self.save_decision(decision)
        self.save_cost_record(pack.cost_record)
        for tool_call in pack.tool_calls:
            self.save_tool_call(tool_call)
        for record in pack.memory_records:
            self.save_memory_record(record)
        for trigger in pack.trigger_events:
            self.save_trigger_event(trigger)
        if pack.release_gate is not None:
            self.save_release_gate_result(pack.release_gate)

    def get_task_payload(self, task_id: str) -> dict[str, Any]:
        payload = self._load_record("tasks", "task_id", task_id)
        if payload is None:
            raise KeyError(task_id)
        return payload

    def list_memory_payloads(self, scope: str | None = None) -> list[dict[str, Any]]:
        if scope is None:
            return self._list_payloads("memory_records", order_by="memory_id ASC")
        return self._list_payloads("memory_records", "scope = ?", (scope,), order_by="memory_id ASC")


SQLiteStorage = SherryRepository


__all__ = ["SQLiteStorage", "SherryRepository"]
