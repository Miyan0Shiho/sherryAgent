---
title: "MVP-5 Skill插件与生态 详细计划"
status: approved
created: 2026-04-03
updated: 2026-04-03
related: ["mvp-roadmap.md", "mvp-4-plan.md"]
---

# MVP-5 Skill插件与生态 详细计划

## 目标

实现插件化能力扩展，支持动态加载Skill和连接MCP工具服务器。

## 实现范围

- 插件系统：基于pluggy的hook机制
- Skill加载：SKILL.md描述 + 门控检查 + 热加载/卸载
- MCP客户端：连接外部MCP工具服务器
- 权限系统完善：补充第3-5层

## 任务列表

### Week 1

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T1.1 | 插件系统基础 | P0 |
| T1.2 | Skill加载实现 | P0 |
| T1.3 | MCP客户端实现 | P0 |

### Week 2

| 任务 | 描述 | 优先级 |
|------|------|--------|
| T2.1 | 自动模式分类器 | P0 |
| T2.2 | 用户配置规则 | P0 |
| T2.3 | 企业策略支持 | P1 |
| T2.4 | 集成测试 | P1 |

## 技术要点

### 插件Hook规范

```python
import pluggy

hookspec = pluggy.HookspecMarker("sherry_agent")
hookimpl = pluggy.HookimplMarker("sherry_agent")

class SkillSpec:
    @hookspec
    def on_load(self) -> dict:
        """Skill加载时调用，返回工具定义"""
        pass

    @hookspec
    def on_unload(self) -> None:
        """Skill卸载时调用"""
        pass

    @hookspec
    def get_tools(self) -> list[Tool]:
        """返回Skill提供的工具列表"""
        pass
```

### SKILL.md 格式

```markdown
# Skill: GitHub Operations

## Description
提供GitHub仓库操作能力，包括创建PR、查看Issue等。

## Trigger Conditions
- 用户询问GitHub相关操作
- 用户提到PR、Issue、Repository等关键词

## Gate Conditions
- 需要配置 GITHUB_TOKEN 环境变量
- 需要安装 gh CLI 工具

## Tools
- create_pr: 创建Pull Request
- list_issues: 列出Issues
- review_pr: 审查Pull Request

## Examples
用户: "帮我创建一个PR"
Agent: 调用 create_pr 工具，参数: {title, body, base, head}
```

### MCP客户端

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def connect_mcp_server(command: str, args: list[str]):
    """连接MCP工具服务器"""
    server_params = StdioServerParameters(
        command=command,
        args=args,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            return tools
```

### 自动模式分类器

```python
class AutoPermissionClassifier:
    async def classify(self, request: PermissionRequest) -> RiskLevel:
        """使用LLM判断操作风险等级"""
        prompt = f"""
        判断以下操作的风险等级（低/中/高/严重）：

        工具: {request.tool_name}
        操作: {request.operation}
        目标: {request.target_path}
        上下文: {request.context}

        风险等级定义：
        - 低: 只读操作，无副作用
        - 中: 写入操作，可恢复
        - 高: 删除操作，不可恢复
        - 严重: 系统级操作，影响范围大
        """
        response = await self.llm.generate(prompt)
        return RiskLevel(response.strip())
```

## 验收标准

| 编号 | 验收条件 | 验证方式 |
|------|---------|---------|
| 5.1 | 运行时动态加载Skill插件 | 手动测试 |
| 5.2 | Skill卸载后Agent不再调用相关工具 | 回归测试 |
| 5.3 | MCP客户端成功连接外部工具服务器 | 集成测试 |
| 5.4 | 自动模式分类器正确判断风险等级 | 单元测试 |
| 5.5 | 用户配置规则正确生效 | 配置测试 |

## 依赖

- MVP-1 至 MVP-4 全部完成
- pluggy >= 1.5
- mcp >= 1.0
