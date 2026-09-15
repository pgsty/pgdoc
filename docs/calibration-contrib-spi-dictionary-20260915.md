PG10—PG20 contrib／SPI／dict_int 校准记录（2026-09-15）

以 PG18 为入口，实际读完 9 个主分块、19 个完整英文变体及全部中文候选，覆盖三个文件的十一版，共 33 个完整主文件。contrib.sgml 是两个附录的框架与模块包含清单，不将所包含的其他模块正文算入本批阅读。另读完 19 组关联内容、5 组补充内容和 14 组 serial 关联段落，共 126 个关联范围，其中包括 PG20 完整的 refint 过时页面。总计 127 文件、159 范围，25 正文文件修订。规范仍为 647 条，九项用户回退保持。

五类确认问题已逐版核对：

- CSD001：恢复 PG10—14 contrib 本版引言和短标题、PG10—15 包装说明中的“模块”、PG10—15 dict_int 短标题，以及 PG15 SPI 短标题。新版副标题和组件措辞保留在自身英文适用的版本。
- CSD002：PG14/15 混入未来的 20 项受信任扩展清单及新版组件说明。移除自身英文没有的清单，恢复旧版构建、模块注册、目标模式和预加载说明；CREATE EXTENSION 示例参数恢复为 module_name。PG16 起的清单保留。
- CSD003：移除 PG15/16 混入的嵌套 BEFORE 触发器警告；恢复 PG14—17 autoinc 覆盖插入值及可选更新行为。PG18 起的零值／NULL 判断、零值时再次调用 nextval 的说明，以及 PG18/19 的嵌套触发器警告，均按自身英文保留。
- CSD004：PG10—13 将 serial 类型名误译为“序列列”，按不翻译词表第 840 行恢复 serial。完整水平扫描 94 个相关段落，其中 11 个主模块段落和 83 个额外关联范围；其余原已正确的 serial、身份列、默认值、序列所属关系、RETURNING 与权限说明保留。
- CSD005：PG14—18 发行说明把 quoting key values 译成“引用键值”，改为“为键值加引号”。相关安全修复条目的完整段落和原始提交链接已逐版阅读。

25 个正文文件分属 6 个 contrib、6 个 dict_int、8 个 SPI 和 5 个发行说明。13 组最终译文全部复读；删除未来段落后引入的四个空白行尾随空格已在应用前清理。53 条正文变更记录不等于 53 个独立缺陷。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-matrix.md)共 26 组、286 格：21 修复、197 核准、56 不适用、12 原文疑点。矩阵记录各版检查结果，不是全书完成率。

contrib 核准 make／check／installcheck 的执行位置与时机、预打包子包、逐库 CREATE EXTENSION、template1、CREATE 权限、受信任规则、目标模式及非扩展模块加载方式；保留 PG10—12 FROM unpackaged、PG10 chkpass、PG10—13 pg_standby、PG14—16 old_snapshot、截至 PG16 的 adminpack 和各新版新增模块边界。两附录分工、客户端程序可在任意位置使用而服务器程序仅在服务器端使用，均依固定英文核准。

SPI 核准主键／外键检查的两侧、参数数量和顺序、模式安全、标识符引用、级联／限制／置空行为、NULL 与唯一索引；旧版 BEFORE、PG18/19 AFTER 时机及 PG20 refint 移除分别核准。PG10/11 timetravel 的 abstime 起止列、infinity、更新和删除如何结束有效期、可选用户列、会话级开关与返回值均读完。autoinc、insert_username 和 moddatetime 的列类型、触发事件及参数保持自身版本。

dict_int 核准 maxlen 默认 6、rejectlong 默认 false、超长词元截取前缀或忽略的区别；PG13 起 absval 先去除正负号再判断长度的规则；intdict_template／intdict、选项修改、测试和配置映射全部原样保护。未把现有有效的“文本检索”措辞当作缺陷。

574 个叶段、72 个父段和 116 个原始块核准。116 块均与自身英文逐字节一致，其中仅两块恢复 module_name，其他 114 块未变。159 个范围的保护标记、链接和源码注释一致；33 个行内值例外仅为既有 SCHEMA／BEFORE INSERT OR UPDATE／timestamp with time zone 换行。PG16—20 的 world 目标保留既有 quote 标签，共五个显式结构例外。两处未来清单 ID 的移除已检查十一版引用，不遗留悬空引用。

630 处模块源标记全部分拣：561 处渲染内容、25 处源码注释、44 处实体声明。586 处绑定完整已读范围，44 处实体声明逐版追溯到 contrib 包含行和完整模块。PG14—18 CVE 条目还核对了缓存旧键值、NULL 解引用和缓冲区相关修复说明，不根据关键词直接判缺陷。

保留两类固定英文疑点：十一版 dict_int 修改选项例子之后展示默认六位长度输出，本次按原文例子保留，未假称顺序执行通过；PG10 contrib 客户端引言有 “are that” 词序问题，中文保留意图。共 12 格，不计为新翻译缺陷。未执行 SQL、服务器命令或 C 示例。

新快照 checkpoint-contrib-spi-dictionary-ready：十一版 1,289 个节点精确绑定，12 条范围内提示全部核准，零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。共享工作区的关联文件发生过其他修改，已凭本批原范围逐字未变的证据更新偏移并保留对方工作；未声称阅读或提交这些无关修改。全书审计原始退出码保留，阶段结论仅覆盖列明范围。

上一批地理与表函数提交 9d8eeed 已核验。本批准备阶段提交，下一批 sepgsql 已开始完整逐版阅读。全书余项、历史 2,466 条绑定独立对账，以及十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-scope-proof.json)、[变更](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-protected-proof.json)、[结构](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-structure-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-version-boundary-proof.json)、[源标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-all-occurrences-closure.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-source-inclusion-proof.json)、[serial 横扫](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-horizontal-serial-proof.json)、[原文疑点](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-matrix.json)、[共享修改保留](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-unrelated-peer-refresh-2.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/contrib-spi-dictionary-full-reviewed-certificate.json)。
