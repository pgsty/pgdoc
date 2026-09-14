PG10—PG20 EXPLAIN 与 auto_explain 全页校准记录（2026-09-15）

本阶段从 PG18 开始，完成十一版 EXPLAIN 参考页和 auto_explain 扩展页的全文中英核对。共读完 22 个 EXPLAIN 章节变体、8 个外围结构变体、7 个 auto_explain 全文变体及所有中文候选，覆盖 534 个叶段落和 157 个代码／语法块。修订 13 个正文文件，新稿 17 组逐项复读。

发现并修复的问题：

- PG14、15 删除本版没有的 GENERIC_PLAN 参数、语法条目及示例；PG16—20 保留。PG14—16 删除 SERIALIZE、MEMORY 参数及语法条目，PG17—20 保留。
- PG14 从说明和 statement 列表中删除未来的 MERGE；PG15—20 保留自己的 MERGE 支持。PG14—16 补回旧式无括号语法概要及其说明段，把误用新版位置的兼容性文字恢复为本版结构；PG17—20 保留新版位置。
- PG14—17 WAL 段删除本版未列出的缓冲区变满次数。PG18 保留该计数，PG19、20 另保留整页镜像字节数。
- PG14—17 的 PREPARE 示例恢复自己的计划数字、字段、参数值与显示行数：PG14、15 为旧版 6 行示例，PG16、17 为 7 行示例；PG18—20 的 10 行示例、Index Searches 与小数形式实际行数保留。样例直接依照本版原文核对，不重新运行当前服务器来替代历史输出。
- PG14 auto_explain 删除未来的 log_parameter_max_length，PG16—20 保留；PG14、15 的日志计划示例恢复本版整数形式的实际行数。
- 十一版 EXPLAIN 注意节中的普通 autovacuum 术语按现行术语表译为自动清理；PG10—13 聚合示例引导句删除重复的“查询”。TOAST“行外存储”用语技术含义正确，现行规范未禁止，本批保留。

[13 类问题及一致性项的十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-matrix.md)共有 143 格：40 格本批修订、75 格全文核准后保留、28 格本版无对应条款。[每格证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-issue-version-matrix.json)包含本版英文、修订前中文和最终中文的文件摘要。多个问题可能落在同一段落，格数不是独立缺陷数。

BUFFERS 在前一个 hash 阶段完成修复，本批全页重新核准。PG10—12 保留与 ANALYZE 同用的限制；PG13—17 为 false 默认值；PG18 为 ANALYZE 时自动包含；PG19、20 保留只报告规划阶段的相应条件。auto_explain.log_buffers 的独立开关条件与本版英文一致。PG19、20 的 IO、auto_explain.log_io 和 log_extension_options 也已核准，未回填旧版。

当前中文、审定稿和修订后的新快照逐字相同，固定英文与新解包英文一致。2,205 个节点精确配对，98 条范围内结构提示全部逐项核定，零未决、零漂移、零子节点计数缺口。未来选项携带的 8 个中文自动 ID 随无效内容删除：对应选项不在本版英文中，所属版本所有 SGML 也没有对这些 ID 的引用；其余有效 ID 保留。受保护标记、代码、语法和 13 个修改文件的差异检查通过。PG14 原文示例中的行尾空格已清除，代码内容未变。

仅 checkpoint-explain-full-ready 用于本阶段验收。前置写入检查未完成时启动的旧 checkpoint-explain-full-reviewed 已停止并标记为不作验收，未计入通过记录。

关联词扫描的 40 个版本／文件／词项记录另发现 PG14—16 的 bloom、rules 示例共 6 个文件仍有未来 Index Searches 输出。这些提示没有被全页通过状态掩盖：bloom 全页及 rules 物化视图节已完成十一版阅读，示例恢复和“可能”限定修复进入下一批。rules 其余章节、全书余项及历史范围对账继续；最终十一版 HTML / A4 PDF / US PDF 共 33 项构建尚未完成。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-file-plans.json)、[修改记录](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-changes.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-native-validation.json)、[提示逐项分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-native-classification.json)、[未来 ID 核查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-removed-future-ids.json)、[核验证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-certificate.json)、[关联扫描](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/explain-full-reviewed-related-token-scan.json)。
