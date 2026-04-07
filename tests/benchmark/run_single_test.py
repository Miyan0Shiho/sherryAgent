#!/usr/bin/env python3
"""
示例脚本：运行单个测试用例
演示如何使用 BenchmarkRunner
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from tests.benchmark.runner import (
    BenchmarkRunner,
    TestCase,
    create_simple_test_case,
    BenchmarkStatus,
)


async def main():
    """主函数：运行示例测试"""
    print("=" * 80)
    print("SherryAgent Benchmark Runner - 单个测试示例")
    print("=" * 80)
    print()

    # 创建 BenchmarkRunner，默认使用 qwen3:0.6b 模型
    runner = BenchmarkRunner(
        model="qwen3:0.6b",
        ollama_base_url="http://localhost:11434",
        log_dir="tests/benchmark/logs",
        max_tokens=1024,
        max_tool_rounds=5,
        token_budget=50_000,
    )

    # 创建测试用例
    test_case = create_simple_test_case(
        test_id="test_001",
        name="简单问候测试",
        user_prompt="你好，请介绍一下自己，用简短的几句话回答。",
        system_prompt="你是一个友好的助手，回答要简洁明了。",
        max_tokens=512,
    )

    print(f"测试 ID: {test_case.test_id}")
    print(f"测试名称: {test_case.name}")
    print(f"用户提示: {test_case.user_prompt}")
    print()
    print("-" * 80)
    print("开始执行测试...")
    print()

    # 运行测试
    result = await runner.run_test(test_case)

    print()
    print("-" * 80)
    print("测试执行完成")
    print("-" * 80)
    print(f"测试状态: {result.status.value}")
    print(f"开始时间: {result.start_time}")
    print(f"结束时间: {result.end_time}")
    print(f"总 Token 数: {result.total_tokens}")
    print(f"输入 Token 数: {result.input_tokens}")
    print(f"输出 Token 数: {result.output_tokens}")
    print()
    
    if result.log_files:
        print("日志文件:")
        for log_type, log_path in result.log_files.items():
            print(f"  - {log_type}: {log_path}")
        print()

    if result.status == BenchmarkStatus.FAILED:
        print(f"错误信息: {result.error_message}")
        print()

    if result.final_response:
        print("最终响应:")
        print("-" * 80)
        print(result.final_response)
        print("-" * 80)
        print()

    print("执行日志:")
    print("-" * 80)
    for i, log in enumerate(result.execution_logs, 1):
        content_preview = log.content[:100]
        if len(log.content) > 100:
            content_preview += "..."
        print(f"{i}. [{log.timestamp.strftime('%H:%M:%S')}] "
              f"{log.event_type.value}: {content_preview}")
    print("-" * 80)
    print()

    print("测试结果已保存到 logs 目录")


async def run_multiple_tests_example():
    """运行多个测试用例的示例"""
    print("\n" + "=" * 80)
    print("批量测试示例")
    print("=" * 80)
    print()

    runner = BenchmarkRunner(
        model="qwen3:0.6b",
        log_dir="tests/benchmark/logs",
    )

    test_cases = [
        create_simple_test_case(
            test_id="batch_001",
            name="数学计算测试",
            user_prompt="请计算 123 + 456 的结果",
        ),
        create_simple_test_case(
            test_id="batch_002",
            name="语言测试",
            user_prompt="请用英语说一句问候语",
        ),
    ]

    results = await runner.run_multiple_tests(test_cases)

    print("批量测试结果:")
    for result in results:
        print(f"  - {result.test_id}: {result.status.value}")


if __name__ == "__main__":
    try:
        # 运行单个测试示例
        asyncio.run(main())

        # 如果需要运行批量测试示例，取消下面的注释
        # asyncio.run(run_multiple_tests_example())

    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n运行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
