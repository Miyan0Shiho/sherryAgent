# Release Program Tasks

## Phase 0: Program Alignment

### Work Packages
- [ ] P0-W1: 汇总 7 条主线的 spec/tasks/checklist 作为 program 输入
- [ ] P0-W2: 清点仍然残留的旧路线图、旧阶段口径和隐性依赖
- [ ] P0-W3: 建立 master program 的主线、阶段、gate 与风险术语
- [ ] P0-W4: 定义 `Program Conductor` 的职责、状态对象和阻断权限

### Deliverables
- [ ] D0-1: 主线输入清单
- [ ] D0-2: 隐性依赖清单
- [ ] D0-3: `docs/roles/program-conductor.md`
- [ ] D0-4: `docs/standard/program-conductor-state.md`

## Phase 1: Program Structure Freeze

### Work Packages
- [ ] P1-W1: 固定 7 条主线的前后顺序和关键依赖
- [ ] P1-W2: 固定先决条件：哪些主线必须先于恢复实现完成
- [ ] P1-W3: 固定 Story 验收与平台级验收的先后关系
- [ ] P1-W4: 固定哪些工作可并行推进，哪些必须等待 gate 通过
- [ ] P1-W5: 将 `Phase A-D` 与 `G1-G4` 映射到多子 Agent 调度程序

### Deliverables
- [ ] D1-1: 依赖图
- [ ] D1-2: 阶段图与并行窗口
- [ ] D1-3: 多子 Agent phase program

### Dependencies
- [ ] DEP1-1: 其余 6 条主线 spec 已明确输入、输出和退出条件

## Phase 2: Gate Policy Freeze

### Work Packages
- [ ] P2-W1: 定义文档定稿门禁
- [ ] P2-W2: 定义恢复实现前必须满足的评测、成本、安全和回滚条件
- [ ] P2-W3: 定义哪些风险未关闭时不得进入实现或发布阶段
- [ ] P2-W4: 定义 `G1` 到 `G4` 的必需输入、阻断条件和输出
- [ ] P2-W5: 建立 GitHub PR required checks（Spec-Docs Sync / Glossary Consistency / Gate Eligibility / No Active Conflict Claim）
- [ ] P2-W6: 建立 PR 模板与 `contract-impacting` 双权威审批要求
- [ ] P2-W7: 将 `role_owner`, `next_role`, `handoff_ready` 接入 Issue / PR 治理模板

### Deliverables
- [ ] D2-1: 门禁矩阵
- [ ] D2-2: 实现切换条件
- [ ] D2-3: `.github/workflows/pr-governance-gates.yml`
- [ ] D2-4: `scripts/ci/pr_governance_checks.py`

### Blockers
- [ ] B2-1: 门禁标准仍然无法直接引用质量、成本或安全正式指标

## Phase 3: Risk & Readiness Freeze

### Work Packages
- [ ] P3-W1: 定义主线级风险台账结构
- [ ] P3-W2: 定义跨主线冲突的升级与裁决方式
- [ ] P3-W3: 定义上线前必须准备的 runbook、回滚和观测资产
- [ ] P3-W4: 定义 Story 验收、benchmark 验收、运营验收三层关系
- [ ] P3-W5: 固定 `conflict-decision` Issue 流程与 A/B 裁决回写机制
- [ ] P3-W6: 定义跨角色交接契约与无效交接阻断规则
- [ ] P3-W7: 固定 `Story-01` 与 `Story-05` 的首批 rollout 证明责任

### Deliverables
- [ ] D3-1: 风险台账模板
- [ ] D3-2: 发布准备清单
- [ ] D3-3: `.github/ISSUE_TEMPLATE/conflict-decision.yml`
- [ ] D3-4: `docs/standard/role-handoff-contract.md`
- [ ] D3-5: `docs/standard/story-rollout-record.md`

## Phase 4: Program Adoption

### Work Packages
- [ ] P4-W1: 定义从 planning-first 进入实现阶段的切换条件
- [ ] P4-W2: 定义未来 release / hotfix 进入条件
- [ ] P4-W3: 把 `master-program.md`、`implementation-program.md` 与本主线保持同步
- [ ] P4-W4: 形成总控主线完成证明，作为全项目执行入口
- [ ] P4-W4a: 产出“是否开始开发”的正式 gate 决策文档，逐项判定 `G1-G4` 当前缺口
- [ ] P4-W5: 固定 Issue-first 并行单元（`1 Issue + 1 Branch + 1 PR`）并发布模板
- [ ] P4-W6: 发布 7 角色手册与对话启动模板
- [ ] P4-W7: 发布 `Program Conductor` 启动模板与首批 rollout 运行手册

### Deliverables
- [ ] D4-1: program adoption 说明
- [ ] D4-2: 全项目 gate 通过说明
- [ ] D4-2a: `docs/plans/development-readiness-gate-decision.md`
- [ ] D4-3: `.github/ISSUE_TEMPLATE/work-unit.yml`
- [ ] D4-4: `.github/ISSUE_TEMPLATE/contract-change.yml`
- [ ] D4-5: `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] D4-6: `.github/CODEOWNERS`
- [ ] D4-7: `docs/guides/multi-conversation-development.md`
- [ ] D4-8: `docs/roles/*`
- [ ] D4-9: `docs/roles/prompts/*`
- [ ] D4-10: `docs/roles/prompts/program-conductor.md`
