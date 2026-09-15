PG10—PG20 通用 WAL 与表访问方法全文校准记录（2026-09-15）

十一版 generic-wal.sgml、PG12—20 的 tableam.sgml 共 20 个完整章节已中英对照。从 PG18 两章全文起读，阅读全部 7 组英文全文变体与中文候选；另阅读 PG10/11 两个完整 CREATE ACCESS METHOD 参考页，以及 PG12—20 九个关联处理器定义段落。共 31 文件、31 范围、22 完整文件，修订 19 个正文文件。

- 十一版通用 WAL 中 pin/unpin、lock/unlock 的说明采用现行钉住／解除钉住、加锁／解锁译法，保留锁的完整持有时间和不能直接修改缓冲区的约束。
- 十一版同源错误退出句明确为无需调用 GenericXLogAbort，避免原直译的歧义。固定 PG20 的 Start 和 Abort 函数已静态核对，作为共同文档语句的佐证；没有据此宣称十一版运行测试。
- PG15/16/18—20 的 table access method 是普通概念，补译为表访问方法并保留 literal；PG17 原本已有中文，但省略了这个标签，现恢复。PG12—14 原译与标签保持。
- PG10/11 旧 CREATE ACCESS METHOD 参数段中的处理函数统一为处理器函数；PG12—20 对应定义已正确。PG17 同源处理器段落措辞亦复用其他版本。
- PG14 处理器说明在中文分成两个段落，内容没有缺失。完整中英和已读 PG13 同源段核准后保留原分隔，不为行数或标签数量机械改写。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-matrix.md)含 18 个问题与检查组、198 格：31 修复、140 本项已正确、27 不适用。每格绑定对应完整源文。PG10/11 表访问方法不适用的结论结合了完整旧参考页仅支持 INDEX 的明确规定、全树类型／包含引用检索和章节文件清单；PG12 起本版已有 TABLE 接口。

完整核准通用 WAL 的四步调用、临界区、整页镜像和增量、页布局、锁顺序、脏标志／LSN 及不记录 WAL 的关系；也核准表处理器签名与生命周期、回调、元组槽、TID、可选缓冲区和位图扫描、崩溃保护与跨访问方法事务。PG15 起自定义 WAL 管理器及逻辑解码注意项、PG17 起通用 WAL 章节归属、PG18 起处理器 SQL/C 示例分别保持本版。

302 个叶段落、24 个嵌套父段落、10 个原始代码／语法块绑定本版英文，7 组最终修订文本已完整复读。46 个同源叶段组、3 个父段组、18 个其他单元组无未决冲突。五组等价差异涉及 PG14 分段、既有产品名称／AM 包装和 TID 英文复数与中文基础形式，均按完整对应段保存精确例外。31 范围受保护内容和链接核准，10 原始块一致，没有新增术语规则。

新快照 checkpoint-storage-interfaces-ready 完成十一版准备、解析和对齐，687 节点精确绑定，范围内 1 条提示逐项核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。原始全书审计退出码保留，本批结论只覆盖列明范围。

前一阶段后台工作进程提交 0fba89d 已核验。本批准备阶段提交。全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建为 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-changes.json)、[最终复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-version-boundary-proof.json)、[PG14 分段](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-paragraph-split-proof.json)、[PG10/11 完整参考与不存在性核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-old-am-reference.json)、[固定 PG20 佐证](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-pg20-abort-source-corroboration.json)、[矩阵数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-native-classification.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/storage-interfaces-full-reviewed-certificate.json)。
