PG10—PG20 CREATE FOREIGN TABLE 参考页校准记录（2026-09-15）

从 PG18 英中全文开始，读完其余所有版本的完整差异：7 个英文全文变体及全部 8 个中文候选，覆盖 66 节、184 个条目、409 个段落和 33 个语法／程序块。修订后的 19 个初始段落变体及 DEFAULT 共用段落已复读。相同英文采用审定中文，各版保留自己的语法、链接、分区边界和生成列限制。

PG14—17 移除了本版英文没有的 LIKE 整组语法、条目和兼容性说明，恢复 STORED 必需语法，移除未来 VIRTUAL 默认选项、ENFORCED/NOT ENFORCED 以及 NOT NULL 的 NO INHERIT 说明。删除的 28 个 ID 仅属于被移除的未来 LIKE 条目，其余原有 ID 保留。PG12/13 的 operator 按现行词表恢复为“操作符”；PG18—20 的 base columns 校正为“普通基础列”。十一版还逐一核对并统一 DEFAULT 定义、语法块说明和适用的共用段落，补回 PG10 的可见行限定。

下表修＝修订，核＝原已正确，读＝完整回归核对，—＝不适用。检查组含回归和措辞项，不能当作独立缺陷计数。

| 检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-CREATE-FOREIGN-TABLE-001 移除 PG14—17 未来 LIKE 语法、整组条目及兼容性说明 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-002 恢复本版 NOT NULL 语法和 NO INHERIT 说明范围 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-003 PG14—17 恢复 STORED 必需语法，移除未来 VIRTUAL 默认值 | — | — | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-004 移除 PG14—17 未来 ENFORCED/NOT ENFORCED 语法 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-005 语法块可见说明补译及共用措辞统一 | 修 | 修 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CREATE-FOREIGN-TABLE-006 生成列的可见索引翻译 | — | — | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CREATE-FOREIGN-TABLE-007 PG12/13 operator 恢复现行词表的操作符 | — | — | 修 | 修 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-008 LIKE INCLUDING GENERATED 的 base columns 误作基表列 | — | — | — | — | — | — | — | — | 修 | 修 | 修 |
| C19-CREATE-FOREIGN-TABLE-009 DEFAULT 定义保留不含变量及两项限制的原文顺序 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CREATE-FOREIGN-TABLE-010 PG10 补回查询约束说明的可见行限定 | 修 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-011 旧版对象名称枚举保持自己的英文范围和信息结构 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-CREATE-FOREIGN-TABLE-012 相同英文的共用段落按审定中文统一 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 | 修 | 核 |
| C19-CREATE-FOREIGN-TABLE-013 所有权、USAGE、默认排序规则和约束求值条件 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CREATE-FOREIGN-TABLE-014 FDW 约束责任、生成列读写与元组路由的各版限制 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CREATE-FOREIGN-TABLE-015 PG10 分区边界、PG11 hash 分区和 PG12 生成列的原文差异 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CREATE-FOREIGN-TABLE-016 本版示例、tableoid 标记与原有合法 ID | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |

16 组 176 格：59 个修订格、59 个原已正确格、14 个不适用格、44 个回归格。十一版当前文件、审定稿、新快照、固定及解包英文精确一致；82 条既有 ID 提示已逐项绑定，零未决、零漂移。原始整书审计退出码仍为 PG10—12 的 3、PG13—20 的 1，本页核验不代表整书通过。

关联扫描另发现 PG14—17 的 ALTER TABLE 含未来语法及说明，已进入完整对照；CREATE TABLE 的生成列及 LIKE 两个关联条款已完成十一版检查并修订 PG12—20，但改动晚于本快照，须在下一次新快照核验。跨章问题、全书阅读及最终 33 项 HTML/A4/US PDF 构建均保持未完成。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-foreign-table-full-issue-version-matrix.json)、[完整英中审定稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-foreign-table-full-finalized-file-plans.json)、[代码及语法](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-foreign-table-full-raw-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-foreign-table-native-validation.json)、[原生提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-foreign-table-native-classification.json)、[关联 CREATE TABLE 条款](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/foreign-associated-create-table-parent-plans.json)。

后续核验：关联 ALTER TABLE 全页及 CREATE TABLE 两个生成列条款已通过十一版干净新快照核验，详见 [ALTER TABLE 与关联条款报告](/Users/vonng/pgsty/pgdoc/docs/calibration-alter-table-20260915.md)。新发现的 ALTER FOREIGN TABLE 未来内容继续修复；全书和最终构建仍未完成。
