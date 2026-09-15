PG10—PG20 缩略词、系统限制与颜色支持校准记录（2026-09-15）

从 PG18 开始实际读完 acronyms、limits、color，覆盖 28 个完整文件：十一版缩略词、PG12—20 系统限制、PG13—20 颜色支持。另读 24 个相关范围，包括十一版 ANALYZE 的高频值列表段、PG19／20 的完整 GUC 词条，以及十一版 WAL 内部机制节标题，共 52 文件、52 范围。7 个正文文件修订，均为 PG14—20 的 acronyms.sgml。规范仍为 647 条，九项用户回退保持。

三类确认问题均水平核对十一版：

- AL001：PG14、15、16 各有 17 个缩略词条采用未来版本的外链，共恢复 51 处本版英文链接。涉及 ASCII、DBMS、DDL、DML、Git、GMT、ISSN、MSVC、OLAP、OLTP、ORDBMS、PAM、RDBMS、SGML、SSL、SYSV、UTF8。其他八版核准自身链接，PG10 的 HTTP 及旧版大小写 ID 按原文保留。
- AL002：PG16—20 把 MCF 的“与某个高频值相关联的频率”写成“某些高频值”。五版恢复单值含义；PG10—15 无该缩略词条。十一版 ANALYZE 的 “list of some of the most common values” 本来是复数，完整上下文中的“某些高频值”核准保留。
- AL003：PG15 的 LSN 词条把 WAL Internals 引用名称写成“WAL 内部结构”，与目标节标题不一致。改为“WAL 内部机制”；其余十版词条及各版自己的目标节标题核准。

90 个 PG18 主分块、11 组完整文件英文变体及全部中文候选、3 组相关范围实际读完。38 组最终段落或词条完整复读；7 个大父段以已读且未变的外围文本，以及未变或完整复读的子词条组合核准。1,042 叶段、27 父段，179 叶段同源组、4 父段组、136 其他组无未决冲突。PG19 GUC 词条比同源译文多出的 firstterm 包装单独核准，不抹除合法标记。

905 个完整缩略词条与 135 个限制表行共 1,040 项逐版核准。缩略词版本边界：JIT／JSON 从 PG11 起，MITM／SNI 从 PG14 起，MCF／MCV 从 PG16 起，AM 从 PG17 起，AIO／ACL／I/O 从 PG18 起，MXID 仅 PG20。PG10 的 HOT 外链、PG11 起 storage-hot 链接，以及 PG16 起 LSN 词汇表链接均按本版英文保持。GUC 的正式展开名 Grand Unified Configuration 保留，配套中文说明覆盖配置子系统、单个参数及内部／构建时设置；它不属于漏译。

系统限制逐行核对所有数字、单位、边界及说明：数据库数 4,294,950,911，关系数 1,431,650,303，默认页大小下关系 32 TB，页数 4,294,967,295，表列数 1,600，结果列数 1,664，字段 1 GB，索引列数／分区键 32，标识符 63 字节，函数参数 100，查询参数 65,535。单页约束、定长与变长字段、TOAST 指针、删除列与 NULL 位图，以及行外值 OID 空间、分配性能与分区说明全部读完；不把理论限制当作操作建议。PG10、11 不存在独立 limits 附录，已核对对应文件、实体声明和主文档包含项。

颜色支持核准 PG_COLOR 的 always／auto、标准错误终端条件，PG_COLORS 的冒号分隔、SGR 值和终端解释，以及默认 error／warning／locus 颜色。note 与青色 01;36 从 PG15 起存在，旧版默认串不加入未来字段。PG10—12 无独立 color 附录，已核对文件与包含边界。

全部行内字面量与源注释核准；本批无 programlisting／screen 等原始代码块。保留五个 LSN 中文链接标签、七个既有 PostgreSQL productname 包装和一个既有 GUC firstterm 包装。24 个已有本地 ID 均绑定自身英文匿名对应节点，完整保留。387 处问题相关源标记全部绑定到完整已读范围；28 条实体声明、包含和完整目标链，以及五个旧版缺节边界均有证据。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-matrix.md)含 19 组、209 格：9 修复、161 核准、32 不适用、7 格式例外。这些是列明范围的核验结果，不是全书完成率。

新快照 checkpoint-acronyms-limits-color-ready：十一版 4,704 节点，159 条范围内提示全部闭合，零未决、零漂移、零子节点数量差异。其中 24 条为已有本地 ID；135 条来自限制表首列已译为中文，包括 126 条行名定位和 9 条整表配对提示，已逐版将完整 14 个数据行、上限值与说明双向绑定。保留初次解析与分类结果，不按提示类别直接忽略。

当前中文＝审定稿＝新快照，固定英文＝本次解包英文。历史与参考书目上一批提交 45960603 已核验。本批准备阶段提交，BKI 正文继续阅读。历史 2,466 个待追溯单元已有 73 个以当前完整核准范围重新绑定，仍余 2,393 个；这是证据追溯，不新增语义阅读完成量。全书余项和十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-reread-proof.json)、[父段组合](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-composed-parent-proof.json)、[词条与表行](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-entry-and-limit-row-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-version-boundary-proof.json)、[不存在的独立附录](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-absence-proof.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-source-inclusion-proof.json)、[全部问题标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-all-occurrences-closure.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-existing-local-ids-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/acronyms-limits-color-full-reviewed-certificate.json)。
