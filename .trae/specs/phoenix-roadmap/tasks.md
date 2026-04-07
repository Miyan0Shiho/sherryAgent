# SherryAgent - Phoenix Roadmap（docs-only -> 重生实现）任务清单

## Phase 1: docs-only 收敛（Egg）

- [ ] Task 1: 删除实现代码与测试资产
  - [ ] 删除 `src/ tests/ examples/ plugins/ skills/`
  - [ ] 删除根目录 `test_*.py`、`run_*.py`
  - [ ] 删除产物/缓存/本地数据（htmlcov/.venv/*cache/*.db/.coverage/uv.lock 等）

- [ ] Task 2: 入口文档改为 docs-only 口径
  - [ ] README 移除安装/运行/测试命令，改为 Story Suite 阅读入口
  - [ ] AGENTS 改为 docs-only 工作流与双权威
  - [ ] project-structure 改为 docs-only 结构
  - [ ] pyproject.toml 变为占位元数据（无 scripts/依赖/工具链配置）

- [ ] Task 3: legacy 承接层
  - [ ] `docs/legacy/implementation-snapshot.md`
  - [ ] `docs/legacy/source-map.md`

- [ ] Task 4: research 去代码链接
  - [ ] 去除 `file:///...` 绝对链接
  - [ ] 去除 `src/`、`tests/` 路径引用
  - [ ] 替换为指向 legacy 的能力引用

## Phase 2: 计划体系重生（Story 驱动）

- [ ] Task 5: 新建 Story 执行计划
  - [ ] `.trae/specs/story-01-rigorous-dev-copilot/`
  - [ ] `.trae/specs/story-02-personal-clerk/`
  - [ ] `.trae/specs/story-03-ops-sentinel-incident-responder/`
  - [ ] `.trae/specs/story-04-research-miner-security-auditor/`
  - [ ] `.trae/specs/story-05-repo-guardian-release-pilot/`

- [ ] Task 6: 归档旧 MVP 体系
  - [ ] 移动 `.trae/specs/mvp-*` 等 pre-phoenix 目录到 `.trae/specs/archive/pre-phoenix/`

## Phase 3: Chick Gate（预留）

- [ ] Task 7: 定义 Chick 的最小骨架清单（仅定义，不实现）
  - [ ] 每个 Story 的最小闭环“实现必须项”
  - [ ] 权限/审计/回放的最小契约

