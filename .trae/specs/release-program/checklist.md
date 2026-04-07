# Release Program Checklist

## Gate Scope

- [ ] 本 checklist 用于 `G4 Release Readiness Gate`
- [ ] 本主线交付物已同步到 `docs/plans/master-program.md` 与 `docs/plans/implementation-program.md`

## Entry Criteria

- [ ] `release-program/spec.md` 已包含输入、输出、依赖、里程碑、阻断条件和退出条件
- [ ] `release-program/tasks.md` 已拆分为 `Phase 0-4`，且包含工作包、交付物、依赖和阻断项
- [ ] 其余 6 条主线均已具备可供消费的完成证明

## Pass Criteria

### Program Structure Gate
- [ ] 7 条主线的依赖关系已定稿
- [ ] 阶段图、并行窗口与先决条件已定稿

### Gate Policy Gate
- [ ] 恢复实现前的门禁已定稿
- [ ] `G1` 到 `G4` 的必需输入、阻断条件和输出已定稿
- [ ] GitHub required checks 已定义且与 gate 口径一致

### Risk & Readiness Gate
- [ ] 风险台账和升级裁决方式已定稿
- [ ] Story / benchmark / 运营验收三层关系已定稿
- [ ] 上线前必须准备的 runbook、回滚和观测资产已定稿
- [ ] `conflict-decision` Issue 流程和 A/B 裁决回写机制已定稿
- [ ] 跨角色交接契约和无效交接阻断规则已定稿

### Program Adoption Gate
- [ ] 进入未来 release / hotfix 阶段的条件已定稿
- [ ] 从 planning-first 进入实现阶段的切换条件已定稿
- [ ] `master-program.md` 与本主线保持同步
- [ ] `1 Issue + 1 Branch + 1 PR` 已作为并行开发默认单元
- [ ] Issue/PR/CODEOWNERS 模板已落库并可直接使用
- [ ] 7 角色手册与 prompt 模板已落库并可直接驱动对话

## Blocking Conditions

- [ ] 7 条主线之间仍存在隐性依赖，无法形成清晰交付顺序
- [ ] 门禁标准不能直接引用质量、成本或安全正式指标
- [ ] Story 验收与主线里程碑脱节
- [ ] 仍需引用旧路线图才能解释当前排期

## Handoff

- [ ] 全项目已经具备统一执行入口
- [ ] 7 条主线与 5 个 Story 可被纳入同一套 gate 程序
- [ ] 该主线可作为 `G4 Release Readiness Gate` 正式输入
