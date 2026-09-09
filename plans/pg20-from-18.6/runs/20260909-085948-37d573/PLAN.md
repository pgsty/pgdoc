# PG20 正式执行计划

准备阶段一、二均已完成，本次停在生成正式翻译提示词；未执行新增/变更正文翻译。唯一执行入口为 [TRANSLATE-PG20.md](TRANSLATE-PG20.md)，任务源 [TASKS.tsv](TASKS.tsv)，固定提交 `86f7c82cf1023e3599f40f939727791a7090cd44`。

输入和所有绝对路径见 [RUN.json](RUN.json) 与 [/Users/vonng/pgsty/pgdoc/en/diff/20-vs-18.6/20260909-085948-37d573/source-manifest.json](/Users/vonng/pgsty/pgdoc/en/diff/20-vs-18.6/20260909-085948-37d573/source-manifest.json)。本轮 Git HEAD `8ff9e69bff64a8f8f1bc025dc6a1faf10ad4e137`，工作区已有未跟踪的历史交付证据；已保存开工状态，保留原文/旧版及人工修改。

| 批次 | 任务行数 |
|---|---:|
| 0 | 1 |
| 1 | 255 |
| 2 | 264 |
| 3 | 505 |
| 4 | 34 |
| 5 | 243 |
| 6 | 1 |
| 7 | 3 |
| 8 | 1 |
| 9 | 1 |

0：复核固定输入/后续人工修改。1：核对继承和 254 个英文不变路径。2：结构迁移及结构外壳；35 个跨路径根映射（函数章 32 个、废弃附录 3 个）和 5 个 logicaldecoding 重归属根按本轮结构表实施。3：真正新增、局部修改、历史译文复用以及其范围内的字面更新。4：资源、七类派生目标、三项项目定制和固定源码能力。5：先新后旧核对删改配对，最后删除 zh/20/func.sgml 与 release-18.sgml，审查基线差异。6：源码/引用/术语/覆盖验收。7：三个实际构建。8：视检。9：本地交付。

任务表依赖是权威顺序，同一批次内也要遵守依赖。按文件维度协调修改，避免不同单元任务相互覆盖。翻译单元通常是完整段落、列表条目、选项或表格行；结构/空白单元有单独动作。old/new 文本是上下文，不能因单元较大而重写未变中文；同文件 unpaired_old_span 在目标新增和修改完成后统一核对替换关系。

主英文原始范围：490 路径联合集、1,133 块。12,368 个单元含 2,357 个 PG18 英文完全匹配复用、1,410 个 PG19 英文完全匹配的中文候选、95 个 PG19 部分语境候选、56 个首次翻译候选。其余是结构/资源和删除/替换配对。生成表 25 块单列。逐文件数字在 [translation-scope.tsv](/Users/vonng/pgsty/pgdoc/en/diff/20-vs-18.6/20260909-085948-37d573/translation-scope.tsv)。

未检索到对齐历史基础的首次候选出现在以下具体文件（同文件其他内容仍应继承或历史复用）：

- `appendix-obsolete-refint.sgml`
- `config.sgml`
- `ddl.sgml`
- `func/func-json.sgml`
- `func/func-matching.sgml`
- `func/func-string.sgml`
- `glossary.sgml`
- `logical-replication.sgml`
- `monitoring.sgml`
- `mvcc.sgml`
- `pgbuffercache.sgml`
- `postgres-fdw.sgml`
- `ref/alter_aggregate.sgml`
- `ref/alter_publication.sgml`
- `ref/create_aggregate.sgml`
- `ref/create_publication.sgml`
- `ref/drop_subscription.sgml`
- `release-20.sgml`
- `system-views.sgml`
- `wal.sgml`
- `xfunc.sgml`

优先协调 monitoring/config/system-views 的监控和配置含义、logical-replication/ref/create_subscription 的复制语义、func/* 的函数和术语、ref/repack 与旧 CLUSTER/存储叙述、废弃附录与主章节引用。新增 pgplanadvice、pgstashadvice、func-tid 等已有 PG19 参考，不等于首次全文翻译。release-20 当前是上游占位，不沿用旧发布说明清单或 PROPERTY GRAPH 页面。

历史方法取舍：继承旧流程的递归路径清单、原始 unified diff、逐块唯一 ID、按英文共义归并、逐处前后哈希、SGML/字面/引用审计和真实 HTML/A4/US 构建。纠正旧流程中小版本中文目录、先删除后迁移、全部内联标签冻结、仅检查 marker/文件存在、旧统计写死、忽略 generated inputs、自动用开发 snapshot 和宽松 IDREF 构建充当验收的问题。已读历史材料的 217 份文件/表/差异及 SHA256 在 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/historical-inputs.json`；只借鉴方法，不复用其中过时术语决定。

本次没有构建中文继承底稿；12 个两版生成表命令成功，依赖检查成功，固定源码参数还未实现。所有正文与构建验收任务仍处于 formal execution 待执行状态。源码固定、哈希、原始 diff 重建、文件/hunk/unit/任务覆盖及无旧文件修改的准备验收见 [preparation-validation.json](/Users/vonng/pgsty/pgdoc/en/diff/20-vs-18.6/20260909-085948-37d573/preparation-validation.json)。
