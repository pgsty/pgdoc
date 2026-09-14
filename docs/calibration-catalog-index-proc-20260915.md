PG10—PG20 索引和函数系统目录校准记录（2026-09-15）

`pg_index` 与 `pg_proc` 两个小节已完成十一版完整英中对照、修复和新快照原生 SGML 核验。先读 PG18，再读各版自己的全部行、表头、节结构、表外段落及所有中文候选。范围为 22 个完整小节、552 个表行、44 个表外段落；36 个修订译文变体逐一复读。

主要修复：`indnkeyatts` 把键列数量译成编号；`indkey`、`indcollation`、`indclass`、`indoption` 未清楚表达数组元素个数；`indisvalid` 把仍须维护索引的要求译成肯定正在修改的事实。`indisreplident` 的复制标识未译且 USING 修饰关系错误。`proparallel` 缺并行工作者不得调用的整句，serial 误作顺序；`provolatile` 把优化时消除调用误作不能优化。另校准函数参数、默认值、NULL、字符串字面量和函数源码表示的条件。

PG10 不加入 PG11 才有的内含列或 indnkeyatts。`indoption` 保留 PG10 的 indnatts 和 PG11+ 的 indnkeyatts。PG10—13 的 probin 按原文保留“不使用”；PG14+ 按自己的原文说明 NULL，并保留 SQL 标准函数体差异。PG10 的 proisagg/proiswindow、PG10/11 的 protransform、PG12+ 的 prosupport，以及各版链接和字段集合均逐项核对。

修＝已修订，核＝原已正确，读＝完整回归核对，—＝不适用，疑＝保留固定英文疑点。29 组含措辞和回归项，不等于 29 个独立缺陷。

| 问题／检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-CATALOG-IP-001 总列数、键属性和内含属性 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-002 键列数量误译编号 | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-003 索引无效时仍须维护的要求 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-004 HOT 链及查询可见性条件 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-005 复制标识和 USING 的从属关系 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-006 数组元素数量、键列和内含列 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-007 排序规则数组元素数量 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-008 操作符类数组元素数量 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-009 逐列标志数组数量 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-010 表达式树与零值条目的对应关系、NULL | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-011 非部分索引时的 NULL | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-012 实现语言和调用接口的修饰关系 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-013 可变参数数组的元素类型 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-014 安全定义者函数措辞 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-015 严格函数的实参和 NULL 行为 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-016 易失性、副作用与优化消除调用 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-017 并行工作者禁用条件缺句和串行执行 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-018 调用签名 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-019 全体参数类型字段与 NULL | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-020 参数模式字段与 NULL | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-021 参数名称的空字符串与 NULL | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-022 默认值数量、输入参数和 NULL | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-023 转换类型数组与 NULL | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-024 整个源码表示列表的决定条件 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-025 SQL 函数体与字符串字面量 | — | — | — | — | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-026 编译型函数、SQL 函数体与本版 probin 含义 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-CATALOG-IP-027 全部其余字段、表头、标题、段落及本版版本边界 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CATALOG-IP-028 全部其余字段、表头、标题、段落及本版版本边界 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CATALOG-IP-029 复合唯一索引情况下每列一个 null 的固定英文疑点 | — | — | — | — | — | 疑 | 疑 | 疑 | 疑 | 疑 | 疑 |

319 格中有 272 格修订、9 格原已正确、10 格不适用、22 格回归核对、6 格固定英文疑点。PG15+ 的 indnullsnotdistinct 原文把 NULL 相等描述为每列只能有一个 null，复合唯一索引情况下疑似过度概括，留待独立源文核证；本轮保持同版原文，没有擅改这一技术断言。

所有既有表头、标识符、标签、属性、ID 和短结束标记保持原样；这两个小节没有程序块。当前文件、审定稿、修复后新快照、固定英文及解包英文精确一致。0 条范围内既有 ID 提示均已逐项绑定，零未决、零漂移。原生审计保留 PG10—12 的退出码 3、PG13—20 的退出码 1，因为整书其余内容仍有待处理信号；本报告只关闭这两个小节。

系统目录／视图其余范围继续逐项阅读和修复；全书校准、最终独立对账、十一版 HTML 与 A4/US PDF 共 33 项最终构建仍未完成。本次核验不是 HTML/PDF 构建验收。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalog-index-proc-full-issue-version-matrix.json)、[完整审定小节](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalog-index-proc-full-parent-plans.json)、[全部表行](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalog-index-proc-full-row-proof.json)、[表外段落](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalog-index-proc-full-para-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalog-index-proc-full-native-validation.json)、[原生提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalog-index-proc-full-native-classification.json)。
