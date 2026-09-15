PG10—PG20 查询章校准记录（2026-09-15）

已完成十一版 queries.sgml 整章英中核对：先读 PG18 的 28 个完整子节或父级文本范围，再读全部 10 个完整英文变体及每种中文候选。另核对十一版教程关系模型段、22 个 SELECT LATERAL 关联段、十一版 tablefunc 层次查询段，以及 PG19 完整属性图定义节。共 45 个文件、56 个范围，1,716 个叶段落、691 个含列表或示例父段落、1,216 个代码／语法块。本批修改 23 个正文文件及 3 个规范文件。

- 十一版修正 ON 的通用性误成出现频率，补齐 JOIN USING 的列出顺序、右连接与左连接的对应关系，以及 JOIN 别名隐藏内部原名的说明。
- 十一版修正 LATERAL 引用方向和位于 JOIN 右侧的前提。关联 SELECT 说明逐版复核，已有正确内容保留。修正无 OUT 参数的条件应限定函数，以及 ROWS FROM 并列输出各函数结果列的含义。
- 十一版补齐 GROUPING SETS 允许零个表达式，修正 ROLLUP 的层次数据误成历史数据，以及按部门、事业部和全公司汇总的层级。修正聚合示例是某种产品的销量，以及分组后非分组列没有单一值的说明。
- PG13—20 修正窗口函数输入行顺序保证；PG14—20 修正关键词用作列标签时的 AS 要求及未来关键词兼容建议。十一版修正集合操作无括号时的两种结果、LIMIT／OFFSET 的具体值影响计划、VALUES 用途的频率关系和递归查询以迭代方式求值。
- PG15/16 的 WITH 辅助语句不能使用 MERGE，主语句可以使用 MERGE；两处说明均恢复本版边界。PG14—16 恢复自身 NATURAL JOIN 的等价写法和 LIMIT／OFFSET 摘要参数。分别保留 PG10/11、PG12/13 与 PG14 起的 CTE 求值和限制条件下推说明。
- 十一版修正 WITH RETURNING 结果供同一查询其余部分引用，以及返回给客户端的受影响行数。补译教程可见索引和普通 SQL 注释；所有实际代码、标识符和各版示例输出保持自身英文。
- PG19 属性图节恢复本版章节顺序，补齐连接 employees 的边这一明确主语，翻译可见索引与脚注概念，并恢复查询章两处 quote 标记。其他版本按自身内容核验，不引入此节。

新增第 641 条术语 derived table → 派生表，沿用查询章稳定译法，消除生成表／推导表混用。十一版固定英文全树扫描用于定位对应位置，实际修订均有完整英中语境；普通生成动作、基本表和 derived data 不作机械替换。词表及规则各 641 条，既定九项用户回退保留。

[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-matrix.md)共 35 个问题、术语、一致性与回归组、385 格：275 格修订、53 格原已正确、42 格不适用、15 格保留固定英文疑点。组数不是独立缺陷数。每格绑定完整英中上下文与哈希；216 个同源叶段落组、94 个父段落组、96 个其他文本组无未处理的中文冲突。92 组最终修订文本均已复读；43 项受保护词差异逐项核准，涵盖内联 SQL 空白、明确代词先行词及既有产品名称标签，未以计数替代语义。

保留的固定英文疑点包括 GROUP BY DISTINCT 的 NULL 措辞、CYCLE 示例 depth 初值差异，以及 PG19 图定义中将顶点称为边和图模式示例括号缺失。均保留本版事实及代码，未擅自改写上游。PG19 属性图关联段的初始整文件序号绑定在人工通读时被发现错配，已撤销并改为自身锚点下完整章节绑定；错误中间产物单独归档。

新快照 checkpoint-queries-ready 已实际执行十一版准备、解析与对齐核验：6,002 个节点精确绑定，49 条范围内提示全部核准，零未决、零漂移、零子节点计数差异。PG19 的两处 quote 修复后已另取新快照复核，前一轮记录保留。原生检查对全书仍有范围外提示，原始退出码与日志完整保留，未宣称全书检查零告警。源码差异检查通过。

本报告关闭完整查询章及明确的关联范围。下一批继续数据修改章和 INSERT／UPDATE／DELETE／MERGE 参考页。全书逐句语义校准、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-raw-proof.json)、[受保护词](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-protected-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/queries-full-reviewed-certificate.json)。
