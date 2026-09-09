# PostgreSQL 10—13 中文归档文档最终报告

四版源码准备、文件迁移、批量增量翻译及最终验收已完成。目标分别为13.23、12.22、11.22、10.23，共12项正式构建通过；待译、未处置hunk、未关闭源文问题和已发现排版缺陷均为0。本报告对应最终r4源码清单 `dd2c53ebf07c9d39d407d11c7439d1c2e21da5273bbe6da24b1d9160001ab401`，生成于2026-09-09T12:50:20.891283+00:00。

| 版本 | 中文源文 | HTML | A4 PDF | US PDF |
|---|---|---|---|---|
| 13.23 | [源码目录](/Users/vonng/pgsty/pgdoc/zh/13) · [源码包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-13.23-zh-source.tar.gz) | [HTML](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/13-html/html/index.html) · [HTML包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-13.23-zh-html.tar.gz) | [A4](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/13-A4/postgresql-13.23-zh-A4.pdf)（2654页） | [US](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/13-US/postgresql-13.23-zh-US.pdf)（2804页） |
| 12.22 | [源码目录](/Users/vonng/pgsty/pgdoc/zh/12) · [源码包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-12.22-zh-source.tar.gz) | [HTML](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/12-html/html/index.html) · [HTML包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-12.22-zh-html.tar.gz) | [A4](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/12-A4/postgresql-12.22-zh-A4.pdf)（2640页） | [US](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/12-US/postgresql-12.22-zh-US.pdf)（2770页） |
| 11.22 | [源码目录](/Users/vonng/pgsty/pgdoc/zh/11) · [源码包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-11.22-zh-source.tar.gz) | [HTML](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/11-html/html/index.html) · [HTML包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-11.22-zh-html.tar.gz) | [A4](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/11-A4/postgresql-11.22-zh-A4.pdf)（2570页） | [US](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/11-US/postgresql-11.22-zh-US.pdf)（2709页） |
| 10.23 | [源码目录](/Users/vonng/pgsty/pgdoc/zh/10) · [源码包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-10.23-zh-source.tar.gz) | [HTML](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/10-html/html/index.html) · [HTML包](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/postgresql-10.23-zh-html.tar.gz) | [A4](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/10-A4/postgresql-10.23-zh-A4.pdf)（2435页） | [US](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/10-US/postgresql-10.23-zh-US.pdf)（2563页） |

下载校验见 [DELIVERY-MANIFEST.json](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/DELIVERY-MANIFEST.json)、[SHA256SUMS](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/SHA256SUMS)；审计材料见 [audit.tar.gz](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/audit.tar.gz)。源码包及HTML包逐成员解包计算SHA256，与最终源清单和构建产物清单一致。

**固定输入与版本边界。** 五份官方发布包均校验官方SHA256，并记录真实版本声明、完整源码和文档树哈希。四份目标包记录本轮取得时间；14.24复用缓存，原下载时间未知，明确记录本轮重新核验时间，未以mtime冒充下载时间。来源身份见 [SOURCES.md](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/SOURCES.md) 和 [SOURCES.json](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/SOURCES.json)。四条主差异始终直接来自同一官方14.24，中文各自从开工冻结的当前zh/14继承，没有逐版整树串接。原en/14.24的422个文件与官方相同，官方包另有1456个生成HTML/man文件；生成表分别由各版本自己的源码与生成器生成。没有给发布包虚构Git提交。

开工HEAD为 `8ff9e69bff64a8f8f1bc025dc6a1faf10ad4e137`；交付检查HEAD为 `918e6031f235ffbfa97473d2403f398eb74c6f4c`。本轮未提交、推送或发布。1950项冻结输入和3137项既有受保护文件最后逐项核验无漂移，PG14—20保持原样，既有未知文件和人工修改保留。证据为 [最终验收记录](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/FINAL-ACCEPTANCE.json)、[输入快照清单](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/input-files.json)、[受保护文件清单](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/protected-existing-files.json)。

**逐版实测统计。** “组应用范围”是本版用到的全局共享组，跨版不可相加作为唯一组数；“应用”是实际源片段，不是段落数。

| 版本 | 中文源文件 | HTML页面 | 原始hunk | 组应用范围 | 实际应用 | 整SGML文件恢复 / 删除 |
|---|---:|---:|---:|---:|---:|---:|
| 13.23 | 418 | 1060 | 7212 | 8126 | 34397 | 2 / 6 |
| 12.22 | 412 | 1054 | 8464 | 11611 | 45446 | 2 / 10 |
| 11.22 | 388 | 1048 | 9083 | 12126 | 48442 | 4 / 14 |
| 10.23 | 380 | 1010 | 13543 | 12669 | 49045 | 6 / 22 |

完整原始树路径并集分别为1914、1917、1924、1926项。PG13为1635改变/194相同/56仅PG14/29仅目标；PG12为1676/134/75/32；PG11为1683/84/118/39；PG10为1693/12/180/41。包含生成HTML/man的路径计数与中文 authored source 文件数分开统计。路径等式、全部原始diff和重建校验见 [SOURCE-INVENTORY.json](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/SOURCE-INVENTORY.json)、[SOURCE-VALIDATION.json](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/SOURCE-VALIDATION.json)、[四版路径矩阵](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/path-matrix.tsv)、[中文继承清单](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/chinese-inheritance.tsv)。

逐版 inventory.tsv、changes-summary.tsv、full.diff、diffs/、structural-map.tsv 位于：

- [13.23](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/13.23)。
- [12.22](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/12.22)。
- [11.22](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/11.22)。
- [10.23](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/10.23)。

恢复的历史完整SGML文件为：

- PG13：pgstandby.sgml、release-13.sgml。
- PG12：pgstandby.sgml、release-12.sgml。
- PG11：pgstandby.sgml、recovery-config.sgml、ref/pg_verify_checksums.sgml、release-11.sgml。
- PG10：chkpass.sgml、contacts.sgml、pgstandby.sgml、recovery-config.sgml、release-10.sgml、standalone-install.sgml。

文件内部另恢复历史系统目录、恢复配置、旧SQL/函数/权限限制及相应发布历史；移除PG14独有功能时保存迁移来源、维持各版自己的ID和包含链。所有整文件删除及413条修复、上下文重组、明确沿用和退役记录见 [完整统计及修复目录](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/agents/reference_acceptance/FINAL-REPORT-FACTS.md)。413是可追踪记录数，不是413个独立基线错误。

**跨版译文与复用。** 18052个活跃共享组共51577次canonical应用，另有125753次自动继承、结构或字面应用，总计177330次。4715组用于四版，4914组用于三版，2507组用于两版，5916组仅用于一版。31份被后续完整语境决定替代的记录保留来源，共18083份canonical决定；待处理组与实际应用均为0。

| 正式决定的来源/动作分层 | 唯一活跃组 | canonical实际应用 |
|---|---:|---:|
| 无冻结英文/中文对应引用的新译决定 | 10964 | 32546 |
| 有冻结英文、无冻结中文对应引用的新译决定 | 1172 | 3532 |
| 有冻结英中底稿的局部翻译决定 | 2381 | 5468 |
| 明确复用类决定（可含链接、来源或术语调整） | 1683 | 4137 |
| 明确 partial_reuse 部分复用决定 | 372 | 617 |
| 其他字面、标识符、结构或专门审阅决定 | 1480 | 5277 |

其中无冻结中文对应引用的新译决定为12136组/36078次应用，有冻结英中底稿的局部翻译决定2381组/5468次应用。这里的“新译”仅指本轮可追踪冻结引用，不能证明全项目历史首次翻译；`translated`标签14517组/41546次应用不冒充全部首次翻译。原样继承`inherit_exact`共95747次，逐项核对冻结中文SHA；全实际台账中明确reuse命名动作12725次，包含自动复用，口径不同于上表canonical复用4137次和部分复用617次。来源分层、4827个非空冻结引用哈希和逐版统计见 [翻译来源分层](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/agents/reference_acceptance/FINAL-REPORT-FACTS-TRANSLATION-PROVENANCE.json)。

共用台账保存目标英文、冻结英中引用和确认中文；逐版应用保存位置、前后片段、来源哈希、规则与检查结果。入口为 [共享组](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/semantic/final-groups.jsonl)、[实际应用](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/semantic/final-applications.jsonl)、[正式决定目录](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/decisions)、[共用一致性独立核查](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/semantic/shared-decisions-final-audit.json)。早期Luna候选经过Astra主题分工、逐组及完整父段核验，主Agent统一装配；没有四版独立定译。13项历史术语决定保存在 [TERMS-NEW.tsv](/Users/vonng/pgsty/pgdoc/plans/pg10-13-from-14/runs/20260909-150220/TERMS-NEW.tsv)，七项现用规则保存在输入快照中。

**源文验收。** 38302个原始hunk均与两侧固定英文逐字节对应，1474份SGML由实际非重叠应用精确重建，并与最终zh/10—13匹配。105个资源/定制hunk、15372个正文骨架及中文替换hunk、104个PG14独有源文件删除hunk、22400个自有版本生成参考hunk、321个PG14独有生成输出删除hunk分别处置。最后资源复查包含r2 HTML与r3/r4 PDF样式兼容链，错误0。生成参考由各版自身源码完成要求的HTML/A4/US构建，原包HTML/man不被复制为中文交付，见 [生成内容构建闭环](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/GENERATED-BUILD-CLOSURE.json)。

四份中文及四份英文使用各版实际DocBook DTD独立展开校验：PG10为SGML4.2、PG11/12为XML4.2、PG13为XML4.5；重复ID、缺失引用及包含链问题均为0。55个不同片段/107次应用的字面或结构例外、71项整文件诊断均逐项闭合。源文证据见 [hunk独立验收](/Users/vonng/pgsty/pgdoc/en/diff/pg10-13-from-14/20260909-150220/HUNK-DISPOSITION-AUDIT.json)、[严格整书结构核查](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/agents/archive_build/strict-book-preflight/final-applied-source/comparison.json)、[源文契约闭合](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/semantic/source-contract-final-closure.json)、[主Agent完整父段复核](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/root-parent-review/FINAL-SEMANTIC-ACCEPTANCE.json)。交付时`git diff --check`通过。

必要基线修复包括pg_depend被引用方向、归档成功/失败契约、历史配置与DDL限制、函数正则和XML语义、libpq类型/否定、协议与PL/pgSQL上下文，以及PG12/13 XMLTABLE输出尾空格；完整21类重点摘要及每个源引用均保留于修复目录。没有因审美偏好整树重译或回改PG14。长英文散文185492个节点扫描后保留8类/32处（书目标题、真值表关键词及缩写解释）并单独审阅；HTML实际核对的33个短英文索引词与冻结底稿相同。Table of Contents、Synopsis、Note、Index等继承DocBook界面行为保留，不宣称全书不存在任何英文。

**构建、链接和版式。** 每项正式构建记录实际命令、环境、官方归档SHA、退出码、完整及内部日志、最终1598文件源码清单和产物SHA。四HTML、四A4、四US均exit0且构建前后源码不变。全部4172个HTML页面的101164个本地正文链接无破损、无重复ID，5个SVG对象资源存在；八PDF的实际命名目标、书签、链接注释以及FO引用均无缺失。每个PDF的六个Alibaba/Courier中文/代码字体嵌入并保留Unicode映射；缺字、资源错误和溢出均为0。每份PDF保留4条普通诊断：两条符号字体替代、一条英文断词配置、一条span继承提示；未伪报为无任何警告，完整分类见 [最终技术验收](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/inspection/r4-technical-audit.json)。文内外部历史URL已记录，未宣称全部在线可访问。

HTML实际浏览26个代表页、操作16次目录/索引锚点，52张截图中实际查看30张，覆盖各版历史独有、修改、迁移、目录索引和COPY页面。最终4181个HTML/资源文件与此前已视检版本逐字一致并重新绑定哈希，未声称重新浏览全部4172页。官方CSS与字体依赖的请求验证及精确浏览范围见 [HTML最终视检](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/html/HTML-VISUAL-QA-r4.md)。

最终A4实际查看76页，US实际查看53页，分别覆盖四版封面、目录、历史内容、代码、表格、索引和分页；另有前轮及候选问题页记录。所有已发现缺陷均修复并复验，具体页号、纸型、截图SHA和结论见 [A4最终视检](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/a4/A4-VISUAL-REVIEW-r4.md)、[US最终视检](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/US-VISUAL-REVIEW-r4.md)。这是明确范围的实际视检，不是对上万页逐页人工审阅的声明。

PDF样式适配保留正文SGML：为旧版标题/refname补充既有目标锚点；55张函数五列表及3张pgbench五列表采用标签/值排版；窄表、自动引用、索引和预格式输出增加显示断点，边界数字采用可读小字号。独立审核14655个预格式块的原字符、空格和换行，92397个ID及113277个引用属性/目标完整，新增标签逐格核对。显示断点仅在FO/PDF；SGML代码保持原字面。对应 [FO内容守恒证明](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/agents/sources-inventory/pdf-overflow-r3/R4-114c1ddd5ea6-FO-CONTENT-ID-SUMMARY.md) 及 [最终样式兼容记录](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/pdf-overflow-compatibility-applied.json)。

公共脚本仅适配固定历史发布包、旧版版本声明与生成规则，保留现有Git/默认版本调用；PG10补齐自身OpenSP Unicode目录配置。7项HTML、2项PDF英文冒烟通过。脚本语法检查通过；ShellCheck改动前后均报告同一条既有SC2034（paper_type未使用），未新增诊断，未把该检查的exit1写为通过。最终公共脚本相对开工快照的补丁为 [build-compatibility.patch](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/build-compatibility.patch)；四版定制改动与此前失败原因保留于 [兼容证据](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/build-compatibility)、[公共脚本静态检查](/Users/vonng/pgsty/pgdoc/tmp/pg10-13-from-14/20260909-150220/agents/archive_build/final-static-checks.json)。

前轮r1构建失败、r2/r3虽构建成功但PDF未通过的记录，分别保留在 [attempt-01](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/attempt-01)、[attempt-02](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/attempt-02)、[attempt-03](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/attempt-03)；搬移逐文件哈希相同并保留路径映射。最终结论只绑定r4，未覆盖或追改历史失败状态。

执行计划和25751项统一任务的最终状态见 [PLAN.md](/Users/vonng/pgsty/pgdoc/plans/pg10-13-from-14/runs/20260909-150220/PLAN.md)、[TASKS.tsv](/Users/vonng/pgsty/pgdoc/plans/pg10-13-from-14/runs/20260909-150220/TASKS.tsv)。本轮全部要求已关闭；源码和可查看产物保留在上述目录，未提交、推送或发布。
