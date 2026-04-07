---
title: "OpenSpec 集成指南"
status: approved
created: 2026-04-07
updated: 2026-04-07
related: ["sdd-workflow.md"]
---

# OpenSpec 集成指南

> **定位声明（SherryAgent 专用）**：OpenSpec 在本项目中是“规范驱动开发（SDD）的方法论与模板参考”，用于提升写规范的结构化程度；它**不是**本项目的权威规范来源。
>
> - 开发执行权威：`.trae/specs/*`
> - 系统契约与叙事权威：`docs/*`
> - 冲突裁决规则见：[spec-authority.md](spec-authority.md)

## 什么是 OpenSpec？

OpenSpec 是一个轻量级的规范驱动开发（Spec-Driven Development, SDD）框架，专为 AI 编码助手设计。它通过在写代码之前先定义和确认规范（Spec），让 AI 的输出从"不可预测"变为"可预期、可审查、可追溯"。

**核心价值**：
- **减少返工**：提前明确需求，避免理解偏差
- **提高质量**：规范驱动的开发过程，确保代码符合要求
- **增强协作**：团队和 AI 助手在同一页面上
- **建立可追溯性**：完整的文档记录，便于后续维护

## OpenSpec 目录结构（docs-only 形态）

### 推荐的目录结构

> 本仓库进入 docs-only / planning-first 阶段后，不保留可运行的 OpenSpec 工具目录。模板以文档形式保存在：
>
> - `docs/legacy/openspec-templates/`

### 目录说明

- **changes/**：存放所有变更的目录
  - **archive/**：已完成的变更归档
  - **<change-id>/**：具体的变更目录，使用描述性的变更 ID
- **templates/**：存放文档模板的目录

## 文档模板（参考）

### 1. 提案模板（proposal.md）

参考：`docs/legacy/openspec-templates/proposal.md`

```markdown
---
title: "[Change Title]"
status: draft | in-review | approved | implemented | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors: ["Author Name"]
---

# [Change Title] 提案

## 1. 背景

[描述为什么需要这个变更，问题的背景和上下文]

## 2. 目标

[描述变更的具体目标和期望结果]

## 3. 范围

### 包含
- [列出包含的内容]

### 不包含
- [列出不包含的内容]

## 4. 成功标准

[描述如何衡量变更的成功，具体的验收标准]

## 5. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| [风险描述] | [影响程度] | [缓解措施] |

## 6. 时间线

[描述预计的时间线和里程碑]
```

### 2. 设计模板（design.md）

参考：`docs/legacy/openspec-templates/design.md`

```markdown
---
title: "[Change Title] 设计文档"
status: draft | in-review | approved | implemented
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors: ["Author Name"]
---

# [Change Title] 设计文档

## 1. 架构设计

[描述技术架构，可使用 Mermaid 图表]

## 2. 实现细节

[描述具体的实现方法和技术选择]

## 3. 数据流

[描述数据流动和处理逻辑，可使用 Mermaid 图表]

## 4. 依赖关系

### 外部依赖
- [列出外部依赖及其版本]

### 内部依赖
- [列出内部模块依赖]

## 5. 测试策略

[描述测试方法和测试用例]

## 6. 部署计划

[描述部署步骤和注意事项]
```

### 3. 任务模板（tasks.md）

参考：`docs/legacy/openspec-templates/tasks.md`

```markdown
---
title: "[Change Title] 任务清单"
status: draft | in-progress | completed
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors: ["Author Name"]
---

# [Change Title] 任务清单

## 任务列表

### Phase 1: [Phase Name]

- [ ] Task 1: [Task Description]
  - [ ] SubTask 1.1: [SubTask Description]
  - [ ] SubTask 1.2: [SubTask Description]

- [ ] Task 2: [Task Description]

### Phase 2: [Phase Name]

- [ ] Task 3: [Task Description]
- [ ] Task 4: [Task Description]

## 任务依赖关系

- [Task 2] depends on [Task 1]
- [Task 4] depends on [Task 3]

## 优先级

| 任务 | 优先级 | 估算时间 |
|------|--------|----------|
| Task 1 | P0 | 2h |
| Task 2 | P1 | 4h |
| Task 3 | P1 | 3h |
| Task 4 | P2 | 2h |
```

### 4. 规范模板（specs/）

参考：`docs/legacy/openspec-templates/specs/feature.md`

#### 功能规范模板

```markdown
---
title: "[Feature Name] 功能规范"
status: draft | in-review | approved
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors: ["Author Name"]
---

# [Feature Name] 功能规范

## 1. 功能描述

[描述功能的详细信息]

## 2. 验收标准

### Scenario 1: [Scenario Name]
- **Given** [前置条件]
- **When** [操作]
- **Then** [预期结果]

### Scenario 2: [Scenario Name]
- **Given** [前置条件]
- **When** [操作]
- **Then** [预期结果]

## 3. 非功能需求

- **性能**：[性能要求]
- **安全**：[安全要求]
- **可用性**：[可用性要求]
- **兼容性**：[兼容性要求]
```

## 与 SherryAgent 的集成

### 1. 文档集成

将 OpenSpec 相关内容作为“写规范的参考模板”添加到 SherryAgent 的文档体系中：

- **操作指南**：添加 SDD 工作流和 OpenSpec 集成指南
- **标准与规范**：添加 SDD 相关的标准和模板
- **实施计划**：使用 SDD 工作流管理实施计划

### 2. 流程集成

将 SDD 工作流与 SherryAgent 的现有流程集成：

- **需求评审**：参考 OpenSpec 的 proposal 结构组织需求
- **技术预研**：参考 OpenSpec 的 design 结构记录方案与权衡
- **任务管理**：参考 OpenSpec 的 tasks 结构拆分任务，但权威执行仍以 `.trae/specs` 为准
- **测试策略**：在 specs 中定义验收标准（本项目可不要求测试，但验收必须可验证）

### 3. AI 助手集成

为 AI 助手添加 SDD 工作流相关的指令：

- **启动变更**：`/opsx:new <change-id>`
- **生成文档**：`/opsx:ff`（fast-forward）
- **执行任务**：`/opsx:apply`
- **归档变更**：`/opsx:archive`
- **查看状态**：`/opsx:status`

## 使用示例

### 示例 1：添加新功能

```
# 1. 启动变更
/opsx:new add-user-profile-page

# 2. 生成完整文档
/opsx:ff

# 3. 编辑和确认文档
# （手动编辑 proposal.md、design.md、tasks.md、specs/）

# 4. 执行任务
/opsx:apply

# 5. 验证和测试
# （运行测试套件）

# 6. 归档变更
/opsx:archive
```

### 示例 2：修复缺陷

```
# 1. 启动变更
/opsx:new fix-api-error-handling

# 2. 生成文档
/opsx:ff

# 3. 编辑文档
# （描述缺陷和修复方案）

# 4. 执行修复
/opsx:apply

# 5. 验证修复
# （运行测试）

# 6. 归档变更
/opsx:archive
```

## 最佳实践

### 1. 文档管理

- **保持文档简洁**：只包含必要的信息
- **实时更新**：随着开发进展更新文档
- **版本控制**：将文档纳入 Git 版本控制
- **模板使用**：使用标准化的文档模板

### 2. 工作流执行

- **早期对齐**：在实现前与团队和 AI 助手对齐规范
- **小步快跑**：将变更分解为小的、可管理的任务
- **持续验证**：在每个任务完成后进行验证
- **定期审查**：定期审查文档和实现

### 3. 团队协作

- **明确职责**：定义每个角色的职责
- **有效沟通**：保持团队成员之间的沟通
- **知识共享**：通过文档共享知识和决策
- **反馈循环**：建立有效的反馈机制

## 常见问题与解决方案

### Q: 如何处理规范的变更？

**A**: SDD 支持迭代式开发，规范可以在开发过程中调整。当规范变更时：
1. 更新相关文档
2. 记录变更原因
3. 评估变更影响
4. 通知相关人员

### Q: 如何确保文档与代码同步？

**A**: 
- 将文档纳入版本控制
- 在代码提交时更新相关文档
- 建立文档审查流程
- 使用自动化工具验证文档与代码的一致性

### Q: 如何处理大型变更？

**A**: 
- 将大型变更分解为多个小变更
- 为每个子变更创建单独的目录
- 建立变更之间的依赖关系
- 按顺序执行变更

### Q: 如何衡量 SDD 的效果？

**A**: 
- **减少返工**：统计因需求变更导致的返工次数
- **提高质量**：统计缺陷率和代码质量指标
- **提高效率**：统计开发时间和交付速度
- **团队满意度**：调查团队成员对 SDD 的满意度

## 总结

OpenSpec 作为轻量级的规范驱动开发框架，可以与 SherryAgent 深度集成，提高 AI 开发的可预测性、可审查性和可追溯性。通过采用 SDD 工作流，我们可以：

- **提高代码质量**：规范驱动的开发过程确保代码符合要求
- **减少开发时间**：提前明确需求，避免理解偏差导致的返工
- **增强团队协作**：团队和 AI 助手在同一页面上
- **建立可追溯的开发历史**：完整的文档记录便于后续维护

通过将 OpenSpec 的理念和实践融入 SherryAgent 项目，我们可以构建更加可靠、高效的 AI 开发流程。
