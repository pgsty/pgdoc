PG10—PG20 pgcrypto 全文校准记录（2026-09-15）

十一版 pgcrypto 正文已完整对照。以 PG18 的 52 个完整子块和外层框架为入口，阅读全部 10 组英文全文变体与中文候选；267 处关联命中中，211 处在完整正文内，其余 56 个完整段落归为 33 组后逐一阅读。共覆盖 31 个文件、67 个范围，修改 12 个正文文件。

- PG14—16 算法清单混入未来 CFB 模式，PG10—16 的 IV 说明也错误提及 CFB，均按本版修正。PG17 原本正确；PG18 起保留 CFB 支持。PG15/16 误带的六列格式也恢复本版。
- PG10—13 的 44 个参数布局块还残留说明性英文，已复用同源、已读的 PG14 译文。逐块保留 OpenSSL-only 算法限制、所有取值、默认值、函数名、S2K 范围及适用条件。
- 十一版 somewhat impractical 的语气不再强化为显然不切实际。PG10—15 的基准说明恢复作者 I can show；PG16 起原文为被动形式，保留自身语气。
- PG10—14 可见索引和算法来源表中的普通说明补译；算法名称、作者、路径、代码与标识符保持。相同英文的五组不同译文已完整比较并统一。
- PG18 发布说明原把给 pgcrypto 添加 CFB 模式颠倒成给 CFB 添加 pgcrypto 模式，现已修正；同处配置参数对应的是密码学函数，亦与完整定义统一。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-matrix.md)包含 21 个问题与检查组、231 格：52 修复、114 本项语义已正确、55 本版不适用、10 固定英文疑点格。完整核准 PG10—14 可选 OpenSSL、PG15 起强制依赖、PG13 起受信任及核心 UUID、PG18 起 SHA-2 crypt／FIPS 功能，以及各版参数、函数、限制、表格和示例。

1,446 个叶段落、115 个嵌套父段落和 400 个原始块均绑定本版源文。25 组最终修订文本已复读，207 个同源叶段组、11 个父段组、202 个其他单元组无未决冲突。128 个描述性 literallayout 块按 12 组完整中英对核验；其余 272 个代码、签名和输出块与本版英文一致。67 个范围的受保护标记和链接全部核准，未新增术语规则。

固定英文自身两类疑点单列保留：PG14—20 选项引言仍说除 convert-crlf 外仅用于加密，却已有解密专用的 ignore-cipher-failure；PG18—20 的 SHA-crypt 表中 Salt Bits 写 up to 32，而固定实现定义最多 16 个盐字符，每字符取随机输入的 6 位。后者已核准发布包、固定 PG20 提交、头文件、盐生成函数及调用路径；核对的盐生成与调用片段中，只有 PG20 的内存清零调用有变化。这些是静态源文／源码核对，没有执行密码学运行测试，也没有擅改固定英文表值。

新快照 checkpoint-pgcrypto-ready 完成十一版准备、解析与对齐。5,841 个节点精确绑定，范围内 133 条提示全部核准，零未决、零漂移、零子节点数量差异。50 条表格提示是普通表首列翻译导致的键匹配差异；另 1 条父级提示仅因既有中文祖先 ID，实际层级与路径相同。原始 51 条记录保留，均逐节点核准。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计的非零退出码保留，此结论只覆盖本批范围。

前一阶段 FDW 处理器提交 962932f 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-raw-proof.json)、[布局块完整对照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-literal-layout-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-version-boundary-proof.json)、[选项引言疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-source-questions.json)、[盐值位数疑点及固定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-shacrypt-source-question.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/pgcrypto-full-reviewed-certificate.json)。
