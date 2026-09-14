PG10—PG20 CREATE VIEW／CREATE RULE 全文校准记录（2026-09-15）

十一版的两类参考页已完成本批中英文核对，共 22 个完整文件，其中 16 个修订。从 PG18 开始，完整阅读 28 个英文节变体、全部中文候选和 3 个外层框架；覆盖 652 个叶段落、33 个外层段落和 143 个代码／语法块。新译文 22 组和两组外层说明已复读。

修复与核准的重点如下：

- PG14—16 的 CREATE VIEW 移除提前出现的 MERGE 说明，PG17 起按自身英文保留。
- PG14 移除 security_invoker 选项及后加的权限说明，恢复本版表／函数权限、CREATE OR REPLACE VIEW 可修改属性以及 check_option 的 ALTER VIEW 说明。
- PG11—15 的 CREATE RULE 补回“将这种规则附加到表上会将该表转换为视图”。PG10 保留自身完整解释，PG16 起原文已移除此句。
- PG10—14 恢复本版视图关系名称列举和兼容性段落。这里校准的是该版英文段落，不能由新增解释段落推断所有相关功能的引入版本。
- PG11—20 翻译递归视图的可见索引 in views；PG10 无此索引。十一版将 UPDATE is allowed 的许可含义明确为“仍允许”，保留各自的 MERGE、ON CONFLICT 和 PG20 时态范围条件。
- 统一十组共用段落和两组外层说明，聚合函数含义完整；保留本版的 SQL、PG10 SGML 转义、链接形式和已有标记。85 个共用散文组无未处理的译文冲突。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-matrix.md)包含八组问题／一致性检查及一组源文疑点，共 99 格：55 格修订、31 格原本正确、6 格不适用、7 格保留明确例外。每格有[完整中英上下文、行号和哈希](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-issue-version-matrix.json)。这些格数不是独立缺陷数。

源文疑点单独处理：十一版第一个示例的英文散文写 film，同段 SQL 和后文均为 films。PG14 起的中文已使用正确的 films；本批保留并同步到 PG10—13，固定英文不改。25 处受保护标记差异逐项解释，另包括已有 SELECT 命令标记和 PG20 时态残留术语链接。移除的唯一 PG14 选项锚点属于不存在于本版英文的未来条目，已核实 PG14 全目录无指向它的链接；其他锚点原样保留。

新快照 checkpoint-view-rule-reference-ready 完成十一版实际解析和对齐检查：2,141 个节点绑定，132 条本范围提示全部核准，零未决、零漂移、零子节点计数差异。全书原始退出码和其他范围的提示仍保留；本批通过不代表全书通过。

关联 ALTER／DROP VIEW、ALTER／DROP RULE 及物化视图四类参考页继续逐版处理。全书语义通读、历史范围独立对账与十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-changes.json)、[新译文复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-reread-proof.json)、[标记判断](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-protected-dispositions.json)、[移除锚点依据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-removed-id-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-rule-reference-reviewed-certificate.json)。
