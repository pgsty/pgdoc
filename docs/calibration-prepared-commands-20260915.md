PG10—PG20 预备语句参考页校准记录（2026-09-15）

已完成 PREPARE、EXECUTE、DEALLOCATE 十一版 33 个参考文件的全文核对。PG18 的三个完整参考页先读，其余十版按全部英文变体及全部中文候选对照，合计 11 个英文全文变体。另核对 EXPLAIN 的十一版关联索引；全部 44 个 prepared statements 可见索引位置均已覆盖。合计 44 个精确范围、339 个叶段落、31 个含示例父段落与 64 个原始块，本批修改 33 个正文文件，没有新增或变更翻译规范。

- 补译预备语句索引中的创建、执行和释放，使用现有词表的“预备语句”。EXPLAIN 的“显示查询计划”索引此前已正确。
- 十一版将 potentially 的“往往”改为“可能”，保留性能优势的可能性限定。
- PG10/11 的旧版计划选择说明沿用“非重复值”和“代价”术语，保留五次或更多次、包含规划开销、33% 以及计划选择规则。PG12 起该段已改写，按各版本保留不同正文。
- PG10—13 的 INSERT 示例引言、PG12/13 的 SELECT 示例引言与相同英文统一；原样 SQL 和参数不变。

逐版核准的事实包括：参数类型推断、会话生命周期、EXECUTE 参数兼容与不按参数重载、DEALLOCATE 的可选 PREPARE 关键字、通用／自定义计划选择规则、DDL／统计信息／search_path 变更后的处理。PG14 的 MERGE 串入已在 d63c4c7 修复，本批记为已正确；PG15 起的 MERGE 语句、PG12 起的 plan_cache_mode，以及 PG14 起英文明确写入的统计信息更新说明各自保留。交叉引用的下划线／连字符、PG10 属性和短结束标记采用本版有效形式。

[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-matrix.md)共 11 个问题及一致性／回归组、121 格：30 格本批修订、73 格此前正确、18 格不适用。组数和格数不是独立缺陷数。每格都有[自身完整英中范围及源码哈希](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-issue-version-matrix.json)。44 个叶段落英文组、5 个含示例父段落组及 14 个索引／标题组没有未处理的同源中文冲突；10 组最终修订文本均已复读。

新快照 checkpoint-prepared-commands-ready 完成十一版实际准备、解析与对齐检查。1,565 个节点精确绑定，26 条范围内提示全部核准，零未决、零漂移、零子节点计数差异。全部既有 ID 和代码保留，修订范围差异检查通过。本报告关闭三个完整参考页及明确的关联索引；SELECT 完整参考页的审校继续。全书语义校准、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-raw-proof.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/prepared-commands-reviewed-certificate.json)。
