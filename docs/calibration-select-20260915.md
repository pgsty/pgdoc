PG10—PG20 SELECT 参考页校准记录（2026-09-15）

已完成十一版 SELECT 参考文件的全文英中核对。PG18 的 34 个完整子节或父级文本范围先读，其余十版按 10 个完整英文变体及全部中文候选逐项核对。另读 queries.sgml 的十一版 WITH 索引，以及 syntax.sgml 的 PG11—20 窗口帧排除段。共 32 个文件、32 个精确范围，1,782 个叶段落、367 个含列表或示例父段落、410 个原始块；本批修改 11 个 SELECT 正文文件，没有修改规范，词表仍为 640 条。

- 十一版修正递归 SELECT 结果用于“数据修改语句”的说明，明确 WITH 同行修改的结果并无规定，修正 ORDINALITY 与列定义列表的组合位置和 LATERAL 的 JOIN 左右引用范围。
- 十一版修正函数依赖的集合关系：分组列或其子集构成主键。原译误写成分组列可以是主键的子集。聚合函数及 CASE 求值说明沿用既定术语。
- PG11—20 补全窗口帧排除同时考虑开始与结束选项的说明，复用 syntax.sgml 已正确的同源译文。RANGE 明确偏移量表示与当前值的差距；PG13 原有差距含义正确，本批同步数值术语。PG10 保留仅 ROWS 允许偏移量等自身限制。
- 十一版修正输出列名误写为行名、函数名／类型名与自动生成名称的选择关系、NULL 排序默认条件、查询快照时的锁定条件，以及预计并发更新时的排序建议。PG11—20 修正“为 Oracle 编写”误成“Oracle 编写”；PG10 原本正确。
- PG14—16 清除 WITH 语法摘要中的未来 MERGE，恢复本版锁定摘要参数 table_name 和对应说明。PG14/15 恢复 FROM 子查询必须提供别名的语法、正文与兼容性；PG16 起保留允许省略别名。
- 补译 TABLE 和 WITH 可见索引，澄清零列的表，并统一相同英文的段落、父级引言与标题。PG19 的 GRAPH_TABLE 完整条目按自身英文顺序排列；其他版本不引入此条目。

[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-matrix.md)共 30 个问题、一致性与回归组、330 格：216 格本批修订、90 格此前正确、14 格不适用、10 格保留固定英文疑点。组数不是独立缺陷数。每格绑定完整英中上下文和源码哈希。223 个同源叶段落组、48 个父段落组、38 个索引／标题／摘要组没有未处理的中文冲突；66 组最终修订文本均已复读。全部既有 ID 与链接保留；44 处受保护词计数差异分别核准为“分组集”的普通术语翻译或代词先行词的明确重述。

保留并核准的版本差异包括 PG11 起 GROUPS、PG12 起 MATERIALIZED、PG13 起 WITH TIES 和更详细的 ORDINALITY 返回类型、PG14 起 GROUP BY DISTINCT／SEARCH／CYCLE、PG17 起 WITH 中的 MERGE，以及 PG19/20 的 GROUP BY 表达式限制文字。初始的 common data type、non-null、clustering effects 和 volatile functions 措辞疑点在语境中可成立，未强改既有译法。xreflabel 属性按现行规范保留；DISTINCT ON 的“每组第一行”既有说明已由完整本版子节确认。PG11 起英文 JOIN 记法便利及 CROSS JOIN 条件说明中的疑点如实记录，未擅自改写上游事实。

新快照 checkpoint-select-ready 已完成十一版实际准备、解析与对齐检查：3,862 个节点精确绑定，112 条范围内提示全部核准，零未决、零漂移、零子节点计数差异。差异检查通过。本报告关闭完整 SELECT 参考页及明确的关联范围；queries.sgml 整章阅读继续。全书逐句语义校准、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-reread-proof.json)、[受保护词](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-protected-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-raw-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/select-full-reviewed-certificate.json)。
