PG10—PG20 数据库管理与表空间校准记录（2026-09-16）

从 PG18 开始，实际阅读十一版 manage-ag.sgml 以及 CREATE／ALTER／DROP TABLESPACE 的 33 个完整参考文件。管理数据库章节的七种完整英文变体、表空间命令的十五种完整英文变体和全部中文候选均已对照。另读 513 个完整相关范围，共 269 个文件、557 个范围、1,308 叶段、264 父段、359 原始块。

八类确认问题均水平核对十一版，并在全部适用位置修复：

- MA001：十一版管理数据库章的普通 database 索引词漏译，按既有第 120 条规则译为“数据库”。实际 DATABASE 关键字不变。
- MA002：十一版删除表空间的条件误写成移除相关数据库中的所有对象；改为移除“所有数据库中使用该表空间的对象”，并核对本版 DROP TABLESPACE、权限、系统信息和备份说明。
- MA003：PG10—16 的 pg_global 用途段混入未来的 only 限定，依自身英文移除“只”；PG17—20 保留。
- MA004：PG16 的手工调整表空间符号链接段漏掉 PostgreSQL 9.1 及更早版本还需更新 pg_tablespace，否则 pg_dump 继续输出旧位置的说明。已补齐，并在相同英文的 PG10—17 复用审定译文；PG18 起原文移除了该说明。
- MA005：PG14／15 CREATE TABLESPACE 漏掉“仅在支持符号链接的系统上受支持”注解，已补齐。该说明在 PG10—15 存在，从 PG16 起移除。
- MA006：PG13—17 CREATE／ALTER TABLESPACE 混入 PG18 的并发 I/O 数量说明，恢复本版“执行器的预取行为”。PG18—20 保留并发数量，但修正“由同名配置参数确定”同时限定读取代价估计和并发数量的关系。PG10—12 自身旧参数段单独核准。
- MA007：PG19／20 分区维护段把末尾链接前移，遗漏了独立 ATTACH PARTITION 术语及“更多细节”链接句，已按同源 PG17／18 完整段补回；保留自身两个代码块、锁模式和链接。
- MA008：PG13—20 CREATE／ALTER TABLESPACE 把“同一 I/O 子系统的其余部分”误说成“其他 I/O 子系统”，已修正。PG10—12 原义正确，并复用相同英文的审定参数说明。

本批改动 33 个正文文件，规范维持 653 条，九项用户回退保持。182 个跨标记正文组、204 个常规叶段组、37 个父段组、48 个其他组已核对；相同英文复用正文并保留本版原始块和链接，零未决冲突。两组既有行折行／本地锚点差异单独核准。最终 13 个新文本组实际复读，其中 12 组与前一次完整复读稿逐字相同，1 组是最后修正的配置限定范围。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-matrix.md)共 22 组、242 格：57 修复／复用、121 核准、41 不适用、19 例外、4 源文疑义。十一版 8,523 个中英文 SGML 文件的 1,533 处相关命中均绑定完整已读范围。其中九处“空值”候选反向核对了四种 acldefault 完整英文／中文变体，确认 NULL 默认权限语义正确。原始宽泛检索将“空”匹配到“表空间”的 3,245 处结果仅保留作过程记录，不作为完成依据。

359 个原始块全部不变：338 个与自身英文逐字节相同；7 个 PG10 原始块使用等价 replaceable 短结束标签；11 个 WITH ORDINALITY 示例只存在一行既有中文注释；3 个 PG14—16 oid2name 示例只存在一行等义英文注释。每条注释均按完整上下文和精确替换核验，其他命令、代码和输出字节一致。60 个既有本地 ID（含两处段内 anchor）及 4 处原文普通引号对应的中文 quote 标签均精确核准。示例未执行。

版本边界逐版保留：CURRENT_ROLE 从 PG14 起；maintenance_io_concurrency 从 PG13 起；旧版三个参数与新版四个参数不同；CREATE TABLESPACE 的目录存在要求和 mkdir／chown 示例从 PG12 起；ALTER TABLESPACE 的直接／间接角色成员资格与 PG16 起的 SET ROLE 条件不同。数据库模板、连接限制、权限复制、默认与临时表空间、表空间迁移、备份协议、物理存储、分区锁、临时文件、DROP OWNED 与 REASSIGN OWNED 的对象范围，以及关联发行说明的作者和本版链接，均依各自英文核准。

MA-SQ01：PG17—20 pg_walsummary 关于界限块的创建／截断条件说明存在表面疑义，忠实保留固定英文和已有译文，单独记录。这不算翻译缺陷，也未断言运行时行为错误。

新快照 checkpoint-manageag-ready：十一版 3,647 配对节点，62 处范围内提示全部精确归位，零未决、零漂移、零未解释子节点差异。其中两条集合提示只核准本批范围内的 ddl_command_start 锚点，其余十个范围外成员未被本批归类。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。这是解析核验，尚未进行本批的 HTML／PDF 构建。

前一字符集阶段已提交 62b31b02，未推送。本批随后单独阶段提交。历史原 2,466 待追溯单元上次核准 221、余 2,245，需在最终内容上重新对账；全书剩余章节的逐句校准、此前批次跨原始块及行内标记一致性复核、独立追溯和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-changes.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-all-occurrences-closure.json)、[跨标记分组](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-cross-markup-prose-groups.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-raw-proof.json)、[受保护值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-protected-proof.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-existing-local-ids-proof.json)、[引号及源文疑义](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-existing-quote-context-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-version-boundary-proof.json)、[包含链](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-source-inclusion-proof.json)、[术语复查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-post-apply-term-check.json)、[规范状态](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-norm-state.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-native-validation.json)、[提示归类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/manageag-full-reviewed-certificate.json)。
