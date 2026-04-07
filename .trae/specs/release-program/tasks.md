# Release Program Tasks

## Phase 0: Program Alignment

### Work Packages
- [ ] P0-W1: 汇总 7 条主线的 spec/tasks/checklist 作为 program 输入
- [ ] P0-W2: 清点仍然残留的旧路线图、旧阶段口径和隐性依赖
- [ ] P0-W3: 建立 master program 的主线、阶段、gate 与风险术语

### Deliverables
- [ ] D0-1: 主线输入清单
- [ ] D0-2: 隐性依赖清单

## Phase 1: Program Structure Freeze

### Work Packages
- [ ] P1-W1: 固定 7 条主线的前后顺序和关键依赖
- [ ] P1-W2: 固定先决条件：哪些主线必须先于恢复实现完成
- [ ] P1-W3: 固定 Story 验收与平台级验收的先后关系
- [ ] P1-W4: 固定哪些工作可并行推进，哪些必须等待 gate 通过

### Deliverables
- [ ] D1-1: 依赖图
- [ ] D1-2: 阶段图与并行窗口

### Dependencies
- [ ] DEP1-1: 其余 6 条主线 spec 已明确输入、输出和退出条件

## Phase 2: Gate Policy Freeze

### Work Packages
- [ ] P2-W1: 定义文档定稿门禁
- [ ] P2-W2: 定义恢复实现前必须满足的评测、成本、安全和回滚条件
- [ ] P2-W3: 定义哪些风险未关闭时不得进入实现或发布阶段
- [ ] P2-W4: 定义 `G1` 到 `G4` 的必需输入、阻断条件和输出

### Deliverables
- [ ] D2-1: 门禁矩阵
- [ ] D2-2: 实现切换条件

### Blockers
- [ ] B2-1: 门禁标准仍然无法直接引用质量、成本或安全正式指标

## Phase 3: Risk & Readiness Freeze

### Work Packages
- [ ] P3-W1: 定义主线级风险台账结构
- [ ] P3-W2: 定义跨主线冲突的升级与裁决方式
- [ ] P3-W3: 定义上线前必须准备的 runbook、回滚和观测资产
- [ ] P3-W4: 定义 Story 验收、benchmark 验收、运营验收三层关系

### Deliverables
- [ ] D3-1: 风险台账模板
- [ ] D3-2: 发布准备清单

## Phase 4: Program Adoption

### Work Packages
- [ ] P4-W1: 定义从 planning-first 进入实现阶段的切换条件
- [ ] P4-W2: 定义未来 release / hotfix 进入条件
- [ ] P4-W3: 把 `master-program.md`、`implementation-program.md` 与本主线保持同步
- [ ] P4-W4: 形成总控主线完成证明，作为全项目执行入口

### Deliverables
- [ ] D4-1: program adoption 说明
- [ ] D4-2: 全项目 gate 通过说明
