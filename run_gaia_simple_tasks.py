#!/usr/bin/env python3
"""
运行 GAIA Level 1 简单任务测试
使用 qwen3:0.6b 执行 2 个简单任务
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tests.benchmark.runner import (
    BenchmarkRunner,
    TestCase,
    create_simple_test_case,
    BenchmarkStatus,
)


async def main():
    """主函数：运行 GAIA Level 1 简单任务测试"""
    print("=" * 80)
    print("SherryAgent - GAIA Level 1 简单任务测试")
    print("=" * 80)
    print()

    runner = BenchmarkRunner(
        model="qwen3:0.6b",
        ollama_base_url="http://localhost:11434",
        log_dir="tests/benchmark/logs",
        max_tokens=1024,
        max_tool_rounds=5,
        token_budget=50_000,
    )

    test_cases = [
        create_simple_test_case(
            test_id="gaia_level1_001",
            name="GAIA Level 1 - 简单数学计算",
            user_prompt="计算 25 * 17 的结果是多少？",
            system_prompt="你是一个能解决数学问题的助手，只需要给出计算结果。",
        ),
        create_simple_test_case(
            test_id="gaia_level1_002",
            name="GAIA Level 1 - 简单信息查询",
            user_prompt="地球绕太阳公转的周期是多少天？",
            system_prompt="你是一个知识丰富的助手，请准确回答问题。",
        ),
    ]

    results = []
    for test_case in test_cases:
        print(f"\n{'=' * 80}")
        print(f"执行测试: {test_case.test_id}")
        print(f"名称: {test_case.name}")
        print(f"用户提示: {test_case.user_prompt}")
        print('=' * 80)
        print()

        result = await runner.run_test(test_case)
        results.append(result)

        print(f"\n结果:")
        print(f"  状态: {result.status.value}")
        print(f"  总 Token: {result.total_tokens}")
        if result.final_response:
            print(f"  最终响应: {result.final_response[:200]}")
        if result.status == BenchmarkStatus.FAILED:
            print(f"  错误: {result.error_message}")

    print("\n" + "=" * 80)
    print("测试执行完成总结")
    print("=" * 80)
    for result in results:
        print(f"  - {result.test_id}: {result.status.value}")
    print("\n日志已保存到 tests/benchmark/logs/ 目录")

    return results


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
