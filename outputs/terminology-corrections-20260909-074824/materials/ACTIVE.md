# 当前术语规范状态

2026-09-09 最终审查订正已完成，结论 **GO**。用户批准的 R1—R4 及所列 P3 已落实到 34 个中文文件，六版 HTML、A4 PDF、US PDF 共 18 项重新构建通过。当前记录入口为 [CORRECTIONS-REVIEW.md](CORRECTIONS-REVIEW.md)，完整结果见 [订正验收交付](../../outputs/terminology-corrections-20260909-074824/REPORT.md)。现用词表及九项回退保持不变；本轮只补充七条语境规则和一条旧译检索别名。旧基线内容及版面问题另列，本轮新增问题和未决证据均为 0。

以下是上轮九项回退完成时的记录，保留追溯；其构建通过不代替本轮订正版验收。

2026-09-09：用户确认的九项术语回退已落实到现用规则及 PG14—19 正文。正文共 1,895 个原子修改、321 个文件；最终六版 HTML、A4 PDF、US PDF 共 18 个构建目标及配套检查全部通过。执行入口见 [ROLLBACK-9.md](ROLLBACK-9.md)。

当前生效输入是项目根目录下的 `tmp/ref/glossary.tsv`、`tmp/ref/glossary.rules.tsv`、`tmp/ref/glossary-aliases.tsv`、`tmp/ref/terms-to-preserve.tsv`，以及现行译风和排除表。词表与逐条规则各 631 条；字面保护说明 48 条。修改记录见 [change.md](../../tmp/ref/change.md)。

| 原序号 | 英文词头 | 已恢复原译 |
|---|---|---|
| 27 | B-tree | B-树 |
| 127 | default B-tree operator class | 默认 B-树操作符类 |
| 179 | first-committer-win | 以先提交者为准 |
| 180 | first-updater-win | 以先更新者为准 |
| 199 | full-page image | 整页镜像 |
| 213 | header data | 首部数据 |
| 267 | Join Types and Methods | 连接类型和方式 |
| 385 | percentiles | 百分位点 |
| 600 | Value Insertion | 插入值 |

同时更新了 backup block 对整页镜像的关联规则。真实代码、名称和输出的字面保护继续有效；`wins` 形式作为来源词形保留，不自动改写英文文献。

`refs/` 是复审前的 v2 冻结输入，`reconsideration/` 是随后复审时的候选与证据。两者保留追溯，不能整体覆盖当前生效规范。本次只安装上述九项及必要关联规则，没有安装复审候选中的其他规则调整。

本轮正文任务已按用户给出的九项回退指令执行：此前可确认的目标词形修改均恢复原译，并核对对应版本英文、补齐关联概念及可见索引。实际访问方法名、代码、输出、文献和其他术语保持原样。此前复审补充中与这项用户决定冲突的建议不再适用。

正文运行记录：`/Users/vonng/pgsty/pgdoc/tmp/terminology-rollback/20260909-000310/`。最终验收使用其中的 `builds-r3/`；`builds/` 为初轮产物，`builds-r2/` 是已中止的中间构建，均不替代最终验收。

较早的规则回退备份与验证目录：`/Users/vonng/pgsty/pgdoc/tmp/terminology-calibration/rules-rollback-9-20260908-235820/`，该次只更新规则，未执行正文。历史校验报告反映各自检查时的状态，不能代替本轮正文验收。

本轮完整回退汇总、六版逐处台账、基线问题及最终构建链接见 [验收交付](../../outputs/terminology-rollback-9-20260909-000310/REPORT.md)。本地完成，未提交、推送或发布。
