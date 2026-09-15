PG10—PG20 SQL 语法全文校准记录（2026-09-15）

十一版 syntax.sgml 全文已完成同版中英核对，以 PG18 的 34 个完整子节与外层框架为入口，再读取其余十版的全部英文差异和中文候选，共 10 个英文全文变体。关联搜索覆盖复合值、舍入、窗口帧、列表顶层、区域设置、布尔参数和索引语境；40 组关联段落、10 组补充检查及 3 组旧版检查均已完整阅读。最终绑定 122 个文件中的 357 个范围，其中 11 个为完整语法章，346 个为关联完整单元。本批修改 29 个正文文件，规范未变。

- PG14—16 聚合节恢复本版 array_agg 排序示例，以及 DISTINCT 的表达式必须匹配常规参数的限制和 PostgreSQL 扩展说明；移除错误回填的新版 JSON 聚合和 DISTINCT 示例。行构造器节恢复本版行比较、IS NULL 示例及原有两个交叉引用。PG17+ 保留自身新版段落和已移入比较函数节的示例。
- 十一版把 parameter-less aggregate 改为“无参数聚合”，并明确专用窗口函数的限制。PG11—20 补回窗口帧仅供作用于帧的窗口函数使用的限定，PG10 原译已正确。PG14—20 的 ROWS/GROUPS 偏移说明补上“或结束”，并恢复分区两端边界的含义；PG10—13 各自原有说明核对后保留语义。
- 十一版在行类型语境把“组合值”修为“复合值”；正文 expression/subscript 占位符恢复为与语法相同的名称。修正“SELECT 列表的顶层”被写成“顶层 SELECT 列表”的问题。rowtypes、PL/pgSQL、xfunc 和 SELECT 关联说明逐版检查；GIN 中的组合值泛指数组、文档等索引项，33 段按其语境保留。
- 十一版将聚合归属规则中的 exception 从“产生异常”改为规则“例外”，明确 null 输入指值为 null。类型转换函数命名的 By convention 恢复为“按照惯例”；COLLATE 说明明确结果受区域设置影响；min/avg 同时求值不再误称为并行执行计划。
- 十一版数组下标，以及 PG12—20 整数配置参数，改用不附加中点取舍规则的“舍入”。数学函数的 numeric 与浮点中点规则逐版核对，原译保留。PG10/11 配置仍保持本版只有浮点参数可含小数点的限制。PG15 对 interval 小数输入按整数月数舍入的发布说明同步校准。
- PG13—20 的 array_to_json/row_to_json 普通 boolean 参数说明改为“布尔参数”；PG10—12 的 pretty_bool 表行原已正确。补译 88 处相同上下文的可见索引及 SQL 示例普通注释，真实函数名、语法、数值、输出和错误消息保留。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-matrix.md)包含 30 个问题及检查组、330 格：176 格修复、113 格本项语义原已正确、19 格不适用、22 格保留固定英文疑点。每项均横向覆盖十一版；适用范围、完整源文和译文哈希可在矩阵 JSON 中追溯。

核对范围包括 2,241 个叶段落、43 个嵌套父段落及 1,195 个代码/语法/输出块。257 个同源叶段落组、90 个父段落组、199 个其他文本组没有未处理的语义分歧；6 组原有等价行内标记差异保留。64 组最终修订文本已复读，357 个范围的受保护元素（含操作符表 token）及全部本版链接属性均核准。15 个范围保留既有 off、:=、ROW 或 NULL 行内标记，不为消除计数差异而改动合法标记。

PG14—16 原译多出的 functions-comparison 链接随新版行构造器段落撤回；本版英文在该处只包含 functions-comparisons 和 functions-subquery，两者都已保留。现有 ID 与其他定位属性没有移除。

版本边界逐一核准：PG10—12 Unicode 的 UTF8/ASCII 限制；PG13 起的编码转换；PG10—13 后缀操作符；PG16 起的进制及下划线数值字面量；PG17 起 AT LOCAL 表行；PG19/20 的 null treatment 和旧字符串配置说明删除。固定英文的四反斜线描述、类型常量概括与数组限制的疑问单列保留，没有擅自修改代码或上游事实。

新快照 checkpoint-syntax-ready 完成十一版准备、解析和对齐检查。8,254 个节点与审定内容精确绑定，范围内 22 条提示全部逐项核准，零未决、零漂移、零子节点数量差异。当前源码、审定稿、新快照和解包固定英文一致，源码差异检查通过。原始全书审计及其非零退出码完整保留，本报告只关闭本批已读范围。

教程阶段已提交 5e0c235。接下来从 PG18 的 COPY 命令全文继续；全书逐句语义校准、历史独立对账和十一版 HTML/A4 PDF/US PDF 共 33 项最终构建仍未完成，最终构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-reread-proof.json)、[代码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-raw-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-protected-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/syntax-full-reviewed-certificate.json)。
