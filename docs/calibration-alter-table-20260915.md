PG10—PG20 ALTER TABLE 与关联 CREATE TABLE 条款校准记录（2026-09-15）

十一版 ALTER TABLE 已完成全文审读、正文修复和新快照结构核验。从 PG18 开始，读完 164 个完整条目变体、82 个条目外段落变体、13 个节框架、10 个全文框架及 42 个语法／代码变体；其他版本按自身英文逐项核对。共覆盖 66 节、721 个含嵌套条目、1645 个叶段落或掩去嵌套条目后的段落、314 个语法／代码块。PG19 合并拆分条目的原有中文另在其实际位置完整复读。44 个修订段落变体和 20 处最终细化也已复读。这些数量是覆盖范围，不是缺陷数量。

PG14—17 的主要问题是误用未来语法及其说明，已恢复本版生成列、约束、统计目标、存储选项、访问方法、触发器和表重写规则。PG10—13 补回了被重复磁盘空间段落替代的分区附加扫描说明；PG10—17 的 NOT VALID 验证步骤移除本版没有的非空约束。PG19 合并、拆分条目保留正文和 ID，移回英文对应的描述节。303 个程序示例逐字保留；11 个语法块只作本版语法恢复及可见说明本地化。删除的 9 个条目均为本版英文不存在的未来功能，其他既有锚点保留。

修＝修订，核＝原已正确，读＝完整回归核对，—＝不适用。每组均有十一格；措辞及回归组不能当作独立缺陷。

| 检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ALTER-TABLE-001 VIRTUAL 未来语法及 STORED 必需边界 | — | — | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-002 WITHOUT OVERLAPS / PERIOD 未来语法 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-003 NOT NULL 表约束及 NO INHERIT 未来语法 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-004 ENFORCED / NOT ENFORCED 未来语法 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-005 SET EXPRESSION 未来条目与语法 | — | — | — | — | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-006 SET STATISTICS 恢复数值及 -1；DEFAULT 仅本版已有时保留 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-007 SET STORAGE 恢复 DEFAULT 选项的本版范围 | 核 | 核 | 核 | 核 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-008 SET ACCESS METHOD 条目、DEFAULT 及后续分区说明范围 | — | — | — | — | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-009 SET/DROP NOT NULL 移除未来 NOT VALID、ONLY 与验证说明 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-010 SET DATA TYPE / SET EXPRESSION 统计信息说明与虚拟列边界 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-011 DROP EXPRESSION 存储生成列说明及虚拟列段落边界 | — | — | — | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-012 ADD/VALIDATE CONSTRAINT 的约束种类和 NOT ENFORCED 范围 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-013 恢复分区表外键不得声明 NOT VALID 的旧版限制 | — | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-014 触发器克隆状态递归说明的本版范围 | 核 | 核 | 核 | 核 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-015 SET LOGGED/UNLOGGED 序列持久性及分区表说明范围 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-016 INHERIT 中 NOT NULL 与 CHECK 的不同限制 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-017 REPLICA IDENTITY DEFAULT 保持本版原文范围 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-018 USING INDEX 说明中的 CREATE INDEX/CREATE UNIQUE INDEX 本版形式 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-019 Notes 的 DEFAULT、表重写、索引重建与列种类边界 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-020 补回分区附加扫描句，移除误替的重复磁盘空间说明 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ALTER-TABLE-021 NOT VALID 验证步骤移除旧版误入的非空约束 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-022 恢复本版 SQL 标准兼容性段落 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-ALTER-TABLE-023 PG19 MERGE/SPLIT 完整内容及 ID 从参数节移回描述节 | — | — | — | — | — | — | — | — | — | 修 | — |
| C19-ALTER-TABLE-024 补译语法块全部可见 phrase，保留各版代码 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-025 DROP EXPRESSION 的 normal base column 统一为普通基础列 | — | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-026 ONLY 父表删除 NOT NULL 的可见标记恢复本版形式 | — | — | — | — | — | — | — | — | 修 | 修 | 修 |
| C19-ALTER-TABLE-027 存储参数交叉引用纠正所属文档关系 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-028 varchar 添加列示例明确填充的是新列 | — | — | — | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-029 hash/Hash 分区按不翻译词表处理 | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-030 规则与行安全性策略的所属关系及现行术语 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-031 USER 触发器选项明确内部约束触发器为排除项 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-032 COLUMN 的 noise 改为不影响语义的准确说明 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-033 所有者角色、new_owner 与单个触发器的措辞 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-034 ATTACH FOR VALUES 不误限于范围分区 | — | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ALTER-TABLE-035 PG19 SPLIT 说明明确新分区边界合并后须匹配 | — | — | — | — | — | — | — | — | — | 修 | — |
| C19-ALTER-TABLE-036 并发分离的锁、两事务、CHECK 等价条件及 FINALIZE | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-TABLE-037 所有权、USAGE、SET ROLE 与旧版成员身份要求 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-TABLE-038 OID、分区、PG19 合并拆分与 PG20 原文边界保留 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-TABLE-039 全部 314 语法及代码块、本版链接和合法 ID | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-ALTER-TABLE-040 完全相同英文和语境的共用译文一致性 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |

ALTER TABLE 合计 40 组 440 格：179 修订、156 原已正确、50 不适用、55 回归。十一版当前文件、审定稿、干净新快照、固定及解包英文精确一致；124 条既有 ID 提示逐项核定，零未决、零漂移。一次包含空白行尾空格的初始快照已取消，验收只使用 checkpoint-alter-table-clean。

关联 CREATE TABLE 的 GENERATED 和 LIKE INCLUDING GENERATED 两个完整条款也已核对十一版：PG10/11 原文无该功能，PG12—20 共 18 个适用父条目。修正“其他生成列”和“任何生成表达式”，保留 STORED、VIRTUAL 默认选项及虚拟列对用户定义类型／函数的各版限制。

| 检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-foreign-associated-create-table-generated 共同生成表达式限制段与外部表参考统一 | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-foreign-associated-create-table-like-generated INCLUDING GENERATED 共同段与外部表参考统一 | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |

关联条款共 2 组 22 格：15 修订、3 原已正确、4 不适用；4 条既有 ID 提示逐项核定，零未决、零漂移。该证明仅覆盖这两个完整条款；CREATE TABLE 其余正文及 106 条范围外提示仍待全页审校。

固定英文疑点保留原文并留档：PG19 的 MERGE PARTITION 单数写法及 partition_name1/2 的拆分说明，PG18 ALTER CONSTRAINT 的语法与外键说明范围，以及 PG18—20 Notes 中 CHECK 递归说明与新非空约束的关系。没有擅自改写英文或将疑点当成译文事实。

关联扫描又确认 ALTER FOREIGN TABLE 的 PG14—17 ADD NOT NULL 说明及 PG14/15 STORAGE DEFAULT 是未来内容，并找到十一版 COLUMN 的 noise 直译。该参考页已完整读完，修复和新快照核验继续。原始整书审计退出码仍为 PG10—12 的 3、PG13—20 的 1，不能表示整书通过；全书剩余阅读、历史对账和 33 项最终 HTML/A4/US PDF 构建均未完成。

证据：[ALTER TABLE 十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-table-full-issue-version-matrix.json)、[完整英中审定稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-table-full-clean-file-plans.json)、[程序和语法](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-table-full-clean-raw-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-table-native-validation.json)、[原生提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/alter-table-native-classification.json)、[CREATE TABLE 关联条款](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/foreign-associated-create-table-parent-plans.json)、[关联条款新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/foreign-associated-create-table-native-validation.json)。
