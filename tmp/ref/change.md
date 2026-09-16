

## 2026-09-08 PG14—19 历史正文术语校准

正式启用 plans/terminology-14-19/refs 的 631 条最终术语表与 631 条逐条规则，并安装 glossary-aliases.tsv、terms-to-preserve.tsv。本次主迁移集合为 68 项净变化；按版本英文语义、字面保护、术语及条件、译风顺序执行。原表与现用表完全相同，已完成三方核对，无后来人工词条冲突。style.md 和 exclude.tsv 保持现行文件。规则、正文、备份及逐处台账运行目录：/Users/vonng/pgsty/pgdoc/tmp/terminology-calibration/20260908-195117。

## 2026-09-09 用户确认的九项术语回退：现用词表已更新

按用户确认，在当前 glossary.tsv 恢复原序号 27、127、179、180、199、213、267、385、600 的原词条与原译：B-树、默认 B-树操作符类、以先提交者为准、以先更新者为准、整页镜像、首部数据、连接类型和方式、百分位点、插入值。第 179、180 项英文词头恢复 first-committer-win、first-updater-win，wins 形式保留为检索别名，不改写文献和代码中的实际拼写。

同步更新上述九条逐条规则，以及 backup block 对整页镜像的关联规则；别名表记录已撤回译法；从 terms-to-preserve.tsv 移除普通概念 B-tree，保留 exclude.tsv 中的真实访问方法名 btree。词表与规则仍各 631 条，字面保护说明现为 48 条。其他词条、译风、排除表及历史审查材料保持原样，未整体安装复审候选中的其他规则调整。

本次仅落实词表及配套规则，未回退 PG14—19 正文。后续正文任务按用户的九项回退指令逐处执行；已确认由此前校准引入的这九项修改，应恢复原译，不以新译也成立为由保留。备份与验证记录：/Users/vonng/pgsty/pgdoc/tmp/terminology-calibration/rules-rollback-9-20260908-235820/。

## 2026-09-09 用户确认的九项术语回退：六版正文与验收完成

本轮按用户明确决定落实原序号 27、127、179、180、199、213、267、385、600 及其必要关联规则，保留前一条记录中已恢复的现用词表、逐条规则、别名与字面保护说明。未整体安装复审候选，backup block 对整页镜像的关联规则已核对一致。原始术语表、冻结 refs、复审意见及旧执行台账完整保留，当前执行入口见 plans/terminology-14-19/ACTIVE.md 与 ROLLBACK-9.md。

PG14—19 中文源文完成 1,895 个定点原子修改、321 个文件：1,626 个撤回历史校准，269 个同步对应概念、索引及简介。第 127 项的 66 处包含在 B-tree 第 27 项的 1,691 处中，不重复累计；full-page image 及明确回指 156 处，percentiles 48 处。其他五项已核查六版，未发现需撤回的历史正文动作。真实 btree 方法名、代码、文献及独立 discrete percentile 的离散百分位数保留。

六版总账包含 299 个语义单元、1,794 个版本格，每个实际修改均有最终行号、同版英文依据和六版处理结果。旧台账的 1,644 个目标片段逐一给出处置，4,778 个非目标历史片段完整保留。当前可确定的回退未决项为 0；39 条既有技术内容、链接或缺位观察以及原有索引与构建诊断另列，不以基线问题拒绝已确认的术语恢复。

最终源码的六版 HTML、A4 PDF、US PDF 共 18 个目标全部实际构建成功；源码精确重建、SGML 结构与字面保护、差异、索引引用、代表页视检及构建内部诊断对比完成。最终验收采用 builds-r3，初轮及中止的中间构建不计入。执行与完整证据：tmp/terminology-rollback/20260909-000310/；交付汇总：outputs/terminology-rollback-9-20260909-000310/REPORT.md。未提交、推送或发布。


## 2026-09-09 最终审查后的订正与六版验收完成

按用户批准的最终审查思路，完成 R1—R4 及所列 P3：区分 index vacuuming 与 index cleanup 阶段；恢复 PG16—19 对流式传入的进行中事务进行并行应用的动作；六版补齐字符输入转义；PG16 普通正文 multixact 统一多事务；同步六版 BKI/psql 空白、BRIN 语序与 PG15 一句发布说明。保留九项既定回退及其余人工修改，不改变任何词表首选。

本轮只补充逐条规则 51、78、84、251、324、476、538 的相关语境，并新增 78 的旧译检索别名。词表与规则各 631 条，别名 26 条，字面保护 48 条；译风、排除表、字面保护、原始表、旧复审及旧执行记录不变。开工入口与结果见 plans/terminology-14-19/CORRECTIONS-REVIEW.md 和 ACTIVE.md。

相对本轮开工备份，34 个中文文件有 108 条混合粒度修改记录，重组为 24 个语义位置、144 个版本结果。每条修改恰好覆盖一次，逐处对照固定版本英文并保留技术差异，未决证据为 0。源文可由备份与台账精确重建；2637 个中文源文件和 2353 个英文源文件已核验，标签、实体、代码、标识符及原换行保持。

订正后的六版 HTML、A4 PDF、US PDF 共 18 项实际构建通过，相关文字与图像验收完成。与上轮 builds-r3 对比，532 条 FOP 警告均为既有诊断，无新增或加重；其中 BKI 类型列表的既有长行越界已通过新旧 PDF 图像比较单列。PG14 config、PG15 logical-replication 的旧未来参数段及监控表旧阶段字面译法另列为历史基线，不借本轮改动扩展成全面重译。

本轮完整台账、前后差异、规则快照、六版构建与验收：outputs/terminology-corrections-20260909-074824/REPORT.md；运行备份与原始证据：tmp/terminology-corrections/20260909-074824/。结论 GO，适用于本轮已批准订正及所审本地修改，不表示整套历史手册不存在其他基线问题。未提交、推送或发布。


## 2026-09-15 PG10—PG20 CREATE TABLE 及关联章节校准

按现行译风与十一版自身英文，新增原序号 632—637：内含列、激进清理、激进扫描、半死亡、hash 分区、由插入触发的清理；同步语境规则和五条旧译检索记录。补充第 380 条分区剪枝的语境说明，保留原首选译名。词表与逐条规则各 637 条；不改写此前用户确认的九项术语回退、排除表及字面保护说明。

新增规则来自 CREATE TABLE 完整页与关联文本的逐版阅读：保留 INCLUDE、扫描与清理操作、页面状态、插入触发条件及 hash 大小写的区别。普通包含关系不视作内含列，实际代码、公式、参数和本版独有功能保持。十一版实际位置、修订稿、规则前后文本和核验记录位于 outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-*；这些校准过程记录仅保留在本地工作区，不纳入版本管理。

本批不代表整书校准或最终 HTML/PDF 验收完成，十一版共 33 项最终构建仍待整书修复后执行。


## 2026-09-15 PG10—PG20 性能章节及关联术语校准

根据十一版各自英文和性能章节完整阅读，新增原序号 638：initplan → 初始计划，配套说明实际 InitPlan 计划标签、输出和内部名称的保留边界。PG17—20 性能正文及 PG11—15 相关发行说明同步使用中文概念；其余版本只核对自身实际位置，不添加新版说明。词表与逐条规则各 638 条，九项既定回退和其余规范不变。选择率、代价、非重复值、B-树及 hash 继续按现行词条及例外执行。

本轮证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-*。全书对账和最终十一版 HTML/A4/US PDF 共 33 项构建继续；范围内修复不代表整书或最终构建通过。


## 2026-09-15 PG10—PG20 维护与权限参考页校准

根据十一版自身英文和关联说明，新增第 639 条：buffer access strategy → 缓冲区访问策略，沿用表采样和术语表章节已有译法。普通说明中的单复数及 literal 标签内的概念均使用此译名；首次括注英文和实际 BufferAccessStrategy 类型、参数、代码、配置值保持。横向核对覆盖 PG10—20 表采样说明和 PG16—20 配置、术语表、ANALYZE、VACUUM、vacuumdb，保留 PG16 的 256 kB 默认值及 PG17 起的 2MB。词表与规则各 639 条，不改动既定九项回退。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-*；全书校准及 33 项最终构建继续。


## 2026-09-15 PG10—PG20 清理与授权说明校准

补入第 640 条 grantee → 被授权者，沿用 ACL 函数参考页的既有译法。十一版全部 366 处英文出现位置逐项归入完整 GRANT 参考页、完整 ddl-priv 节及 281 个信息模式/ACL 函数相关单元；实际字段名、参数和格式占位符保持原样，普通说明中的受让人、被授权人、被授予者统一为被授权者。词表与规则各 640 条，不改动既定九项回退。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-* 和 grantee-horizontal-*；全书校准与 33 项最终构建继续。

## 2026-09-15 PG10—PG20 查询章校准

新增第 641 条 derived table → 派生表，沿用查询章对子查询和 FROM 结果的稳定译法，消除同一章中的生成表、推导表混用。十一版自身英文的全部对应位置均已完整核对；保留基本表与普通生成动作的区别。词表与规则各 641 条，既定九项回退不变。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-*；全书及 33 项最终构建继续。

## 2026-09-15 数据修改章节与命令校准

新增第 642 条 composite column → 复合列，沿用十一版行类型章和发布说明的稳定译法，统一 INSERT／MERGE 的组合列。已扫描十一版固定英文并完整核对所有对应段落，保留复合类型、复合键、列和字段的区别。词表及规则各 642 条，既定九项用户回退不变。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-*；全书及 33 项最终构建继续。

## 2026-09-15 PG10—PG20 转储恢复工具与引用语法校准

新增第 643 条 dollar quoting → 美元引用，沿用语法章的稳定译法，统一普通说明中的美元符引用、美元符号引用及未译概念。已按十一版自身英文核对空格、连字符与 dollar-quoted 形式的全部关联段落；保留美元符号、定界符、标签、原始代码、字面量和选项 --disable-dollar-quoting，区分对整个函数体加引用与在函数体内部引用固定文本。词表及逐条规则各 643 条，既定九项用户回退不变。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-*、dump-dollar-expanded-*；全书校准与 33 项最终构建继续。

## 2026-09-15 PG10—PG20 物理存储及关联说明校准

新增第 644/645 条：out-of-line storage → 行外存储，in-line storage → 行内存储，沿用位串类型、SP-GiST 及既有发行说明的稳定译法。十一版按各自英文核对 TOAST、存储策略、系统目录、限制和相关用例，区分 SQL 文本之外独立传递的参数、编译器函数内联、匿名代码块及脚本内联数据；实际代码、类型、选项与原始输出保持。词表和规则各 645 条，既定九项用户回退保留。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-*；全书及 33 项最终构建继续。

## 2026-09-15 PG10—PG20 amcheck 及 TOAST 关联说明校准

新增第 646 条 toasted → 经过 TOAST 处理，沿用十一版横向核对中已有的 SP-GiST、过程快照和局部解压说明译法。连同 TOASTed 和 acronym 标签拆分的形式完整核对，修复普通说明中的英文残留、toast 字段及 TOAST 化混用，保留实际函数宏、错误消息和原始代码。词表及规则各 646 条，既定九项用户回退保留。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-*；全书校准与 33 项最终构建继续。

## 2026-09-15 PG10—PG20 缓冲区扩展与文件节点说明校准

新增第 647 条 filenode → 文件节点，沿用十一版已核准的 oid2name 旧版选项和 pg_checksums 译法，覆盖普通说明中的复数和 file node，保留实际标识符、路径、代码及输出表头。同步修复旧版未来接口说明、角色成员边界、普通引用和索引标签、NUMA 发行说明。词表及规则各 647 条，既定九项用户回退保留。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-*。全书余项和 33 项最终构建继续。

## 2026-09-16 PG10—PG20 规划器统计信息校准

新增第 648 条 n-distinct → 非重复值，沿用十一版性能指南及 PG10—13 规划器统计信息章节的稳定译法。按上下文统一计数、估计、统计信息和系数的普通说明，保留实际标识符、锚点与原始代码；区别 non-distinct。同步按既有第 325、317、318 条校准多元统计信息和高频值。本批逐版核对未来 EXPLAIN 输出、连接估计公式、8.3 输出提示、psql 提示与反馈例外语义。词表及规则各 648 条，九项用户回退保留。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-*；全书与 33 项最终构建继续。

## 2026-09-16 PG10—PG20 本地化和字符集校准

新增第 649—653 条，统一 Cyrillic → 西里尔字母、Hangul → 谚文、root collation → 根排序规则、root locale → 根区域设置及 Latin 的文字系统用法；复用 SQL 语法、ICU 定制与 CREATE COLLATION 现有译文，区分实际名称、语言、字符编码和文字系统。保留代码、标识符、Unicode 代码点与 BCP 47 标签。十一版完整章节、相关段落与表格水平核查，包含数据库复制约束、SQL_ASCII 含义和 PG16 未来脚注修复。词表和规则各 653 条，九项用户回退保持；全书与 33 最终构建继续。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-*。

## 2026-09-16 PG10—PG20 日期与时间附录校准

新增第 654 条 time zone abbreviation → 时区缩写，沿用数据类型、配置和附录的稳定译法，统一系统目录总览中的时区简写。按十一版自身英文核对空格、连字符和复数形式，保留实际时区名称、缩写值、标识符和代码。同步按既有 Julian Date → 儒略日 规则统一格式模板和日期输入示例标签，区分儒略历。词表与规则各 654 条，九项用户回退不变。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-*；全书及 33 最终构建继续。
- 2026-09-16 zh/16 精校收官批（内部模块 98 文件 + release-16 + 4 小文件）：零新缺陷，无新术语、无术语变更；B-01~B-08 修复均沿用既有术语表条目。
- 2026-09-16 zh/14 精校批次 14c（ref 组 3：create_foreign_table→discard，36 文件 1039 对）：6 项未来内容修复，无新术语。create_function 恢复 PG14/15「8.3 之前」SET 子句段（删 createrole_self_grant PG16+ 污染）；create_sequence 删 UNLOGGED synopsis+条目（PG15+）；create_statistics 删「如果给定了名称」前缀与「必须提供统计对象名称」句（PG16+，zh/10-15 六版）；create_subscription conninfo 还原 PG14 母本句式；create_transform plpython3u→plpythonu（PG15+ 更名，zh/14）；declare 删活动游标唯一名句（PG16+，zh/10-15 六版）。提交 a972f5e + 5cc2765；make -C zh/14 html exit 0（1080 文件）。
- 2026-09-16 zh/14 精校批次 14d（ref 组 4：do→values 全部 SQL 命令页，83 文件约 2400 对）：3 项未来内容修复，无新术语。drop_role 删「并且已被授予该角色上的 ADMIN OPTION」句（PG16+，zh/14+15）；drop_transform plpython3u→plpythonu（PG15+ 更名，zh/14）；set 还原「有些参数需要超级用户权限才能更改」母本措辞（PG15+ 参数级 SET 权限，zh/14）。提交 dc90132；make -C zh/14 html exit 0（1080 文件）。

## 2026-09-16 zh/15 全量精校（tmp/final15 程序收官）

对照 en/15.19，468 单元 + 1 na（pgdoccn-notes）全部完成。共 6 个修复提交：

- **86ebffe** ddl 常量默认值 tip 补「从 PostgreSQL 11 开始」限定语（zh/14-17 四版同修，86 版式）
- **bebb4fe** 未来内容清理：features/declare/pg_waldump（zh/14+15；zh/14 pg_waldump 另删 6 处 PG15 起选项）
- **f0a9d61** monitoring tup_returned 补「该数据库中」限定语（M-01，zh/15/16/17/18/20 五版同修）+ regress 两处 PG16+ 前向污染还原（make check 输出 193/==== 格式、float4 平台示例 HP-UX 10）
- **de51eca** logicaldecoding 可选回调列表删 message_cb（PG16+ 前向污染；zh/14 同修）
- **399970e** pgupgrade 删空 note 残留元素
- **6ca2dee** create_statistics 删 PG16+ 可选名称句（zh/14 同修）

横向波及：M-01（5 版）、86ebffe 限定语（4 版）、bebb4fe/de51eca/6ca2dee（zh/14 同修）。构建验证：zh/15 html 1088 页 / pdf A4 2816 页 / US 2980 页，全部 exit 0 零 error。
- 2026-09-16 zh/14 精校批次 14e（ref 客户端应用：clusterdb→vacuumdb 22 文件约 1300 对）：4 项未来内容修复，无新术语。dropuser 删 PG16+ ADMIN OPTION 权限句（与 drop_role 同族，zh/14+15）；pg_receivewal 删 PG15+ READ_REPLICATION_SLOT 起始位置项、还原 -Z/--compress=level 压缩条目（PG15+ method 形式，zh/14）、删 PG16+ SIGTERM 措辞（zh/14+15）。--restrict-key/\restrict 经核为 en/14.24 含有的 2025 安全回移项，非污染。提交 af2de8f；make -C zh/14 html exit 0（1080 文件）。
- 2026-09-16 zh/14 精校批次 14f（ref 服务器应用：initdb→postmaster 13 文件约 377 对）：3 项未来内容修复，无新术语。pg_checksums 还原「集簇中的每个文件都会被原地重写」措辞（PG15+ 改为按块重写，zh/12-14）；pg_waldump 删「可以多次指定该选项以选择多个资源管理器」句（PG15+，zh/14）与「可以用十进制或十六进制指定」时间线句（PG16+，zh/14+15）。提交 4a1d0fc；make -C zh/14 html exit 0（1080 文件）。
- 2026-09-16 zh/14 精校批次 14g（arch-dev 45 对 + catalogs 2078 对 + protocol 全文）：零缺陷，无改动。protocol 段落计数差（EN 685/zh 625）经逐节结构探针定性为两类既有惯例（EN 嵌套 para 包裹 variablelist、zh 过渡句 para 包裹），82 消息条目字段逐一核对完整；证据见 findings/catalogs-protocol.md。

## 2026-09-16 PG10—PG20 事务内部机制与 pg_resetwal 校准

新增第 655 条 epoch → 纪元和第 656 条 subcommitted → 已子提交。前者沿用现有术语章、协议与函数译法，区分事务纪元计数和时间基准；EXTRACT 字段、输入值及代码标识符保持英文。后者明确子事务状态，不与最终持久提交或预备事务混淆。十一版完整相关上下文已核对；词表与规则各 656 条，九项用户回退不变。证据见 outputs/pg10-20-calibration-20260911-134417/zcode-followup/xact-resetwal-full-reviewed-*；全书及 33 最终构建继续。
- 2026-09-16 zh/14 精校批次 14h-1（服务器编程残留 + 索引方法 + 内部细节 18 文件约 940 对）：3 项未来内容修复（均在 nls）。还原 nls.mk/AVAIL_LANGUAGES 新翻译工作指引（PG16+ 改为 po/LINGUAS）、删除 procedure 中 PG16+ "Add a file po/LINGUAS" step、合并还原 PG14 PO 编辑器段（PG16+ 拆段并新增专用编辑器句）；母本=zh/13。tableam 段落粒度差（9/10）定性为 zh 拆段惯例，内容完整。提交 807ebae；make -C zh/14 html exit 0（1080 文件）。
- 2026-09-16 zh/14 精校批次 14h-2（附录区 6 文件 151 对 + release-14 全文 2349 对）：零缺陷，无改动。release-14 采证：pairdump 2349=2349 平价；结构多重集全等（sect1=25/sect2=52/sect3=13/listitem=1215/itemizedlist=52）；全对标识符+数字保真探针（两轮去噪后仅剩已译英文复合形容词如 out-of-bounds/row-level）；长度离群全量核查为正常中文压缩；零 LONG 离群（无未来内容）。
- 2026-09-16 zh/14 精校批次 14i（附录杂项 16 单元：indexam/external-projects/sourcerepo/docguide/limits/acronyms 81/glossary 200/color/appendix-obsolete×7/biblio）：零缺陷，无改动。证据见 tmp/final14/findings/appendix-misc.md。
- 2026-09-16 zh/14 精校批次 14i-contrib（contrib 区 49 单元 1753 对三组全量精读）：零缺陷，无改动。三重探针全过：平价断言；标识符保真（flag 项全为已译复数缩写/复合形容词/全角括号边缘标点，真缺失为零）；长度离群 SHORT 全量核实为完整中文压缩、LONG 为零（无未来内容）。pgcrypto CVE-2026-14663 ignore-cipher-failure、contrib-spi PG20 移除句均经核为 en/14.24 含有的 2025 上游回移，非污染。证据见 tmp/final14/findings/contrib-review.md。
