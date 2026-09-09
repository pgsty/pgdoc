# PG14—19 术语校准交付 · 修订 2

六版中文已原地完成可确认范围内的术语迁移，正式启用 631 条定稿词表及配套规则。当前修改 **631 个中文源文件、6,422 个原子文本片段**。六版 HTML、A4 PDF、US PDF 共 **18 项验收全部通过**，每项产物均对应当前源文件。

本轮独立复核此前全部 145 条未决来源记录，补充应用 20 处修改：3 条直接闭合；17 条完成可隔离的术语校准，但其所在段落仍有技术基线观察；另有 29 条术语已规范。最终保留 **96 条真正未决来源记录**，并另列 **46 条术语已规范但技术基线仍需处理的观察记录**。这些记录可能涉及同一根因，不等于独立缺陷数量。

因此**不能宣称全量任务全部完成**。实际改动、跨版本台账、豁免、结构保护及构建验收已交付；剩余项受现有提示词的同版来源、结构保护和术语范围约束。没有提交、推送或发布。

**修改与构建结果**

| 英文来源 | 修改文件 | 原子修改 | HTML | A4 PDF | US PDF |
|---|---:|---:|---|---|---|
| 14.24 | 98 | 1037 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/14/html/html/index.html) | [通过 · 2896 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/14/A4/postgresql-14-zh-A4.pdf) | [通过 · 3056 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/14/US/postgresql-14-zh-US.pdf) |
| 15.19 | 102 | 1051 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/15/html/html/index.html) | [通过 · 2908 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/15/A4/postgresql-15-zh-A4.pdf) | [通过 · 3077 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/15/US/postgresql-15-zh-US.pdf) |
| 16.15 | 103 | 1076 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/16/html/html/index.html) | [通过 · 2918 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/16/A4/postgresql-16-zh-A4.pdf) | [通过 · 3078 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/16/US/postgresql-16-zh-US.pdf) |
| 17.11 | 104 | 1066 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/17/html/html/index.html) | [通过 · 2899 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/17/A4/postgresql-17-zh-A4.pdf) | [通过 · 3061 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/17/US/postgresql-17-zh-US.pdf) |
| 18.6 | 106 | 1091 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/18/html/html/index.html) | [通过 · 2934 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/18/A4/postgresql-18-zh-A4.pdf) | [通过 · 3099 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/18/US/postgresql-18-zh-US.pdf) |
| 19beta3 | 118 | 1101 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/19/html/html/index.html) | [通过 · 3010 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/19/A4/postgresql-19-zh-A4.pdf) | [通过 · 3179 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/builds/19/US/postgresql-19-zh-US.pdf) |

PG14–16 在本轮补丁后重新执行 9 个实际 make 目标；PG17–19 沿用上轮已实际执行且源/产物哈希完全一致的 9 个结果。[验收清单](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/build-manifest.jsonl)记录命令、退出码、日志、产物及哈希。每个构建目录含 `command.json`、`result.json` 与 `build.log`。

**审阅与追溯**

- [完整补丁](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/diff/working-tree.patch)；[本轮 20 处补丁](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/diff/revision-2.patch)；[逐词差异](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/diff/word-diff.txt)。
- [408 格词条/版本矩阵](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/term-version-coverage.jsonl)；[按词条和大版本的处数及文件数](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/term-version-change-counts.tsv)；[6422 条有效修改记录](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/active-edits.jsonl)。
- [1422 个跨版本台账单元](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/cross-version-semantic-ledger.jsonl)；[本轮逐处六版附录](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/revision-2-six-version-addendum.jsonl)；[145 条复核处置](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/continuation-dispositions.jsonl)。
- [豁免与保留清单](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/exemptions-and-retentions.jsonl)；[96 条未决项](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/UNRESOLVED.md)；[46 条技术基线观察](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/BASELINE-OBSERVATIONS.md)。
- [原交付](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/previous-delivery/REPORT.md)保留原样；[本轮审查证据](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/continuation-review)及[台账读取说明](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/ledgers/README.md)解释历史快照与当前处置的关系。

1422 个单元均有六版处置，共 8532 格；这些是台账分组，不能与独立修改位置数混同。本轮修正了两处重复引用，只标明主位置，不合并或删除包含其他位置的单元。一个词形若被内嵌 SGML 分隔，可能对应多个原子修改；一个位置也可能属于多个词条，因此不能直接加总所有词条处数。

**检查与显示验收**

- 对照不可变备份核查 2637 个源文件；631 个修改文件均由当前有效修改记录精确重构，其余源文件未变。2353 个固定英文 SGML 文件未变。
- SGML 标签、属性、ID、linkend、实体、注释和代码/名称保护区签名与原基线一致；`git diff --check` 通过。6422 条修改所附 6429 个英文证据对象均验证通过。
- 台账中 6955 个唯一英文文件/哈希/原文证据对象验证通过，涉及 968 个来源文件。六版索引页面与前次完整索引审计产物逐字节一致，没有本轮新增索引目标失配。
- 六版原代表 HTML 页面 12 个均验证为相同产物；本轮另实际查看 5 个 HTML 页面。重建 PDF 的 24 个标题/目录/正文/索引代表页与前次已查看页面逐像素一致，另实际查看 10 个修改相关正文页。未见所查页面缺字、重叠或裁切。
- [源码与结构检查](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/summary.json)；[英文证据校验](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/ledger-english-evidence-validation.json)；[PDF 验收](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/visual-qa/pdf-manifest.json)；[HTML 验收](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/visual-qa/html-manifest.json)。

现有构建包装脚本使用 `loaddtd`，这里证明的是实际解析/构建成功及结构保护区不变，不冒称严格 DTD 有效性检查通过，也不冒称逐页目视检查整书。

**仍需处理的范围**

| 词族 | 真正未决来源记录 |
|---|---:|
| F01 | 14 |
| F03 | 19 |
| F04 | 15 |
| F05 | 27 |
| F06 | 2 |
| F07 | 2 |
| F09 | 17 |

剩余项包含：本版英文已有但中文缺失的条目/字段/说明；旧版中文出现后版对象与功能、却没有可靠的本版对应来源；转义行为与受保护示例不同步等。仅替换词语无法闭合这些问题。全部位置、版本、英文证据及最小后续动作见未决清单。

PG16 的 `reference.sgml` 实际包含 `pg_combinebackup`、`pg_createsubscriber`、`pg_walsummary` 三页，而固定 `en/16.15` 没有对应参考页；Git 可追溯至 `3ca4516` 的批量更新，但没有找到可靠的项目回移约定。准备包明确要求证据不足时保留 `pg_createsubscriber` 中的术语候选，不把 PG17 英文冒充 PG16 来源。[包含链审计](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/include-chain.json)保留完整证据。

当前提示词要求“保持 SGML 标签、属性、ID、实体、注释、代码、名称、输出和示例不变”，并要求证据不足时保留原内容。补缺译、纠正超前技术内容或调整这些参考页的归属，需要单独确定基线处理范围；本轮没有扩大成技术内容重译。

**规则与恢复**

- [完整词表](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/rules/glossary.tsv)、[逐条规则](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/rules/glossary.rules.tsv)、[检索别名](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/rules/glossary-aliases.tsv)、[保留说明](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/rules/terms-to-preserve.tsv)已正式安装；现行 `style.md` 和 `exclude.tsv` 保留不变。
- [执行前状态](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/baseline.json)；[规则三方安装记录](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/rules-install.json)；[最终源哈希](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/audit/final-source-hashes.json)；[串行集成状态](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117-r2/run/integration-state.json)。恢复以当前有效提案为准，不重复应用历史已撤销或未采纳草案。

生成时间：2026-09-08T22:19:53（Asia/Shanghai）。
