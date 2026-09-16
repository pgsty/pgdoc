# PG10—PG20 顺序校准：2026-09-16 阶段记录

以 PG18 固定英文为入口，按书内顺序核对中文；每项发现都横向检查 PG10—PG20 自身英文并修复全部适用位置。未扫描 Git 历史。任务继续中，全书及最终构建尚未完成。

## 当前进度与断点

原先 131 个待续 PG18 文件中，已补完 125 个的剩余范围；另有此前已完成的 258 个完整范围候选。文件大小差异很大，**这不是语义校对完成百分比**。日期时间附录已在前一专门批次完成，不重复计为本轮新阅读。

已补完：DDL、XML 函数、配置、角色管理、监控、WAL、回归测试、逻辑解码，以及原剩余的全部 SQL／应用参考页。书框架、包含入口、错误码、关键词表、过时章节入口亦已处理。此前已完成的范围保留；语法、示例和版本差异按各版英文保留。

剩余 6 个文件：`features.sgml`（当前正在读）、`release-18.sgml`、`sources.sgml`、`nls.sgml`、`docguide.sgml`、`glossary.sgml`。其中发行说明明显大于普通参考页，不能按文件数估算剩余工作量。

## 已修复内容

| 问题类别 | 十一版核验与修复情况 |
| --- | --- |
| 事务／恢复、DDL、XML、配置／监控、回归测试 | 前一阶段 74 个正文文件的修复保留：epoch／subcommitted、PREPARE 限定、外键对应同一行、NULL 条件、分区索引与继承边界、XMLTABLE 输入和默认值、恢复参数重设、测试行为与版本差异。 |
| 逻辑解码 | startup 回调设置 output_type、synchronous_commit 条件、unlogged／temporary 修饰对象、停止流与删除槽区别、用户目录和两阶段回调含义。十一版逐版核验并修复。 |
| SQL 参考页 | 行级安全术语；sequence 递增方向；用户映射权限对象；聚集运行状态；类型转换歧义；统计信息来源；可见索引及交叉引用标签。按自身英文保留各版参数和功能边界。 |
| 通知与截断 | 十一版 LISTEN／NOTIFY／UNLISTEN 的两阶段提交预备状态；TRUNCATE CASCADE 对递归加入表的外键引用关系。 |
| 工具说明 | 十一版 pg_config 对接措辞、pg_receivewal 非致命错误的适用范围、pg_waldump 按记录类型汇总；PG12—20 校验和损坏表现；Histogram 在 pg_test_timing 与 width_bucket 的术语。 |
| 关键词表版本污染 | PG14／15 生成配置错误使用 SQL:2023，恢复自身英文的 SQL:2011／2016 及对应输入；补齐 PG14／15／19 缺失的本版关键词数据。其余八版核验通过。 |
| 生成表与可见标签 | 十一版 SQLSTATE 类别说明、PG12—20 关键词分类标签补齐中文。PG10／11 关键词表原为内嵌中文。代码、错误条件名、关键字、SGML 结构保留；生成修复落实到版本目录中的 localize-generated.py 和 generated-translations.json，保留 PG19／20 既有其他生成翻译。 |

从本轮顺序续作开始，修订涉及 **404 个不同中文 SGML 文件**，另有 **41 个生成器／生成输入／本地化配置文件**；此数不含更早批次，不等于这些文件全篇都在本轮阅读。规则第 655／656 条已经落地。统计见 `outputs/pg18-sequential-20260916/current-summary.json`。

## 验证与提交

- 十一版当前整书原生解析全部通过：PG10 OpenSP；PG11—20 DocBook DTD；退出码 0、诊断 0。
- 最近结果：`outputs/pg18-sequential-20260916/appendix-generated-localization-validation.json`。关键词与错误码表使用固定本版输入重新生成，原始英文产物与固定英文一致，再应用中文映射。
- `generated-localization-checks.json` 核验 20 个生成表的标记和受保护标识符不变；输入哈希、匹配次数、输出哈希三种错误均在写入前拒绝。
- 首阶段已提交 `3f4eb05be99543d929403f79c26d5e014826e630`；当前后续修复待本阶段提交。共享工作区其他任务可能推进 HEAD，本记录不追索其提交归属。
- **最终 HTML／A4 PDF／US PDF 验收仍为 0／33**。原生解析不等于渲染构建；本任务没有推送或发布。

## 轻量续作入口

`outputs/pg18-sequential-20260916/progress.jsonl` 记录已读范围、逐版结论与精确补丁。`review.py` 提取当前正文并保存小补丁；`validate_current.py` 在临时目录解析并自动清理，调用 `refresh_generated.py` 从固定源码重新生成附录表。不要重新执行已经产生同名补丁的应用脚本。

只读当前同版英文、中文和现行规范即可继续，不需恢复历史解析缓存、扫描 Git 历史或重新构建过程台账。具体接续要求见 [交接文档](/Users/vonng/pgsty/pgdoc/docs/calibration-handoff-20260916.md)。
