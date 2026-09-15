PG10—PG20 本地化与字符集校准记录（2026-09-16）

从 PG18 的 258 个完整单元及外层框架开始，实际阅读十一版 charset.sgml、十种完整英文变体和所有中文候选，并核对 103 个完整相关范围。共涉及 93 个文件、114 个正文范围、1,404 叶段、221 父段、371 原始块。相关范围包括 SQL 语法、psql、pgbench、数据库模板、CREATE DATABASE、CREATE COLLATION、编码转换、JSON、information_schema 和发行说明。release-12.sgml 只核对一段非渲染源文注释，不代表通读该文件。

七类确认问题均横向检查十一版：

- CS001：PG14—20 的 libc 编码兼容约束多出“通常”，削弱了原文“只有一种字符集”的限制，已移除；PG10—13 原义正确。
- CS002：十一版普通 ICU root collation 概念改用已有“根排序规则”译法；实际 root／und 名称、BCP 47 标签与 SQL 字符串保留。
- CS003：十一版把复制数据库的约束写成“不能更改源数据库”。明确为“新数据库的编码和区域设置都必须与源数据库一致”，保留 template0 例外和本版示例。
- CS004：十一版 JOHAB 行补回 Hangul 限定，UHC 说明采用“统一谚文编码”；PG14—18 相关发行说明中的普通 Hangul 同步译为“谚文”，保留 U+11A7、TBASE、作者和本版提交链接。
- CS005：十一版编码表区分 Latin／Cyrillic 等文字系统与具体语言；采用“拉丁字母／西里尔字母”等已有译法。PG16—20 BCP 47 script-id 示例中的拉丁、希腊字母名称同步核准。俄语、乌克兰语、韩语等语言限定及实际编码标识符保留。
- CS006：PG10—12 将 SQL_ASCII 的未知编码含义误说成“不关心编码”，改为“承认自己不知道编码是什么”；PG13—20 已有正确解释，保留。
- CS007：PG16 level4 行混入 PG17 才有的 ka-shifted 脚注，依本版英文删除脚注及其一处链接。PG17—20 保留，PG10—15 无该表格。

修订 16 个正文文件、3 个规范文件。新增第 649—653 条 Cyrillic、Hangul、root collation、root locale 和 Latin 语境规则，复用既有稳定译法。规范共 653 条，旧规范前缀和九项用户回退保持。93 个涉及文件修订后再次核对，普通文字系统名称的已知错译残留为零。

相同英文在跨代码块、列表和行内标记后复用审定正文；191 个跨标记正文组、208 个常规叶段组、29 个父段组、493 个其他组均无未决冲突。保留两组已核准的句法／标记差异。28 个最终新文本组已实际复读：26 组与上一轮完整复读稿逐字相同，2 组是最后统一的 script-id 完整段落和表格单元。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-matrix.md)共 24 组、264 格：64 修复／复用、116 核准、45 不适用、34 例外、5 源文疑义。十一版 8,523 个中英文 SGML 文件中的 642 处相关命中全部归位：640 处绑定完整已读范围，2 处是中英文同一段非渲染发行说明注释。

371 个原始块均不变：364 个与自身英文逐字节相同，5 个 PG10—14 psql 输出只存在既有行尾空格，2 个 PG10 命令使用等价的 SGML replaceable 短结束标签。46 个既有本地 ID、24 处额外行内包装、25 处原文普通引号对应的中文 quote 标签及 6 个 domain → 域词汇链接已精确核准。全部代码、输出和语法均未运行。

逐版保留：非确定性排序规则从 PG12 起；提供程序小节从 PG15 起；ICU 名称、验证、比较级别和定制说明从 PG16 起；builtin 提供程序及 pg_c_utf8 从 PG17 起；PG_UNICODE_FAST／pg_unicode_fast 从 PG18 起；MULE_INTERNAL 到 PG18 为止；GB18030 的 2022 标签从 PG19 起。EUC_TW 的 1–3／1–4 字节数、默认转换属性、SQL_ASCII 的验证说明、UTF-8 与 C／POSIX／libc／ICU 的兼容限制、库链接和书名均依本版固定源文处理。LC_COLLATE 的“非 libc 时忽略”限定仅固定 PG19 有，PG20 无，保留差异。

CS-SQ01：PG16—20 kr 行的字符类别排序规则与 digit-currency-space 示例存在表面疑义，译文忠实保留英文，单独记录；这不算翻译缺陷，也未断言运行时行为错误。

新快照 checkpoint-charset-ready：十一版 14,280 配对节点，46 处范围内提示全部精确归位，零未决、零漂移、零未解释子节点差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。此项是解析核验，不是 HTML／PDF 构建。

前一规划器统计信息阶段已提交 b9748805，未推送。本批随后单独阶段提交，并继续管理数据库章节。历史原 2,466 待追溯单元上次核准 221、余 2,245，需在最终内容上重新对账；全书逐句校准、此前批次跨原始块及行内标记一致性复核、独立追溯和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-changes.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-all-occurrences-closure.json)、[跨标记分组](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-cross-markup-prose-groups.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-raw-proof.json)、[受保护值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-protected-proof.json)、[行内标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-existing-inline-wrapper-proof.json)、[引号上下文](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-existing-quote-context-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-version-boundary-proof.json)、[源文疑义](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-source-question-proof.json)、[术语复查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-post-apply-term-check.json)、[规范](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-norm-changes.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-native-validation.json)、[提示归类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/charset-full-reviewed-certificate.json)。
