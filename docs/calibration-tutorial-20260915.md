PG10—PG20 教程与关联继承说明校准记录（2026-09-15）

十一版 start.sgml、query.sgml、advanced.sgml 共 33 个完整教程文件，以及十一版 ddl-inherit 完整节均已完成同版英中核对。先读 PG18 的 23 个完整子节及外层框架，再读其余版本全部 14 个英文全文变体及所有中文候选；关联核对 22 个窗口函数定义表行、429 处同类可见索引和 112 个维护、监控、命令参考与发行说明段落。共 166 个文件中的 321 个精确范围，本批修订 58 个正文文件，规范没有变更。

- PG15/16 的窗口教程恢复本版 rank() 示例、并列排名输出和排名子查询；PG14—17 移除错误套用的 row_number 连续编号及并列行顺序解释。PG10—17 同源排名说明统一，去掉本版未收录的“每个部门前两行”解释；PG18—20 保留自己的 row_number 示例。十一版 rank 与 row_number 函数参考表同步核验。
- PG14—17 的继承章节移除误入的 PG18 VACUUM/ANALYZE 默认递归及 ONLY 说明。PG10—13 保留本版行为，PG18—20 保留新行为；维护章、监控章、ANALYZE/VACUUM 参考页及分区注意事项等关联段落已完整核对，原已正确的版本边界继续保留。
- 十一版继承说明补准“已有表的定义必须兼容”及 CHECK 约束名称、检查表达式都须匹配的条件；恢复 LIKE 的 INCLUDING CONSTRAINTS 应当指定以及子表满足兼容性要求的因果关系。PG19/20 自身新增的非空约束要求保留，未回填旧版。
- 十一版修正 OVER 子句的含义：它决定如何划分查询中的行。继承示例的 capitals 改为“州首府”，DDL 示例的海拔单位“尺”改为“英尺”；实际表名、列名和数值保持原样。
- 十一版将安装“很可能”校正为“可能”，删去 psql/createdb 诊断关系中额外的“通常”；PG15/16 恢复本版创建数据库引导语。PG10—13 调整 HAVING/FILTER 引导句，保留 PG10 独有的查询结构、数据及输出。
- 补译天气表、保存点和海拔示例的普通 SQL 注释。聚合错误示例的 WRONG 标注译为“错误”，PG14—16 去掉误入的新版注释前缀，仍保持自身 lineannotation 结构。命令、函数、选项和 SQL 代码没有被当作自然语言翻译。
- 同类可见索引按十一版全文检索逐项绑定，统一数据库、行、列、查询、聚合函数、子查询、视图、外键、事务、窗口函数和继承等索引文字，保留原有 zone 等定位属性。PG15 的 version() 索引恢复为函数标识符 version。PG10—12 的 n_distinct 说明沿用现行第 138 条“非重复值”译法，其余八版已正确。

[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-matrix.md)共 30 个问题、术语、一致性、回归及源文疑点检查组、330 格：168 格修订、107 格原已正确、19 格不适用、36 格保留固定英文疑点。组数不是独立缺陷数。每格绑定完整同版英中语境或已读完整文件的版本边界。

本批实际核对 1,626 个叶段落、110 个嵌套父段落及 1,100 个代码／示例块。200 个同源叶段落组、64 个父段落组及 101 个其他文本组均无未处理的语义冲突；一组纯格式差异保留原样。79 组最终修订文本已经复读。321 个范围的受保护标记及 linkend/endterm/zone/arearefs 与本版英文严格相符，不需要差异豁免；全部现有 ID 和定位属性保留。

工具候选中的 inherits/parent 曾因中文语序调整而发生顺序误配，已根据完整父句及“继承／父表”实际标记重新绑定，原译文没有问题。PG14—16 DDL 多出的既有默认权限定制索引位于本批继承范围之外，未为消除计数差异而删除。匿名练习段落也是合法结构，已逐一绑定其完整英中内容。

固定英文疑点单列保留：数据库名首字母限制未区分引号形式；初始化用户与服务器操作系统用户关系作了简化；自连接说明和示例的包含方向有疑问；PG10 FILTER 示例 count=5 与所给数据不符；PG19/20 对失败事务允许命令的概括与后文 ROLLBACK TO 恢复说明需结合理解。这些均没有擅自改写固定英文或用新版本事实替换旧版代码。

新快照 checkpoint-tutorial-ready 实际完成十一版准备、解析和对齐检查，5,493 个节点精确绑定，范围内 4 条匿名配对提示全部核准，零未决、零漂移、零子节点数量差异。源码差异检查通过。原始全书审计及其非零退出码完整保留，本报告只关闭上述已读范围。

上一阶段数据修改章及四类命令已提交 cfedc04。下一批继续十一版 SQL 语法章，已建立 34 个 PG18 完整阅读块和 10 个英文全文变体清单。全书逐句语义校准、历史独立对账及十一版 HTML/A4 PDF/US PDF 共 33 项最终构建仍未完成，最终构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-reread-proof.json)、[代码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-raw-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-protected-proof.json)、[索引横向核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-index-horizontal-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tutorial-full-reviewed-certificate.json)。
