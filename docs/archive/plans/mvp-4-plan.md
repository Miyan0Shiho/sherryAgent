---
title: "MVP-4 多Agent编排 详细计划"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["mvp-roadmap.md", "mvp-3-plan.md"]
---

# MVP-4 多Agent编排 详细计划

## 目标

实现任务分解和并行执行能力，支持子Agent Fork和Lane队列。

## 实现范围

- 编排器：任务分解为子任务 + 依赖解析
- 子Agent Fork：继承系统提示 + 独立工具池
- Lane队列：session串行 + global并发控制
- 基础Agent Teams：Team Lead + Teammate协作

## 任务列表

### Week 1-2

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T1.1 | 编排器基础结构 | P0 |
| T1.2 | 任务分解实现 | P0 |
| T1.3 | 子Agent Fork实现 | P0 |
| T1.4 | Lane队列实现 | P0 |

### Week 3

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T2.1 | 子任务执行调度 | P0 |
| T2.2 | Agent Teams基础 | P1 |
| T2.3 | 集成测试 | P1 |

## 技术要点

### 任务分解

```python
class Orchestrator:
    async def decompose(self, task_description: str) -> list[SubTask]:
        """将顶层任务分解为子任务"""
        prompt = f"""
        将以下任务分解为独立的子任务，并标注依赖关系：

        任务：{task_description}

        输出格式：
        - sub_task_id: 唯一标识
        - description: 子任务描述
        - dependencies: 依赖的子任务ID列表
        """
        response = await self.llm.generate(prompt)
        return self._parse_subtasks(response)
```

### 子Agent Fork

```python
class AgentForker:
    async def fork(
        self,
        parent_context: AgentContext,
        config: ForkConfig,
    ) -> SubAgent:
        """派生子Agent"""
        # 继承系统提示前缀
        system_prompt = parent_context.system_prompt_prefix
        if config.inherit_system_prompt:
            system_prompt += parent_context.system_prompt_suffix

        # 配置独立工具池
        tools = self._filter_tools(
            parent_context.tools,
            config.inherit_tools,
            config.extra_tools,
        )

        return SubAgent(
            system_prompt=system_prompt,
            tools=tools,
            permissions=config.extra_permissions,
        )
```

### Lane队列

```python
class LaneQueue:
    async def submit(self, sub_task: SubTask) -> str:
        """提交子任务到队列"""
        ticket_id = generate_ticket_id()

        # Session级串行
        if self._session_serial:
            await self._session_queues[sub_task.session_id].put(sub_task)
        else:
            # Global级并发控制
            await self._global_queue.put(sub_task)

        return ticket_id
```

## 验收标准

| 编号 | 验收条件 | 验证方式 |
|------|---------|---------|
| 4.1 | 编排器能将复杂任务分解为合理子任务 | 人工评审 |
| 4.2 | 无依赖的子任务并行执行 | 并发测试 |
| 4.3 | 有依赖的子任务按序执行 | 顺序测试 |
| 4.4 | 子Agent继承父Agent系统提示 | 对比测试 |
| 4.5 | Lane队列并发度不超过配置上限 | 压力测试 |

## 依赖

- MVP-1 的 Agent Loop
- MVP-2 的记忆系统
- MVP-3 的自主运行
- asyncio.TaskGroup
