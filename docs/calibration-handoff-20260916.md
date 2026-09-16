# PG10—PG20 统一校准：总结与续作交接

交接时间：2026-09-16T08:07:37+08:00。本次按用户要求暂停校准、整理交接；**全书任务没有完成**。

**2026-09-16 存储清理更新：** outputs 从 293.42 GiB 降至 97.92 GiB，减少 195.50 GiB。168 个旧 checkpoint 的大型解析缓存已压缩归档并逐文件校验，233 个源码展开工作区已删除；当前 checkpoint、源文快照、阅读证据和未应用草稿保留。旧脚本若依赖散装节点缓存，先按 [清理记录与恢复方法](/Users/vonng/pgsty/pgdoc/docs/calibration-outputs-cleanup-20260916.md) 取回所需文件；本交接的校准进度不变。

## 先看这里

- 工作目录：`/Users/vonng/pgsty/pgdoc`，当前分支 `main`。本次统计时 HEAD：`d0ac90d2aaf472269ad6dd9657d8e7aa763b6bec`。
- 本任务最近一笔完成验收并提交的正文批次：日期与时间附录，`09799bc1a8233430dd5186efc4112a91d8d6bc01`。其后 `b6b6911`、`ad0b645`、`d0ac90d` 是其他工作产生的提交，已保留，不计入本任务的修复数量。
- **已核对当前 HEAD 祖先关系的 65 笔阶段提交，累计修改过 1,779 个不同的 PG10—PG20 中文 SGML 文件**，按批次重复计数为 2,679 文件次。这个数字说明提交涉及的文件范围，不说明每个文件都已完整通读。
- 十一版原始中英文 SGML 扫描清单共 **8,523 个文件**。这也不是语义通读完成数量。
- 当前进行中的事务／`pg_resetwal` 批次：**16 个完整文件、624 个完整关联范围，共 640 个范围，涉及 182 个中文文件**。完整正文和全部候选译文已读，28 个正文文件有修订草稿；**尚未写入正文、尚未提交、尚未完成本批证明和新解析**。
- 当前生效规范仍为 **654 条**。`epoch → 纪元`、`subcommitted → 已子提交` 是第 655、656 条草稿，未应用。
- 历史待追溯项上次核准 **221／2466**，尚余 **2245**；该统计是 2026-09-15 的独立对账结果，尚未纳入其后所有批次。
- 最终中文验收仍为 **0／33**：11 版 HTML + 11 版 A4 PDF + 11 版 US PDF。本任务没有推送或发布。

## 执行要求与固定输入

先完整读取 [原始 PROMPT](/Users/vonng/.codex/worktrees/c22a/pgdoc/plans/pg10-20-calibration-20260911/PROMPT.md)、[执行 TODO](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/TODO.md)、[执行 PROGRESS](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/PROGRESS.md)，再读现行 [译风规范](/Users/vonng/pgsty/pgdoc/tmp/ref/style.md)、[不翻译词表](/Users/vonng/pgsty/pgdoc/tmp/ref/exclude.tsv)、[术语表](/Users/vonng/pgsty/pgdoc/tmp/ref/glossary.tsv) 和 [逐条语境规则](/Users/vonng/pgsty/pgdoc/tmp/ref/glossary.rules.tsv)。优先级为 exclude > glossary > style > 既有译文。

英文固定为：PG10=10.23、PG11=11.22、PG12=12.22、PG13=13.23、PG14=14.24、PG15=15.19、PG16=16.15、PG17=17.11、PG18=18.6、PG19=19beta3；PG20 为提交 `86f7c82cf1023e3599f40f939727791a7090cd44`。在 `zh/<大版本>/` 原目录更新，从 PG18 完整阅读切入，每发现一类问题就横向核对十一版；相同英文复用译文，保留各版自己的功能、代码、SGML、链接、默认值和限制。

必须区分机器信号、实际读过的完整范围、源码修复、新快照解析、提交、最终构建。不得把匹配数量、结构计数或高覆盖百分比当作逐句语义验收。

## 已修复内容

原始 **F-001—F-026** 已逐版处理，包含“修复／原已正确／不适用／项目例外”的明确区分。完整十一版矩阵、每项结论及原报告更正在 [阶段总报告](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)；原始状态索引在 [status.json](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/status.json)。主要修复包括：

- 遗漏的 xref/link/glossterm、引导句、函数表行、参数说明、例子和完整小节。
- 旧版混入未来版本的功能、表格行列、函数、协议参数与示例；按每版英文恢复适用边界。
- 锁表容量公式、复制引言、SQL/JSON 数据模型、文件函数权限、备份控制和 WAL 文件名换算。
- PG14 协议清单、PG15 配置缺段、并行受限项目、RECHECK、SHOW 区域变量、文档指南和 NLS 缺文。
- `polygon(circle)` 的损坏输出、负数 `to_hex` 示例、libpq 参数状态、PG15 `pg_walinspect` 函数集合。
- 后续完整范围校准还覆盖文本检索、数据类型与函数、libpq、ECPG、协议、大对象、查询／DML／DDL、COPY 与转储恢复、权限维护、规则与视图、目录与信息模式、性能、存储与大量扩展模块。具体范围以各批报告和证书为准，不代表这些主题的所有关联文件都已全篇闭合。

原清单并非全部判断都正确：例如对象标识引导句十一版原本都有；`pg_get_acl` 示例缺口实际涉及 PG18/20；纯文本输出小节实际在 PG10—16 存在；`scram_iterations` 缺口实际涉及 PG16—18。已在执行报告中更正，不回写原独立审查材料。

最近完成并提交的批次如下。“正文文件”是该批修订数量，各批之间有重复，不能相加作为去重总数。

| 批次 | 完整主文件 | 关联范围 | 修订正文文件 | 新解析配对节点／范围提示 | 提交 |
| --- | ---: | ---: | ---: | --- | --- |
| 并行查询 | 11 | — | 11 | 1299／0 | `16c3a21c` |
| pageinspect | 11 | 29 | 12 | 2541／14，全部核准 | `39f647f6` |
| 规划器统计信息 | 11 | 147 | 50 | 1279／6，全部核准 | `b9748805` |
| 本地化与字符集 | 11 | 103 | 16 | 14280／46，全部核准 | `62b31b02` |
| 数据库管理与表空间 | 44 | 513 | 33 | 3647／62，全部核准 | `52f4c64f` |
| 日期与时间附录 | 11 | 297 | 44 | 3559／0 | `09799bc1` |

日期与时间附录最后修复了：回拨日两次 1:30AM 的时间关系、转换前后实际采用的 UTC 偏移、PG10—16 缩写由配置文件提供的说明、PG14—16 混入的未来 IANA 优先级内容、儒略日与时区缩写术语。`text search` 短称“文本检索”疑报已经撤回，不能把它批量替换成“全文检索”。见 [该批完整报告](/Users/vonng/pgsty/pgdoc/docs/calibration-datetime-appendix-20260916.md)。

### 文件数量口径

以下按版本、实际文件路径去重。英文和中文文件数包含 SGML 包含文件、参考页等，不等于章节数；“已提交修改过”不等于全文件已读。

| 版本 | 英文 SGML | 中文 SGML | 本任务已提交修改过的不同中文 SGML |
| --- | ---: | ---: | ---: |
| PG10 | 362 | 363 | 152 |
| PG11 | 368 | 369 | 159 |
| PG12 | 370 | 371 | 157 |
| PG13 | 374 | 375 | 161 |
| PG14 | 378 | 379 | 167 |
| PG15 | 385 | 386 | 169 |
| PG16 | 385 | 386 | 165 |
| PG17 | 386 | 387 | 158 |
| PG18 | 389 | 390 | 157 |
| PG19 | 430 | 431 | 168 |
| PG20 | 429 | 430 | 166 |

计算依据：[当前统计及全部提交／文件清单](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/handoff-current-statistics-20260916.json)。所有计入提交已检查为统计时 HEAD 的祖先。另有旧 FDW handler 回执记录 `962932f5faf0a7d9b09c6f9216895faf6f0f0f2c`，当前不是 HEAD 祖先，**本次保守统计已排除**，后续需核查其等价提交或历史变更，不能仅凭回执称它已在当前分支合入。

## 精确断点：事务与 pg_resetwal，正文尚未写入

当前读写证据目录统一为：

```text
/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup
/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/scripts
```

前缀：`xact-full` 为事务阅读清单；`resetwal-full` 为工具参考页阅读清单；**`xact-resetwal-full-reviewed` 为合并修订草稿**。不要与历史 `datetime-full`（日期时间函数）或已经闭合的 `datetime-appendix-full` 混淆。

已实际阅读并保存断点：

- PG16—20 共 5 份完整 `xact.sgml`：PG18 的 5 个完整分块、2 种完整英文变体及全部中文候选。PG10—15 无该文件，包含链缺席证明还需正式落证据。
- 十一版完整 `ref/pg_resetwal.sgml`：PG18 的 21 个分块、6 种完整英文变体和全部中文差异。
- **权威关联清单为 v3**：603 范围、103 组全部读完。v1、v2 是废弃路由，不可用它们宣称实际阅读。
- 手工绑定：13 范围、4 组；补查扩展探针：8 范围、2 组；合计 624 个相关范围。
- 另实际读过 PG17/18/19 的 3 行生成式 `virtualxid` 等待事件和 2 处非渲染源码注释。生成行的英文来自固定源码生成产物，不能当作原始 `monitoring.sgml` 中存在的文本。
- 1851 个主要检索命中、52 个补充命中已用于定位；最终逐命中闭合证明尚未写出。
- 草稿含 927 个叶子段落、49 个嵌套父段、181 个原始块。12 组最终新增文本已全部复读，组 2、3 在去掉“处于 已子提交”的残余空格后再次复读。
- 同源检查：142 组正文、8 组父段、134 组其他文本；跨标记与常规冲突均已消除，仅保留一类既有 `xmin` 行内标签差异。

### 本批确认问题和草稿修复

| ID | 问题及草稿动作 | 适用版本 |
| --- | --- | --- |
| XA001 | GID 引言中的 `xid` 恢复本版 `<type>` 标签 | 16 |
| XA002 | 普通事务计数说明中的 epoch 统一为“纪元” | 16—20 |
| XA003 | subcommitted 译为“已子提交”，保留其不等于最终持久提交的限定 | 16—20 |
| XA004 | 日志文件创建时间“纪元”改为明确的“纪元时间戳” | 10—20 |
| XA005 | 发布说明明确 epoch 或 infinity 不能与其他日期时间字段组合 | 16；其余版本已在关联扫描中核对 |
| RW001 | 恢复旧版四段描述，移除未来选项解释、额外数据目录说明条目、8 kB 注解及新增 WAL 段用途；恢复旧版警告前提 | 描述等 14—16；警告前提 11—16 |
| RW002 | “部分已提交的事务”改为“仅部分提交的事务” | 11—20；10 原本正确 |
| RW003 | WAL 段大小选项恢复本版顺序 | 14—17 |
| RW004 | 清理未来版本非渲染注释；PG20 注释乘数恢复本版 32768 | 清理 10—16；乘数 20 |

注意：RW001 删除的是 PG17 才新增的**说明条目／段落**，不是声称 `-D` 或 `--pgdata` 选项在 PG17 才引入；旧版命令概要已经包含它们。

### 已读例外与待完成的证明

- 181 原始块均未改动。与英文逐字不完全相同的 35 块分为：33 块合法 Result 行注释译文（其中 PG10—12 各一块还有既有空行差异）、PG14 一块输出表头行尾空格差异、PG20 一块 `cmdsynopsis` 标签间空白差异。8 组不同的完整差异都已实际查看。不得把 `synraw` 的 34 个信号直接等同于缺陷；它会忽略那一块行尾空格差异。
- 受保护元素的 11 个信号：PG14—16 三处普通 `xmin` 加 `<literal>` 的既有标记、PG13—20 八处匿名词条 `Epoch → 纪元`。已实际核对，需精确的上下文例外证明，不能全局放宽。
- PG19 `pg_resetwal` 16 个既有本地 ID、PG14—20 `epoch` 条目各 1 个既有本地 ID 应保留。草稿没有增删现有 ID、链接属性。
- 上游疑点 SQ001：`xact` 说 GID 最长 200 字节，十一版 PREPARE 参考页说少于 200 字节。两处分别忠实翻译并单列，不能擅自统一数值。
- 上游疑点 SQ002：`xact` 的“后续唯一命令”可能被读成会话限制。PG18 PREPARE 参考页的“任何会话”和“执行后无活动当前事务”两段刚读过，**尚未纳入完整横向范围**；继续时补读并绑定其他十版，再决定是否仅作为上游表述疑点记录。
- 上游疑点 SQ003：PG16—20 `buffer-extend-start/done` 英文原型的参数数量与说明中的编号数量不一致；五版完整行已读，旧版无相同探针行。保留本版英文对应译文并记录，不自行改参数。

### 直接续作顺序

1. 检查当前 HEAD、工作区和规范。读取 `xact-full-human-progress.json`、`resetwal-full-human-progress.json`、合并前缀的 `counts.json`、`file-plans.json`、`scope-proof.json`、`changes.json`、`new-text-read.json`、`norm-state.json`、`norm-changes.json`。
2. **不要直接重跑现有 prepare／plan／refine 脚本**：它们有防覆盖断言，输入清单和最终草稿已经存在。新增证据写新文件；需调整草稿时先保存原派生结果，并注明精确继承与复读关系。当前已保存一次复读前派生结果于 `xact-resetwal-full-reviewed-pre-reread-amendment-20260916/`。
3. 补齐 SQ002 的十一版关联范围；完成范围／命中／原始块／标签／链接／版本边界／包含链的严格证明，保存真实 `reread-proof`、`raw-proof` 等。参考已经闭合的 `prove_datetime_appendix_final.py`，**不能直接换前缀后无条件套用其固定数字或例外**。
4. 完成每个问题的十一版矩阵与适用性说明，复核计划中全部修改和规范新增。源码哈希必须仍匹配；出现外部修改则先核对、精确重绑定，绝不覆盖。
5. 写入 28 正文和 3 份规范文件草稿后，执行全十一版新快照／原生 SGML 对齐，逐项核准本批范围提示。PG17—19 的生成等待事件行要用带源码清单哈希的独立适配器，不能伪装成原始英文文件中的范围。
6. 新解析通过后生成本批报告、更新总报告／TODO／PROGRESS，以私有 index 提交本批经过审定的路径，保留其他工作的 index 和源码。然后继续全书余项及最终验收。

**当前不存在**合并前缀的 `reread-proof.json`、`protected-proof.json`、`raw-proof.json`、`matrix.json`、`applied.json`、`certificate.json`；没有本批构建或提交。脚本目前只有 [计划脚本](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/scripts/plan_xact_resetwal_full.py) 和 [精修脚本](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/scripts/refine_xact_resetwal_full.py) 等准备工具，后续证明／应用／解析／提交入口尚未建立。不要把文件名里的 reviewed 当作验收已完成。

本批计划时发现其他会话的新 DDL 提交，PG10—16 的 `ddl.sgml` 已改变。本批完整阅读范围仍逐字不变，已通过等值区间重新绑定；详见 `xact-resetwal-full-reviewed-baseline-adapters.json`，保留了外部修改。原始扫描坐标与重绑定坐标不同，最终命中证明应使用原始输入和 `read_chinese_before_offsets`，不能把旧偏移直接套到现文件。

## 剩余工作

### 全书阅读与覆盖缺口

截至数据库管理批次的 PG18 导航清单是 **389 个英文文件、257 个完整覆盖候选**。之后日期附录整篇闭合，可确认为新增 1 个候选，因此交接导航为 **258 个完整覆盖候选、131 个待补读或补证文件**。其中 `xact.sgml` 和 `ref/pg_resetwal.sgml` 的完整阅读已经完成，但本批尚未写入、证明和解析；其他文件可能已经部分读过，甚至主体已读完但边角范围还没补齐，不能统称“完全没读”。这只是 PG18 导航口径，不能乘以 11 推算其他版本的完成度，也不是最终验收比例。

原导航证据：[PG18 逐文件范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/coverage-routing-20260916/pg18-through-manageag.json)、[其摘要](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/coverage-routing-20260916/through-manageag-summary.json)。下一轮应重新生成带新批次的全版本精确覆盖清单，不覆盖旧结果。

30 个主文件／包含入口待补读或补证（以下相对 `en/18.6/`）：

```text
appendix-obsolete-default-roles.sgml
appendix-obsolete-pgreceivexlog.sgml
appendix-obsolete-pgresetxlog.sgml
appendix-obsolete-pgxlogdump.sgml
appendix-obsolete-recovery-config.sgml
appendix-obsolete.sgml
bloom.sgml
config.sgml
dblink.sgml
ddl.sgml
docguide.sgml
errcodes.sgml
features.sgml
filelist.sgml
func.sgml
glossary.sgml
indextypes.sgml
keywords.sgml
logical-replication.sgml
logicaldecoding.sgml
monitoring.sgml
nls.sgml
postgres.sgml
regress.sgml
release-18.sgml
release.sgml
sources.sgml
user-manag.sgml
wal.sgml
xact.sgml
```

101 个参考页待补读或补证（以下相对 `en/18.6/`）：

```text
ref/abort.sgml
ref/alter_aggregate.sgml
ref/alter_conversion.sgml
ref/alter_domain.sgml
ref/alter_function.sgml
ref/alter_large_object.sgml
ref/alter_policy.sgml
ref/alter_procedure.sgml
ref/alter_routine.sgml
ref/alter_schema.sgml
ref/alter_sequence.sgml
ref/alter_server.sgml
ref/alter_statistics.sgml
ref/alter_subscription.sgml
ref/alter_tsconfig.sgml
ref/alter_tsdictionary.sgml
ref/alter_tstemplate.sgml
ref/alter_type.sgml
ref/alter_user_mapping.sgml
ref/call.sgml
ref/checkpoint.sgml
ref/close.sgml
ref/comment.sgml
ref/create_aggregate.sgml
ref/create_cast.sgml
ref/create_collation.sgml
ref/create_conversion.sgml
ref/create_function.sgml
ref/create_procedure.sgml
ref/create_schema.sgml
ref/create_sequence.sgml
ref/create_server.sgml
ref/create_statistics.sgml
ref/create_subscription.sgml
ref/create_table_as.sgml
ref/create_transform.sgml
ref/create_tsconfig.sgml
ref/create_tsdictionary.sgml
ref/create_type.sgml
ref/create_user_mapping.sgml
ref/createdb.sgml
ref/declare.sgml
ref/discard.sgml
ref/do.sgml
ref/drop_aggregate.sgml
ref/drop_cast.sgml
ref/drop_collation.sgml
ref/drop_conversion.sgml
ref/drop_database.sgml
ref/drop_domain.sgml
ref/drop_foreign_table.sgml
ref/drop_function.sgml
ref/drop_group.sgml
ref/drop_policy.sgml
ref/drop_procedure.sgml
ref/drop_publication.sgml
ref/drop_role.sgml
ref/drop_routine.sgml
ref/drop_schema.sgml
ref/drop_sequence.sgml
ref/drop_server.sgml
ref/drop_statistics.sgml
ref/drop_subscription.sgml
ref/drop_table.sgml
ref/drop_transform.sgml
ref/drop_tsconfig.sgml
ref/drop_tsdictionary.sgml
ref/drop_tsparser.sgml
ref/drop_tstemplate.sgml
ref/drop_type.sgml
ref/drop_user.sgml
ref/drop_user_mapping.sgml
ref/dropdb.sgml
ref/dropuser.sgml
ref/fetch.sgml
ref/import_foreign_schema.sgml
ref/listen.sgml
ref/load.sgml
ref/move.sgml
ref/notify.sgml
ref/pg_checksums.sgml
ref/pg_config-ref.sgml
ref/pg_controldata.sgml
ref/pg_isready.sgml
ref/pg_receivewal.sgml
ref/pg_resetwal.sgml
ref/pg_rewind.sgml
ref/pg_waldump.sgml
ref/pgarchivecleanup.sgml
ref/pgtestfsync.sgml
ref/pgtesttiming.sgml
ref/pgupgrade.sgml
ref/reset.sgml
ref/security_label.sgml
ref/select_into.sgml
ref/set.sgml
ref/set_constraints.sgml
ref/show.sgml
ref/truncate.sgml
ref/unlisten.sgml
ref/values.sgml
```

上面含 `bloom`、`dblink`、`config`、`func` 等接近完整覆盖的文件；应先查具体缺口，不从头重复整批工作。其他大版本还需核对本版独有文件、被拆分的包含文件、发行说明和适用边界。

### 历史追溯与一致性复核

上次对账记录在 [summary.json](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/historical-pending-explicit-adapters-20260915/summary.json)：221 条已核准、2245 条待处理，其中 1036 条至少一个原始出现位置缺当前闭合范围证据，961 条不是完整 SGML 根节点的无损序列，248 条无法按记录的出现次数找到根节点。此前 73 条核准记录全部保留、当次零回退；当次涉及 47 组闭合证据、10189 范围。

还要将其后的 BKI、架构、GEQO、JIT、并行、pageinspect、统计信息、字符集、数据库管理、日期附录等新闭合证据纳入新一轮对账；其他历史单元、删除／不适用／生成元素证据仍要独立核对。原始历史台账有 38907 个版本格、3537 个单元，不能把只针对 2466 条待追溯记录的进度扩张为整个台账完成。

续作脚本为 `reconcile_historical_pending_against_closed_scopes.py` 和 `reconcile_historical_pending_explicit_adapters.py`；新结果使用新的日期目录。先前批次跨原始代码块、行内标记的同源正文一致性也仍有独立复核工作。`INPUTS.md`／`INPUTS.json` 的最终输入清单需重新对账。

### 最终构建

本任务最终验收仍为 0／33，已有分批原生解析不代替 HTML/PDF 构建。最后应冻结一个相同源码快照，全部十一版分别生成 HTML、A4 PDF、US PDF，保存命令、退出状态、日志、产物哈希，并抽查 PDF 实际渲染和关键页面／链接。

根 [Makefile](/Users/vonng/pgsty/pgdoc/Makefile) 默认批量版本只有 PG14—18，**必须显式指定十一版**。单版中文目标是 `make zh ZH_VERSION=18`，PDF 为 `make zh-pdf ZH_VERSION=18 PAPER=A4`；批量 PDF 可指定 `ZH_VERSIONS="10 11 12 13 14 15 16 17 18 19 20" PAPERS="A4 US"`。实际执行前读每版 Makefile，正确提供本机依赖；这些是入口说明，不是已运行的构建记录。`check-deps` 仅检查依赖。

可用工具链线索：

- OpenSP 依赖：`/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/agents/archive_build/deps`；PG10 原生解析使用 `NSGMLS`、`OSX`、`SGML_CATALOG_FILES`、`SP_ENCODING=UTF-8`、`SP_CHARSET_FIXED=YES`。
- FOP：`/Users/vonng/pgsty/pgdoc/.cache/tools/fop-2.11/fop/fop`；此前使用 AlibabaPuHuiTi3 字体。
- 现有字体配置：`/Users/vonng/pgsty/pgdoc/.cache/work/standalone-pdf-zh-18.6.GRnjqP/doc/src/sgml/fop-local.xconf`，续作时验证仍存在。
- PDF skill 已在本任务读取，路径 `/Users/vonng/.codex/skills/pdf/SKILL.md`；最终应使用 Poppler 渲染核验。

## 保留事项与易错点

- 本工作目录由多个会话共享；PG9.3、PG9.4 等任务也会推进，HEAD 会变化。只提交本批明确路径，不能 `git add .`、回退或覆盖他人改动。
- PG10—20 规范的九项用户回退保持：B-树、默认B-树操作符类、以先提交者为准、以先更新者为准、整页镜像、首部数据、连接类型和方式、百分位点、插入值。
- `text search` 短称“文本检索”与 `Full-Text Search`“全文检索”有意区分；此前广义检索的 2285 个信号已撤回，不是缺陷或全文阅读证明。
- `NULL`、实际字段／函数／参数／状态常量和代码依规范保留。普通英文概念是否翻译以完整上下文决定，不能按标签类型或字面量扫描统一放宽。
- 日期函数旧 `prepare_datetime_full.py` 曾被误执行，只重建了六份中间清单，没有修改正文。后来从不可变原审定输入确定性重建，1386 历史单元的编号与哈希匹配。记录在 `datetime-function-inventory-recovery-20260916/receipt.json`；它是确定性重建，不是原字节备份。不要再次运行该旧脚本。
- 本任务的重要证据在 `outputs/`，通常不受 Git 跟踪。同一台机器的新会话必须直接使用上述绝对目录；新建 worktree 或克隆不会自动获得这些证据，不能仅看提交中的报告就跳过它们。
- 没有运行文档中的数据库修改命令或 `pg_resetwal` 实例；那些仅是被阅读、对比的示例。

建议下一个会话的首条指令：**“完整读取 docs/calibration-handoff-20260916.md 及其指向的当前断点；从 xact-resetwal 草稿的证明、十一版矩阵和新解析继续，不重跑旧准备脚本、不覆盖共享工作；随后补齐全书阅读、历史对账与 33 项最终构建。”**
