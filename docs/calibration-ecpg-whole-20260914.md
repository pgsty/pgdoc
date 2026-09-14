PG10—PG20 ECPG 全章校准记录（2026-09-14）

十一版 `ecpg.sgml` 已完成完整中英阅读、正文修复、同义译文统一、版本差异核对及本批原生验收。**全书余项、历史台账最终对账和 33 项最终 HTML/A4/US PDF 构建仍未完成。**

本章修复包括：PG14/15 混入未来的 typedef 及预备事务说明，char[] 和 VARCHAR 的类型含义，时间戳减时间间隔的方向，日期格式输入被误翻译，数值溢出和日期指针条件，SQLDA 的结果列、字段和 SCALE，sqlwarn 与 SQLSTATE 的错误处理语义，PG14+ 漏失的 extern "C" 声明段，以及 ECPGdo 被误设为最多 50 个参数。SQL 命令参考另修正“使用后应释放”、SQL 常量误作标识符、声明的源代码顺序和 Notes 漏译。具体版本结果逐项列在七份报告中。

阅读以 PG18 为入口，随后逐一核对十个版本的独有正文、结构、语法和代码。最终覆盖 844 个节范围（186 个顶层节）、183 个命令参考页、2940 个外层条目和全部 2929 个程序／签名／输出块。七批完整文件修改可从本章初始快照逐步精确重放到当前文件，章首三种英文框架及全部中文变体已读，没有未归属节。

源代码、函数名和字面输入保留本版内容。代码差异只包含各批已列明的可见注释和 21 处原有箭头实体拼写；本章固定英文的类型、分配、日期、COUNT 与 WHENEVER 等疑点均有独立记录。依据固定源码校正的项目与仍保留的原文疑点分开，不把实现核查说成运行测试。

下表汇总 209 个问题／回归组、2299 个版本格：1262 格修复或措辞校准，795 格原已正确，26 格不适用，205 格原文疑点，以及 11 格依据源码核对的日期转换纠正记录。格数不是独立缺陷数；点击各范围可逐项查看十一版结果。

| 范围及逐项十一版表 | 检查组 | 版本格 | 修复/统一 | 原已正确 | 不适用 | 原文疑点 | 源码核准纠正 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [前五节](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-front-20260914.md) | 41 | 451 | 252 | 127 | 6 | 66 | 0 |
| [pgtypes 与相关接口](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-pgtypes-20260914.md) | 34 | 374 | 224 | 88 | 0 | 51 | 11 |
| [描述符](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-descriptor-20260914.md) | 21 | 231 | 131 | 89 | 0 | 11 | 0 |
| [错误处理](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-errors-20260914.md) | 20 | 220 | 152 | 67 | 1 | 0 | 0 |
| [预处理、编译及 C++](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-toolchain-20260914.md) | 23 | 253 | 139 | 87 | 5 | 22 | 0 |
| [兼容及内部机制](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-compat-20260914.md) | 31 | 341 | 208 | 98 | 2 | 33 | 0 |
| [SQL 命令参考](/Users/vonng/pgsty/pgdoc/docs/calibration-ecpg-sqlrefs-20260914.md) | 39 | 429 | 156 | 239 | 12 | 22 | 0 |

十一份最新中文快照、当前文件、审定稿、固定英文和解包英文精确一致。539 条全章结构提示逐项绑定 673 个节点：510 个既有本地 ID、18 个匿名组、11 个重复日期格式键的表行组，未决和漂移均为零。4847 个完整节点提供准确行号配对，初始 397 条路由信号也已逐项归入已读范围。保留原始审计退出码 PG10—12 的 3、PG13—20 的 1；这是整书原始结果，不等于全书通过。

正文未再变化，因此完整 ECPG 验收复用刚完成的 `checkpoint-ecpg-sqlrefs-full` 十一版整书快照，并再次核对全部字节，无需重复生成相同内容。HTML 与 PDF 最终构建另行执行。

证据：[209组逐格矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-issue-version-matrix.json)、[844个已读范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-full-parent-plans.json)、[七批精确重放](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-full-applied-stage-replay.json)、[2929个代码块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-full-raw-proof.json)、[当前快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-native-current-snapshot-proof.json)、[539条逐项核定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-native-classification.json)、[初始信号处置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-whole-initial-routing-dispositions.json)。
