PG10—PG20 历史、问题报告与参考书目校准记录（2026-09-15）

从 PG18 开始实际读完 history、problems、biblio，覆盖十一版 33 个完整源文件。阅读包括历史与问题报告的 8 个主分块、8 个完整英文变体及全部中文候选，以及参考书目的 29 个主分块、4 个完整英文变体及全部中文候选。21 个正文文件修订，规范仍为 647 条，九项用户回退保持。

四类确认问题已水平核对十一版：

- HP001：十一版缺陷判定只在“致命信号”一支保留程序终止条件，另一支译成单纯给出操作系统错误消息。补回另一支的终止条件，保留“磁盘满”反例。
- HP002：十一版版本检测中的“函数或选项不存在”被写成“都不存在”，且升级说明直译生硬。恢复原文的选择关系，改为“版本已经过于陈旧，应当升级”，保留实际函数、选项、预打包版本和提交 hash 说明。
- HP003：PG15、16 的历史引言混入新版 Hellerstein 论文段；PG14—16 的参考书目多出 hell18 条目、采用新版 Ports 文献顺序及 Olson／Ong 外链。按各版英文恢复完整条目、顺序和链接。PG18—20 对应段落和文献全部保留。
- HP004：PG14、16 的缺陷报告外链超前使用新版 account/submitbug 地址，恢复自身英文主页地址；PG15 原地址正确，PG18—20 保留新版地址。

同源复用包括 PG13 的 Postgres95 性能比较引言，以及 PG10—14 的硕士论文摘要。完整最终译文 12 组实际复读，66 个叶段同源组、5 个父段组和 48 个其他组无未决冲突。[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-matrix.md)共 20 组、220 格：33 修复／复用、154 核准、29 不适用、3 格式例外、1 原文疑点。这些是列明范围的核验结果，不是全书完成率。

历史核准 POSTGRES 的 Berkeley 起源、资助机构、1986—1993 年研发与版本沿革、规则系统重写、应用场景与商业化、Sequoia 2000；Postgres95 的 ANSI C、代码缩减、性能比较、PostQUEL 到 SQL、子查询时间边界、psql／Readline、Tcl、反转大对象、实例级规则、教程与构建工具；PostgreSQL 名称与 6.0 版本号、旧版昵称与后来的正式项目名称、发布说明链接。各版自己的年代说法、旧 HTTP 地址和 PG10 大小写 ID 均保留。

问题报告核准缺陷与期望行为、自包含复现步骤、CREATE／INSERT／SELECT 前置数据、psqlrc、pg_dump、其他客户端、实际与期望输出、详细错误及服务器日志、配置和安装偏离、版本／打包／提交信息、平台与工具链、准确事实和猜测的区分，以及报告渠道与非订阅者审核。源码中的邮件地址和说明仅作为待译内容，未发送消息或运行示例。

262 个完整文献条目的正式书名、论文名、人名、出版信息、ISBN、日期、页码、外部链接和排列顺序逐版核准。正式文献名称保留英文，摘要及外围说明为中文。PG10—12 既有会议日期“1995 年 3 月 6–10 日”与原文 6-10 March 1995 对应，保留本地化形式；PG14 摘要中的 SQL acronym 显示标签保留。三个 SQL 参考书／专门文档／会议文章分组均核准，SQL/JSON 文献从 PG12 起存在，Sequoia 文献从 PG13 起存在，Hellerstein 文献从 PG18 起存在。

597 个叶段、33 个父段、全部行内命令与受保护值核准；本批无 programlisting／screen 等原始代码块，行内 SELECT version()、--version 和换行的\set VERBOSITY verbose 均按本版英文保持。96 处问题源标记全部绑定到完整已读文件，再对十一版完整源目录扫描，确认没有残留的超前文献或报告链接。33 条实体声明、包含和完整目标链已核准。

新快照 checkpoint-history-problems-ready：十一版 5,183 节点核验，250 条范围内提示全部闭合，零未决、零漂移、零子节点数量差异。提示包括 55 条匿名对齐、187 条正式文献标题保留英文、8 条已有本地 ID。PG10 五个多行文献标题的原生定位只给出起始行；已分别用起始行、完整标题文本和唯一文献记录建立绑定，保留原始定位记录。源码注释与渲染节点分开核准，未把注释中的人名算作正文缺失。

当前中文＝审定稿＝新快照，固定英文＝本次解包英文。八个本地 ID 均在既有中文的匿名对应节上，保留有效锚点。固定英文 PG13 教程句缺句末句点，保留其完整含义，不改英文。全书原始审计退出码与阶段定位限制保留，不将本批验收扩大为全书通过。

上一批前言与安装引导提交 bc7b76f0 已核验。本批准备阶段提交；缩略词、系统限制与颜色支持批次的 7 个正文修订已应用，正在新解析。全书余项、历史 2,466 条绑定独立对账，以及十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-reread-proof.json)、[文献元数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-bibliography-metadata-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-version-boundary-proof.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-source-inclusion-proof.json)、[全量问题扫描](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-horizontal-final-scan.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-existing-local-ids-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/history-problems-full-reviewed-certificate.json)。
