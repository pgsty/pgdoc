PG10—PG20 earthdistance／seg／tablefunc 校准记录（2026-09-15）

从 PG18 开始，实际读完 26 个主分块、16 个完整英文变体和全部中文候选，覆盖 33 个完整模块文件。另读完 24 组关联内容、2 组补充内容、受信任扩展完整清单和两组 fillfactor 完整说明，合计 106 文件、126 范围，其中 93 个关联范围。28 个正文文件修订，规范仍为 647 条，九项用户回退保持。

修复两类确认问题：PG10—14 的 earthdistance 和 seg 标题混入新版副标题，10 处恢复自身英文短标题；十一版 tablefunc 将 44 处普通描述中的 extra 翻译为“额外”。SQL 列名 extra、extra_col、branch 以及所有函数、类型和输出不变。对 quoted extra 做十一版整树搜索，还核准了 PG14—20 CREATE INDEX 中 14 处原已正确的“额外空间／额外元组版本”，没有将关键词命中直接当作缺陷。

同源复用包括 PG10—13 两类 crosstab 返回声明，以及 PG10—16 psql 交叉表示例的引导句。保留所有原始块与版本差异。28 个文件分属 5 个 earthdistance、5 个 seg、11 个 tablefunc 和 7 个 psql。13 组最终译文全部复读，178 个原叶段同源组在增加关联清单后扩展为 184 组；没有未决同源冲突。保留 earthdistance 的 CREATE 权限标记和换行差异，不因有效格式差异重写正文。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-matrix.md)包含 25 组、275 格：32 修复／复用、206 核准、19 不适用、18 原文疑点。它记录每项的版本适用性和对应源码范围，不能当作全书完成率。

earthdistance 核准球面假设、cube 三维坐标和 earth 域、可调整的地球半径、180/pi() 度数单位、八个函数及包围盒的第二次精确检查。ll_to_earth 的参数是纬度在先、经度在后；point 表示则是经度在先、纬度在后。point 路径的距离单位固定为英里，改变 earth() 不影响该路径。极点与正负 180 度经度边界，以及安装依赖和整条搜索路径的受信任要求均逐版核对。

seg 核准区间、中心加减偏差、确定性标记、单端无界输入、下界大于上界的拒绝、32 位浮点数与有效数字、尾随零、GiST 操作符的端点公式、比较和排序。旧 @／~ 包含操作符说明保留于 PG10—13，PG14 移除说明另行核准。精度示例、已知边界和输入排序脚本按固定英文保留。

tablefunc 核准 normal_rand 的行数、均值和标准偏差；单参数 crosstab 的三列输入、连续分组、从左至右填充、缺值为 NULL、超额值跳过及 ORDER BY 1,2；N 包装函数和复合类型／OUT 参数示例；双参数类别查询的单列、非空、唯一要求、额外列从首行复制、忽略未匹配类别和缺值处理；connectby 的参数、返回类型、最大深度为零时不限深度、可选分支列和排序序号、标识符引号、分隔符与递归判断。没有执行 SQL 或示例程序。

关联 psql 核准纵横表头、可选排序列、默认列号、空单元格与重复组合报错；JSON 坐标样本、时区和 UTC 段落亦读完。历史发行条目覆盖超长 seg 输入、确定性标记输出、GiST 仅索引扫描、NULL 类别、负数行数、earthdistance SQL 标准函数体与升级行为，并保留各版自身提交链接。

1,452 个叶段、176 个父段、363 个原始块核准。全部原始块未改动：328 块与自身英文逐字节一致，22 块只有此前已译的两类 SQL 注释，12 块为已记录的 psql 提示符／行尾空格例外，1 块为原生 SGML 简写结束标签展开。保护标记的七个范围例外仅为既有 domain 术语显示和 CREATE 标签；25 个行内值例外仅为已有标签或声明换行。代码比较未据此放宽。

2,428 处源标记全部分拣：2,294 处渲染内容、35 处源码注释、99 处实体声明／包含引用。2,329 处绑定完整已读范围，33 条模块包含链实际解析。受信任清单里的 10 个 xref 单独绑定到完整清单，未误计为实体声明。

保留两类原文疑点：十一版 crosstab N 概要表写作 table_crosstab_N，详细示例写作 tablefunc_crosstab_N；PG10—16 的 psql 示例原文提示符为 testdb(，既有明确勘误已改为 testdb-，本次核准保留。它们不计为新翻译缺陷。

新快照 checkpoint-geometry-table-extensions-ready：十一版 4,894 节点精确绑定，36 条范围内提示全部核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。保留原始全书审计退出码；阶段结论仅覆盖列明范围。

前批诊断与认证提交 79971df 已核验。本批准备阶段提交；下一批 contrib 框架、SPI 扩展和 dict_int 已开始完整阅读，发现的旧版未来内容将继续逐版修复。全书余项、历史独立对账和十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-version-boundary-proof.json)、[源标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-all-occurrences-closure.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-source-inclusion-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-source-questions.json)、[extra 横扫](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-horizontal-defect-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-matrix.json)、[新快照](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geometry-table-extensions-full-reviewed-certificate.json)。
