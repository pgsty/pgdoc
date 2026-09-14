PG10—PG20 CREATE TABLE 与关联章节校准记录（2026-09-15）

CREATE TABLE 十一版完整页已完成中英文对照、正文修订、横向一致性复核和修复后新快照核验。另逐项核对配置、维护、分区、索引、系统目录、全文检索及发行说明中的关联文本；共 105 个正文文件、527 处文本修订，六条术语及配套规则同步落盘。

从 PG18 开始，对照各版自己的固定英文，完整读取 66 个主节、769 个递归列表项、2,046 个叶段落以及语法、代码、标题、索引词和外围框架。CREATE TABLE 的 283 个实际代码/语法位置逐版核对并保持原字节。关联范围为 219 个英文变体及全部中文候选，共 746 个文本位置；231 个候选文件的源文快照用于精确绑定，不表示这 231 个文件都已完整阅读。162 个修订译文变体、35 个最终细化变体与最后一条新增规划表述均再次复读。

本轮发现并修复的问题：

- 分区锁定说明串版：PG14、15、16、17、19 错用了未来版本的缓存计划行为。已按本版英文恢复“初始化剪枝去掉的分区仍在执行开始时被锁定”；PG13 只统一同源措辞，PG18、20 原事实正确。PG10—12 没有本句，不添加。
- 分区定义：PG12—20 校正列名、类型必须与所属分区表相同的主语；十一版明确列表分区允许 SQL NULL、范围键值中的非 NULL 条件和第一个键列；PG10、11 将 LIKE 复制列的“空默认值”改为 NULL 默认值。
- 分区规划：PG11—20 明确索引只帮助扫描较少分区的情况，恢复“前一种情况无帮助”的限定；说明 CHECK 约束可在分区边界约束之外另加；区分查询规划与查询计划，统一分区剪枝及计划代价用语。
- 清理与扫描：逐版区别 aggressive vacuum 操作和 aggressive scan 动作；修复多事务 ID 应比较年龄而不是 ID 值的两处阈值语义，保留真正的扫描、全冻结页及各版触发条件。PG13—20 相关位置明确是“由插入触发的清理”。
- 索引与可见文字：十一版补译 EXCLUDE 说明中的谓词；PG11—20 对照 INCLUDE 的内含列、内含属性及 hash 分区术语；纠正发行说明将死索引条目写成已删除条目或留英文、半死亡状态缺中文，以及 B-树词内空白。PG14 一段普通清理动作补译。

[二十类问题/一致性项的十一版横向矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-matrix.md)逐项列出修订和原已正确的文本数量。细分为 160 个英文变体、1,760 个版本格：517 格有修订、17 格原已正确、1,226 格没有该精确英文变体。后者不是断言该版本没有相邻功能；一个段落也可能涉及多个类别，不能把这些数字作为独立缺陷总数。527 处实际改动全部绑定到问题类别及固定英文。

新增词表原序号 632—637：内含列、激进清理、激进扫描、半死亡、hash 分区、由插入触发的清理；词表和逐条规则各 637 条，别名记录 31 条。分区剪枝仍使用既定首选译名。普通“包含列名”“包含属性”、正确的“空值”、堆内元组更新及真实类型、参数、程序、状态名均保持；九项用户既定术语回退未变。

固定英文疑点单列保留：多列范围示例的 a 前缀断言、清理阈值公式与说明中标签的词序、PG18 发行说明 btree 的 xfunc-sql 链接目标。未静默改写固定英文或把疑点记为已修复。

十一版当前正文、审定稿、新快照和固定/解包英文精确一致。110 条范围内提示已逐项核定（88 个既有 ID、22 组匿名小节），零未决、零漂移；所有相关代码与 ID 保持。仅 checkpoint-create-table-finalized 用于本批验收。全书审计仍保留 PG10—12 退出码 3、PG13—20 退出码 1；关联候选文件中的 1,936 条范围外提示留待所属章节处理，不能据本批检查关闭。

CREATE INDEX 全页及其他尚未完成章节继续；全书最终对账、十一版 HTML 和 A4/US PDF 共 33 项最终构建仍未完成。

证据：[问题类别矩阵原始数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-semantic-families.json)、[英文变体十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-issue-version-matrix.json)、[精确修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-file-plans.json)、[标准变更前后对照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-norm-plans.json)、[完整校准证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-certificate.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-native-validation.json)、[提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-table-full-finalized-native-classification.json)。
