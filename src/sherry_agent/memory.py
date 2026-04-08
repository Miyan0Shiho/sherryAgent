from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from .models import MemoryRecord, utc_now
from .storage import SherryRepository


class MemoryStore:
    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.repository = SherryRepository(db_path)

    def close(self) -> None:
        self.repository.close()

    def __enter__(self) -> "MemoryStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def put(self, record: MemoryRecord) -> MemoryRecord:
        if record.expires_at is None and record.ttl_seconds is not None:
            record.expires_at = record.created_at + timedelta(seconds=record.ttl_seconds)
        self.repository.save_memory_record(record)
        return record

    def list(self, *, scope: str | None = None, include_expired: bool = False) -> list[MemoryRecord]:
        records = [self._from_payload(payload) for payload in self.repository.list_memory_payloads(scope)]
        if include_expired:
            return records
        return [record for record in records if not record.is_expired()]

    def retrieve(self, query: str, *, scope: str | None = None, limit: int = 5) -> list[MemoryRecord]:
        terms = [term for term in query.lower().split() if term]
        scored: list[tuple[int, MemoryRecord]] = []
        for record in self.list(scope=scope):
            haystack = f"{record.key} {record.value} {record.scope}".lower()
            score = sum(1 for term in terms if term in haystack)
            if terms and score == 0:
                continue
            scored.append((score, record))
        scored.sort(key=lambda item: (item[0], item[1].created_at), reverse=True)
        return [record for _, record in scored[:limit]]

    def compress(self, *, scope: str, ttl_seconds: int = 3600) -> MemoryRecord:
        source_records = self.list(scope=scope)[:5]
        if not source_records:
            raise ValueError(f"no records available to compress for scope: {scope}")
        record = MemoryRecord(
            task_id=source_records[0].task_id,
            run_id=source_records[0].run_id,
            scope=scope,
            kind="summary",
            key=f"{scope}:summary",
            value="; ".join(item.value for item in source_records),
            metadata={"compressed_from": [item.memory_id for item in source_records]},
            source_evidence_id=source_records[0].source_evidence_id,
            ttl_seconds=ttl_seconds,
            version=source_records[0].version,
        )
        return self.put(record)

    def purge_expired(self) -> int:
        expired = [record for record in self.list(include_expired=True) if record.is_expired()]
        if not expired:
            return 0
        conn = self.repository._conn  # internal use for compact test harness
        for record in expired:
            conn.execute("DELETE FROM memory_records WHERE memory_id = ?", (record.memory_id,))
        conn.commit()
        return len(expired)

    def _from_payload(self, payload: dict[str, object]) -> MemoryRecord:
        expires_at = payload.get("expires_at")
        created_at = payload.get("created_at")
        return MemoryRecord(
            memory_id=str(payload["memory_id"]),
            task_id=str(payload["task_id"]),
            run_id=str(payload["run_id"]),
            scope=str(payload["scope"]),
            kind=str(payload["kind"]),
            key=str(payload["key"]),
            value=str(payload["value"]),
            content=str(payload.get("content") or payload["value"]),
            story=None if payload.get("story") is None else str(payload["story"]),
            relevance=float(payload.get("relevance", 1.0)),
            metadata=dict(payload.get("metadata") or {}),
            source_evidence_id=None if payload.get("source_evidence_id") is None else str(payload["source_evidence_id"]),
            ttl_seconds=None if payload.get("ttl_seconds") is None else int(payload["ttl_seconds"]),
            version=str(payload["version"]),
            created_at=utc_now() if created_at is None else datetime.fromisoformat(str(created_at)),
            expires_at=None if expires_at is None else datetime.fromisoformat(str(expires_at)),
        )
