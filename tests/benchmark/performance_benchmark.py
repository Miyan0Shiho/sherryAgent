"""
性能基准测试模块

提供系统化的性能基准测试框架，包括：
- 记忆系统性能测试
- LLM 客户端性能测试
- 并发性能测试
- 性能报告生成
"""

from __future__ import annotations

import asyncio
import random
import statistics
import tempfile
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from sherry_agent.infrastructure.cache import TTLCache
from sherry_agent.infrastructure.concurrency import ConcurrencyManager
from sherry_agent.llm.client import MockLLMClient
from sherry_agent.memory.bridge import MemoryBridge
from sherry_agent.memory.long_term import LongTermMemory
from sherry_agent.memory.short_term import ShortTermMemory


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    name: str
    iterations: int
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    std_dev: float
    ops_per_second: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ComparisonResult:
    """对比测试结果"""
    name: str
    baseline: BenchmarkResult
    optimized: BenchmarkResult
    improvement_percent: float
    speedup_factor: float


class PerformanceBenchmark:
    """性能基准测试框架"""

    def __init__(self, warmup_iterations: int = 3):
        self._warmup_iterations = warmup_iterations
        self._results: list[BenchmarkResult] = []
        self._comparisons: list[ComparisonResult] = []

    async def run_benchmark(
        self,
        name: str,
        func: Callable[[], Awaitable[Any]],
        iterations: int = 100,
        metadata: dict[str, Any] | None = None,
    ) -> BenchmarkResult:
        """运行单个基准测试"""
        for _ in range(self._warmup_iterations):
            await func()

        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            await func()
            end = time.perf_counter()
            times.append(end - start)

        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            total_time=sum(times),
            avg_time=statistics.mean(times),
            min_time=min(times),
            max_time=max(times),
            std_dev=statistics.stdev(times) if len(times) > 1 else 0,
            ops_per_second=iterations / sum(times),
            metadata=metadata or {},
        )
        self._results.append(result)
        return result

    async def run_comparison(
        self,
        name: str,
        baseline_func: Callable[[], Awaitable[Any]],
        optimized_func: Callable[[], Awaitable[Any]],
        iterations: int = 100,
    ) -> ComparisonResult:
        """运行对比测试"""
        baseline = await self.run_benchmark(
            f"{name}_baseline",
            baseline_func,
            iterations,
        )
        optimized = await self.run_benchmark(
            f"{name}_optimized",
            optimized_func,
            iterations,
        )

        improvement = ((baseline.avg_time - optimized.avg_time) / baseline.avg_time) * 100
        speedup = baseline.avg_time / optimized.avg_time if optimized.avg_time > 0 else 0

        comparison = ComparisonResult(
            name=name,
            baseline=baseline,
            optimized=optimized,
            improvement_percent=improvement,
            speedup_factor=speedup,
        )
        self._comparisons.append(comparison)
        return comparison

    def generate_report(self, output_path: Path | None = None) -> str:
        """生成 Markdown 格式的性能报告"""
        lines = [
            "# 性能基准测试报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 测试概览",
            "",
            f"- 总测试数: {len(self._results)}",
            f"- 对比测试数: {len(self._comparisons)}",
            "",
        ]

        if self._results:
            lines.extend([
                "## 性能测试结果",
                "",
                "| 测试名称 | 迭代次数 | 平均时间 (ms) | 最小时间 (ms) | 最大时间 (ms) | 标准差 | 操作/秒 |",
                "|----------|----------|---------------|---------------|---------------|--------|---------|",
            ])

            for result in self._results:
                lines.append(
                    f"| {result.name} | {result.iterations} | "
                    f"{result.avg_time * 1000:.4f} | {result.min_time * 1000:.4f} | "
                    f"{result.max_time * 1000:.4f} | {result.std_dev * 1000:.4f} | "
                    f"{result.ops_per_second:.2f} |"
                )

            lines.append("")

        if self._comparisons:
            lines.extend([
                "## 对比测试结果",
                "",
                "| 测试名称 | 基线时间 (ms) | 优化时间 (ms) | 改进百分比 | 加速比 |",
                "|----------|---------------|---------------|------------|--------|",
            ])

            for comp in self._comparisons:
                lines.append(
                    f"| {comp.name} | {comp.baseline.avg_time * 1000:.4f} | "
                    f"{comp.optimized.avg_time * 1000:.4f} | "
                    f"{comp.improvement_percent:.2f}% | {comp.speedup_factor:.2f}x |"
                )

            lines.append("")

        report = "\n".join(lines)

        if output_path:
            output_path.write_text(report, encoding="utf-8")

        return report

    def clear_results(self) -> None:
        """清除所有测试结果"""
        self._results.clear()
        self._comparisons.clear()


class MemoryBenchmark:
    """记忆系统性能基准测试"""

    def __init__(self, benchmark: PerformanceBenchmark):
        self._benchmark = benchmark
        self._temp_files: list[str] = []

    async def run_all(self) -> list[BenchmarkResult]:
        """运行所有记忆系统基准测试"""
        results = []
        results.extend(await self._test_short_term_memory())
        results.extend(await self._test_long_term_memory())
        results.extend(await self._test_memory_bridge())
        results.extend(await self._test_search_performance())
        return results

    async def _test_short_term_memory(self) -> list[BenchmarkResult]:
        """短期记忆性能测试"""
        results = []

        memory = ShortTermMemory(max_tokens=10000)

        async def add_single_item() -> None:
            memory.add_item({
                "role": "user",
                "content": f"Test message {random.randint(1, 10000)}",
            })

        result = await self._benchmark.run_benchmark(
            "short_term_add_single",
            add_single_item,
            iterations=1000,
            metadata={"max_tokens": 10000},
        )
        results.append(result)

        memory.clear()
        items = [{"role": "user", "content": f"Message {i}"} for i in range(100)]

        async def add_batch() -> None:
            for item in items:
                memory.add_item(item)

        result = await self._benchmark.run_benchmark(
            "short_term_add_batch_100",
            add_batch,
            iterations=10,
            metadata={"batch_size": 100},
        )
        results.append(result)

        memory.clear()
        for i in range(100):
            memory.add_item({"role": "user", "content": f"Message {i}"})

        def get_memory_inner() -> list[dict[str, Any]]:
            return memory.get_memory()

        async def get_memory() -> list[dict[str, Any]]:
            return get_memory_inner()

        result = await self._benchmark.run_benchmark(
            "short_term_get_memory",
            get_memory,
            iterations=1000,
        )
        results.append(result)

        compact_memory = ShortTermMemory(max_tokens=100)

        async def add_with_compaction() -> None:
            compact_memory.add_item({
                "role": "user",
                "content": f"Long message {random.randint(1, 10000)} " * 10,
            })

        result = await self._benchmark.run_benchmark(
            "short_term_add_with_compaction",
            add_with_compaction,
            iterations=100,
            metadata={"max_tokens": 100, "compaction_enabled": True},
        )
        results.append(result)

        return results

    async def _test_long_term_memory(self) -> list[BenchmarkResult]:
        """长期记忆性能测试"""
        results = []

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name
        self._temp_files.append(db_path)

        try:
            ltm = LongTermMemory(db_path=db_path)
            await ltm.initialize()

            async def add_single() -> int:
                await ltm.add_memory(
                    f"Test memory {random.randint(1, 10000)}",
                    {"category": "test"},
                )
                return 0

            result = await self._benchmark.run_benchmark(
                "long_term_add_single",
                add_single,
                iterations=100,
            )
            results.append(result)

            items = [
                {"content": f"Batch memory {i}", "metadata": {"index": i}}
                for i in range(50)
            ]

            async def add_batch() -> list[int]:
                return await ltm.add_memories_batch(items)

            result = await self._benchmark.run_benchmark(
                "long_term_add_batch_50",
                add_batch,
                iterations=10,
                metadata={"batch_size": 50},
            )
            results.append(result)

            for i in range(100):
                await ltm.add_memory(f"Search test content {i}", {"index": i})

            async def search() -> list[dict[str, Any]]:
                return await ltm.search_memory("test", limit=10)

            result = await self._benchmark.run_benchmark(
                "long_term_search",
                search,
                iterations=100,
                metadata={"limit": 10},
            )
            results.append(result)

            async def get_recent() -> list[dict[str, Any]]:
                return await ltm.get_recent_memories(limit=20)

            result = await self._benchmark.run_benchmark(
                "long_term_get_recent",
                get_recent,
                iterations=100,
                metadata={"limit": 20},
            )
            results.append(result)

        finally:
            await ltm.close()

        return results

    async def _test_memory_bridge(self) -> list[BenchmarkResult]:
        """记忆桥接性能测试"""
        results = []

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name
        self._temp_files.append(db_path)

        try:
            stm = ShortTermMemory(max_tokens=5000)
            ltm = LongTermMemory(db_path=db_path)
            await ltm.initialize()
            bridge = MemoryBridge(stm, ltm)

            for i in range(50):
                stm.add_item({
                    "role": "user",
                    "content": f"Important message {i} with key information",
                })

            async def process_cycle() -> dict[str, Any]:
                return await bridge.process_memory_cycle(importance_threshold=0.5)

            result = await self._benchmark.run_benchmark(
                "memory_bridge_process_cycle",
                process_cycle,
                iterations=10,
                metadata={"items": 50, "threshold": 0.5},
            )
            results.append(result)

        finally:
            await ltm.close()

        return results

    async def _test_search_performance(self) -> list[BenchmarkResult]:
        """搜索性能对比测试"""
        results = []

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name
        self._temp_files.append(db_path)

        try:
            ltm = LongTermMemory(db_path=db_path)
            await ltm.initialize()

            for i in range(500):
                await ltm.add_memory(
                    f"Document {i}: This is a test document about topic {i % 10}",
                    {"topic": i % 10},
                )

            async def fts_search() -> list[dict[str, Any]]:
                return await ltm.search_memory("document", limit=20)

            result = await self._benchmark.run_benchmark(
                "search_fts5",
                fts_search,
                iterations=50,
                metadata={"method": "FTS5", "total_docs": 500},
            )
            results.append(result)

            async def recent_search() -> list[dict[str, Any]]:
                memories = await ltm.get_recent_memories(limit=100)
                return [m for m in memories if "document" in m.get("content", "").lower()][:20]

            result = await self._benchmark.run_benchmark(
                "search_like_fallback",
                recent_search,
                iterations=50,
                metadata={"method": "LIKE", "total_docs": 500},
            )
            results.append(result)

            comparison = await self._benchmark.run_comparison(
                "search_method_comparison",
                recent_search,
                fts_search,
                iterations=50,
            )
            results.extend([comparison.baseline, comparison.optimized])

        finally:
            await ltm.close()

        return results

    def cleanup(self) -> None:
        """清理临时文件"""
        import os
        for path in self._temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass
        self._temp_files.clear()


class LLMBenchmark:
    """LLM 客户端性能基准测试"""

    def __init__(self, benchmark: PerformanceBenchmark):
        self._benchmark = benchmark

    async def run_all(self) -> list[BenchmarkResult]:
        """运行所有 LLM 基准测试"""
        results = []
        results.extend(await self._test_mock_client())
        results.extend(await self._test_session_reuse())
        return results

    async def _test_mock_client(self) -> list[BenchmarkResult]:
        """Mock LLM 客户端性能测试"""
        results = []

        client = MockLLMClient(responses=["Test response"])

        messages = [{"role": "user", "content": "Hello"}]

        async def single_chat() -> Any:
            return await client.chat(messages, model="mock", max_tokens=100)

        result = await self._benchmark.run_benchmark(
            "llm_mock_single_chat",
            single_chat,
            iterations=100,
        )
        results.append(result)

        async def stream_chat() -> list[Any]:
            chunks = []
            async for event in client.chat_stream(messages, model="mock", max_tokens=100):
                chunks.append(event)
            return chunks

        result = await self._benchmark.run_benchmark(
            "llm_mock_stream_chat",
            stream_chat,
            iterations=50,
        )
        results.append(result)

        return results

    async def _test_session_reuse(self) -> list[BenchmarkResult]:
        """Session 复用性能测试"""
        results = []

        client = MockLLMClient(responses=["Response"])

        async def new_session() -> Any:
            new_client = MockLLMClient(responses=["Response"])
            return await new_client.chat(
                [{"role": "user", "content": "Test"}],
                model="mock",
                max_tokens=100,
            )

        result = await self._benchmark.run_benchmark(
            "llm_new_session",
            new_session,
            iterations=50,
        )
        results.append(result)

        async def reuse_session() -> Any:
            return await client.chat(
                [{"role": "user", "content": "Test"}],
                model="mock",
                max_tokens=100,
            )

        result = await self._benchmark.run_benchmark(
            "llm_reuse_session",
            reuse_session,
            iterations=50,
        )
        results.append(result)

        comparison = await self._benchmark.run_comparison(
            "llm_session_comparison",
            new_session,
            reuse_session,
            iterations=50,
        )
        results.extend([comparison.baseline, comparison.optimized])

        return results


class ConcurrencyBenchmark:
    """并发性能基准测试"""

    def __init__(self, benchmark: PerformanceBenchmark):
        self._benchmark = benchmark

    async def run_all(self) -> list[BenchmarkResult]:
        """运行所有并发基准测试"""
        results = []
        results.extend(await self._test_concurrent_limits())
        results.extend(await self._test_cache_performance())
        results.extend(await self._test_batch_execution())
        return results

    async def _test_concurrent_limits(self) -> list[BenchmarkResult]:
        """不同并发限制下的吞吐量测试"""
        results = []

        async def cpu_bound_task() -> int:
            await asyncio.sleep(0.01)
            return sum(i * i for i in range(100))

        for max_concurrent in [1, 2, 4, 8]:
            manager = ConcurrencyManager(max_concurrent=max_concurrent)

            async def run_with_limit(m: ConcurrencyManager = manager) -> int:
                async with m.limit():
                    return await cpu_bound_task()

            tasks = [run_with_limit() for _ in range(50)]

            start = time.perf_counter()
            await asyncio.gather(*tasks)
            total_time = time.perf_counter() - start

            result = BenchmarkResult(
                name=f"concurrency_limit_{max_concurrent}",
                iterations=50,
                total_time=total_time,
                avg_time=total_time / 50,
                min_time=0,
                max_time=0,
                std_dev=0,
                ops_per_second=50 / total_time,
                metadata={"max_concurrent": max_concurrent},
            )
            self._benchmark._results.append(result)
            results.append(result)

        return results

    async def _test_cache_performance(self) -> list[BenchmarkResult]:
        """缓存性能测试"""
        results = []

        cache = TTLCache[str, str](default_ttl=60.0, max_size=100)

        async def cache_miss() -> str | None:
            key = f"key_{random.randint(1, 10000)}"
            await cache.set(key, "value")
            return await cache.get(key)

        result = await self._benchmark.run_benchmark(
            "cache_miss",
            cache_miss,
            iterations=100,
            metadata={"cache_size": 100},
        )
        results.append(result)

        for i in range(50):
            await cache.set(f"hot_key_{i}", f"value_{i}")

        async def cache_hit() -> str | None:
            key = f"hot_key_{random.randint(0, 49)}"
            return await cache.get(key)

        result = await self._benchmark.run_benchmark(
            "cache_hit",
            cache_hit,
            iterations=100,
            metadata={"cache_size": 100, "hot_keys": 50},
        )
        results.append(result)

        comparison = await self._benchmark.run_comparison(
            "cache_hit_vs_miss",
            cache_miss,
            cache_hit,
            iterations=100,
        )
        results.extend([comparison.baseline, comparison.optimized])

        return results

    async def _test_batch_execution(self) -> list[BenchmarkResult]:
        """批量执行性能测试"""
        results = []

        manager = ConcurrencyManager(max_concurrent=4)

        async def simple_task() -> int:
            await asyncio.sleep(0.01)
            return 1

        async def sequential_batch() -> list[int]:
            tasks = [simple_task() for _ in range(20)]
            seq_results = []
            for task in tasks:
                result = await manager.execute_with_limit(task)
                seq_results.append(result)
            return seq_results

        result = await self._benchmark.run_benchmark(
            "batch_sequential",
            sequential_batch,
            iterations=10,
            metadata={"tasks": 20, "mode": "sequential"},
        )
        results.append(result)

        async def parallel_batch() -> list[int]:
            tasks = [simple_task() for _ in range(20)]
            return await manager.execute_batch_parallel(tasks)

        result = await self._benchmark.run_benchmark(
            "batch_parallel",
            parallel_batch,
            iterations=10,
            metadata={"tasks": 20, "mode": "parallel"},
        )
        results.append(result)

        comparison = await self._benchmark.run_comparison(
            "batch_execution_comparison",
            sequential_batch,
            parallel_batch,
            iterations=10,
        )
        results.extend([comparison.baseline, comparison.optimized])

        return results


async def run_full_benchmark_suite(
    output_path: Path | None = None,
) -> tuple[str, list[BenchmarkResult]]:
    """运行完整的性能基准测试套件"""
    benchmark = PerformanceBenchmark(warmup_iterations=3)
    all_results: list[BenchmarkResult] = []

    print("开始性能基准测试...")
    print("=" * 60)

    print("\n[1/3] 记忆系统性能测试...")
    memory_benchmark = MemoryBenchmark(benchmark)
    try:
        memory_results = await memory_benchmark.run_all()
        all_results.extend(memory_results)
        print(f"  完成 {len(memory_results)} 项测试")
    finally:
        memory_benchmark.cleanup()

    print("\n[2/3] LLM 客户端性能测试...")
    llm_benchmark = LLMBenchmark(benchmark)
    llm_results = await llm_benchmark.run_all()
    all_results.extend(llm_results)
    print(f"  完成 {len(llm_results)} 项测试")

    print("\n[3/3] 并发性能测试...")
    concurrency_benchmark = ConcurrencyBenchmark(benchmark)
    concurrency_results = await concurrency_benchmark.run_all()
    all_results.extend(concurrency_results)
    print(f"  完成 {len(concurrency_results)} 项测试")

    print("\n" + "=" * 60)
    print("生成性能报告...")

    report = benchmark.generate_report(output_path)

    print(f"\n测试完成！共 {len(all_results)} 项测试")
    if output_path:
        print(f"报告已保存至: {output_path}")

    return report, all_results


def print_summary(results: list[BenchmarkResult]) -> None:
    """打印测试结果摘要"""
    print("\n性能测试摘要:")
    print("-" * 80)
    print(f"{'测试名称':<35} {'平均时间(ms)':<15} {'操作/秒':<15} {'迭代次数':<10}")
    print("-" * 80)

    for result in results:
        print(
            f"{result.name:<35} "
            f"{result.avg_time * 1000:>12.4f}   "
            f"{result.ops_per_second:>12.2f}   "
            f"{result.iterations:>8}"
        )

    print("-" * 80)


if __name__ == "__main__":
    output_file = Path(__file__).parent / "benchmark_report.md"
    report, results = asyncio.run(run_full_benchmark_suite(output_file))
    print_summary(results)
    print(f"\n完整报告: {output_file}")
