# OpenSpec 参考模板（非权威）与 SDD 写法约定

## Why
为了强化 SherryAgent 的开发文档表达质量，需要引入规范驱动开发（Spec-Driven Development, SDD）理念，让输出从"不可预测"变为"可预期、可审查、可追溯"。

**定位声明（SherryAgent 专用）**：
- `.trae/specs/*` 是开发执行权威（做什么、验收是什么、任务如何拆分）
- `docs/*` 是系统契约与叙事权威（长期结构、术语、安全原则、Story 口径）
- OpenSpec 在本项目中仅作为“文档写法/模板参考”，不作为权威规范来源

## What Changes
- 提供 OpenSpec 风格的最小模板，便于按 proposal/design/tasks/spec 的结构写文档
- 在 docs 中明确其“参考模板”定位，避免与 `.trae/specs` 权威冲突

## Impact
- Affected specs: 开发文档写法（参考）
- Affected code: 无（不要求实现 `/opsx:*` 命令）

## ADDED Requirements

### Requirement: OpenSpec 风格模板（参考）
系统 SHALL 提供 OpenSpec 风格的最小文档模板，供人类/Agent 参考使用。

#### Scenario: 模板使用
- **WHEN** 开发者需要结构化地写需求/设计/任务
- **THEN** 可以在 `openspec/templates/` 中找到可复用模板

## REMOVED Requirements（本项目不要求）

- 不要求实现 `/opsx:*` 命令
- 不要求将 OpenSpec 作为权威规范来源
- 不要求与编排/执行/CLI 深度绑定
