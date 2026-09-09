# PostgreSQL 14—19 术语校准准备包

> 最新阶段：最终审查后的订正及六版验收已完成，结论 GO；当前执行入口为 [CORRECTIONS-REVIEW.md](CORRECTIONS-REVIEW.md)，状态见 [ACTIVE.md](ACTIVE.md)。以下九项回退入口、数量和续跑指令保留为历史上下文；本轮以最新入口和现用 `tmp/ref` 为准。

> 九项回退阶段的历史执行入口：[当前规范状态](ACTIVE.md) 与 [九项回退指令](ROLLBACK-9.md)。现用词表和配套规则以项目 `tmp/ref` 为准。旧冻结 refs、复审候选和历史台账保留追溯，不整体安装；当前任务只落实用户确认的九项回退及必要关联规则。

> 复审材料记录了对全部 68 项的历史判断。用户随后明确要求九项实际正文回退，覆盖其中“只恢复首选”“已一致可保留”等建议；其他候选调整没有安装。下文的原始准备数量和状态仅描述历史时点。

从最初原表至最终定稿，631 条词条中有 68 条净变化。本包准备正式迁移所需的完整规范、版本实况、执行计划和可直接使用的提示词；当前没有改动文档正文或现用词表。

当前九项回退的开工材料是 [ROLLBACK-9.md](ROLLBACK-9.md)；[PROMPT.md](PROMPT.md) 已指向这一入口并保留旧全量校准上下文。续跑可使用以下指令：

> 请在 `/Users/vonng/pgsty/pgdoc` 中读取 `plans/terminology-14-19/ACTIVE.md`，完整执行 `ROLLBACK-9.md`。只处理用户明确决定的九项术语回退及必要关联规则；根据当前文本、备份、有效台账和同版英文逐处核对六版，保护人工修改和其他术语修订，完成实际修改、跨版本台账、结构检查及受影响版本 HTML/A4/US PDF 验收。已有完成位置先核实，避免重复改动。

## 文件用途

| 文件 | 用途 |
|---|---|
| [ROLLBACK-9.md](ROLLBACK-9.md) | 当前九项回退的完整用户决定与执行约束 |
| [ACTIVE.md](ACTIVE.md) | 当前规范、回退状态和最新执行证据 |
| [PROMPT.md](PROMPT.md) | 当前入口及保留的旧全量校准上下文 |
| [PLAN.md](PLAN.md) | 历史全量校准阶段安排、六版对齐与验收 |
| [USAGE.md](USAGE.md) | 使用方法、适用条件、语境边界、代码保护和豁免 |
| [现用词表](../../tmp/ref/glossary.tsv) | 631 条当前中英词表，包含九项恢复原译 |
| [现用逐条规则](../../tmp/ref/glossary.rules.tsv) | 与现用词表配套；其他术语规则保留 |
| [refs/glossary.tsv](refs/glossary.tsv) | 631 条 v2 冻结历史词表，不能覆盖现用规范 |
| [refs/glossary.rules.tsv](refs/glossary.rules.tsv) | 631 条 v2 冻结历史规则，仅供追溯 |
| [refs/changes.tsv](refs/changes.tsv) | 68 条原始版本至最终定稿的净变化、理由、规则与来源 |
| [refs/net-changes.md](refs/net-changes.md) | 便于阅读的完整修订对照表 |
| [refs/aliases.tsv](refs/aliases.tsv) | 20 条历史别名记录；现用 glossary-aliases.tsv 有 25 条 |
| [refs/preserve.tsv](refs/preserve.tsv) | 49 条历史保留说明；现用 terms-to-preserve.tsv 有 48 条，已撤销 B-tree 概念保护 |
| [refs/glossary.original.tsv](refs/glossary.original.tsv) | 最初原表，用于三方比对和追溯 |
| [refs/manifest.json](refs/manifest.json) | 输入来源、哈希、数量及审定版本 |
| [families.json](families.json) | 九个词族的工作拆分，完整覆盖 68 个目标条目 |
| [search-variants.json](search-variants.json) | 英文词形与中文简称的检索提示，不授权替换 |
| [baseline/summary.md](baseline/summary.md) | 六版实测快照、文件数量和词族候选分布 |
| [baseline/alignment-notes.md](baseline/alignment-notes.md) | PG16 已有版本基线差异及正式处理边界 |
| [baseline/build-readiness.json](baseline/build-readiness.json) | 六版 check-deps 结果，区别于正式构建证明 |
| [baseline/candidate-matrix.json](baseline/candidate-matrix.json) | 408 个词条/版本单元，全部待语义核实 |
| [baseline/candidate-hits.jsonl](baseline/candidate-hits.jsonl) | 按文件记录的字面命中、行号与上下文样例 |
| [baseline/file-hashes.json](baseline/file-hashes.json) | 盘点时 4,714 个非生成 SGML 文件哈希 |
| [templates/unit.json](templates/unit.json) | 逐处跨版本语义位置台账模板 |
| [templates/exception.json](templates/exception.json) | 带证据的豁免与未决记录模板 |
| [scripts/preflight.py](scripts/preflight.py) | 可重跑的只读盘点，不修改文档 |

## 重要实况

- 当前对应英文快照为 14.24、15.19、16.15、17.11、18.6、19beta3；以各中文 Makefile 实测值为准，开工时再次核对。
- `en/current` 指向 18.3，不能作为校准基准；顶层批量构建默认漏掉 19，需要显式枚举六版。
- 中文目录里有少量没有同版英文对应的文件，需核查本版书籍的包含链；不以此添加、删除或回移功能。
- 准备包完整词表与三轮审定稿逐字节相同，原表和首修/二修产物均保留。
- 字面候选不能作为错误数量或自动替换清单。执行以 `USAGE.md`、逐条规则和各版本英文为准。

## 重跑盘点

从项目根目录运行 `python3 plans/terminology-14-19/scripts/preflight.py --repo /Users/vonng/pgsty/pgdoc --out <新的盘点目录>`。目录名由执行者按本次运行自行选择；工具拒绝覆盖已经存在的目录。正式执行应放到唯一的 `tmp/terminology-calibration/<运行名>/preflight` 下，保留本包的准备时基线。

`scripts/prepare_refs.py` 是组装本包的一次性来源记录，不是开工命令；它拒绝覆盖已冻结的 refs。`preflight.py` 仍按冻结的 68 项生成历史口径盘点，不负责安装规则，不能作为当前九项回退的自动替换清单。当前续跑按 ROLLBACK-9.md 和最新台账核实。

实际构建留给正式正文校准完成后进行；本次准备验收只覆盖输入一致性、文件引用、词族覆盖、盘点脚本行为、版本映射和 SGML 未被修改。
