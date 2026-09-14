PG10—PG20 操作符参考页、xoper 与关联文本校准记录（2026-09-15）

本阶段已完成十一版 11 种操作符及访问方法参考页和 xoper.sgml 的完整中英文对照，共 132 个完整文件；另核对 216 个明确绑定的关联文本位置。116 个正文文件有修改，共 273 处修订。性能章节及全书剩余 hash 用语正在继续核对，不包含在本阶段闭合范围内。

按 PG18 优先、各版固定英文为准的流程，读取全部 34 个参考页英文全文变体、7 个 xoper 全文变体及其所有中文候选。已核对 653 个完整主节、2,144 个叶段落、标题、索引词、外围文字和 349 个代码/语法位置；新译文的 45 个变体也已复读。代码原样保留，两种既有 SQL 示例注释的中文本地化分别核准。259 个候选文件用于精确绑定，不表示全部文件已完整读完。

发现并修复的问题：

- PG14—16 CREATE OPERATOR 的 Notes 混入未来版本三种交换器定义方法、ALTER OPERATOR 设置交换器及相关所有权说明。已恢复各版自己的四段说明和链接；PG10—16 xoper 中合法的两种定义方法、占位操作符返回类型说明保留；PG17—20 的新属性和说明保留。
- 十一版 CREATE OPERATOR 将 lexical token 统一为“词元”，PG17、18 发行说明的数字 JSON token 同步修复；notation 语境中的“记号”经核对保留。CREATE OPERATOR 和适用版本 ALTER OPERATOR、PG19 发行说明中的 selectivity 统一为“选择率”。
- 操作符类、操作符族、xoper 及已读的 bloom、pageinspect、pgcrypto、xindex、发行说明关联段按不翻译词表统一 hash，保留实际代码和“哈希连接”“哈希槽”等既定例外；PG14—16 发行说明的 negator functions 改为“求反器函数”。
- PG13—20 ALTER OPERATOR FAMILY 的 equalimage 说明改为“等值映像函数”，并用各版相关定义和已有译文交叉核实；PG10—12 本条款未出现。十一版 DROP OPERATOR FAMILY 的 B-tree 改为“B-树”。
- 十一版 xoper 严格函数说明将含混的“非空”明确为“非 null 的输入”；PG10—16 CREATE OPERATOR 将 optimization clauses 译为“优化子句”，PG17—20 本版的 attributes 仍译为“属性”。

[问题与一致性项的十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-matrix.md)给出每项适用范围；[精确英文变体矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-issue-version-matrix.json)包含 45 组、495 格。格子和修订位置包含复用、正确项及不同版本措辞，不是独立缺陷总数。

RECHECK、后缀操作符、本版权限语法与链接均逐版核准；没有将新版本要求回填旧版。21 项额外标记是准确的既有 NONE、WHERE、size 包装，已逐项对照英文后保留。没有新增或改动翻译规范文件，使用现行不翻译词表和术语优先级。

新快照中当前中文、审定稿与快照逐字一致，固定英文与解包英文一致。418 条范围内提示均已绑定到完整已读单元：412 条既有 ID 提示、6 组匿名节点配对，零未决、零漂移。4,182 个节点有精确绑定记录；相关候选文件仍有 1,925 条范围外提示，留待所属章节处理，不计为本批缺陷或已通过项。仅 checkpoint-operator-reference-ready 用于验收；较早 clean 快照在空白检查后废弃。

此前 CREATE INDEX 十一版完整页复核也已闭合，本阶段一并保存其报告。全书逐句阅读、历史证据对账、十一版 HTML / A4 PDF / US PDF 共 33 项最终构建仍未完成；本批原生检查不等同于全书或构建通过。

证据：[审定源文件](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-file-plans.json)、[逐项改动](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-changes.json)、[完整证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-certificate.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-native-validation.json)、[提示逐项核定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-native-classification.json)、[显式标记处置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/operator-reference-ready-protected-dispositions.json)。
