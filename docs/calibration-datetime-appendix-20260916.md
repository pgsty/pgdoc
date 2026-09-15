PG10—PG20 日期与时间附录校准记录（2026-09-16）

从 PG18 开始，实际阅读十一版 datetime.sgml 全文、七种完整英文变体及全部中文候选，再对照 297 个完整相关范围。共 98 文件、308 范围、1,041 叶段、80 父段及 91 个原始块。六类确认问题均横向核对十一版并同步修复所有适用位置：

- DA001：十一版秋季回拨示例把“一小时后”误放在调钟动作上。两次 1:30AM 分别采用 EDT 与 EST，相隔一小时；调钟发生在两者之间。现已按自身英文纠正。
- DA002：十一版把转换前后“当时采用的偏移”写成“刚刚生效的偏移”。现改为转换前一刻／后一刻采用的 UTC 偏移，保留“在大多数时区”等价于优先按标准时间解释的限定。
- DA003：PG10—16 的输入规则混入未来“配置设置决定”措辞。依各自英文恢复“配置文件提供”；PG17 本来正确，PG18—20 的配置设置表述保留。
- DA004：PG14—16 的缩写配置引言混入 PG18 的 IANA 优先级和后备列表。恢复本版单段说明，保留用户可修改参数而可选文件由管理员控制的约束，移除仅存在于未来段落的两条链接。其余八版分别依自身机制核准。
- DA005：十一版格式模板表和日期输入示例使用“儒略日期”，已依既有术语统一为“儒略日”；日期算法中的儒略历与该日数系统保持区别。
- DA006：十一版系统目录总览使用“时区简写”，统一为“时区缩写”，并追加第 654 条术语规则。实际 IANA 时区名称、缩写值、配置项和视图名保持。

本批修改 44 个正文文件及 3 个规范文件，九项用户回退不变。140 个跨原始块／行内标记正文组、171 个叶段组、9 个父段组和 94 个其他组核准，无未决同源冲突；19 个新文本组实际复读。十一版 8,523 个中英文 SGML 文件的 1,865 条相关检索命中全部绑定已读完整范围，包含主检索及术语补充检索的重叠命中。

DA007 疑报已撤回：PG15 的 text-search-related 沿用“文本检索”短称，符合既有术语校准；它不应机械套用 Full-Text Search → 全文检索。宽泛匹配所得 2,285 条字符串信号仅作为被撤回的检索过程记录，不计缺陷，也不据此声称逐段阅读。实际涉及的 PG15 完整条目已对照。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-matrix.md)：22 组、242 格，58 修复／复用、132 核准、37 不适用、15 例外。91 个原始块完全未变，其中 88 个与自身英文逐字节一致，3 个 PG18—20 输出块各保留六处 Result 行注释译文，其他 SQL 与输出字节相同。十一版 ECPG 示例的 literal 包装内“儒略日”是普通解释标签，输入 J2451187 不变；逐行核准为合法翻译。示例未执行。

各版边界保留：PG10—12 使用 posixrules 并含 2038 限制；PG13 起采用固定美国转换规则并提示 2007 年以前不适用。PG18 起 IANA 缩写优先，配置列表作为后备；关联 GUC、pg_timezone_abbrevs、pg_timezone_names 及发行说明分别核准。儒略日示例在 PG10—13 保留 date_part 浮点输出，PG14 起保留 numeric 输出，PG19 起保留 SQL 大小写改动。输入解析顺序、无公元零年、两位年份、英文月份星期词元、POSIX 三种日期形式、正负偏移方向、配置文件命名／包含／覆盖约束、负夏令时、闰秒说明及历法历史均依固定源文阅读。

新快照 checkpoint-datetime-appendix-ready：十一版 3,559 配对节点、0 提示全部核准，零未决、零漂移、零未解释子节点差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。这是原生解析核验，最终 HTML／PDF 构建仍为 0/33。

上一阶段数据库管理与表空间已提交 52f4c64f，未推送。本批随后单独阶段提交。全书剩余章节、历史 2,466 待追溯单元对账（上次核准 221，余 2,245）、此前批次跨代码块和标记一致性复核，以及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍继续。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-changes.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-all-occurrences-closure.json)、[跨标记分组](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-cross-markup-prose-groups.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-raw-proof.json)、[受保护值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-protected-proof.json)、[日期标签例外](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-existing-date-label-proof.json)、[移除未来链接](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-removed-future-links-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-version-boundary-proof.json)、[包含链](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-source-inclusion-proof.json)、[术语复查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-post-apply-term-check.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-native-validation.json)、[提示归类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/datetime-appendix-full-reviewed-certificate.json)。
