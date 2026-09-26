---
name: pgdoc-major-migration
description: PostgreSQL 中文文档跨大版本迁移（新建大版本如 zh/20 从 zh/18 迁移，或以新版为底稿回填旧归档版本 10–13）。需要固定源码、生成完整 diff、结构迁移映射与两阶段执行时使用。流程见 ref/major-migration.md。
---

执行 pgdoc 跨大版本迁移任务（正向新建或反向回填）。

1. 完整读取并遵循 `ref/major-migration.md` 的两阶段流程与判例。
2. 先读 `AGENTS.md` 与 `ref/README.md` 的共用纪律及 `docs/` 规则文件。
3. 核心约束：devel 版必须固定完整提交 SHA；中文基线取当前工作区（含人工修改）；主差异始终是基线英文→目标英文（回填不逐版串接）；搬移/拆分先建映射保存中文再迁移；第二阶段生成的执行提示词不留占位符。
4. 验收含：包含链、hunk 全处置、复用可证明、目标版本 HTML + A4/US PDF 构建及显示版本核对。不提交/推送/发布。
