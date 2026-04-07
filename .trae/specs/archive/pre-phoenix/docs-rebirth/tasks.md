# SherryAgent - Docs Rebirth（文档驱动重生）实现计划

## Phase 1: 北极星与入口改造（Distill-1 起步）

## [x] Task 1: 新增北极星文档
- **Priority**: P0
- **Description**:
  - 新增 `docs/vision/north-star.md`
  - 写清融合命题、成功指标、失败边界

## [x] Task 2: 新增双权威与冲突裁决文档
- **Priority**: P0
- **Description**:
  - 新增 `docs/guides/spec-authority.md`
  - 在 `AGENTS.md` 写入权威矩阵、DoD 与推荐阅读路径

## [x] Task 3: 新增术语表
- **Priority**: P0
- **Description**:
  - 新增 `docs/reference/glossary.md`
  - 统一关键术语（Story、Lane、Fork、Risk 等）

## [x] Task 4: 新增 Story 模板
- **Priority**: P1
- **Description**:
  - 新增 `docs/standard/story-template.md`

## [x] Task 5: 新增 5 个官方 Story 文档
- **Priority**: P0
- **Description**:
  - 新增 `docs/stories/` 下 5 个 story 文档
  - 补齐演示脚本、输出契约、权限策略、失败降级、六层映射

## [x] Task 6: 改造 docs/INDEX.md 入口
- **Priority**: P0
- **Description**:
  - 让 Story Suite 成为索引第一入口
  - 补齐北极星/术语表/权威规则入口

## Phase 2: 蒸馏计划与命名清理（Distill-1 完成）

## [x] Task 7: 新增 Distill 计划文档
- **Priority**: P0
- **Description**:
  - 新增 `docs/plans/docs-rebirth.md`，写清 Distill-1/2/3 Gate

## [x] Task 8: 清理历史命名残留
- **Priority**: P0
- **Description**:
  - `.trae/specs` 中统一 “Fusion Agent” -> “SherryAgent”
  - 若发现其它残留，同步清理

## Phase 3: Distill-2/3（后续执行，不在本次强制完成）

## [ ] Task 9: Distill-2 Gate 明细化
- **Priority**: P1
- **Description**:
  - 为每个 Story 增加更具体的输出字段与审计事件列表
  - 明确“低能力模型输出不合格”的判定规则

## [ ] Task 10: Distill-3 docs-only Gate 决策文档
- **Priority**: P2
- **Description**:
  - 定义 docs-only 的删除范围候选与风险评估
  - 明确保留/不保留最小骨架的利弊

