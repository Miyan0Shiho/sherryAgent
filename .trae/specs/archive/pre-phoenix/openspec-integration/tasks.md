# OpenSpec 参考模板（非权威）任务

## Phase 1: 目录结构与模板创建（仅模板）

### [x] Task 1: 创建 OpenSpec 目录结构
- **Description**: 创建 OpenSpec 风格的目录结构
- **SubTasks**:
  - [x] 创建 `openspec/` 主目录
  - [x] 创建 `openspec/changes/` 目录
  - [x] 创建 `openspec/changes/archive/` 目录
  - [x] 创建 `openspec/templates/` 目录

### [x] Task 2: 创建 OpenSpec 文档模板
- **Description**: 创建 SDD 工作流所需的文档模板
- **SubTasks**:
  - [x] 创建 `openspec/templates/proposal.md` 模板
  - [x] 创建 `openspec/templates/design.md` 模板
  - [x] 创建 `openspec/templates/tasks.md` 模板
  - [x] 创建 `openspec/templates/specs/feature.md` 模板

## Phase 2: 定位与说明（防止权威冲突）

### [x] Task 3: 在 docs 中明确 OpenSpec 是参考模板
- **Description**:
  - 更新 `docs/guides/openspec-guide.md` 添加定位声明
  - 在 `docs/guides/sdd-workflow.md` 补充 SherryAgent 约束说明
  - 将权威矩阵与冲突裁决写入 `docs/guides/spec-authority.md`
