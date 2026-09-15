PG10—PG20 lo／vacuumlo／tcn／uuid-ossp 校准记录（2026-09-15）

从 PG18 开始，实际阅读 11 个主分块、17 个英文全文变体及所有中文候选，覆盖四模块共 44 个完整文件；随后实际阅读 12 组完整关联内容和 21 组补充范围。合计 99 文件、122 范围，其中 78 个关联范围。31 个正文文件有修订，没有新增术语规则，现行 647 条和九项用户回退保持。

确认并修复两类缺陷：lo 的 PG10—14、tcn 的 PG15 混入未来版本长标题，恢复各自短标题，PG16+ 长标题保留；PG19 核心 UUID 函数说明重复保留 uuid_extract_timestamp 和 uuid_extract_version 的两组索引，移除重复的引言位置，保留与 PG18／20 相同的既有函数行位置。其余版本的完整标题与索引逐一核准，PG10—16 尚无这两个提取函数。

同源译文复用包括：lo PG13—20 的受信任段、tcn 的触发器引言和完整示例引言、vacuumlo PG10—13 的两处参数引导句，以及 PG17—20 的 UUID 安装前置条件。所有选项列表、源代码和链接均保留自身版本。命名空间／名字空间在现行词表未有强制条目，旧版有效译法保留；没有将用词偏好误记为技术缺陷。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-matrix.md)包含 21 组、231 格：36 修复／复用、161 核准、34 不适用。13 组最终译文全部复读；7 组同源候选全部核对。145 个叶段同源组、11 个父段组和 111 个其他单元组无未决冲突。全文变体首组中的 vacuumlo PG13 额外中文候选另以已读 PG18 为基准重读并保存差异证据，避免自比对遗漏候选。

lo 的完整核对涵盖大对象可由多处引用且不会随引用行自动删除、lo_manage／lo_unlink 的单引用假设、lo 域与普通 oid 的区别、逐列触发器、可选 UPDATE OF 和 DROP／TRUNCATE 不触发清理的限制。PG10 使用 EXECUTE PROCEDURE，PG11+ 使用 EXECUTE FUNCTION，按同版原始 SQL 保留。

vacuumlo 核对孤立对象判定、只扫描名称为 oid／lo 的列而不涵盖其域、事务中大对象锁和默认删除批量 1000、limit 为 0 的行为、dry run、口令提示和连接参数。英文 PG10／11 尚无本批新式长选项和环境变量节，PG12 起增加相关说明，PG13 起包含 PG_COLOR；这些是固定文档边界，未据此推断全部程序 API 的实际引入时间。

tcn 核对 AFTER／FOR EACH ROW 要求、可选通道名和默认 tcn、I／U／D、主键列和值、标识符双引号及值单引号转义。完整 INSERT／UPDATE／DELETE 通知示例、日期、进程号和输出均逐字节核准。PG19／20 源示例改用大写 SQL 关键字，未统一成旧版小写。

uuid-ossp 完整核对版本 1／1mc／3／4／5 算法、MAC／时间戳、随机多播 MAC、名字空间 UUID 与名称、确定性生成、MD5／SHA1、nil 和四个名字空间常量；OSSP、bsd、e2fs 构建选项和 Windows 前置条件保留本版范围。旧版表格、签名与新式函数表分别核对。

关联完整范围包括十一版 UUID 数据类型、PG13+ 核心 UUID 函数、configure／Meson 和 Windows 构建前置条件、受信任安装策略和完整模块清单，以及 NetBSD uuid_create、客户端默认数据库、vacuumlo 选项与失败处理、lo_manage 崩溃的发行说明。PG17 的提取函数、PG18 起的 uuidv4／uuidv7 和可选偏移量、48 位毫秒范围、无限偏移限制、时间戳并非精确生成时刻、NULL 返回条件、PG20 提取版本 6、PG19 起的 uuid／bytea 转换和 PG20 排序及 min／max 语义均按自身英文核准。未执行 SQL、程序或运行时行为试验。

948 个叶段、67 个嵌套父段和 78 个原始代码块已核准。78 块均与自身英文逐字节一致且原样保留。9 处保护标记差异均为原有且实际审读过的标签：6 处 domain 术语链接的“域”显示文本、PG17 两个 NULL 字面标签、PG19／20 为说明双向类型转换而各重复一次 uuid 和 bytea 类型名。14 个行内值检查例外包括这后三处及 lo 十一版 BEFORE UPDATE OF 的既有关键字换行；没有放宽代码块比较。UUID 两个索引在函数行内的既有放置会被检查器计入签名文字；六条提示逐行复读，并证明除非渲染索引外实际函数签名完全相同，按明确范围关闭。

1,129 处源标记逐项分拣：949 处渲染内容，48 处源注释，132 处实体声明／包含引用。其中 994 处绑定到已读完整范围，3 处仅在范围外的发行源码注释中出现并精确保留；四模块各十一版共 44 条实体包含链已验证。没有把只包含声明或引用的包装文件全文算作已读。

新快照 checkpoint-utility-extensions-ready：十一版 3,167 个节点精确绑定，28 条范围内提示全部核准（16 个既有 ID、6 组匿名节点、6 个由索引位置引起的签名提示），零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留，阶段结论仅覆盖列明范围。

上一批 intagg／intarray 提交 b147a08 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-protected-proof.json)、[字面量](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-all-occurrences-closure.json)、[源分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-occurrence-kinds.json)、[实体引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-source-inclusion-proof.json)、[注释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-source-comment-proof.json)、[首组额外候选](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-first-group-alternate-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-native-validation.json)、[签名位置证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-signature-placement-proof.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/utility-extensions-full-reviewed-certificate.json)。
