PG10—PG20 amcheck 与 TOAST 语境校准记录（2026-09-15）

从 PG18 的完整 amcheck 模块开始，阅读 9 个分块、10 个全文变体及全部中文候选。关联发行说明扩展到完整条目，共阅读 104 组；另读命令参考页 2 组索引／概要和 2 组完整页头。补查 TOASTed 及 acronym 标签拆分形式，阅读 12 组完整段落；PG14 协议中的 Byte1('u') 条目单独按原始标记精确核对。合计 11 完整模块文件、313 关联范围，涉及 115 文件、324 范围。

本批修订 79 正文文件与 3 个规范文件，确认并修复八类问题：

- AMC001：PG15 混入未来的 gin_index_check 完整条目，按自身英文删除；PG18—20 保留。PG18 完整发行说明的引入条目也已核对。
- AMC002：PG14—15 amcheck 章节混入新版 search_path 说明，恢复自身英文范围；PG17—20 保留该段。旧版完整发行说明中的修复仍然保留，不能把正文新增时间当作底层行为变更时间。
- AMC003：PG17 文件系统／存储子系统故障说明未译，补译后与其他同源版本统一。
- AMC004：十一版把“不应是误报”写成“不要当作误报”，恢复对错误性质的原始判断；同时补回被代词替代的 amcheck 标记。PG10 自身额外的软件／硬件比较句保留。
- AMC005：PG14—20 对备份恢复工具的说明遗漏 faulty，补齐“有缺陷且设计欠妥”。旧版没有该段。
- AMC006：统一十一版 toasted、TOASTed 和由 SGML 标签拆分的形式，沿用“经过 TOAST 处理”。涉及模块、协议、类型定义、逻辑复制、存储、EXPLAIN 和完整发行说明，保留所有实际错误消息、函数宏和代码。
- AMC007：PG14—20 父索引检查说明省略函数名标记，补回；PG10—12 同步补齐一般错误惯例的措辞。PG13 原已完整。
- AMC008：PG14 三部分名称模式说明将错误写成警告，按英文及固定 PG14.24 的 pg_dump／psql 源码恢复“报错”；只读验证了 fatal 和 pg_log_error 路径，没有执行数据库操作。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-matrix.md)共 16 组、176 格：51 修复／复用、100 核准、21 不适用、4 原文疑点格。49 组最终译文已复读；837 叶段落、19 嵌套父段落、26 个原始块及 324 个保护标记范围核准。218 个同源叶段组、4 个父段组和 42 个其他单元组无未决冲突。

逐版保留函数演进：heapallindexed 自 PG11、rootdescend 自 PG12、调试提示自 PG13、verify_heapam 自 PG14、序列说明自 PG15、扩展标题自 PG16、checkunique 与章节 search_path 说明自 PG17、gin_index_check 自 PG18。这里记录的是固定文档中各项出现的边界；各版锁级别、热备限制、父子链接检查位置、CREATE INDEX 与 CREATE INDEX CONCURRENTLY 的区别均按自身文本保留。

完整核对近似验证的临时汇总结构、每元组约 2 字节内存与不超过 2% 的漏检概率、maintenance_work_mem 限制、重新检测机会以及关系锁不变；堆检查的停止条件、TOAST 风险、跳过全可见／全冻结块、起止块边界、四列输出和诊断限制均已核准。保留损坏存在与不存在、数据页校验和与逻辑一致性之间的区别。

933 处相关源标记出现位置全部精确绑定：922 处落在完整已读正文范围，11 处为 contrib 中的实体包含引用，逐版核对 SYSTEM 声明指向完整已读模块。大小写补查新增 141 处，其中包含旧版 SGML 短结束标签形式。没有将整个 contrib 包装文件或整本协议算作本批已读。

22 处 application 标签内的校验和描述是普通概念，既有中文译文逐项核准；所有实际应用名称保持原样。26 个原始块中，PG11—13 三个 ASCII 表头仅有原有行尾空格差异，其余与自身英文完全一致。两处属性删除仅随 PG14—15 的未来说明移除；其余属性和全部源注释保持。PG10—13 固定发行说明在工具引入前提到 pg_amcheck，四版原文疑点保留，未当作中文错误删改。

新增术语规则第 646 条 toasted → 经过 TOAST 处理，覆盖大小写及标签拆分形式，保留实际错误消息和标识符；不把 TOAST 处理一律等同于压缩或行外存储。词表与规则各 646 条，既定九项用户回退保留。

新快照 checkpoint-amcheck-ready 完成十一版准备和解析；1,856 个节点精确绑定，9 条范围内提示全部核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，本结论仅覆盖列明范围。

补读关联 ALTER TYPE 段落时，确认 PG13—20 的索引副词条 per-type storage settings 仍为英文；已逐版核对，作为紧接本批的修复项登记，不计为本批已修复。

上一阶段元组检查提交 8eb3d80 已核验，本批准备阶段提交。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-protected-proof.json)、[描述标签](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-descriptive-label-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-all-occurrences-closure.json)、[包含引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-source-inclusion-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-source-questions.json)、[错误级别源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-cross-database-error-source-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/amcheck-full-reviewed-certificate.json)。
