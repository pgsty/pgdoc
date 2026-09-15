PG10—PG20 后台工作进程全文校准记录（2026-09-15）

十一版 bgworker.sgml 已完整中英对照。从 PG18 两个完整标志条目和完整章节外层框架起读，阅读全部 7 组英文全文变体和所有中文候选。全文关联检索得到 87 个命中，全部位于已读章节内。修改 6 个正文文件。

- PG15/16 的 BackgroundWorker 结构体混入未来库名长度 MAXPGPATH，恢复同版 BGW_MAXLEN；同时删除本版尚无的 BGWORKER_BYPASS_ROLELOGINCHECK 说明。PG17—20 自身已有这两项，保留；PG10—14 原本正确。
- PG10—13 两段同源外层说明复用其他版已审定译文。子结构和代码仍使用各自版本，保留 PG10 无 bgw_type、PG10 连接函数无 flags、PG16 起 pid_t 字段等差异；此项为措辞一致性。
- 全文核准注册与启动、共享内存、动态库入口、Datum 传参、连接身份及 NULL 行为、信号、退出和重启、状态查询、等待与异步通知。PG15 起共享内存标志必需，PG16 起导出入口说明、PG19/20 可中断工作进程及长循环中断检查，分别按本版保留。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-matrix.md)共 15 个问题与检查组、165 格：8 修复、147 本项已正确、10 不适用。组数包括版本边界和一致性检查，不等于独立缺陷数。

273 个叶段落、24 个嵌套父段落和 11 个原始结构体代码块完整核准；9 组最终修订文本已复读。46 个同源叶段组、3 个父段组和 9 个其他单元组无未决冲突。十一版的受保护标记及链接核准；英文 PostgreSQL's 的所有格译为中文“的”，部分版本原有首句 productname 包装，均按完整未改动段落记录具体例外。代码与标识符使用本版源文，未新增术语规则。

新快照 checkpoint-bgworker-ready 完成十一版准备、解析及对齐：482 个节点精确绑定，范围内 14 条提示逐项核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，此结论只覆盖本章。

前一阶段自定义扫描和表采样提交 282532d 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账以及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-version-boundary-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-matrix.json)、[关联检索](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-related-search.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/bgworker-full-reviewed-certificate.json)。
