PG10—PG20 规则系统全文校准记录（2026-09-15）

十一版 rules.sgml 全章已完成中英文核对：从 PG18 开始，读取 24 个本版英文节变体、全部中文候选和两种章框架，覆盖 1,309 个叶段落、55 个外层段落以及 946 个代码／计划块。32 组新正文和五组说明性代码分别复读。此前物化视图专项的正文也纳入本批一致性核对；保留每版自己的 SQL 和计划输出。

修复的版本问题包括：

- PG14 恢复本版视图实现引言。PG10—15 的等价建表说明与 PG16 起的无实际存储说明各自保留。
- PG14—16 清除视图更新说明中提前出现的 MERGE；该章 PG17 起的内容逐版保留。
- PG14—17 移除后加的 PG18 RETURNING OLD／NEW 解释段，以及安全屏障视图索引扫描／\dAo+ 说明段。这里只校准段落所属版本，不把段落增加时间当作所有相关功能的引入时间。
- 十版补译 view／updating 可见索引，PG15 原本正确；十一版翻译说明性 SQL 注释和列列表占位文字，保留 mytab 等真实标识符。
- 十一版校准两处 null 说明、plan 名词、范围表重名的对比、NEW／OLD 在 SELECT 介绍中的讨论范围，以及命令状态中“最后一条满足条件的查询”。按版本保留 previous section 单复数；统一默认值和防泄漏性用词。

九组共用散文候选及两组外层框架已逐一取舍，统一视图展开、权限、销售汇总、拼写查询及规则／触发器示例的同义文字。147 个共用散文组不存在未处理的中文冲突；不同版本的代码内容、标记和引用分别保留。这里的组数不是独立缺陷数量。

[十五组问题／一致性检查的十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-matrix.md)共 165 格：123 格修订、42 格核准；每格绑定[完整本版上下文、行号和源码哈希](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-issue-version-matrix.json)。严重程度、技术事实和措辞校准没有混为一个缺陷总数。

新快照 checkpoint-rules-full-ready 完成十一版实际解析和对齐检查：3,718 个节点精确绑定，79 条规则章提示全部逐项核准，零未决、零漂移、零子节点计数差异。46 个受保护标记差异逐个绑定，包括可翻译占位文字、已有索引命令标记和为明确指代重复的命令名；没有批量豁免。真实代码及输出在仅还原已审定说明性文字后与各自英文一致。PG10 使用原生 SGML 检查链，原始全书检查退出码和未关闭的其他章节提示保留。

固定英文中的历史 OID 状态、shoelace_arrive.sl_name 列引用及带 ORDER BY 的未排序展示均有[源文疑点记录](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-source-questions.json)。本批未更改这些演示输出，也不以原样相同声称运行时正确。

本阶段范围为十一版规则系统全章。关联 CREATE VIEW／CREATE RULE 参考页正在完整核对，已发现其自身的版本说明差异；它们尚未计入本批通过范围。全书逐句覆盖、历史范围独立对账、十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-changes.json)、[新稿复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-reread-proof.json)、[标记差异判断](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-protected-dispositions.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/rules-full-reviewed-certificate.json)。
