**PG10—PG20：ECPG pgtypes 与相关兼容接口校准结果**

完整阅读 pgtypes 全节的 61 个接口条目变体、14 个外层段落和 9 个节框架，以及 8 个相关 Informix 接口的 13 个条目变体；全部十一版共覆盖 99 个 pgtypes 节范围、616 个条目、550 个表行和 3432 个文本段，另有 88 个完整兼容接口及 429 个文本段。94 个修订稿变体和 17 个后续精炼/关联变体已复读，561 个程序与函数签名字节保持不变并逐一核对本版英文。

主要修复：十一版时间戳减去时间间隔的运算方向译反、日期指针所指变量的设置目标、%G 的年份定义；PG13—20 的 %e 漏掉“一个月中的日”；PG14—20 日期解析示例的两条英文输入误被翻译；PG14—16 混用了 PG17 起的 numeric_to_long 文档。另校准字符串表示、MDY、类型名称、格式说明符、内存与返回值说明，并同步相关兼容接口。

版本边界经源码澄清：numeric_to_long 的下溢处理在全部十一版实现中都已存在，PG17 起只是这段英文文档补明下溢，不能称为新功能。PGTYPEStimestamp_to_asc 首句把 timestamp 写成 date，经全部十一版声明、实现与同一条目签名核实，修正 PG10—13 译文，保留 PG14—20 已有订正。示例中传入 &tsout 等英文自身问题另列，不擅改示例，也不声称已运行。

下表 34 个检查组包含缺陷、措辞、回归、版本差异和源文问题。374 格不是 374 个独立缺陷；修＝修复或措辞校准，核＝原本正确，源码核实＝有逐版声明/实现证据的英文笔误订正，源疑＝保留本版原文并记录疑点。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-PGTYPES-001 时间戳减去时间间隔的方向译反 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-002 PG14—16 混用 PG17 起的 numeric_to_long 文档措辞 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-003 日期解析的英文输入字符串不可翻译 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-004 设置日期指针所指变量及 rtoday 同步说明 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-005 %G 为该周多数天所在年份 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-006 %e 漏掉一个月中的日 | P2 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-007 字符串表示误译成字符串词元 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-008 MDY 格式及变量误译成变体 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-009 date_mdyjul 与 rmdyjul 避免错误暗示数组元素顺序 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-010 日期和格式掩码是输入、指针所指值是输出 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-011 %j 为一年中的第几天 | P3 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-012 格式掩码与格式说明符的关系 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-013 本地化月份独立形式及 POSIX 区域设置 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-014 空格填充、零填充以及 UTC 偏移 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-015 格式说明符的值、范围和起始星期 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-016 numeric 和 decimal 的分配释放及精度 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-017 保留 C 与 SQL 的类型名称 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-018 interval 类型与错误消息语境 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-019 日期表的描述性标签与真实字面输入区分 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-020 char 指针、完整字符串解析及 endptr | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-021 日期示例引导、逆函数及 errno 双重检查 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-022 相关 Informix 日期与时间接口共用译文 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-PGTYPES-023 PGTYPEStimestamp_to_asc 的 date 笔误经十一版声明和实现核实 | EXCEPTION | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 | 源码核实 |
| C19-ECPG-PGTYPES-024 numeric 加减乘除、复制及比较的方向与返回值 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-025 numeric 与 decimal 转换的溢出差异 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-026 日期格式表、输出与内存释放责任 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-027 时间戳解析忽略时区、错误常量与默认掩码 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-028 timestamp 差值与 interval 复制的目标内存 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-029 errno 错误码和有效哨兵值的双重条件 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-030 旧英文未说明下溢，但旧实现已经处理下溢 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 核 | 核 | 核 | 核 |
| C19-ECPG-PGTYPES-031 英文示例给按值接口传入 &tsout | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-PGTYPES-032 英文 MDY 假定与 01/02/03 结果的疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-PGTYPES-033 英文格式说明中的 $_* 拼写疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-PGTYPES-034 主变量堆分配段与库支持栈分配的语境边界 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |

十一版新快照解析完成，当前中文、审定稿、固定/解包英文和新快照精确一致。93 条提示逐一绑定 203 个完整已读节点：82 个既有本地 ID 和 11 组重复日期格式键（121 行）。范围内零未决、零漂移。68 个文本级保护标记差异分别核实为三种描述性日期标签的翻译和原有 char* 类型标记，没有按类别整批豁免。正文差异检查通过。ECPG 其他各节、全书通读和最终 33 项 HTML/A4/US 构建仍未完成。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-pgtypes-full-issue-version-matrix.json)、[十一版源码证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-pgtypes-pinned-source-proof.json)、[最终修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-pgtypes-full-finalized-parent-plans.json)、[原生精确核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-pgtypes-native-validation.json)、[93 条提示处理](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-pgtypes-native-classification.json)。
