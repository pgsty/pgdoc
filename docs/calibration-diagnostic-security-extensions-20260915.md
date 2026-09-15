PG10—PG20 sslinfo／passwordcheck／pg_logicalinspect／pg_overexplain 校准记录（2026-09-15）

从 PG18 开始，实际读完 12 个主分块、14 个完整英文变体及所有中文候选；覆盖 28 个完整模块文件。随后读完 30 组完整关联内容、7 组补充内容和全部同源候选，合计 92 文件、191 范围，其中 163 个关联范围。28 个正文文件修订，规范仍为 647 条，九项用户回退保持。

确认并修复两类问题。其一，cipher 被误译为用户密码：十一版 ssl_cipher() 返回值应为“密码套件名称”；十一版 ssl_ciphers 的 HIGH／MEDIUM 组说明应为“密码算法”，3DES 排序说明应为“密码套件”；PG14—17 的 TLS 1.3 限制也应为“密码套件”，而非“密码选择”。48 处修订分属十一版 sslinfo 和 config；同时完整核对 libpq、pg_stat_ssl、runtime 和 pgcrypto 相关上下文，按密码、密码算法、SSL 密码套件区分，真实标识符 cipher／ciphers 和命令保持。

其二，PG18 发行说明颠倒了模块和变量的关系，原译为“向 min_password_length 添加可配置变量 passwordcheck”，现恢复“向 passwordcheck 添加可配置变量 min_password_length”。十一版整树搜索得到 11 处变量名，其中一个是源码注释，所有可见用例均绑定到完整中英范围；PG18—20 参数正文原已正确，PG10—17 尚无此功能。

另复用三类已有同源译文：PG14 passwordcheck 的源代码修改说明、PG10—13 pgcrypto 的摘要与密码算法支持说明，以及十一版本批 SSL 参数的设置位置句。保留本版 OpenSSL 标签、CrackLib 网址、参数列表与代码。共 11 个 sslinfo、11 个 config、4 个 pgcrypto、1 个 passwordcheck 和 1 个 release-18 文件修订。没有为措辞偏好新增术语规则；密码算法和密码套件沿用已核准的 pgcrypto／libpq 同语境译文。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-matrix.md)包含 23 组、253 格：54 修复／复用、119 核准、69 不适用、11 原文疑点。11 组最终译文全部复读；3 组同源候选均已读，其中 auto_explain 的一组仅有既有换行差异并保留。134 个叶段同源组、5 个父段组和 89 个其他单元组没有未决冲突。

sslinfo 完整核对十个函数的签名、true／false、无 SSL 时多数函数返回 NULL、证书存在性、序列号与颁发者唯一标识证书而非所有者、CA 和中间 CA、DN 编码、SQL_ASCII 下 UTF-8 表示、字段缺失的 NULL、ASN1 字段名和证书扩展。固定文档的 --with-openssl 至 PG13，--with-ssl=openssl 自 PG14；TLSv1.3 示例自 PG14，root.crt 具体文件名仅 PG10。未从文档措辞变化推断 API 实际引入日期。

passwordcheck 核对 CREATE／ALTER ROLE、shared_preload_libraries 与重启、CrackLib 可选构建、预加密口令导致的检查限制，以及 PG18 起的 min_password_length 默认 8 字节、仅超级用户可改、会话内动态修改和预加密时无效。PG10—17 整棵中英文源树及实体声明已检查，pg_logicalinspect／pg_overexplain 没有文件或迁移内容，未把新模块补进旧版。

pg_logicalinspect 核对两个逻辑快照函数、pg_logical/snapshots、filename 错误行为、pg_read_server_files 权限和 GRANT、完整三类查询输出；PG19／20 的 0/00000000 与 PG18 的 0/0 各自保留。pg_overexplain 核对 LOAD／会话和共享预加载、DEBUG 每节点和每查询字段、禁用节点计数、Parallel Safe、extParam／allParam、六个 PlannedStmt 标记、执行器参数不包括用户预备语句参数、Parse Location、范围表与 RTI、继承展开、已删除子查询和类型限定显示。PG19／20 auto_explain 扩展选项的加载顺序和超级用户限制另行核对。

关联内容包括完整 SSL 参数和默认值清单、pg_stat_ssl 表行、libpq cipher 属性、pgcrypto 原始加密函数和源码来源表、密码算法提供程序及历史失败处理，以及 PG10 DH 参数升级、passwordcheck 钩子共存和 PG18 新扩展、RANGE_TABLE 输出修复等完整发行说明。48 处 cipher 误译全部有自身英文；全十一版当前中文针对已识别的四种错误短语搜索为零，该搜索仅用于复查修订，没有当作全书语义验收。

803 个叶段、41 个嵌套父段、61 个原始块核准。61 块全部保持不变，其中 60 块与本版英文逐字节相同；PG10 一块 synopsis 仅把原生 SGML 简写结束标签展开为完整标签。保护标记、链接属性和源码注释完全匹配；三个行内值例外是 PG18—20 的 Scan RTI／Exclude Relation RTI 标签既有换行。没有放宽代码或输出内容比较。

1,002 处源标记全部分拣：886 处渲染内容、32 处源码注释、84 处实体声明或包含引用；914 处绑定已读完整范围，4 处范围外源码注释与关联可见发行条目一并核准。28 条实际模块实体链和 16 个旧版缺席格均有独立证据。sslinfo 的原文证书字段列表十一版均重复 description，按固定源码保留并记录原文疑点；未据此擅改英文或运行 SQL、SSL 连接及示例程序。

新快照 checkpoint-diagnostic-security-extensions-ready：十一版 2,614 节点精确绑定，40 条范围内提示全部核准（15 个既有本地 ID、20 个已翻译表格行键及 5 组对应行匹配提示），零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。保留原始全书审计退出码，阶段结论仅覆盖列明范围。

上一批 lo／vacuumlo／tcn／UUID 提交 2e725ee 已核验。本批准备阶段提交；下一批 earthdistance／seg／tablefunc 已从 PG18 开始阅读。全书剩余语义范围、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-reread-proof.json)、[代码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-inline-literal-proof.json)、[版本及缺席边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-version-boundary-proof.json)、[源标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-all-occurrences-closure.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-source-inclusion-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-source-questions.json)、[变量横扫](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-horizontal-defect-proof.json)、[全部中文错误短语复查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-all-zh-cipher-pattern-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-certificate.json)。

表格键提示已逐行绑定到自身来源表，作者与代码来源列保持不变：[精确分类证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/diagnostic-security-extensions-full-reviewed-translated-table-key-proof.json)。
