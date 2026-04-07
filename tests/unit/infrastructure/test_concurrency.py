import asyncio

import pytest

from src.sherry_agent.infrastructure.concurrency import (
    ConcurrencyManager,
    ConcurrencyStats,
)


class TestConcurrencyManager:
    def test_init_default_max_concurrent(self):
        manager = ConcurrencyManager()
        import os
        expected = (os.cpu_count() or 4) * 2
        assert manager.max_concurrent == expected
        assert manager.current_count == 0

    def test_init_custom_max_concurrent(self):
        manager = ConcurrencyManager(max_concurrent=5)
        assert manager.max_concurrent == 5
        assert manager.current_count == 0

    def test_init_max_concurrent_one(self):
        manager = ConcurrencyManager(max_concurrent=1)
        assert manager.max_concurrent == 1

    @pytest.mark.asyncio
    async def test_acquire_release(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        assert manager.current_count == 0
        
        await manager.acquire()
        assert manager.current_count == 1
        
        await manager.acquire()
        assert manager.current_count == 2
        
        manager.release()
        assert manager.current_count == 1
        
        manager.release()
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_limit_context_manager(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        assert manager.current_count == 0
        
        async with manager.limit():
            assert manager.current_count == 1
            
            async with manager.limit():
                assert manager.current_count == 2
            
            assert manager.current_count == 1
        
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_concurrent_limit_enforcement(self):
        manager = ConcurrencyManager(max_concurrent=2)
        execution_order = []
        
        async def task(task_id: int, delay: float):
            async with manager.limit():
                execution_order.append(f"start_{task_id}")
                await asyncio.sleep(delay)
                execution_order.append(f"end_{task_id}")
        
        tasks = [
            asyncio.create_task(task(1, 0.1)),
            asyncio.create_task(task(2, 0.1)),
            asyncio.create_task(task(3, 0.1)),
        ]
        
        await asyncio.gather(*tasks)
        
        assert manager.current_count == 0
        assert len(execution_order) == 6
        start_count = sum(1 for item in execution_order if item.startswith("start_"))
        assert start_count == 3

    @pytest.mark.asyncio
    async def test_semaphore_blocking(self):
        manager = ConcurrencyManager(max_concurrent=1)
        results = []
        
        async def blocking_task(task_id: int):
            async with manager.limit():
                results.append(f"{task_id}_start")
                await asyncio.sleep(0.1)
                results.append(f"{task_id}_end")
        
        task1 = asyncio.create_task(blocking_task(1))
        task2 = asyncio.create_task(blocking_task(2))
        
        await asyncio.gather(task1, task2)
        
        assert results == ["1_start", "1_end", "2_start", "2_end"]

    @pytest.mark.asyncio
    async def test_stats_tracking(self):
        manager = ConcurrencyManager(max_concurrent=3)
        
        async with manager.limit():
            pass
        
        async with manager.limit():
            async with manager.limit():
                pass
        
        stats = manager.stats
        assert stats.total_acquired == 3
        assert stats.total_released == 3
        assert stats.peak_count == 2
        assert stats.current_count == 0

    @pytest.mark.asyncio
    async def test_peak_count_tracking(self):
        manager = ConcurrencyManager(max_concurrent=5)
        
        async def concurrent_task():
            async with manager.limit():
                await asyncio.sleep(0.05)
        
        tasks = [asyncio.create_task(concurrent_task()) for _ in range(4)]
        await asyncio.gather(*tasks)
        
        assert manager.stats.peak_count == 4

    def test_adjust_for_memory_high_usage(self):
        manager = ConcurrencyManager(max_concurrent=10)
        
        manager.adjust_for_memory(85)
        assert manager._pending_adjustment == 8
        
        manager._pending_adjustment = None
        manager.adjust_for_memory(75)
        assert manager._pending_adjustment == 9

    def test_adjust_for_memory_low_usage(self):
        manager = ConcurrencyManager(max_concurrent=8)
        manager._initial_max = 10
        
        manager.adjust_for_memory(40)
        assert manager._pending_adjustment == 9

    def test_adjust_for_memory_no_change(self):
        manager = ConcurrencyManager(max_concurrent=10)
        
        manager.adjust_for_memory(60)
        assert manager._pending_adjustment is None

    def test_adjust_for_cpu_high_usage(self):
        manager = ConcurrencyManager(max_concurrent=10)
        
        manager.adjust_for_cpu(95)
        assert manager._pending_adjustment == 8
        
        manager._pending_adjustment = None
        manager.adjust_for_cpu(85)
        assert manager._pending_adjustment == 9

    def test_adjust_for_cpu_low_usage(self):
        manager = ConcurrencyManager(max_concurrent=8)
        manager._initial_max = 10
        
        manager.adjust_for_cpu(40)
        assert manager._pending_adjustment == 9

    def test_adjust_for_cpu_no_change(self):
        manager = ConcurrencyManager(max_concurrent=10)
        
        manager.adjust_for_cpu(60)
        assert manager._pending_adjustment is None

    @pytest.mark.asyncio
    async def test_apply_pending_adjustment_increase(self):
        manager = ConcurrencyManager(max_concurrent=5)
        manager._pending_adjustment = 7
        
        result = await manager.apply_pending_adjustment()
        
        assert result is True
        assert manager.max_concurrent == 7
        assert manager._pending_adjustment is None
        assert len(manager.stats.adjustment_history) == 1

    @pytest.mark.asyncio
    async def test_apply_pending_adjustment_decrease(self):
        manager = ConcurrencyManager(max_concurrent=5)
        manager._pending_adjustment = 3
        
        result = await manager.apply_pending_adjustment()
        
        assert result is True
        assert manager.max_concurrent == 3

    @pytest.mark.asyncio
    async def test_apply_pending_adjustment_none(self):
        manager = ConcurrencyManager(max_concurrent=5)
        
        result = await manager.apply_pending_adjustment()
        
        assert result is False
        assert manager.max_concurrent == 5

    @pytest.mark.asyncio
    async def test_execute_with_limit(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        async def sample_coro():
            return 42
        
        result = await manager.execute_with_limit(sample_coro())
        assert result == 42
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_execute_batch_sequential(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        async def sample_coro(value: int):
            await asyncio.sleep(0.01)
            return value * 2
        
        coros = [sample_coro(i) for i in range(3)]
        results = await manager.execute_batch(coros)
        
        assert results == [0, 2, 4]
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_execute_batch_parallel(self):
        manager = ConcurrencyManager(max_concurrent=3)
        execution_times = []
        
        async def timed_coro(value: int):
            start = asyncio.get_event_loop().time()
            await asyncio.sleep(0.05)
            end = asyncio.get_event_loop().time()
            execution_times.append((value, start, end))
            return value
        
        coros = [timed_coro(i) for i in range(3)]
        results = await manager.execute_batch_parallel(coros)
        
        assert sorted(results) == [0, 1, 2]
        assert manager.current_count == 0

    def test_get_available_slots(self):
        manager = ConcurrencyManager(max_concurrent=5)
        manager._current_count = 2
        
        assert manager.get_available_slots() == 3

    def test_is_available(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        assert manager.is_available() is True
        
        manager._current_count = 2
        assert manager.is_available() is False

    @pytest.mark.asyncio
    async def test_wait_for_slot_success(self):
        manager = ConcurrencyManager(max_concurrent=1)
        
        result = await manager.wait_for_slot(timeout=0.1)
        assert result is True

    @pytest.mark.asyncio
    async def test_wait_for_slot_timeout(self):
        manager = ConcurrencyManager(max_concurrent=1)
        
        async def hold_slot():
            async with manager.limit():
                await asyncio.sleep(0.2)
        
        holder = asyncio.create_task(hold_slot())
        await asyncio.sleep(0.01)
        
        result = await manager.wait_for_slot(timeout=0.05)
        assert result is False
        
        await holder

    def test_reset_stats(self):
        manager = ConcurrencyManager(max_concurrent=5)
        manager._stats.total_acquired = 10
        manager._stats.peak_count = 3
        
        manager.reset_stats()
        
        assert manager.stats.total_acquired == 0
        assert manager.stats.peak_count == 0
        assert manager.stats.max_concurrent == 5


class TestConcurrencyStats:
    def test_init(self):
        stats = ConcurrencyStats()
        
        assert stats.current_count == 0
        assert stats.max_concurrent == 0
        assert stats.total_acquired == 0
        assert stats.total_released == 0
        assert stats.peak_count == 0
        assert stats.adjustment_history == []

    def test_init_with_max_concurrent(self):
        stats = ConcurrencyStats(max_concurrent=10)
        
        assert stats.max_concurrent == 10

    def test_adjustment_history_append(self):
        stats = ConcurrencyStats()
        
        stats.adjustment_history.append({
            "old_max": 5,
            "new_max": 3,
            "current_count": 2,
        })
        
        assert len(stats.adjustment_history) == 1
        assert stats.adjustment_history[0]["old_max"] == 5


class TestConcurrencyManagerEdgeCases:
    @pytest.mark.asyncio
    async def test_release_below_zero_protection(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        manager.release()
        assert manager.current_count == 0
        
        manager.release()
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_concurrent_acquire_release_stress(self):
        manager = ConcurrencyManager(max_concurrent=10)
        
        async def stress_task():
            for _ in range(100):
                await manager.acquire()
                manager.release()
        
        tasks = [asyncio.create_task(stress_task()) for _ in range(5)]
        await asyncio.gather(*tasks)
        
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_adjustment_with_active_tasks(self):
        manager = ConcurrencyManager(max_concurrent=5)
        
        async def long_task():
            async with manager.limit():
                await asyncio.sleep(0.2)
        
        tasks = [asyncio.create_task(long_task()) for _ in range(3)]
        await asyncio.sleep(0.05)
        
        manager.adjust_for_memory(85)
        await manager.apply_pending_adjustment()
        
        await asyncio.gather(*tasks)
        
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_exception_in_context_manager(self):
        manager = ConcurrencyManager(max_concurrent=2)
        
        try:
            async with manager.limit():
                assert manager.current_count == 1
                raise ValueError("Test error")
        except ValueError:
            pass
        
        assert manager.current_count == 0

    @pytest.mark.asyncio
    async def test_nested_limit_calls(self):
        manager = ConcurrencyManager(max_concurrent=5)
        
        async with manager.limit():
            assert manager.current_count == 1
            async with manager.limit():
                assert manager.current_count == 2
                async with manager.limit():
                    assert manager.current_count == 3
                assert manager.current_count == 2
            assert manager.current_count == 1
        assert manager.current_count == 0
