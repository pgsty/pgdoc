**PG10—PG20：ECPG 错误处理全节校准结果**

完整对照 52 个条目变体、21 个外层段落、4 个节框架及 8 个代码与输出变体。十一版共覆盖 44 个节范围、560 个条目和 867 个文本段，27 个修订稿变体和 1 个术语精炼变体已复读。88 个代码与输出块逐版保持原样；IGNORE 区域和不可见注释也逐一核对保留。

主要修复：sqlwarn 限定的是其余元素；SQLSTATE 代码大多由 SQL 标准定义；描述符错误遗漏“索引”或“条目”；空值指示符遗漏“变量”；sqlwarn[1] 表示已经发生的截断。数值主变量的 numeric 是通用数值含义，不能误限为 numeric 类型，已核对十一版 get_int_item/get_char_item 的 22 个固定源码函数。还校准 WHENEVER 按源代码顺序生效、库版本兼容关系及 SQL 通信区域等术语。

PG10 没有 DO CONTINUE，保留自己的动作清单；PG11+ 对 SQL CALL/DO 的说明按本版保留。下表包含实质缺陷、措辞和回归检查，220 格不是独立缺陷数。修＝修复或统一，核＝本项原本正确，—＝本版不适用。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-ERRORS-001 sqlwarn 其余元素的限定范围 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-002 大部分 SQLSTATE 代码由 SQL 标准定义 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-003 描述符索引超出范围遗漏索引 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-004 无效描述符条目遗漏条目 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-005 主变量数值类型不限定为 numeric 类型 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-006 空值指示符变量的准确对象 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-007 sqlwarn 指示已经发生的截断 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-008 预处理器与库版本不兼容的关系 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-009 SQL 编码方案、通信区域和字段术语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-010 已预备语句与描述符错误的用词 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-011 WHENEVER 指令按源代码顺序生效 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-012 DO CONTINUE 的循环起点和 PG11 起版本范围 | P3 | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-013 回调函数与 SQL CALL/DO 的 PG11 起说明 | P3 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-014 适用条件、错误列表引导、无效与标点 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-ERRORS-015 错误警告无数据三种条件、默认动作和退出状态 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-ERRORS-016 线程局部 sqlca、副本、最后错误和错误码正负 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-ERRORS-017 SQLCODE 数值符号、SQLSTATE 和类型转换方向 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-ERRORS-018 数值代码与 SQLSTATE 多对多及可移植性限制 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-ERRORS-019 忽略区和注释中的非可见错误项保持原样 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-ERRORS-020 WHENEVER 和 sqlca 完整示例原程序及输出 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |

十一版新快照与审定正文精确一致，98 条结构提示均以完整已读条目的既有 ID 证据核定，范围内零未决、零漂移。原始退出码保留为 PG10—12 的 3、PG13—20 的 1，不表示全书检查通过。ECPG 其余各节、全书通读与最终 33 项 HTML/A4/US 构建继续。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-errors-full-issue-version-matrix.json)、[完整修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-errors-full-finalized-parent-plans.json)、[数值类型源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-errors-numeric-source-proof.json)、[原生精确核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-errors-native-validation.json)、[98 条提示绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-errors-native-classification.json)。
