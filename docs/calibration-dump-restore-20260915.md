PG10—PG20 转储与恢复工具全文校准记录（2026-09-15）

十一版 pg_dump、pg_restore、pg_dumpall 共 33 个参考文件已完成同版中英全文核对。以 PG18 为入口，先读 pg_dump/pg_restore 的 144 块和 pg_dumpall 的 62 块，再读 30 组完整英文变体及各自中文候选；另读 26 组关联内容与 14 组美元引用补充范围。总计绑定 170 文件、370 范围，其中 337 个为关联完整单元；修改 49 个正文文件及 3 个规范文件。

- PG14—17 三个工具页移除 107 个不属于本版的选项条目，涉及统计信息、过滤文件、表访问方法、子表选择、sequence-data、transaction-size 等版本边界。所有选项均以自身英文清单为准；例如 exclude-extension 从 PG17 开始存在，PG17 pg_restore/pg_dumpall 的 filter 仍在短选项后，不能照搬 PG18 顺序。
- PG14/15 恢复 blobs 别名、compress 的 0–9 参数和旧 gzip 压缩说明；PG14—16 删除未来过滤文件示例；PG14—17 恢复旧 ANALYZE 建议。PG10—17 的 data-only、schema-only、触发器说明也有未来统计信息语义串入，已逐段恢复本版内容。
- 校准各版本最低可导出服务器版本、unlogged 表与序列的不同适用范围、统计收集器与累积统计系统名称。PG13 起补丁版已有的安全警告、restrict-key 和 psql -X 按固定英文保留，不误判为未来内容。
- 十一版修正 tar 格式说明中遗漏的“使用”、多个排除模式匹配任意一个即可的条件、binary-upgrade 不建议且不受支持的关系，以及对函数体使用美元引用的对象。同步快照保留本版“可能导致”限定；分区根对象的 text 类型按本版原文核准。
- pg_restore 十一版明确恢复到“以记录名称命名的数据库”，校准 row_security 的 off/on 条件；归档格式“不必显式指定”、普通 table 与键的译法也按原文修订。PG19/20 恢复外键条款中“被选中进行恢复”的限制；PG19 依赖选择说明恢复到本版位置。
- 将 dollar quoting 的 44 处普通术语变体统一为“美元引用”，补充第 643 条语境规则，保留美元符号、定界符、标签、选项与代码。PL/pgSQL 的 format() 说明明确假定对整个函数体使用了美元引用；PG10—14 发布说明按自身英文重写 walsender 失败的三个条件和错误恢复后果。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-matrix.md)含 49 个问题与检查组、539 格：235 格修复、196 格本项语义原已正确、100 格不适用、8 格保留固定英文疑点。15 种未来选项分别列组；检查格与结构条目数均不是独立缺陷数。

完整范围包含 3,598 个叶段落、319 个嵌套父段落和 545 个代码/语法/输出块。134 组最终修订文本已复读；451 个同源叶段组、33 个父段组和 198 个其他文本组没有未处置的语义分歧。7 组既有等价形式保留，包括行宽换行、GRANT/REVOKE 大小写和标记，以及工具自身对象上下文差异。

370 个范围的受保护元素及链接属性已核准。7 个范围保留自身原有的 14 个 GRANT/REVOKE 标记；545 个原始块按自身英文核对。移除未来选项随之删除的 107 个定制 ID 已在各版本全部中文 SGML 中确认无入链；33 个完整工具页的选项顺序均与自身英文一致。删块留下的新增纯空白行定点清理，既有格式保留。

PG17—20 pg_restore 的 filter 英文使用 --indexes，而实际定义及固定 C 源码使用 --index；该固定英文疑点单列保留。另一处“每行一个数据库模式”与下方列出的对象类型不一致，中文保留符合自身子条目的对象描述；不能与 pg_dumpall 的数据库模式段机械合并。PG17—19 C 文件来自核准 SHA256 的发布包，PG20 来自固定提交工作树，相关选项与解析分支已逐行读过。这是静态源代码核对，不是运行时测试。

新快照 checkpoint-dump-restore-ready 完成十一版准备、解析与对齐检查。12,451 个节点与审定范围精确绑定，范围内 1,266 条提示逐项核准，零未决、零漂移、零子节点数量差异。当前中文、审定稿、新快照以及固定英文与解包英文均一致。原始全书审计的非零退出码保留，本报告只关闭本批实际读过的范围。

COPY 阶段已提交 26ac7f5。转储与恢复批次准备阶段提交；全书余项、历史独立对账和十一版 HTML/A4 PDF/US PDF 共 33 项最终构建仍未完成，最终构建验收为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-raw-proof.json)、[受保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-protected-proof.json)、[选项顺序](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-option-order-proof.json)、[删除 ID 入链](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-removed-id-reference-proof.json)、[固定 C 源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-fixed-filter-source.json)、[规范](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-norm-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/dump-restore-full-reviewed-certificate.json)。
