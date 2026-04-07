# Tooling Integration Tasks

## Phase 1: 工具最小契约

- [ ] Task 1.1: 定义工具输入、输出、错误、审计的最小字段
- [ ] Task 1.2: 定义只读、写入、高风险、破坏性工具分类
- [ ] Task 1.3: 定义工具与 Evidence / Decision / Cost Record 的关系

## Phase 2: 接入边界

- [ ] Task 2.1: 定义本地工具、CLI、repo 系统接入边界
- [ ] Task 2.2: 定义 MCP / 外部 API / 外部服务接入边界
- [ ] Task 2.3: 定义“工具调用”与“业务决策”的责任分离

## Phase 3: 治理与可靠性

- [ ] Task 3.1: 定义幂等、超时、重试和隔离策略
- [ ] Task 3.2: 定义外部依赖失败时的降级、回退和证据输出
- [ ] Task 3.3: 定义敏感路径、敏感环境、敏感操作的额外限制

## Phase 4: Story / Policy 对齐

- [ ] Task 4.1: 确认 5 个 Story 中所有工具动作都可落入统一分类
- [ ] Task 4.2: 确认 Policy & Guardrail 可以对所有工具分类做一致裁决
- [ ] Task 4.3: 确认高风险工具不会绕过审计或确认

