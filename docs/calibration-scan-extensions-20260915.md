PG10—PG20 自定义扫描及表采样全文校准记录（2026-09-15）

十一版 custom-scan、tablesample-method、tsm-system-rows、tsm-system-time 共 44 个完整文件已中英对照。从 PG18 的 8 个接口章节子块／外层框架和 4 个模块子块起读，阅读接口章节全部 8 组英文全文变体、模块全部 8 组全文变体及所有中文候选。208 处关联命中中，206 处位于这四章内；其余 PG10/11 两个完整发布段落也已读。共 46 文件、46 范围，修改 26 个正文文件。

- PG14—16 自定义扫描章混入后续固定文档的 Gather Merge、add_partial_path、custom_restrictinfo 结构字段及说明、连接子句附注，已恢复各自英文的完整段落和代码。PG15/16 自身已有投影标志，保留其解释。
- 十一版表采样章将“该表页的一小部分”改为“该表中的一小部分页”，澄清访问比例；EndSampleScan 改为“在没有此类资源的常见情况下”，明确可省略清理函数的实际条件。
- PG14—20 NextSampleBlock 的说明澄清为返回下一个待扫描页的块号；PG10—13 原本含义正确，复用同源语句。PG10/11 无 nblocks 参数的旧签名和可见性数组契约完整保留。
- PG10—13 路径钩子中的 base relation 统一为基本关系。PG15 的 tsm_system_time 恢复本版短标题；PG16 起长标题按本版保留。
- 两个模块的受信任说明从 PG13 起存在，相同英文复用“该模块”的完整译文；函数、采样限制、单位、权限和链接均核准。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-matrix.md)包含 21 个问题与检查组、231 格：49 修复、179 本项语义已正确、3 本版不适用。逐项核对对象所有权和初始化、回调约定、并行共享内存、参数和种子、采样估计、可重复性、预取及可见性检查，以及两种采样模块的行数／毫秒单位和均不支持 REPEATABLE 的限制。

功能和文档版本边界分开记录：固定 PG17 英文开始包含上述扩展路径说明，不能据此推断接口也从 PG17 才可用。PG10/11 自身发布说明已经记载部分路径支持，本批完整核准并保留该证据。

714 个叶段落、318 个嵌套父段落和 340 个原始块绑定本版源文；17 组最终修订文本已完整复读。78 个同源叶段组、31 个父段组、24 个其他单元组无未决冲突。两组等价差异仅为既有 Gather literal 包装，保留各版形式；七个章节中的这些既有标记另有精确例外记录。46 范围受保护内容和链接均核准，340 代码／签名／输出块与本版英文一致，未新增术语规则。

新快照 checkpoint-scan-extensions-ready 完成十一版准备、解析和对齐，1,631 个节点精确绑定，范围内 25 条提示逐项核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，此结论仅覆盖本批范围，不代表全书检查通过。

前一阶段 pgcrypto 提交 b316630 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-version-boundary-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/scan-extensions-full-reviewed-certificate.json)。
