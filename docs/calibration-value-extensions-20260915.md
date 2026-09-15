PG10—PG20 hstore、ltree、cube 全文校准记录（2026-09-15）

十一版三个扩展共 33 份正文已完整对照，另核对 11 处 pg_type 的 int 对齐定义。以 PG18 的 114 个完整子块和外层框架为入口，完整阅读 21 组本版英文全文变体及全部中文候选；全书关联检索 65 处命中，54 处在已读正文，余下 11 处为同源目录定义。最终修改 33 个正文文件，未修改规范、链接或既有定制锚点。

- PG14—16 ltree 的示例仍含未来 CREATE INDEX path_hash_idx，现已按本版完整程序块移除。此前 hash 批次只修到了正文索引清单，未覆盖这三处原始示例；这次补足，并核准 PG17 起保留 hash 索引。
- PG15/16 ltree 缺少转换扩展安装提醒，已恢复完整 caution；PG17 同段普通 transform 漏译改为转换。PG10—14 ltree 和 PG10—17 hstore 已有提醒，按同源语义统一；PG18—20 原文移除，不添加。
- PG11—20 cube 的负编号取得的是对应正编号所取坐标值的相反数，原译容易误读为正坐标值的相反数，已校准。PG10 固定英文与 C 实现均无负编号支持，保持自身语义。
- PG10—14 cube 的标题误用了未来长标题，且作者 I believe／I assume 的语气丢失，已恢复本版。PG15 原有短标题与第一人称正确；PG16 起保留自身长标题和无主语表述。
- 十一版 hstore 引言恢复可能性，明确 rarely examined 修饰属性；cube 普通 is point 标志及几何 box 漏译已修。PG13—20 ltree 明确 siglen 是 int 对齐单位的正整数倍，最大 2024 字节；十一版 pg_type 的对应定义原本正确。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-matrix.md)共 21 个问题与检查组、231 格：68 修复、126 本项语义已正确、20 本版不适用、17 固定英文疑点格。组数包含功能边界和一致性检查，不等于独立缺陷数。

完整范围绑定 3,123 个叶段落、259 个嵌套父段落和 474 个原始块。374 个同源叶段组、30 个父段组、461 个其他单元组无未处置的语义冲突；5 组等价换行或既有负偏移标记保留。25 组最终修订文本及 12 组完整行注释（含一处既有标点变体）已复读；44 范围的受保护标记与链接核准。PG14—20 两个额外 -offset 参数包装是既有等义形式，原样保留。

十一版固定英文 cube 排序示例称按右上角第一坐标排序，却写 c ~> 3。固定 C 实现与本页公式一致：3 对应第二维下界，第一维上界应为 2。这是源文疑点，保留原始示例及相应译文；发布包 SHA256、C 文件哈希及 PG20 固定提交均已核准，两个完整实现变体和共同头文件定义已读。仅进行静态源码核对，没有宣称运行时测试。ltree PG13—18 源文的多余右括号也单列记录，中文原已配对正确。

新快照 checkpoint-value-extensions-ready 完成十一版准备、解析与对齐。8,799 个节点精确绑定，范围内 66 条提示逐项核准，零未决、零漂移、零子节点数量差异；当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计的非零退出码保留，这一结论只覆盖本批实际读过的范围。

前一阶段转储恢复提交 c3b45a3 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-raw-proof.json)、[行注释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-annotation-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-version-boundary-proof.json)、[固定 C 源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-fixed-cube-source.json)、[源文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-source-questions.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/value-extensions-full-reviewed-certificate.json)。
