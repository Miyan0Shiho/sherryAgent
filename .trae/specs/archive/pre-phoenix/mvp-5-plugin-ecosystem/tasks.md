# SherryAgent - MVP-5 Skill插件与生态 实现计划

## [ ] Task 1: 插件系统基础
- **Priority**: P0
- **Depends On**: MVP-1, MVP-2, MVP-3, MVP-4
- **Description**:
  - 集成pluggy框架
  - 定义Hook规范
  - 实现PluginManager类
- **Acceptance Criteria Addressed**: FR-1
- **Test Requirements**:
  - `programmatic` TR-1.1: pluggy框架集成正确
  - `programmatic` TR-1.2: Hook规范定义完整

## [ ] Task 2: Skill加载实现
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 实现SKILL.md解析
  - 实现门控条件检查
  - 实现Skill生命周期管理
  - 实现热加载/卸载
- **Acceptance Criteria Addressed**: FR-2, AC-1, AC-2
- **Test Requirements**:
  - `manual-test` TR-2.1: 动态加载Skill无需重启
  - `regression-test` TR-2.2: Skill卸载后工具不可调用

## [ ] Task 3: MCP客户端实现
- **Priority**: P0
- **Depends On**: MVP-1
- **Description**:
  - 集成MCP SDK
  - 实现MCP连接管理
  - 实现工具发现和调用
  - 实现错误处理和重连
- **Acceptance Criteria Addressed**: FR-3, AC-3
- **Test Requirements**:
  - `integration-test` TR-3.1: MCP连接成功
  - `programmatic` TR-3.2: 工具发现和调用正确

## [ ] Task 4: 自动模式分类器
- **Priority**: P0
- **Depends On**: MVP-1
- **Description**:
  - 实现RiskLevel枚举
  - 实现LLM驱动的风险判断
  - 实现PermissionDecision决策
  - 集成到权限管道
- **Acceptance Criteria Addressed**: FR-4, AC-4
- **Test Requirements**:
  - `unit-test` TR-4.1: 风险等级判断正确
  - `programmatic` TR-4.2: 权限管道集成正确

## [ ] Task 5: 用户配置规则
- **Priority**: P0
- **Depends On**: Task 4
- **Description**:
  - 设计配置文件格式
  - 实现配置解析和验证
  - 实现Glob模式匹配
  - 集成到权限管道
- **Acceptance Criteria Addressed**: FR-4, AC-5
- **Test Requirements**:
  - `config-test` TR-5.1: 用户配置规则生效
  - `programmatic` TR-5.2: Glob模式匹配正确

## [ ] Task 6: 企业策略支持
- **Priority**: P1
- **Depends On**: Task 5
- **Description**:
  - 设计企业策略配置格式
  - 实现策略加载和验证
  - 实现策略优先级
  - 集成到权限管道
- **Acceptance Criteria Addressed**: FR-4
- **Test Requirements**:
  - `programmatic` TR-6.1: 企业策略正确加载
  - `programmatic` TR-6.2: 策略优先级正确

## [ ] Task 7: 集成测试
- **Priority**: P1
- **Depends On**: All Tasks
- **Description**:
  - 编写插件系统测试
  - 编写MCP集成测试
  - 编写权限系统测试
  - 性能优化
- **Acceptance Criteria Addressed**: All ACs
- **Test Requirements**:
  - `programmatic` TR-7.1: 所有测试通过
  - `programmatic` TR-7.2: 性能满足要求

## Task Dependencies
- Task 2 depends on Task 1
- Task 5 depends on Task 4
- Task 6 depends on Task 5
- Task 7 depends on all other tasks
