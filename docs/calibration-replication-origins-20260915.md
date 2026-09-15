PG10—PG20 复制进度跟踪与测试解码全文校准记录（2026-09-15）

从 PG18 的 replication-origins.sgml 与 test-decoding.sgml 两个全文块开始，对照全部六组英文全文变体及全部中文候选，完成十一版 22 个完整文件。没有发现新增正文缺陷，没有改动正文或规范。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-matrix.md)覆盖 10 组检查、110 格：106 本项已正确、4 个旧版不适用的新增示例。已核准安全进度跟踪、名称与本地标识符、会话和事务级函数、崩溃持久化、复制环路和来源过滤，以及测试插件定位与全部示例。

四个版本差异完整保留：PG10—14 源文称 OID，PG15 起称 ID；PG14 起本版具有进行中事务的 stream-changes 示例；PG16 起模块有解释性长标题；PG19 起示例 LSN 低位段补前导零且分隔线加宽。名称用于跨系统引用，而本地 ID 不应跨系统共享的限定完整，没有从文档改写推定实际接口引入日期。

117 叶段落、29 嵌套父段落、18 原始代码／输出块绑定本版英文；14 同源叶段组、3 父段组、6 其他单元组没有译文冲突。受保护元素及链接与对应英文精确匹配。

复用刚完成的 checkpoint-wal-extensions-ready，已逐文件确认当前中文＝本次全文读稿＝快照，固定英文＝本次解包英文，289 个原生节点精确绑定，范围内零提示、零未决、零漂移。复用的是内容完全相同的解析证据，没有声称重新运行整套准备。WAL 扩展与归档模块阶段提交 9f9367b 已核验；本批仅提交两份报告。

全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-scope-proof.json)、[全部变体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-whole-variants.json)、[阅读进度](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-human-progress.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-version-boundary-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-matrix.json)、[快照绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-native-validation.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/replication-origins-full-reviewed-certificate.json)。
