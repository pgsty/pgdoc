---
name: pgdoc-minor-sync
description: PostgreSQL 中文文档小版本增量同步（如 18.6→18.7）。当上游发布新小版本、需要固定英文差异并增量翻译 zh/<大版本> 时使用。流程见 ref/minor-sync.md。
---

执行 pgdoc 小版本增量同步任务。

1. 完整读取并遵循 `ref/minor-sync.md` 的流程与判例。
2. 先读 `AGENTS.md` 与 `ref/README.md` 的共用纪律；译法按 `docs/exclude.tsv` > `docs/glossary.tsv`（+rules）> `docs/style.md` > 稳定现有译文。
3. 核心约束：只改英文差异涉及的内容；生成文件（GENERATED_SGML）用对应版本源码重建后再比；中英不按行号匹配；跨版本复用译文但保留各版自己的结构与链接。
4. 交付含：差异台账、构建证据（HTML + A4/US PDF）、未决项。不提交/推送/发布。
