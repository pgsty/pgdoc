PG10—PG20 FDW 处理器全文校准记录（2026-09-15）

十一版 fdwhandler 及 CREATE／ALTER／DROP FOREIGN DATA WRAPPER 共 44 份正文已完整对照，另核对 203 个关联范围，共 111 个文件、247 个范围。以 PG18 的完整子块和外层框架为入口，逐一阅读 9 组处理器章全文变体、9 组命令页全文变体和全部中文候选；回调名、字段译法、实际 text 数组及包装器术语均进行十一版关联扫描。最终修改 68 个正文文件，现行 643 条术语规则、链接及既有定制锚点保持通过检查。

- PG12—20 RefetchForeignRow 的“仅当 SKIP LOCKED 时才能返回空槽”曾被反译，已恢复必要条件。PG10/11 使用 HeapTuple／NULL 的原有语义正确，保留本版接口。
- PG14—20 AcquireSampleRowsFunc 遗漏活行、死行总数是估计值，现复用 PG10—13 已正确表达的语义。INSERT／UPDATE 的成功返回条件在 PG12—20 校准为必须返回一个槽；DELETE 同类歧义覆盖十一版。
- PG14—20 批量插入遗漏“省去返回列”，以及 BeginForeignInsert 被误写成逐元组调用，已修正。PG11—20 COPY FROM 是不在 mtstate 中提供计划相关数据，不能理解为整个 mtstate 不存在。
- PG14/15 单行 ExecForeignInsert 的说明还漏了 COPY FROM 及与 INSERT 不同的调用方式；同版批量回调的英文只写分区路由，因此分别按本版修复。PG16 起批量说明提及 COPY，保留版本边界。
- PG14—16 混入 PG17 才有的连接条件存储说明，已移除。PG19 ImportForeignStatistics 段落误置于采样函数示例之前，已恢复本版顺序。
- 十一版 GetForeignJoinPaths 应是针对不同内外关系组合多次调用；约束处理、导入模式和并行计划中的可能性、建议强度均按英文校准。并行回调是全部可选，支持并行时需要其中大部分。
- 字段误译为域、异步回调的请求关系和返回约定、TRUNCATE 命令所请求的选项、实际 text 数组类型、XPath 局部别名的比较对象、旧版 regexp_matches 捕获子串及 JSON 任一键说明，均按关联范围逐版修复。PG16 发布说明唯一残留的“外部数据封装器”统一为“外部数据包装器”。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-matrix.md)共 37 个问题与检查组、407 格：252 修复、106 本项语义已正确、45 本版不适用、4 固定英文疑点格。组数包含功能边界和一致性检查，不等于独立缺陷数。

完整范围绑定 2,498 个叶段落、673 个嵌套父段落和 697 个原始块。326 个同源叶段组、77 个父段组、72 个其他单元组无未处置冲突；5 组等价标记或换行保留。155 个最终修订组经 45 组完整中英文本复读和 101 个已读全文原样配对复用核准。247 范围受保护标记与链接全部核准；PG19 原有 NIL 包装、PG14 原有 text[] 包装属于等义定制，均保留。

固定英文自身两类疑点单列保留：PG19/20 源码路径写作 src/backend/command/analyze.c，而固定源码实际目录为 commands；PG10/11 ALTER FOREIGN DATA WRAPPER 示例写 DROP 'bar'，固定语法对应 generic_option_name／ColLabel。发布包与文件哈希、PG20 固定提交已核验；这是静态源码核对，没有宣称 SQL 运行验证，也没有擅改固定英文示例。

新快照 checkpoint-fdw-handler-ready 完成十一版准备、解析与对齐。5,298 个节点精确绑定，范围内 160 条提示逐项核准，零未决、零漂移、零子节点数量差异；当前中文＝审定稿＝新快照，固定英文＝本次解包英文。66 条 SQL 命令名称提示保留初始记录后按 6 组名称逐版闭合。原始全书审计的非零退出码保留，此结论只覆盖实际读过的范围。

前一阶段 hstore／ltree／cube 提交 a198268 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-raw-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-version-boundary-proof.json)、[源文疑点及固定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-source-questions.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/fdw-handler-full-reviewed-certificate.json)。
