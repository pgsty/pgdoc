**PG10—PG20：ECPG 前五节校准结果**

已从 PG18 开始完整核对十一版的概念、连接、命令执行、主变量和动态 SQL 五节：152 个段落变体、10 个事务条目变体、21 个表行变体、1 个表框架、50 个节框架和 3 个章外框。实际覆盖 383 个节范围、1218 个外段、77 个事务条目、209 个表行及 737 个代码块。所有修改复读，程序、结果、标识符及本版结构逐项保护。

已修复 PG14/15 混入的 PG16 起 typedef 说明、十一版 char 数组被写成字符串、VARCHAR 为每个变量生成结构体的限定、为值加引号的含义和主语言标记缺失；另校准游标取行、complex 类型、指针自动分配及预备事务术语。保留旧版连接方式、bytea 引入范围、DISCONNECT DEFAULT 等版本差异。

下表 41 个检查组包含缺陷、措辞、原本正确项、版本差异与英文疑点，451 格不是 451 个缺陷。修＝已修或措辞校准；核＝本版原本正确；无＝本版无此内容；源疑＝英文自身疑点，保留并单列。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-FRONT-001 char[] 是字符数组 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-002 VARCHAR 为每个变量生成具名结构体 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-003 为值加引号不是引用值 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-004 补齐主语言 firstterm 标记与主客体关系 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-005 游标取行不是预取 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-006 PG14/15 混入 PG16+ typedef 行为 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-007 complex 类型名称与原本正确的复数释义 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-008 bytea 二进制零字节及收发转换 | P3 | 无 | 无 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-009 预备事务与预备状态术语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-010 动态 SQL 的预备与参数替换 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-011 声明写入输出 C 文件的含义 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-012 指针目标变量与自动内存分配 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-013 非简单类型与章节标题一致 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-014 连接名可省略 | P3 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-015 连接参数的 key=value 项 | P3 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-016 用户名和密码的 SQL 字符串常量 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-017 多连接三种方式与参数选项的区别 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-018 显式断开连接的编程习惯 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-019 多行结果集与逐行读取过程 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-020 预备语句适用条件的表达 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-021 DECLARE 与后端 OPEN 的执行时机 | P3 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-022 C 变量插入 SQL 的使用方式 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-023 主变量说明和相同英文译文复用 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-024 类型映射表标题与中文分隔符 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-025 既有 C 注释与嵌入式 SQL 可见索引 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-026 typedef 在 ECPG 中的索引 | P3 | 无 | 无 | 无 | 无 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-FRONT-027 PG10 DISCONNECT DEFAULT 与 PG11+ 列表 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-028 两种与三种连接管理方式的版本界线 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-029 连接目标解析及 unix 主机名的版本变化 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-030 每个线程连接的并发访问限制 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-031 自动提交默认关闭与事务块例外 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-032 SQL 类型到 C 类型、bytea 版本与脚注 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-033 指示符正负零及 no_indicator 的空串最小值 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-034 数组和复合类型的逐元素读取及变通方案 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-035 EXECUTE IMMEDIATE 无结果集及 EXECUTE 子句组合 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-FRONT-036 固定英文 create_complex 示例的类型与字符串拼写疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-FRONT-037 固定英文读取示例 test1/test 和 VARCHAR 声明疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-FRONT-038 固定英文指示符示例 END DECLARE SECTION 冒号 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-FRONT-039 固定英文结构示例把 typedef 名称称为变量 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-FRONT-040 固定英文数组示例循环八次却列七行输出 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |
| C19-ECPG-FRONT-041 固定英文 SQL 数组可直接映射与后段限制的关系 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |

十一版新快照解析完成，当前中文、审定稿、固定英文、解包英文及快照精确绑定。34 条原生提示已逐条匹配 40 个完整已读节点：28 个既有中文 ID、6 组匿名 typedef/指针小节；范围内零未决、零漂移。`git diff --check` 通过。这是前五节的核验结果，ECPG 后续各节、全书通读和最终 33 项 HTML/A4/US 构建仍未完成。

英文示例的 test1/test、声明结尾冒号、数组输出行数、复合类型函数拼写等六类疑点均保留本版原文，并有十一版记录；不计为中文缺陷，也未声称运行这些示例。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-front-full-issue-version-matrix.json)、[完整修改与阅读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-front-full-finalized-parent-plans.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-front-native-validation.json)、[34 条提示逐项处理](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-front-native-classification.json)。
