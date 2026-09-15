PG10—PG20 并行查询校准记录（2026-09-15）

从 PG18 的十一块完整正文和外层框架开始，实际阅读十一版 parallel.sgml；八种完整英文变体及全部中文候选逐项对照。全章 536 叶段、18 父段均纳入本批。规范仍为 647 条，九项用户回退保留。

PQ001：十一版“可以获得两倍以上的速度提升”容易混淆速度比例与增加量。对照 more than twice as fast，统一为“运行速度可以达到原来的两倍以上”。后续四倍或更高、查询受益条件与实现限制保留。十一版中英文 8,523 个 SGML 文件水平扫描，33 处相关命中全部绑定到实际读过的完整章节。

PG10—13 的 Gather 示例和扫描段外层说明复用相同英文的 PG18 审定译文，保留自己的原始输出及全部子段。四组新文本已完整复读。68 同源叶段组、2 父段组、18 其他组无未决译文冲突。十一版正文修订。[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-matrix.md)共 16 组、176 格：15 修复／复用、145 核准、14 不适用、2 格式例外。

本批完整核准 Gather 与 Gather Merge 的单子节点、排序语义、工作进程数量限制及领导者参与方式；计划生成和实际执行的不同限制、无可用工作进程和非零 fetch count 的回退；部分计划每个结果行恰由一个进程产生；顺序、位图堆和 B-树索引扫描的分工；嵌套循环、合并连接、普通 hash 与并行 hash 的内部输入处理；部分聚合和最终聚合、组合和序列化函数、DISTINCT／ORDER BY／GROUPING SETS 限制；Parallel Append 对部分与非部分子计划的处理；代价参数和 EXPLAIN 的调节提示；三类并行安全级别、函数默认标记、事务状态和本地状态、工作进程锁的寿命，以及规划器不会自动将受限谓词延后到 Gather 上方。

版本边界逐版保留：PG10 没有建表命令例外、Parallel Append 和共享并行 hash 说明，另有 CREATE TABLE .. AS EXECUTE .. 的限制；PG10、11 的动态共享内存和可串行化事务限制保留；PG11—13 的建表例外与 PG14 起含 REFRESH MATERIALIZED VIEW 的 SELECT 部分清单分别核准。PG10—13 顺序扫描按单块分发，PG14 起按范围分发。PG19、20 才有并行 TID 范围扫描。PG10—16 保留自身 InitPlan 限制，PG17 起相关清单移除该项，并允许使用子事务进行错误恢复的情形。此前 F-017 的 PG14—16 修复已在完整清单中再次复核，无再缺项。

十一个原始 EXPLAIN 块均未改动。九版与固定英文逐字节一致；PG13、14 仅有既有 QUERY PLAN 标题行尾空格差异，其他字节均相同。未执行示例。所有受保护值、链接、实体及主文档包含链按自身版本核准，无额外本地 ID。

新快照 checkpoint-parallel-ready：十一版 1,299 配对节点，零范围内提示、零未决、零漂移、零子节点差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文；全书原始审计退出码保留。本项为解析核验，并非 HTML／PDF 构建。

前一 JIT 阶段提交 b6f4ade5 已核验、未推送。本批准备阶段提交，继续 pageinspect。历史原 2,466 待追溯单元累计核准 221、余 2,245；全书逐句语义校准、独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-reread-proof.json)、[代码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-version-boundary-proof.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-source-inclusion-proof.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-all-occurrences-closure.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-native-validation.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/parallel-full-reviewed-certificate.json)。
