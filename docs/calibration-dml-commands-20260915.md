PG10—PG20 数据修改章和四类命令校准记录（2026-09-15）

已完成十一版 dml.sgml 及 INSERT、UPDATE、DELETE 参考页、PG15—20 MERGE 参考页，共 50 个完整文件的英中核对。先读 PG18 的 36 个完整范围，再读全部 34 个完整英文变体及对应中文候选；另读 106 个关联范围，涵盖十一版行类型、相关发布说明、规则触发器、逻辑复制、MVCC 及 MERGE 支持函数。共 118 个文件、156 个范围，2,198 个叶段落、581 个含子级内容父段落、701 个代码／语法块。本批修订 55 个正文文件和 3 个规范文件。

- PG14—17 的 INSERT、UPDATE、DELETE 移除误入的 PG18 OLD/NEW 别名参数、返回表达式说明及相关示例。PG10—17 的 UPDATE 说明恢复本版只返回更新后值的含义及示例，清除“可以请求旧值”的未来行为。PG18—20 保留自身完整新旧值语法及显式标记。
- PG15/16 的 MERGE 恢复本版两种匹配状态，移除未来的 RETURNING、BY SOURCE/BY TARGET、视图目标和相应触发器处理。同步核对摘要、参数、执行步骤、条件引用范围、可达性、兼容性和示例，补回“MERGE 没有 RETURNING，内部动作不能包含 RETURNING 或 WITH”的原文说明。
- PG17 MERGE 保留本版 RETURNING 支持，恢复按具体动作返回新值或旧值的行为和库存示例，移除 PG18 新旧值别名内容。PG15—17 补回完整 MATCHED 等价查询示例。PG17 起的 MERGE 支持函数、MVCC 和 PG17 发布说明逐段复核，原已正确的内容保留。
- PG14—16 UPDATE／DELETE 删除本版英文尚未收录的分批示例。这是文档归属错误，不表示这些版本不能执行示例中的 SQL。PG14 同时恢复自身 salesmen／sales_id 联系人示例，移除本版没有的祖先外键限制说明。
- PG11—20 修正分区移动的条件：是行必须满足目标分区的分区约束。PG17—20 修正 ORDER BY 确定优先更新哪些行的说明。十一版修正 ON CONFLICT 权限方向：读取 excluded 列需要目标表对应列的 SELECT 权限，并补回仲裁约束的 emphasis 标记。
- 十一版 INSERT 与 PG15—20 MERGE 的 composite column 统一为“复合列”；rowtypes 中原有正确译法保留。PG11—15 发布说明修正行外 TOAST 存储，PG17 发布说明统一复合列术语，PG18 发布说明纠正四类命令的 RETURNING 列表被误写成 MERGE 列表的问题。
- PG10—13 补回按完整行插入的概念限定，移除本版 RETURNING 说明中的未来“默认”限定；PG17—20 修正“通常更有用”被扩写成“更常见也更有用”。补译普通 SQL 注释及 MERGE 语法摘要引导语，所有实际代码、标识符和示例输出仍按对应版本英文保留。

新增第 642 条 composite column → 复合列，沿用行类型章稳定术语。词表及规则各 642 条，既定九项用户回退保留。修订只在明确语境中应用，不影响复合键、多列组合和真实标识符。

[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-matrix.md)共 37 个问题、术语、一致性和回归组、407 格：144 格修订、93 格原已正确、150 格不适用、20 格固定英文疑点保留。组数不是独立缺陷数。每格绑定本版完整英中语境或全文版本边界证明。365 个同源叶段落组、87 个父段落组、55 个其他文本组无未处理冲突；99 组最终修订文本均已复读。68 项受保护词处置覆盖 88 个计数差异，逐项区分空白、译出的术语链接标签、既有标签和明确的代词先行词；所有 linkend/endterm 目标与本版英文一致。

22 个随非本版内容移除的 ID 已逐一证明：它们属于被删除的未来参数或新文档示例，本版英文无相应内容，十一版对应中文树内没有残留入链。没有把合法中文定制 ID 普遍当作错误处理。PG14 未被包含的 MERGE 孤立文件按既有边界保留。

固定英文疑点单独记录：MERGE 散文 customer_accounts 与代码 customer_account 的单复数不一致；MERGE 与 INSERT 对 OVERRIDING USER VALUE 的标识列条件不同；库存说明只提零值而示例使用 > 0；PG19/20 时态残留段的提交时点表述。均保留各版原文与代码。规则触发器和逻辑复制中正常的新旧行用法没有被误当成 PG18 RETURNING 功能。

新快照 checkpoint-dml-commands-ready 实际完成十一版准备、解析和对齐检查，6,574 个节点精确绑定，范围内 439 条提示全部核准，零未决、零漂移、零子节点计数差异。原生检查仍保留全书范围外的原始提示和退出码，本报告只关闭上述完整文件及关联范围。源码及规范差异检查通过；删除段落产生的空行尾随空格已按差异逐行清理，其他既有格式保留。

查询章上一阶段已提交 8c2e293。下一批继续入门、SQL 语言及高级特性教程。全书逐句语义校准、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-reread-proof.json)、[原始代码块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-raw-proof.json)、[受保护词](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-protected-proof.json)、[移除 ID 核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-removed-id-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dml-commands-full-reviewed-certificate.json)。
