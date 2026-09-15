PG10—PG20 物理存储全文校准记录（2026-09-15）

从 PG18 的完整 storage 章节开始，读完 34 个分块及其全部父级说明，再核对 11 个英文全文变体和所有中文候选。十一版完整章节及 626 个关联范围共涉及 317 文件、637 范围；修订 82 个正文文件和 3 个规范文件。

- 十一版 TOAST 的线外／线内统一为行外／行内；关联修正系统目录、列存储策略、CREATE TYPE、数据限制和 C 函数说明中的内联存储等混用。系统目录的压缩存储说明同步调顺。新增第 644/645 条语境规则，区分独立于 SQL 文本传递的参数、编译器内联和 PL 内联处理器，保留全部实际标识符。
- 十一版明确数组中的空值元素、长度字所占用的最高／最低两位、包含长度字节自身的长度、展开后可能使元组过大的条件、页面内整理空闲空间，以及 t_ctid 所指的较新行版本。
- PG11—14 删除误入的摘要索引例外；PG11—16 恢复本版旧行版本清理段落；PG11—14 补回索引列未更新的总结句。PG15 原有总结句保留，PG16 起的 BRIN 摘要索引例外保留；PG17 起的重定向和行版本链说明按自身英文保留。
- PG10—16 的临时关系文件名使用 backend ID，修正套用新版 process number 的译法；PG17—20 保留本版进程号说明，不与操作系统 PID 混同。
- PG12—16 修正未能察觉目录缓存条目失效的句子；PG10—13 六处关联发行说明按既有规则将热后备恢复为热备。复用同源 TOAST 引言及父段落、宏说明、PG11 的 PL 声明说明，并保留各自代码和链接。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-matrix.md)包含 20 组、220 格：118 修复、81 本项正确、21 本版文档不适用。HOT 的三个子项分别记录；PG10 没有独立 storage-hot 节，其他 HOT 关联说明已核准，并不表示 PG10 没有 HOT 功能。历史发行说明的不存在性结合完整横向出现位置和自身文档版本判断。

完整核对 PGDATA 文件清单、filenode 与对象 OID、关系分支和分段；TOAST 的 1 GB 限制、单字节头部、约 2000 字节块、18 字节磁盘指针、四种存储策略与内存指针生命周期；FSM 的页内树与最大值、VM 两位的保守性和设置／清除条件、初始化分支的恢复行为；24 字节页头、23 字节元组固定头部、空值位图、对齐、页项标识符稳定性、TID 和 HOT 条件。PG10 独有的 PLAIN 单字节头部限制、PG14 起的压缩方法设置、PG19 起的 varlena 类型名称和 PG20 的 TOAST_OID_MAX_CHUNK_SIZE 均按本版保留。

关联检索没有止于段落：107 组正文、22 组额外表格／代码／标题、SPI 简介及热备发行说明均已完整阅读。1,176 处原文可见出现位置全部精确归入已读范围，其中 18 处 SPI refpurpose 单独补齐绑定。早期大小写不敏感 HOT 检索引入的 hot standby、hot backup 等宽泛信号单列为检索记录，没有计入全文阅读。

1,264 个叶段落、127 个嵌套父段落和 127 个原始块核准；69 组最终修订稿逐组复读，系统目录的三个措辞组再次复读。201 个同源叶段组、17 个父段组和 174 个其他单元组无未决措辞冲突；3 组仅保留合法既有 FSM／NULL 包装或大小写。4 个完整 JSON 下标示例中的中文注释单独逐句核对，七版共 28 处精确绑定，实际 SQL 和示例输出不变。受保护元素及全部链接、图片属性经 637 范围核验。

PG12—20 页面布局 SVG 与自身英文逐字节一致；用 Batik 实际渲染并查看图像，PageHeaderData、ItemId、Item 与 Special 等技术标签、空间布局和箭头方向完整。PG10/11 自身没有此图。[图示核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-diagram-proof.json)及[实际预览](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-page-layout-preview.png)单列，不能替代整本 PDF 的最终视觉验收。

新快照 checkpoint-physical-storage-ready 完成十一版准备、解析和对齐，4,824 节点精确绑定，44 条范围内提示全部按具体节点核准；零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，本次结论仅覆盖列明范围。

前一阶段复制进度跟踪与测试解码提交 f346f59 已核验；本批准备阶段提交。全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-version-boundary-proof.json)、[全部出现位置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-all-occurrences-closure.json)、[规范核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-norm-proof.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/physical-storage-full-reviewed-certificate.json)。
