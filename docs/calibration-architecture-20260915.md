PG10—PG20 内部架构与相关 GEQO 参数校准记录（2026-09-15）

从 PG18 开始完整阅读十一版 arch-dev.sgml；十个 PG18 主块、六个完整英文变体及全部中文候选均实际核对。另读 68 个完整相关范围，包括十一版 geqo_threshold 参数条目及“上传”扫描命中的全部其他语境，共 75 文件、79 范围。22 正文修订：十一版 arch-dev.sgml 与 config.sgml。规范仍为 647 条，九项用户回退保留。

三类确认问题已逐版处理：

- AR001：原译“在下一次调用时，或者在当前这一对输入无法连接时立即……”语序不清。明确 MergeJoin 在下一次调用时前进并重新匹配；若当前两行不能连接，则立即执行。十一版全部修复。
- AR002：执行器内部 feeds/fed up to 被译成“上传给”。改为“向上传递给”，准确表示计划树向父节点传递行数据。PG10—14 每版三处，PG15—20 每版四处，包含后者自己的 MERGE 段。
- AR003：geqo_threshold 将执行次优计划增加的耗时译为“惩罚值”，把查询规模译为“查询尺寸”，且漏明通常最好使用穷举搜索规划器。十一版均改为明确的耗时比较和查询规模说明；保留至少达到阈值、FULL OUTER JOIN 只算一个 FROM 项、默认 12 等事实。

同源连接计划引言复用实际读过的 PG13 译文，保留各版完整三种连接策略子段。六组最终全文实际复读；69 叶段组、5 父段组、63 其他组无未决冲突。总计核准 563 叶段、55 父段；22 个回归测试示例块满足固定英文＝原中文＝审定中文，逐字节一致，未执行示例。

全章对照覆盖查询处理四阶段、客户端和后端进程、连接建立、实例与共享内存；flex／bison 源和生成文件、语法解析与事务及目录查找的边界；规则系统历史和视图重写；扫描路径、索引和操作符类、连接顺序、三种连接策略与最低估计代价；执行器按需返回行／NULL、排序、选择、投影，以及 INSERT、UPDATE、DELETE、MERGE 的 ModifyTable 流程。

版本边界逐版保留：PG10—13 旧连接说明，PG14 起实例及客户端等词汇表链接；MERGE 执行说明自 PG15 起；PG10 的 SIM98 大写引用与其余版 sim98；PG19—20 的 WHERE 示例大小写和空格均使用自身原文。28 个已本地化词汇表链接逐个核准可见文本和 linkend，未把合法译名当作字面量缺失。PG14／15 共六个既有本地 ID 核准保留。

十一版中英文共 8,523 个 SGML 文件水平扫描，162 处命中全部绑定到实际读过的完整范围。GSSAPI 的“网络上传输／连接上传输”、命令行上传递环境变量、级联热备反馈向上传播、双向拷贝协议，以及 JSON／备份清单／增量备份的真实上传含义均逐段核准并保留。11 条实体声明、主文档包含和完整目标链核准。

记录一类原文边界疑义，涉及十一版：架构概述使用 exceeds a threshold，同章后文以 fewer than 描述穷举路径，而配置条目使用 at least 并以 FROM 项计数。保留各处自己的原文含义，未据此改写为一致的不等式，也未声称完成运行时行为验证。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-matrix.md)：18 组、198 格，40 修复／复用、131 核准、14 不适用、2 格式例外、11 原文疑点。这些是检查状态，不是缺陷数或全书完成率。

新快照 checkpoint-architecture-ready：十一版 1,817 配对节点、6 条范围内提示全部闭合；零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留，不扩大为全书通过。

前一阶段 BKI 提交 a8df319e 已核验，12 路径、未推送。本批准备阶段提交，继续完整阅读 GEQO 等余下章节。历史原 2,466 待追溯单元累计核准 221、余 2,245；全书逐句语义校准、独立对账以及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-reread-proof.json)、[代码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-version-boundary-proof.json)、[术语链接](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-localized-glossary-labels.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-source-inclusion-proof.json)、[命中闭合](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-all-occurrences-closure.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-existing-local-ids-proof.json)、[原文疑义](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/architecture-full-reviewed-certificate.json)。
