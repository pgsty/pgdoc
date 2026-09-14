PG10—PG20 视图管理参考页全文校准记录（2026-09-15）

完成十一版八类参考页全文核对：ALTER／DROP VIEW、ALTER／DROP RULE，以及 CREATE／ALTER／DROP／REFRESH MATERIALIZED VIEW。88 个文件中有 64 个修订。从 PG18 开始，31 个英文全文变体及全部中文候选均已读过，包括 881 个叶段落、11 个外层段落和 187 个代码／语法块。11 组新译文、说明性注释和语法引导文字已复读。

主要修复如下：

- PG14 ALTER VIEW 移除未来的 security_invoker 选项；其余版本按各自英文核准。
- PG14 ALTER MATERIALIZED VIEW 移除提前出现的 SET ACCESS METHOD；PG14/15 移除 SET STORAGE 中的 DEFAULT。分别保留 PG15 起与 PG16 起的本版语法。
- PG14—16 CREATE／REFRESH MATERIALIZED VIEW 移除后加的临时 search_path 说明；REFRESH 恢复本版所有者要求，PG17 起保留 MAINTAIN 权限说明。
- PG10—14 CREATE MATERIALIZED VIEW 恢复本版名称参数说明，避免加入后版的完整重名关系类型清单。
- 十一版把 SQL notice 译为提示，并保留 IF NOT EXISTS 不保证现有对象相似的限制；PG10—13 补译普通的 security-barrier 属性说明。
- 十一版翻译 ALTER VIEW 示例中两条说明性注释，保留 NULL 和实际 SQL。统一 DROP 的默认行为、普通视图用词及两组共用段落；四个旧版本统一语法引导文字，保留本版参数标记。

[十一组问题／一致性矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-matrix.md)共 121 格：55 格修订、66 格原本正确；逐格绑定[本版完整上下文、行号和源码哈希](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-issue-version-matrix.json)。这里的格数不等于独立缺陷数量。94 个共用段落组无未处理的中文冲突，受保护标记比较零差异。唯一移除的 PG14 选项锚点属于未来条目，已核实本版全目录无指向它的链接。

新快照 checkpoint-view-management-ready 完成十一版实际解析与对齐检查：4,505 个节点绑定，236 条范围内提示全部核准，零未决、零漂移、零子节点计数差异。SQL 与语法在仅还原明确审定的说明性翻译后，逐版匹配自身英文。最初差异预检发现删除选项后遗留的一行空白字符；修正后才应用源码并创建本次快照，未将失败预检计为验收。

横向关联搜索确认了待继续修复的范围：PG14—16 ALTER DEFAULT PRIVILEGES 的 MAINTAIN 语法、CLUSTER 的 MAINTAIN 段落，PG15/16 ANALYZE 的权限说明，以及 PG14 CREATE POLICY 的 security_invoker。已建立这四类及 LOCK 的十一版全文阅读清单，当前继续处理。**本报告只关闭上述八类视图管理参考页的本批范围，关联权限问题和全书尚未完成。**

全书语义通读、历史范围独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-changes.json)、[新稿复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-reread-proof.json)、[代码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-raw-reread-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-protected-signals.json)、[锚点依据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-removed-id-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/view-management-reviewed-certificate.json)。
