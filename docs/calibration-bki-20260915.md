PG10—PG20 BKI 系统目录初始化校准记录（2026-09-15）

从 PG18 开始实际读完十一版 bki.sgml，并读完 pg_depend／pg_shdepend 的 27 个相关完整段落、条目或表行，共 22 文件、38 范围。PG18 的六个主分块中，大外围块另拆成六个完整子节和一个章框架阅读；六块均完成。八个完整英文变体和全部中文候选均已核对，其中 PG10 直接完整阅读中英文件。10 个正文文件修订，均为 PG11—20 的 bki.sgml。规范仍为 647 条，九项用户回退保持。

两类确认问题均已水平核对十一版：

- BK001：PG11—20 的 close 段只说“给出表名是为了做交叉校验”，漏明原文 must。补为“必须给出表名，以便进行交叉校验”。PG10 的原文语法与说明允许省略表名，保留其正确译文。
- BK002：PG11—20 的新增默认列操作说明多出原文没有的“通常”。改为“数据文件只需在需要非默认值的现有行中补上该字段”。PG10 无这一数据文件操作章节，未回填未来内容。

五组同源候选全文比较后，复用 PG15 的前端头文件和基础目录说明、PG13 的唯一函数名说明，以及 PG18 的格式化规则与示例引言。函数名说明清楚表达 proname 唯一性并去掉重复标记。旧版自己的命令、数据字段和示例字节保留。九组最终段落及完整父段实际复读，134 个叶段同源组、11 个父段组和 39 个其他组无未决冲突。

全章核准范围包括：C 结构映射与字段顺序，变长／可空列和 CATALOG_VARLEN，NOT NULL 推断及强制标注，EXPOSE_TO_CLIENT_CODE 与派生头文件，引导目录的自举前置条目；Perl 数据结构、元数据键、默认字段省略、引号及双层反斜线转义、NULL、格式化和批量迁移；OID 预分配、C 宏、重复值检测、保留范围与补丁重编号；符号查找、操作符与函数参数、模式限制、外键元数据及数组类型自动生成；全部七条 BKI 命令、所支持类型、索引填充与自举顺序。

版本差异逐版核准：PG10 是旧版 BKI 后端接口章；PG11 起增加目录声明及初始数据说明；PG12 起增加数组类型自动生成和 8000—9999 开发 OID 重编号说明；PG14 起 BKI_LOOKUP_OPT 及相关外键说明；PG15 起 OID 计数器、12000 固定对象边界与例外；PG19 起 proargdefaults 的 text 数组解释及 Const 节点构造、直接支持类型变化，以及移除 insert 语法中的可选 oid_value。

PG10／11 的 without_oids、insert OID= 与两列示例，PG12 起三列示例，PG10—13 双引号和 PG14 起单引号语法分别保留。pg_database 示例中的 datdba、PGUID、datlastsysoid、datlocprovider、daticulocale、datlocale、dathasloginevt 和 TemplateDbOid／Template1DbOid 均按自己的英文版本核对，未把最新字段回填旧版。

固定对象的完整依赖说明核准：PG10—14 保留 DEPENDENCY_PIN／SHARED_DEPENDENCY_PIN 条目及依赖对象列为零的说明；PG15 起说明系统自身依赖的固定对象不会删除，因此省略相应目录依赖记录。BKI 的“固定”与目录章节保持一致；现行 pinned 术语规则针对缓冲区语境，不据此改写内置对象说明。

926 叶段、82 父段、77 个完整命令条目已核准。61 个原始代码块满足固定英文＝修改前中文＝审定中文，逐字节一致，未运行示例。行内值、命令语法、全部链接、实体及源注释核准；PG10 term 外围换行不同，仅在比较标签内边缘空白时归一化，语法内容保留。十一版中英文共 8,523 个 SGML 文件扫描得到的 42 处问题标记全部落在已读 bki.sgml 中。11 条实体声明、主文档包含和目标文件链已核准。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-matrix.md)共 20 组、220 格：30 修复／复用、143 核准、31 不适用、6 格式例外、10 原文疑点。原文疑点是一类文件名说明：PG11—20 的初始数据段仍以 pg_class.h 举例，而同章说明初始数据保存于 .dat 文件。保留各版本固定英文文件名，记录疑义，不擅改原文或示例。这些格不是缺陷总数或全书完成率。

新快照 checkpoint-bki-ready：十一版 2,114 节点，47 条范围内提示全部闭合，包括 37 个既有本地 ID 和 10 组匿名配对。零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。保留全书原始审计退出码，不把本批核准扩大为全书通过。

上一批缩略词、限制与颜色支持提交 124dfb26 已核验，本批准备阶段提交，内部架构概述继续。历史追溯本次显式适配八类既有验收格式，并严格拆分完整 SGML 根节点：原 2,466 个待追溯单元累计核准 221 个，余 2,245 个，此前 73 个全部保持有效。未改正文、未重放旧补丁，也未计为新增语义阅读。全书余项和十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-reread-proof.json)、[原始代码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-raw-proof.json)、[命令条目](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-command-entry-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-version-boundary-proof.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-source-inclusion-proof.json)、[全部问题标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-all-occurrences-closure.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-existing-local-ids-proof.json)、[源文件名疑义](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bki-full-reviewed-certificate.json)、[历史追溯](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/historical-pending-explicit-adapters-20260915/summary.json)。
