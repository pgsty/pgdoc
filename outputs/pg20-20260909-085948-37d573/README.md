# PostgreSQL 20devel 中文增量翻译交付

本轮已将正式增量翻译写入 [zh/20](/Users/vonng/pgsty/pgdoc/zh/20)，完成固定源码适配、实际 HTML / A4 PDF / US PDF 构建和视检。验收结论为**增量交付通过，继承底稿未决项单列保留**。没有提交、推送或发布；PG14—19 中文、英文输入和冻结术语规则未改动。

## 产物

| 产物 | 结果 | 文件 |
|---|---:|---|
| HTML | 1,157 页；构建退出码 0 | [HTML 首页](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/html/index.html) · [本地预览](http://127.0.0.1:18420/) · [HTML 压缩包](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/postgresql-20-zh-html.tar.gz) |
| A4 PDF | 2,852 页；构建退出码 0 | [A4 PDF](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/postgresql-20-zh-A4.pdf) |
| US PDF | 3,035 页；构建退出码 0 | [US PDF](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/postgresql-20-zh-US.pdf) |
| 中文源码 | 490 个文件，包括 2 个生成表本地化文件 | [源码及构建适配压缩包](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/postgresql-20-zh-source.tar.gz) |
| 中文差异 | 相对于开工继承底稿；已在隔离目录应用并重算全部文件哈希 | [zh20-source.patch](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/zh20-source.patch) |
| 构建适配差异 | 两个入口和一个固定源码准备器 | [build-adaptation.patch](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/build-adaptation.patch) |

源文件对开工中文底稿的实际变化：新增 57、删除 2、修改 177、不变 256。其中 55 个上游新路径加 2 个生成表本地化源文件组成 57 个新增文件。英文未变的 254 个路径均逐字节保留冻结中文；另有 2 个英文变更路径不需要改变最终中文。完整逐文件哈希在 [final-files.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/final-files.json)。

## 固定身份与复现

- 上游完整提交：`86f7c82cf1023e3599f40f939727791a7090cd44`，版本声明 `20devel`，源码位置 [固定 PostgreSQL 完整源码](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20)。
- 三次构建分别复制了相同的 7,680 个已验证跟踪文件；`configure.ac`、`configure`、`meson.build` 的版本一致。清单见 [upstream-source-manifest.json](/Users/vonng/pgsty/pgdoc/outputs/pg20-20260909-085948-37d573/upstream-source-manifest.json)。
- 唯一英文主差异是 `en/18.6 → en/20`；中文主底稿为本轮冻结 `zh/18`，树 SHA256 `70d2dd7be53957a588c3840d6da39cde3d12a346874ae1f667780c77e4b8f2a3`。PG19 仅作经英文确认的局部复用来源。
- 七个现行规则文件集合 SHA256 `e69e0634ca572ee8eca23304983474ed083c3c20e550d48d8fa341b32a38325c`；逐文件身份见 [frozen-rules-files.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/frozen-rules-files.json)，全部单元已关联这些输入哈希。
- 最终中文源文件清单 [final-source-files.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/final-source-files.json)，构建工作区的每个覆盖文件均与该清单一致。命令、时间、退出码、工作区、日志哈希和产物哈希保存在 [results.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/results.json)；独立复核见 [final-build-audit.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/final-build-audit.json)。

复现同一固定源码的命令如下。PDF 使用已安装字体的规范名称，以保证 SVG 内的中文也能被 FOP 正确识别。

```bash
cd /Users/vonng/pgsty/pgdoc
export PGDOC_SOURCE_DIR='/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20'
export PGDOC_SOURCE_COMMIT='86f7c82cf1023e3599f40f939727791a7090cd44'
export PDF_CJK_FAMILY='阿里巴巴普惠体 3.0'
KEEP_WORK=1 bin/build_standalone_docsrc.sh zh/20 zh 20 '/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/html'
KEEP_WORK=1 bin/build_standalone_pdfsrc.sh zh/20 zh 20 '/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/postgresql-20-zh-A4.pdf' A4
KEEP_WORK=1 bin/build_standalone_pdfsrc.sh zh/20 zh 20 '/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/postgresql-20-zh-US.pdf' US
```

构建器仅在显式给出固定源码参数时启用该路径，拒绝不完整参数、短提交、提交不符、版本不符及脏跟踪文件。两个入口的 12 个拒绝测试通过；未提供固定源码参数的 18.6 原默认路径也完成了 1,148 页 HTML 构建。见 [pinned-build-negative.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/pinned-build-negative.json)、[build-compatibility-18.6.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/build-compatibility-18.6.json)。`zh/20/Makefile` 保留项目定制，仅把默认版本改为 20。

## 覆盖与翻译证据

1,158 个差异块全部关联实际处置：原始 1,133 个，生成表 25 个。12,393 个单元中，原始 12,368 个、生成表 25 个；每个单元恰好归属于一个内容任务。53,104 个去重的精确片段逐一重读原文件并验证 Unicode 偏移、完整文本和 UTF-8 SHA256，8,732 个涉及输入文件重新核对哈希。这里的单元数量包含结构、资源、空白和旧侧替换配对，不能当作新译段落数量。

| 单元状态 | 数量 |
|---|---:|
| `verified` | 1,868 |
| `structure_only` | 3,398 |
| `reused` | 4,753 |
| `baseline_unresolved` | 5 |
| `deleted` | 2,313 |
| `literal_synced` | 31 |
| `regenerated` | 25 |

任务表共 1,308 行，最终状态为 1,294 项 `verified`、9 项 `reviewed_with_baseline`、5 项 `baseline_unresolved`。原始 TASKS.tsv 保持冻结；最终结果另存为 [TASKS-RESULT.tsv](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/TASKS-RESULT.tsv) 与 [tasks.jsonl](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/tasks.jsonl)。最终核对按依赖 DAG 的拓扑顺序进行，该顺序用于验收对账，不伪造早期翻译操作时间；原始事件和工作前快照仍保留。

| 证据 | 用途 |
|---|---|
| [units.jsonl](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/units.jsonl) | 唯一任务归属、来源文件哈希、复用依据、精确前后片段引用、术语、检查和未决原因 |
| [fragments.jsonl](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/fragments.jsonl) | 去重保存前后及来源完整文本，路径、零起始 Unicode 偏移与 SHA256；部分结构单元引用容器作为上下文，不表示整容器被重译 |
| [hunks.jsonl](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/hunks.jsonl) | 每个原始/生成差异块与单元、处置状态的关系 |
| [decisions.jsonl](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/decisions.jsonl) | 11,950 条局部组装、继承、复用、字面同步与基线决定 |
| [canonical-review.jsonl](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/canonical-review.jsonl) | 2,905 个共义检索组的任务与决定映射；涉及实际复核译文的 8 个完全相同英文复用组无分歧 |
| [terms-new.tsv](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/terms-new.tsv) | 14 条术语/术语族决定，其中多事务为既有词族确认；获取或创建关联 ON CONFLICT DO SELECT 语境 |
| [final-ledger-audit.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/final-ledger-audit.json) | 独立片段、输入、单元唯一归属及差异块覆盖检查 |

结构迁移共 40 个根映射：函数章拆为 32 个目标，3 个废弃附录迁移，5 个 logicaldecoding 同文件归属调整。根映射全部落地，旧 `func.sgml` 在片段保存及核对后删除；旧 `release-18.sgml` 由开发版占位发布说明替代。276 条嵌套映射中 275 个最终锚点存在；`functions-sqljson-misc` 在冻结中文中已经缺少对应表格，明确保留为基线未决，未伪报迁移完成。来源片段与结果见 [结构片段](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/structures)、[source-audit.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/source-audit.json)。

生成表由固定 PG20 输入实际产生，并通过 [localize-generated.py](/Users/vonng/pgsty/pgdoc/zh/20/localize-generated.py) 与 [generated-translations.json](/Users/vonng/pgsty/pgdoc/zh/20/generated-translations.json) 的完整输入/输出哈希约束进行局部本地化。监控章节原来内嵌的旧等待事件表改用 PG20 生成实体，231 条已有中文说明迁入可复现覆盖层；仅为匹配 PG20 身份修正旧事件名称大小写。39 条底稿原已缺失的说明保留英文并单列。源缓存中的原始生成表未改动；六张实际生成表和 version.sgml 的三个构建副本均已核对一致。

## 验收结果与必要附加修正

- 严格 XML DTD 验证通过，独立 SGML 检查未发现重复 ID 或悬空 `linkend/endterm/zone/otherterm`；包含实体均由实际固定构建展开成功。共有 7,538 个源/生成 ID。缺少的 14 个英文 ID 均为已确认底稿缺口，没有最终活跃交叉引用指向它们。
- 已审查字面、代码、数字和英文残留候选；10 项字面差异均有语境/底稿解释，9 项数字候选均确认是中文数量、日期或数字表达而非数值错误。证据见 [literal-exception-review.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/literal-exception-review.json)、[numeric-review.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/numeric-review.json)、[terminology-candidates.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/terminology-candidates.json)。
- 现行九项术语订正及索引清理/索引收尾清理、并行应用、输入转义约定继续有效；未借本轮工作整体替换或润色未变化正文。
- 6 处已有中文内容补齐必需上游 ID；移除 3 处复制带来的重复自动 ID；混合变量列表补上 19 个最小必要自动 ID，以满足上游链接样式的构建约束。全部附加修正有单独台账，不算作新功能翻译。
- 视检后完成 11 项局部修正：WAIT FOR / OAuth 说明标签、SNI/config/datatype/查询树/BKI 参数串换行、新 pg_plan_advice 索引长名称换行，以及新 psql `%S` 与旧 `%s` 的 HTML 锚点区分。所有真实命令值、标识符和源 SGML ID 保留。
- 实际查看 20 个 HTML 页面截图与 31 张 PDF 页面图；两种纸型都检查中文字体、表格和代码，封面均显示 20devel，中文字体嵌入且无缺字警告。具体页码与观察见 [视检记录](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/visual-qa/REVIEW.md)。
- 全站本地链接/资源检查 35,653 项：无新增失效链接、无重复 HTML ID；已记录的旧邮箱页脚问题单列。`git diff --check` 和两个构建脚本的 Bash 语法检查通过；源补丁已在隔离目录重放并验证完整最终哈希，不对继承格式做批量清理。

必要附加修正清单：[final-structure-repairs.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/final-structure-repairs.json)、[build-source-repairs.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/build-source-repairs.json)、[visual-source-repairs.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/ledgers/visual-source-repairs.json)。最新实际源文件哈希优先于较早的分阶段中间快照。

## 确切保留项

以下是按照“英文未变不整段重译”的合同保留的底稿缺口及版式问题，不标记为已翻译；几类清单存在交叉，不能相加作为缺译总数。

| 原始单元 | 文件 | 已确认的底稿缺口 |
|---|---|---|
| `U20-6784978e7bd214c3` | `func/func-aggregate.sgml` | json_object_agg_strict 行缺失；英文仅 can not → cannot。 |
| `U20-056ef988ce93deb7` | `func/func-aggregate.sgml` | json_object_agg_unique_strict 行缺失；英文仅 can not → cannot。 |
| `U20-b1fe151be99ccd93` | `func/func-binarystring.sgml` | 整型与 bytea 转换段落缺失；英文仅 AS 大写。 |
| `U20-087448fbac662ba2` | `func/func-json.sgml` | jsonb_populate_record_valid 行缺失；英文仅示例 SQL 大小写。 |
| `U20-07c76cd9d92a31bd` | `func/func-json.sgml` | JSON lax 数组过滤示例段落缺失；英文仅 SELECT 大写。 |

101 条基线 ID 候选全部审查，其中 6 条只补锚点，80 条已分类为生成表身份、项目自动锚点或不应导入的历史候选。仍保留的 15 条 ID 问题如下：

- `functions-sqljson-misc`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-PQconnectPoll`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-PQconnectionUsedGSSAPI`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-PQfullProtocolVersion`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-PQgetCurrentTimeUSec`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-PQsocketPoll`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-connection-check-standby`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-connection-gss-startup`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-pgres-tuples-chunk`：冻结底稿缺少该英文 ID/相应内容。
- `planner-stats-extended-functional-deps`：冻结底稿缺少该英文 ID/相应内容。
- `planner-stats-extended-functional-deps-limits`：冻结底稿缺少该英文 ID/相应内容。
- `planner-stats-extended-mcv-lists`：冻结底稿缺少该英文 ID/相应内容。
- `planner-stats-extended-n-distinct-counts`：冻结底稿缺少该英文 ID/相应内容。
- `planner-stats-single-column`：冻结底稿缺少该英文 ID/相应内容。
- `libpq-connection-setenv`：冻结中文已有的额外旧连接状态条目。

39 条等待事件说明保留为 PG20 生成英文，完整事件名：

`CheckpointerShutdown`, `IoWorkerMain`, `LogicalParallelApplyMain`, `ReplicationSlotsyncShutdown`, `WalSummarizerWal`, `WaitForStandbyConfirmation`, `AioIoCompletion`, `AioIoUringExecution`, `AioIoUringSubmit`, `CopyFileCopy`, `DsmAllocate`, `RelationMapReplace`, `WalSummaryRead`, `WalSummaryWrite`, `CheckpointDelayComplete`, `CheckpointDelayStart`, `HashGrowBatchesReallocate`, `HashGrowBucketsReallocate`, `LogicalApplySendData`, `LogicalParallelApplyStateChange`, `MultixactCreation`, `WalReceiverUpstreamCatchup`, `WalSummaryReady`, `applytransaction`, `AioUringCompletion`, `AioWorkerSubmissionQueue`, `DSMRegistry`, `DSMRegistryDSA`, `DSMRegistryHash`, `InjectionPoint`, `LogicalRepLauncherDSA`, `LogicalRepLauncherHash`, `ParallelBtreeScan`, `ParallelVacuumDSA`, `SerialControl`, `WaitEventCustom`, `WALSummarizer`, `SpinDelay`, `WalSummarizerError`.

其他已记录的继承例外：collation 等少数中英文段落原已合并，保留原正文及示例；项目保留的自动 ID、既有界面词（Table of Contents / Index / Synopsis 等）未整体重做。页脚 `pgsql-docs@lists.postgresql.org` 未带 `mailto:`，在 1,157 个 HTML 页面各保留一次。A4 / US 分别仍有 20 / 16 条旧版式溢出提示，以及字体回退、断词模式和 span 提示；本轮新增溢出已修复，剩余项的冻结中文来源与完整日志见 [pdf-baseline-layout-proof.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/pdf-baseline-layout-proof.json)、[pdf-layout-diagnostics-final.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/pdf-layout-diagnostics-final.json)、[pdf-final-audit.json](/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/checks/pdf-final-audit.json)。

正式原始任务表与计划仍是输入证据，其 pending_formal_execution 字段不代表未执行；应以本轮独立的 TASKS-RESULT.tsv 及具体单元状态判定。交付目录中的 execution/ledgers/checks/visual-qa 链接指向保留的完整运行证据，源码与 HTML 压缩包和两个 PDF 可独立取用。`MANIFEST.json` 和 `SHA256SUMS` 提供产物身份。
