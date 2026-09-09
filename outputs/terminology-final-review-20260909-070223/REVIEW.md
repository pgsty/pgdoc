**PG14—19 本地术语修改最终审查：NO-GO**

多数改动提高了术语准确性，但当前版本仍有 **2 类语义回归、2 类同步遗漏**。它们需要订正后才能通过“译文更可靠”和“所有适用大版本一致”这两项要求。本次只审查，未修改正文或生效规则。

审查对象是当前全部未提交术语改动，包括九项回退后的结果，并非只复查回退词表。现场 HEAD 为 `e1bedd55af220a19d4c2fe3c204e22a409c04c8f`；固定英文为 14.24、15.19、16.15、17.11、18.6、19beta3。九项既定译法不重新讨论。

**需要订正的 4 项（均为 P2）**

| 编号 | 问题 | 性质 | 影响范围 |
|---|---|---|---|
| R1 | 两个 VACUUM 阶段都变成“索引清理” | 新增语义回归 | PG19，1 处 |
| R2 | 并行应用被改成“流式传输的并行度” | 新增语义回归 | PG16—19，各 1 处 |
| R3 | 同一正则类别混用“字符输入转义”和“字符项转义” | 术语校准遗漏 | PG14—19，各 2 处 |
| R4 | PG16 的多事务说明漏同步 | 跨版校准遗漏 | PG16，4 处正文用法 |

**R1：必须保留两个不同阶段。** [PG19 config.sgml:8047](/Users/vonng/pgsty/pgdoc/zh/19/config.sgml:8047) 从“索引清理和索引清除阶段”改成了“索引清理和索引清理阶段”。[本版英文](/Users/vonng/pgsty/pgdoc/en/19beta3/config.sgml:9807) 分别是 `index vacuuming` 和 `index cleanup`；[同版阶段说明](/Users/vonng/pgsty/pgdoc/en/19beta3/monitoring.sgml:7656) 还明确后者发生在堆扫描以及索引、堆的 vacuum 都完成之后。现在的中文丢失了这个区别。

可以改成“索引清理（index vacuuming）和索引收尾清理（index cleanup）阶段”，并为 [cleanup stage 规则](/Users/vonng/pgsty/pgdoc/tmp/ref/glossary.rules.tsv:85) 与 [Index Vacuuming 规则](/Users/vonng/pgsty/pgdoc/tmp/ref/glossary.rules.tsv:252) 补充相邻出现时的消歧要求。这是完整句子的语境处理，不需要全局重新定义“清理”。`autovacuum_max_parallel_workers` 在固定的 PG14—18 中英文配置文件里均不存在；不能为对齐而向旧版加入该参数。

**R2：并行的是订阅端的应用动作。** `max_parallel_apply_workers_per_subscription` 原译“对正在进行中的事务流进行并行应用的程度”，现为“对正在进行中的事务进行流式传输的并行度”。这删掉了 apply 的限定，使读者容易把该参数理解成控制传输并行度。config 英文采用了简略的 `parallelism for streaming` 表述，但同段第一句是 parallel apply workers，同版 CREATE SUBSCRIPTION 明确由可用的并行应用工作进程直接应用传入的更改。

| 大版本 | 当前中文 | 同版英文语义依据 | 处理结论 |
|---|---|---|---|
| PG14 | [config.sgml:4354](/Users/vonng/pgsty/pgdoc/zh/14/config.sgml:4354) | 14.24 英文没有此参数 | 中文段落为校准前已有串版，本批未改；单列旧问题 |
| PG15 | 无此参数 | 15.19 英文没有此参数 | 不适用 |
| PG16 | [config.sgml:4029](/Users/vonng/pgsty/pgdoc/zh/16/config.sgml:4029) | [CREATE SUBSCRIPTION:270](/Users/vonng/pgsty/pgdoc/en/16.15/ref/create_subscription.sgml:270) | 应恢复并行应用动作 |
| PG17 | [config.sgml:4254](/Users/vonng/pgsty/pgdoc/zh/17/config.sgml:4254) | [CREATE SUBSCRIPTION:286](/Users/vonng/pgsty/pgdoc/en/17.11/ref/create_subscription.sgml:286) | 同 PG16 |
| PG18 | [config.sgml:4486](/Users/vonng/pgsty/pgdoc/zh/18/config.sgml:4486) | [CREATE SUBSCRIPTION:275](/Users/vonng/pgsty/pgdoc/en/18.6/ref/create_subscription.sgml:275) | 同 PG16 |
| PG19 | [config.sgml:4691](/Users/vonng/pgsty/pgdoc/zh/19/config.sgml:4691) | [CREATE SUBSCRIPTION:297](/Users/vonng/pgsty/pgdoc/en/19beta3/ref/create_subscription.sgml:297) | 同 PG16 |

建议四版统一为：“该参数控制订阅设置为 `streaming = parallel` 时，对流式传入的进行中事务进行并行应用的程度。”各版自身默认值、限制条件与链接保持。logical-replication 对应段落原本也有简略表述，修复时可一起澄清；不把该旧问题另算一次新增回归。

**R3：同一转义类别的 12 处旧译未同步。** 标题、定义及下一段已用“字符输入转义”，但紧邻的编码说明仍写“数字字符项转义”和“字符项转义”。英文两处都是 character-entry escapes，没有另一种“字符项”类别。旧词形本来就存在；问题是本批校准留下了同章混用，不能声称该词族已经完成。

| 大版本 | 中文两处 | 英文对应两处 |
|---|---|---|
| PG14 | [func.sgml:5944](/Users/vonng/pgsty/pgdoc/zh/14/func.sgml:5944)、[5947](/Users/vonng/pgsty/pgdoc/zh/14/func.sgml:5947) | [6413](/Users/vonng/pgsty/pgdoc/en/14.24/func.sgml:6413)、[6417](/Users/vonng/pgsty/pgdoc/en/14.24/func.sgml:6417) |
| PG15 | [func.sgml:5944](/Users/vonng/pgsty/pgdoc/zh/15/func.sgml:5944)、[5947](/Users/vonng/pgsty/pgdoc/zh/15/func.sgml:5947) | [6750](/Users/vonng/pgsty/pgdoc/en/15.19/func.sgml:6750)、[6754](/Users/vonng/pgsty/pgdoc/en/15.19/func.sgml:6754) |
| PG16 | [func.sgml:5940](/Users/vonng/pgsty/pgdoc/zh/16/func.sgml:5940)、[5943](/Users/vonng/pgsty/pgdoc/zh/16/func.sgml:5943) | [6809](/Users/vonng/pgsty/pgdoc/en/16.15/func.sgml:6809)、[6813](/Users/vonng/pgsty/pgdoc/en/16.15/func.sgml:6813) |
| PG17 | [func.sgml:5963](/Users/vonng/pgsty/pgdoc/zh/17/func.sgml:5963)、[5966](/Users/vonng/pgsty/pgdoc/zh/17/func.sgml:5966) | [6927](/Users/vonng/pgsty/pgdoc/en/17.11/func.sgml:6927)、[6931](/Users/vonng/pgsty/pgdoc/en/17.11/func.sgml:6931) |
| PG18 | [func.sgml:5978](/Users/vonng/pgsty/pgdoc/zh/18/func.sgml:5978)、[5981](/Users/vonng/pgsty/pgdoc/zh/18/func.sgml:5981) | [7119](/Users/vonng/pgsty/pgdoc/en/18.6/func.sgml:7119)、[7123](/Users/vonng/pgsty/pgdoc/en/18.6/func.sgml:7123) |
| PG19 | [func/func-matching.sgml:1244](/Users/vonng/pgsty/pgdoc/zh/19/func/func-matching.sgml:1244)、[1247](/Users/vonng/pgsty/pgdoc/zh/19/func/func-matching.sgml:1247) | [1679](/Users/vonng/pgsty/pgdoc/en/19beta3/func/func-matching.sgml:1679)、[1683](/Users/vonng/pgsty/pgdoc/en/19beta3/func/func-matching.sgml:1683) |

仅补齐这 12 处“字符输入转义”即可；编码条件、转义示例与 PG19 的拆分文件结构保持。

**R4：PG16 同一配置项漏了四处普通正文。** 另外五版的 `autovacuum_multixact_freeze_max_age` 已写“4亿个多事务”，PG16 仍是“4 亿个 multixact”。[PG16:7051](/Users/vonng/pgsty/pgdoc/zh/16/config.sgml:7051)、[7053](/Users/vonng/pgsty/pgdoc/zh/16/config.sgml:7053)、[7057](/Users/vonng/pgsty/pgdoc/zh/16/config.sgml:7057)、[7059](/Users/vonng/pgsty/pgdoc/zh/16/config.sgml:7059) 的四个 multixact 都是正文用法；[本版英文](/Users/vonng/pgsty/pgdoc/en/16.15/config.sgml:8688) 与其他五版的对象相同，不能作为版本差异豁免。

| PG14 | PG15 | PG16 | PG17 | PG18 | PG19 |
|---|---|---|---|---|---|
| [已用多事务:7503](/Users/vonng/pgsty/pgdoc/zh/14/config.sgml:7503) | [已用多事务:3014](/Users/vonng/pgsty/pgdoc/zh/15/config.sgml:3014) | [漏同步:7059](/Users/vonng/pgsty/pgdoc/zh/16/config.sgml:7059) | [已用多事务:7294](/Users/vonng/pgsty/pgdoc/zh/17/config.sgml:7294) | [已用多事务:7635](/Users/vonng/pgsty/pgdoc/zh/18/config.sgml:7635) | [已用多事务:7918](/Users/vonng/pgsty/pgdoc/zh/19/config.sgml:7918) |

建议补齐 PG16 四处“多事务”；参数名、`pg_class.relminmxid` 和 `pg_multixact/members`、`pg_multixact/offsets` 等真实标识符保持。它是遗漏，不是本批新造的误译。

**流畅性建议（P3，不另作阻塞项）**

- 六版 BKI 章存在“以 引导 模式”“引导 代码”等替换后留下的中文词内空格，例如 [PG14 bki.sgml:19](/Users/vonng/pgsty/pgdoc/zh/14/bki.sgml:19)。可整理成“以引导模式”“引导代码”。
- 六版 psql 同一句“模式的安全  使用方式”残留双空格，例如 [PG14 psql-ref.sgml:537](/Users/vonng/pgsty/pgdoc/zh/14/ref/psql-ref.sgml:537)。[PG15 发行说明:20708](/Users/vonng/pgsty/pgdoc/zh/15/release-15.sgml:20708) 的“推荐的模式的安全使用方式之一”也宜重排为“这种默认设置属于……所推荐的模式安全使用方式”。
- 六版 BRIN 删除摘要说明可以调整语序，例如 [PG14 func.sgml:25372](/Users/vonng/pgsty/pgdoc/zh/14/func.sgml:25372) 的“删除为覆盖给定表块的页面范围生成摘要的BRIN索引元组，如果有的话”。建议“如果存在涵盖指定表块的页面范围摘要，则删除对应的 BRIN 索引元组”。原句对象未错，不列为语义回归。

“外部排序／内排序”的长短不对称本身不足以判错，没有将这种偏好列为订正要求。

**覆盖、验证与结论边界**

| 检查 | 结果与含义 |
|---|---|
| 当前差异覆盖 | 457 个中文文件，2991 个净差异文本块、3637 个变化文本节点；646 组初审与 20 组补审共同覆盖，详见逐块台账 |
| 生效规则 | 631 条术语表的九项回退保持；8 个生效规则文件与上轮验收哈希一致。R1 仍需补充复合语境规则 |
| 工作区保护 | 2637 个中文源文件与审查开始及上轮最终构建输入逐一匹配；审查未改正文和规则 |
| 差异及 SGML | 本轮 `git diff --check` 通过；457 个变化文件的标记、实体及代码/标识符保护签名与 HEAD 相同。不声称进行了严格 DTD 校验 |
| 六版构建 | 上轮 HTML、A4 PDF、US PDF 共 18 项退出码均为 0；本轮复核 6806 个产物文件哈希，全部匹配，没有重跑构建 |
| 既有构建诊断 | 上轮最终报告为 532 条既有警告，新增错误或溢出为 0；这项构建事实不证明译文语义正确 |
| 最终内容判定 | NO-GO：上述 4 项完成订正并复核前，不应作为术语校准最终通过版 |

已审的 C 结构体用法、聚合转移函数词族、BRIN 摘要、B-树概念与 btree 标识符边界，以及百分位点与独立完整词条的区分，未发现本批新增的阻塞问题。大部分修改方向正确，现有版本技术差异和标识符得到保留。

旧译中的版本串入、缺失 API、WAL 信号施受关系等另列于各家族的 baseline observations；其中有些值得后续修正，但不是本批新引入。以上结论覆盖本地术语改动及必要的对应位置检查，不代表整套手册的所有旧译都已通过逐字技术复审。

订正后需要重新审查受影响词族和对应六版位置，并重新验证受影响版本的构建。当前 18 项旧构建仅对应本报告审查的源码，不能直接作为未来订正版的构建证明。

完整证据：

- [最终 finding 与六版原文证据](/Users/vonng/pgsty/pgdoc/outputs/terminology-final-review-20260909-070223/findings.json)
- [净差异覆盖汇总](/Users/vonng/pgsty/pgdoc/outputs/terminology-final-review-20260909-070223/coverage.json)；[逐块审读映射](/Users/vonng/pgsty/pgdoc/outputs/terminology-final-review-20260909-070223/coverage-by-block.jsonl)；[覆盖方法及历史反演审计不适用说明](/Users/vonng/pgsty/pgdoc/tmp/terminology-final-review/20260909-070223/audit/coverage-method.md)
- [源码、规则和既有构建产物复核](/Users/vonng/pgsty/pgdoc/outputs/terminology-final-review-20260909-070223/validation.json)
- [索引根审查](/Users/vonng/pgsty/pgdoc/tmp/terminology-final-review/20260909-070223/agents/root/REVIEW.md)；[SQL 审查](/Users/vonng/pgsty/pgdoc/tmp/terminology-final-review/20260909-070223/agents/sql/REVIEW.md)；[内部与存储审查](/Users/vonng/pgsty/pgdoc/tmp/terminology-final-review/20260909-070223/agents/internals/REVIEW.md)；[语言与复合词审查](/Users/vonng/pgsty/pgdoc/tmp/terminology-final-review/20260909-070223/agents/language/REVIEW.md)

本次交付仅为本地审查记录，没有提交、推送或发布。
