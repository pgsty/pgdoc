PG10—PG20 pageinspect 校准记录（2026-09-15 开始，2026-09-16 验收）

从 PG18 的十四块完整正文开始，实际阅读十一版 pageinspect.sgml、十种完整英文变体和全部中文候选，随后核对 29 个完整相关范围。共 37 文件、40 范围、489 叶段、298 个完整函数条目。规范仍为 647 条，九项用户回退保留。

确认并修复六类问题：

- PI001：PG13、14、16—20 将普通概念 minus infinity 留为英文，改为“负无穷”；PG10—12、15 自身译文已正确。
- PI002：PG10—16 的 GIN 叶页说明混入“压缩”限定，删除自身英文未包含的限定；PG17 起保留。
- PI003：PG14、15 多出 PG16 才新增的 bt_multi_page_stats，删除两个完整未来函数条目；PG16 起自身条目保留。
- PI004：PG14、15 的 brin_page_items 示例混入未来 empty 列，恢复自身七列输出；PG16 起保留八列。
- PI005：PG14 的 gist_page_items 示例误用新版六行坐标，恢复自身七行输出及全部坐标。
- PI006：PG14、15 的 bt_page_stats 将 single pages 改成新版“数据页”，恢复“单个页面”。

相同英文的页面参数、示例和校验和说明复用审定译文，并另行跨代码块和行内标签分组，补齐页面时间一致副本、FSM 指针、B-树示例说明及 PG15 一条发行说明的同源复用。各版自己的完整原始块、链接、行内标记与 SGML 框架保留。最终 20 组新文本均已实际中英复读；79 同源叶段组、73 其他组及 62 个跨标记正文组无未决译文冲突。共修改 12 个正文文件。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-matrix.md)为 22 组、242 格：32 修复／复用、158 核准、28 不适用、13 例外、11 源文疑义。十一版中英文 8,523 个 SGML 文件扫描到 498 处命中：496 处绑定完整已读范围，另 2 处为实际读过的 PG16 非渲染源文提交注释，均已归类。

完整核准原始块读取和数据分支、时间一致性、页面头与校验和，堆行指针和 MVCC、属性拆分和 infomask，B-树元页、倒排列表、高键、下行链接和 htid，BRIN 类型／元页／范围映射／数据，GIN 元页和叶页，GiST 键解码和原始输出，Hash 桶／溢出／位图／元页及所有函数的参数和返回约定。相关 GiST 距离、分区 MINVALUE／MAXVALUE、发行说明和功能新增边界逐版对照。

自身版本差异保留：heap_tuple_infomask_flags、B-树倒排列表和 allequalimage 从 PG13 起；GiST 函数和 bigint 块号从 PG14 起；FSM／VM 链接与 FSM acronym 从 PG15 起；bt_multi_page_stats 和 BRIN empty 列从 PG16 起；GIN 压缩限定从 PG17 起；校验和未启用的说明、PG19 起 LSN 填零和 SQL 大写等均依本版英文。B-树元页版本号 PG10 为 2、PG11—12 为 3、PG13 起为 4，清理字段和 ctid／htid 语义分别核准。

276 个本版原始块中，3 个恢复本版示例输出，273 个未改动；另移除未来函数的 2 个完整示例。33 处既有行尾空格差异逐行列明，其余原始字节与自身英文一致。14 个本地 ID 和 8 个既有高键 quote 包装保留。brin_page_items 与 hash_bitmap_info 的固定英文将索引参数标为 oid，示例却直接传索引名：两项各十一版分别记录疑义并保留；未执行示例，也未断言其为运行错误。

最终新快照 checkpoint-pageinspect-final-ready：十一版 2,541 配对节点，14 处提示均精确绑定并归类为既有本地 ID，零未决、零漂移、零子节点差异。当前中文＝审定稿＝最终新快照，固定英文＝新解包英文。早先 checkpoint-pageinspect-ready 只代表补充修改前的中间稿，最终验收使用新快照。PG14 审计曾因磁盘空间耗尽失败，PG15 随后主动停止；失败日志保留，清理临时生成目录和不可变审计文件去重后，在已成功生成的同一份审定输入上重新运行这两版审计。重跑证据为 commands-retry1.json 与 audit-retry1，PG10—13 已完成结果保留，PG16—20 正常续跑。本项是解析核验，不是 HTML／PDF 构建。

前一并行查询阶段提交 16c3a21c 已核验、未推送。本批准备阶段提交，继续规划器统计信息章节。历史原 2,466 待追溯单元累计核准 221、余 2,245；全书逐句语义校准、独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。另需把本轮加强的跨代码块和行内标签正文分组检查纳入此前各批次的最终一致性复核，不能用旧的整单元分组零冲突替代。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-changes.json)、[补充复用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-consistency-amendments.json)、[跨标记分组](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-cross-markup-prose-groups.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-raw-proof.json)、[保护值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-version-boundary-proof.json)、[所有函数](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-complete-function-proof.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-all-occurrences-closure.json)、[源文疑义](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-source-questions.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-native-validation.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pageinspect-final-reviewed-certificate.json)。
