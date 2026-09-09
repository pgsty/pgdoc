# 正式执行：PostgreSQL 20devel 中文增量翻译

请实际完成本轮正式翻译与验收。当前准备已经完成；这份提示词被明确交付执行后，才开始翻译。工作目录 `/Users/vonng/pgsty/pgdoc`。唯一中文目标 `/Users/vonng/pgsty/pgdoc/zh/20/`。不提交、推送或发布。

## 固定身份与先读材料

- 上游为 PostgreSQL 官方 GitHub 镜像 master 上已固定的完整提交 `86f7c82cf1023e3599f40f939727791a7090cd44`，提交时间 `2026-09-08T13:04:56-07:00`，版本声明 `20devel`。固定完整源码 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20`；英文目标 `/Users/vonng/pgsty/pgdoc/en/20`，488 个文件。
- 唯一主英文差异：`en/18.6 → en/20`。冻结英文旧树 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/inputs/en/18.6`，435 个文件，与官方 18.6 源码包逐字节一致；不使用 en/current，不改为 19→20。
- 中文主底稿是本轮开工工作区冻结的 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/inputs/zh/18`，树 SHA256 `70d2dd7be53957a588c3840d6da39cde3d12a346874ae1f667780c77e4b8f2a3`；zh/20 已继承 435 个源文件/资源。它仍是 PG18 底稿，PG_VERSION=18.6 未适配，不能当作已经完成的 PG20。
- 现用规则固定在 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/inputs/tmp/ref`，七个生效文件集合 SHA256 `e69e0634ca572ee8eca23304983474ed083c3c20e550d48d8fa341b32a38325c`。读取其中 style.md、exclude.tsv、glossary.tsv、glossary.rules.tsv、glossary-aliases.tsv、terms-to-preserve.tsv、change.md。目录中额外的 calibrate.md 仅作历史背景。
- 历史可复用来源：`/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/inputs/en/19beta3` 与 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/inputs/zh/19`。英文已与官方 19beta3 源码包 491 个文件逐字节核验；不能整树复制中文 PG19 代替 PG18。
- 完整报告 `/Users/vonng/pgsty/pgdoc/en/diff/20-vs-18.6/20260909-085948-37d573`。先读取 README.md、source-manifest.json、baseline-issues.md、translation-scope.tsv、structural-map.tsv、project-customizations.tsv；随后按具体任务读 raw diffs、hunks.tsv、translation-units.jsonl 和 historical-reuse.tsv。
- 执行任务表 `/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/TASKS.tsv`，共 1308 行；执行计划 `/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/PLAN.md`；固定源码适配 `/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/BUILD-ADAPTATION.md`；台账字段 `/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/LEDGER-SCHEMA.json`。`python3 '/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/scripts/task_view.py' TASK_ID` 可输出一个任务及全部中英文单元，不执行修改。

首次执行先运行 `python3 '/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/scripts/verify_preparation.py' --check-draft`。续作运行同脚本但不带 --check-draft，并核对 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution` 的实际修改台账。不要重新初始化或覆盖 zh/20 中已完成的工作。源文件、规则或上游提交若漂移，记录具体文件和哈希差异；有用户后续订正则落实该明确决定，保留新旧规则身份，不静默混用，也不默认重新抓 master。

## 实测范围

完整路径：新增 55、删除 2、修改 179、不变 254；原始 1,133 个 hunk，+45,519/-48,461 行。SGML 是新增 42、删除 2、修改 169、不变 218；其余为图片、脚本、生成输入、样式和元数据。类型变化和二进制变化均为 0。共有源文件不能整文件重译。

276 条结构锚点记录含 40 个根映射：func.sgml 拆为 32 个目标文件，RADIUS、libpq fast-path、refint 各迁到一个废弃附录；另外 5 个为 logicaldecoding 同文件归属调整。32 是本次实测，完整列表在结构表，不引用旧 PG19 文件清单。functions 章映射只搬章头、简介和章尾，子节按各自映射搬移；先保存并验证全部中文片段，再删除目标旧 func.sgml。libpq-fastpath/refint 的锚点虽继承，正文已改为废弃/移除说明，要按新语义更新。

12,368 个原始差异语义/结构单元中，有 2,357 个 PG18 英文完全匹配继承/迁移单元、1,410 个 PG19 英文完全匹配的中文候选、95 个 PG19 部分语境参考、56 个无对齐历史基础的首次翻译候选。其余包含结构、注释、空白、资源及旧片段删除/替换配对，不能当成首次翻译工作量。生成表另有 25 个辅助 hunk，见 generated-hunks.tsv 与 generated-translation-units.jsonl；它们不抵消主差异。

## 翻译合同

1. 只处理英文新增或发生实际变化的内容；英文未变的 PG18 中文原样复用，不整文件重译，不顺手润色。同一文件允许同时有 copy_unchanged、relocate_or_split、delete、update_structure、translate_new_content、translate_changed_content、sync_literal_or_resource、regenerate、retain_project_customization、baseline_unresolved 等动作；不能为便于分工把文件全标为一种正文翻译动作。
2. 内容比较仅允许忽略非字面块空白、注释和 id/zone 属性，不能丢弃代码或链接目标。id/zone 的原始变化仍必须同步；historical-anchor-map.tsv 记录新增 ID/更名的复用线索。新路径先查结构来源；已有文件新增段落同样先查历史译文。搬移/拆分先使用 PG18 中文，再处理该片段内部英文增量。历史复用必须证明所对应的 PG19beta3 英文与目标片段一致，局部不同则只借用共有内容。old_english/historical_english 标为 structural_path_candidate 或 partial_context 时只是导航，绝非自动替换依据。
3. 按章节 ID、实体入口、标题、相邻段落、列表/表格结构与字面签名定位中文。char_start/char_end 是从零计数的 Unicode 字符偏移，右端不含；行号从一计数，片段 SHA256 基于 UTF-8 字节。所有行号分别来自各自文件；绝不把英文行号用于中文编辑。单位 text 是完整语义上下文，context 字段可能指整章，只供阅读，实际修改范围限于原始差异对应的文本节点。逐项确认边界再写入。
4. 纯移动、空白、注释、结构和代码变动分别处置。旧侧 unpaired_old_span 是尚需与目标替换配对的片段，不是已确认功能删除；同一文件先处理新增/修改，再核对删改台账，避免重复删除替换内容。旧文件删除仅限 zh/20，必须在所有迁移片段保存并核对后进行；同时维护包含链、索引和交叉引用。
5. PG20 英文决定最终技术事实、条件、数值、函数/参数、代码示例及 SGML 层级。原文变更的代码、名称和例子原样同步新版本；保护字面形式不是保留过时 PG18 示例的理由。没有变化的字面内容和手工排版继续保留。不能将所有内联标签内容一概冻结：title、indexterm 可见索引、replaceable 占位说明、lineannotation 和说明性 type/literal 等须按语境判断；真实标识符和命令值必须保护。
6. 规则顺序：先确认对应版本英文语义，再按 exclude.tsv 保护真实字面形式，再按 glossary.tsv 与逐条适用规则选译名，最后应用译风与稳定既有中文。glossary-aliases.tsv 只用于检索/消歧，不作为批量替换字典。禁止用 plans/terminology-14-19/refs 的旧 v2 或 reconsideration 候选整体覆盖当前规则。
7. 九项已确认译法继续有效：B-树、默认 B-树操作符类、以先提交者为准、以先更新者为准、整页镜像、首部数据、连接类型和方式、百分位点、插入值。只按完整词条和语境应用，discrete percentile 的离散百分位数独立处理。继续区分 index vacuuming/索引清理与并列 index cleanup/索引收尾清理，保留 streaming=parallel 的并行应用动作和字符输入转义等现行订正。
8. 同一英文含义出现在多个章节或历史版本时，复用一份确认的中文；canonical-groups.tsv 提供检索组，结构/字面/适用条件不同须记录例外。只读核对并利用 PG14—19，不因 PG20 特性回改旧版，也不能抹平真实大版本差异。一个文件在同一阶段由同一执行者统一处理，其关联术语族使用同一决策记录。
9. 新术语仅对本轮真实新增概念定稿，先查现有同族和技术语境，在 `/Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/runs/20260909-085948-37d573/TERMS-NEW.tsv` 或 execution 的可追溯术语台账记录英文、中文、单元、依据与决定。不重开既有正确词条的审美修订。输入规则保持冻结；需要记录后来用户订正时单独追加来源和哈希。
10. 不调用通用翻译 API 批量重译，不从网上拼接中文手册。可复用本项目已与英文核对的中文，必要技术查证用固定官方源码及官方文档。release-20.sgml 的日期和说明当前是上游占位，保持其真实开发状态，不编造发布日期或移植 PG19 发布说明。

## 执行与台账

按 TASKS.tsv 的 dependencies 组成的有向无环图执行，batch 是粗粒度阶段，不能仅按 task_id 字面顺序运行；P20-BATCH-* 是阶段核对任务。首次动作是检查现有继承底稿，随后进行结构迁移、增量内容、资源/生成/固定构建适配、删除与基线复核、源码验收、实际构建及视检。新建 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution` 保存逐单元台账、目标文件工作前后快照、术语记录、检查和日志。

每个原始/生成 hunk 必须关联实际处置，每个语义单元恰好由一个内容任务负责（结构映射任务提供同一内容的来源证据，不重复翻译）。逐单元记录输入来源与哈希、复用方式、修改前后精确片段、语境判断、当前术语规则 ID、独立检查及未决原因。文件存在、有中文、marker 或自报完成都不能作为完成证明。词法定位候选与 101 条基线 ID 差异要经过审查；未变英文的基线问题单列，必要修复须有同版英文及目标 PG20 需求依据，不伪装成 PG20 增量，不因此整章重译。

## 验收与交付

- 目标目录、包含链、实体、ID 与 PG20 对齐；新增没有遗漏，删除没有错误残留，35 个跨路径根映射及 5 个同文件归属调整全部有处置证据。
- 1,133 个原始 hunk、25 个生成 hunk 与所有单元覆盖可审计；未决项不能标为完成。未变化中文有文件哈希/片段映射证明，额外修改逐项有必要性与来源。
- 独立检查标签/实体、重复与缺失 ID、linkend/endterm/zone/otherterm、包含文件、可见索引、代码/示例、数字和版本条件、当前术语。原脚本放宽中文 IDREF 验证，HTML 构建成功不代替这些检查。
- 按 BUILD-ADAPTATION.md 完成固定源码参数的最小兼容改动；不改旧版默认目标。使用同一固定 PG20 源码和最终中文实际构建 HTML、A4 PDF、US PDF，显示为 20devel；保存命令、退出码、内部日志、最终源码哈希与产物哈希/路径。
- 检查代表性新增页（如 pgplanadvice/ref/repack/func-tid）、实际变更页（monitoring/config/mvcc）、结构迁移页（函数子树、废弃附录）、目录/索引，以及两个 PDF 的中文字体、代码和表格。记录具体可见结果、继承问题与本轮新增问题；check-deps 不能代替实际构建和视检。
- 最终提供 zh/20 源码差异、动作/翻译台账、术语记录、完整 PG20 源码身份、三个实际构建产物、验证结果、基线问题和确切未决项。不要提交、推送或发布。

现在从 P20-INPUT 开始，持续完成上述正式任务；断点续作先对照台账，不覆盖已有成果。
