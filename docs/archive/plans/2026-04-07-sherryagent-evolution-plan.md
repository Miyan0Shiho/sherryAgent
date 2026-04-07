# SherryAgent 系统进化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 SherryAgent 从 demo 项目进化为完整的 AI Agent 框架，实现场景驱动的模块化架构。

**Architecture:** 采用三层架构（接入层、核心层、场景层），保留现有六层架构的核心能力，通过场景化设计提升系统实用性和扩展性。

**Tech Stack:** Python 3.12+, asyncio, Textual, anthropic/openai SDK, aiosqlite, APScheduler, pydantic-settings, structlog, pluggy, pytest

---

## 阶段一：核心能力构建（2-3周）

### 任务 1: 完善核心 Agent Loop

**Files:**
- Modify: `src/sherry_agent/execution/agent_loop.py`
- Test: `tests/unit/execution/test_agent_loop.py`

- [ ] **Step 1: 增强 Agent Loop 执行流程**

```python
# src/sherry_agent/execution/agent_loop.py
async def agent_loop(self, task: str, context: dict = None) -> str:
    """增强的 Agent Loop 执行流程"""
    # 初始化上下文
    context = context or {}
    # 循环执行
    for step in range(self.max_steps):
        # 构建提示
        prompt = self.build_prompt(task, context)
        # 调用 LLM
        response = await self.llm_client.generate(prompt)
        # 解析响应
        action = self.parse_response(response)
        # 执行操作
        result = await self.execute_action(action, context)
        # 更新上下文
        context = self.update_context(context, result)
        # 检查是否完成
        if self.is_complete(result):
            return result
    return "任务执行超时"
```

- [ ] **Step 2: 编写测试用例**

```python
# tests/unit/execution/test_agent_loop.py
def test_agent_loop_basic():
    # 测试基本执行流程
    agent = AgentLoop()
    result = await agent.agent_loop("测试任务")
    assert isinstance(result, str)
```

- [ ] **Step 3: 运行测试验证**

Run: `pytest tests/unit/execution/test_agent_loop.py -v`
Expected: PASS

- [ ] **Step 4: 提交代码**

```bash
git add src/sherry_agent/execution/agent_loop.py tests/unit/execution/test_agent_loop.py
git commit -m "feat: 增强 Agent Loop 执行流程"
```

### 任务 2: 优化记忆系统

**Files:**
- Modify: `src/sherry_agent/memory/short_term.py`
- Modify: `src/sherry_agent/memory/long_term.py`
- Modify: `src/sherry_agent/memory/bridge.py`
- Test: `tests/unit/memory/test_short_term.py`
- Test: `tests/unit/memory/test_long_term.py`

- [ ] **Step 1: 实现四层压缩策略**

```python
# src/sherry_agent/memory/short_term.py
def compress_context(self, context: dict, level: int = 3) -> dict:
    """四层压缩策略"""
    if level == 0:  # 无压缩
        return context
    elif level == 1:  # 基本压缩
        return {k: v for k, v in context.items() if k in ['task', 'last_action']}
    elif level == 2:  # 中度压缩
        return {'task': context.get('task', ''), 'summary': self.summarize(context)}
    else:  # 深度压缩
        return {'task': context.get('task', ''), 'summary': self.deep_summarize(context)}
```

- [ ] **Step 2: 增强长期记忆存储**

```python
# src/sherry_agent/memory/long_term.py
async def store_memory(self, key: str, value: str, metadata: dict = None):
    """存储长期记忆"""
    metadata = metadata or {}
    # 生成向量嵌入
    embedding = await self.embedding_client.generate(value)
    # 存储到 SQLite
    await self.db.execute(
        "INSERT INTO memories (key, value, embedding, metadata) VALUES (?, ?, ?, ?)",
        (key, value, embedding, json.dumps(metadata))
    )
    await self.db.commit()
```

- [ ] **Step 3: 编写测试用例**

```python
# tests/unit/memory/test_short_term.py
def test_compress_context():
    memory = ShortTermMemory()
    context = {'task': '测试任务', 'details': '详细信息', 'last_action': '执行操作'}
    compressed = memory.compress_context(context, level=2)
    assert 'task' in compressed
    assert 'summary' in compressed
```

- [ ] **Step 4: 运行测试验证**

Run: `pytest tests/unit/memory/ -v`
Expected: PASS

- [ ] **Step 5: 提交代码**

```bash
git add src/sherry_agent/memory/ tests/unit/memory/
git commit -m "feat: 优化记忆系统"
```

### 任务 3: 完善工具调用能力

**Files:**
- Modify: `src/sherry_agent/infrastructure/tool_executor.py`
- Modify: `src/sherry_agent/infrastructure/tools/base.py`
- Test: `tests/unit/infrastructure/test_tool_executor.py`

- [ ] **Step 1: 增强工具执行器**

```python
# src/sherry_agent/infrastructure/tool_executor.py
async def execute_tool(self, tool_name: str, parameters: dict) -> dict:
    """增强的工具执行"""
    # 检查工具是否存在
    if tool_name not in self.tools:
        return {"error": f"工具不存在: {tool_name}"}
    
    # 权限检查
    if not await self.permission_checker.check_tool_access(tool_name, parameters):
        return {"error": "权限不足"}
    
    # 执行工具
    try:
        tool = self.tools[tool_name]
        result = await tool.execute(parameters)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
```

- [ ] **Step 2: 编写测试用例**

```python
# tests/unit/infrastructure/test_tool_executor.py
def test_execute_tool():
    executor = ToolExecutor()
    result = await executor.execute_tool("file_read", {"file_path": "test.txt"})
    assert isinstance(result, dict)
```

- [ ] **Step 3: 运行测试验证**

Run: `pytest tests/unit/infrastructure/test_tool_executor.py -v`
Expected: PASS

- [ ] **Step 4: 提交代码**

```bash
git add src/sherry_agent/infrastructure/tool_executor.py src/sherry_agent/infrastructure/tools/base.py tests/unit/infrastructure/test_tool_executor.py
git commit -m "feat: 完善工具调用能力"
```

### 任务 4: 强化安全权限体系

**Files:**
- Modify: `src/sherry_agent/infrastructure/security/checker.py`
- Modify: `src/sherry_agent/infrastructure/security/rules.py`
- Test: `tests/unit/infrastructure/security/test_checker.py`

- [ ] **Step 1: 实现六层权限管道**

```python
# src/sherry_agent/infrastructure/security/checker.py
async def check_tool_access(self, tool_name: str, parameters: dict) -> bool:
    """六层权限检查"""
    # 1. 工具白名单检查
    if not self._check_whitelist(tool_name):
        return False
    
    # 2. 参数验证
    if not self._validate_parameters(tool_name, parameters):
        return False
    
    # 3. 路径安全检查
    if not self._check_path_safety(parameters):
        return False
    
    # 4. 命令安全检查
    if not self._check_command_safety(parameters):
        return False
    
    # 5. 资源限制检查
    if not self._check_resource_limits(tool_name, parameters):
        return False
    
    # 6. 审计日志
    self._log_access(tool_name, parameters)
    
    return True
```

- [ ] **Step 2: 编写测试用例**

```python
# tests/unit/infrastructure/security/test_checker.py
def test_check_tool_access():
    checker = PermissionChecker()
    result = await checker.check_tool_access("file_read", {"file_path": "test.txt"})
    assert result is True
```

- [ ] **Step 3: 运行测试验证**

Run: `pytest tests/unit/infrastructure/security/test_checker.py -v`
Expected: PASS

- [ ] **Step 4: 提交代码**

```bash
git add src/sherry_agent/infrastructure/security/ tests/unit/infrastructure/security/
git commit -m "feat: 强化安全权限体系"
```

## 阶段二：场景能力开发（4-6周）

### 任务 5: 开发开发辅助场景模块

**Files:**
- Create: `src/sherry_agent/scenes/dev_assist/__init__.py`
- Create: `src/sherry_agent/scenes/dev_assist/code_generator.py`
- Create: `src/sherry_agent/scenes/dev_assist/code_reviewer.py`
- Create: `src/sherry_agent/scenes/dev_assist/doc_generator.py`
- Test: `tests/unit/scenes/test_dev_assist.py`

- [ ] **Step 1: 创建开发辅助场景模块**

```python
# src/sherry_agent/scenes/dev_assist/__init__.py
from .code_generator import CodeGenerator
from .code_reviewer import CodeReviewer
from .doc_generator import DocGenerator

class DevAssistScene:
    """开发辅助场景"""
    def __init__(self):
        self.code_generator = CodeGenerator()
        self.code_reviewer = CodeReviewer()
        self.doc_generator = DocGenerator()
    
    async def handle_task(self, task: str, context: dict = None) -> str:
        """处理开发辅助任务"""
        # 根据任务类型选择处理方法
        if "生成代码" in task or "code" in task.lower():
            return await self.code_generator.generate(task, context)
        elif "审查代码" in task or "review" in task.lower():
            return await self.code_reviewer.review(task, context)
        elif "生成文档" in task or "doc" in task.lower():
            return await self.doc_generator.generate(task, context)
        else:
            return "无法识别的开发辅助任务"
```

- [ ] **Step 2: 实现代码生成功能**

```python
# src/sherry_agent/scenes/dev_assist/code_generator.py
class CodeGenerator:
    """代码生成器"""
    async def generate(self, task: str, context: dict = None) -> str:
        """生成代码"""
        # 实现代码生成逻辑
        return f"生成的代码: {task}"
```

- [ ] **Step 3: 编写测试用例**

```python
# tests/unit/scenes/test_dev_assist.py
def test_dev_assist_scene():
    scene = DevAssistScene()
    result = await scene.handle_task("生成一个Python函数")
    assert isinstance(result, str)
```

- [ ] **Step 4: 运行测试验证**

Run: `pytest tests/unit/scenes/test_dev_assist.py -v`
Expected: PASS

- [ ] **Step 5: 提交代码**

```bash
git add src/sherry_agent/scenes/dev_assist/ tests/unit/scenes/test_dev_assist.py
git commit -m "feat: 开发开发辅助场景模块"
```

### 任务 6: 开发数据分析场景模块

**Files:**
- Create: `src/sherry_agent/scenes/data_analysis/__init__.py`
- Create: `src/sherry_agent/scenes/data_analysis/data_processor.py`
- Create: `src/sherry_agent/scenes/data_analysis/visualizer.py`
- Create: `src/sherry_agent/scenes/data_analysis/insight_generator.py`
- Test: `tests/unit/scenes/test_data_analysis.py`

- [ ] **Step 1: 创建数据分析场景模块**

```python
# src/sherry_agent/scenes/data_analysis/__init__.py
from .data_processor import DataProcessor
from .visualizer import Visualizer
from .insight_generator import InsightGenerator

class DataAnalysisScene:
    """数据分析场景"""
    def __init__(self):
        self.data_processor = DataProcessor()
        self.visualizer = Visualizer()
        self.insight_generator = InsightGenerator()
    
    async def handle_task(self, task: str, context: dict = None) -> str:
        """处理数据分析任务"""
        # 根据任务类型选择处理方法
        if "处理数据" in task or "process" in task.lower():
            return await self.data_processor.process(task, context)
        elif "可视化" in task or "visual" in task.lower():
            return await self.visualizer.visualize(task, context)
        elif "分析" in task or "insight" in task.lower():
            return await self.insight_generator.generate(task, context)
        else:
            return "无法识别的数据分析任务"
```

- [ ] **Step 2: 实现数据处理功能**

```python
# src/sherry_agent/scenes/data_analysis/data_processor.py
class DataProcessor:
    """数据处理器"""
    async def process(self, task: str, context: dict = None) -> str:
        """处理数据"""
        # 实现数据处理逻辑
        return f"处理的数据: {task}"
```

- [ ] **Step 3: 编写测试用例**

```python
# tests/unit/scenes/test_data_analysis.py
def test_data_analysis_scene():
    scene = DataAnalysisScene()
    result = await scene.handle_task("处理CSV数据")
    assert isinstance(result, str)
```

- [ ] **Step 4: 运行测试验证**

Run: `pytest tests/unit/scenes/test_data_analysis.py -v`
Expected: PASS

- [ ] **Step 5: 提交代码**

```bash
git add src/sherry_agent/scenes/data_analysis/ tests/unit/scenes/test_data_analysis.py
git commit -m "feat: 开发数据分析场景模块"
```

### 任务 7: 开发自动化运维场景模块

**Files:**
- Create: `src/sherry_agent/scenes/auto_ops/__init__.py`
- Create: `src/sherry_agent/scenes/auto_ops/monitor.py`
- Create: `src/sherry_agent/scenes/auto_ops/troubleshooter.py`
- Create: `src/sherry_agent/scenes/auto_ops/maintenance.py`
- Test: `tests/unit/scenes/test_auto_ops.py`

- [ ] **Step 1: 创建自动化运维场景模块**

```python
# src/sherry_agent/scenes/auto_ops/__init__.py
from .monitor import Monitor
from .troubleshooter import Troubleshooter
from .maintenance import Maintenance

class AutoOpsScene:
    """自动化运维场景"""
    def __init__(self):
        self.monitor = Monitor()
        self.troubleshooter = Troubleshooter()
        self.maintenance = Maintenance()
    
    async def handle_task(self, task: str, context: dict = None) -> str:
        """处理自动化运维任务"""
        # 根据任务类型选择处理方法
        if "监控" in task or "monitor" in task.lower():
            return await self.monitor.monitor(task, context)
        elif "排查" in task or "troubleshoot" in task.lower():
            return await self.troubleshooter.troubleshoot(task, context)
        elif "维护" in task or "maintain" in task.lower():
            return await self.maintenance.maintain(task, context)
        else:
            return "无法识别的自动化运维任务"
```

- [ ] **Step 2: 实现监控功能**

```python
# src/sherry_agent/scenes/auto_ops/monitor.py
class Monitor:
    """系统监控"""
    async def monitor(self, task: str, context: dict = None) -> str:
