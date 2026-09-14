PG10—PG20 ALTER FOREIGN TABLE 参考页校准记录（2026-09-15）

从 PG18 完整英中参考页开始，读完 6 个英文全文变体和全部 7 个中文候选。其余版本逐一对照全部差异；仅有 SGML 短结束标记、ID、属性大小写及空白差异时保留本版写法。范围覆盖 66 节、376 个条目、499 个叶段落、11 个语法块和 22 个程序块；五个修订段落变体已复读。

PG14—17 的 ADD table_constraint 错用了 PG18 新增的 NOT NULL 支持及其 NOT VALID 限定，已恢复本版仅 CHECK 的说明。PG14/15 的 SET STORAGE 语法移除本版没有的 DEFAULT。十一版的 COLUMN “只是噪声”改为“不影响语义”；PG16—20 明确 new owning role 是新的所有者角色。PG19 的 ADD IF NOT EXISTS 段落按相同英文共用审定译文。各版 OID、成员身份与 SET ROLE 权限、远端一致性限制、触发器、链接均保留自己的边界。

修＝修订，核＝原已正确，读＝完整回归核对，—＝不适用，疑＝固定英文疑点。检查组含措辞与回归项，不能当成独立缺陷数量。

| 检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ALTER-FOREIGN-TABLE-001 ADD table_constraint 移除未来 NOT NULL 及 NOT VALID 限定 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-FOREIGN-TABLE-002 SET STORAGE 恢复本版 DEFAULT 选项范围 | 核 | 核 | 核 | 核 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| C19-ALTER-FOREIGN-TABLE-003 COLUMN 的 noise 说明改为不影响语义 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-FOREIGN-TABLE-004 new owning role 明确为新的所有者角色 | 核 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-FOREIGN-TABLE-005 ADD IF NOT EXISTS 同文同译及语句顺序 | — | — | — | — | 核 | 核 | 核 | 核 | 核 | 修 | 核 |
| C19-ALTER-FOREIGN-TABLE-006 SET WITH/WITHOUT OIDS 保留本版能力和废弃边界 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-FOREIGN-TABLE-007 所有权、成员身份/SET ROLE、USAGE、触发器及远端一致性 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-FOREIGN-TABLE-008 完整语法、示例、参数、链接及既有锚点 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-FOREIGN-TABLE-009 PG10 DROP 选项示例保留固定英文的 value3 并记录疑点 | 疑 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |

9 组 99 格：23 修订、28 原已正确、4 不适用、43 回归、1 源文疑点。PG10 固定英文示例中的 DROP opt3 带有 value3，而该动作语法无需值；本轮保留该版原代码并记录疑点。PG11—20 保留不带 value3 的自己的示例。22 个程序块均未改动。

十一版当前文件、审定稿、修复后的新快照、固定及解包英文精确一致。唯一既有 ID 提示已逐项核定，零未决、零漂移。验收使用 checkpoint-alter-foreign-table-reviewed；提前于修复启动的快照已取消，不计验收。原始整书审计退出码仍为 PG10—12 的 3、PG13—20 的 1，本页通过不等于全书通过。

前一阶段表定义参考页与关联条款已提交 b6f2bb929d2116a2f57805be881f58d6650ec838，34 个文件（31 正文、3 报告），未推送。本页关联修复现已核验完成。系统目录与视图的 367 个段落变体、129 个节框架已读，表格及剩余条目继续；全书语义校准、历史对账和最终 33 个 HTML/A4/US PDF 构建均未完成。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-foreign-table-full-issue-version-matrix.json)、[完整英中审定稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-foreign-table-full-file-plans.json)、[代码及语法](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-foreign-table-full-raw-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-foreign-table-native-validation.json)、[原生提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-foreign-table-native-classification.json)。
