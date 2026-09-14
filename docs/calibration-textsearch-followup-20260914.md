**PG10—PG20：全文检索关联章节与 initdb 补充校准**

更新时间：2026-09-14T15:45:48+08:00。本报告追加 23 个检查组、253 个版本格；检查组包含同一问题的多个表现及术语校准，不等于 23 个新增独立缺陷。

已按 PG18 优先阅读，并对照十一版各自固定英文完成本批正文修复。原 26 项清单和先前批次见[阶段总报告](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)，全文检索主章见[主章校准报告](/Users/vonng/pgsty/pgdoc/docs/calibration-textsearch-20260914.md)。

**逐问题版本核验**。修＝本轮修复；核＝对照本版英文后确认原有内容正确；无＝本版英文不具备该参数或内容。已经清除的未来内容记为“修”。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| initdb 混入 PG18 默认启用与性能损失说明 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| initdb 混入 --no-data-checksums | P2 | 无 | 无 | 无 | 无 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| initdb 混入 --no-sync-data-files | P2 | 无 | 无 | 无 | 无 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| initdb 混入 -c / --set | P2 | 无 | 无 | 无 | 无 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| initdb 混入 -s / --show | P2 | 无 | 无 | 无 | 无 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| initdb 混入 --sync-method | P2 | 无 | 无 | 无 | 无 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| PG14 认证说明沿用新版段落与链接 | P2 | 核 | 核 | 核 | 核 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| PG14 --sync-only 混入新版补充句 | P2 | 核 | 核 | 核 | 核 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| 超级用户有效身份；PG15 缺 postgres 名称说明 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| 密码选项保留各版超级用户称谓 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| initdb 交叉引用标签遗漏与未译 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 无 | 无 | 无 |
| initdb 默认文本检索配置术语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| initdb 选项分组与顺序混入新版 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| PG14/15 集簇定义及模板库引言未跟随本版 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| PG14 参见列表混入新版链接 | P3 | 核 | 核 | 核 | 核 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| unaccent 混入 PG17 起的带引号转换规则 | P2 | 无 | 无 | 无 | 无 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| 全文/文本检索、词典、词元、解析器及索引标题 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| dict_int 把不同词误译为唯一词 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| pg_ts_config_map 缺解析器限定；恢复查询顺序 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| 词典模板实现函数及普通用户说明 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| headline / lextype 回调名称误译 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| get_current_ts_config 说明标点与 OID | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| 创建词典模板中普通用户设置参数的含义 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |

**本批阅读与检查证据**：`initdb` 完整对照了 56 个参数/环境变量变体、10 个文件框架、336 个条目，复核 15 组最终改动。共移除 16 个未来参数条目，保留各版 ICU/builtin、校验和、认证、编码和环境变量差异。`unaccent` 十一版全文完成对照，188 个段落绑定，PG14—16 的带引号规则及示例整项删除，PG17—20 保留。

关联术语完成了 182 个初始配对变体、34 个补充变体，以及三个 SQL 参考页的十一版完整对照。235 个文件内有 1444 个完整父单元绑定；48 组补充最终中英对照已复核，1225 处为经过逐组阅读后确定的术语替换。该范围内的 SGML 标签、属性、链接及 3847 个代码块保持原样。范围之外的章节仍按全书待办继续核查。

全项目十一版重新检索“全文搜索、文本搜索、文本检索字典、过滤字典、分类字典”已无残留；该检索结果只作为术语残留检查。新参数在其他章节的三处命中均位于 PG18 发行说明，三个完整中英段落已读，内容与本版一致。差异检查清理了 14 处代码块之外的行尾空白，`git diff --check` 通过。

**本批解析核验完成**：257 个文件、1466 个完整父单元与当前源码、审定稿、固定英文和新快照一致，零漂移。334 个范围内提示已逐项核定，证据见下方文件。全书原始结构检查退出码仍为 PG10—12 的 3、PG13—20 的 1；此处仅声明本批范围内完成核验。

**固定英文疑义已保留并记录**：`pg_ts_parser` 将解析器输出称为 lexeme；`ALTER TEXT SEARCH PARSER/TEMPLATE` 说明仅改名而语法含 `SET SCHEMA`；`dict_int` 的独立示例配置顺序存在歧义；PG11 发行说明将 `json(b)_to_tsvector` 的结果称为 query。没有自行改写固定英文的这些陈述。

**全任务仍在进行**：全书逐章语义核查、历史范围对账及最终 HTML/A4/US 构建继续进行。33 个最终构建目标均尚未完成验收，本报告不将此前构建或本批解析替代最终构建。

详细证据：[逐组十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/textsearch-followup-issue-version-matrix.json)、[initdb 全文审定稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/initdb-full-file-plans.json)、[unaccent 全文审定稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/unaccent-full-finalized-file-plans.json)、[关联父单元绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/textsearch-terms-followup-finalized-parent-plans.json)、[差异空白修正](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/textsearch-followup-whitespace-finalization.json)。

解析证据：[当前源码与快照绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/textsearch-followup-native-current-snapshot-proof.json)、[逐项处置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/textsearch-followup-native-dispositions.json)、[完整父块复核](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/textsearch-followup-native-parent-proof.json)。
