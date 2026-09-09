# 最初原表至最终定稿：术语修订汇总

对比最初提供的 `tmp/ref/glossary.tsv` 与三轮讨论后的 `glossary.final.tsv`。两版均为 631 条；最终有 **68 条实际变化**：59 条仅改中文、5 条仅改英文词头、4 条中英文都改。

下表完整列出这 68 条净变化；“原序号”对应最初词表中的条目序号，不含表头。英文词头有变化的，使用箭头显示。修订理由按最终依据重述，省略中间讨论过程。措辞和格式统一不等同于认定原译有概念性错误。

| 原序号 | 英文词条（原 → 最终） | 最初中文 | 最终中文 | 修订理由 |
|---:|---|---|---|---|---|
| 27 | `B-tree` | B-树 | B 树 | 规范中文名称和连接符；正文中的 B-tree 名称仍按使用规则保留。 |
| 43 | `binary coercible` | 二进制可强制 | 二进制可强制转换 | 补全 coercible 所指的强制转换；原译“可强制”不完整。此处转换无需转换函数。 |
| 50 | `Bloom Classes` | Bloom 类 | Bloom 操作符类 | 补明这是 BRIN 操作符类，避免把“类”误解成一般分类或编程语言中的类。 |
| 51 | `Bootstrap` | 初始启动 | 引导 | 采用计算机启动语境中的“引导”，比“初始启动”简洁；统计学语境另译“自助法”。 |
| 60 | `buffer table` | 缓冲表 | 缓冲区映射表 | 说明其实际作用：将缓冲区标签映射到缓冲区编号，避免误解成存放数据的普通表。 |
| 68 | `Caching Rows (Memoization)` | 缓存行 (Memoization) | 行缓存（记忆化） | 补出 memoization 的中文“记忆化”，并把标题整理为自然的名词短语。 |
| 78 | `Character-entry escapes` | 字符项逃逸 | 字符输入转义 | 正则表达式中的 escape 应译“转义”；character-entry 表示字符输入。 |
| 82 | `cid` | 命令标识 | 命令标识符 | 补足“标识符”，准确说明 cid 的含义，并与 command id 统一；类型名 cid 不译。 |
| 83 | `Class-shorthand escapes` | 类缩写逃逸 | 字符类简写转义 | 补出“字符类”，将 shorthand、escape 分别明确为“简写”“转义”。 |
| 84 | `cleanup stage` | 清除阶段 | 清理阶段 | 与 VACUUM 的“清理”用语统一，避免同一流程混用“清除”和“清理”。 |
| 91 | `combine function` | 组合函数 | 合并函数 | 该函数合并部分聚合状态；“合并”比“组合”更直接，也能区别于函数复合。 |
| 92 | `command id` | 命令标识 | 命令标识符 | 补足“标识符”，与 cid 的中文释义保持一致。 |
| 103 | `constraint escape` | 约束逃逸 | 约束转义 | 修正 escape 的译法；此处指正则表达式的零宽约束转义，不是数据库表约束。 |
| 127 | `default B-tree operator class` | 默认 B-树操作符类 | 默认 B-tree 操作符类 | 保留正文中的 B-tree 名称，并统一“操作符类”的译法。 |
| 137 | `discrete percentile` | 离散百分位 | 离散百分位数 | 补全统计量名称“百分位数”，与 percentiles 统一。 |
| 139 | `DTrace probe` | 探针 | DTrace 探针 | 恢复原译遗漏的 DTrace 限定，避免扩大为任意探针。 |
| 140 | `DTrace probes` | 探针 | DTrace 探针 | 恢复 DTrace 限定，与单数条目统一；中文无需另加复数形式。 |
| 150 | `Escapes` | 逃逸 | 转义 | 字符和正则表达式语境采用“转义”；“逃逸”不适用于这里的含义。 |
| 165 | `External Sorting` | 外排 | 外部排序 | 正式术语表采用完整名称；“外排”可作为介绍后的简称，并非概念性错误。 |
| 179 | `first-committer-win` → `first-committer-wins` | 以先提交者为准 | 先提交者胜出 | 统一词头为 first-committer-wins，并采用“胜出”句式；旧拼写保留为检索别名，不判定来源写错。 |
| 180 | `first-updater-win` → `first-updater-wins` | 以先更新者为准 | 先更新者胜出 | 统一词头为 first-updater-wins，并采用“胜出”句式；来源中的单数 win 保留为检索别名。 |
| 195 | `Frozen txid` | 冻结事务标识 | 冻结事务 ID | 与 transaction id、txid 的“事务 ID”译法统一。 |
| 199 | `full-page image` | 整页镜像 | 整页映像 | 与前映像、后映像等相关术语统一；这是项目词形选择，不表示“镜像”在所有 IT 语境中都错误。 |
| 213 | `header data` | 首部数据 | 头部数据 | 与页头、元组头的用语统一；“首部”本身不属于误译。 |
| 215 | `heap only tuple` → `heap-only tuple` | 堆内元组 | 堆内元组 | 仅规范英文复合词的连字符；中文保留项目既有“堆内元组”，“仅堆元组”作为别称。 |
| 242 | `Inclusion Classes` | Inclusion 类 | Inclusion 操作符类 | 保留 Inclusion 类族名称，同时明确对象是 BRIN 操作符类。 |
| 258 | `inverse transition function` | 逆向转换函数 | 逆向状态转移函数 | 明确逆向操作针对聚合状态，避免误解成类型转换或任意函数的数学逆函数。 |
| 260 | `io_in_progress` | IO 进行标记位 | I/O 进行中标志位 | 补足“进行中”这一状态，并统一 I/O 和“标志位”的写法；标识符保持原样。 |
| 261 | `io_in_progress_lock` | IO 进行锁 | I/O 进行中锁 | 补足“进行中”，与 io_in_progress 对齐；这是历史内部名称的释义，名称本身保留。 |
| 267 | `Join Types and Methods` | 连接类型和方式 | 连接类型与方法 | 与 join method 的“连接方法”用语统一，属于标题措辞调整。 |
| 288 | `log compaction` | 日志压缩 | 日志压实 | 区别按键保留记录的 compaction 与字节压缩 compression；并与单独的 compaction 译名统一。 |
| 297 | `LWW` | 最后写入胜利 | 最后写入胜出 | “胜出”更自然，并与 first-committer-wins、first-updater-wins 的中文句式统一。 |
| 301 | `master` | 主 | 主库 | 在复制角色语境补明“库”，使条目可独立理解；master key 等其他组合不套用。 |
| 302 | `master/slave` | 主/从 | 主库/从库 | 与“主库”“从库”成对统一，明确这是数据库复制角色。 |
| 311 | `Merging Sorted Sets` | 归并排序数据集 | 归并有序集合 | 原文指归并已经有序的集合；避免被读成“归并排序”算法处理的数据集。 |
| 313 | `Minmax Classes` | Minmax 类 | Minmax 操作符类 | 保留 Minmax 类族名称，同时补足 BRIN 操作符类这一对象类型。 |
| 314 | `Minmax-Multi Classes` | Minmax-Multi 类 | Minmax-Multi 操作符类 | 保留 Minmax-Multi 名称并补足“操作符类”，与其他 BRIN 类族统一。 |
| 322 | `multi-table index cluster tables` | 多表索引集群表 | 多表索引簇表 | Oracle 此处的 cluster 是表簇，不能译成服务器集群；该条限于 Oracle 对比语境。 |
| 324 | `Multitransactions` | 组事务 | 多事务 | 采用 MultiXact 的“多事务”译法，减少与组提交或普通事务分组的混淆。 |
| 332 | `No-Wait Locks` | 无等待锁定 | 无等待加锁 | 突出不等待的获取锁行为，用“加锁”表述这一操作。 |
| 360 | `Page Pruning` | 页剪枝 | 页内剪枝 | 明确处理范围在页内，并与分区剪枝区分。 |
| 370 | `parameterized (index) path` | 参数化索引路径 | 参数化（索引）路径 | 保留英文中 index 的括号，避免把参数化路径一概限定为索引路径。 |
| 384 | `peer group` | 平级组 | 同等行组 | 与 peers 的“同等行”衔接；同等性按窗口 ORDER BY 键判断，不要求整行相同。 |
| 385 | `percentiles` | 百分位点 | 百分位数 | 采用完整统计量名称，与“离散百分位数”统一；“百分位点”保留为特定来源别称。 |
| 387 | `pg_checksum` → `pd_checksum` | 页校验和 | 页校验和 | 按原中文“页校验和”及官方页头结构，勘误为实际字段 pd_checksum；不据此自动替换代码。 |
| 388 | `pg_flag` → `pd_flags` | 页标志位 | 页标志位 | 按原中文“页标志位”及官方页头结构，勘误为实际字段 pd_flags；不据此自动替换代码。 |
| 389 | `pg_lsn` | 日志序列号 | 日志序列号类型 | 补明 pg_lsn 是数据类型，区别于它所表示的日志序列号；类型名保持原文。 |
| 393 | `pin count` | 钉数 | 钉住计数 | 补足“钉住计数”的含义，与 pinned 词族衔接；不能与 usage count 混为一谈。 |
| 401 | `postgres server process` | Postgres 服务器进程 | postgres 服务器进程 | 此处 postgres 指程序名，应保留实际小写拼写；泛指产品时仍写 PostgreSQL。 |
| 421 | `Quicksort` | 快排 | 快速排序 | 正式术语表采用完整算法名称；“快排”可作为简称。 |
| 423 | `Range Summarization` | 范围提要 | 范围摘要 | 与 BRIN 块范围的“摘要”概念统一。 |
| 454 | `rescan` | 重扫描 | 重新扫描 | “重新扫描”更自然、完整，属于措辞优化。 |
| 469 | `save-point` → `savepoint` | 保存点 | 保存点 | 采用 PostgreSQL 文档和 SQL 术语中的 savepoint 拼写；旧词头保留为检索别名。 |
| 476 | `secure schema usage pattern` | 安全的模式使用模式 | 模式的安全使用方式 | schema 仍译“模式”，usage pattern 改译“使用方式”，消除重复并明确安全修饰使用方式。 |
| 504 | `skew` | 偏差 | 倾斜 | 数据或负载分布不均时用“倾斜”；时钟、读、写 skew 等仍按完整术语采用“偏差”。 |
| 530 | `START WAL` → `START WAL LOCATION` | WAL 起始位置 | WAL 起始位置 | 补全备份标签中的实际字段名 START WAL LOCATION；中文释义保持不变。 |
| 533 | `state transition functions` | 状态转换函数 | 状态转移函数 | 明确聚合状态随输入发生的转移，与逆向状态转移函数统一，减少与类型转换的混淆。 |
| 538 | `streaming` | 流复制 | 流式传输 | streaming 本身不蕴含复制；streaming replication 才对应“流复制”。 |
| 542 | `struct` | 结构 | 结构体 | 采用 C 语言 struct 的通用中文名称“结构体”；代码关键字不译。 |
| 561 | `TimelineID` → `TimeLineID` | 时间线标识 | 时间线 ID | 按实际 C 类型名修正大小写为 TimeLineID，并统一 ID 译法；不能连带修改相近变量名。 |
| 569 | `transaction id` | 事务标识 | 事务 ID | 采用简洁的“事务 ID”，与 txid 等相关条目统一。 |
| 579 | `Trigrams` | 三元组 | 三字符组 | pg_trgm 中指连续三个字符；“三字符组”能避免与数据库 tuple 的“元组”混淆。 |
| 585 | `txid` | 事务标识 | 事务 ID | 与 transaction id 的“事务 ID”统一；txid 标识符本身保留。 |
| 586 | `txid wrap around` → `txid wraparound` | 事务标识回卷 | 事务 ID 回卷 | 规范 wraparound 的拼写，并与“事务 ID”词族统一；旧词头保留为检索别名。 |
| 591 | `unlogged` | 不记录日志 | 不记录 WAL | 限定所指日志为 WAL，避免理解为不记录任何日志；此处针对相应关系的普通数据变更。 |
| 600 | `Value Insertion` | 插入值 | 值插入 | 标题采用名词短语“值插入”；句中仍可按语法写“插入值”。 |
| 619 | `walreceiver` | WAL 接收器 | WAL 接收进程 | 明确这是 WAL 接收进程，比“接收器”更能说明对象类别；进程名保留。 |
| 620 | `walsender` | WAL 发送器 | WAL 发送进程 | 明确这是 WAL 发送进程，与 WAL 接收进程成对统一；进程名保留。 |

中途修改后最终恢复原样的词条，不计入这 68 条。其余 563 条的英文词头与中文两列不变，但可能补充了使用规则或别称；这些辅助信息详见 [使用规则](glossary.rules.tsv) 与 [别名及勘误](aliases.tsv)。例如 HOT 的中文主译仍为“堆内元组”。

类型名、函数名、字段名、SQL、代码及缩写是否保留原文，按配套规则处理；中文列中的释义不表示可以改写代码。英文词头规范化也不代表可以自动替换引用原文或代码中的实际拼写。

可追溯文件：[最初原表](glossary.original.tsv) · [最终完整词表](glossary.tsv) · [带使用规则和来源的 68 项差异表](changes.tsv) · [三轮讨论记录](../../../outputs/01a08005-ffff-72b1-84e0-109c680e9bc8/v2/讨论记录.md)。现用词表和 SGML 正文没有被替换。
