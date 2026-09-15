PG10—PG20 citext 校准记录（2026-09-15）

从 PG18 开始完整阅读 citext：6 个主阅读分块、5 个全文变体及全部中文候选，覆盖 11 个完整模块文件。随后实际阅读 5 组扩展安装总览、受信任列表和完整 FIPS 发行说明，合计 23 文件、28 范围，其中 17 个关联范围。11 个正文文件有修订，没有新增术语规则，现行 647 条及九项用户回退保持。

确认并修复的问题是 PG10—14 的 citext 标题混入未来版本的说明性长标题。五版均恢复自身英文的短标题；PG15 原本正确，PG16—20 具有自身英文长标题，予以保留。此外，将 PG14—20 同源示例说明中的 tuple 按现行词表统一为“元组”，复用 PG10—13 已有译法；该项属于术语和同源复用，不把原先“返回一行”称为功能错误。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-matrix.md)包含 12 组、132 格：12 修复／复用、108 核准、12 不适用。3 组最终译文全部复读，两组同源候选全部核对。41 个叶段同源组、5 个父段组和 11 个其他单元组无未决冲突。

按自身版本核准的边界：非确定性排序规则建议及 Unicode 大小写映射／折叠末段自 PG12；受信任安装和 B-树去重限制说明自 PG13；长标题自 PG16。PG10 示例使用 md5(random()::text)，PG11—20 使用 sha256(random()::text::bytea)，各自原样保留；没有将文档示例差异推断为函数首次引入时间。PG17 的 OpenSSL FIPS 测试发行说明已完整阅读，作者、acronym、嵌套 application/xref 和提交链接均完整。

正文核对涵盖：lower 转换后比较、数据库 LC_CTYPE 与非默认 COLLATE 的两步行为，Unicode 大小写处理的限制，以及转换数据类型或显式 c 标志后的大小写敏感匹配。正则表达式的 ~／~*、!~／!~*、LIKE 操作符及九个字符串函数逐项核准。函数索引、主键和唯一性、search_path 内操作符解析、混合大小写比较需要两个索引、复制与小写转换的代价均保留。没有执行文中 SQL 示例。

351 叶段、25 嵌套父段、25 原始代码块核准。25 块均与本版英文逐字节一致且没有改动；字面量、参数、类型、函数、标记、链接及源注释逐项一致。PG10 的短结束标签只在比较视图中展开，不修改英文源。

346 处源标记逐项分拣：312 处绑定实际读过的正文，33 处对应 11 条模块实体声明／包含链，1 处为完整保留的非渲染 FIPS 作者注释。仅出现在 xref 中的发行说明及受信任列表引用也已经补查，未将其他包装文件的全文算作已读。

新快照 checkpoint-citext-ready：十一版 928 个节点精确绑定，10 条范围内提示全部核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留，该阶段结论仅覆盖列明范围。

btree_gin／btree_gist 阶段提交 f3977a6 已核验，本批准备阶段提交。整数数组扩展的后续完整核对正在进行。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-protected-proof.json)、[字面量](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-all-occurrences-closure.json)、[实体引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-source-inclusion-proof.json)、[源注释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-source-comment-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/citext-full-reviewed-certificate.json)。
