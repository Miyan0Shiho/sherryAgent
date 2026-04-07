#!/usr/bin/env python3
"""
GAIA 基准测试套件执行脚本
从 GAIA 数据集中每个难度级别抽取 3-5 个任务，使用 qwen3:0.6b 模型执行
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from tests.benchmark.datasets.gaia import (
    GaiaDatasetLoader,
    GaiaLevel,
    GaiaTestCase,
)
from tests.benchmark.runner import (
    BenchmarkResult,
    BenchmarkRunner,
    BenchmarkStatus,
    TestCase,
)


class GaiaBenchmarkSuite:
    """GAIA 基准测试套件执行器"""

    def __init__(
        self,
        model: str = "qwen3:0.6b",
        results_dir: str = "tests/benchmark/results",
        num_tasks_per_level: int = 4,
    ):
        self.model = model
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.num_tasks_per_level = num_tasks_per_level
        self.suite_results: list[dict[str, Any]] = []

        self.loader = GaiaDatasetLoader()
        self.runner = BenchmarkRunner(
            model=model,
            log_dir=str(self.results_dir / "logs"),
            max_tokens=2048,
            max_tool_rounds=10,
            token_budget=50_000,
        )

    def _sample_tasks_by_level(self, level: GaiaLevel, num_tasks: int) -> list[GaiaTestCase]:
        """从指定难度级别抽取任务"""
        cases = list(self.loader.get_cases_by_level(level))
        if len(cases) < num_tasks:
            num_tasks = len(cases)
        return cases[:num_tasks]

    def _gaia_to_test_case(self, gaia_case: GaiaTestCase, level_name: str) -> TestCase:
        """将 GAIA 测试用例转换为 TestCase"""
        return TestCase(
            test_id=f"gaia_{level_name}_{gaia_case.id}",
            name=f"GAIA {level_name} - {gaia_case.id}",
            description=f"GAIA 测试用例 (Level {gaia_case.level}): {gaia_case.task[:100]}...",
            user_prompt=gaia_case.task,
            system_prompt="你是一个有用的 AI 助手。请仔细分析问题，使用可用的工具来解决问题。",
            max_tokens=2048,
            timeout=600.0,
        )

    def _determine_status(self, result: BenchmarkResult) -> str:
        """确定任务执行状态（成功/部分成功/失败）"""
        if result.status == BenchmarkStatus.COMPLETED:
            if result.final_response and len(result.final_response) > 0:
                return "success"
            else:
                return "partial_success"
        return "failed"

    async def run_suite(self) -> None:
        """运行完整的测试套件"""
        print("=" * 80)
        print("GAIA 基准测试套件")
        print(f"模型: {self.model}")
        print(f"每个难度级别任务数: {self.num_tasks_per_level}")
        print("=" * 80)
        print()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        levels = [
            (GaiaLevel.LEVEL_1, "Level 1 (简单)"),
            (GaiaLevel.LEVEL_2, "Level 2 (中等)"),
            (GaiaLevel.LEVEL_3, "Level 3 (困难)"),
        ]

        for level, level_name in levels:
            print(f"\n{'=' * 80}")
            print(f"执行 {level_name} 任务")
            print('=' * 80)

            tasks = self._sample_tasks_by_level(level, self.num_tasks_per_level)
            print(f"抽取到 {len(tasks)} 个任务\n")

            for i, gaia_task in enumerate(tasks, 1):
                print(f"任务 {i}/{len(tasks)}: {gaia_task.id}")
                print(f"问题: {gaia_task.task[:80]}...")

                test_case = self._gaia_to_test_case(gaia_task, level_name.lower().replace(" ", "_").replace("(", "").replace(")", ""))

                try:
                    result = await self.runner.run_test(test_case)

                    status = self._determine_status(result)

                    result_info = {
                        "level": level_name,
                        "task_id": gaia_task.id,
                        "test_id": test_case.test_id,
                        "task": gaia_task.task,
                        "expected_answer": gaia_task.expected_answer,
                        "status": status,
                        "start_time": result.start_time.isoformat(),
                        "end_time": result.end_time.isoformat() if result.end_time else None,
                        "total_tokens": result.total_tokens,
                        "input_tokens": result.input_tokens,
                        "output_tokens": result.output_tokens,
                        "final_response": result.final_response,
                        "error_message": result.error_message,
                        "log_files": result.log_files,
                    }

                    self.suite_results.append(result_info)

                    print(f"  状态: {status.upper()}")
                    print(f"  Token 消耗: {result.total_tokens}")

                except Exception as e:
                    print(f"  错误: {str(e)}")
                    self.suite_results.append({
                        "level": level_name,
                        "task_id": gaia_task.id,
                        "test_id": test_case.test_id,
                        "task": gaia_task.task,
                        "expected_answer": gaia_task.expected_answer,
                        "status": "failed",
                        "error_message": str(e),
                    })

                print()

        self._save_results(timestamp)
        self._generate_summary(timestamp)

    def _save_results(self, timestamp: str) -> None:
        """保存所有测试结果"""
        results_file = self.results_dir / f"benchmark_results_{timestamp}.json"

        with open(results_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "model": self.model,
                "num_tasks_per_level": self.num_tasks_per_level,
                "results": self.suite_results,
            }, f, ensure_ascii=False, indent=2)

        print(f"测试结果已保存到: {results_file}")

    def _generate_summary(self, timestamp: str) -> None:
        """生成测试汇总文档"""
        summary_file = self.results_dir.parent / "test_summary.md"

        total_tasks = len(self.suite_results)
        success_count = sum(1 for r in self.suite_results if r["status"] == "success")
        partial_success_count = sum(1 for r in self.suite_results if r["status"] == "partial_success")
        failed_count = sum(1 for r in self.suite_results if r["status"] == "failed")

        level_stats: dict[str, dict[str, int]] = {}
        for result in self.suite_results:
            level = result["level"]
            if level not in level_stats:
                level_stats[level] = {"total": 0, "success": 0, "partial_success": 0, "failed": 0}
            level_stats[level]["total"] += 1
            level_stats[level][result["status"]] += 1

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("# GAIA 基准测试汇总\n\n")
            f.write(f"**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**模型**: {self.model}\n\n")

            f.write("## 总体统计\n\n")
            f.write("| 指标 | 数值 |\n")
            f.write("|------|------|\n")
            f.write(f"| 总任务数 | {total_tasks} |\n")
            f.write(f"| 成功 | {success_count} |\n")
            f.write(f"| 部分成功 | {partial_success_count} |\n")
            f.write(f"| 失败 | {failed_count} |\n")
            f.write(f"| 成功率 | {success_count/total_tasks*100:.1f}% |\n\n")

            f.write("## 各难度级别统计\n\n")
            for level, stats in level_stats.items():
                f.write(f"### {level}\n\n")
                f.write("| 状态 | 数量 |\n")
                f.write("|------|------|\n")
                f.write(f"| 成功 | {stats['success']} |\n")
                f.write(f"| 部分成功 | {stats['partial_success']} |\n")
                f.write(f"| 失败 | {stats['failed']} |\n\n")

            f.write("## 详细任务结果\n\n")
            f.write("| 级别 | 任务ID | 状态 | Token 消耗 | 简要观察 |\n")
            f.write("|------|--------|------|------------|----------|\n")

            for result in self.suite_results:
                status_emoji = {
                    "success": "✅",
                    "partial_success": "⚠️",
                    "failed": "❌",
                }.get(result["status"], "❓")

                observation = ""
                if result["status"] == "success":
                    observation = "任务完成，有响应输出"
                elif result["status"] == "partial_success":
                    observation = "执行完成但响应可能不完整"
                else:
                    observation = result.get("error_message", "执行失败")[:50]

                f.write(
                    f"| {result['level']} | {result['task_id']} | "
                    f"{status_emoji} {result['status']} | "
                    f"{result.get('total_tokens', 'N/A')} | "
                    f"{observation} |\n"
                )

            f.write("\n---\n\n")
            f.write(f"详细结果文件: `{self.results_dir}/benchmark_results_{timestamp}.json`\n")

        print(f"测试汇总文档已生成: {summary_file}")


async def main() -> None:
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="GAIA 基准测试套件")
    parser.add_argument(
        "--model",
        default="qwen3:0.6b",
        help="使用的模型 (默认: qwen3:0.6b)",
    )
    parser.add_argument(
        "--num-tasks",
        type=int,
        default=4,
        help="每个难度级别抽取的任务数 (默认: 4)",
    )
    parser.add_argument(
        "--results-dir",
        default="tests/benchmark/results",
        help="结果保存目录 (默认: tests/benchmark/results)",
    )

    args = parser.parse_args()

    suite = GaiaBenchmarkSuite(
        model=args.model,
        results_dir=args.results_dir,
        num_tasks_per_level=args.num_tasks,
    )

    await suite.run_suite()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n运行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

