PG10—PG20 intagg／intarray 校准记录（2026-09-15）

从 PG18 开始完整核对两个扩展：34 个主阅读分块、7 个英文全文变体及全部中文候选，覆盖 22 个完整模块文件。随后实际阅读 42 组完整关联内容和 12 组补充范围，合计 97 文件、148 范围，其中 126 个关联范围。28 个正文文件有修订，没有新增术语规则，现行 647 条及九项用户回退保持。

确认并修复三类问题：PG10—14 的 intagg 混入未来版本长标题，恢复本版短标题；PG14—16 的 intagg 示例正文和六个 SQL 块混入新版 many_to_many／left_table／right_table 命名，恢复自身英文的 one_to_many 旧示例，共 18 个代码块；PG14—18 发行说明的 selectivity 误译为“选择性”，按现行第 479 条词表改为“选择率”。十一版全部中文 SGML 中针对“选择性估算／估计”的搜索找到 25 处，均逐一绑定到实际读过的本版英文后修复；“选择性恢复”等其他含义保留。

此外，复用已有同源译文：PG10—14 intarray 作者段、PG15 NOTICE 与崩溃风险说明，以及十一版 ECPG TYPE 参考页的“示例”标题。共 7 个 intagg、5 个 intarray、11 个 ecpg 和 5 个发行说明文件修订。这些措辞统一不另计技术缺陷。旧版“交换操作符”与新版“交换子”均忠实，现行词表未另设该条，本批未因偏好替换。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-matrix.md)包含 21 组、231 格：30 修复／复用、126 核准、59 不适用、16 原文疑点。22 组最终译文均已复读；3 组同源候选全部核对后复用。165 个叶段同源组、10 个父段组和 137 个其他单元组无未决冲突。

本版边界均保留：intagg 的新版示例自 PG17，说明性长标题自 PG16；intarray 受信任说明及可配置 numranges／siglen 自 PG13。旧版两类表格与新版函数签名、相邻去重和排序去重区别、数组 NULL 限制、多维数组按存储顺序处理、全部操作符和 query_int 布尔表达式、GiST／GIN 包含方向差异均完整核对。旧别名说明到 PG13，PG14 的移除条目另行阅读。签名参数默认值、上下限、空间精度权衡和性能基准步骤均保留。

关联核对包括完整 CREATE OPERATOR CLASS 示例、GiST union 的 C 示例、ECPG TYPE 全参考、SQL 多态函数示例、安装权限和受信任清单，以及字段溢出、超大输入、INT_MAX、重复解压、统计缓存和选择率估算的完整发行说明。C 局部变量 numranges、SQL 列别名 intarray 和 ECPG 类型名 intarray 均按原始代码处理，没有误当扩展功能。

962 叶段、58 嵌套父段、179 原始代码块核准。179 块均与本版英文逐字节一致，其中 18 块恢复本版英文、161 块原样保留。链接、标记、属性和源注释完整；两处旧版发行说明中的六个行内 SQL 值仅存在既有换行差异，操作符、占位符和标识符保持，未放宽原始代码块比较。

810 处源标记逐项分拣：721 处渲染内容、23 处范围内源码注释，均绑定实际读过的完整范围；另 66 处对应两个模块各十一版共 22 条实体声明／包含链。仅出现在 xref 中的安装、发行说明和受信任清单也已补查，没有将包装文件全文算作已读。

四类固定英文疑点单列：PG10—16 intagg 先声明 left，末例却查询 left_table；PG14—20 的 CREATE OPERATOR CLASS 示例仍列出已从同版 intarray GiST 说明中移除的 &lt;@；PG14 发行说明同时提及两个包含方向，而本版扩展章仍保留 @&gt;；PG13 发行说明中“四字节和八字节整数数组”的链接措辞与目标章节的 int4 数组说明有疑义。共 16 个版本格保留固定英文，并未据此擅改源码或补充译文。没有执行文中 SQL、C 程序或性能基准。

新快照 checkpoint-integer-array-extensions-ready：十一版 3,026 个节点精确绑定，36 条范围内提示全部核准（30 个既有 ID、6 组匿名节点），零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留，阶段结论仅覆盖列明范围。

citext 阶段提交 be4fe38 已核验，本批准备阶段提交。下一批 lo／vacuumlo／tcn／uuid-ossp 的完整核对正在进行。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-protected-proof.json)、[字面量](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-all-occurrences-closure.json)、[实体引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-source-inclusion-proof.json)、[选择率横扫](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-selectivity-horizontal-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/integer-array-extensions-full-reviewed-certificate.json)。
