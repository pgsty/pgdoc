PG10—PG20 bloom 与物化视图校准记录（2026-09-15）

本阶段完成十一版 bloom 扩展全文，以及 rules.sgml 中物化视图完整节的中英文核对。PG18 优先，随后读取其余各版自己的全部差异和中文候选：6 个 bloom 全文变体、5 个物化视图节变体，覆盖 286 个叶段落、220 个代码块和全部外层文字。共修改 14 个文件，12 个最终稿组已复读。

发现并修复的问题：

- PG14—16 bloom 的四个计划示例混入未来 BUFFERS、Index Searches 和小数形式实际行数。按各自原文恢复字段和显示行数，保留本版示例中的代价、时间及大小数据；PG10—13、17—20 原本准确的样例逐版核准后保留。
- PG14—16 物化视图节的四个计划示例同样混入未来 Index Searches 和小数形式实际行数，已恢复本版输出。这两项共恢复 24 个代码块，覆盖最初关联扫描中发现的全部六个文件。
- 十一版销售汇总说明补回 may not care 的可能性，改为“可能不关心当天尚不完整的数据”，避免把示例中的可能需求写成确定事实或“不必关心”。
- PG10—13 将 might be useful 对应的“可以用于”校准为“可能适合”，PG14—20 已有可能性限定，核对后保留。

[四项问题的十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-matrix.md)共 44 格：21 格修订、23 格核准保留；每格都有[本版完整范围及源文摘要](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-issue-version-matrix.json)。同一问题涉及多处代码块，格数和代码块数量不作为独立缺陷数。

PG10—12 固定英文的建表示例为 10,000,000 行，但旧查询示例输出为 100,000 行；PG10 还重复显示了一次 EXPLAIN 命令。这两类源文疑点已记录并保留，未用新版本数字回填。PG19、20 的 AS 大小写、PG10 的 SGML 简写也各自保留。

修订后的新快照证明：当前中文、审定稿与快照逐字一致，固定英文与新解包英文一致。935 个节点精确配对，16 条范围内提示全部核准，零未决、零漂移、零子节点计数缺口；有效 ID 保留。14 个源文件差异检查及受保护标记、代码核对通过。前批关联扫描的 40 个版本／文件／词项重新核查，原来的六处存在性差异全部消除；这项扫描不替代未读文件的语义验收。

仅 checkpoint-bloom-materializedviews-ready 用于本阶段验收。rules 其他部分的 93 条范围外提示保留，物化视图节通过不等于 rules 全章通过。查询树、命令状态、规则／触发器对比的后续阅读已进行，相关措辞待完成本章校准后统一核验；视图重写、更新规则、权限等范围继续。全书对账和十一版 HTML / A4 PDF / US PDF 共 33 项最终构建仍未完成。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-file-plans.json)、[完整范围绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-scope-proof.json)、[逐项修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-changes.json)、[新稿复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-reread-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-native-classification.json)、[核验证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bloom-materializedviews-reviewed-certificate.json)。
