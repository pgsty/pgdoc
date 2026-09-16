# PG10—PG20 校准交接：当前续作入口

更新于 2026-09-16。**任务正在继续，正文尚未全部闭合，最终构建未完成。** 本文替代旧的事务草稿断点；不要按旧交接重新做已完成工作。

## 用户当前要求

从 PG18 按顺序核对当前中英文。发现任何问题，立即核对另外十版各自英文，修复全部适用位置并保留版本差异。继续完成正文、跨版本一致性检查及最终构建。**不扫描 Git 历史、不追索提交归属、不重建历史过程台账。** Git 仅用于当前状态／差异检查、保护共享修改和已经授权的阶段提交。

工作目录 `/Users/vonng/pgsty/pgdoc`。读取 [AGENTS.md](/Users/vonng/pgsty/pgdoc/AGENTS.md) 和 [译风规范](/Users/vonng/pgsty/pgdoc/tmp/ref/style.md)；术语优先级：`tmp/ref/exclude.tsv` > `tmp/ref/glossary.tsv` > 译风规范 > 既有译文。逐条语境规则在 `tmp/ref/glossary.rules.tsv`。最初要求仍可查 [PROMPT.md](/Users/vonng/.codex/worktrees/c22a/pgdoc/plans/pg10-20-calibration-20260911/PROMPT.md)，按用户最新范围纠偏执行。

## 到哪里了

- 原先 131 个待续 PG18 文件中，**125 个已补齐剩余范围**。258 个此前完整范围候选保留。文件大小不同，此数不能换算成语义完成百分比。
- 原剩余 SQL 与应用参考页已经全部核对；逻辑解码、回归测试、DDL／XML／配置／监控等原缺口已补齐。
- 日期时间附录已由前一专门批次完成，见 [日期附录记录](/Users/vonng/pgsty/pgdoc/docs/calibration-datetime-appendix-20260916.md)。旧 `pg18-through-manageag.json` 尚未计入这一批，不能据此误判 datetime.sgml 未读。
- **当前正在核对 `en/18.6/features.sgml` 与 `zh/18/features.sgml`。** 其英文尾部及生成的 supported／unsupported 特性表仍须核对，尚未记完成。
- 其余待续：`release-18.sgml`、`sources.sgml`、`nls.sgml`、`docguide.sgml`、`glossary.sgml`。release-18 很大，应逐节记录断点。
- 本轮顺序续作修复涉及 404 个不同中文 SGML 文件及 41 个生成相关文件；具体问题和十一版边界见 [阶段记录](/Users/vonng/pgsty/pgdoc/docs/calibration-sequential-20260916.md)。事务／pg_resetwal 修订以及规则 655／656 已经应用，不再是草稿。

## 当前证据与工具

轻量工作目录：`/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/`。

- `progress.jsonl`：已读范围、问题、十一版结论；各 `.patch` 为精确修改。`current-summary.json` 是当前数量口径。
- `review.py`：按 SGML ID 提取正文、记录已读范围、精确写入补丁。已有补丁名不能重复应用。
- `validate_current.py`：临时目录中整书原生解析并清理。最新 `appendix-generated-localization-validation.json`：十一版全部退出码 0、诊断 0。
- `refresh_generated.py`：从固定本版源码读取两个必要输入，以当前生成器重建关键词／错误码表，先验证原始产物再本地化；不扫描 Git，不解包整套源树。
- `generated-localization-checks.json`：20 个表的标记和受保护标识符保留；哈希／次数异常均在写入前拒绝。
- `xact-resetwal-applied.json`：前批 28 个正文修复，不包含在 progress 的 fix 行中；去重统计已合并它。

PG14／15 关键词生成配置混入 SQL:2023 已恢复为自身的 SQL:2011／2016，相关本版输入补齐。十一版 `localize-generated.py`、`generated-translations.json` 用于持久化生成表译文，现有构建入口会调用；PG19／20 原有其他映射已保留。后续改动不得以更新哈希掩盖实际输入差异。

固定版本：10.23、11.22、12.22、13.23、14.24、15.19、16.15、17.11、18.6、19beta3、PG20 固定源码目录 `tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20`。PG19／20 函数按 `func/func-*.sgml` 拆分。

## 验收和提交边界

原生解析已通过，**最终构建仍为 0／33**：十一版 HTML、A4 PDF、US PDF。正文完成后，使用同一源码快照执行现有构建入口，保存命令／退出状态／日志／产物摘要，并检查实际页面、PDF 渲染及重要链接。`check-deps` 只检查依赖。

根 Makefile 批量默认仅 PG14—18，必须显式传入 PG10—20。单版 `make zh ZH_VERSION=18`；PDF `make zh-pdf ZH_VERSION=18 PAPER=A4`。先阅读实际脚本确定固定源码、输出路径及本机依赖。OpenSP 在 `tmp/pg10-13-from-14/20260909-150220/agents/archive_build/deps`，FOP 在 `.cache/tools/fop-2.11/fop/fop`。PDF 视觉验收时使用 PDF skill。

首阶段提交 `3f4eb05be99543d929403f79c26d5e014826e630` 已完成。共享主分支会由其他任务推进，只看当前状态和本批明确路径；不要 `git add .`、回退或覆盖他人修改。当前 PG9.3 工作属于其他任务。本任务没有推送或发布。

## 保留事项

- `sequence`、datum／Datum 等遵循排除词表；行级安全、美元引用、shell 类型、预备事务、直方图依现行规范。保留用户九项既有术语回退；不要将短称“文本检索”机械改为“全文检索”。
- 当前固定英文自身疑点只记录，不能暗改：GID 长度表述、动态探针参数编号、逻辑解码示例 `(4 row)` 等。`VALUES` 关于 FROM 后 AS 的说明也按固定英文保留。
- outputs 清理已完成：293.42 → 97.92 GiB，释放 195.50 GiB；见 [清理记录](/Users/vonng/pgsty/pgdoc/docs/calibration-outputs-cleanup-20260916.md)。不要为了续作重新解压大型缓存；阅读当前正文即可。
- 原 F-001—F-026 已逐版处理，原误报和边界记录在 [前期问题总结](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)。不必重新追索其历史归属。
- outputs 不受 Git 跟踪；同机任务使用绝对路径续作，其他 checkout 不会自动拥有这些记录。
