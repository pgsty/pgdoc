PG10—PG20 字符串搜索扩展校准记录（2026-09-15）

从 PG18 开始完整阅读 pg_trgm、fuzzystrmatch 和 dict_xsyn：35 个主阅读分块、11 个全文变体及全部中文候选，覆盖 33 完整模块文件。随后阅读 48 组完整关联段落／发行说明、2 组补查和 4 组扩展信任规则；合计 125 文件、167 范围，其中 134 个关联范围。共修订 46 个正文文件，规范保持现行 647 条及九项用户回退。

- SSE001：十一版 Levenshtein 和 Metaphone 的 non-null string 被译为非空字符串，改为“非 NULL 字符串”，保留 255 字符限制与代价参数默认值。安装参数、libpq、PL/Tcl 的 nonempty string 原译正确；PL/pgSQL 的非 NULL 游标名也核准。
- SSE002：PG15—20 fuzzystrmatch 和 PG13—20 扩展总览残留普通修饰语 trusted，补为“受信任的”。十一版原始 quote 标记扫描的 14 处残留全部绑定、修复；PG10—12 保留本版超级用户要求。
- SSE003：PG14—20 函数签名中的 returns 被译为返回，恢复原始签名；PG10—13 原已正确。PG15 以前的类型在前顺序和 PG16 起的名称在前顺序分别保留。
- SSE004：PG14—20 dict_xsyn 配置引导句省掉模块名称及 literal 标记，逐版补齐；PG10—13 原已有。
- SSE005：PG10—13 fuzzystrmatch、PG10—15 dict_xsyn 混入新版长标题，恢复各自短标题；其余版本核准。
- SSE006：PG14 pg_trgm 提前写入默认构建不区分大小写的章节说明，删除自身英文没有的句子。PG16—20 保留该句；文档出现时间不作为底层行为首次出现的推断。
- SSE007：十一版 pg_trgm 的全文检索集成标题按该节语境统一术语。
- SSE008：十一版辅助词表的“全部唯一词”改为“所有不重复的词”，明确原文的去重含义；完整 ts_stat/to_tsvector 示例保持。
- SSE009：PG18 大小写转换修复条目残留 ICU locale，补译区域设置，保留单字节编码、字符数与字节数以及数组指针条件。
- SSE010：PG13—15 扩展总览的模块措辞被新版扩展措辞覆盖，恢复自身 modules 语境和 CREATE EXTENSION 的执行主体。
- SSE011：PG18 排序规则变更条目统一数据库集簇，恢复实际提供程序名 builtin，准确保留 LC_CTYPE 行为差异和升级后重新索引的建议。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-matrix.md)共 21 组、231 格：78 修复／复用、123 核准、30 不适用。46 组最终译文全部复读，25 组原始同源信号全部核对；189 个同源叶段组、28 个父段组和 105 个其他单元组无未决冲突。两组配置参数类型标签的中英文括号属于既有等义排版，逐项保留。

版本边界逐版核准：strict_word_similarity 自 PG11；GiST siglen、受信任安装说明及新版表格布局自 PG13；pg_trgm 等值索引查询自 PG14；模块长标题、Daitch-Mokotoff 及新版签名顺序自 PG16。PG10 的交换子原始标记核对正确，没有把差异显示中的疑点记为缺陷。PG19 的 Double Metaphone 单字节编码变更及各版自身多字节限制按原文保留。

三字符组的前置两个空格、后置一个空格、非字母数字分隔、连续区段与完整单词边界逐字核对；相似度与距离方向、0.3／0.6／0.5 阈值、GiST 与 GIN 对最近邻查询的差别，以及无法提取三字符组时的退化行为均保留。Daitch-Mokotoff 的多音编码数组、GIN／全文检索示例，Levenshtein 的 max_d 上下界行为和各类 Metaphone 长度限制已读。dict_xsyn 的四个布尔选项、规则文件和全部命令示例按自身版本核准。没有执行这些数据库示例。

1,229 叶段落、183 嵌套父段落、402 原始块核准。原始块中 389 个逐字相同；4 个仅为既有 PG10 SGML 短结束标签展开，9 个仅为既有 ASCII 输出表头行尾空格差异。实际类型、函数、参数、文件名和字面量进一步按原始内容比较，包含三字符组填充空格，未依赖空白归一化掩盖字面量差异。

2,577 处源标记出现位置精确分拣：2,476 处绑定已读正文，99 处对应 33 条模块实体声明／包含链，2 处为非渲染源注释。PG16 既有缺失的编写者注释作为源观察保留，正文作者和提交链接齐全；PG19 注释原样保留。没有把包装文件的其他内容算作已读。

新快照 checkpoint-string-search-extensions-ready：十一版 3,769 个节点精确绑定，50 条范围内提示全部核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留，本结论仅覆盖列明范围。

上一阶段提交 19b2e1c 已核验，本批准备阶段提交。btree_gin／btree_gist 的后续通读正在进行。全书剩余语义范围、历史独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-protected-proof.json)、[字面量空格](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-version-boundary-proof.json)、[源出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-all-occurrences-closure.json)、[实体引用](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-source-inclusion-proof.json)、[源注释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-source-comment-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/string-search-extensions-full-reviewed-certificate.json)。
