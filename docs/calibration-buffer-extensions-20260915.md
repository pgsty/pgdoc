PG10—PG20 缓冲区扩展与文件节点校准记录（2026-09-15）

从 PG18 开始完整阅读 pg_prewarm、pg_buffercache、oid2name，再核对各版全文变体与中文候选：共 31 个主阅读分块、17 个全文变体、33 个完整文件。关联内容扩展到完整发行说明条目及最小完整表格／参数范围，59 组原始关联、4 组补查和 13 组源出现位置余项均已实际阅读。合计 117 文件、259 范围，其中 226 为关联范围。

本批修订 88 正文文件及 3 规范文件，十二类问题逐版修复如下：

- BUF001：PG10—14 pg_prewarm 混入新版扩展标题，恢复各自短标题；PG15 原已正确，PG16—20 保留自身长标题。
- BUF002：PG10—13 pg_buffercache 引言提前写入逐出缓存能力，删除自身英文没有的句子；PG14—16 原已正确，PG17—20 保留逐出能力。
- BUF003：十一版普通说明混用 filenode、文件结点、文件节点，统一为文件节点。覆盖存储章、函数表格、oid2name、校验工具、WAL 工具和监控；严格保留参数、列名、路径、filenode.1／filenode.2 文件名示意、代码与输出表头。
- BUF004：PG14—20 预热参数说明残留关系 fork，改为关系分支；PG15 发行说明的分叉号改为分支编号。PG10—13 相关说明原已正确。
- BUF005：PG13—20 ALTER TYPE 的 per-type storage settings 索引词条未译，补为“各类型的存储设置”；PG10—12 没有该词条。上一批 amcheck 报告登记的待修项在此闭合。
- BUF006：PG13—20 pg_buffercache 的三处列引用说明残留 references，全部补译；pg_stat_statements 的两处相同问题同步核对，PG15 原已正确，其余七版修复。PG10—12 保留自身四列表格布局。
- BUF007：PG10—14 pg_monitor 的成员被写成具有该角色权限的角色，恢复自身成员措辞；PG15—20 保留本版英文权限措辞。
- BUF008：PG18 NUMA 发行说明漏掉感知含义，并把函数、系统视图和 NUMA 节点拼成断句；恢复完整两段语义及全部原始链接。其余十版无该对应发行说明条目。
- BUF009：PG18 新增逐出接口的发行说明将未钉住缓冲区写成未固定，按现行规则校准；PG19—20 同类接口核准。
- BUF010：PG19 发行说明中的普通 buffer／dirty 未译，补为“将缓冲区标记为脏”；不改实际函数和列名。
- BUF011：PG11—13 预热未完成时关闭数据库集簇的发行说明混用集群，按现行术语统一；其他版本无该条目。
- BUF012：PG15 两个预热配置参数的索引标签未译，补齐“配置参数”；其余适用版本核准，PG10 无这两个参数。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-matrix.md)共 27 组、297 格：64 修复／复用、126 核准、87 不适用、20 英文疑点格。62 组最终译文已复读；1,136 叶段落、22 嵌套父段落和 74 原始块核准。229 个同源叶段组、2 个父段组及其他单元经核对，无未决同源冲突；保留既有合法标记与不同表格中等义的说明标签。

逐版保留接口边界：后台预热自 PG11，模块长标题自 PG16；缓存汇总和使用计数自 PG16，逐出单个缓冲区自 PG17，NUMA、逐出关系和全部缓冲区自 PG18，操作系统页视图及标脏接口自 PG19。PG17 的逐出函数返回 boolean；PG18 起保留对应的逐出／刷出状态列。oid2name 的长选项与环境节自 PG12，PG_COLOR 自 PG13，扩展路径列自 PG19；PG10—11 的 -H、-P 保持本版文本。

预热三种方法、NULL 起止块语义、缓存不足时的淘汰行为、自动预热状态文件和工作进程、各版权限与诊断限制均已核准。缓存视图跨数据库关联必须限定数据库 OID，单个缓冲区信息一致不代表整次查询一致；NUMA 页面查询的成本与内存分配影响、并发导致逐出结果过时、工具要求运行中的服务器及完整系统目录，均按原文保留。

1,811 处相关源标记精确分拣：1,701 处绑定已读正文，99 处绑定 33 条实体声明／包含链，11 处为非渲染源注释出现位置。其中 PG16 两个既有缺失的编写者注释涉及 3 处出现位置，完整可见条目的作者和提交链接保留；其余 8 处注释完全一致。各版本实体包装文件按实际来源核对，未把整个包装文件算作本批已读。

74 个原始块中，71 个与自身英文逐字一致；PG14—16 oid2name 的一条英文提问注释采用既有等义措辞，命令、输出及其他字节均一致，予以保留。PG14 两处既有包装分别是相同 PostgreSQL 名称的 productname 标签和两次 FSM 的 acronym 标签；PG16 额外的 pg_buffercache_usage_counts 索引词条指向本版已有函数，也予以保留。这些均有原始标记级证据，未作笼统豁免。

英文原文疑点分三类保留：PG10 发行说明提前提及 PG11 才引入的 autoprewarm；十一版 oid2name 示例的表空间路径缺少自身存储章描述的版本子目录；PG13—20 反向映射说明使用 pg_relation_filepath，而 PG10—12 使用 pg_relation_filenode。这里记录原文差异，不擅自改写中文函数名或示例。

新增第 647 条 filenode → 文件节点，词表和规则各 647 条，九项用户确认回退保留。当前中文＝审定稿＝checkpoint-buffer-extensions-ready 新快照，固定英文＝本次解包英文；十一版 3,621 节点精确绑定，21 条范围内解析提示全部核准，零未决、零漂移。全书原始审计退出码保留，本结论只覆盖本报告范围。

上一阶段提交 5eb2434 已核验；本批准备阶段提交。字符串搜索扩展的后续通读已启动。全书剩余语义范围、历史独立对账，以及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-all-occurrences-closure.json)、[实体链](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-source-inclusion-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/buffer-extensions-full-reviewed-certificate.json)。
