---
title: "插件开发指南"
status: approved
created: 2026-04-04
updated: 2026-04-04
---

# 插件开发指南

本指南详细介绍如何为 SherryAgent 开发插件，包括插件SDK的使用、插件结构、工具开发和最佳实践。

## 1. 插件系统概述

SherryAgent 插件系统基于 `pluggy` 框架，提供了以下功能：

- 插件热加载和卸载
- 工具注册和管理
- 事件钩子系统
- 技能系统集成

## 2. 开发环境设置

### 2.1 安装依赖

```bash
# 安装 SherryAgent 及其开发依赖
uv sync --extra dev
```

### 2.2 项目结构

推荐的插件项目结构：

```
my-plugin/
├── pyproject.toml        # 项目配置
├── README.md              # 插件说明
├── src/
│   └── my_plugin/
│       ├── __init__.py    # 插件入口
│       └── tools/         # 工具实现
```

## 3. 插件开发SDK

### 3.1 导入SDK

```python
from sherry_agent.plugins.sdk import BasePlugin, BaseTool, ToolDefinition, plugin, tool
```

### 3.2 创建插件类

#### 基本插件

```python
from sherry_agent.plugins.sdk import BasePlugin, plugin

@plugin
class MyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "my-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "我的第一个SherryAgent插件"
    
    @property
    def dependencies(self) -> list:
        return []
```

#### 带工具的插件

```python
from sherry_agent.plugins.sdk import BasePlugin, BaseTool, plugin

class HelloTool(BaseTool):
    @property
    def name(self) -> str:
        return "hello"
    
    @property
    def description(self) -> str:
        return "向世界问好"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "要问候的名字"
                }
            },
            "required": ["name"]
        }
    
    async def execute(self, name: str) -> str:
        return f"Hello, {name}!"

@plugin
class MyPlugin(BasePlugin):
    # ... 基本属性定义 ...
    
    def get_tools(self) -> list:
        return [HelloTool()]
```

### 3.3 使用装饰器定义工具

```python
from sherry_agent.plugins.sdk import BasePlugin, plugin, tool

@plugin
class MyPlugin(BasePlugin):
    # ... 基本属性定义 ...
    
    @tool(
        name="greet",
        description="向用户打招呼",
        parameters={
            "type": "object",
            "properties": {
                "user": {
                    "type": "string",
                    "description": "用户名"
                }
            },
            "required": ["user"]
        }
    )
    async def greet_tool(self, user: str) -> str:
        return f"Hello, {user}! Welcome to SherryAgent!"
    
    def get_tools(self) -> list:
        # 从类中提取装饰的工具
        tools = []
        for name in dir(self):
            attr = getattr(self, name)
            if hasattr(attr, "__tool_name__"):
                from sherry_agent.plugins.sdk.tools import ToolDefinition
                tool_def = ToolDefinition(
                    name=attr.__tool_name__,
                    description=attr.__tool_description__,
                    parameters=attr.__tool_parameters__,
                    permissions=attr.__tool_permissions__,
                    func=attr
                )
                tools.append(tool_def)
        return tools
```

## 4. 事件钩子

插件可以响应以下事件：

```python
from sherry_agent.plugins.sdk import BasePlugin, plugin

@plugin
class MyPlugin(BasePlugin):
    # ... 基本属性定义 ...
    
    def agent_started(self, agent_id: str, config: dict) -> None:
        """Agent启动时触发"""
        print(f"Agent {agent_id} started with config: {config}")
    
    def agent_stopped(self, agent_id: str, status: str) -> None:
        """Agent停止时触发"""
        print(f"Agent {agent_id} stopped with status: {status}")
    
    def plugin_enabled(self, plugin) -> None:
        """插件启用时触发"""
        print(f"Plugin {plugin.name} enabled")
    
    def plugin_disabled(self, plugin) -> None:
        """插件禁用时触发"""
        print(f"Plugin {plugin.name} disabled")
```

## 5. 插件打包与发布

### 5.1 配置 pyproject.toml

```toml
[project]
name = "my-plugin"
version = "1.0.0"
description = "我的SherryAgent插件"
requires-python = ">=3.12"

[project.dependencies]
sherry-agent = ">=0.1.0"

[project.entry-points.sherry_agent.plugins]
my_plugin = "my_plugin:MyPlugin"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 5.2 安装插件

```bash
# 从本地安装
uv add -e .

# 从 PyPI 安装
uv add my-plugin
```

## 6. 技能系统

### 6.1 创建技能

创建 `SKILL.md` 文件：

```markdown
# 天气查询
version: 1.0.0
description: 查询指定城市的天气信息

## Dependencies
- requests

## Triggers
- keyword: "天气"
- keyword: "temperature"

## Entry Point
weather_tool.py:WeatherTool

## Environment Variables
API_KEY=your_api_key
```

### 6.2 技能实现

```python
# weather_tool.py
import os
import requests
from sherry_agent.plugins.sdk import BaseTool

class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather"
    
    @property
    def description(self) -> str:
        return "查询天气信息"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    
    async def execute(self, city: str) -> dict:
        api_key = os.getenv("API_KEY")
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url)
        return response.json()
```

## 7. 最佳实践

### 7.1 插件开发最佳实践

1. **命名规范**：
   - 插件名称使用小写字母和连字符
   - 工具名称使用小写字母和下划线
   - 类名使用驼峰命名法

2. **错误处理**：
   - 使用 `PluginError` 和 `ToolError` 异常类
   - 提供清晰的错误信息
   - 避免在插件中捕获所有异常

3. **性能优化**：
   - 避免在 `get_tools` 中执行耗时操作
   - 使用异步方法提高性能
   - 合理使用缓存

4. **安全性**：
   - 避免硬编码敏感信息
   - 使用环境变量存储配置
   - 实现适当的权限检查

5. **文档**：
   - 为插件和工具提供详细的文档
   - 使用类型提示
   - 提供示例代码

### 7.2 工具开发最佳实践

1. **参数定义**：
   - 使用清晰的参数名称
   - 提供详细的参数描述
   - 定义合理的默认值

2. **返回值**：
   - 返回结构化数据
   - 避免返回过大的数据
   - 提供一致的返回格式

3. **测试**：
   - 为工具编写单元测试
   - 测试边界情况
   - 模拟外部依赖

4. **日志**：
   - 使用结构化日志
   - 记录关键操作
   - 避免过度日志

## 8. 示例插件

### 8.1 基础示例

```python
# src/my_plugin/__init__.py
from sherry_agent.plugins.sdk import BasePlugin, BaseTool, plugin

class GreetTool(BaseTool):
    @property
    def name(self) -> str:
        return "greet"
    
    @property
    def description(self) -> str:
        return "向用户打招呼"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "用户名称"
                }
            },
            "required": ["name"]
        }
    
    async def execute(self, name: str) -> str:
        return f"Hello, {name}! Welcome to SherryAgent!"

@plugin
class MyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "my-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "一个示例插件"
    
    def get_tools(self) -> list:
        return [GreetTool()]
```

### 8.2 高级示例

```python
# src/advanced_plugin/__init__.py
from sherry_agent.plugins.sdk import BasePlugin, tool, plugin
import requests

@plugin
class AdvancedPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "advanced-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "高级功能插件"
    
    @tool(
        name="get_joke",
        description="获取一个笑话",
        parameters={
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "笑话类别",
                    "enum": ["general", "programming", "knock-knock"]
                }
            },
            "required": ["category"]
        }
    )
    async def get_joke(self, category: str) -> str:
        url = f"https://api.chucknorris.io/jokes/random?category={category}"
        response = requests.get(url)
        data = response.json()
        return data["value"]
    
    @tool(
        name="calculate",
        description="执行数学计算",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式"
                }
            },
            "required": ["expression"]
        }
    )
    async def calculate(self, expression: str) -> float:
        # 注意：在生产环境中应该使用更安全的计算方法
        return eval(expression)
    
    def get_tools(self) -> list:
        tools = []
        for name in dir(self):
            attr = getattr(self, name)
            if hasattr(attr, "__tool_name__"):
                from sherry_agent.plugins.sdk.tools import ToolDefinition
                tool_def = ToolDefinition(
                    name=attr.__tool_name__,
                    description=attr.__tool_description__,
                    parameters=attr.__tool_parameters__,
                    permissions=attr.__tool_permissions__,
                    func=attr
                )
                tools.append(tool_def)
        return tools
    
    def agent_started(self, agent_id: str, config: dict) -> None:
        print(f"AdvancedPlugin: Agent {agent_id} started")
    
    def agent_stopped(self, agent_id: str, status: str) -> None:
        print(f"AdvancedPlugin: Agent {agent_id} stopped with status {status}")
```

## 9. 故障排除

### 9.1 常见问题

1. **插件未加载**：
   - 检查插件目录是否在配置中
   - 确保插件实现了所有必需的属性
   - 检查插件依赖是否安装

2. **工具未注册**：
   - 确保在 `get_tools` 方法中返回工具
   - 检查工具名称是否唯一
   - 验证工具参数格式是否正确

3. **技能未加载**：
   - 检查 `SKILL.md` 文件格式
   - 确保技能目录结构正确
   - 验证技能依赖是否安装

### 9.2 调试技巧

1. **启用调试模式**：
   ```bash
   uv run sherry-agent run --debug
   ```

2. **查看插件状态**：
   ```bash
   uv run sherry-agent status
   ```

3. **检查日志**：
   - 查看控制台输出
   - 检查系统日志
   - 使用 `structlog` 记录详细信息

## 10. 贡献指南

### 10.1 提交插件

1. **创建插件**：
   - 遵循本指南的最佳实践
   - 确保插件功能完整
   - 提供详细的文档

2. **测试插件**：
   - 运行单元测试
   - 测试插件在不同环境中的表现
   - 确保插件与最新版本的 SherryAgent 兼容

3. **提交代码**：
   - 创建 GitHub 仓库
   - 编写清晰的 README
   - 提交到 SherryAgent 插件注册表

### 10.2 插件注册表

提交你的插件到 SherryAgent 插件注册表，让其他用户可以发现和使用你的插件。

---

通过本指南，你应该能够成功开发和发布 SherryAgent 插件。如果有任何问题或建议，请在 GitHub 仓库中提交 Issue。