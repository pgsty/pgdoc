**PG10—PG20：ECPG SQL 命令参考校准结果**

从 PG18 开始完整阅读 39 个英文命令页面变体、对应的全部中文候选及两个顶层框架。十一版共 183 个参考页、2626 个文本段、422 个外层条目和 55 个嵌套连接形式；30 个修订稿变体及全部修改注释已复读。454 个语法、程序和输出块按本版英文核准，改动限于 45 处明确列出的可见 C 注释，代码与内联受保护内容无残余差异。

主要修复：十一版 ALLOCATE DESCRIPTOR 的“使用后应释放”被弱化为“以后可以释放”；SET DESCRIPTOR 接收的 SQL 常量误写成标识符。PG14+ DECLARE STATEMENT 的关联有效性取决于声明位于动态语句之前，原译把源代码顺序写成了物理顶部；同一节及 EXECUTE IMMEDIATE、PREPARE 的 Notes 标题未译。预备语句、结果列元数据、描述符头部、VAR 类型指定和自动提交说明也已横向校准。

保留各版差异：PG10 的 DEFAULT 连接语法、PG11 起 DO CONTINUE、PG14 起 ASENSITIVE 与 DECLARE STATEMENT、PG10—13 的描述符头部多项目形式及 C 字符串说明。对照十一版固定实现后，将 GET DESCRIPTOR 引言行数与 COUNT 实际列数的差异、WHENEVER NOT FOUND BREAK 缺 DO 两项列为原文疑点，译文保留本版英文，未声称运行或上游修复。

修＝修复或统一，核＝原本正确，—＝不适用，源疑＝保留原文疑点。以下 39 组共 429 格，含完整页面回归检查，不是独立缺陷数。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-SQLREFS-001 描述符使用后应释放而不是以后可以释放 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-002 SET DESCRIPTOR 接收 SQL 常量而非标识符 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-003 DECLARE STATEMENT 的关联范围与源代码顺序 | P2 | — | — | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-004 Notes 标题遗漏翻译 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-005 DESCRIBE 获取结果列元数据的含义 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-006 GET DESCRIPTOR 头部项目适用于整个结果集 | P3 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-007 主程序与 Unix 域套接字连接术语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-008 相同连接目标和连接名说明共用译文 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-009 DECLARE STATEMENT 的标识符及兼容性用语 | P3 | — | — | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-010 预备语句术语与动态执行说明 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-011 PG14 起字符串字面量与参数占位符说明 | P3 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-012 需要提交时显式 COMMIT 的自动提交说明 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-013 SET DESCRIPTOR 头部和编号数据项的区别 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-014 VAR 指定类型及 WHENEVER 条件动作的准确措辞 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-015 关闭连接、声明游标及 while 循环的可见注释 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-016 SQL 命令总引言的复用范围 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-SQLREFS-017 PG10 DISCONNECT DEFAULT 及 SET CONNECTION DEFAULT 语法 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-018 PG11 起 DO CONTINUE 与 PG14 起 ASENSITIVE 和 DECLARE STATEMENT | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-019 PG10—13 描述符头部多项目与 PG14 起单项目语法 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-020 PREPARE 各版参数名、C 字符串及 PG14 起转义注意事项 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-021 固定英文 GET DESCRIPTOR 行数示例与 COUNT 实现不一致 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-SQLREFS-022 固定英文 WHENEVER NOT FOUND BREAK 缺 DO | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-SQLREFS-023 ecpg-sql-allocate-descriptor 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-024 ecpg-sql-connect 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-025 ecpg-sql-deallocate-descriptor 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-026 ecpg-sql-declare 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-027 ecpg-sql-declare-statement 全部语法、参数、示例和兼容性 | CHECK | — | — | — | — | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-028 ecpg-sql-describe 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-029 ecpg-sql-disconnect 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-030 ecpg-sql-execute-immediate 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-031 ecpg-sql-get-descriptor 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-032 ecpg-sql-open 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-033 ecpg-sql-prepare 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-034 ecpg-sql-set-autocommit 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-035 ecpg-sql-set-connection 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-036 ecpg-sql-set-descriptor 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-037 ecpg-sql-type 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-038 ecpg-sql-var 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-SQLREFS-039 ecpg-sql-whenever 全部语法、参数、示例和兼容性 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |

十一版新快照与当前完整命令节、固定英文及上游解包英文精确一致。94 条结构提示逐项绑定 100 个已读条目，范围内零未决、零漂移。原始整书退出码 PG10—12 为 3、PG13—20 为 1，不能据此宣称全书验收。ECPG 全章对账继续，最终 33 项 HTML/A4/US 构建未完成。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-sqlrefs-full-issue-version-matrix.json)、[全部完整命令页](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-sqlrefs-full-parent-plans.json)、[代码证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-sqlrefs-full-raw-proof.json)、[固定源码证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-sqlrefs-pinned-source-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-sqlrefs-native-validation.json)、[提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-sqlrefs-native-classification.json)。
