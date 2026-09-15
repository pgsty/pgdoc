PG10—PG20 清理、授权与关联位置校准记录（2026-09-15）

完成十一版 VACUUM、vacuumdb、clusterdb、GRANT、REVOKE、DROP OWNED、REASSIGN OWNED 共 77 个参考文件的全文核对。从 PG18 开始，52 个英文全文变体及全部中文候选已读完；其余版本按完整来源及无损差异对照。还完整核对 ddl-priv 的 11 个版本，逐项核对 281 个 grantee 关联单元，以及 104 个 MERGE／权限索引相关范围。合计 155 个文件中的 473 个精确范围，包含 2811 个叶段落和 305 个代码／语法块。本批实际修改 84 个正文文件、3 份翻译规范文件；最终 112 组新文字完成复读。

- VACUUM：PG14—18 补回并行工作进程数受 PARALLEL 约束的前提“如果指定该选项”；PG13 原有条件保留，PG19/20 按改写后的英文说明，PG10—12 无该选项。PG14—20 统一既定“代价”术语；十一版保留可见性映射损坏的 should 限定。PG12—20 的布尔值说明复用已经核准的相同英文译文。
- clusterdb：PG14—16 恢复自身的两个概要形式，移除混入的新版单一形式。连接参数、选项、环境变量及示例按十一版全文核对；相同英文采用相同译文，真实版本差异和代码保留。
- GRANT／REVOKE：十一版把 unspecified 从“系统不会指明”修正为角色选择“并无规定”；REVOKE 保留 PG10—18 的 SET ROLE 与 PG19—20 的 GRANTED BY。PG16—20 修复“引导超级用户”的词内换行。PG10/11 补译 ACL 格式的八类说明性注释，实际权限字母、SQL、输出列名和格式变量不改。
- 权限语义：明确对象所有者角色、所有权转移时的新旧角色要求、授权链接收者涵盖角色；补译普通 with grant option 和 default privileges 说明。PG14—20 恢复 INSERT 的命令标记，按原文校正外键检查／触发器授权的 should 限定。PG12—20 统一“过程语言”，保留类型依赖“可能”阻止后续更改的条件；PG13 沿用“受信任的扩展”。
- ACL：PG17—20 明确“权限条目不为 null 但为空集合”，避免混淆两种状态。PG18—20 恢复 acronym 标记，早期版本保留自己的展开式。ACL 解释表中的读取／追加／写入与中文列表标点统一，表内标识符保持。权限、所有者、默认权限及模式权限的可见索引补译；规则与函数中的关联索引十一版已核准。
- grantee：新增第 640 条“被授权者”，沿用 ACL 函数说明中的既有译法。十一版全部 366 处英文出现位置归入完整 GRANT 页、完整权限节和 281 个信息模式／ACL 单元；普通说明中的受让人、被授权人、被授予者统一，实际列名、函数参数与 ACL 格式占位符 grantee 保留。词表和规则均为 640 条，九项既定原译不变。
- 继续追查版本串入：PG14 的 SELECT 权限、PREPARE 和“物化视图”词条删除本版英文没有的 MERGE；PG14—16 的 WITH 说明、SQL 兼容段及“结果集”词条删除提前出现的 MERGE 用法。各项已逐版核对：例如 PREPARE 从 PG15 起的 MERGE 与 WITH／RETURNING 从 PG17 起的 MERGE 分开处理。
- DROP OWNED／REASSIGN OWNED：十一版全文、角色与数据库作用域、依赖和示例均核准，本批无需修改这两类参考页。

[逐问题十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-matrix.md)共 36 个缺陷、术语或一致性检查组、396 格：209 格本批修订、115 格此前正确、55 格不适用、17 格保留固定英文疑点。组数和格数均不是独立缺陷数。每格可追溯[完整上下文、行号及源码哈希](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-issue-version-matrix.json)。390 个叶段落英文组、31 个外层段落组及 122 个表项／标题组没有未处理的同源中文冲突。

固定英文疑点保留：PG13/14 发布说明中的 MERGE 均见于同版原文，未按关键词删除；PG10/11 的 MERGE 属于 SQL 标准关键字表。PG17 起权限段落的一个 miriam ACL 字面示例仍省略 m，中文与本版英文一致。信息模式 role_udt_grants 对类型权限的历史说明继续按固定源文保留，不能重新计为译文错误。GRANT／REVOKE 中文明确写出 g1 是对英文 of which 的等价回指，不是补回英文遗漏的标识符。

新快照 checkpoint-vacuum-privileges-ready 已完成十一版实际准备、解析与对齐检查。12,821 个节点精确绑定，370 条范围内提示逐项关闭，零未决、零漂移、零子节点计数差异。24 条需单独复核的提示来自“Table column → 表列”的行名，以及 PG14—16 默认权限段落已有的锚点／索引；逐一核对了完整行、段落与 ALTER DEFAULT PRIVILEGES 链接。108 项普通概念、等价回指及既有包装差异均有解释，305 个原始块经自身英文校验。全部既有 ID 保留。正文写入前检查发现的十一行旧行尾空格已清理；早期候选及检查记录保留，不能当作最终验收证据。

本报告仅关闭七类完整参考页及列明的关联范围。PREPARE／EXECUTE／DEALLOCATE 的完整正文正在继续对照；SELECT、术语表和其他尚未通读的范围仍有后续工作。全书逐句语义校准、历史证据独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，构建验收为 0/33。

证据：[审定源码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-file-plans.json)、[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-scope-proof.json)、[逐处修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-changes.json)、[终稿复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-raw-proof.json)、[受保护标记解释](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-protected-dispositions.json)、[规则前后文本](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-norm-changes.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-native-classification.json)、[特殊提示的完整证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-native-specific-proof.json)、[阶段证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/vacuum-privileges-reviewed-certificate.json)。
