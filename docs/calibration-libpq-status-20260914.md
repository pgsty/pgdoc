**PG10—PG20：libpq 连接状态章节校准**

本批从 PG18 开始完整阅读连接状态节，再核对其余十版的全部 API 条目、外层段落和版本差异。27 个检查组、297 个版本格包含技术问题、措辞、术语和适用性检查，不代表 27 个独立新增缺陷。180 格修复，84 格原本正确，33 格不适用。正文修复和本批新快照核验均已完成。

主要修复：PG10—14 的 `PQsslAttribute`、`PQsslStruct` 混入了后续版本的返回条件；PG14 多出 PG15 起才有的 SSL 库检测整段；PG13—20 把错误消息“可能包含多行”译成必然包含多行。此外补齐错误消息索引层级，明确 `PQtty` 的 NULL 唯一例外，并校准访问函数、字段、版本号及 NOTIFY 通知等说明。

修＝本轮修复；核＝就该问题对照本版英文后原本正确；无＝本版不适用。F-024 的参数状态列表已重新完整阅读十一版，包括 `scram_iterations`、`search_path`、指针有效期与各自版本范围。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-LQS-001 主机名与端口信息生成失败的说明 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-002 PQhostaddr 的 NULL 与空字符串说明 | P3 | 无 | 无 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-003 PQtty 的唯一例外与始终为空返回值 | P3 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-004 PQoptions 是连接请求中传递的选项 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-005 PQstatus 保留本版状态常量标记 | P3 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 |
| C19-LQS-006 事务状态的有效事务块措辞 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-007 协议版本说明与旧版协议 2.0 范围 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 |
| C19-LQS-008 服务器版本号两位数字与次版本措辞 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-009 PQerrorMessage 漏译 functions | P3 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-010 错误消息可能含多行而非必然多行 | P2 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-011 错误消息索引补齐 PGconn 层级 | P3 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 |
| C19-LQS-012 PQsocket 的文件描述符编号 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-013 后端 PID 与 NOTIFY 通知的关系 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-014 后端 PID 可见索引未译 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-015 PQsslInUse 布尔返回值语序 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-016 旧版 PQsslAttribute 混入新版返回条件 | P2 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQS-017 PG14 混入 PG15 SSL 库探测整段 | P2 | 无 | 无 | 无 | 无 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQS-018 旧版 PQsslStruct 混入新版 NULL 条件 | P2 | 修 | 修 | 修 | 修 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQS-019 PQsslStruct 所请求对象与 SSL 实现的关系 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-020 PG14 OpenSSL 名称应保留同版引号结构 | P3 | 核 | 核 | 核 | 核 | 修 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQS-021 访问函数获取内容与内部字段术语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-022 连接与 PGconn 对象的生命周期表述 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-LQS-023 F024 参数状态列表与指针有效期重新全读 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-LQS-024 完整协议版本函数仅 PG18 起存在 | CHECK | 无 | 无 | 无 | 无 | 无 | 无 | 无 | 无 | 核 | 核 | 核 |
| C19-LQS-025 GSSAPI 认证状态函数仅 PG16 起存在 | CHECK | 无 | 无 | 无 | 无 | 无 | 无 | 核 | 核 | 核 | 核 | 核 |
| C19-LQS-026 SSL 属性 ALPN 仅 PG17 起存在 | CHECK | 无 | 无 | 无 | 无 | 无 | 无 | 无 | 核 | 核 | 核 | 核 |
| C19-LQS-027 SSL 属性名称扩展说明仅 PG16 起存在 | CHECK | 无 | 无 | 无 | 无 | 无 | 无 | 核 | 核 | 核 | 核 | 核 |

完整阅读覆盖 58 个英文条目变体及全部中文候选、9 个外层段落、1 个框架、259 个实际条目；32 个最终条目变体、5 个完整外层框架和 7 个返回条件精炼均已复读。270 个签名/代码块保留原样，除原有可读 C 注释翻译外，与本版英文精确相同。

十一版当前源码、审定稿、固定英文、原生解包英文及新解析快照一致，零漂移。29 个范围内结构提示均为既有 SSL 属性锚点，逐项核对属性名、相邻次序、父路径及完整 API 中英正文后保留。PG14 删除未来段落后遗留的一行空白已单独清理并记录；`git diff --check` 通过。

本批仅关闭 `libpq-status`。执行查询和 libpq 其余节继续校准；全书其他待读范围、历史证据对账和最终 33 项 HTML/A4/US 构建仍未完成。全书原始结构检查退出码仍为 PG10—12 的 3、PG13—20 的 1，不能报告为全书通过。

详细证据：[逐问题十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-status-full-issue-version-matrix.json)、[完整审定父块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-status-full-accepted-parent-plans.json)、[259 条目绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-status-full-accepted-entry-proof.json)、[新快照核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-status-native-current-snapshot-proof.json)、[29 条逐项处置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-status-native-dispositions.json)、[完整父块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/libpq-status-native-parent-proof.json)。
