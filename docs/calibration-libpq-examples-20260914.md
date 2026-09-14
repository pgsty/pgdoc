**PG10—PG20：libpq 示例与章首校准**

从 PG18 起完整阅读三个示例，再核对五个英文框架变体、全部十一版中文程序和版本差异。修复 PG16—20 仍保留的 HAVE_SYS_SELECT_H 条件编译；PG19 查询与注释中的 SQL 大小写及多余 standard_conforming_strings 设置按本版英文恢复。保留旧版头文件规则、连接错误输出、字节串转义及各版输出。

41 个原有 C 注释变体均已翻译并复读，内嵌 SQL、输出、文件名和可执行代码单独校验。同步校准示例所在发行包的引言，并恢复 PG13 起章标题的 &mdash; 实体。另复读六个章框架和命令执行外层框架，统一五个共用引言段落。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-LQEX-001 PG16 起无条件包含 sys/select.h | P2 | 核 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 |
| C19-LQEX-002 PG19 查询示例 SQL 及注释大小写 | P3 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 修 | 核 |
| C19-LQEX-003 PG19 多余 standard_conforming_strings 设置 | P3 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 修 | 核 |
| C19-LQEX-004 程序原有可译注释 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQEX-005 示例所在源代码发行包的引言 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQEX-006 PG13 起章标题的上游 mdash 实体 | P3 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQEX-007 旧版连接失败输出与新版本差异 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQEX-008 各版示例字节串、转义与预期输出 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQEX-009 通知次数、事务和资源清理行为 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQEX-010 三个程序的接口、数组、消息与 SQL 顺序 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQOUT-001 章首 C 应用程序编程接口定义 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQOUT-002 底层应用接口与用户可见行为 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQOUT-003 章末示例及源代码发行包引言 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQOUT-004 头文件包含和库链接两项要求 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 核 | 修 | 修 | 修 |
| C19-LQOUT-005 连接建立后的命令执行引言 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |

这 15 个检查组包含措辞、已正确条件和本版差异，不能视为 15 个新增缺陷。示例与章首修订已纳入十一版全章新快照核验，代码有完整审定父块及专门的 33 个程序比对记录。`git diff --check` 通过；尚未执行最终 HTML/PDF 构建或示例运行测试。

证据：[全部程序比对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-examples-full-finalized-raw-proof.json)、[最终注释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-examples-full-finalized-comment-final-read.json)、[全章源码覆盖](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-whole-source-coverage.json)。
