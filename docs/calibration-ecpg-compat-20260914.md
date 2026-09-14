**PG10—PG20：ECPG 兼容模式与内部机制校准结果**

Informix/Oracle 兼容部分完整对照 87 个条目变体、17 个外层段落变体和 7 个框架；内部机制完整对照 18 个外层段落变体、1 个框架和 6 个完整条目。十一版覆盖 87 个节范围、869 个条目和 2623 个文本段；71 个修订稿变体及 15 个精炼稿均已复读。PG10 尚无 Oracle 兼容节，已以完整原文核实不适用。

主要修复：十一版 ECPGdo 的参数数量是可轻易达到约 50 个，原译错误设置了上限；decimal 类型名及加法含义被误译；rfmtlong 应为每三位一组；日期错误说明存在“自如穿”笔误。预处理指令前的空白限制、string 的尾随空格、SQLDA 字段、NULL 指针、返回缓冲区及数组偏移也逐版校准。十一版固定源码的 SQLDA 分配函数及 rtrim 分支均已完整核对，修正了释放主结构及去除尾随空格的注释。

561 个程序、签名和输出块逐版核准，改动限于 22 处已列明的可见 C 注释；14 处原有箭头实体拼写和 33 处内联标记差异逐项保留。deccmp 参数名、SQLDA 示例及 intoasc 格式等英文疑点单列，未擅改代码，也未声称运行过示例。修＝修复或统一，核＝本项原本正确，—＝不适用，源疑＝保留原文疑点；341 格包含回归检查，不是独立缺陷数。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-COMPAT-001 $ 与后续预处理指令之间禁止空白的条件 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-002 decimal 加法错译为添加且类型名被翻译 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-003 复制、ASCII 转换及乘减运算保留 decimal 类型 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-004 日期错误说明的字符串笔误 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-005 ECPGdo 约 50 个参数并非最大数量 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-006 SQLDA 只需释放主结构的注释含义 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-007 rfmtlong 每三位一组并非三位数组 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-008 string 伪类型去除尾随空格的语义 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-009 C 主程序与兼容范围和不能直接替代的条件 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-010 Informix SQLDA 标题及结构体字段 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-011 NULL 指针、指示符数据及参数查询类型 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-012 sqlda.h 是头文件 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-013 decimal 舍入规则及输出缓冲区失败条件 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-014 C 类型及转换目标的准确表达 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-015 日期时间转换中的 date 与 timestamp 变量 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-016 日期错误和 numeric 无效值的条件 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-017 Oracle 字符数组填充和空字符串指示 | P3 | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-018 内部参数的类型符号和数组元素相对偏移 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-019 完整引导句、返回缓冲区和相同英文的译文统一 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-COMPAT-020 两种 Informix 模式及缺失的 FREE cursor 语句 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-021 SQLDA 链表、SQLSMINT、长度及未使用字段 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-022 算术操作数顺序、返回码、溢出及平台范围 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-023 日期格式、数组顺序、星期编号及既有八项联动修复 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-024 rfmtlong 格式字符、字符串与 NULL 接口 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-025 错误常量定义、数值符号及错误条件 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-026 Oracle 三条规则及 PG11 起文档范围 | CHECK | — | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-027 内部十参数排列、游标替换与带版本限定的完整示例 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-028 全部原始程序、签名与示例输出 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-COMPAT-029 英文 deccmp 将 arg2 写作 var2 的原文疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-COMPAT-030 英文 Informix SQLDA 示例的成员访问及格式实参疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-COMPAT-031 英文 intoasc 将 interval 格式写作日期时间的疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |

32 个完整父节与十一版新快照一致；162 条结构提示逐项绑定 174 个已读条目，范围内零未决、零漂移。原始退出码仍为 PG10—12 的 3、PG13—20 的 1，不能据此宣称全书检查通过。SQL 命令参考待应用，全书通读和最终 33 项 HTML/A4/US 构建继续。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-compat-full-issue-version-matrix.json)、[完整修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-compat-full-finalized-parent-plans.json)、[代码证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-compat-full-finalized-raw-proof.json)、[固定源码证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-compat-pinned-source-finalized-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-compat-native-validation.json)、[提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-compat-native-accepted-classification.json)。
