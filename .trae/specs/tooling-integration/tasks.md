# Tooling Integration Tasks

## Phase 0: Tooling Scope Alignment

### Work Packages
- [ ] P0-W1: 对齐 `permission-system.md`、`agent-loop.md`、`module-map.md` 的工具相关术语
- [ ] P0-W2: 汇总 Story 与 4 条主链路涉及的工具动作类型
- [ ] P0-W3: 列出最容易越权、最难回放、最容易高成本失控的工具类别

### Deliverables
- [ ] D0-1: 工具范围清单
- [ ] D0-2: 高风险工具清单

## Phase 1: Tool Contract Freeze

### Work Packages
- [ ] P1-W1: 定义工具输入、输出、错误、审计的最小字段
- [ ] P1-W2: 定义只读、写入、高风险、破坏性工具分类
- [ ] P1-W3: 定义工具与 Evidence / Decision / Cost Record 的关系
- [ ] P1-W4: 固定工具元数据中的超时、幂等、重试和副作用声明

### Deliverables
- [ ] D1-1: 工具最小契约表
- [ ] D1-2: 工具风险分类表

### Dependencies
- [ ] DEP1-1: `platform-foundation` 已冻结审计、风险与成本字段

## Phase 2: Integration Boundary Freeze

### Work Packages
- [ ] P2-W1: 定义本地工具、CLI、repo 系统接入边界
- [ ] P2-W2: 定义 MCP / 外部 API / 外部服务接入边界
- [ ] P2-W3: 定义“工具调用”与“业务决策”的责任分离
- [ ] P2-W4: 明确鉴权、隔离、回放、模拟运行和凭证边界

### Deliverables
- [ ] D2-1: 三类接入模型说明
- [ ] D2-2: 工具与决策责任边界矩阵

### Blockers
- [ ] B2-1: 任何一种接入方式仍然把策略判断和执行混在一起

## Phase 3: Reliability & Governance Freeze

### Work Packages
- [ ] P3-W1: 定义幂等、超时、重试和隔离策略
- [ ] P3-W2: 定义外部依赖失败时的降级、回退和证据输出
- [ ] P3-W3: 定义敏感路径、敏感环境、敏感操作的额外限制
- [ ] P3-W4: 定义高风险工具默认需要人工确认的条件

### Deliverables
- [ ] D3-1: 治理与可靠性规则表
- [ ] D3-2: 故障降级与审计说明

### Dependencies
- [ ] DEP3-1: `runtime-orchestration` 已冻结失败与恢复模板

## Phase 4: Acceptance Adoption

### Work Packages
- [ ] P4-W1: 确认 5 个 Story 中所有工具动作都可落入统一分类
- [ ] P4-W2: 确认 Policy & Guardrail 可以对所有工具分类做一致裁决
- [ ] P4-W3: 确认高风险工具不会绕过审计或确认
- [ ] P4-W4: 形成工具治理完成证明，供 `quality-evaluation` 和 `release-program` 使用

### Deliverables
- [ ] D4-1: Story-Tool 映射矩阵
- [ ] D4-2: capability gate 输入说明
