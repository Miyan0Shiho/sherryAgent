#!/usr/bin/env python3
"""
实际任务测试脚本

测试SherryAgent框架的完整能力：
1. 任务分解
2. 多Agent协作
3. 执行流程
4. 结果验证
"""

import asyncio
import sys
import os
from typing import List, Dict

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 直接从源码目录导入
from src.sherry_agent.llm.client import LLMClient, OllamaClient, AnthropicClient, OpenAIClient, MockLLMClient
from src.sherry_agent.orchestration.orchestrator import Orchestrator
from src.sherry_agent.orchestration.lane import LaneQueue
from src.sherry_agent.orchestration.models import SubTask, LaneConfig


async def analyze_project_task(llm_type='ollama', model='llama3'):
    """分析项目状态并生成改进建议"""
    print("=== SherryAgent 实际任务测试 ===")
    print()
    
    # 1. 初始化LLM客户端
    print(f"1. 初始化{llm_type}客户端...")
    
    if llm_type == 'ollama':
        llm_client = OllamaClient()
        print(f"   使用本地Ollama模型: {model}")
    elif llm_type == 'anthropic':
        api_key = os.environ.get('ANTHROPIC_API_KEY', 'YOUR_API_KEY')
        llm_client = AnthropicClient(api_key=api_key)
        print(f"   使用Anthropic模型: {model}")
    elif llm_type == 'openai':
        api_key = os.environ.get('OPENAI_API_KEY', 'YOUR_API_KEY')
        llm_client = OpenAIClient(api_key=api_key)
        print(f"   使用OpenAI模型: {model}")
    else:
        llm_client = MockLLMClient()
        print("   使用Mock LLM客户端")
    
    # 2. 创建任务编排器
    print("2. 创建任务编排器...")
    orchestrator = Orchestrator(llm_client)
    
    # 3. 创建Lane队列（用于任务调度）
    print("3. 创建任务执行队列...")
    lane_config = LaneConfig(max_concurrent=3)
    lane = LaneQueue(config=lane_config)
    
    # 4. 定义实际任务
    actual_task = "分析SherryAgent项目的当前状态并生成改进建议，包括：\n- 分析项目结构和代码组织\n- 评估测试覆盖率和质量\n- 检查性能瓶颈\n- 识别潜在的安全问题\n- 生成具体的改进建议和实施计划"
    
    print(f"4. 任务描述：{actual_task}")
    
    # 5. 分解任务为子任务
    print("\n5. 分解任务为子任务...")
    # 临时修改orchestrator的模型设置
    original_model = getattr(orchestrator.llm_client, 'model', 'claude-3-opus-20240229')
    if hasattr(orchestrator.llm_client, 'model'):
        orchestrator.llm_client.model = model
    
    sub_tasks = await orchestrator.decompose(actual_task, "project_analysis")
    
    # 恢复原始模型设置
    if hasattr(orchestrator.llm_client, 'model'):
        orchestrator.llm_client.model = original_model
    
    print(f"   生成了 {len(sub_tasks)} 个子任务：")
    for i, task in enumerate(sub_tasks, 1):
        deps = "无" if not task.dependencies else ", ".join(task.dependencies)
        print(f"   {i}. {task.description} (优先级: {task.priority.name}, 依赖: {deps})")
    
    # 6. 执行子任务
    print("\n6. 执行子任务...")
    print("   注意：这将调用LLM API，可能会产生费用")
    print("   预计执行时间：3-5分钟")
    
    results = await orchestrator.execute_sub_tasks(sub_tasks, lane)
    
    # 7. 展示执行结果
    print("\n7. 执行结果：")
    print("=" * 80)
    
    for task_id, result in results.items():
        task = next((t for t in sub_tasks if t.sub_task_id == task_id), None)
        if task:
            print(f"\n【{task.description}】")
            print("-" * 60)
            print(result)
            print("-" * 60)
    
    # 8. 生成综合报告
    print("\n8. 生成综合报告...")
    
    # 构建综合报告提示
    subtask_results = "\n".join([f"子任务：{task.description}\n结果：{results.get(task.sub_task_id, '无结果')}\n" for task in sub_tasks])
    report_prompt = f"""
    基于以下子任务的执行结果，生成一份综合的项目分析报告：
    
    {subtask_results}
    
    报告要求：
    1. 项目现状概述
    2. 主要问题和挑战
    3. 具体改进建议（按优先级排序）
    4. 实施计划和时间线
    5. 预期效果
    """
    
    # 生成综合报告
    report_response = await llm_client.chat(
        messages=[{"role": "user", "content": report_prompt}],
        model=model,
        max_tokens=4096
    )
    
    print("\n9. 综合分析报告：")
    print("=" * 80)
    print(report_response.content)
    print("=" * 80)
    
    # 10. 清理资源
    print("\n10. 清理资源...")
    await lane.shutdown()
    
    print("\n=== 实际任务测试完成 ===")


async def setup_environment():
    """设置测试环境"""
    print("=== 环境设置 ===")
    
    # 检查环境变量
    if 'ANTHROPIC_API_KEY' not in os.environ:
        print("提示：未设置 ANTHROPIC_API_KEY 环境变量")
        print("请在运行前设置 API 密钥，或编辑脚本中的默认值")
        print()
    
    # 检查项目结构
    print("检查项目结构...")
    if not os.path.exists('/Users/liuminxuan/Desktop/sherryAgent/src'):
        print("错误：项目结构不完整")
        return False
    
    print("环境检查完成")
    return True


if __name__ == "__main__":
    print("SherryAgent 实际任务测试")
    print("=" * 60)
    
    # 设置环境
    if not asyncio.run(setup_environment()):
        print("环境设置失败，退出测试")
        sys.exit(1)
    
    # 自动选择Ollama本地模型
    llm_type = "ollama"
    model = "qwen3:0.6b"
    
    # 运行实际任务
    print(f"\n开始执行实际任务，使用 {llm_type} 的 {model} 模型...")
    print("这将使用本地Ollama模型")
    print("预期执行时间：3-5分钟")
    
    # 自动执行
    print("自动执行测试...")
    asyncio.run(analyze_project_task(llm_type=llm_type, model=model))
