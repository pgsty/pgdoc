PG10—PG20 性能章节与关联文本校准记录（2026-09-15）

本阶段完成十一版 perform.sgml 全章及 235 个明确关联文本位置的中英文核对，共修改 56 个正文文件和 3 个规范文件。阅读顺序从 PG18 开始，再逐一核对各版自己的英文差异；完整读取 23 个正文变体、104 个示例变体及所有中文候选，覆盖 55 个主节、1,341 个叶段落、447 个实际示例位置和外围文字。关联文件只关闭明确绑定的文本，不将其余内容算作已读。

发现并修复的问题：

- PG14—16 EXPLAIN 章节混入未来版本的 Index Searches、跳跃扫描、禁用节点显示、初始计划新说明、SERIALIZE 等内容和新计划输出。现已恢复各自原文；PG14 不增加 MERGE，PG15、16 保留自己的 MERGE 说明。统计节的新版示例和“只显示前十项”限定也恢复为本版内容。
- PG10—16 说明中的页面数和总估计代价恢复为 358 / 458；PG17—20 保留自己的 345 / 445。旧版传输代价段删除其原文没有的文本格式转换说明。PG13—16 固定英文的排序示例仍出现 445，这一源文内部疑点单独保留，未做数字全局替换。
- 十一版归并连接说明明确为停止读取“尚未耗尽的输入”，补齐仅重扫匹配部分的限定；多列非重复值统计补齐“两个或更多列”，函数依赖说明恢复“不能据此断定结果为零行”的逻辑。
- 十一版显式连接说明补齐“内连接”，将连接顺序数量“减少五倍”修正为“减少到原来的五分之一”。PG12—20 MCV 说明补齐估计的对象为分组数量；PG14—20 将“42%的时间”修正为“42%的情况”，PG10—13 原译准确保留。
- 按规范统一估计代价、选择率、非重复值、非 null 输入和外连接补齐 null，区分 hash 表、桶、运算与“哈希连接”；PG18—20 跳跃扫描段统一为 B-树。planstats、syntax、教程、psql 和适用发行说明中的关联位置同步核对修复。
- 将普通概念 initplan 译为“初始计划”，新增术语表第 638 条、对应语境规则及变更记录。实际计划输出和内部标识 InitPlan、InitPlans、SubPlan 保留。PG11—15 本轮修订普通概念的发行说明，PG17—20 修订性能正文；PG10、16 本次选定位置只有实际标签。这些适用格不是功能引入版本判断。
- 标题和可见索引词与正文同步；保留各版已有 ID。PG17、18、20 的 15 个中文标题锚点逐项绑定本版英文标题及完整父节，仅三处非重复值标题的 xreflabel 随术语修订。

[18 类问题与一致性项的十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-matrix.md)列明每版修复、已核保留和不适用位置。[精确英文矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-issue-version-matrix.json)为 54 组、594 格：375 格修复、22 格核对后保留、197 格未出现该英文变体；最后一类不表示功能不存在。386 个不同修订绑定包括整节恢复及其内部细化，不能作为互不重叠的缺陷数量。

新原生快照中，当前中文、审定稿与快照逐字一致，固定英文与解包英文一致。2,038 个节点精确配对；44 条范围内提示已逐项核定为既有 ID 或标题锚点，零未决、零漂移。初次核验中的 30 条未决保留原始记录，补充标题和父节证据后归入最终分类，未删除有效锚点来消除提示。候选文件的 1,398 条范围外提示仍属后续全书工作。

59 个正文及规范差异检查无空白问题，638 条术语与规则对应一致；示例只保留已核准的原有本地化、实体和空白差异。仅 checkpoint-performance-full-finalized 是本阶段验收快照。

更广的 hash 相关文本、其余未读章节、历史范围对账仍在继续。最终十一版 HTML / A4 PDF / US PDF 共 33 项构建尚未完成，本阶段的原生解析不能替代最终构建验收。

证据：[逐项修改](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-unique-changes.json)、[审定源文](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-file-plans.json)、[核验证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-certificate.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-native-validation.json)、[最终提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-native-final-classification.json)、[标题锚点证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/performance-full-finalized-native-anchor-proof.json)。
