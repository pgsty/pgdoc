**PG10—PG20：ECPG 预处理、编译、库函数、大对象及 C++ 校准结果**

五节完整对照 47 个外层段落变体、13 个条目变体、12 个框架及全部代码和输出。十一版共覆盖 110 个节范围、88 个条目和 864 个文本段；27 个修订稿变体与两个可见索引译文已复读。242 个代码块逐版核准，只改每版五处可见 C 注释，另保留七处有精确证据的原有箭头实体拼写。

主要修复：PG14—20 C++ 引言遗漏 extern "C" 头文件声明整句；十一版 ECPGdebug 的 stream 参数名被误译，头文件中的声明被写成定义；PG12+ 漏掉每个输入文件开始时的宏初始状态；PG13+ 条件编译示例应只编译三个命令中的一个。文件包含、目标文件、变量作用域、局部变量和可见索引也按共同语义校准。

原文大对象示例的事务、CDATA 字面内容和 Oid 比较，以及 C++ 示例的 Test/TestCpp 类名疑点单列，代码按固定英文保留，未声称运行过示例。下表包含缺陷、措辞、回归检查与原文疑点；修＝修复或统一，核＝本项原本正确，—＝不适用，源疑＝保留原文疑点。253 格不是独立缺陷数量。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-TOOLCHAIN-001 C++ 引言缺失 extern "C" 头文件声明整句 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-002 ECPGdebug 参数名 stream 被误译 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-003 头文件中的声明误译为定义 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-004 每个输入文件开始时的 DEFINE/UNDEF 初始状态 | P2 | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-005 条件示例只编译一个 SET TIMEZONE 命令 | P2 | — | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-006 ECPG 与 C 预处理文件包含及大小写区别 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-007 条件编译备选区段及 PG13 起说明 | P3 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-008 头文件搜索路径与库链接的准确用语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-009 直接调用 libecpg 函数的可移植性限制 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-010 事务状态返回值及各版自己的链接 | P3 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-011 C++ 主变量作用域和局部变量 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-012 C 与 C++ 目标文件和编译器驱动程序 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-013 大对象示例五处可见 C 注释 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-014 C++ 可见索引 with ecpg | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-TOOLCHAIN-015 文件包含的目录顺序与 .h 回退条件 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-016 宏替换阶段、命令行 -D 与版本专属条件指令 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-017 编译选项、工具命令、make 规则和线程支持 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-018 Windows 调试流限制、连接句柄与状态 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-019 大对象连接获取及事务要求原文 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-020 完整 C/C++ 示例、命令和输出对应原版 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-021 原有 t-&gt;test() 实体等价拼写 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-TOOLCHAIN-022 英文大对象示例的事务及字面代码疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-TOOLCHAIN-023 英文 C++ 示例 Test 与 TestCpp 类名不一致 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |

55 个完整父节与十一版新快照精确一致，16 条结构提示逐项绑定已读条目的既有 ID，范围内零未决、零漂移。原始退出码保留 PG10—12 的 3、PG13—20 的 1，不表示全书检查通过。ECPG 余项、全书通读和最终 33 项 HTML/A4/US 构建继续。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-toolchain-full-issue-version-matrix.json)、[完整修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-toolchain-full-finalized-parent-plans.json)、[代码证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-toolchain-full-finalized-raw-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-toolchain-native-validation.json)、[提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-toolchain-native-classification.json)。
