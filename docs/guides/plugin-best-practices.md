---
title: "插件开发最佳实践"
status: approved
created: 2026-04-04
updated: 2026-04-04
---

# 插件开发最佳实践

本文档提供 SherryAgent 插件开发的最佳实践，帮助开发者创建高质量、安全可靠的插件。

## 1. 命名规范

### 1.1 插件命名
- **插件名称**：使用小写字母和连字符（例如：`weather-plugin`）
- **插件类名**：使用驼峰命名法（例如：`WeatherPlugin`）
- **版本号**：遵循语义化版本规范（例如：`1.0.0`）

### 1.2 工具命名
- **工具名称**：使用小写字母和下划线（例如：`get_weather`）
- **工具类名**：使用驼峰命名法（例如：`WeatherTool`）
- **参数名称**：使用小写字母和下划线，保持简洁明了

### 1.3 文件命名
- **插件文件**：使用小写字母和下划线（例如：`weather_plugin.py`）
- **工具文件**：使用小写字母和下划线（例如：`weather_tool.py`）
- **目录结构**：保持层次清晰，使用有意义的目录名称

## 2. 代码质量

### 2.1 类型标注
- 使用 Python 类型提示标注函数参数和返回值
- 为复杂类型创建类型别名
- 确保类型标注的一致性和准确性

### 2.2 文档
- 为插件和工具提供详细的文档字符串
- 使用 NumPy 风格的文档格式
- 文档应包括：
  - 插件/工具的功能描述
  - 参数说明
  - 返回值说明
  - 示例用法

### 2.3 代码风格
- 遵循 PEP 8 代码风格规范
- 使用 4 个空格进行缩进
- 保持代码行长度不超过 100 字符
- 合理使用空行分隔代码块

## 3. 安全性

### 3.1 输入验证
- 对所有用户输入进行验证
- 使用类型检查和边界检查
- 避免使用 `eval()` 等危险函数

### 3.2 权限管理
- 明确声明插件和工具所需的权限
- 遵循最小权限原则
- 对敏感操作进行权限检查

### 3.3 敏感信息
- 避免硬编码敏感信息（如 API 密钥）
- 使用环境变量存储配置
- 对敏感数据进行加密处理

### 3.4 安全审计
- 定期进行安全审计
- 检查潜在的安全漏洞
- 遵循安全最佳实践

## 4. 性能优化

### 4.1 异步操作
- 使用 `async/await` 进行异步操作
- 避免阻塞性操作
- 合理使用 `asyncio.gather()` 进行并行操作

### 4.2 缓存
- 对频繁访问的数据使用缓存
- 设置合理的缓存过期时间
- 避免缓存过大的数据

### 4.3 资源管理
- 合理管理文件句柄和网络连接
- 使用 `with` 语句确保资源正确释放
- 避免内存泄漏

### 4.4 代码优化
- 避免重复计算
- 优化算法复杂度
- 使用适当的数据结构

## 5. 错误处理

### 5.1 异常处理
- 使用 `try/except` 捕获异常
- 避免捕获所有异常
- 抛出有意义的异常信息

### 5.2 错误信息
- 提供清晰、准确的错误信息
- 包含足够的上下文信息
- 避免泄露敏感信息

### 5.3 日志记录
- 使用 `structlog` 进行结构化日志记录
- 记录关键操作和错误信息
- 避免过度日志

## 6. 插件结构

### 6.1 目录结构
```
my-plugin/
├── pyproject.toml        # 项目配置
├── README.md              # 插件说明
├── src/
│   └── my_plugin/
│       ├── __init__.py    # 插件入口
│       ├── tools/         # 工具实现
│       └── utils/         # 工具函数
```

### 6.2 插件类结构
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
        return "插件描述"
    
    def get_tools(self) -> list:
        return [Tool1(), Tool2()]
```

### 6.3 工具实现
- 可以通过继承 `BaseTool` 类实现
- 也可以使用 `@tool` 装饰器定义
- 确保工具参数定义清晰

## 7. 测试

### 7.1 单元测试
- 为插件和工具编写单元测试
- 测试边界情况
- 模拟外部依赖

### 7.2 集成测试
- 测试插件与 SherryAgent 的集成
- 测试插件间的依赖关系
- 测试插件在不同环境中的表现

### 7.3 测试覆盖率
- 目标覆盖率：80% 以上
- 重点测试核心功能
- 定期运行测试套件

## 8. 发布与维护

### 8.1 打包
- 使用 `pyproject.toml` 配置项目
- 定义清晰的依赖关系
- 使用标准的打包流程

### 8.2 发布
- 发布到 PyPI
- 提供详细的发布说明
- 维护发布历史

### 8.3 版本管理
- 遵循语义化版本规范
- 记录版本变更
- 向后兼容旧版本

### 8.4 维护
- 定期更新依赖
- 修复安全漏洞
- 响应用户反馈

## 9. 最佳实践示例

### 9.1 基础插件示例

```python
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
        return f"Hello, {name}!"

@plugin
class HelloPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "hello-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "一个示例插件"
    
    def get_tools(self) -> list:
        return [GreetTool()]
```

### 9.2 高级插件示例

```python
from sherry_agent.plugins.sdk import BasePlugin, tool, plugin
import aiohttp
import os

@plugin
class WeatherPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "weather-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "天气查询插件"
    
    @property
    def dependencies(self) -> list:
        return ["aiohttp"]
    
    @tool(
        name="get_weather",
        description="获取城市天气",
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    )
    async def get_weather(self, city: str) -> dict:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            raise ValueError("WEATHER_API_KEY 环境变量未设置")
        
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"API 请求失败: {response.status}")
                return await response.json()
    
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
```

## 10. 故障排除

### 10.1 常见问题

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

### 10.2 调试技巧

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

4. **使用交互式调试**：
   - 使用 `breakpoint()` 设置断点
   - 使用 `pdb` 进行交互式调试
   - 检查变量值和执行流程

## 11. 贡献指南

### 11.1 提交插件

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

### 11.2 插件注册表

提交你的插件到 SherryAgent 插件注册表，让其他用户可以发现和使用你的插件。

## 12. 结论

遵循这些最佳实践，你可以创建高质量、安全可靠的 SherryAgent 插件。插件系统为 SherryAgent 提供了无限的