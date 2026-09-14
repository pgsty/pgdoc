PG10—PG20 CREATE INDEX 完整页复核记录（2026-09-15）

在关联术语修复提交 353db5e27808ee16a3cf8e1d748d48df48277332 的基础上，十一版 CREATE INDEX 完整页现已逐一完成中英对照及原生核验。本轮没有新增确认缺陷，也没有额外改动正文。

从 PG18 开始完整读取参数、存储选项、并发构建、注解、示例、兼容性和页面框架，再对照其余版本自己的全部差异及中文候选。范围为 9 个英文全文变体、23 个完整节变体、66 个实际主节、297 个递归条目、915 个叶段落、139 个代码/语法位置。后两处同源中文候选只在段落空白上有区别，保留原格式；排他约束和规则允许的排除约束别称均未因偏好改写。

逐版保留 INCLUDE、GiST/SP-GiST 支持范围、NULLS DISTINCT、操作符类参数、旧 vacuum_cleanup_index_scale_factor、填充因子说明、GiST 缓冲与排序构建、并行索引构建支持方法、search_path、并发等待规则和 REINDEX CONCURRENTLY 的本版差异。PG10 没有 INCLUDE、ONLY 和单次索引构建的并行工作者说明，未补入新版功能；各版命令、示例、属性和链接原样核准。

当前正文未变，因此直接使用与当前文件逐字一致的 checkpoint-create-table-finalized 新快照。固定英文、解包英文、中文快照和当前文件精确一致；1,396 个完整节点配对，146 条提示逐项核定，零未决、零漂移。六类完整节形成 66 格 READ_OK，不能把这些通过项计为新增修复。全书余项、历史最终对账及十一版 HTML/A4/US 共 33 项最终构建仍未完成。

证据：[完整证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-index-full-certificate.json)、[十一版完整节矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-index-full-issue-version-matrix.json)、[完整页快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-index-full-file-plans.json)、[原生核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-index-full-native-validation.json)、[全部提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-index-full-native-classification.json)、[代码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-index-full-raw-proof.json)。
