PG10—PG20 ecpg 命令行参考校准记录（2026-09-14）

作为 ECPG 全章的关联核查，十一版 `ref/ecpg-ref.sgml` 已完整对照：3 个英文全文变体及全部 4 个中文候选、34 个共用文本族、352 个实际文本段、165 个内外条目和 22 个代码／命令语法块。全部 9 个修订稿变体已复读。

修订主要是与正文统一用语：include 文件和路径明确为包含文件及搜索路径，no_indicator 使用“指示符”，Notes 统一为“注意事项”，改顺 pg_config 查询安装目录的表述。PG10 的两种兼容模式、PG11 起 ORACLE、PG10/11 的 -D 形式以及 PG12 起可选值和默认 1 均以本版英文为准；缓存淘汰、显式事务例外、扩展名和编译示例原已正确，保留复核。

源码标识符、全部 ID、命令语法和示例未改。十一版原有的参数拼写 option 与 -r 语法一致，英文段落首词写作 Option，逐项记录为既有大小写例外；这不表示缺文或功能缺陷。下表修＝修订或统一，核＝原已正确，例＝已核实例外；121 格不是独立缺陷数量。

| 检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-CLI-001 include 文件、搜索路径与目录用语 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-CLI-002 no_indicator 与正文的指示符术语一致 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-CLI-003 Notes 及相同命令引导句一致 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-CLI-004 pg_config 查询当前安装目录的表述 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-CLI-005 输入输出默认扩展名及标准输入输出覆盖 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-CLI-006 PG10 两种兼容模式与 PG11 起 ORACLE | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-CLI-007 PG10/11 宏语法与 PG12 起可选值和默认 1 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-CLI-008 头文件扩展名及强制开启 -c | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-CLI-009 预备语句缓存、问号与显式事务例外 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-CLI-010 帮助、版本、编译链接及完整示例 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-CLI-011 保留与 -r 语法一致的原有 option 大小写 | 例 | 例 | 例 | 例 | 例 | 例 | 例 | 例 | 例 | 例 | 例 |

当前十一版文件、审定稿、新快照、固定英文及上游解包英文完全一致；105 条既有锚点提示逐项绑定完整条目，范围内零未决、零漂移。原始整书审计退出码保留 PG10—12 的 3、PG13—20 的 1。本批校准已闭合，全书阅读和最终 33 项 HTML/A4/US PDF 构建继续。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-cli-full-issue-version-matrix.json)、[完整英中修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-cli-full-file-plans.json)、[全部条目](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-cli-full-entry-proof.json)、[当前快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-cli-native-validation.json)、[逐项锚点核定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-cli-native-classification.json)。
