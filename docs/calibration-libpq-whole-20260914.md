**PG10—PG20：libpq 全章校准结果**

十一版 libpq 全章已按完整中英语义单元完成本阶段校准，并以修订后的新快照核验。原始阅读清单覆盖 468 个条目变体、336 个段落变体、12 个表行变体、3 个表格框架、94 个节框架、6 个章框架及 225 个代码变体；相同英文的所有不同中文候选均按本版核对。

最终源码覆盖 537 个节范围及 2,079 个本版英文代码块。526 个节直接匹配完整审定父块；11 个命令执行父节由已读外层框架和四个完整子节组成。十一版当前源码、审定稿、新快照、固定英文与原生解包英文对应一致。

累计 398 个检查组、4378 个逐版格：ALREADY_CORRECT=987、FIXED=2712、NOT_APPLICABLE=667、RETAINED_SOURCE_DOUBT=7、REVIEWED_EXCEPTION=5。这些格包含缺陷修复、措辞、原本正确的条件、不适用与源文疑点，不能当作新增缺陷数量。

主要修复包括旧版混入未来功能、参数归属、容量与字节单位、返回值和 NULL 条件、内存与对象生存期、读写与发送顺序、并发与回调条件、SSL 反义及版本规则、OAuth 跨文件遗漏、代码示例不同步和原有可译注释。完整逐项状态见[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-issue-version-matrix.json)。

最初 87 条配对信号中，86 条来自合法的已翻译标签，另 1 条为 PG14 混入未来证书说明，已修复。最终原生检查保留 222 条提示：193 个既有本地 ID、17 组匿名单元配对、11 组文件用途表行、1 条 PG14 英文错误 API 名所致引用差异。每条均重新按当前行号绑定完整审定文本或对应版本源码勘误证据，零未决提示、零源码漂移。

这次关闭的是 libpq 全章的语义及源码结构核验。**其余全书语义校准、历史修复对账和最终 33 项 HTML/A4 PDF/US PDF 构建仍未完成。** 原生工具的全书原始退出码仍保留，不把合法定制忽略掉或降低检查强度；本报告也不把它们冒充全书构建通过。

证据：[全章逐节覆盖](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-source-coverage.json)、[代码覆盖](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-source-raw-coverage.json)、[原始信号处理](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-source-initial-signal-closure.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-native-validation.json)、[222 条全文分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-native-classification.json)。
