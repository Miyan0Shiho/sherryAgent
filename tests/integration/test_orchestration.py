"""多Agent编排系统集成测试"""

import asyncio
import pytest

from sherry_agent.orchestration import (
    Orchestrator,
    AgentForker,
    LaneQueue,
    TeamLead,
    Teammate,
    ForkConfig,
    LaneConfig,
    TaskStatus,
    TaskPriority,
)
from sherry_agent.orchestration.forker import AgentContext
from sherry_agent.llm.client import MockLLMClient


@pytest.mark.asyncio
async def test_orchestrator_decompose():
    """测试编排器任务分解功能"""
    # 创建Mock LLM客户端
    llm_client = MockLLMClient(["""{
        "subtasks": [
            {
                "sub_task_id": "sub1",
                "description": "分析需求",
                "priority": "HIGH",
                "dependencies": []
            },
            {
                "sub_task_id": "sub2",
                "description": "实现功能",
                "priority": "CRITICAL",
                "dependencies": ["sub1"]
            },
            {
                "sub_task_id": "sub3",
                "description": "测试验证",
                "priority": "NORMAL",
                "dependencies": ["sub2"]
            }
        ]
    }"""])

    # 创建编排器
    orchestrator = Orchestrator(llm_client)

    # 测试任务分解
    task_description = "实现用户认证功能"
    parent_task_id = "test_task"
    subtasks = await orchestrator.decompose(task_description, parent_task_id)

    # 验证结果
    assert len(subtasks) == 3
    assert subtasks[0].sub_task_id == "sub1"
    assert subtasks[0].description == "分析需求"
    assert subtasks[0].priority == TaskPriority.HIGH
    assert subtasks[0].dependencies == []

    assert subtasks[1].sub_task_id == "sub2"
    assert subtasks[1].description == "实现功能"
    assert subtasks[1].priority == TaskPriority.CRITICAL
    assert subtasks[1].dependencies == ["sub1"]

    assert subtasks[2].sub_task_id == "sub3"
    assert subtasks[2].description == "测试验证"
    assert subtasks[2].priority == TaskPriority.NORMAL
    assert subtasks[2].dependencies == ["sub2"]


@pytest.mark.asyncio
async def test_lane_queue_concurrency():
    """测试Lane队列的并发控制"""
    # 创建Lane队列配置
    config = LaneConfig(max_concurrent=2)
    lane = LaneQueue(config)

    # 创建测试子任务
    from sherry_agent.orchestration import SubTask
    tasks = []
    for i in range(5):
        task = SubTask(
            sub_task_id=f"task_{i}",
            description=f"测试任务 {i}",
            parent_task_id="test_parent"
        )
        tasks.append(task)

    # 提交任务
    tickets = []
    for task in tasks:
        ticket_id = await lane.submit(task)
        tickets.append(ticket_id)

    # 等待所有任务完成
    results = []
    for ticket_id in tickets:
        result = await lane.wait_for_result(ticket_id)
        results.append(result)

    # 验证所有任务都已完成
    for result in results:
        assert result.status == TaskStatus.COMPLETED

    # 关闭队列
    await lane.shutdown()


@pytest.mark.asyncio
async def test_agent_fork():
    """测试子Agent Fork功能"""
    # 创建父Agent上下文
    parent_context = AgentContext(
        system_prompt_prefix="You are a helpful assistant",
        system_prompt_suffix="Please be concise.",
        tools=["tool1", "tool2", "tool3"],
        permissions=["read", "write"]
    )

    # 创建Fork配置
    config = ForkConfig(
        inherit_system_prompt=True,
        inherit_tools=["tool1", "tool3"],
        extra_tools=["tool4"],
        extra_permissions=["execute"]
    )

    # 创建AgentForker
    forker = AgentForker()

    # 派生子Agent
    sub_agent = await forker.fork(parent_context, config)

    # 验证结果
    assert sub_agent.system_prompt == "You are a helpful assistantPlease be concise."
    assert len(sub_agent.tools) == 3  # 2 inherited + 1 extra
    assert "tool1" in sub_agent.tools
    assert "tool3" in sub_agent.tools
    assert "tool4" in sub_agent.tools
    assert len(sub_agent.permissions) == 3  # 2 inherited + 1 extra
    assert "read" in sub_agent.permissions
    assert "write" in sub_agent.permissions
    assert "execute" in sub_agent.permissions


@pytest.mark.asyncio
async def test_agent_teams():
    """测试Agent Teams功能"""
    # 创建Mock LLM客户端
    llm_client = MockLLMClient(["""{
        "subtasks": [
            {
                "sub_task_id": "sub1",
                "description": "分析代码",
                "priority": "HIGH",
                "dependencies": []
            }
        ]
    }"""])

    # 创建编排器和Lane队列
    orchestrator = Orchestrator(llm_client)
    lane_config = LaneConfig(max_concurrent=3)
    lane = LaneQueue(lane_config)

    # 创建Team Lead和Teammate
    team_lead = TeamLead(orchestrator, lane)
    teammate = Teammate("teammate1")
    team_lead.add_teammate("teammate1", teammate)

    # 分配任务
    result = await team_lead.assign_task("分析代码库中的认证模块", "teammate1")
    assert "任务已分配给Teammate teammate1" in result

    # 等待任务完成
    await asyncio.sleep(1.5)  # 等待任务执行

    # 监控进度
    progress = await team_lead.monitor_progress()
    assert len(progress) > 0

    # 关闭队列
    await lane.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_execute_sub_tasks():
    """测试编排器执行子任务功能"""
    # 创建Mock LLM客户端
    llm_client = MockLLMClient()

    # 创建编排器和Lane队列
    orchestrator = Orchestrator(llm_client)
    lane_config = LaneConfig(max_concurrent=3)
    lane = LaneQueue(lane_config)

    # 创建测试子任务
    from sherry_agent.orchestration import SubTask
    subtasks = [
        SubTask(
            sub_task_id="sub1",
            description="任务1",
            parent_task_id="test_parent"
        ),
        SubTask(
            sub_task_id="sub2",
            description="任务2",
            parent_task_id="test_parent",
            dependencies=["sub1"]
        ),
        SubTask(
            sub_task_id="sub3",
            description="任务3",
            parent_task_id="test_parent",
            dependencies=["sub2"]
        )
    ]

    # 执行子任务
    results = await orchestrator.execute_sub_tasks(subtasks, lane)

    # 验证结果
    assert len(results) == 3
    assert "sub1" in results
    assert "sub2" in results
    assert "sub3" in results

    # 关闭队列
    await lane.shutdown()