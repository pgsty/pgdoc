PG10—PG20 维护与权限参考页校准记录（2026-09-15）

完成十一版 ANALYZE、CLUSTER、LOCK、CREATE POLICY、ALTER DEFAULT PRIVILEGES 共 55 个参考页的全文对照。从 PG18 开始，35 个英文全文变体及全部中文候选已读完；关联核对表采样、术语表、配置、VACUUM 和 vacuumdb 共 31 个文件中的 36 个完整范围。合计 91 个范围，含 1398 个叶段落和 184 个代码／语法块。本批修改 46 个正文文件和 3 份规范文件，41 组新文字已复读。

- ANALYZE：PG14—17 恢复各版语法、表选择、继承与分区分析行为，移除未来 ONLY 和递归说明；PG14—16 恢复旧式语法说明位置和读锁段，移除未来临时 search_path；PG14/15 移除未来 size 参数；PG15/16 恢复所有者／超级用户要求。PG14—17 VERBOSE 不再提前宣称 INFO 级别；PG14—20 的高频值说明按词表统一。
- CLUSTER：PG14—16 恢复本版语法、兼容语法、所有者／超级用户处理范围，移除未来 MAINTAIN 和临时 search_path；PG14 移除本版未有的分区段，PG15 移除后加的事务块限制句。PG14—17 VERBOSE 恢复本版说明。PG19/20 已改为通过 REPACK 说明聚簇，保留其自身精简结构。
- 默认权限：PG14—16 去掉提前出现的 MAINTAIN，PG14—17 去掉提前出现的 LARGE OBJECTS 语法。PG10—15 恢复全局与按模式设置的本版段落；PG14/15 恢复引言结构及 target_role 的 SET ROLE 说明。新版本的实际能力、角色继承说明和示例保持。
- 行安全性策略：PG14 移除未来 security_invoker 例外；十一版补译策略组合伪代码中的八条说明，保留关键字、逻辑运算和括号。明确 ON CONFLICT 检查各适用 UPDATE 策略；PG15—20 明示 MERGE 相对独立 UPDATE 的报错差异；PG14—20 的检查／筛选图例与中文表格一致。
- 缓冲区访问策略：沿用已有中文并新增词表及语境规则 639。十一版表采样说明已核对，PG16—20 ANALYZE／VACUUM 的 literal 内普通概念补译；术语表沿用既定 WAL 刷盘用词，配置相同段落统一。保留 PG16 的 256 kB 与 PG17 起的 2MB 默认值、首次英文括注、实际 BufferAccessStrategy 类型及参数代码。
- LOCK：十一版全文、权限变体和示例核准，无需正文改动。其他同源段落按自身英文复用审定译文，真实链接与版本差异保留。

[逐问题十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-matrix.md)共 23 组、253 格：111 格本批修订、127 格原本正确、15 格不适用；格数并非独立缺陷数。每格绑定[完整上下文、行号与源码哈希](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-issue-version-matrix.json)。204 个叶段落英文组及 17 个含示例父段组无未处理的同源中文冲突。

全树横向核查已确认，PG10—16 无提前出现的 MAINTAIN，PG10—14 无提前出现的 security_invoker。新增规则的概念检查覆盖全部十一版；实际代码类型已对照固定 PG20 源码。只移除了 PG14/15 未来 size 条目上的两个本地 ID，逐版确认对应英文无此项，整个中文目录无指向它们的链接。

新快照 checkpoint-maintenance-permissions-ready 完成十一版实际准备、解析与对齐检查。4,987 个节点精确绑定，182 条范围内提示逐项核准，零未决、零漂移、零子节点计数差异。252 项普通说明标记／既有等价包装差异已逐项解释；其余代码与受保护内容匹配自身英文。修订范围差异检查通过。删除 PG15 分区句后产生的一行空白在应用前已修正，原候选证据保留。

本报告关闭本批五类完整参考页及明确列出的关联范围。VACUUM、客户端维护工具、GRANT／REVOKE 与所有权参考页的其他正文继续全文审查；全书语义校准、历史证据独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-changes.json)、[终稿复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-reread-proof.json)、[原始代码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-raw-reread-proof.json)、[受保护标记解释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-protected-dispositions.json)、[规则前后文本](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-norm-changes.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/maintenance-permissions-reviewed-certificate.json)。
