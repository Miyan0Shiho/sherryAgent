# SherryAgent - Phoenix Roadmap 验证清单（docs-only）

## Gate-0: docs-only 形态

- [ ] 工作区不存在 `src/` 目录
- [ ] 工作区不存在 `tests/` 目录
- [ ] README 不包含 `uv run` / `pytest` / `mypy src/` / `ruff check src/`
- [ ] AGENTS 不包含 `uv run` / `pytest` / `mypy src/` / `ruff check src/`

## Gate-1: Distill-2（文档即规范）

- [ ] 5 个 Story 文档齐全并可导航
- [ ] 每个 Story 包含演示脚本、输出契约、权限策略、失败降级、六层映射
- [ ] `docs/research/*` 中不包含任何 `file:///`
- [ ] `docs/research/*` 中不引用 `src/`、`tests/` 路径
- [ ] 研究文档引用已映射到 `docs/legacy/*`

## 计划入口

- [ ] `.trae/specs` 下存在 `phoenix-roadmap/`
- [ ] `.trae/specs` 下存在 `story-01..05/`
- [ ] 旧 `mvp-*` 计划已归档到 `.trae/specs/archive/pre-phoenix/`

