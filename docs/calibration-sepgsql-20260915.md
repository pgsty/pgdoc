PG10—PG20 sepgsql 校准记录（2026-09-15）

从 PG18 开始，实际读完 16 个主分块、8 个完整英文变体和全部中文候选，覆盖 sepgsql 的 11 个完整模块文件。另读完 16 组关联内容、2 组补充内容，合计 47 文件、78 范围，其中 67 个关联范围。8 个正文文件修订，全部为 PG10—17 的 sepgsql.sgml。规范仍为 647 条，九项用户回退保持。

三类确认问题已水平核对十一版：

- SP001：PG10—15 混入新版模块长标题，恢复自身英文的短标题；PG16 起保留长标题。
- SP002：PG14—17 漏掉旧版回归测试必须手工调用脚本的说明，其中 PG14—16 还混入 PG18 的 PG_TEST_EXTRA 引言。恢复本版完整回归测试流程和链接；PG18—20 保留新入口及手工测试的区分。
- SP003：PG14—16 的外部资源链接使用了新版 SEPostgreSQL_Introduction 地址，恢复本版英文的 SEPostgreSQL 地址。仅核准固定英文链接的一致性，未把远端网站连通性算作验收。

同源复用包括 PG10—13 的数据库设置段落和 DML 权限示例说明，保留 PG10 自身 md5sum(y) 以及 PG11 起 func1(y) 的代码差异。矩阵只将产生最终正文变化的复用计作“修”；复原草稿后与最初正文相同的段落计作“核”。9 组最终译文全部复读，111 个叶段同源组、3 个父段组和 50 个其他组无未决冲突。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-matrix.md)共 23 组、253 格：21 修复／复用、191 核准、27 不适用、14 原文疑点。这些是明确范围的版本核验结果，不是全书完成率。

安装与测试核准 Linux／SELinux／libselinux／selinux-policy 的版本条件、预加载要求、逐库 sepgsql.sql 初始化与初始标签；测试所需策略包、系统域、免密码超级用户连接、测试开关及完成后的关闭／卸载。构建选项的直接文字与 PG17 起的 configure／meson 链接条目分别保留，PG13 起的策略开发包说明亦核对。

权限正文核准主体／对象标签、未标记对象、父对象与类型转换规则；DML 的表级／列级检查、WHERE／RETURNING 数据来源、视图展开、模式搜索、函数执行及入口权限、序列权限检查的限制；DDL 的创建、模板 getattr、模式 add_name／remove_name、列权限、LEAKPROOF install、CASCADE、附属对象和 relabelfrom／relabelto。保留禁止 LOAD、系统目录修改和 TOAST 表访问，以及 DDL／DCL、行级访问和隐蔽通道的实现限制。

受信任过程核准标签转换、受控访问和信用卡掩码示例；动态域转换核准 setcurrent／dyntransition、缩小权限、连接池通过受信任过程检查凭据后切换标签、NULL 恢复及凭据存储保护。五个函数的签名、返回类型、mcstrans 转换方向和恢复初始标签规则均核准，旧版两列表格与新版单列表格保持。

关联范围包含 SECURITY LABEL 标签提供者职责、设置和删除标签示例及完整“另见”列表；COPY PROGRAM 的操作系统限制；安装选项与 PG_TEST_EXTRA 配置项；历史缓存引用泄漏、测试兼容、弃用警告、TRUNCATE 权限控制、日志状态及 meson 安装位置修复的完整条目。所有自身提交链接、路径和非渲染注释保持。

897 个叶段、22 个父段和 164 个原始块核准。全部原始块未改动：161 块与自身英文逐字节相同；PG10—12 的三个输出块仅少了英文列标题 sepgsql_setcon 后的一个既存尾随空格，逐块实际比对并单列，不放宽其他代码比较。78 范围的保护标记、链接、源码注释和行内值精确核准，没有其他结构例外。未运行 SQL、SELinux 管理命令或回归脚本。

1,550 处源标记全部分拣：1,504 处渲染内容、13 处源码注释、33 处实体声明／包含。1,516 处绑定完整已读范围，1 条范围外源码注释单独核准，33 处实体引用解析到各版完整模块。

固定英文疑点保留：十一版动态域示例的初始输出含 c0.c1023，后续段落描述 c1.c1023；PG18—20 的测试引言有 to checks 语法问题。中文按固定英文含义保留，不计作新翻译缺陷，不声称示例已执行。

新快照 checkpoint-sepgsql-ready：十一版 2,201 节点精确绑定，31 条范围内提示全部核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书审计原始退出码保留，阶段结论仅覆盖列明范围。

上一批 contrib／SPI／dict_int 提交 37ef1b0f 已核验。本批准备阶段提交，下一批前言、约定、信息、法律声明、二进制安装与源码仓库说明已开始完整逐版阅读。全书余项、历史 2,466 条绑定独立对账，以及十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-version-boundary-proof.json)、[源标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-all-occurrences-closure.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-source-inclusion-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/sepgsql-full-reviewed-certificate.json)。
