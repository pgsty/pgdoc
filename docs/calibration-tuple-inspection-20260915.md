PG10—PG20 元组检查扩展全文校准记录（2026-09-15）

从 PG18 的 pgstattuple、pgrowlocks、pg_surgery 开始，完整阅读 19 个分块、11 个英文全文变体及全部中文候选，随后把关联发行说明扩展到完整条目，逐组阅读 43 组完整关联范围。共 29 完整文件、45 关联范围，涉及 41 文件、74 范围。

本批确认并修复四类问题，改动 21 个正文文件：

- TUP001：PG10—14 的 pgstattuple、pgrowlocks 标题误用 PG16 起的扩展说明，恢复本版短标题；PG15 已正确，PG16—20 保留本版长标题。
- TUP002：PG14—20 的 pgrowlocks 函数签名把 returns 译成中文，恢复原始签名；PG10—13 原已正确。
- TUP003：PG14—16 的锁模式表混入后续文档的 For Key Share／For Share，恢复本版 Key Share／Share，并复用同源表格译文。保留本版示例中的 For Share，不擅自修改英文内部差异。
- TUP004：PG12—16 发行说明把“对分区表应抛出预期错误”的修复写成“修复抛出预期错误的问题”，恢复正确目的；完整保留后文实际错误消息和各版提交链接。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-matrix.md)包含 14 组、154 格：20 修复、97 本项核准、18 不适用、19 原文疑点格。9 组最终译文已完整复读；454 叶段落、80 嵌套父段落、102 原始块与 74 个保护标记范围核准。同源 92 个叶段落组、8 个父段落组及 130 个其他单元组无未决冲突。

完整核对 pgstattuple 九个函数的签名、全部统计字段、页头和对齐开销、只读锁、扫描时间跨度、死元组判定、近似扫描的可见性映射与空闲空间映射语义、所有示例数字和输出。PG19 起新增的索引密度和碎片说明保留在自身版本；PG10 的安装权限表述与前批次证据精确衔接。

完整核对 pgrowlocks 六列输出、六种锁模式、ACCESS SHARE 锁及阻塞条件、不保证自一致快照、逐元组扫描代价和 ctid 连接示例。保留 PG15 起的角色权限措辞与 PG16 起的事务 ID 链接。pg_surgery 的两个函数、参数、完整示例、损坏状态处理和使用限制均按自身版本核准；PG10—13 自身源清单及包含声明均无该模块，并已读 PG14 的完整引入条目。

横向搜索得到 761 处源标记出现位置，其中 739 处精确绑定到完整已读正文范围，另外 22 处为 contrib.sgml 中的实体包含引用。后者逐版核对 filelist.sgml 的 SYSTEM 声明，确认指向本批已全文阅读的模块；没有将整个 contrib 包装文件及其他扩展算作已读。

固定英文疑点单列：十一版 pgstathashindex 统计表使用 dead_tuples，而示例输出使用 dead_items；PG10—16 pgrowlocks 表格使用 Key Share／Share，而示例有 For Share。另精确继承页面映射批次的 PG10 pgstattuple 权限原文疑点。共 19 个版本记录，不计作 19 个新增缺陷。PG15 一条发行说明原有的非渲染提交元数据注释缺失已实际核对并保留；本批未改任何源注释。PG14 pg_surgery 两个输出块仅有既有行尾空格差异，逐行核对后原样保留，其余原始块与自身英文完全相同。

新快照 checkpoint-tuple-inspection-ready 完成十一版准备与解析；4,044 个节点精确绑定，88 条范围内提示全部按已读节点核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。保留原始全书审计退出码，只对列明范围给出通过结论。本批没有新增术语规则。

前一阶段页面映射提交 fcfb514 已核验，本批准备阶段提交。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-all-occurrences-closure.json)、[包含引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-source-inclusion-proof.json)、[不适用证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-absent-version-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/tuple-inspection-full-reviewed-certificate.json)。
