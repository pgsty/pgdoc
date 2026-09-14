PG10—PG20 hash 及关联语义校准记录（2026-09-15）

本阶段从 PG18 开始，逐一核对十一版自己的英文及中文，修改 303 个 SGML 正文文件和 PG20 的一份生成译文映射。规范中的 hash / Hash / HASH 与“哈希连接”“哈希槽”等完整术语分别处理；未增加新术语规则。

本轮发现并解决的主要问题：

- PG16 pg_stat_statements 的 queryid 说明混入新版函数、表别名及常量列表归并规则和示例，现恢复本版英文的表删除重建与 hash 冲突说明。PG17 补齐残留英文句的翻译及遗漏的文件标记；PG18—20 保留本版新规则。
- PG14—17 EXPLAIN BUFFERS 的默认值恢复为 false；PG14 只写本版的数据文件块计时范围，PG15、16 保留数据和临时文件，PG17 保留数据、本地和临时块。PG18 保留 ANALYZE 时自动启用，PG19、20 另保留规划阶段的自身条件。
- PG14—16 ltree 索引列表删除本版尚无的 Hash 条目；hstore 补回转换扩展应安装在同一模式的提示。PG10—14 的 Python 2 扩展名称和 PG15+ 的 Python 3 名称逐版保留；PG18—20 不回填上游已删除的安装提示。
- PG15、16 MERGE join_condition 删除本版没有的 WHEN NOT MATCHED BY SOURCE / FULL 连接说明；PG17—20 保留。PG10—14 中英文均无该参考页，已核对路径。
- 十一版 FDW 将“但会降低”修正为“但可能降低”，恢复 can result 的可能性；PG14—18 相关发行说明的 can prevent 也补回“可能”。
- PG15 发行说明将“所有分区的元组”改回“该分区的所有元组”；PG18 将“散列加盟”修正为哈希连接中的 hash 表大小选择逻辑。其他版本分别核对各自条款，未复制其他版发行说明。
- 十一版密码认证段区分密码学 hash 与加密；可规划查询统一为“可规划的查询”。PG11—20 并行计划说明使用代价用语，PG10 保留自身旧说明。INCLUDE 注释、hash API 注释、生成等待事件说明、可见索引及段落外层文字同步校准。

[16 类问题及一致性项的十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-matrix.md)逐项列明修复、已核正确和无对应条款；[精确英文矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-issue-version-matrix.json)为 302 组、3,322 格：1,043 格修订、1 格核对后保留、2,278 格未出现同一英文变体。英文变体格、文本绑定和实际缺陷不是同一计数，未出现同一英文变体也不表示该功能不存在。

本阶段完整读取 339 个初始英文变体、8 个其他译法变体及所有中文候选；另读完 22 个 hstore / ltree 相关节、6 个 MERGE 参数条目、32 个外层段首和 78 个生成表行。新译文中 56 个语义修订组逐项复读，262 个纯拼写组核准仅改变 hash 拼写、大小写或间距，并保留完整连接名称；最终细化稿再次复读。核验时补读十一版 hstore 作者节，用完整相邻节配对解决匿名结构提示。

1,294 个主体绑定与补充生成映射均有源文位置证据。PG20 的 10 个修改后生成行经新快照实际重放，与审定稿完全相同。当前中文、审定稿和新快照逐字一致；固定英文与解包英文一致。原生核验 1,857 个配对节点、18 条范围内提示全部核定，零未决、零漂移、零子节点计数缺口。初次六条未决及后补的两条作者节 ID 提示均保留证据；有效中文 ID 未为消除提示而删除。

全部 304 个源码差异无空白问题，受保护标记及代码核对通过。普通“哈希／散列／杂凑”的源码残余扫描为零；这只证明本轮术语扫描结果，不替代全书语义阅读。本批候选文件中还有 2,970 条范围外结构提示，仍纳入后续全书对账。

原始 F-001—F-026 的逐版状态见[累计报告](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)。本阶段关闭明确读过的文本及相关完整节；其余文件内容、全书语义校准、历史范围对账仍在进行。最终十一版 HTML / A4 PDF / US PDF 共 33 项构建尚未完成，原生解析不是最终构建验收。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-file-plans.json)、[文本位置绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-atom-proof.json)、[新快照验证](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-native-validation.json)、[最终提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-native-final-classification.json)、[补读作者节](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-hstore-authors-reread.json)、[核验证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/hash-horizontal-ready-certificate.json)。本阶段仅以 checkpoint-hash-horizontal-ready 为验收快照。
