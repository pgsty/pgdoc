# outputs 清理记录（2026-09-16）

记录时间：2026-09-16T08:37:09.553932+08:00。用户要求清理占用数百 GB 的无用输出，已执行并核验。

## 实际结果

| 项目 | 结果 |
| --- | ---: |
| 清理前整个 outputs 占用 | 293.42 GiB |
| 清理后整个 outputs 占用（包含压缩归档） | 97.92 GiB |
| outputs 占用减少 | **195.50 GiB** |
| 归档旧 checkpoint | 168 个 |
| 校验后删除的散装缓存文件 | 22,689 个 |
| 缓存逻辑长度 → 压缩归档长度 | 279.96 → 23.30 GiB |
| 删除的源码展开工作区 | 233 个（正常准备 224、失败／中断 9） |

空间口径使用同一工作目录下清理前后的 `du -sk outputs`，单位为 GiB（1024³ 字节），包含保留的所有项目、证据、最新 checkpoint 和压缩包。缓存的逻辑字节数未扣除硬链接等共享因素，不能直接作为实际释放量；APFS 的 `df` 可用量也会受其他会话及快照影响。

## 清理范围与保留内容

本次仅清理 `/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417` 的旧 `checkpoint-*`，未清理其他项目的输出目录。

旧 checkpoint 的 `audit/` 中，以下大型中间文件按 checkpoint 保存为 `.tar.zst` 后删除散装文件：`en-nodes.jsonl`、`zh-nodes.jsonl`、`landmark-pairs.jsonl`、`tables.json`、`title-pairs.json`、`title-pairs.tsv`、英中文 `references.json`／`inventory.json`、`counts.tsv`、`findings.tsv`；另含 `audit/native-en/` 与 `audit/native-zh/` 下的 `validated.esis`、`postgres.xml`、`converted.xml.tmp`、`source-locations.json`。

每个压缩包均已重新解压读取全部成员，并逐文件核对原始 SHA256，确认内容完全一致后才删除对应散装文件。各包还保存了 SHA256，供日后验证压缩包完整性。原 `findings.json`、`REPORT.md`、manifest、coverage、日志及源文快照仍保留。

另外删除 233 个旧 `prepared/upstream` 源码解包／配置工作区。固定发布包和 PG20 固定源码位于 outputs 外，仍保留；准备清单、源码来源、生成后的英中文文档、原始 SGML 快照和失败日志也保留。删除前已检查保留的源文目录没有指向这些工作区的符号链接。它们可以按原命令和固定输入重新生成，无需恢复重复的源码展开副本。

完整保留：

- 当前 `checkpoint-datetime-appendix-ready` 的十一版缓存和全部文件。
- `zcode-followup` 的修复／阅读证据、未应用事务与 pg_resetwal 草稿、历史证明和脚本。
- 初始审计、基线、原始快照、TODO／PROGRESS，以及独立审查等其他 outputs 项目。
- `en/`、`zh/`、`tmp/ref/` 的源文、译文和规范。

清理后已核对：事务／pg_resetwal 的 **182 个当前源文件**仍与草稿的 before 一致，**5 份规范文件哈希**不变；当前 checkpoint 的十一版英中文节点数据、PG17—19 生成等待事件表均存在。没有应用待续草稿，也没有执行新的 HTML/PDF 构建。

复查剩余大目录后，保留的校准主目录约 66.17 GiB，其中 `zcode-followup` 为 14.10 GiB，当前 checkpoint 为 2.14 GiB，其余主要是各批源文快照、原始审计和报告。它们用于历史追溯及续作；另保留 23.30 GiB 可恢复压缩包，以及独立审查等其他项目输出。剩余内容没有作为重复展开工作区一并删除。

## 旧缓存恢复

旧报告中的散装缓存路径部分已不存在，运行依赖旧节点索引的脚本前，按需从归档取回相应文件。归档内路径相对原 checkpoint，例如 `18/audit/en-nodes.jsonl`。

以恢复一个文件为例（`-k` 保留已存在文件，避免覆盖）：

```bash
zstd -dc '/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/archives/checkpoint-acronyms-limits-color-ready.tar.zst' \
  | tar -xkf - \
      -C '/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/checkpoint-acronyms-limits-color-ready' \
      '18/audit/en-nodes.jsonl'
```

单个原文件的 SHA256 在对应 `manifests/<checkpoint>.json`；整个压缩包的 SHA256 在 `validation.json`。需要多个文件时，在命令末尾追加成员路径。去掉成员列表会恢复该 checkpoint 的全部缓存；不应一次性恢复全部历史 checkpoint，否则会重新占用数百 GiB。

后续批次保留当前完整 checkpoint，旧批次的大型解析缓存经核验后压缩保存，已不再需要的源码展开工作区及时删除。不要直接删除 `zcode-followup`、阅读清单、修复草稿、证明和源码快照。

## 清单与交接

- [清理计划](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/plan.json)、[删除前检查](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/deletion-preflight.json)。
- [执行摘要](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/summary.json)、[空间测量](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/disk-usage.json)、[核验结果与压缩包哈希](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/validation.json)。
- [剩余大目录复查](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/remaining-inventory.json)。
- [逐包原文件清单与 SHA256](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/manifests)、[压缩归档](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/archives)。
- [224 个正常工作区删除清单](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/deleted-workspaces.json)、[9 个失败／中断工作区删除清单](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/deleted-failed-workspaces.json)、[失败工作区原始来源记录](/Users/vonng/pgsty/pgdoc/outputs/cleanup-20260916/failed-workspace-provenance.json)。
- [原校准交接文档](/Users/vonng/pgsty/pgdoc/docs/calibration-handoff-20260916.md)。

本次是存储清理，不改变原校准完成度。全书余项、历史对账、事务／pg_resetwal 草稿证明及 33 项最终构建仍按交接文档续作。归档和逐文件清单仍位于被 Git 忽略的 outputs；另建 worktree 或克隆不会自动带走它们。
