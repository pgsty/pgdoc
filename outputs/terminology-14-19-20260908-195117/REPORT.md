# PG14—19 术语校准与验收交付

六版中文已在 `zh/14` 至 `zh/19` 原地校准，正式启用完整 631 条定稿词表及配套规则。共修改 **631 个中文源文件、6,402 个原子文本片段**；六版 HTML、A4 PDF、US PDF 共 **18 项实际构建均通过**，且构建源哈希与现行正文完全匹配。

本次覆盖 **68 × 6 = 408 个词条/版本单元**，交付 **1422 个跨版语义位置、8532 个版本处置**。仍有 **145 条未决来源记录**，主要是执行前已有的中英文基线错配，因此**不宣称所有适用项全部完成**。记录数不等于独立缺陷数；同一基线问题可能影响多个词条或位置。

执行前基线、当前全文、词形处数、语义位置和构建结果分别保存，词法命中数量不作为完成证据。Git 未提交、未推送，产物未发布。

**实际修改与构建**

| 固定英文版本 | 中文修改文件 | 原子文本修改 | HTML | A4 PDF | US PDF |
|---|---:|---:|---|---|---|
| 14.24 | 98 | 1024 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/14/html/html/index.html) | [通过 · 2896 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/14/A4/postgresql-14-zh-A4.pdf) | [通过 · 3056 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/14/US/postgresql-14-zh-US.pdf) |
| 15.19 | 102 | 1045 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/15/html/html/index.html) | [通过 · 2908 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/15/A4/postgresql-15-zh-A4.pdf) | [通过 · 3077 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/15/US/postgresql-15-zh-US.pdf) |
| 16.15 | 103 | 1075 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/16/html/html/index.html) | [通过 · 2918 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/16/A4/postgresql-16-zh-A4.pdf) | [通过 · 3078 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/16/US/postgresql-16-zh-US.pdf) |
| 17.11 | 104 | 1066 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/17/html/html/index.html) | [通过 · 2899 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/17/A4/postgresql-17-zh-A4.pdf) | [通过 · 3061 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/17/US/postgresql-17-zh-US.pdf) |
| 18.6 | 106 | 1091 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/18/html/html/index.html) | [通过 · 2934 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/18/A4/postgresql-18-zh-A4.pdf) | [通过 · 3099 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/18/US/postgresql-18-zh-US.pdf) |
| 19beta3 | 118 | 1101 | [通过](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/19/html/html/index.html) | [通过 · 3010 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/19/A4/postgresql-19-zh-A4.pdf) | [通过 · 3179 页](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/builds/19/US/postgresql-19-zh-US.pdf) |

命令逐版实际展开为 `make -C zh/<大版本> html BUILD_OUT=…`、`make -C zh/<大版本> pdf PAPER=A4 PDF_OUT=…` 和 `make -C zh/<大版本> pdf PAPER=US PDF_OUT=…`。PG19 已显式执行。[验收清单](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/build-manifest.jsonl) 保存退出码、用时、日志、产物 SHA256 及当前源匹配结果；每项产物旁均有 `command.json`、`result.json`、`build.log`。先前构建仅作过程记录，正式结果使用 `builds-final`。

**审阅入口**

- [工作区补丁](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/diff/working-tree.patch)；[逐词差异](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/diff/word-diff.txt)；[规则前后差异](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/diff/rules.patch)。
- [408 格覆盖矩阵](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/term-version-coverage.jsonl)；[按词条和大版本的实际修改处数及文件数](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/term-version-change-counts.tsv)。
- [跨版本语义位置台账](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/cross-version-semantic-ledger.jsonl)；[当前有效精确修改记录](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/active-edits.jsonl)。
- [豁免与已规范保留清单](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/exemptions-and-retentions.jsonl)；[未决索引](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/UNRESOLVED.md)；[未决原始证据](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/unresolved-source-records.jsonl)。
- [台账来源、行号及哈希索引](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/ledger-source-index.json)；[完整运行证据目录](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/run)。

“原子修改”是一次精确字符片段替换；跨行或内嵌 SGML 的同一术语可能拆成多个原子修改。处数表另列合并这些片段后的实际编辑词形位置数，文件数按词条/版本去重。跨版本语义台账可把 primary/secondary 索引限定词归入一个概念位置。一个位置可能属于两个词条，禁止直接加总词条处数作为全库独立修改总数。

**保护和渲染检查**

- 对照不可变备份核查 2637 个源文件。631 个修改文件均能由有效修改记录精确重构，其余源文件未变；2,353 个固定英文 SGML 源文件未变。
- 6,402 条修改所附英文原句及来源哈希均验证通过。SGML 标签、属性、ID、linkend、实体、注释及代码/标识符保护区签名与基线一致；`git diff --check` 通过。
- 六版可见索引 `see`/`seealso` 与 primary 的比对未发现新增失配；未把原有失配当作本次引入。270 个非 SGML 源文件也已盘点，没有发现需处理的图内中文可见文字。
- 实际查看六版 HTML 章节标题、目录、正文和索引；12 份 PDF 共检查 49 个代表页面。未见所查页面缺字、重叠或裁切；长标题及表格会随纸型换行或跨页。只验收所列代表页，不宣称逐页检查整书。
- [源码和保护检查](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/summary.json)；[索引引用检查](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/index-target-audit.json)；[PDF 页码、图片及结果](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/visual-qa/pdf-manifest.json)；[HTML 页面及结果](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/visual-qa/html-manifest.json)。

现有构建包装脚本使用 `loaddtd`，上述结论是实际解析/构建通过及结构保护区未变，并不冒称全书通过严格 DTD 有效性检查。

**保留的未决项**

| 词族 | 未决来源记录 |
|---|---:|
| F01 | 18 |
| F03 | 22 |
| F04 | 18 |
| F05 | 43 |
| F06 | 2 |
| F07 | 2 |
| F09 | 40 |

典型基线问题包括：旧版本中文夹入较新版 libpq 取消/OAuth API、HOT 或 B-tree 行为说明；复制协议、配置或 MultiXact/DTrace 段落的中文缺项；转义说明与同版英文的技术内容不一致。每项具体版本、文件、锚点和英文证据见未决索引及原始记录。未决保持原内容，没有以“未找到”冒充已验证版本不存在，也没有借用其他大版本英文补译。

PG16 的 `reference.sgml` 确实引用 `pg_combinebackup`、`pg_createsubscriber`、`pg_walsummary` 三页，而固定 `en/16.15` 没有这些参考页。这是额外的书籍来源前置问题，三个文件的包含关系均已保存于 [包含链审计](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/include-chain.json)；其中命中术语的 `pg_createsubscriber` 位置也已进入术语未决台账。PG14/15 的未包含页面另有孤立文件证据，二者未混为一类。

这些位置需要先确定或修复中英文原始基线的版本归属，才能完成余下校准。本次未扩大为全书技术内容重译。

**规则与恢复证据**

- [完整定稿词表](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/rules/glossary.tsv)；[逐条使用规则](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/rules/glossary.rules.tsv)；[检索别名](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/rules/glossary-aliases.tsv)；[保留说明](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/rules/terms-to-preserve.tsv)。
- 原有 `style.md`、`exclude.tsv` 保持未变；规则安装采用执行前原版/当前版/定稿三方比对。[安装与哈希记录](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/rules-install.json)。
- [执行前状态与备份清单](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/baseline.json)；[最终源文件哈希](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/audit/final-source-hashes.json)；[串行集成与恢复断点](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/run/integration-state.json)。历史冻结提案包含已撤销或替代的中间态，恢复时以当前有效记录为准。

报告生成时间：2026-09-08T21:44:36（Asia/Shanghai）。

附：[33 条额外历史译义/缺文观察](/Users/vonng/pgsty/pgdoc/outputs/terminology-14-19-20260908-195117/ledgers/preexisting-out-of-scope-observations.jsonl)，未计入上述术语未决。
