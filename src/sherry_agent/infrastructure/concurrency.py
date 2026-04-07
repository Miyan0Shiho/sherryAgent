from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, TypeVar


@dataclass
class ConcurrencyStats:
    current_count: int = 0
    max_concurrent: int = 0
    total_acquired: int = 0
    total_released: int = 0
    peak_count: int = 0
    adjustment_history: list[dict[str, Any]] = field(default_factory=list)


T = TypeVar("T")


class ConcurrencyManager:
    def __init__(self, max_concurrent: int | None = None):
        if max_concurrent is None:
            max_concurrent = (os.cpu_count() or 4) * 2
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._max_concurrent = max_concurrent
        self._initial_max = max_concurrent
        self._current_count = 0
        self._stats = ConcurrencyStats(max_concurrent=max_concurrent)
        self._lock = asyncio.Lock()
        self._pending_adjustment: int | None = None

    @property
    def max_concurrent(self) -> int:
        return self._max_concurrent

    @property
    def current_count(self) -> int:
        return self._current_count

    @property
    def stats(self) -> ConcurrencyStats:
        return self._stats

    async def acquire(self) -> None:
        await self._semaphore.acquire()
        async with self._lock:
            self._current_count += 1
            self._stats.current_count = self._current_count
            self._stats.total_acquired += 1
            if self._current_count > self._stats.peak_count:
                self._stats.peak_count = self._current_count

    def release(self) -> None:
        self._semaphore.release()
        self._current_count = max(0, self._current_count - 1)
        self._stats.current_count = self._current_count
        self._stats.total_released += 1

    @asynccontextmanager
    async def limit(self) -> AsyncIterator[None]:
        await self.acquire()
        try:
            yield
        finally:
            self.release()

    def adjust_for_memory(self, memory_usage_percent: float) -> None:
        if memory_usage_percent > 80:
            new_max = max(1, self._max_concurrent - 2)
        elif memory_usage_percent > 70:
            new_max = max(1, self._max_concurrent - 1)
        elif memory_usage_percent < 50 and self._max_concurrent < self._initial_max:
            new_max = min(self._initial_max, self._max_concurrent + 1)
        else:
            return

        if new_max != self._max_concurrent:
            self._pending_adjustment = new_max

    def adjust_for_cpu(self, cpu_usage_percent: float) -> None:
        if cpu_usage_percent > 90:
            new_max = max(1, self._max_concurrent - 2)
        elif cpu_usage_percent > 80:
            new_max = max(1, self._max_concurrent - 1)
        elif cpu_usage_percent < 50 and self._max_concurrent < self._initial_max:
            new_max = min(self._initial_max, self._max_concurrent + 1)
        else:
            return

        if new_max != self._max_concurrent:
            self._pending_adjustment = new_max

    async def apply_pending_adjustment(self) -> bool:
        if self._pending_adjustment is None:
            return False

        async with self._lock:
            if self._pending_adjustment is None:
                return False

            new_max = self._pending_adjustment
            old_max = self._max_concurrent

            if new_max < old_max:
                for _ in range(old_max - new_max):
                    try:
                        await asyncio.wait_for(
                            self._semaphore.acquire(),
                            timeout=0.001
                        )
                    except TimeoutError:
                        break
            elif new_max > old_max:
                for _ in range(new_max - old_max):
                    self._semaphore.release()

            self._max_concurrent = new_max
            self._stats.max_concurrent = new_max
            self._stats.adjustment_history.append({
                "old_max": old_max,
                "new_max": new_max,
                "current_count": self._current_count,
            })
            self._pending_adjustment = None
            return True

    async def execute_with_limit(
        self,
        coro: Awaitable[T],
    ) -> T:
        async with self.limit():
            return await coro

    async def execute_batch(
        self,
        coros: list[Awaitable[T]],
    ) -> list[T]:
        results: list[T] = []
        for coro in coros:
            result = await self.execute_with_limit(coro)
            results.append(result)
        return results

    async def execute_batch_parallel(
        self,
        coros: list[Awaitable[T]],
    ) -> list[T]:
        async def wrapped(coro: Awaitable[T]) -> T:
            async with self.limit():
                return await coro

        tasks = [wrapped(coro) for coro in coros]
        return await asyncio.gather(*tasks)

    def get_available_slots(self) -> int:
        return self._max_concurrent - self._current_count

    def is_available(self) -> bool:
        return self._current_count < self._max_concurrent

    async def wait_for_slot(self, timeout: float | None = None) -> bool:
        try:
            await asyncio.wait_for(self.acquire(), timeout=timeout)
            self.release()
            return True
        except TimeoutError:
            return False

    def reset_stats(self) -> None:
        self._stats = ConcurrencyStats(max_concurrent=self._max_concurrent)
