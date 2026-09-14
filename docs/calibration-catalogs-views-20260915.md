PG10—PG20 系统目录与系统视图校准记录（2026-09-15）

十一版的系统目录与系统视图已完成全章中英文对照、正文修复、横向一致性复核和修复后新快照原生核验。PG10—14 的视图仍在各自 catalogs.sgml 中，PG15—20 保留独立 system-views.sgml；17 个文件在原目录更新。此前提交的 pg_index/pg_proc 两节此次只做回归核对。

本批读取范围为 1,092 个完整节、10,416 个表行、2,642 个表外段落、199 个列表项；另完整核对表头、标题、索引词、节框架、外围正文和示例。先读 PG18，再逐版读取不同英文与全部中文候选；相同内容复用已读文本，差异通过完整单元或无省略差异复核。1,281 组表行正文与 1,335 个中文候选全部读完；修订译文经过单独复读。

修复集中在以下问题，每项均与 PG10—PG20 自身英文核对后确定适用范围：

- 版本内容串入：PG14 恢复两类 PIN 依赖及零值说明；PG14—16 删除未来 INITACL、默认权限大对象类型、时区额外条件，补回 convalidated 的外键/CHECK 限定；PG14 恢复序列 last_value 的两个 NULL 条件、共享内存读取权限、参数上下文权限与自定义参数段落顺序。
- 对象与依赖方向：修正依赖对象和被引用对象、事件与触发器、统计信息对象所在表、外部服务器/用户映射选项、权限对象、操作符与操作数位置等关系。
- 条件和数量：仅偶数枚举 OID 保证顺序；排序值在各自枚举类型内唯一；名字空间与编码组合唯一；数组长度、统计直方图分组数量、频率比例、附加值位置、范围上下界均按原文校准。
- NULL 与存储：区别 SQL NULL、空字符串、空数组、空表达式树和 C 字符串的空字符；typstorage 同时说明能否使用 TOAST 与默认策略，保留线外存储及原关系的 TOAST 关系条件。
- 复制与事务：订阅本身进行复制、槽向备库同步、表复制完成/就绪状态、复制源、提交记录刷盘、lost 槽状态、事务已经处于预备提交状态，均纠正歧义并保留各版本独有状态。
- 术语和可见文字：恢复 heap 访问方法名；统一操作符、宽松策略、求反器、字段、类型修饰符、受信任、缓存、hash 表等用语；补译 typcategory Codes 标题和物化视图索引词。

PG12—16 的 adbin 及相关引言按固定英文只描述默认值，不能据此断言这些版本没有生成列功能。PG15+ 的固定对象段、PG17+ 的 INITACL、PG18+ 的大对象默认权限类型等本版内容保留。PG19/20 的属性图、序列复制等独有字段与语义逐版核对。

358 组校准和回归项形成 3,938 格：2,043 格修订、306 格原已正确、494 格不适用、3 格删除未来条目、1,092 格完整节回归。238 条原始阅读观察含重复记录、术语疑问和非缺陷，均保留逐条处置及十一版证据，不能当作 238 个独立缺陷。

65 个节的结构计数差异均为准确的既有 NULL、WITH CHECK、synced、ACL 等行内包装，没有借计数差异删除合法标记。同源文本只保留 typstorage 一处语义等价、原有行内标签顺序不同的引言。仅三个随未来 INITACL 条目删除的本地 ID 被移除，已确认无剩余引用。36 个实际示例位置与各版英文一致，程序内容逐字保持原样；19 行新增行尾空白已清理，差异检查通过。

固定英文疑点单独保留，包括复合唯一索引的 NULL 描述、parser 的 lexemes 用词、multirange 示例注释等；未把源文疑点误记成翻译已修复，也未静默更改固定英文。

十一版修复后新快照核验中，74 条范围内既有 ID 提示逐项绑定到审定条目，零未决、零漂移。当前源码、审定稿、新快照、固定英文与解包英文精确对应。仅 checkpoint-catalogs-views-clean 用于最终本批验收；此前快照先于空白清理，不作为当前源码验收。整书审计仍保留 PG10—12 退出码 3、PG13—20 退出码 1，反映其余章节的待处理信号。

此前已提交的 libpq、协议、大对象、ECPG、information_schema、CREATE DOMAIN、多项表 DDL 及 pg_index/pg_proc 修复见[累计阶段记录](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)。CREATE TABLE 整页及其余章节继续逐版校准。全书最终对账、十一版 HTML 与 A4/US PDF 共 33 项最终构建仍未完成；本批原生核验不能代替构建验收。

证据：[完整十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-matrix.md)、[矩阵原始数据](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-issue-version-matrix.json)、[238条阅读观察逐项处置](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-human-observation-dispositions.json)、[审定完整节](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-parent-plans.json)、[完整校准证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-certificate.json)、[新快照原生核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-native-validation.json)、[全部提示逐项绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/catalogs-views-clean-native-classification.json)。
