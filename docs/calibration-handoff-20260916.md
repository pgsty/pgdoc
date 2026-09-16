# PG10—PG20 校准交接：当前续作入口

更新于 2026-09-16。**本轮待续正文、十一版同步修复和 33 个构建目标的最终验收全部完成。当前无待续正文或验收项。** 本文替代旧的事务草稿断点；不要按旧交接重新做已完成工作。

## 用户当前要求

从 PG18 按顺序核对当前中英文。发现任何问题，立即核对另外十版各自英文，修复全部适用位置并保留版本差异。继续完成正文、跨版本一致性检查及最终构建。**不扫描 Git 历史、不追索提交归属、不重建历史过程台账。** Git 仅用于当前状态／差异检查、保护共享修改和已经授权的阶段提交。

**2026-09-16 用户再次纠偏：以 `en/18.6/` 为基准校对当前 PG18 文档正文，不逐个校对 PG18.4、18.3 等旧小版本的发行说明，也不向其他大版本扩展历史发行说明。此前误将这些发行说明纳入工作，是范围扩大；这部分不计入任务完成进度。停止 `release-18.sgml` 的发行历史阅读，直接续作剩余正文。已误做的发行说明修改尚未提交，保留待处理，不混入后续正文阶段提交。**

工作目录 `/Users/vonng/pgsty/pgdoc`。读取 [AGENTS.md](/Users/vonng/pgsty/pgdoc/AGENTS.md) 和 [译风规范](/Users/vonng/pgsty/pgdoc/tmp/ref/style.md)；术语优先级：`tmp/ref/exclude.tsv` > `tmp/ref/glossary.tsv` > 译风规范 > 既有译文。逐条语境规则在 `tmp/ref/glossary.rules.tsv`。最初要求仍可查 [PROMPT.md](/Users/vonng/.codex/worktrees/c22a/pgdoc/plans/pg10-20-calibration-20260911/PROMPT.md)，按用户最新范围纠偏执行。

## 到哪里了

- 原先 131 个待续文件中，130 个的剩余范围已补齐；`release-18.sgml` 发行历史依用户纠偏排除。此前已完成的范围保留。机器扫描、额外发行历史阅读不计为正文逐条校对进度，文件数不换算为语义正确率。
- 原剩余 SQL 与应用参考页已经全部核对；逻辑解码、回归测试、DDL／XML／配置／监控等原缺口已补齐。
- 日期时间附录已由前一专门批次完成，见 [日期附录记录](/Users/vonng/pgsty/pgdoc/docs/calibration-datetime-appendix-20260916.md)。旧 `pg18-through-manageag.json` 尚未计入这一批，不能据此误判 datetime.sgml 未读。
- `features.sgml` 及生成的 supported／unsupported 特性表已核对；十一版 22 个特性表的描述译文已落实到本版生成映射。
- 最后四个正文文件 `sources.sgml`、`nls.sgml`、`docguide.sgml`、`glossary.sgml` 已完整对照，其中术语表共 131 个词条。新增问题已逐版核验并修复；PG10—12 无术语表定义，未回填新版附录。不要返回旧小版本发行说明。
- 本轮顺序续作修复涉及 422 个不同中文 SGML 文件及 41 个生成相关文件（排除误做的发行说明修改）；具体问题和十一版边界见 [阶段记录](/Users/vonng/pgsty/pgdoc/docs/calibration-sequential-20260916.md)。事务／pg_resetwal 修订以及规则 655／656 已经应用，不再是草稿。

## 当前证据与工具

轻量工作目录：`/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/`。

- `progress.jsonl`：已读范围、问题、十一版结论；各 `.patch` 为精确修改。`current-summary.json` 是当前数量口径。
- `review.py`：按 SGML ID 提取正文、记录已读范围、精确写入补丁。已有补丁名不能重复应用。
- `validate_current.py`：临时目录中整书原生解析并清理。最新 `final-body-validation.json`：十一版全部退出码 0、诊断 0。
- `refresh_generated.py`：从固定本版源码读取必要输入，以当前生成器重建关键词／错误码／特性表，先验证原始产物再本地化；不扫描 Git，不解包整套源树。
- `generated-localization-checks.json`：42 个表的标记和受保护标识符保留；输入哈希／次数／输出哈希异常三类检查均在写入前拒绝。
- `glossary-final-horizontal.json`：最后六组术语表问题的 66 格原文、修改前后及版本适用性证据。
- `final_build.py` 与 `final/`：33 个实际构建目标；`inputs.json` 为固定输入，`consumed/` 逐文件验证构建消费的正文及生成表，`results/` 保存命令、状态、产物摘要，`logs/` 保留构建及 FOP 日志。三个目标共用每版同一份约 10 MiB 文档快照；完整构建临时目录自动删除。
- `xact-resetwal-applied.json`：前批 28 个正文修复，不包含在 progress 的 fix 行中；去重统计已合并它。

PG14／15 关键词生成配置混入 SQL:2023 已恢复为自身的 SQL:2011／2016，相关本版输入补齐。十一版 `localize-generated.py`、`generated-translations.json` 用于持久化生成表译文，现有构建入口会调用；PG19／20 原有其他映射已保留。后续改动不得以更新哈希掩盖实际输入差异。

固定版本：10.23、11.22、12.22、13.23、14.24、15.19、16.15、17.11、18.6、19beta3、PG20 固定源码目录 `tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20`。PG19／20 函数按 `func/func-*.sgml` 拆分。

## 验收和提交边界

原生解析、最终构建、全部 HTML 本地引用检查、整书 PDF 页边界及日志检查均已通过。十一版 HTML、A4 PDF、US PDF 共 **33／33**；12,135 个 HTML 页面，333,943 条本地引用无错误，62,573 页 PDF 无溢出／缺字诊断。22 本 PDF 各实际抽看一页，另查看 10 页修复重点页；十一版 HTML 已在浏览器检查，PG18 术语链接和 PG19 `%S`／`%s` 锚点另行验证。

结果入口：[最终报告](/Users/vonng/pgsty/pgdoc/docs/calibration-final-20260916.md)、[acceptance.json](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/acceptance.json)、[visual-review.json](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/visual-review.json)。每本 PDF 仍有 4 条已核验的非阻断字体／连字符／继承提示，详见最终报告；没有把自动几何检查当作逐页人工检查。

根 Makefile 批量默认仅 PG14—18，必须显式传入 PG10—20。单版 `make zh ZH_VERSION=18`；PDF `make zh-pdf ZH_VERSION=18 PAPER=A4`。先阅读实际脚本确定固定源码、输出路径及本机依赖。OpenSP 在 `tmp/pg10-13-from-14/20260909-150220/agents/archive_build/deps`，FOP 在 `.cache/tools/fop-2.11/fop/fop`。PDF 视觉验收时使用 PDF skill。

首阶段提交 `3f4eb05be99543d929403f79c26d5e014826e630`、参考页及生成附录阶段提交 `7af7818ed83b703c8279a72849c63731e06a4c19` 已完成。最后 30 个正文／生成映射文件已核实进入共享提交 `8fb47319d0504aef8b137c49c390aa75eeaf2c5c`（同时含另一任务的 PG9.3 文件，未重写）；PDF 排版及 PG19 锚点修复已独立提交 `28ffbb399accfd2715c74a6bd1db5e8f36ac039d`。文档收尾提交见本机 `final/completion.json`。共享主分支会由其他任务推进，只看当前状态和本批明确路径；不要 `git add .`、回退或覆盖他人修改。当前 PG9.3 工作属于其他任务。本任务没有推送或发布。

## 完成后的操作边界

无需重新执行已完成的校对队列。若核验本机现状，运行 `python3 outputs/pg18-sequential-20260916/finalize_checks.py`；它会验证当前正文、固定快照、构建消费、全部产物和抽页证据的哈希，发生改动就拒绝复用旧验收。不是只有构建退出码 0 即算完成。

本轮实际口径为 **422 个正文 SGML 文件、41 个生成相关文件、4 个构建／测试／样式文件**。此前 423 误包含一个发行说明文件，已剔除。正文待续清单是 130／130；另一个 `release-18.sgml` 按用户要求排除，不转回待办。

已保留的 `zh/10/release-10.sgml` 至 `zh/18/release-18.sgml` 旧修改未进入本轮正文提交。最终构建使用当前工作区的固定快照，包含这些保留内容，因此不能声称是某个纯提交树的构建；精确快照和哈希已保存。不要把其他任务的 PG9.3 修改混入后续提交。

## 保留事项

- `sequence`、datum／Datum 等遵循排除词表；行级安全、美元引用、shell 类型、预备事务、直方图依现行规范。保留用户九项既有术语回退；不要将短称“文本检索”机械改为“全文检索”。
- 当前固定英文自身疑点只记录，不能暗改：GID 长度表述、动态探针参数编号、逻辑解码示例 `(4 row)` 等。`VALUES` 关于 FROM 后 AS 的说明也按固定英文保留。
- outputs 清理已完成：293.42 → 97.92 GiB，释放 195.50 GiB；见 [清理记录](/Users/vonng/pgsty/pgdoc/docs/calibration-outputs-cleanup-20260916.md)。不要为了续作重新解压大型缓存；阅读当前正文即可。
- 原 F-001—F-026 已逐版处理，原误报和边界记录在 [前期问题总结](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)。不必重新追索其历史归属。
- outputs 不受 Git 跟踪；同机任务使用绝对路径续作，其他 checkout 不会自动拥有这些记录。
