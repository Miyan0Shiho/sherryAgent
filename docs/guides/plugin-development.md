---
title: "插件开发指南（Legacy / Future Phase）"
status: archived
created: 2026-04-04
updated: 2026-04-07
related:
  - "../plans/implementation-program.md"
  - "../../.trae/specs/tooling-integration/spec.md"
---

# 插件开发指南（Legacy / Future Phase）

本文档保留为未来 `tooling-integration` 主线进入实现阶段时的参考资料。

## 当前定位

- 当前仓库没有插件 SDK 或插件运行时实现。
- 当前主计划只要求明确工具接入边界、幂等、隔离、审计和外部依赖治理。
- 插件机制是否继续采用 `pluggy`，应在 `tooling-integration` 主线内决策，而不是由本文档预设为既定事实。

## 当前应参考的文档

- `docs/architecture/module-map.md`
- `docs/specs/permission-system.md`
- `.trae/specs/tooling-integration/spec.md`

## 保留价值

未来如果恢复插件体系，可以复用本文档中的结构建议和风险点，但必须先通过当前蓝图重新审查。

