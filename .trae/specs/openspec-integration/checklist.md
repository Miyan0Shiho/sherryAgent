# OpenSpec 集成与 SDD 工作流实现验证清单

## Phase 1: 目录结构与模板创建

- [ ] `openspec/` 目录存在
- [ ] `openspec/changes/` 目录存在
- [ ] `openspec/changes/archive/` 目录存在
- [ ] `openspec/templates/` 目录存在
- [ ] `openspec/templates/proposal.md` 模板存在
- [ ] `openspec/templates/design.md` 模板存在
- [ ] `openspec/templates/tasks.md` 模板存在
- [ ] `openspec/templates/specs/` 目录和模板存在

## Phase 2: 核心功能实现

- [ ] SDD 工作流核心逻辑实现完成
- [ ] `/opsx:new` 命令实现并正常工作
- [ ] `/opsx:ff` 命令实现并正常工作
- [ ] `/opsx:apply` 命令实现并正常工作
- [ ] `/opsx:archive` 命令实现并正常工作
- [ ] `/opsx:status` 命令实现并正常工作
- [ ] 与 Orchestrator 集成完成
- [ ] 与 Agent Loop 集成完成
- [ ] 与测试系统集成完成
- [ ] 与 CLI 系统集成完成

## Phase 3: 配置与工具

- [ ] `openspec/config.toml` 配置文件存在
- [ ] 配置加载和验证功能正常
- [ ] 与 SherryAgent 配置系统集成完成
- [ ] 与 Git 版本控制集成完成
- [ ] 与测试工具集成完成
- [ ] 与代码检查工具集成完成

## Phase 4: 文档与测试

- [ ] `docs/guides/openspec-guide.md` 存在
- [ ] `docs/guides/sdd-workflow.md` 存在
- [ ] `docs/INDEX.md` 已更新
- [ ] 单元测试编写完成并通过
- [ ] 集成测试编写完成并通过
- [ ] 端到端测试编写完成并通过

## 功能验证

- [ ] 能够通过 `/opsx:new` 创建新的变更
- [ ] 能够通过 `/opsx:ff` 生成完整的规划文档
- [ ] 能够通过 `/opsx:apply` 执行代码实现
- [ ] 能够通过 `/opsx:archive` 归档变更
- [ ] 工作流能够与现有的 SherryAgent 系统无缝集成
- [ ] 生成的代码质量符合项目标准
