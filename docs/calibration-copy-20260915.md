PG10—PG20 COPY 与 file_fdw 全文校准记录（2026-09-15）

十一版 COPY 参考页与 file_fdw 全文已完成同版中英核对，以 PG18 为入口，读取 COPY 的 15 个完整子节/框架及 10 个全文变体，file_fdw 的 2 个完整子节/框架及 9 个全文变体，包含所有中文候选。另读 36 组关联内容与 20 组补充全文范围，覆盖 psql 的完整反斜线 copy 定义、协议三种响应的全部五个字段、libpq 接口和发布说明。最终绑定 77 个文件、172 个范围，其中 22 个为完整文件，150 个为关联完整单元；修改 24 个正文文件，规范未变。

- PG14—17 的 COPY 语法和选项恢复本版边界：PG14/15 没有 DEFAULT；PG14 没有 HEADER MATCH；PG14—16 没有 FORCE_NOT_NULL/FORCE_NULL 星号、ON_ERROR 或 LOG_VERBOSITY。PG17 保留自己的错误处理选项，移除未来 REJECT_LIMIT 和 silent。PG15/16 查询参数移除未来 MERGE，PG14—16 恢复遇第一处错误停止及空间回收说明。
- PG14—17 恢复本版 FREEZE 条件、FORMAT 定义、文本结束标记的旧协议上下文及 CSV 反斜线点说明，移除 PG18 才有的 CSV 兼容性注解；PG14/15 的 PROGRAM 段落按自身英文恢复。PG14—17 原有合法格式标题 xreflabel 保留。
- file_fdw 中，PG14 移除未来 default 和三个错误处理选项；PG16 保留 default，移除未来错误处理选项。两版均移除 PG17 才出现的列选项示例。PG15 原已正确，PG17—20 保留自身选项；PG19/20 的 header 整数及布尔形式逐版核准。
- 十一版修正命令标签输出的逻辑条件，明确“既不是 A，也不是 B”；backslashed character 改为前面加反斜线的字符。二进制头部的固定字段、标志字段术语，以及长度字后跟随字段数据的说明同步修订，原始字节、位编号和输出保持同版值。
- PG14—20 校准 CSV 文件包含带引号多行值的主客体；PG10—13 原译正确。PG17—20 的错误通知中，line 明确为行号。PG19/20 进一步明确消息列出的列名对应“值被替换为 NULL”的列。
- PG18 发布说明修正为给 file_fdw 添加 on_error 和 log_verbosity 两个选项；silent 抑制的是被丢弃输入行的相关消息。PG19 发布说明修正 SIMD CPU 指令与 COPY FROM 输入性能的修饰关系。三个原始提交链接在十一版本版发布文件中逐一搜索，其他版本没有同一条目，不回填。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-matrix.md)包含 32 个问题及检查组、352 格：95 格修复、196 格本项语义原已正确、47 格不适用、14 格保留固定英文疑点。它同时记录历史 OID、WHERE、生成列、null/空字符串、权限和编码等原本正确的版本边界，不将所有检查格计作缺陷。

共核对 1,601 个叶段落、168 个嵌套父段落，以及 173 个代码/语法/输出块。58 组最终修订文本已复读。248 个同源叶段组、20 个父段组、98 个其他文本组没有未处置的语义分歧；2 组既有等价行内标记保留。172 个范围的受保护元素和 linkend/endterm/zone/arearefs/url 属性均核准，14 个范围只保留自身原有的 SELECT/INSERT/NULL/TRUE/verbose 行内标记。PG14 三种协议响应的透明外层 para 包装差异经完整消息核对后保留，全部五个字段均存在。

删除未来选项时随之移除的 12 个旧版本地 ID，已在各版本全部中文 SGML 中确认没有入链。相应未来链接按本版英文删除，其余定位属性保留。差异检查发现六个文件新增了纯空白行；这些由删块留下的行尾空格已清理，原有空白未扩大调整。

错误通知的行号与列值语义额外核对了 PG17—20 固定源代码 copyfromparse.c：PG17—19 来自已固定 SHA256 的发布包，PG20 文件与固定提交 86f7c82cf1023e3599f40f939727791a7090cd44 的 blob 相同。这是源代码核验，不是运行时测试。固定英文二进制头部“15 字节”与后文 11+4+4 的疑点，以及 PG18—20 COPY TO 对继承子表的概括疑点，单列保留；没有自行改写固定英文数字或命令行为。

新快照 checkpoint-copy-ready 完成十一版准备、解析和对齐检查。4,783 个节点与审定内容精确绑定，范围内 244 条提示全部逐项核准，零未决、零漂移、零子节点数量差异。当前源文件、审定稿、新快照及解包后的固定英文一致。原始全书审计及其非零退出码完整保留，本报告仅关闭本批已读范围。

SQL 语法阶段已提交 bd541e0。pg_dump/pg_restore 全文从 PG18 继续；全书逐段语义校准、历史独立对账和十一版 HTML/A4 PDF/US PDF 共 33 项最终构建仍未完成，最终构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-reread-proof.json)、[代码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-raw-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-protected-proof.json)、[删除 ID 入链检查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-removed-id-reference-proof.json)、[固定 C 源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-fixed-source-context.json)、[PG20 固定提交核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-fixed-pg20-source-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/copy-full-reviewed-certificate.json)。
