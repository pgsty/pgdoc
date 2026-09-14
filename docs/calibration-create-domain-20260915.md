PG10—PG20 CREATE DOMAIN 参考页校准记录（2026-09-15）

信息模式复合类型术语的关联扫描发现了此页差异，随后完整对照十一版参考页：先读 PG18 英中全文，再逐一读完其他所有全文变体的完整差异，覆盖 4 个英文变体及全部 5 个中文候选、383 个文本单元、88 个条目和 33 个代码／语法块。全部 3 个最终修订差异变体均已复读。

PG14—16 的语法恢复为本版 `constraint` 占位符；`domain_constraint` 是本组固定英文 PG17 起才使用的形式。移除 PG14/15 尚无的 CHECK 表达式不应抛错建议，以及 PG14—16 尚无的 NOT NULL 扩展说明，分别保留 PG16 起和 PG17 起本版已有的文字。PG17—20 将“非组合数据类型”校正为“非复合数据类型”。这里区分的是本版文档内容，未把新增说明的版本当作功能首次实现版本。

默认值覆盖顺序、USAGE 权限、CHECK 对 TRUE/UNKNOWN/FALSE 的处理、约束检查时机、空值例外、函数变更后的重新验证及 PG10 reload 用语逐版核对保留。7 个文件有修订，PG10—13 原样不变；22 个程序示例原样保留，11 个语法块按本版英文核准。所有原有 ID 保留，包括旧中文 Notes 节的合法定制锚点。

下表修＝修订，核＝原已正确，读＝全文回归核对，—＝不适用。7 组 77 格包含回归和正确项，不是独立缺陷数量。

| 检查组 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-CREATE-DOMAIN-001 恢复 PG14—16 自己的 constraint 语法占位符 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-CREATE-DOMAIN-002 移除 PG14/15 本版英文尚无的 CHECK 不抛错建议 | 核 | 核 | 核 | 核 | 修 | 修 | 核 | 核 | 核 | 核 | 核 |
| C19-CREATE-DOMAIN-003 移除 PG14—16 本版英文尚无的 NOT NULL 扩展说明 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 核 | 核 | 核 | 核 |
| C19-CREATE-DOMAIN-004 PG17—20 非复合数据类型术语 | — | — | — | — | — | — | — | 修 | 修 | 修 | 修 |
| C19-CREATE-DOMAIN-005 默认值覆盖顺序、USAGE 权限及 CHECK 求值规则 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CREATE-DOMAIN-006 域约束检查时机、空值例外及函数变更后的重新验证 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |
| C19-CREATE-DOMAIN-007 保留 PG10 reload、PG16 起建议与所有代码、链接、原有锚点 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 | 读 |

统计：12 个修订格、25 个原已正确格、7 个不适用格、33 个回归核对格。十一版当前文件、审定稿、新快照、固定及解包英文精确一致；59 条既有 ID 提示已逐项绑定完整已读节点，范围零未决、零漂移。原始整书审计退出码仍保留 PG10—12 的 3、PG13—20 的 1。本页校准完成；全书阅读和最终 33 项 HTML/A4/US PDF 构建尚未完成。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-domain-full-issue-version-matrix.json)、[完整英中审定稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-domain-full-file-plans.json)、[全部代码和语法块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-domain-full-raw-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-domain-native-validation.json)、[逐项原生提示](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/create-domain-native-classification.json)。
