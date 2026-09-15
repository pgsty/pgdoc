PG10—PG20 页面映射扩展全文校准记录（2026-09-15）

从 PG18 的 pg_freespacemap 和 pg_visibility 两个完整文件开始，阅读全部 7 个分块、8 个英文全文变体和所有中文候选，随后完整核对 14 组关联段落及 3 组额外表格／词条。共 22 个完整文件和 66 个关联范围，涉及 61 文件、88 范围。

修复 PG10—14 的 pg_freespacemap 与 pgrowlocks 共 10 文件：固定英文的 members of the role 统一恢复为角色成员，保留各自 GRANT 和表级 SELECT 条件。PG15—20 原文为 roles with privileges，保留角色权限表述；pg_visibility 的旧版成员、新版权限及截断函数的超级用户例外均已正确。没有据文档改写时间推断底层权限机制的版本起点。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-matrix.md)包含 10 组、110 格：5 修复、83 本项正确、16 本版没有对应疑点、6 原文疑点格。2 组最终译文完整复读；271 叶段落、11 个完整示例输出块、88 个保护标记范围核准。42 个同源叶段组和 23 个其他单元组无未决冲突，4 组仅有既有 PG14 FSM 包装与换行差异，未因机械比对删除合法包装。

逐版核对两个空闲空间函数的重载签名、每页返回值、BLCKSZ 的 1/256 精度及不保证实时更新；索引跟踪完全未使用的页。PG10—12 原文使用 full，PG13 起使用 in-use，各自保留；8.4 接口历史注释仅保留至 PG13，storage-fsm 链接自 PG15 起存在，标题扩展说明自 PG16 起存在。

完整核对八个可见性函数的参数、返回集合与记录、VM 的 all-visible／all-frozen 两位和页头 PD_ALL_VISIBLE 的区别、崩溃恢复及并发读取导致的不一致、读取数据页的额外代价、非空检查结果所表明的损坏、截断后首次 VACUUM 全页扫描重建及重建前全零视图。所有函数签名、代码、示例数字和输出保持本版。

全部 356 处相关原文可见出现位置均精确绑定到已读范围，包括 pg_stat_scan_tables 的目录条目和监控角色说明。固定英文的两类疑点原样保留：PG13—17 发行说明称函数为 pg_freespacemap()，但同版模块完整定义为 pg_freespace；PG10 pgstattuple 权限段先称安装时仅超级用户，后又称默认允许角色成员。它们没有计作新增中文缺陷。

新快照 checkpoint-page-maps-ready 完成十一版准备与解析；877 个节点精确绑定，58 条范围内提示全部按已读节点核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，仅对列明范围给出通过结论。没有新增术语规则。

前一阶段物理存储提交 e062f4f 已核验，本批准备阶段提交。全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-version-boundary-proof.json)、[全部出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-all-occurrences-closure.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/page-maps-full-reviewed-certificate.json)。
