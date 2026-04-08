from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from .models import TriggerEvent, utc_now


class TriggerScheduler:
    def __init__(self, events: Iterable[TriggerEvent] | None = None) -> None:
        self._events: dict[str, TriggerEvent] = {}
        for event in events or ():
            self.schedule(event)

    def schedule(self, event: TriggerEvent) -> TriggerEvent:
        self._events[event.trigger_id] = event
        return event

    def schedule_periodic(self, *, source: str, interval_seconds: int, payload: dict | None = None, when: datetime | None = None) -> TriggerEvent:
        event = TriggerEvent(
            trigger_kind="scheduled",
            trigger_ref=source,
            payload=payload or {},
            scheduled_for=(when or utc_now()) + timedelta(seconds=interval_seconds),
        )
        return self.schedule(event)

    def schedule_event(self, *, source: str, payload: dict | None = None, when: datetime | None = None) -> TriggerEvent:
        event = TriggerEvent(
            trigger_kind="event",
            trigger_ref=source,
            payload=payload or {},
            scheduled_for=when or utc_now(),
        )
        return self.schedule(event)

    def due_events(self, at: datetime | None = None) -> list[TriggerEvent]:
        probe = at or utc_now()
        return sorted((event for event in self._events.values() if event.is_due(probe)), key=lambda item: item.scheduled_for)

    def dispatch_due(self, at: datetime | None = None) -> list[TriggerEvent]:
        dispatched = self.due_events(at)
        for event in dispatched:
            event.mark_dispatched()
        return dispatched

    def complete(self, trigger_id: str, status: str = "completed") -> TriggerEvent:
        event = self._events[trigger_id]
        event.mark_completed(status)
        return event

    def list(self) -> list[TriggerEvent]:
        return sorted(self._events.values(), key=lambda item: item.scheduled_for)
