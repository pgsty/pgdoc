PG10—PG20 btree_gin／btree_gist 校准记录（2026-09-15）

从 PG18 开始完整阅读两个模块：6 个主阅读分块、11 个全文变体及其全部中文候选，覆盖 22 个完整模块文件。随后实际阅读 45 组完整关联说明和 17 组补查；合计 86 文件、135 范围，其中 113 个关联范围。共修订 40 个正文文件，没有新增术语规则，现行 647 条规则和九项用户回退保留。

- BGD001：PG10—14 btree_gin 引言漏译 sample，补为“示例”；PG15 原已有，PG16—20 原文移除了限定词，不向这些版本添加。
- BGD002：PG15/16 btree_gist 混入未来排序构建段落，按自身英文删除。PG17 原已没有，PG18—20 保留本版段落。
- BGD003：PG18—20 btree_gist 段落中的 firstterm sorted 漏译，采用完整 GiST 章节已有的“排序”。sortsupport 函数和 buffering 参数名称保持原样。
- BGD004：两个模块的普通类型列表改用中文顿号，保留每版类型顺序、名称、标签和原有换行。GIN 的带引号 "char" 与 GiST 的 char 分别保留，没有把二者混同。
- BGD005：PG11—16 对 -multiply_defined suppress 的“报告错误”改为“引发警告”。该条目虽然由检索表达式在 assorted build-time 中的词内匹配带入，仍完整读完并核验；不能把检索命中当作缺陷。最终确认依据是发行说明所指向的[上游提交](https://github.com/postgres/postgres/commit/3aa021b29)及其[原始邮件](https://www.postgresql.org/message-id/467042.1695766998@sss.pgh.pa.us)，后者给出的诊断级别明确为 warning。
- BGD006：PG19 inet/cidr 升级限制中的集簇称谓按数据库语境补全，保留 pg_upgrade 拒绝升级的条件及本应返回的行可能被排除这一缺陷描述。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-matrix.md)包含 16 组、176 格：39 修复／复用、96 核准、41 不适用。10 组最终译文全部复读，4 组原始同源信号全部检查；108 个叶段同源组、5 个父段组及 28 个其他单元组没有未决冲突。时态唯一约束说明中的两组 NULL 前空格差异属于既有等义排版，予以保留。两个扩展在 GIN/GiST 总览中的同一英文说明统一复用。

版本边界分别核准：btree_gin 的 uuid/name/bool/bpchar 自 PG11；btree_gist 的 uuid 在十一版均有、bool 自 PG15；两模块受信任安装说明自 PG13、长标题自 PG16。完整 GiST 章节自 PG14 介绍排序构建，btree_gist 自 PG18 说明排序构建；PG18 发行说明的具体引入条目也已阅读，未混淆这两条边界。PG19/20 的 inet/cidr 弃用节及替换默认操作符类、显式使用旧操作符类和 pg_upgrade 限制已核准。

完整读过 UNIQUE／WITHOUT OVERLAPS 条目、PG19/20 时态主键及唯一约束节，保留 GiST 要求、范围／多范围、空范围与 NULL 的区别、内含列、分区键覆盖及级联删除限定条件。排他约束的动物园示例、按房间排除范围重叠示例、距离最近邻查询和两扩展的标准唯一性限制均按各版原文检查。没有执行这些数据库示例。

完整 GiST 构建方法节与 buffering 参数条目覆盖十一版：sortsupport 前提、OFF／ON／AUTO、effective_cache_size 阈值、有序输入下的代价、额外 CPU／临时磁盘空间和索引质量条件分别保留。相关发行说明还核验了 float4/float8 的 NaN、变长数据不等比较、char(N) 尾部填充、interval 与带引号 "char" 的索引扫描问题，以及相应 REINDEX、升级版本和修复限定条件。float、penalty、distance 和实际 btree 名称按不翻译词表与接口语境保留。

363 叶段、19 嵌套父段、52 原始代码块核准，52 块均与自身英文逐字节一致且未改动。保护标记、链接、源注释和类型列表逐项核准。5 个范围中的 7 个既有行内 SQL 换行差异有精确白名单，只涉及 NOT NULL 与 EXCLUDE 语法的换行，不涉及引号内值或操作符字节。

475 处源标记逐项分拣：403 处绑定已读正文，66 处对应 22 条模块实体声明／包含链，6 处为原样保留的非渲染源注释。仅藏在 xref/link 标签中的引用也补入完整核对范围，没有将其他包装文件内容算作已读。

新快照 checkpoint-btree-data-extensions-ready：十一版 956 个节点精确绑定，34 条范围内提示全部核准，范围内零未决、零漂移、零子节点数量差异。审定范围内当前中文＝审定稿＝新快照，固定英文＝本次解包英文。PG19/20 DDL 文件的范围外分区章节存在随后发生的其他任务修改，完整文件哈希及每个已读范围的当前位置已[单独记录](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-native-external-current-differences.json)；不将这些后续修改计入本批验收。全书原始审计退出码保留，该阶段结论只覆盖上述范围。

其他任务提交的 PG18 GiST 概览修正及 DDL 文件修改位于本批范围之外，已按完整范围哈希确认后保留；本批不包含这些修改。前一批字符串搜索提交 22c09f2 已核验，本批准备阶段提交。下一批 citext 的 PG18 全文及十一版变体已读，关联核对继续。

全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-protected-proof.json)、[行内字面量](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-all-occurrences-closure.json)、[实体引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-source-inclusion-proof.json)、[源注释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-source-comment-proof.json)、[外部修改保留](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-peer-ddl-refresh.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/btree-data-extensions-full-reviewed-certificate.json)。
