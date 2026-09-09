# 最终审查订正交付

结论：**GO**。用户批准的四项主要问题及所列 P3 已订正，适用版本的译法与语义对齐；本轮无新增问题、无未决证据。此结论针对已审本地修改和本轮订正；已记录的历史内容与 PDF 版面问题继续单列。

相对本轮开工备份，共改动 **34 个中文文件**，有 **108 条混合粒度修改记录**。按英文语义重组为 **24 个位置、144 个版本结果**；108 条记录恰好覆盖一次。没有重新安装整份候选规则，九项已定回退及其他人工修改保留。

## 订正结果

|项目|订正前 → 订正后|版本与文件|跨版结论|
|---|---|---|---|
|R1 两个 VACUUM 阶段|PG19 配置原为“索引清理和索引清理”；另有“清理索引和清除索引”“索引 vacuum 和索引清理” → 索引清理（index vacuuming）和索引收尾清理（index cleanup）|PG19 config；PG14–18 ref/vacuum；PG19 maintenance，共 7 个段落|六版共有并行 VACUUM 说明统一；PG19 独有自动清理参数保留其适用范围|
|R2 并行应用动作|把参数解释成传输并行程度 → 对流式传入的进行中事务进行并行应用的程度|PG16–19 config、logical-replication，共 8 个段落、16 个片段|保留 streaming = parallel 条件、默认值、参数名和各版限制|
|R3 字符输入转义|字符项转义 → 字符输入转义|PG14–18 func；PG19 func/func-matching，共 12 处|六版两个对应语义位置全部统一；未改转义示例或编码条件|
|R4 多事务|普通正文 multixact/multixacts → 多事务|PG16 config，共 4 处|另五版同段原已使用多事务；ID、字段和 pg_multixact 路径保留|
|P3 BKI 空格|以 引导 模式、引导 目录等 → 连续中文|六版 bki，共 56 个修改行|九个共有段落同步；OID 计数器、initdb/引导及 PG19 类型清单/Const 差异保留|
|P3 psql 空格|模式的安全使用方式后的双空格 → 去除|六版 ref/psql-ref，共 6 行|术语和链接相同、原 SGML 不变|
|P3 发布说明|叠加“的”的句式 → “这一默认设置是模式的安全使用方式之一；自 … 以来，… 一直推荐这种方式。”|PG15 release-15，1 行|保留安全发布后的时间关系与适用条件，不复制到其他版发布历史|
|P3 BRIN 语序|删除对象与条件含混的原句 → “如果存在涵盖指定表块的页面范围摘要，则删除对应的 BRIN 索引元组。”|六版 func / PG19 func/func-admin，共 6 处|删除对象、存在条件和函数签名六版一致|

每个位置的六版状态、中英文原文、路径、行号、SHA256、版本差异见 [六版语义台账](/Users/vonng/pgsty/pgdoc/outputs/terminology-corrections-20260909-074824/CROSS-VERSION.md) 和 [机器台账](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/ledgers/cross-version-semantic.jsonl)。逐处前后文本见 [修改记录](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/ledgers/applied-changes.jsonl)；可直接查看 [本轮差异](/Users/vonng/pgsty/pgdoc/outputs/terminology-corrections-20260909-074824/corrections.patch)、[34 个文件与行号](/Users/vonng/pgsty/pgdoc/outputs/terminology-corrections-20260909-074824/FILES.md)。

## 规则与保护

仅补充逐条规则 51、78、84、251、324、476、538 的语境说明，并新增第 78 项旧译检索别名。当前词表与规则各 631 条、别名 26 条、字面保护 48 条。现用 glossary.tsv、style.md、exclude.tsv、terms-to-preserve.tsv 与本轮备份逐字节一致，九项回退不变。规则说明区分 index cleanup 阶段、INDEX_CLEANUP 一般操作和 performing final cleanup，避免后续再次混淆。

源文差异可由开工备份与 108 条台账精确重建；全部 2637 个中文源文件、2353 个英文源文件已核验。标签、实体、代码、标识符和换行未动；125 条原台账英文证据及六版补充证据已逐一核对。10321 份上轮回退和最终审查封存文件经 SHA256 复核保持不变。`git diff --check` 通过。

证据：[源码检查](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/source-summary.json)、[结构与字面保护](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/source-protection.jsonl)、[规则及入口差异](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/rules-and-materials.patch)、[历史完整性](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/historical-evidence-preserved.json)。现用规则与入口快照随本目录保存。

## 六版构建与显示验收

以下全部是订正后源文的实际构建，共 **18/18 PASS**，构建期间源文未变。页数为含封面和目录的物理页数；十二份 PDF 版本、全部页尺寸和产物 SHA256 已验证，页数/尺寸与上轮相同。

|版本|本轮中文文件数|HTML|A4 PDF|US PDF|
|---|---:|---|---|---|
|14.24|4|[PASS](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/14/html/html/index.html)|[PASS · 2895 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/14/A4/postgresql-14-zh-A4.pdf)|[PASS · 3056 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/14/US/postgresql-14-zh-US.pdf)|
|15.19|5|[PASS](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/15/html/html/index.html)|[PASS · 2908 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/15/A4/postgresql-15-zh-A4.pdf)|[PASS · 3077 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/15/US/postgresql-15-zh-US.pdf)|
|16.15|6|[PASS](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/16/html/html/index.html)|[PASS · 2918 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/16/A4/postgresql-16-zh-A4.pdf)|[PASS · 3078 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/16/US/postgresql-16-zh-US.pdf)|
|17.11|6|[PASS](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/17/html/html/index.html)|[PASS · 2898 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/17/A4/postgresql-17-zh-A4.pdf)|[PASS · 3061 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/17/US/postgresql-17-zh-US.pdf)|
|18.6|6|[PASS](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/18/html/html/index.html)|[PASS · 2934 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/18/A4/postgresql-18-zh-A4.pdf)|[PASS · 3099 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/18/US/postgresql-18-zh-US.pdf)|
|19beta3|7|[PASS](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/19/html/html/index.html)|[PASS · 3010 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/19/A4/postgresql-19-zh-A4.pdf)|[PASS · 3179 页](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/19/US/postgresql-19-zh-US.pdf)|

HTML 完成六版 46 项渲染文字检查，并在实际浏览器查看涵盖六版的 8 个代表页面截图。A4 完成 50 个目标标签的文本及图像核验；US 完成 41 个订正标签的文本及图像核验，另看 1 个基线标签。所有实际变更类别均有显示验收覆盖，未发现本轮新增乱码、截断、重叠或链接显示问题。没有宣称逐页视觉检查整套约三千页的手册。

构建命令、完整日志与产物指纹见 [18 项构建记录](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/builds/summary.json)。显示证据：[HTML 文字](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/html-qa/text-validation.json)、[HTML 截图观察](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/html-qa/visual-review.json)、[A4 图像验收](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/agents/pdf-a4-qa/REPORT.md)、[US 图像验收](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/agents/pdf-us-qa/REPORT.md)。

## 既有问题与未决项

- **本轮订正未决项：0。** 全部已批准位置及可确定对应位置已完成，无遗漏或重复台账。
- **历史内容边界：** PG14 config 与 PG15 logical-replication 的旧未来参数段在各自固定版英文缺位，原样保留并在台账明确标记；六版监控表旧阶段字面译法、其他既有技术/链接问题不扩成本轮全面重译。“外部排序／内排序”保持最终审查判断，不作为问题修改。
- **既有 PDF 版面：** 532 条 FOP 诊断全部与上轮配对，新增加重均为 0；514 条不变，6 条仅 FO 坐标迁移，12 条是 BKI 段尾空格订正后的同一旧警告。构成为字体替代 24、缺连字规则 12、行内溢出 484、span 继承 12。包装日志无诊断，configure 探测结果逐版一致。BKI 类型列表的长行越界在 PG18 A4 新旧物理 2500 页实际可见；本轮改句没有加重，后续 PDF 版面修复应单独处理，不能把构建成功等同于全书无排版缺陷。

详细归因见 [构建诊断审计](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/agents/build-diagnostics/FINAL-README.md)；新旧版面比较见 [BKI 基线图像记录](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/audit/pdf-a4-bki-baseline/review.json)。独立技术终审见 [R1/R2/R4 与规则复审](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824/agents/internals-qa/FINAL-REVIEW.md)。

运行备份与完整证据：[本轮运行目录](/Users/vonng/pgsty/pgdoc/tmp/terminology-corrections/20260909-074824)。当前入口：[CORRECTIONS-REVIEW.md](/Users/vonng/pgsty/pgdoc/plans/terminology-14-19/CORRECTIONS-REVIEW.md)。本地完成，**未提交、推送或发布**。
