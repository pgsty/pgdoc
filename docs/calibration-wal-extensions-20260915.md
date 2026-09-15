PG10—PG20 WAL 扩展与归档模块全文校准记录（2026-09-15）

从 PG18 的 WAL 扩展、自定义资源管理器、归档模块、basic_archive、basebackup_to_shell 全文开始，完整阅读 14 个分块、11 个英文全文变体与全部中文候选。PG15—20 四类文件及 PG17—20 上级包装共 28 个完整文件；另精确继承本轮刚完成的 PG10—14 五个通用 WAL 全文对照，核准 83 个关联范围，其中包含六版完整 archive_library 参数项。共 73 文件、116 范围、33 个完整文件范围，修订 8 个正文文件。

- PG15/16 自定义资源管理器仍是独立 chapter，将误称本节修为本章。PG17 起自身是 sect1，保留本节。
- PG15—20 归档初始化段明确库基名是 archive_library 指定的名称，避免误读为参数名称本身。
- PG16 归档回调段误入后续版本的或者抛出错误，按对应英文删除；PG17 起本版原文已有该说明，保留。这一文档差异不能用于推断旧版运行时错误处理不支持重试。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-matrix.md)列出 18 个问题与检查组、198 格：9 修复、105 本项已正确、84 不适用。PG10—14 的接口不存在性结合了完整旧通用 WAL 对不能注册自身 redo 的明确规定、固定源树文件和引用清单，以及 PG15 发布说明的新接口和此前仅支持归档命令说明；PG15/16 没有上级包装文件，但两类独立章节仍然存在。

完整核准资源管理器回调字段、描述函数职责、ID 注册和持续加载要求；归档回调的配置检查、成功回收、失败重试及状态清理；基础归档目录、临时文件与重试；备份到 shell 的命令、角色、占位符和 detail 限制。PG15 的初始化函数填写传入结构，PG16 起返回常量结构指针并增加启动回调和状态参数；错误明细宏与短期内存上下文说明则按 PG17 起的本版文本保留。

关联阅读包括归档参数、备用机共享归档、备份停止等待、WAL 保留与软限制、发布说明和表访问方法。PG15 的归档库可以覆盖归档命令，PG16 起两项同时设置报错；basic_archive 的复制需要目录存在，与维护版本允许目录启动时暂不存在的修复并不矛盾。均保留本版条件，没有据文档补入时间推断实际 API 首次可用版本。

355 个叶段落、51 个嵌套父段落、53 个原始块逐版核准，7 组最终修订文本完整复读。86 个同源叶段组、12 个父段组、29 个其他单元组没有未决冲突。116 范围受保护元素与链接匹配；仅 PG15/16 原有 shared_preload_libraries 的 varname 包装按完整未改动段落单列，保持既有合法标记。没有新增术语规则。

新快照 checkpoint-wal-extensions-ready 完成十一版准备、解析与对齐，883 节点精确绑定，范围内 5 条提示逐项核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，此结论只覆盖列明范围。

前一阶段通用 WAL 与表访问方法提交 a02546d 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-version-boundary-proof.json)、[旧版完整原文继承](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-inherited-full-read.json)、[不存在性依据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-absent-version-proof.json)、[完整参数项](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-library-parameter-scopes.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/wal-extensions-full-reviewed-certificate.json)。
